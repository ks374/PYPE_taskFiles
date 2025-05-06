#!/usr/bin/python
# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-


# Standard modules that are imported for every task.
import sys, types
from sprite import *
from Numeric import *
from random import *
#this is the stimulus module -- sends in the stimulus vertices and the order
import b8stim_new as SV

#### first intialize general params

sqr = 0
circ = 0

h = 200 #height and width of encompassing rectangle #### this is equivalent to RF diameter in our system
bg_during = (255,255,255)
sqr_color = (255,255,255)
sizeCoef = 1

## stim specific params
stmclr = (255,0,0)
oclclr = (0,0,255)
ocl_r = 0.5
#ocl_th is variable
ocl_siz = 1.0
ocl_asp = 0.5



dir_name = "aim2images"
filepre = "stim_"
filepost = ".tif"
dir_sep = "/"

fb = quickinit(dpy=":0.0", w=3*h, h=3*h, bpp=32, flags=0)

#Calculate stimulus eccentricity and then figure out stimulus size
#in pixels

xt1 = (SV.Xarr*h/SV.spritesize)+0.5
yt1 = (SV.Yarr*h/SV.spritesize)+0.5
xv1 = xt1.tolist()
yv1 = yt1.tolist()
	
#####################################################
#Create the stimuli
stimid = SV.stmlist
rotid = SV.rotlist
### this is with no occluder, no mode
occl =[0]*len(stimid)
mode = [0]*len(stimid)
ocl_th = [0]*len(stimid)

###Then set up the occluder and mode buffers for show occl
occlstm = range(1,7)
occl1 = occlstm*len(stimid)
occl1.sort()
stimid1 = stimid*len(occlstm)
rotid1 = rotid*len(occlstm)
#next mode
mode1 = [1,2]*len(stimid1)
mode1.sort()
stimid1 = stimid1*2
rotid1 = rotid1*2
occl1 = occl1*2
#then ocl_th
ocl_th1 = SV.rots.tolist()*len(stimid1)
ocl_th1.sort()
stimid1 = stimid1*len(SV.rots.tolist())
rotid1 = rotid1*len(SV.rots.tolist())
occl1 = occl1*len(SV.rots.tolist())
mode1 = mode1*len(SV.rots.tolist())

#Now pattern occluders
occlstm = range(7,22)
occl2 = occlstm*len(stimid)
occl2.sort()
stimid2 = stimid*len(occlstm)
rotid2 = rotid*len(occlstm)
#next mode
mode2 = [1,2]*len(stimid2)
mode2.sort()
stimid2 = stimid2*2
rotid2 = rotid2*2
occl2 = occl2*2
ocl_th2 = [0]*len(occl2)

####Now all stimuli
occlstm = range(1,22)
stimid = stimid+stimid1+stimid2+[0]*len(occlstm) # this third entry is for occluder alone
rotid = rotid+rotid1+rotid2+[0]*len(occlstm)
occl = occl+occl1+occl2+occlstm
mode = mode+mode1+mode2+[3]*len(occlstm)
ocl_th = ocl_th+ocl_th1+ocl_th2+[0]*len(occlstm)

# Now create and display as you go

