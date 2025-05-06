import sys,types, math
from pype import *
from events import *
from Tkinter import *

def createsimpcuestim(myWidth, myLength, myFB, myStimColor1,myX, myY, myBG,myNumdot, line_width,dotrad,seg_length,theta_1,myRFsize,RFprop):
	theta=theta_1/2.0 
	perispace=(myRFsize*RFprop)/(myNumdot*2.0)	# 2 in denomrepresents to divide diameter
	xvertex=0
	yvertex=0
	
	# DOTS ...put a dot @ every perispace
	seg_x=[xvertex]
	seg_y=[yvertex]
	for ii in range(1,myNumdot+1):
		seg_x.append(xvertex + sin(theta)*perispace*ii)
		seg_y.append(yvertex - cos(theta)*perispace*ii)
		seg_x.append(xvertex - sin(theta)*perispace*ii)
		seg_y.append(yvertex - cos(theta)*perispace*ii)
	
	coords= transpose(reshape(concatenate([seg_x,seg_y]),(2,len(seg_x))))
	s1 = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
	s1.fill(myBG)	
	s1.pdots(myStimColor1,coords,dotrad)#segmentverts,segcolor)
	
	# LINES ...coords for center of line in rseg_x etc. endpoints in tline_coords
	rseg_x=[];
	rseg_y=[];
	lseg_x=[];
	lseg_y=[];
	offset=perispace/2.0
	#seg_length=perispace*seg_prop
	for ii in range(1,myNumdot+1):
		#right pair
		rseg_x.append(xvertex +sin(theta)*(perispace*ii-offset))
		rseg_y.append(yvertex -cos(theta)*(perispace*ii-offset))
	for ii in range(1,myNumdot+1):
		#left pair
		lseg_x.append(xvertex -sin(theta)*(perispace*ii-offset))
		lseg_y.append(yvertex -cos(theta)*(perispace*ii-offset))
	# put coords for tlines in linecoords
	tline_coords=[]
	for bb in range(myNumdot):
		xr= sin(theta)* seg_length/2.0
		yr= cos(theta)* seg_length/2.0
		x1=rseg_x[bb] - xr
		x2=rseg_x[bb] + xr
		y1=rseg_y[bb] + yr
		y2=rseg_y[bb] - yr
		tline_coords.append([(x1,y1),(x2,y2)])
		x1l=lseg_x[bb] - xr
		x2l=lseg_x[bb] + xr
		y1l=lseg_y[bb] - yr
		y2l=lseg_y[bb] + yr
		tline_coords.append([(x1l,y1l),(x2l,y2l)])
	
	s2 = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
	s2.fill(myBG)	
	s2.tlines(myStimColor1,tline_coords,line_width)
	return s1,s2
	
def createAngleContourstim(myWidth, myLength, myFB, myStimColor1,myX, myY, myBG,line_width,theta_1,myRFsize,RFprop,Splineprop,smp):
	theta=theta_1/2.0 
	#perispace=(myRFsize*RFprop)/(myNumdot*2.0)	# 2 in denomrepresents to divide diameter
	xvertex=0
	yvertex=0
	contour_length=(myRFsize/2.0)*RFprop
	# angle contour needs only endpoints and vertex.
	seg_x=[]
	seg_x.append(xvertex-sin(theta)*contour_length)
	seg_x.append(xvertex)
	seg_x.append(xvertex+sin(theta)*contour_length)
	seg_y=[]
	seg_y.append(yvertex-cos(theta)*contour_length)
	seg_y.append(yvertex)
	seg_y.append(yvertex-cos(theta)*contour_length)
	
	coords= transpose(reshape(concatenate([seg_x,seg_y]),(2,len(seg_x))))
	s_angle = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
	s_angle.fill(myBG)	
	s_angle.unassumingpolygon(myStimColor1,0,coords,line_width)
	
	# spline contour needs additional info, which is location of control points around vertex
	controlpoint_xl=xvertex-sin(theta)*contour_length*Splineprop
	controlpoint_xr=xvertex+sin(theta)*contour_length*Splineprop
	controlpoint_yl=yvertex-cos(theta)*contour_length*Splineprop
	controlpoint_yr=yvertex-cos(theta)*contour_length*Splineprop
	# endpoints added three times ...this is necessary b/c interpolate does not return control points.
	Xvrt=[seg_x[0],seg_x[0],seg_x[0],controlpoint_xl,seg_x[1],controlpoint_xr,seg_x[2],seg_x[2],seg_x[2]]
	Yvrt=[seg_y[0],seg_y[0],seg_y[0],controlpoint_yl,seg_y[1],controlpoint_yr,seg_y[2],seg_y[2],seg_y[2]]
	Xvrt=asarray(Xvrt)
	Yvrt=asarray(Yvrt)
	nvrt=6
	spline_coords=interpolateBspline(Xvrt,Yvrt,nvrt,smp)
	s_spline = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
	s_spline.fill(myBG)	
	s_spline.unassumingpolygon(myStimColor1,0,spline_coords,line_width)
	
	return s_angle,s_spline

def interpolateBspline(Xvrt,Yvrt,nvrt,smp):
	# NOTE THAT this function does not return control points at either end.
	smp= float(smp)
	ip = arange(smp)/smp 
	incr = zeros((4,int(smp)), Float)
	incr[0,:] = -ip*ip*ip+3*ip*ip-3*ip+1
	incr[1,:] = 3*ip*ip*ip-6*ip*ip+4
	incr[2,:] = -3*ip*ip*ip+3*ip*ip+3*ip+1
	incr[3,:] = ip*ip*ip
	Xarr = zeros(nvrt*int(smp), Float)## array for polygon vertices
	Yarr = zeros(nvrt*int(smp), Float)
	xvrtid = zeros((4,int(smp)), Float)
	yvrtid = zeros((4,int(smp)), Float)
	
	vtx = []
	vty = []
	j = 0
	while j < nvrt:
		k=0
		while k < 4:
			xvrtid[k,:] = Xvrt[j+k]
			yvrtid[k,:] = Yvrt[j+k]
			k = k+1
		xb = list(sum(xvrtid*incr)/6.0)
		vtx.append(xb)
		yb = list(sum(yvrtid*incr)/6.0)
		vty.append(yb)
		j = j+1
	vtx1 = reshape(array(vtx),(nvrt*int(smp),))
	vty1 = reshape(array(vty),(nvrt*int(smp),))

	Xarr[0:nvrt*int(smp)] = vtx1  # adding .5 because anitha does. can't tell if it helps with clipping
	Yarr[0:nvrt*int(smp)] = vty1  # took this out to debug... might distort oridistance. can add .5 alter
	
	bs_coords = transpose(reshape(concatenate([Xarr[0:nvrt*int(smp)],Yarr[0:nvrt*int(smp)]]),\
				(2,smp*nvrt)))
				
	return bs_coords
		

# BAR is used for blank creation. 
def createBar(myWidth, myLength, myFB, myColor, myRot, myX, myY,myBG):
    s = Sprite(myWidth, myLength, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1) 
    s.fill(myColor)
    s.rotate(myRot, 0, 1)
    s.myColor = myColor
    return s


