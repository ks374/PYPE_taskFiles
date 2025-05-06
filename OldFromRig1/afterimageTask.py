## CUE TASK
## jkb, 4/1/08

import sys, types
from pype import *
from Numeric import *
from random import *
from shapes import *
from afterimage_shapes import *
from colors import *
from fixationTask import fixationTask



class cueTask(fixationTask):       	# color task as subclass of fixation task
	def __init__(self, app):         	# constructor stuff. this happens as soon as instantiated.
		self.createParamTable(app)
		self.app = app
		self.mySprites = list()      	# this will be list of sprite objects
		self.numStim = 0		# WHAT IS THIS? num stim?
		self.mySpriteList = list()   	# spritelist is index into sprite lists
		self.spriteColors = list()
	
	def createStimuli(self,app):      	#self. syntax identifies variables of this object.
		self.params = self.myTaskParams.check()   
		params = self.params
		self.mySprites = list()     	# redundant with above. in case sprites/spritelist changes after cuetask constructed
		self.numStim = 0		# ends up being equal to numuniquestims * nreps per stim. don't know why we need this.
		self.mySpriteList = list()
# 		self.b8_idlist = list()		#[51=blank]
# 		self.rot_idlist= list()
# 		self.cue_idlist= list()		#[0=contour,1=dots,2=tlines,3=olines]
# 		self.numcue_idlist= list()	# gives number of cue elements about perimeter
# 		self.dotrad_idlist= list()	#[for these, 0 denotes full contour ie n/a]
# 		self.perispace_idlist=list()
# 		self.linewidth_idlist=list()
		
		## LOCAL VARIABLES FROM PTABLE
		myFB = app.fb               
		myX = params['RF_Center_X']
		myY = params['RF_Center_Y']
		# FOR TESTING: SPRITE IN DIFF COLOR. 
		myBG = params['bg_during']
		## Stimulus and stimulus presentation params
		randomize_stims = params['randomize_stimuli']
		transparent_occluder= params['transparent_occluder']
		full_occluder=params['full_occluder']
		middlebg_occluder=params['middlebg_occluder']
		line_width= params['line_width']
		#rotnums= eval(params['rotnums'])
		bigtri_sidelength= params['bigtri_sidelength']
		myStimColor1= params['StimColor1']
		myStimColor2= params['StimColor2']
		myMidColor= params['MidColor']
		myOutlineColor=params['OutlineColor']
		P= app.getcommon()		# stores all rig and subject parameters within P.
		monppd= P['mon_ppd']
		myWidth=2*bigtri_sidelength
		myLength= myWidth
		# WHAT DO I NEED TO DO HERE.
		# A. (1)red,green,cyan (2)blank triangle up
		# A1. (1) same jewstar, (2) blank triangle down
		# B. (1) occluded jew star (1)blank up
		# B1							(2) occluded down				
		# C (1) black center jew star, (2) up
		# C1
		# can flag for each of these conditions
		# if do 2stimsper trial... in testing mode, will work for psychophysics (control stim time,isi,iti,etc)
		
		# TASK VERSION 1: transparent occluder, followed by blanks.
		if (transparent_occluder==1):
			
			#all_rots=[0,45,90,135,180,225,270,315]
			#SPRITE CREATION LOOP
			# note that you cannot copy an object-- just makes a reference.
			s = createJewstar(myWidth, myLength, myFB, myStimColor1,myStimColor2,myMidColor,myX, myY, myBG, 0, bigtri_sidelength)
			self.mySprites.append(s)
			s2=createBigTriangleUp(myWidth, myLength, myFB, myOutlineColor, myX,myY, myBG, line_width, bigtri_sidelength)
			self.mySprites.append(s2)
			s3=createJewstar(myWidth, myLength, myFB, myStimColor1,myStimColor2,myMidColor,myX, myY, myBG, 0, bigtri_sidelength)
			self.mySprites.append(s3)
			s4=createBigTriangleDown(myWidth, myLength, myFB, myOutlineColor, myX,myY, myBG, line_width, bigtri_sidelength)
			self.mySprites.append(s4)