scount = 0
while scount < len(stimid):
	# create a sprite that is the same as the fb
	dlist = DisplayList(fb)
	s = Sprite(h*1.5, h*1.5, fb=fb, centerorigin=1)
	# fill the square with bg color
	s.fill(bg_during)
	if stimid[scount] != 0:
		coords = transpose(reshape(concatenate([xv1[stimid[scount]-1][0:SV.nvrt[stimid[scount]-1]*50],\
													yv1[stimid[scount]-1][0:SV.nvrt[stimid[scount]-1]*50]]),\
									   (2,50*SV.nvrt[stimid[scount]-1])))
		s.polygon(stmclr, coords, width=0)
		s.rotate(360-rotid[scount],preserve_size=0)
	dlist.add(s)
	#####Draw an occluder if needed
	if occl[scount] != 0:
		if mode[scount] == 2:
			occlclr = bg_during
		else:
			occlclr = oclclr
		if occl[scount] < 7: # this is for rectangle/ellipse/diamond occluders
			cx = cos(pi*ocl_th[scount]/180.0)*ocl_r*h/2.0
			cy = sin(pi*ocl_th[scount]/180.0)*ocl_r*h/2.0
			rotdeg = ocl_th[scount]+((occl[scount]-1)/3)*90
			occlshape =(occl[scount]-1)%3+1 #(1:rect, 2:ellipse; 3:diamond)
			rect_ht = ocl_siz*h/2.0
			rect_width = rect_ht*ocl_asp
			o = Sprite(int(rect_width), int(rect_ht), cx, cy, fb=fb, centerorigin=1)
			o.fill(bg_during+(0,)) # make sprite transparent
	        #draw the appropriate occluder
			if occlshape == 1: # draw a rectangle
				o.fill(occlclr+(255,))
			elif occlshape == 2: # draw an ellipse
				o.ellipse(occlclr+(255,), rect_width, rect_ht, 0, 0)
			elif occlshape == 3: # draw a diamond
				verts = [[rect_width/2.0,0],[0,rect_ht/2.0],[-rect_width/2.0,0],[0,-rect_ht/2.0]]
				o.polygon(occlclr+(255,), verts)
			o.rotate(360-rotdeg, preserve_size=0)

		else:
			rotdeg = ((occl[scount]-7)%5)*45
		    #patrnshape 1 = lines; 2 dots
			if (occl[scount]-7)%5 == 4:
				patrnshape = 2
			else:
				patrnshape = 1
			patrnwidth =(occl[scount]-7)/5+1 #(1:low width; 2: medium; 3: high)

			spriteclr = bg_during
			spriteh = h*ocl_siz
			spritew = h*ocl_siz
			occlrot = rotdeg
			numlines = 9 #keep this odd
			numdots = 81
			numarcs = 49
			o = Sprite(int(spritew), int(spriteh), fb=fb, centerorigin=1)
			o.fill(spriteclr+(0,)) # make sprite transparent
			spacing = spriteh/float(numlines)
			w = (spacing/6.0)*patrnwidth# dia of circles/arc width/linewidth
	        #draw the appropriate occluder
			if patrnshape == 1: # draw parallel lines
				for i in range(numlines):
					o.rect(0, -spacing*(numlines-1)/2.0+spacing*i, spritew, w, occlclr+(255,))
				o.rotate(360-occlrot, preserve_size=0)
			elif patrnshape == 2: # draw random dots
				for i in range(int(sqrt(numdots))):
					xpos = -spacing*(sqrt(numdots)-1)/2.0+spacing*i
					for j in range(int(sqrt(numdots))):
						ypos = -spacing*(sqrt(numdots)-1)/2.0+spacing*j
				        #random xy jitter
						rndx = int(spacing*(random()-0.5)/2.0)
						rndy = int(spacing*(random()-0.5)/2.0)
						o.circlefill(occlclr+(255,),int(w), int(xpos+rndx), int(ypos+rndy))
			elif patrnshape == 3: # semicircular arcs of random orientation
				for i in range(int(sqrt(numarcs))):
					xpos = -spacing*(sqrt(numarcs)-1)/2.0+spacing*i
					for j in range(int(sqrt(numarcs))):
						ypos = -spacing*(sqrt(numarcs)-1)/2.0+spacing*j
				        #random start angle
						rndx = int(spritew*(random()-0.5)/2.0)
				        #	rndy = int(spriteh*(random()-0.5)/2.0)
				        #rand start ang
						rnd_start = random()*2*pi
						o.arc(occlclr+(255,),int(4.0*w),int(4.0*w),xpos,ypos,rnd_start,rnd_start+pi,width=2)	
	if occl[scount]!=0:
		dlist.add(o)
	dlist.update()
	fb.flip()
	imageName = "%s%s%s%02d_r%d_o%d_th%d_m%d%s" % (dir_name,dir_sep,filepre,\
						stimid[scount],rotid[scount],occl[scount],ocl_th[scount],mode[scount],filepost)
	fb.snapshot(imageName)
	dlist.delete(s)
	if occl[scount]!=0:
		dlist.delete(o)
	dlist.update()
	fb.flip()
	scount = scount+1

del fb
sys.stdout.write('>>'); sys.stdin.readline()

