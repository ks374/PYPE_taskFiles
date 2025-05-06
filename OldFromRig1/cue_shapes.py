import sys,types, math
from pype import *
from events import *
from Tkinter import *



def createB8stim(myWidth, myLength, myFB, myColor,myX, myY, myBG, coords,line_width):
    s = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
    s.fill(myBG)    

    s.polygon(myColor, coords, line_width)
    s.myColor = myColor
    return s

def createB8dots(myWidth, myLength, myFB, myColor,myX, myY, myBG, coords,radius,perispace,d_coords,seg_length,line_width):
    ####  POINT SELECTION #####
    
    # slice out first element, which is last point repeated at beginning)
    coords=list(coords) 
    n=len(coords)
    coords= coords[1:n]
    #coords should be list of 2 element lists"

    # oridistance= list of distances from origin used to pick maxima that define segments
    oridistance=[]
    for (x1,y1) in coords:
        distance=(x1**2 + y1**2)**(1.0/2.0)
        oridistance.append(distance)
   
    # doridp= numerical derivative of oridistance
    n=len(oridistance)
    doridp=[]
    doridp.append((-3.0*oridistance[0] + 4.0*oridistance[1] - oridistance[2]) / 2.0)  # first point
    for jj in arange(n)[1:n-1]: # center difference for midpoints
        doridp.append((oridistance[jj+1] - oridistance[jj-1]) / 2.0)
    doridp.append((3.0*oridistance[-1] - 4.0*oridistance[-2] + oridistance[-3]) / 2.0)  
    
    # d2oridp= second derivative of oridistance
    n=len(oridistance)
    d2oridp=[]
    d2oridp.append((-3.0*doridp[0] + 4.0*doridp[1] - doridp[2]) / 2.0)  # first point
    for jj in arange(n)[1:n-1]: # center difference for midpoints
        d2oridp.append((doridp[jj+1] - doridp[jj-1]) / 2.0)
    d2oridp.append((3.0*doridp[-1] - 4.0*doridp[-2] + doridp[-3]) / 2.0)
   
    # zero crossing indices. (oridistance maxima go from positive doridp to negative doridp)
    counter=0
    temp_ind=[]
    for jj in doridp[0:-1]:
        if jj >= 0:
            if doridp[counter+1] < 0:
               temp_ind.append(counter)
        counter=counter+1
    # then looks between first and last
    if doridp[-1] > 0:
        if doridp[0] < 0:
            temp_ind.append(0)   

    
    # discards based on arbitrary (hand-tuned) threshold value of second derivative
    # tried 10**-3 (too big) but no values between this and current 10**-4
    temp_ind2=[]
    d2thresh= 10.0**(-4.0) 
    for jj in temp_ind:
        if abs(d2oridp[jj]) > d2thresh:
            temp_ind2.append(jj)
    
    # for things w/o local maxima (like circles), start at 1 for defining segment endpoints
    if len(temp_ind2)==0:
        temp_ind2.append(0)
    temp_ind2.sort()

       
    # shift coords so that first index is 1 and first element of coords is a segment end (prevents wrapping issues)
    coords2=coords[temp_ind2[0]:]
    coords2.extend(coords[0:temp_ind2[0]])  
    running_shift_counter1= temp_ind2[0]
    temp_ind2= list(asarray(temp_ind2)- temp_ind2[0])

    # peridistance= list of distances around perimeter in this new segment-defined ref frame 
    coords2.append(coords2[0]) #append first element to end so dont need to wrap, later remove
    peridistance=[]
    counter=0
    for (x1,y1) in coords2[:-1]:   #indexing so that don't get last 
        x2=coords2[counter+1][0]
        y2=coords2[counter+1][1]
        distance=(((x2 - x1)**2.0) + ((y2-y1)**2.0))**.50
        peridistance.append(distance)
        counter= counter+1
    del coords2[-1]               # note i had some issues here w/ 'list.remove' that were strange.
      
    # for each segment, perimeter stepping, adaptive point pick, add indices to global(all segs)list
    g_pindex=[]
    g_distances=[]
    g_perispace=[]
    bufvert= coords2
    ind= temp_ind2
    num_segs=len(ind)
    
    # loop through segments
    for cc in range(0,num_segs):
        segstart=ind[cc]
        if cc == num_segs-1:
            segend= len(bufvert)-1
        else:
            segend= ind[cc+1]
        segment_length=sum(peridistance[segstart:segend+1]) #added +1 b/c slice doesn't include endpoint
        numpoints=round(segment_length /perispace)
        perispace= segment_length/numpoints
        
        # for each segment, do perimeter stepping thing
        count=0
        distances=[]
        pindex=[]
        for dd in range(segstart,segend+1):
            if len(distances)+1 == numpoints:       # special case for last point
                distances.append(sum(peridistance[dd:segend+1])+ count)
                pindex.append(segend)
                count=0
                break
            count= count + peridistance[dd] # peridistance is in shifted bufvert ref frame   
            if count > perispace:
                prev_count= count- peridistance[dd];
                
                if len(distances)==0:
                    distances.append(count)
                    pindex.append(dd)
                    count=0
                elif (sum(distances))/len(distances)> perispace:
                    distances.append( prev_count)
                    pindex.append(dd-1)
                    count= peridistance[dd]
                else:
                    distances.append(count)
                    pindex.append(dd)
                    count=0
        g_pindex.extend(pindex)
        g_distances.extend(distances)
        g_perispace.append(perispace)
	coords3=[]    
    for dummy in g_pindex:     
        coords3.append(bufvert[dummy])
    coords=coords3
    numcues=len(coords)

    # SPRITE CREATION
    #segcolor=(255,1,1)  # FOR DEBUGGING
    s = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
    s.fill(myBG)    
    s.pdots(myColor,coords,radius)#segmentverts,segcolor)
    s.myColor = myColor


   # shift d_coords by running shift counter (so it aligns with indices we've been building)
    d_coords=list(d_coords)
    d_coords2= d_coords[running_shift_counter1:]
    d_coords2.extend(d_coords[0:running_shift_counter1])  
    d_coords3=[]
    for dummy in g_pindex:
        d_coords3.append(d_coords2[dummy])
    # get derivative (dy/dx) at all of our selected points
    dydx_peri=[]
    for (dx,dy) in d_coords3:
        if dx==0:
            dydx='Inf'
        else:
            dydx= dy/dx
        dydx_peri.append(dydx)
    # orthogonal lines at each point
    numlines=len(coords)
    oline_coords=[]
    for bb in range(numlines):
        if dydx_peri[bb]=='Inf':
            xr=seg_length/2.0
            x1=coords[bb][0]+xr 
            x2=coords[bb][0]-xr
            y1=coords[bb][1]
            y2=coords[bb][1]
            oline_coords.append([(x1,y1),(x2,y2)])
        else:
            pre_theta= arctan(dydx_peri[bb])
            theta= pre_theta + pi/2.0
            xr= cos(theta)* seg_length/2.0
            yr= sin(theta)* seg_length/2.0
            x1=coords[bb][0] - xr
            x2=coords[bb][0] + xr
            y1=coords[bb][1] - yr
            y2=coords[bb][1] + yr
            oline_coords.append([(x1,y1),(x2,y2)])


   # SPRITE CREATION
    
    s5 = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
    s5.fill(myBG)    
    s5.tlines(myColor,oline_coords,line_width)
    s5.myColor = myColor
    

    return s,s5,numcues





