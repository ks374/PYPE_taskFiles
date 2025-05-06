## WILSON TASK
## jkb, 6/20/08

import sys, types
from pype import *
from Numeric import *
from random import *
from shapes import *
from wilson_shapes import *
from smallbar_shapes import *
from fixationTask import fixationTask
#from padlib import *

class wilsonTask(fixationTask): 			#  task as subclass of fixation task
	def __init__(self, app):         	# constructor stuff. this happens as soon as instantiated.
		self.createParamTable(app)
		self.app = app
		self.mySprites = list()      	# this will be list of sprite objects
		self.numStim = 0				# numstim is a counter
		self.mySpriteList = list()   	# spritelist is index into sprite lists
		self.spriteColors = list()
	
	def createStimuli(self,app):      	#self. syntax identifies variables of this object.
		self.params = self.myTaskParams.check()   
		params = self.params
		self.mySprites = list()     	# redundant with above.
		self.numStim = 0				# ends up being equal to numuniquestims * nreps per stim.
		self.mySpriteList = list()
		## CODE LISTS
		self.subtended_idlist = list()	# angle subtended
		self.rot_idlist= list()			# rotation
		self.mode_idlist= list()		# bars, splines, tips, etc
		#(1)spline, (2)angle, (3)long_notip, (4)lbar, (5)rbar, (6)short_notip, (7)angle_tip, (8)splinetip. (9)globalangle, (20)blank, (21-37)singlebar_locations
		## LOCAL VARIABLES FROM PTABLE
		myFB = app.fb
		myX = params['RF_Center_X']
		myY = params['RF_Center_Y']
		myBG = params['bg_during']
		smp=params['smp']
		## Stimulus and stimulus presentation params
		randomize_stims = params['randomize_stimuli']
		line_width= params['line_width']
		myStimColor1= params['StimColor1']
		P= app.getcommon()		# stores all rig and subject parameters within P.
		# RF SCALING
		# rfScale is backcalculated s.t codes don't change.
		# THEN IN MATLAB ANALYSIS, PULL OUT RF SIZE STUFF AND PUTIN FIG., BUILT IN TEST
		Absolute_RFsizeFlag = params['Absolute_RFsizeFlag']
		Absolute_RFsize = params['Absolute_RFsize']
		monppd= P['mon_ppd']
		ecc = ((myX**2.0)+(myY**2.0))**0.5
		if Absolute_RFsizeFlag:
			myRFsize= Absolute_RFsize
			myRFscale= (myRFsize-monppd)/ecc
		else:
			myRFscale = params['myRFscale']
			myRFsize= int(round(monppd+ myRFscale*ecc))
		print 'myRFsize'
		print myRFsize
		print 'myRFscale'
		print myRFscale
		myWidth=2*myRFsize
		myLength= myWidth
		## LINE WIDTH SCALING
		equivalent_ecc_scaling=myRFsize/monppd
		line_width2= line_width*equivalent_ecc_scaling
		line_width=line_width2
		
		# CREATE ORIENTED BAR, RFSUB STIMULI
		bar_spritelist, loc1_ID, rot1_ID=createOneBarstim(myWidth, myLength, myFB, myStimColor1,myX, myY, myBG, line_width,myRFsize)
		self.mySprites.extend(bar_spritelist)	#68 sprites appended (17loc*4rots)
		
		myDummysubtendedlist=[0]*68
		myDummyrotlist=list(45*asarray(rot1_ID))
		myDummymodelist=list(21+asarray(loc1_ID))
		self.subtended_idlist.extend(myDummysubtendedlist)
		self.rot_idlist.extend(myDummyrotlist)
		self.mode_idlist.extend(myDummymodelist)
		
		# WILSON STIMULI: LOOP THROUGH (1)angle subtended, (2) rotations. 
		all_angles=[45,90,135]
		all_rots=[0,45,90,135,180,225,270,315]
		for theta in all_angles:
			for dummy in all_rots:
				theta_1=theta*(pi/180.)
				s1,s2,s3,s4,s5,s6,s7,s8,s9,s10 = createWilsonstim(myWidth, myLength, myFB, myStimColor1,myX, myY, myBG, line_width,theta_1,myRFsize,smp,dummy)
				# rotations now done manually
				self.mySprites.append(s1)
				self.mySprites.append(s2)
				self.mySprites.append(s3)
				self.mySprites.append(s4)
				self.mySprites.append(s5)
				self.mySprites.append(s6)
				self.mySprites.append(s7)
				self.mySprites.append(s8)
				self.mySprites.append(s9)
				self.mySprites.append(s10)
				#8 sprites for each time through loop, each has same anglerot combo 
				myDummysubtendedlist=[theta]*10 
				myDummyrotlist=[dummy]*10
				myDummymodelist=range(1,11)
				# rotation 0 corresponds to 270degrees, the way things drawn
				self.subtended_idlist.extend(myDummysubtendedlist)
				self.rot_idlist.extend(myDummyrotlist)
				self.mode_idlist.extend(myDummymodelist)
		# APPEND BLANKS TO SPRITELIST (color=mybg)
		for j in arange(0,params['nBlanks']):
			s = createBar(myWidth, myLength, myFB,myBG, 360, myX, myY, myBG)
			self.mySprites.append(s)
			self.subtended_idlist.append(0)
			self.rot_idlist.append(0)
			self.mode_idlist.append(20)
			
		
		# SHUFFLE
		numUniqueStims = len(self.mySprites)
		stimNumbers = arange(0,numUniqueStims)
		for i in arange(0,params['nRepsPerStim']):
			if(randomize_stims):                  
				shuffle(stimNumbers)
			self.mySpriteList.extend(stimNumbers)  # extend is like append but it iterates.
			self.numStim = self.numStim + len(self.mySprites)
		
		# MAKING VARIABLES ACCESSIBLE OUTSIDE OF THIS FUNCTION
		self.myWidth = myWidth  # these definitions just make variables global so accessible outside
		self.myFB = myFB
		self.myX = myX
		self.myY = myY
		self.myBG = myBG
		self.myRFscale = myRFscale
		
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
			("nBlanks",    "2", is_int, "The number of blank stimuli to present per block"),
			("nRepsPerStim",    "10", is_int, "Number of repetitions of each stimulus to present"),
			("bg_during", "(10, 10, 10)", is_color, "The background color during stimulus presentation"),
			("bg_before", "(10, 10, 10)", is_color, "The background color before stimulus presentation"),
			("RF_Center_X", "100",is_int,"X coordinate of the receptive field center in pixels"),
			("RF_Center_Y", "-100",is_int,"Y coordinate of the receptive field center in pixels"),
			("Absolute_RFsizeFlag", "1", is_boolean, "if 1, size passed in, scale ignored"),
			("Absolute_RFsize", "200", is_int, "diameter of RF"),
			("myRFscale", ".625",is_float,"eccentricity scaling (1deg +scale*ecc)"),
			("STIMULUS params", None, None),
			("StimColor1","(164, 1, 1)",    is_color, "color of stimulus"),
			("line_width",    "1", is_int, "width of line for blank"),
			("smp",    "50", is_int, "spline sampling density ie points per spline segment"),
			("TASK Params", None, None),
			("iti",	"2500",		   	is_int, "Inter-trial interval"),
			("IStime",	"200",		   	is_int, "Inter-stimulus interval"),
			("stimon",	"1000",			is_int, "Stimulus presentation time"),
			("nstim",	"8",			is_int, "Number of stimuli in a trial"),
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
			("TaskName","wilsontest",    is_any, "TaskName"),
			("CellGroup","01",    is_int, "# of cell group encountered today"),
			("Iteration","01",    is_int, "# of times this task has been run on this cell group"),
			("Misc Params", None, None, "Miscellaneous Parameters"),
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
		stimparamIndex = self.mySpriteList[sIndex]	#sIndex indexes mySpritelist which indexes all other indexes
		mySubtended= int(self.subtended_idlist[stimparamIndex])
		myRot= int(self.rot_idlist[stimparamIndex])
		myMode= int(self.mode_idlist[stimparamIndex])
		
		app.encode_plex('stimid')
		app.encode('stimid')
		app.encode_plex(mySubtended + app.globals.plexRotOffset)
		app.encode(mySubtended + app.globals.plexRotOffset)
		
		app.encode_plex('rotid')
		app.encode('rotid')
		app.encode_plex(myRot + app.globals.plexRotOffset)	
		app.encode(myRot + app.globals.plexRotOffset)
		
		app.encode_plex('gen_mode')
		app.encode('gen_mode')
		app.encode_plex(myMode + app.globals.plexRotOffset)	
		app.encode(myMode + app.globals.plexRotOffset)
		
		
	
	def encodeTaskParameters(self,app):
		# need RF size task param or RFsize and RFscale double-duty!!??
		# NOTE THAT LINE WIDTH is not scaled. to get actual lw, use matlab end.
		#encode task parameters
		params = self.myTaskParams.check()
		app.encode_plex('rfx')
		app.encode('rfx')
		app.encode_plex(params['RF_Center_X']+ app.globals.yOffset)
		app.encode(params['RF_Center_X']+ app.globals.yOffset)
		
		app.encode_plex('rfy')
		app.encode('rfy')
		app.encode_plex(params['RF_Center_Y'] + app.globals.yOffset)
		app.encode(params['RF_Center_Y'] + app.globals.yOffset)
		
		app.encode_plex('iti')
		app.encode('iti')
		app.encode_plex(int(params['iti']))
		app.encode(int(params['iti']))
		
		app.encode_plex('stim_time')
		app.encode('stim_time')
		app.encode_plex(int(params['stimon']))
		app.encode(int(params['stimon']))
		
		app.encode_plex('isi')
		app.encode('isi')
		app.encode_plex(int(params['IStime']))
		app.encode(int(params['IStime']))
		
		app.encode_plex('numstim')
		app.encode('numstim')
		app.encode_plex(int(params['nstim']))
		app.encode(int(params['nstim']))
		
		app.encode_plex('line_width')
		app.encode('line_width')
		app.encode_plex(int(params['line_width'])+ app.globals.plexRotOffset)
		app.encode(int(params['line_width'])+ app.globals.plexRotOffset)
		
		app.encode_plex('midground_info')
		app.encode('midground_info')
		app.encode_plex(int(round(self.myRFscale*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
		app.encode(int(round(self.myRFscale*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
		
		app.encode_plex('color')
		app.encode('color')
		app.encode_plex(int((params['StimColor1'][0])) + app.globals.plexRotOffset)
		app.encode_plex(int((params['StimColor1'][1])) + app.globals.plexRotOffset)
		app.encode_plex(int((params['StimColor1'][2])) + app.globals.plexRotOffset)
		app.encode(int((params['StimColor1'][0])) + app.globals.plexRotOffset)
		app.encode(int((params['StimColor1'][1])) + app.globals.plexRotOffset)
		app.encode(int((params['StimColor1'][2])) + app.globals.plexRotOffset)
		
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
	app.taskObject = wilsonTask(app)
	app.globals = Holder()
	app.idlefb()
	app.startfn = RunSet
	
# This is also something that all tasks have, and it's a python thing.
# Don't touch it.
if not __name__ == '__main__':
	loadwarn(__name__)
else:
	dump(sys.argv[1])
