## simple CueTASK
## jkb, 6/27/08

import sys, types
from pype import *
from Numeric import *
from random import *
from shapes import *
from simpcue_shapes import *
from fixationTask import fixationTask


class simpcueTask(fixationTask): 			#  task as subclass of fixation task
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
		self.mode_idlist= list()			# (1)angle (2)spline (3)dots 4(lines)
		self.numdot_idlist= list()		# number of dots/lines (excluding vertex in dots case)
		## LOCAL VARIABLES FROM PTABLE
		myFB = app.fb
		myX = params['RF_Center_X']
		myY = params['RF_Center_Y']
		myBG = params['bg_during']
		## Stimulus and stimulus presentation params
		randomize_stims = params['randomize_stimuli']
		line_width= params['line_width']
		dotrad= params['dotrad']
		RFprop=params['RFprop']
		seg_prop=params['seg_prop']
		Splineprop=params['Splineprop']
		numdots= eval(params['numdot_list'])
		myStimColor1= params['StimColor1']
		smp=params['smp']
		P= app.getcommon()		# stores all rig and subject parameters within P.
		# SCALING
		monppd= P['mon_ppd']
		ecc = ((myX**2.0)+(myY**2.0))**0.5     # use this to scale points (pass to b8points) once settled
		myRFsize= int(round(monppd+ 0.625*ecc))
		myWidth=1.2*myRFsize
		myLength= myWidth
		# Scale line segment_length to be fixed proportion of min(perispacelist)
		minperispace=(myRFsize*RFprop)/((max(numdots))*2.0)
		seg_length=minperispace*seg_prop
		
		
		all_angles=[45,90,135]
		all_rots=[0,45,90,135,180,225,270,315]
		for theta in all_angles:
			for dummy in all_rots:
				theta_1=theta*(pi/180.)
				s_angle,s_spline=createAngleContourstim(myWidth, myLength, myFB, myStimColor1,myX, myY, myBG, line_width,theta_1,myRFsize,RFprop,Splineprop,smp)
				s_angle.rotate(dummy)
				s_spline.rotate(dummy)
				self.mySprites.append(s_angle)
				self.mySprites.append(s_spline)
				#2 sprites each time through loop, each has same angle,rot,numdot, but diff mode
				myDummysubtendedlist=[theta]*2
				myDummyrotlist=[dummy]*2
				myDummymodelist=[1,2]
				myDummynumdotlist=[0]*2
				# rotation 0 corresponds to 270degrees, the way things drawn
				self.subtended_idlist.extend(myDummysubtendedlist)
				self.rot_idlist.extend(myDummyrotlist)
				self.mode_idlist.extend(myDummymodelist)
				self.numdot_idlist.extend(myDummynumdotlist)
				for myNumdot in numdots:	
					s1,s2 = createsimpcuestim(myWidth, myLength, myFB, myStimColor1,myX, myY, myBG,myNumdot, line_width,dotrad,seg_length,theta_1,myRFsize,RFprop)
					s1.rotate(dummy)
					s2.rotate(dummy)
					self.mySprites.append(s1)
					self.mySprites.append(s2)
					#2 sprites each time through loop, each has same angle,rot,numdot,bu diff mode
					myDummysubtendedlist=[theta]*2
					myDummyrotlist=[dummy]*2
					myDummymodelist=[3,4]
					myDummynumdotlist=[myNumdot]*2
					# rotation 0 corresponds to 270degrees, the way things drawn
					self.subtended_idlist.extend(myDummysubtendedlist)
					self.rot_idlist.extend(myDummyrotlist)
					self.mode_idlist.extend(myDummymodelist)
					self.numdot_idlist.extend(myDummynumdotlist)
		# APPEND BLANKS TO SPRITELIST (color=mybg)
		for j in arange(0,params['nBlanks']):
			s = createBar(myWidth, myLength, myFB,myBG, 360, myX, myY, myBG)
			self.subtended_idlist.append(0)
			self.rot_idlist.append(0)
			self.mode_idlist.append(0)
			self.numdot_idlist.append(0)
			
		
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
		self.myBG= myBG
		
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
			("StimColor1","(164, 1, 1)",    is_color, "color of stimulus"),
			("nRepsPerStim",    "10", is_int, "Number of repetitions of each stimulus to present"),
			("bg_during", "(10, 10, 10)", is_color, "The background color during stimulus presentation"),
			("bg_before", "(10, 10, 10)", is_color, "The background color before stimulus presentation"),
			("RF_Center_X", "100",is_int,"X coordinate of the receptive field center in pixels"),
			("RF_Center_Y", "-100",is_int,"Y coordinate of the receptive field center in pixels"),
			("STIMULUS params", None, None),
			("numdot_list","[1,3,5]",    is_any, "number of cues on either side of vertex"),
			("StimColor1","(164, 1, 1)",    is_color, "color of stimulus"),
			("line_width",    "2", is_int, "width tangential line cue element"),
			("dotrad",    "2", is_int, " radius of dot cue"),
			("RFprop",    ".75", is_float, "fraction of RF radius where furthest cue found"),
			("seg_prop",    ".7", is_float, "proportion of smallest perispace filled by seg... eg 1= fullcontour when perispace is smallest"),
			("Splineprop", ".2", is_float, "proportion of seg_length from vertex to nextcontrol point ...higher numbers may yield lower curvatures"),
			("smp", "2", is_int, "samples/segment in spline"),
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
			("TaskName","simpcuetest",    is_any, "TaskName"),
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
		stimparamIndex = self.mySpriteList[sIndex]	#sIndex indexes mySpritelist which indexes all other indexes
		mySubtended= int(self.subtended_idlist[stimparamIndex])
		myRot= int(self.rot_idlist[stimparamIndex])
		myMode= int(self.mode_idlist[stimparamIndex])
		myNumdot= int(self.numdot_idlist[stimparamIndex])
		
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
		
		app.encode_plex('gen_submode')
		app.encode('gen_submode')
		app.encode_plex(myNumdot + app.globals.plexRotOffset)	
		app.encode(myNumdot + app.globals.plexRotOffset)
		
		
	
	def encodeTaskParameters(self,app):
		
		#encode task parameters
		# mode(iti),spline_prop, maybe do seg_length instead of seg_prop,
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
		
		# this is new here in wilson task (stays in simpcue)
		app.encode_plex('line_width')
		app.encode('line_width')
		app.encode_plex(int(params['line_width'])+ app.globals.plexRotOffset)
		app.encode(int(params['line_width'])+ app.globals.plexRotOffset)
		
		# this is new here in simplecuetask. NEED TO DEAL WITH FLOATS
		app.encode_plex('dot_rad')
		app.encode('dot_rad')
		app.encode_plex(int(params['dotrad'])+ app.globals.plexRotOffset)
		app.encode(int(params['dotrad'])+ app.globals.plexRotOffset)
# 		
# 		app.encode_plex('stimWidth')
# 		app.encode('stimWidth')
# 		app.encode_plex(int(params['RFprop'])+ app.globals.plexRotOffset)
# 		app.encode(int(params['RFprop'])+ app.globals.plexRotOffset)
# 		
# 		app.encode_plex('occlshape')
# 		app.encode('occlshape')
# 		app.encode_plex(int(params['seg_prop'])+ app.globals.plexRotOffset)
# 		app.encode(int(params['seg_prop'])+ app.globals.plexRotOffset)

# 		app.encode_plex('position')
# 		app.encode('position')
# 		app.encode_plex(int(params['Splineprop'])+ app.globals.plexRotOffset)
# 		app.encode(int(params['Splineprop'])+ app.globals.plexRotOffset)
		
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
	app.taskObject = simpcueTask(app)
	app.globals = Holder()
	app.idlefb()
	app.startfn = RunSet
	
# This is also something that all tasks have, and it's a python thing.
# Don't touch it.
if not __name__ == '__main__':
	loadwarn(__name__)
else:
	dump(sys.argv[1])