### FUNCTION FOR TANGENTIAL LINES ALONG PERIMETER... A LOT OF OVERLAP WITH ABOVE
def createB8tlines(myWidth, myLength, myFB, myColor,myX, myY, myBG, coords,radius,perispace,d_coords,seg_length,line_width):
    ####  POINT SELECTION #####
    # slice out first element, which is last point repeated at beginning CHECK THIS (worked in matlab)
    coords=list(coords) 
    n=len(coords)
    coords= coords[1:n]
    #coords should be list of 2 element lists"
    # oridistance= list of distances from origin used to pick maxima that define segments
    oridistance=[]
    for (x1,y1) in coords:
        distance=(x1**2 + y1**2)**(1.0/2.0)
        oridistance.append(distance)
    # doridp= numerical derivative of oridistance
    n=len(oridistance)
    doridp=[]
    doridp.append((-3.0*oridistance[0] + 4.0*oridistance[1] - oridistance[2]) / 2.0)  # first point
    for jj in arange(n)[1:n-1]: # center difference for midpoints
        doridp.append((oridistance[jj+1] - oridistance[jj-1]) / 2.0)
    doridp.append((3.0*oridistance[-1] - 4.0*oridistance[-2] + oridistance[-3]) / 2.0)  
    # d2oridp= second derivative of oridistance
    n=len(oridistance)
    d2oridp=[]
    d2oridp.append((-3.0*doridp[0] + 4.0*doridp[1] - doridp[2]) / 2.0)  # first point
    for jj in arange(n)[1:n-1]: # center difference for midpoints
        d2oridp.append((doridp[jj+1] - doridp[jj-1]) / 2.0)
    d2oridp.append((3.0*doridp[-1] - 4.0*doridp[-2] + doridp[-3]) / 2.0)
   # zero crossing indices. (oridistance maxima go from positive doridp to negative doridp)
    counter=0
    temp_ind=[]
    for jj in doridp[0:-1]:
        if jj >= 0:
            if doridp[counter+1] < 0:
               temp_ind.append(counter)
        counter=counter+1
    # then looks between first and last
    if doridp[-1] > 0:
        if doridp[0] < 0:
            temp_ind.append(0)   
    # discards based on arbitrary (hand-tuned) threshold value of second derivative
    # tried 10**-3 (too big) but no values between this and current 10**-4
    temp_ind2=[]
    d2thresh= 10.0**(-4.0) 
    for jj in temp_ind:
        if abs(d2oridp[jj]) > d2thresh:
            temp_ind2.append(jj)
    # for things w/o local maxima (like circles), start at 1 for defining segment endpoints
    if len(temp_ind2)==0:
        temp_ind2.append(0)
    temp_ind2.sort()

    # FOR DEBUGGING, PLOT COORDINATES AT SEGMENT ENDS,held in segmentverts passed to sprite.py
    segmentverts=[]
    for dummy in temp_ind2:     
        segmentverts.append(coords[dummy])
   
    # shift coords so that first index is 1 and first element of coords is a segment end (prevents wrapping issues)
    coords2=coords[temp_ind2[0]:]
    coords2.extend(coords[0:temp_ind2[0]])   # this has to be extend. checked in editor..seems good
    running_shift_counter= temp_ind2[0] # note that positive value is leftward shift
    temp_ind2= list(asarray(temp_ind2)- temp_ind2[0])
         
    # peridistance= list of distances around perimeter in this new segment-defined ref frame 
    coords2.append(coords2[0]) #append first element to end so dont need to wrap, later remove
    peridistance=[]
    counter=0
    for (x1,y1) in coords2[:-1]:   #indexing so that don't get last 
        x2=coords2[counter+1][0]
        y2=coords2[counter+1][1]
        distance=(((x2 - x1)**2.0) + ((y2-y1)**2.0))**.50
        peridistance.append(distance)
        counter= counter+1
    del coords2[-1]               # note i had some issues here w/ 'list.remove' that were strange.
      
    #MAJOR DIFFERENCE IN POINT PICKING BETWEEN PDOTS AND TLINES IS HERE.
    # offset segment indices by 1/2 phase shift,
    offset_ind=[]
    for zz in range(len(temp_ind2)):
        offset_count=0
        for ee in range(len(peridistance)):
            offset_count= offset_count + peridistance[ee+temp_ind2[zz]]
            if offset_count >= perispace/2.0:
                offset_ind.append(temp_ind2[zz]+ee)
                break
    offset_ind.sort()
    temp_ind3=offset_ind
        
    #  then realign temp_ind,coords2,and peridistance
    coords3=coords2[temp_ind3[0]:]
    coords3.extend(coords2[0:temp_ind3[0]])   # this has to be extend. checked in editor..seems good
    peridistance2= peridistance[temp_ind3[0]:]
    peridistance2.extend(peridistance[0:temp_ind3[0]])
    running_shift_counter= running_shift_counter + temp_ind3[0]
    temp_ind3= list(asarray(temp_ind3)- temp_ind3[0])
    peridistance=peridistance2
    
   # for each segment, perimeter stepping, adaptive point pick, add indices to global(all segs)list
    g_pindex=[]
    g_distances=[]
    g_perispace=[]
    bufvert= coords3
    ind= temp_ind3
    num_segs=len(ind)
    
    # loop through segments
    for cc in range(0,num_segs):
        segstart=ind[cc]
        if cc == num_segs-1:
            segend= len(bufvert)-1
        else:
            segend= ind[cc+1]
        segment_length=sum(peridistance[segstart:segend+1]) #added +1 b/c slice doesn't include endpoint
        numpoints=round(segment_length /perispace)
        perispace= segment_length/numpoints
        
        # for each segment, do perimeter stepping thing
        count=0
        distances=[]
        pindex=[]
        for dd in range(segstart,segend+1):
            if len(distances)+1 == numpoints:       # special case for last point
                distances.append(sum(peridistance[dd:segend+1])+ count)
                pindex.append(segend)
                count=0
                break
            count= count + peridistance[dd] # peridistance is in shifted bufvert ref frame   
            if count > perispace:
                prev_count= count- peridistance[dd];
                
                if len(distances)==0:
                    distances.append(count)
                    pindex.append(dd)
                    count=0
                elif (sum(distances))/len(distances)> perispace:
                    distances.append( prev_count)
                    pindex.append(dd-1)
                    count= peridistance[dd]
                else:
                    distances.append(count)
                    pindex.append(dd)
                    count=0
        g_pindex.extend(pindex)
        g_distances.extend(distances)
        g_perispace.append(perispace)
    coords3=[]    
    for dummy in g_pindex:     
        coords3.append(bufvert[dummy])
    coords=coords3

    # shift d_coords by running shift counter (so it aligns with indices we've been building)
    d_coords=list(d_coords)
    d_coords2= d_coords[running_shift_counter:]
    d_coords2.extend(d_coords[0:running_shift_counter])  
    d_coords3=[]
    for dummy in g_pindex:
        d_coords3.append(d_coords2[dummy])
    # get derivative (dy/dx) at all of our selected points
    dydx_peri=[]
    for (dx,dy) in d_coords3:
        if dx==0:
            dydx='Inf'
        else:
            dydx= dy/dx
        dydx_peri.append(dydx)
    # tangent lines at each point
    numlines=len(coords)
    line_coords=[]
    for bb in range(numlines):
        if dydx_peri[bb]=='Inf':
            x1=coords[bb][0]
            x2=coords[bb][0]
            yr=seg_length/2.0
            y1=coords[bb][1] - yr
            y2=coords[bb][1] + yr
            line_coords.append([(x1,y1),(x2,y2)])
        else:
            theta= arctan(dydx_peri[bb])
            xr= cos(theta)* seg_length/2.0
            yr= sin(theta)* seg_length/2.0
            x1=coords[bb][0] - xr
            x2=coords[bb][0] + xr
            y1=coords[bb][1] - yr
            y2=coords[bb][1] + yr
            line_coords.append([(x1,y1),(x2,y2)])
    

            
    # SPRITE CREATION
    #segcolor=(255,1,1)  # FOR DEBUGGING
    s = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
    s.fill(myBG)    
    s.tlines(myColor,line_coords,line_width)
    s.myColor = myColor

