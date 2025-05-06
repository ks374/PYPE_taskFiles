import sys,types, math
from pype import *
from events import *
from Tkinter import *

def createOverlapStar(myFB, myStimColor1,myStimColor2,myMidColor,myX, myY, myBG, line_width, length, length2, numPoints,depth,xoffset, yoffset, radius):
	s = Sprite(radius*2, radius*2, myX, myY, fb=myFB, depth=depth, on=0, centerorigin=1)
	s.fill(myBG+(0,))
	#length2 = length/2
	angle_space = 360.0/numPoints
	angle = 0.0
	poly_coords = list()
	poly_coords2 = list()
	for i in range(0, numPoints):
		poly_coords.append((length*cos(math.radians(angle))+xoffset, length*sin(math.radians(angle))+yoffset))
		poly_coords.append((length2*cos(math.radians(angle+angle_space/4))+xoffset,length2*sin(math.radians(angle+angle_space/4))+yoffset))
		slope1 = ((length*sin(math.radians(angle))) - (length2*sin(math.radians(angle+angle_space/4))))/((length*cos(math.radians(angle)))-(length2*cos(math.radians(angle+angle_space/4))))
		slope2 = ((length2*sin(math.radians(angle+angle_space/4+angle_space/2)))-(length*sin(math.radians(angle + angle_space))))/((length2*cos(math.radians(angle+angle_space/4+angle_space/2)))-(length*cos(math.radians(angle + angle_space))))
		b1 = (length*sin(math.radians(angle))) - slope1*(length*cos(math.radians(angle)))
		b2 = (length2*sin(math.radians(angle+angle_space/4+angle_space/2))) - slope2*(length2*cos(math.radians(angle+angle_space/4+angle_space/2)))
		xcoord = (b2 - b1)/(slope1 - slope2)
		ycoord = slope1*xcoord + b1
		poly_coords.append((xcoord+xoffset, ycoord+yoffset))
		poly_coords.append((length2*cos(math.radians(angle+angle_space/4+angle_space/2))+xoffset,length2*sin(math.radians(angle+angle_space/4+angle_space/2))+yoffset))
		angle = angle + angle_space
	angle = angle_space/2
	for i in range(0, numPoints):
		poly_coords2.append((length*cos(math.radians(angle))+xoffset, length*sin(math.radians(angle))+yoffset))
		poly_coords2.append((length2*cos(math.radians(angle+angle_space/4))+xoffset,length2*sin(math.radians(angle+angle_space/4))+yoffset))
		slope1 = ((length*sin(math.radians(angle))) - (length2*sin(math.radians(angle+angle_space/4))))/((length*cos(math.radians(angle)))-(length2*cos(math.radians(angle+angle_space/4))))
		slope2 = ((length2*sin(math.radians(angle+angle_space/4+angle_space/2)))-(length*sin(math.radians(angle + angle_space))))/((length2*cos(math.radians(angle+angle_space/4+angle_space/2)))-(length*cos(math.radians(angle + angle_space))))
		b1 = (length*sin(math.radians(angle))) - slope1*(length*cos(math.radians(angle)))
		b2 = (length2*sin(math.radians(angle+angle_space/4+angle_space/2))) - slope2*(length2*cos(math.radians(angle+angle_space/4+angle_space/2)))
		xcoord = (b2 - b1)/(slope1 - slope2)
		ycoord = slope1*xcoord + b1
		poly_coords2.append((xcoord+xoffset, ycoord+yoffset))
		poly_coords2.append((length2*cos(math.radians(angle+angle_space/4+angle_space/2))+xoffset,length2*sin(math.radians(angle+angle_space/4+angle_space/2))+yoffset))
		angle = angle + angle_space
	s.polygon(myStimColor1, poly_coords, line_width)
	s.polygon(myStimColor2, poly_coords2, line_width)
	overlap_coords = list()
	for i in range(0, numPoints):
		overlap_coords.append(poly_coords[i*4 + 1])
		overlap_coords.append(poly_coords[i*4 + 2])
		overlap_coords.append(poly_coords2[i*4 + 1])
		overlap_coords.append(poly_coords2[i*4 + 2])
	s.polygon(myMidColor, overlap_coords, line_width)
	return s
	
