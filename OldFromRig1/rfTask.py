import sys, types
from pype import *
from Numeric import *
from random import *
from shapes import *
from colors import *
from b8StimFactory import *
from fixationTask import fixationTask

def RunSet(app):
    app.taskObject.runSet(app)

def cleanup(app):
    app.taskObject.cleanup(app)


def main(app):
    app.taskObject = rfTask(app)
    app.globals = Holder()
    app.idlefb()
    app.startfn = RunSet

# This is also something that all tasks have, and it's a python thing.
# Don't touch it.

if not __name__ == '__main__':
	loadwarn(__name__)
else:
	dump(sys.argv[1])



class rfTask(fixationTask):

    def __init__(self, app):
        self.createParamTable(app)
        self.app = app
        self.mySprites = list()
        self.numStim = 0
        self.mySpriteList = list()
        self.spritePositions = list()
        self.achromaticI = 13
        self.minLum = 4
        self.maxLum = 12
        self.lumDicts = colorDicts

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
        orientation = params['Orientation']
        myShape = params['Shape']
        myRadiusX = params['RF Radius X']
        myRadiusY = params['RF Radius Y']
        myFB = app.fb
        myX = params['RF_Center_X']
        myY = params['RF_Center_Y']
        randomize_stims = params['randomize_stimuli']
        myBG = params['bg_during']
        sampling = params['sampling']
        occl_H_offset = params['occl_H_offset']

        XOverlap = params['XOverlap']
        YOverlap = params['YOverlap']
        MaxHExtent = params['Max Horizontal Extent']
        MaxVExtent = params['Max Vertical Extent']
        
        #first, create a sprite and rotate it
        if(myShape >= 801 and myShape <= 851):
            myFac = b8StimFactory(myWidth*4,myWidth)
            s = myFac.getB8Stim(myShape-800, sampling,myFB,myColor,360-orientation, myX, myY,myBG+(0,))
            s.myW = myWidth
            s.myH = myWidth
        elif(myShape >= 901 and myShape <= 951):
            myFac = b8StimFactory(myWidth*4,myWidth)
            s = myFac.getB8StimAsOccluder(myShape-900, sampling,myFB,myBG,360-orientation, myX, myY,myColor,sp_h_offset=myWidth*occl_H_offset)
            s.myW = myWidth
            s.myH = myWidth
            s.alpha_aperture(myWidth, x=0, y=0)
        elif(myShape == 7):
              spat_freq = params['spatial frequency']
              phase = params['phase']
              contrast = params['contrast']/100.0
              bg_lum = params['bg_lum']
              isCircle = params['isCircle']
              minTuple = self.lumDicts[self.minLum][self.achromaticI]
	      maxTuple = self.lumDicts[self.maxLum][self.achromaticI]
              bgTuple = self.lumDicts[bg_lum][self.achromaticI]
              lowerR = bgTuple[0] - (bgTuple[0] - minTuple[0]) * contrast 
              lowerG = bgTuple[1] - (bgTuple[1] - minTuple[1]) * contrast 
              lowerB = bgTuple[2] - (bgTuple[2] - minTuple[2]) * contrast 
              upperR = bgTuple[0] + (maxTuple[0] - bgTuple[0]) * contrast 
              upperG = bgTuple[1] + (maxTuple[1] - bgTuple[1]) * contrast 
              upperB = bgTuple[2] + (maxTuple[2] - bgTuple[2]) * contrast 
              upperColor = (upperR,upperG,upperB)
              lowerColor = (lowerR, lowerG, lowerB)

              s = createSinusoid(myWidth,myWidth,myFB, 360-orientation, myX, myY, myBG+(255,),lowerColor, upperColor,spat_freq,phase, isCircle)
              s.myW = myWidth
              s.myH = myWidth
        else:
            s = shapeDict.get(myShape,0)(myWidth, myHeight,myFB, myColor, 360-orientation, myX, myY, myBG+(0,))

        newW = s.myW
        newH = s.myH
        newX = s.x
        newY = s.y
        print "Sprite is at %d, %d width = %d, height = %d" % (s.x, s.y, s.myW, s.myH)

        #now clone and move sprite

        startingX = myX - 2*myRadiusX + newW/2
        startingY = myY + 2*myRadiusY - newH/2
        #print 'x'
        #print newW
        #print myX
        #print startingX
        #print 'y'
        #print newH
        #print myY
        #print startingY
        endingX = myX + 2*myRadiusX - newW/2
        endingY = myY - 2*myRadiusY + newH/2
        if(XOverlap <= -1.0):
            XOverlap = -.95
        if(YOverlap <= -1.0):
            YOverlap = -.95

        #print 'ending'
        #print endingX
        #print endingY

        xOverlapDist  = XOverlap * newW
        yOverlapDist  = YOverlap * newH
        #print newW

        xIncrement = xOverlapDist + abs(newW)
        yIncrement = yOverlapDist + abs(newH)
        #print xOverlapDist
        #print yOverlapDist
        #print xIncrement
        #print yIncrement
        #print startingX
        #print endingX
        #print xIncrement
        #print startingY
        #print endingY
        #print yIncrement
        #print arange(startingX,endingX,xIncrement)
        #print arange(min(startingY,endingY), max(startingY, endingY), yIncrement)
        for i in arange(startingX,endingX,xIncrement):
            if(abs(i) <= MaxHExtent):
                for j in arange(min(startingY,endingY), max(startingY, endingY), yIncrement):
                    if( abs(j) <= MaxVExtent):
                        newS = s.clone()
                        newS.moveto(int(round(i)),int(round(j)))
                        #print "moving to %d, %d" % ( int(round(i)),int(round(j)) )
                        self.mySprites.append(newS)
                        self.spritePositions.append([int(round(i)),int(round(j))])
                        #print "adding to sprite positions to %d, %d" % ( int(round(i)),int(round(j)) )
        #print self.spritePositions
        numUniqueStims = len(self.mySprites)
        stimNumbers = arange(0,numUniqueStims)
        for i in arange(0,params['nRepsPerStim']):
            if(randomize_stims):
                 shuffle(stimNumbers)
            self.mySpriteList.extend(stimNumbers)
            self.numStim = self.numStim + len(self.mySprites)
        self.myWidth = int(newW)
        self.myHeight = int(newH)
        self.myAspect = aspect
        self.myOrientation = orientation
        self.myShape = myShape
        self.myColor = myColor
        self.myFB = myFB
        self.myX = myX
        self.myY = myY
        self.mySprite = s
 
 
    def createParamTable(self,app):
        #create parameter table and window to go along with it
        P = app.getcommon()

	self.myTaskButton = app.taskbutton(text=__name__, check=1)
	self.myTaskNotebook = DockWindow(title=__name__, checkbutton=self.myTaskButton)
	parfile = "%s.%s" % (app.taskname(), P['subject'])
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
                ("Shape",	"0", is_int, "select shape: 0:rectangle, 4: ellipse, 5: diamond, 6: star 7:Sinusoidal Grating 801-851: B8 stims 1-51 901-951: newAim1 Midground stims 1-51"),
                ("Aspect_Ratio",    "1.0", is_float, "Aspect Ratio (Width/Height)"),
                ("Width",    "100", is_int, "Width of stimulus in pixels"),
                ("nRepsPerStim",    "3", is_int, "Number of repetitions of each stimulus to present"),
                ("nBlanks",    "3", is_int, "The number of blank stimuli to present per block"),
                ("Color", "(184,1,1)", is_color, "The color of the stimulus"),
                ("Orientation",    "0", is_int, "Orientation in degrees of the stimulus. Note that stims rotation clockwise."),
                ("XOverlap","-.6",is_float,"The amount of horizontal distance in sprite widths between stimuli locations(pos = space between, 0 = perfect tiling, neg = equals overlap. Note that this must be > -1 "),
                ("YOverlap","-.6",is_float,"The amount of vertical distance in sprite widths between stimuli locations(pos = space between, 0 = perfect tiling, neg = equals overlap. Note that this must be > -1 "),
                ("bg_during", "(35,19,14)", is_color, "The background color during stimulus presentation"),
                ("bg_before", "(35,19,14)", is_color, "The background color before stimulus presentation"),
		("randomize_stimuli", 0, is_boolean, "Whether or not to randomize stimuli within repetitions."),
                ("Max Horizontal Extent", 700, is_int, "Maximum displacement in horizontal direction that the center of a stimulus will be displayed"),
                ("Max Vertical Extent", 500, is_int, "Maximum displacement in vertical direction that the center of a stimulus will be displayed"),
                ("Shape Specific _Params",None,None),
                ("spatial frequency",    "2.0", is_float, "Spatial Frequency of grating (shape 7) in cycles/stimulus"),
                ("phase",    "2.0", is_float, "Phase of grating (shape 7) in degrees"),
                ("contrast",    "50.0", is_float, "Contrast of grating in percent"),
                ("bg_lum",    "8", is_int, "Luminance of background (4,8,12 or 18)"),
                ("isCircle",   0, is_int, "if 1 then draw the sinusoidal grating as a circle"),
                ("sampling",    "100", is_int, "# of pixels between each control point when using shapes 801-851 or 901-951."),
                ("occl_H_offset",    ".66", is_float, "Fraction of RF to displace occluder for shapes 901-951"),
                ("RF_Params",None,None),
      		("RF_Center_X", "200",is_int,"X coordinate of the receptive field center in pixels"),
      		("RF_Center_Y", "-200",is_int,"Y coordinate of the receptive field center in pixels"),
                ("RF Radius X", "100", is_int, "Stimuli are presented over 2x the RF radius X in the X direction"),
                ("RF Radius Y", "100", is_int, "Stimuli are presented over 2x the RF radius Y in the Y direction"),
                ("Task Params", None, None),
                ("iti",	"2500",		   	is_int, "Inter-trial interval"),
		("IStime",	"200",		   	is_int, "Inter-stimulus interval"),
		("stimon",	"300",			is_int, "Stimulus presentation"),
		("nstim",	"4",			is_int, "Number of stimuli"),
      		("Fixation Params", None, None, "Fixation Parameters"),
       		("fixcolor1",	"(255,255,255)",is_color, 'Color of the fixation dot'),
		("fixcolor2",	"(128,128,128)",is_color),
		("min_err",		"0",		   	is_int),
		("max_err",		"100",		   	is_int),
		("fixwait",		"100",		   	is_int),
		("Reward Params", None, None),
		("numdrops",    "6",           is_int, "Number of juice drops"),
                ("rmult",		"1.0",		   	is_float),
		("Record File Params", None, None, "Params for setting name of record file"),
                ("Use Special Name", "0", is_boolean, "If 1 then the record file name will be AnimalPrefixDate_TaskName_CellGroup_Iteration.rec"),
                ("RFDirectory", "/home/shapelab/recordFiles/", is_any, "Directory to use for Record Files"),               
                ("AnimalPrefix", "m", is_any, "Animal Prefix to use"),
		("Date","080325",    is_any, "Date to use "),
		("TaskName","rftask",    is_any, "TaskName"),
		("CellGroup","01",    is_int, "# of cell group encountered today"),
		("Iteration","01",    is_int, "# of times this task has been run on this cell group"),
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
        del self.mySpriteList
        #app.globals.destroy()
        #self.myTaskParams.destroy()
        #if(len(self.mySprites) > 0):
        #    self.mySprite.__del__()
        #    for i in arange(0,len(self.mySprites)):
        #       self.mySprites[i].__del__()
        del self.spritePositions
        del self.mySprites
    

    def encodeISI(self,app,sIndex):
        sPosIndex = self.mySpriteList[sIndex]
        myPos = self.spritePositions[sPosIndex]
	app.encode_plex('position')
        app.encode_plex(int(myPos[0] + 2*app.globals.yOffset))
	app.encode_plex(int(myPos[1] + 2*app.globals.yOffset))
	app.encode('position')
        app.encode(int(myPos[0] + 2*app.globals.yOffset))
	app.encode(int(myPos[1] + 2*app.globals.yOffset))
	#print "sIndex: %d, sPosIndex: %d" % (sIndex, sPosIndex)
        #print "encoded sprite positions %d, %d as %d, %d" % (myPos[0], myPos[1],int(myPos[0] + 2*app.globals.yOffset), int(myPos[1] + 2*app.globals.yOffset) )

    def encodeTaskParameters(self,app):
        #encode task parameters
        params = self.myTaskParams.check()
	app.encode_plex('rfx')
	app.encode_plex(params['RF_Center_X']+ 2*app.globals.yOffset)
	app.encode_plex('rfy')
	app.encode_plex(params['RF_Center_Y'] + 2*app.globals.yOffset)
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

	app.encode('rfx')
	app.encode(params['RF_Center_X']+ 2*app.globals.yOffset)
	app.encode('rfy')
	app.encode(params['RF_Center_Y'] + 2*app.globals.yOffset)
	app.encode('iti')
	app.encode(int(params['iti']))
	app.encode('stim_time')
	app.encode(int(params['stimon']))
	app.encode('isi')
	app.encode(int(params['IStime']))
	app.encode('numstim')
	app.encode(int(params['nstim']))

	app.encode('color')
        app.encode(int(colorTuple[0] + app.globals.plexRotOffset))
	app.encode(int(colorTuple[1] + app.globals.plexRotOffset))
	app.encode(int(colorTuple[2] + app.globals.plexRotOffset))

        app.encode('stimWidth')
	app.encode(self.myWidth)
        app.encode('stimHeight')
	app.encode(self.myHeight)
        app.encode('stimShape')
	app.encode(self.myShape)


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

    def warnNumStim(self):
        return 1

    def getRecordFileName(self): #gets the record file for this task 
        params = self.myTaskParams.check()
        if(params['Use Special Name']):
            filename = "%s%s%s_%s_%02d_%02d.rec" % (params['RFDirectory'],params['AnimalPrefix'],params['Date'],params['TaskName'],params['CellGroup'],params['Iteration'])
        else:
            filename = None
        return filename