# 			for myStimid in stimlist:
# 				line_width=contour_width
# 				coords = transpose(reshape(concatenate([xvrt[myStimid][0:nvrt[myStimid]*smp],\
# 					yvrt[myStimid][0:nvrt[myStimid]*smp]]),\
# 					(2,smp*nvrt[myStimid])))
# 				# put out derivative info in same x,y framework. 
# 				d_coords = transpose(reshape(concatenate([dxvrt[myStimid][0:nvrt[myStimid]*smp],\
# 					dyvrt[myStimid][0:nvrt[myStimid]*smp]]),\
# 					(2,smp*nvrt[myStimid])))
# 				
# 				numrot=numrot_list[myStimid]
# 				rots=all_rots[0:numrot]
# 				for dummy in rots:
# 					s = createB8stim(myWidth, myLength, myFB, myColor,myX, myY, myBG, coords, line_width)
# 					s.rotate(dummy)
# 					self.mySprites.append(s)
# 					self.b8_idlist.append(myStimid)
# 					self.rot_idlist.append(dummy)
# 					self.cue_idlist.append(0)
# 					self.numcue_idlist.append(0)
# 					self.linewidth_idlist.append(line_width)
# 					self.dotrad_idlist.append(0)	#[for these, 0 denotes full contour ie n/a]
# 					self.perispace_idlist.append(0)
		
# 		# TASK VERSION 2: SELECTED SHAPES AND ROTATIONS, ALL CUE TYPES, CUE SIZE AND SPACING SPECIFIED
# 		else:
# 			if stimnum_from51:
# 				list51= list([5,6,7,10,11] + range(14,40) +[41,42,46,47,50])
# 				tempstimlist=[]
# 				for ii in range(len(stimnums)):
# 					stim_in51= stimnums[ii]
# 					stim_in36= list51.index(stim_in51)
# 					tempstimlist.append(stim_in36)
# 				stimlist=tempstimlist
# 				print 'stimlist from 51'
# 				print stimlist
# 			else:
# 				stimlist = stimnums
# 			
# 			rotlist = rotnums
# 			for index in range(len(stimlist)):       
# 				myStimid= stimlist[index]
# 				print 'stimid'
# 				print myStimid
# 				myRot= rotlist[index]
# 				coords = transpose(reshape(concatenate([xvrt[myStimid][0:nvrt[myStimid]*smp],\
# 					yvrt[myStimid][0:nvrt[myStimid]*smp]]),\
# 					(2,smp*nvrt[myStimid])))
# 				# put out derivative info in same x,y framework. 
# 				d_coords = transpose(reshape(concatenate([dxvrt[myStimid][0:nvrt[myStimid]*smp],\
# 					dyvrt[myStimid][0:nvrt[myStimid]*smp]]),\
# 					(2,smp*nvrt[myStimid])))
# 				# create the sprites of diff cue types
# 				line_width= contour_width	#for contour, use smallest linewidth
# 				s1 = createB8stim(myWidth, myLength, myFB, myColor,myX, myY, myBG, coords, line_width)
# 				s1.rotate(myRot)
# 				self.mySprites.append(s1)
# 				
# 				self.b8_idlist.append(myStimid)
# 				self.rot_idlist.append(myRot)
# 				self.cue_idlist.append(0)
# 				self.numcue_idlist.append(0)
# 				self.linewidth_idlist.append(line_width)
# 				self.dotrad_idlist.append(0)	#[for these, 0 denotes full contour ie n/a]
# 				self.perispace_idlist.append(0)
# 				
# 				for index in range(len(perispacelist)):
# 					perispace= int(round(perispacelist[index]))
# 					line_width=cue_linewidth
# 					radius= cueradius
# 					# for circle cues, compute radius to match area with line segments
# 					cue_area= pi*((float(radius))**2)
# 					seg_length_float= cue_area/line_width
# 					seg_length=int(round(seg_length_float))
# 					print 'seg_length'
# 					print seg_length
# 					s2,s5,numcue = createB8dots(myWidth, myLength, myFB, myColor,myX, myY, myBG, coords,radius,perispace,d_coords,seg_length,line_width)
# 					s3,numcue = createB8tlines(myWidth, myLength, myFB, myColor,myX, myY, myBG, coords,radius,perispace,d_coords,seg_length,line_width)
# 					s2.rotate(myRot)
# 					s3.rotate(myRot)
# 					s5.rotate(myRot)
# 					#append to sprite list                
# 					self.mySprites.append(s2)
# 					self.b8_idlist.append(myStimid)
# 					self.rot_idlist.append(myRot)
# 					self.cue_idlist.append(1)	#[0=contour,1=dots,2=tlines,3=olines]
# 					self.numcue_idlist.append(numcue)
# 					self.linewidth_idlist.append(line_width)
# 					self.dotrad_idlist.append(radius)	#[for these, 0 denotes full contour ie n/a]
# 					self.perispace_idlist.append(perispace)
# 					
# 					self.mySprites.append(s3)
# 					self.b8_idlist.append(myStimid)
# 					self.rot_idlist.append(myRot)
# 					self.cue_idlist.append(2)
# 					self.numcue_idlist.append(numcue)
# 					self.linewidth_idlist.append(line_width)
# 					self.dotrad_idlist.append(radius)	#[for these, 0 denotes full contour ie n/a]
# 					self.perispace_idlist.append(perispace)
# 					
# 		
		# No Blanks for now b/c will throw off ordering... but, once sprites paired into groups will work.
