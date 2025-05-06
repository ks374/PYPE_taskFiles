import sys, types
from pype import *
from Numeric import *
from random import *
from shapes import *
from colors import *
from fixationTask import fixationTask

class orientationTask(fixationTask):

    def __init__(self, app):
        self.createParamTable(app)
        self.app = app
        self.mySprites = list()
        self.numStim = 0
        self.mySpriteList = list()
        self.mySpriteInfo = list()

    def createStimuli(self,app):
        self.params = self.myTaskParams.check()
        params = self.params
        self.mySprites = list()
        self.numStim = 0
        self.mySpriteList = list()

        myWidth = params['Width']
        aspect = params['Aspect_Ratio']
        myHeight = myWidth/aspect
        myColor = params['Color']
        orientations = params['Orientation']
        myShapes = eval(params['Shape'])
        #myRadius = params['RF Radius']
        myFB = app.fb
        myX = params['RF_Center_X']
        myY = params['RF_Center_Y']
        randomize_stims = params['randomize_stimuli']
        myBG = params['bg_during']

        myRots = arange(0,360,360/orientations)

        numShapes = len(myShapes)
        numRots = len(myRots)
        
        for i in arange(0, numShapes):
            for j in arange(0, numRots):
                if(hasPerfectSymmetry(myShapes[i], myWidth, myHeight):
                   if(j == 0):
                      s = shapeDict.get(myShapes[i],0)(myWidth, myHeight, myFB, myColor, 360-myRots[j], myX, myY, myBG)
                      self.mySprites.append(s)
                      self.mySpriteInfo.append([myShapes[i],myRots[j]]
                elif(isSymmetricAroundVertical(myShapes[i], myWidth, myHeight)):
                      if(j < numRots/4):
                          s = shapeDict.get(myShapes[i],0)(myWidth, myHeight, myFB, myColor, 360-myRots[j], myX, myY, myBG)
                          self.mySprites.append(s)
                          self.mySpriteInfo.append([myShapes[i],myRots[j]]
                      elif(isSymmetricAroundHorizontal(myShapes[i], myWidth, myHeight)):
                          if( j %  (numRots/2) < numRots/4):
                              s = shapeDict.get(myShapes[i],0)(myWidth, myHeight, myFB, myColor, 360-myRots[j], myX, myY, myBG)
                              self.mySprites.append(s)
                              self.mySpriteInfo.append([myShapes[i],myRots[j]]
                elif(isSymmetricAroundHorizontal(myShapes[i], myWidth, myHeight)):
                      if(j < numRots/4):
                          s = shapeDict.get(myShapes[i],0)(myWidth, myHeight, myFB, myColor, 360-myRots[j], myX, myY, myBG)
                          self.mySprites.append(s)
                          self.mySpriteInfo.append([myShapes[i],myRots[j]]
                else:
                      s = shapeDict.get(myShapes[i],0)(myWidth, myHeight, myFB, myColor, 360-myRots[j], myX, myY, myBG)
                      self.mySprites.append(s)
                      self.mySpriteInfo.append([myShapes[i],myRots[j]]

#        for j in arange(0,params['nBlanks']):
#            s = createBar(myWidth, myLength, myFB,myBG, 0, myX, myY, myBG)
#            self.mySprites.append(s)
#            self.spriteInfo.append(99,0)
        numUniqueStims = len(self.mySprites)
        stimNumbers = arange(0,numUniqueStims)

        for i in arange(0,params['nRepsPerStim']):
            if(randomize_stims):
                 shuffle(stimNumbers)
            self.mySpriteList.extend(stimNumbers)
            self.numStim = self.numStim + len(self.mySprites)
        self.myWidth = newW
        self.myHeight = newH
        self.myAspect = aspect
        self.myOrientation = orientations
        self.myShape = myShapes
        self.myColor = myColor
        self.myFB = myFB
        self.myX = myX
        self.myY = myY
        self.mySprite = s
 
 
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
		("Stimulus Pres Params", None, None),
                ("Shape",	"[0]",		   	is_int, "select shapes: 0:rectangle, 4: ellipse, 5: diamond, 6: star"),
                ("Aspect_Ratio",    "1.0", is_float, "Aspect Ratio (Width/Height)"),
                ("Width",    "1", is_int, "Width of stimulus in pixels"),
                ("nRepsPerStim",    "3", is_int, "Number of repetitions of each stimulus to present"),
                ("nBlanks",    "3", is_int, "The number of blank stimuli to present per block"),
                ("Color", "(184,1,1)", is_color, "The color of the stimulus"),
                ("Orientations",    "8", is_int, "The number of Orientation to test. Note that stims rotation clockwise."),
                #("overlap","1",is_float,"The amount of space in sprite widths between stimuli locations(pos = space between, 0 = perfect tiling, neg = equals overlap. Note that this must be > -1 "),
                ("bg_during", "(10, 10, 10)", is_color, "The background color during stimulus presentation"),
                ("bg_before", "(10, 10, 10)", is_color, "The background color before stimulus presentation"),
		("randomize_stimuli", 0, is_boolean, "Whether or not to randomize stimuli within repetitions."),
                ("RF_Params",None,None),
      		("RF_Center_X", "0",is_int,"X coordinate of the receptive field center in pixels"),
      		("RF_Center_Y", "0",is_int,"Y coordinate of the receptive field center in pixels"),
                #("RF Radius", "100", is_int, "Stimuli are presented over 2x the RF radius"),
                ("Task Params", None, None),
                ("iti",	"2500",		   	is_int, "Inter-trial interval"),
		("IStime",	"200",		   	is_int, "Inter-stimulus interval"),
		("stimon",	"500",			is_int, "Stimulus presentation"),
		("nstim",	"5",			is_int, "Number of stimuli"),
      		("Fixation Params", None, None, "Fixation Parameters"),
       		("fixcolor1",	"(255,255,255)",is_color, 'Color of the fixation dot'),
		("fixcolor2",	"(128,128,128)",is_color),
		("min_err",		"0",		   	is_int),
		("max_err",		"100",		   	is_int),
		("fixwait",		"100",		   	is_int),
		("Reward Params", None, None),
		("numdrops",    "8",           is_int, "Number of juice drops"),
		("rmult",		"1.0",		   	is_float),
		("Misc Params", None, None, "Miscelaneous Parameters"),
		("Recent Buffer Size", "50", is_int, "The number of trials to use to calculate recent performance"),
		("pause_color", "(150,0,0)", is_color, "The screen will turn this color when the task is paused")
 		), file=parfile)
                #("Spacing", "1", is_float, "The number of units of length that separates each stimulus. e.g., .5 means that each stimuli overlaps the previous one by half of length, 2 means that there is length pixels of space between each stimulus")
 

    def cleanup(self, app):
        #delete parameter table and anything else we created
        self.myTaskParams.save()
        self.myTaskButton.destroy()
        self.myTaskNotebook.destroy()
        #app.globals.destroy()
        #self.myTaskParams.destroy()
        if(len(self.mySprites) > 0):
            self.mySprite.__del__()
            for i in arange(0,len(self.mySprites)):
                self.mySprites[i].__del__()

    

    def encodeISI(self,app,sIndex):
        sPosIndex = self.mySpriteList[sIndex]
        myInfo = self.spriteInfo[sPosIndex]
	app.encode_plex('stimShape')
        app.encode_plex(int(myPos[0]))
        app.encode_plex('stimOrientation')
	app.encode_plex(int(myPos[1]+pype_plex_code_dict(pypeplexRotOffset)))


    def encodeTaskParameters(self,app):
        #encode task parameters
        params = self.myTaskParams.check()
	app.encode_plex('rfx')
	app.encode_plex(params['RF_Center_X']+ app.globals.yOffset)
	app.encode_plex('rfy')
	app.encode_plex(params['RF_Center_Y'] + app.globals.yOffset)
	app.encode_plex('iti')
	app.encode_plex(int(params['iti']))
	app.encode_plex('stim_time')
	app.encode_plex(int(params['stimon']))
	app.encode_plex('isi')
	app.encode_plex(int(params['IStime']))
	app.encode_plex('numstim')
	app.encode_plex(int(params['nstim']))

	app.encode_plex('color')
	colorTuple = self.myColor
        app.encode_plex(int(colorTuple[0] + app.globals.plexRotOffset))
	app.encode_plex(int(colorTuple[1] + app.globals.plexRotOffset))
	app.encode_plex(int(colorTuple[2] + app.globals.plexRotOffset))

        app.encode_plex('stimWidth')
	app.encode_plex(self.myWidth)
        app.encode_plex('stimHeight')
	app.encode_plex(self.myHeight)
        app.encode_plex('stimShape')
	app.encode_plex(self.myShape)



        #encode the following?
        ##	  self.myWidth
        ##        self.myLength
        ##        self.myAspect 
        ##        self.myOrientation 
        ##        self.myShape 
        ##        self.myFB 
        ##        self.myX 
        ##        self.myY 

    def encodeITI(self,app):
        pass

    def getSprite(self, index):
        return self.mySprites[self.mySpriteList[index]]

    def getNumStim(self):
        return self.numStim