##     oline_coords=[]
##     for bb in range(numlines):
##         if dydx_peri[bb]=='Inf':
##             xr=seg_length/2.0
##             x1=coords[bb][0]+xr 
##             x2=coords[bb][0]-xr
##             y1=coords[bb][1]
##             y2=coords[bb][1]
##             oline_coords.append([(x1,y1),(x2,y2)])
##         else:
##             pre_theta= arctan(dydx_peri[bb])
##             theta= pre_theta + pi/2.0
##             xr= cos(theta)* seg_length/2.0
##             yr= sin(theta)* seg_length/2.0
##             x1=coords[bb][0] - xr
##             x2=coords[bb][0] + xr
##             y1=coords[bb][1] - yr
##             y2=coords[bb][1] + yr
##             oline_coords.append([(x1,y1),(x2,y2)])
##     # SPRITE CREATION
    
##     s2 = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
##     s2.fill(myBG)    
##     s2.tlines(myColor,oline_coords,line_width)
##     s2.myColor = myColor
    

    return s,numlines




# note that bar is used for blank creation. worth keeping. none of the other shapes are used.
def createBar(myWidth, myLength, myFB, myColor, myRot, myX, myY,myBG):
    s = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1) 
    s.fill(myColor)
    s.rotate(myRot, 0, 1)
    s.myColor = myColor
    return s