# 		# APPEND BLANKS TO SPRITELIST (color=mybg)
# 		for j in arange(0,params['nBlanks']):
# 			s = createBar(myWidth, myLength, myFB,myBG, 360, myX, myY, myBG)
# 			self.mySprites.append(s)
# 			self.b8_idlist.append(51)
# 			self.rot_idlist.append(0)
# 			self.cue_idlist.append(0)
# 			self.numcue_idlist.append(0)
# 			self.linewidth_idlist.append(0)
# 			self.dotrad_idlist.append(0)	#[for these, 0 denotes full contour ie n/a]
# 			self.perispace_idlist.append(0)
		
		# SHUFFLE
		numUniqueStims = len(self.mySprites)
		stimNumbers = arange(0,numUniqueStims)
		for i in arange(0,params['nRepsPerStim']):
			if(randomize_stims):                  
				shuffle(stimNumbers)
			self.mySpriteList.extend(stimNumbers)  # extend is like append but it iterates.
			self.numStim = self.numStim + len(self.mySprites)
# 		print 'myspritelist'
# 		print self.mySpriteList
# 		print 'len stimnumbers'
# 		print len(stimNumbers)

		# MAKING VARIABLES ACCESSIBLE OUTSIDE OF THIS FUNCTION
		self.myWidth = myWidth  # these definitions just make variables global so accessible outside
		#removed aspect and orientation
		self.myFB = myFB
		self.myX = myX
		self.myY = myY
	
	def createParamTable(self,app):
		#create parameter table and window to go along with it
		self.myTaskButton = app.taskbutton(text=__name__, check=1)
		self.myTaskNotebook = DockWindow(title=__name__, checkbutton=self.myTaskButton)
		parfile = app.taskname()
		# Look for an existing saved parameter file for this task
		if parfile:
			parfile = parfile + '.par'
		
		# Initialization and default values for the parameters.  Each row is
		# one parameter.  The first value is the name of the parameter, the
		# second is its default value, the third defines the type of
		# the value (more on that later) and the fourth is optional and
		# is a descriptive label that pops up when you hold the mouse over
		# that entry in the table.  There are numerous standard parameter
		# types, the most common are self-explanatory.  is_color needs to be
		# 3 or 4 numbers in tuple format, e.g. (255,1,1) for red; the 4th
		# number is optional and is an alpha value (if left off, assumed
		# to be 255).  (0,0,0) is a special code for transparent or for
		# white noise fill pattern, depending on the task, so use (1,1,1)
		# for black.  is_any just gets passed as a string, this is what
		# to use if you need a list of numbers.  is_iparam can take a
		# variance value as either a percentage or an actual number of
		# units, so you'd have "1000+-10%" or "150+-50".  There are a ton of
		# others defined in ptable.py.  Values of None for default value and
		# type make that row into a heading of sorts that can be helpful for
		# organizing a large number of parameters.
		self.myTaskParams = ParamTable(self.myTaskNotebook, (
			("STIMULUS PRESENTATION params", None, None),
			("randomize_stimuli", 0, is_boolean, "Whether or not to randomize stimuli within repetitions."),
			("StimColor1","(164, 1, 1)",    is_color, "color of stimulus"),
			("StimColor2","(1, 164, 1)",    is_color, "color of stimulus"),
			("MidColor","(100, 80, 1)",    is_color, "color of stimulus"),
			("nRepsPerStim",    "10", is_int, "Number of repetitions of each stimulus to present"),
			("OutlineColor",	"(255,255,255)",is_color, 'Color of the outline afterimage goes in'),
			("bg_during", "(10, 10, 10)", is_color, "The background color during stimulus presentation"),
			("bg_before", "(10, 10, 10)", is_color, "The background color before stimulus presentation"),
			("RF_Center_X", "100",is_int,"X coordinate of the receptive field center in pixels"),
			("RF_Center_Y", "-100",is_int,"Y coordinate of the receptive field center in pixels"),
			("STIMULUS params", None, None),
			("transparent_occluder",	"1", 	is_boolean, "'1' gives  intermediate middle fill"),
			("full_occluder",	"1", 	is_boolean, "'1' gives  middle fill = 1 of colors"),
			("middlebg_occluder",	"1", 	is_boolean, "'1' gives  middle fill = bg"),
			("bigtri_sidelength",    "3", is_int, "side length of large equilateral triangle"),
			("line_width",    "1", is_int, "width of line for blank"),
			("TASK Params", None, None),
			("iti",	"2500",		   	is_int, "Inter-trial interval"),
			("IStime",	"200",		   	is_int, "Inter-stimulus interval--NOTE THIS IS LAG BETWEEN INDUCER AND BLANK"),
			("stimon",	"1000",			is_int, "Stimulus presentation time"),
			("nstim",	"2",			is_int, "Number of stimuli in a trial-- note this must be 2!"),
			("Fixation Params", None, None, "Fixation Parameters"),
			("fixcolor1",	"(255,255,255)",is_color, 'Color of the fixation dot'),
			("fixcolor2",	"(128,128,128)",is_color),
			("min_err",		"0",		   	is_int),
			("max_err",		"100",		   	is_int),
			("fixwait",		"100",		   	is_int),
			("REWARD Params", None, None),
			("numdrops",    "8",           is_int, "Number of juice drops"),
			("rmult",		"1.0",		   	is_float),
			("SPECIAL NAME Params", None, None, "Params for setting name of record file"),
			("Use Special Name", "0", is_boolean, "If 1 then the record file name will be AnimalPrefixDate_TaskName_CellGroup_Iteration.rec"),
			("RFDirectory", "/home/shapelab/recordFiles/", is_any, "Directory to use for Record Files"),
			("AnimalPrefix", "M", is_any, "Animal Prefix to use"),
			("Date","080325",    is_any, "Date to use "),
			("TaskName","cuetest",    is_any, "TaskName"),
			("CellGroup","01",    is_int, "# of cell group encountered today"),
			("Iteration","01",    is_int, "# of times this task has been run on this cell group"),
			("Misc Params", None, None, "Miscelaneous Parameters"),
			("Recent Buffer Size", "50", is_int, "The number of trials to use to calculate recent performance"),
			("pause_color", "(150,0,0)", is_color, "The screen will turn this color when the task is paused")
			), file=parfile)
	
	#("nBlanks",    "2", is_int, "The number of blank stimuli to present per block"),
	def cleanup(self, app):
		#delete parameter table and anything else we created
		self.myTaskParams.save()
		self.myTaskButton.destroy()
		self.myTaskNotebook.destroy()
		del app.globals
		
	
	def encodeISI(self,app,sIndex):
		pass