def createEmptyStar1(myFB, myOutlineColor,myX, myY, myBG, line_width, length,length2, numPoints):
	s = Sprite(length*3, length*3, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
	s.fill(myBG)
	#length2 = length/2
	angle_space = 360.0/numPoints
	angle = 0.0
	poly_coords = list()
	for i in range(0, numPoints):
		poly_coords.append((length*cos(math.radians(angle)), length*sin(math.radians(angle))))
		poly_coords.append((length2*cos(math.radians(angle+angle_space/4)),length2*sin(math.radians(angle+angle_space/4))))
		slope1 = ((length*sin(math.radians(angle))) - (length2*sin(math.radians(angle+angle_space/4))))/((length*cos(math.radians(angle)))-(length2*cos(math.radians(angle+angle_space/4))))
		slope2 = ((length2*sin(math.radians(angle+angle_space/4+angle_space/2)))-(length*sin(math.radians(angle + angle_space))))/((length2*cos(math.radians(angle+angle_space/4+angle_space/2)))-(length*cos(math.radians(angle + angle_space))))
		b1 = (length*sin(math.radians(angle))) - slope1*(length*cos(math.radians(angle)))
		b2 = (length2*sin(math.radians(angle+angle_space/4+angle_space/2))) - slope2*(length2*cos(math.radians(angle+angle_space/4+angle_space/2)))
		xcoord = (b2 - b1)/(slope1 - slope2)
		ycoord = slope1*xcoord + b1
		poly_coords.append((xcoord, ycoord))
		poly_coords.append((length2*cos(math.radians(angle+angle_space/4+angle_space/2)),length2*sin(math.radians(angle+angle_space/4+angle_space/2))))
		angle = angle + angle_space
	s.polygon(myOutlineColor, poly_coords, line_width)
	return s
	
def createEmptyStar2(myFB, myOutlineColor,myX, myY, myBG, line_width, length, length2, numPoints):
	s = Sprite(length*3, length*3, myX, myY, fb=myFB, depth=1, on=0, centerorigin=1)
	s.fill(myBG)
	#length2 = length/2
	angle_space = 360.0/numPoints
	angle = angle_space/2
	poly_coords = list()
	for i in range(0, numPoints):
		poly_coords.append((length*cos(math.radians(angle)), length*sin(math.radians(angle))))
		poly_coords.append((length2*cos(math.radians(angle+angle_space/4)),length2*sin(math.radians(angle+angle_space/4))))
		slope1 = ((length*sin(math.radians(angle))) - (length2*sin(math.radians(angle+angle_space/4))))/((length*cos(math.radians(angle)))-(length2*cos(math.radians(angle+angle_space/4))))
		slope2 = ((length2*sin(math.radians(angle+angle_space/4+angle_space/2)))-(length*sin(math.radians(angle + angle_space))))/((length2*cos(math.radians(angle+angle_space/4+angle_space/2)))-(length*cos(math.radians(angle + angle_space))))
		b1 = (length*sin(math.radians(angle))) - slope1*(length*cos(math.radians(angle)))
		b2 = (length2*sin(math.radians(angle+angle_space/4+angle_space/2))) - slope2*(length2*cos(math.radians(angle+angle_space/4+angle_space/2)))
		xcoord = (b2 - b1)/(slope1 - slope2)
		ycoord = slope1*xcoord + b1
		poly_coords.append((xcoord, ycoord))
		poly_coords.append((length2*cos(math.radians(angle+angle_space/4+angle_space/2)),length2*sin(math.radians(angle+angle_space/4+angle_space/2))))
		angle = angle + angle_space
	s.polygon(myOutlineColor, poly_coords, line_width)
	return s