def draw_occl(app, spritex, spritey, spriteclr, spriteh, spritew, occlshape, occlclr, occlrot):				
	"""
	This function creates a sprite with an occluder that's a rect, ellipse or diamond.
	The rest of the sprite surface is transparent
	"""
	occl_sprite = Sprite(int(spritew), int(spriteh), spritex, spritey, fb=app.fb, depth=1, on=0, centerorigin=1)
	occl_sprite.fill(spriteclr+(0,)) # make sprite transparent
	#draw the appropriate occluder
	if occlshape == 1: # draw a rectangle
		occl_sprite.fill(occlclr+(255,))
	elif occlshape == 2: # draw an ellipse
		occl_sprite.ellipse(occlclr+(255,), spritew, spriteh, 0, 0)
	elif occlshape == 3: # draw a diamond
		verts = [[spritew/2.0,0],[0,spriteh/2.0],[-spritew/2.0,0],[0,-spriteh/2.0]]
		occl_sprite.polygon(occlclr+(255,), verts)
	print occlrot
	occl_sprite.rotate(360-occlrot, preserve_size=0)
	return occl_sprite

def draw_patrn(app, spritex, spritey, spriteclr, spriteh, spritew, patrnshape, patrnwidth, occlclr, occlrot):
	"""
	This function creates and returns a pattern occluder sprite. Parallel lines, random dots 
	and arcs are the three options. Rest of the sprite is transparent
	"""
	numlines = 9 #keep this odd
	numdots = 81
	numarcs = 49
	patrn_sprite = Sprite(int(spritew), int(spriteh), spritex, spritey, fb=app.fb, depth=1, on=0, centerorigin=1)
	patrn_sprite.fill(spriteclr+(0,)) # make sprite transparent
	spacing = spriteh/float(numlines)
	w = (spacing/6.0)*patrnwidth# dia of circles/arc width/linewidth
	#draw the appropriate occluder
	if patrnshape == 1: # draw parallel lines
		for i in range(numlines):
			patrn_sprite.rect(0, -spacing*(numlines-1)/2.0+spacing*i, spritew, w, occlclr+(255,))
		patrn_sprite.rotate(360-occlrot, preserve_size=0)
	elif patrnshape == 2: # draw random dots
		#	for i in range(numdots):
		#		rndx = int(spritew*(random()-0.5)/2.0)
		#		rndy = int(spriteh*(random()-0.5)/2.0)
		#		patrn_sprite.circlefill(occlclr+(255,),int(w),rndx,rndy)
		#trying pseudorandom dots
		for i in range(int(sqrt(numdots))):
			xpos = -spacing*(sqrt(numdots)-1)/2.0+spacing*i
			for j in range(int(sqrt(numdots))):
				ypos = -spacing*(sqrt(numdots)-1)/2.0+spacing*j
				#random xy jitter
				rndx = int(spacing*(random()-0.5)/2.0)
				rndy = int(spacing*(random()-0.5)/2.0)
				patrn_sprite.circlefill(occlclr+(255,),int(w), int(xpos+rndx), int(ypos+rndy))
	elif patrnshape == 3: # semicircular arcs of random orientation
		#	for i in range(numarcs):
		#	#find a random x position and y position
		#	rndx = int(spritew*(random()-0.5)/2.0)
		#	rndy = int(spriteh*(random()-0.5)/2.0)
		#	#rand start ang
		#	rnd_start = random()*2*pi
		#	patrn_sprite.arc(occlclr+(255,),int(2.0*w),int(2.0*w),rndx,rndy,rnd_start,rnd_start+pi,width=int(w/2.0))	
		#trying pseudo random
		for i in range(int(sqrt(numarcs))):
			xpos = -spacing*(sqrt(numarcs)-1)/2.0+spacing*i
			for j in range(int(sqrt(numarcs))):
				ypos = -spacing*(sqrt(numarcs)-1)/2.0+spacing*j
				#random start angle
				rndx = int(spritew*(random()-0.5)/2.0)
				#	rndy = int(spriteh*(random()-0.5)/2.0)
				#rand start ang
				rnd_start = random()*2*pi
				patrn_sprite.arc(occlclr+(255,),int(4.0*w),int(4.0*w),xpos,ypos,rnd_start,rnd_start+pi,width=2)	
	return patrn_sprite