# 		stimparamIndex = self.mySpriteList[sIndex]	#sIndex indexes mySpritelist which indexes all other indexes
# 		myB8= int(self.b8_idlist[stimparamIndex])
# 		myRot= int(self.rot_idlist[stimparamIndex])
# 		myCue= int(self.cue_idlist[stimparamIndex])
# 		myNumCue = int(self.numcue_idlist[stimparamIndex])
# 		myLW= int(self.linewidth_idlist[stimparamIndex])
# 		myDotRad= int(self.dotrad_idlist[stimparamIndex])	#[for these, 0 denotes full contour ie n/a]
# 		myPerispace= int(self.perispace_idlist[stimparamIndex])
# 		
# 		app.encode_plex('stimid')
# 		app.encode('stimid')
# 		app.encode_plex(myB8 + app.globals.plexRotOffset)
# 		app.encode(myB8 + app.globals.plexRotOffset)
# 			
# 		app.encode_plex('rotid')
# 		app.encode('rotid')
# 		app.encode_plex(myRot + app.globals.plexRotOffset)	
# 		app.encode(myRot + app.globals.plexRotOffset)
# 		
# 		app.encode_plex('gen_mode')
# 		app.encode('gen_mode')
# 		app.encode_plex(myCue + app.globals.plexRotOffset)	
# 		app.encode(myCue + app.globals.plexRotOffset)
# 		
# 		app.encode_plex('gen_submode')
# 		app.encode('gen_submode')
# 		app.encode_plex(myNumCue + app.globals.plexRotOffset)	
# 		app.encode(myNumCue + app.globals.plexRotOffset)
# 		
# 		app.encode_plex('line_width')
# 		app.encode('line_width')
# 		app.encode_plex(myLW + app.globals.plexRotOffset)	
# 		app.encode(myLW + app.globals.plexRotOffset)
# 		
# 		app.encode_plex('dot_rad')
# 		app.encode('dot_rad')
# 		app.encode_plex(myDotRad + app.globals.plexRotOffset)	
# 		app.encode(myDotRad + app.globals.plexRotOffset)
# 		
# 		app.encode_plex('perispace')
# 		app.encode('perispace')
# 		app.encode_plex(myPerispace + app.globals.plexRotOffset)	
# 		app.encode(myPerispace + app.globals.plexRotOffset)
# 		
# 		print 'sIndex,  stimparamIndex,  myB8,  myRot'
# 		print '%d, %d, %d, %d:' %(sIndex,stimparamIndex,myB8,myRot)
# 		print 'myCue,,myNumCue,myLW,myDotRad,myPerispace'
# 		print '%d, %d, %d, %d, %d:' %(myCue,myNumCue,myLW,myDotRad,myPerispace)
	
	def encodeTaskParameters(self,app):
		pass
# 		#encode task parameters
# 		params = self.myTaskParams.check()
# 		app.encode_plex('rfx')
# 		app.encode('rfx')
# 		app.encode_plex(params['RF_Center_X']+ app.globals.yOffset)
# 		app.encode(params['RF_Center_X']+ app.globals.yOffset)
# 		
# 		app.encode_plex('rfy')
# 		app.encode('rfy')
# 		app.encode_plex(params['RF_Center_Y'] + app.globals.yOffset)
# 		app.encode(params['RF_Center_Y'] + app.globals.yOffset)
# 		
# 		app.encode_plex('iti')
# 		app.encode('iti')
# 		app.encode_plex(int(params['iti']))
# 		app.encode(int(params['iti']))
# 		
# 		app.encode_plex('stim_time')
# 		app.encode('stim_time')
# 		app.encode_plex(int(params['stimon']))
# 		app.encode(int(params['stimon']))
# 		
# 		app.encode_plex('isi')
# 		app.encode('isi')
# 		app.encode_plex(int(params['IStime']))
# 		app.encode(int(params['IStime']))
# 		
# 		app.encode_plex('numstim')
# 		app.encode('numstim')
# 		app.encode_plex(int(params['nstim']))
# 		app.encode(int(params['nstim']))
# 		
# 		app.encode_plex('color')
# 		app.encode('color')
# 		app.encode_plex(int((params['stimcolor'][0])) + app.globals.plexRotOffset)
# 		app.encode_plex(int((params['stimcolor'][1])) + app.globals.plexRotOffset)
# 		app.encode_plex(int((params['stimcolor'][2])) + app.globals.plexRotOffset)
# 		app.encode(int((params['stimcolor'][0])) + app.globals.plexRotOffset)
# 		app.encode(int((params['stimcolor'][1])) + app.globals.plexRotOffset)
# 		app.encode(int((params['stimcolor'][2])) + app.globals.plexRotOffset)
# 	
	
	def encodeITI(self,app):
		pass
	
	def getSprite(self, index):
		print index
		print self.mySprites[self.mySpriteList[index]]
		return self.mySprites[self.mySpriteList[index]]
	
	def getNumStim(self):
		return self.numStim
	
	def getRecordFileName(self): #gets the record file for this task 
		params = self.myTaskParams.check()
		if(params['Use Special Name']):
			filename = "%s%s%s_%s_%02d_%02d.rec" % (params['RFDirectory'],params['AnimalPrefix'],params['Date'],params['TaskName'],params['CellGroup'],params['Iteration'])
		else:
			filename = None
		return filename

def RunSet(app):
	app.taskObject.runSet(app)

def cleanup(app):
	app.taskObject.cleanup(app)

def main(app):
	app.taskObject = cueTask(app)
	app.globals = Holder()
	app.idlefb()
	app.startfn = RunSet

# This is also something that all tasks have, and it's a python thing.
# Don't touch it.
if not __name__ == '__main__':
	loadwarn(__name__)
else:
	dump(sys.argv[1])
