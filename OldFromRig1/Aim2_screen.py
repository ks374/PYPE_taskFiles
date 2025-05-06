import sys, types
from pype import *
from Numeric import *
from random import *
from shapes import *
from afterimage_shapes import *
from colors import *
from xFixationTask import xFixationTask
from b8StimFactory_mm import *
from stimulus import stimulus
from sets import *

def RunSet(app):
    app.taskObject.runSet(app)

def cleanup(app):
    app.taskObject.cleanup(app)

def main(app):
    app.taskObject = Aim2_screen(app)
    app.globals = Holder()
    app.idlefb()
    app.startfn = RunSet

# This is also something that all tasks have, and it's a python thing.
# Don't touch it.

if not __name__ == '__main__':
        loadwarn(__name__)
else:
        dump(sys.argv[1])

class Aim2_screen(xFixationTask):
    def __init__(self, app):
        self.createParamTable(app)
        self.app = app
        self.myStims = list()
        self.numStim = 0
        self.myStimList = list()
        self.circleMode = 1
        self.perceptMode = 1
        self.blankMode = 1
        self.complexShapeMode = 2
        self.midgroundOnlyMode = 3
        self.foregroundOnlyMode = 4
        self.positionMode = 5
        self.reverseColorMode = 6
        self.backgroundColorMode = 7
        self.sameColorMode = 8
        self.temporalDifferenceMode = 9
        self.temporalDifferenceModeMidFirst = 10 #until march 29,09 used to be foreground alone
        self.positionForegroundMode = 12
        self.accidentalContourMode = 11
        self.translationMode = 13
        self.secondStimlusMode = 14
        self.secondStimlusForegroundOnlyMode = 15
        self.secondStimlusMidgroundOnlyMode = 16
        self.locationFlipMode = 17
        self.extraComplexMode = 18
        self.extraMidgroundsMode = 19
        self.extraForegroundsMode = 20
        self.ambiguousControlMode = 21
        self.ambiguousTemporalDifferenceMode = 22
        self.albertControlMode = 23
        self.perceptModeOffset = list()
        self.perceptModeOffset.append(None)
        self.perceptModeOffset.append(0)
        self.perceptModeOffset.append(30)
        self.perceptModeOffset.append(60)
        self.numB8Shapes = 35
        self.numPerceptObjects = 3
        self.B8ShapeSet = arange(1,self.numB8Shapes+1)
        self.B8ScreenSet = [5,6,7,10,11,13,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35,36,37]
        self.AIM1AlternateForeground = [2,10,11,16,17,24,25,28,31,40,43,46,47,50]
        self.AIM1AlternateMidground = [2,10,11,16,17]
        b8Screen = Set(self.B8ScreenSet)
        AIM1AlternateForeground = Set(self.AIM1AlternateForeground)
        tempSet = b8Screen.union(AIM1AlternateForeground)
        self.unionedAIM1AlternateForeground = list(tempSet)
        self.blankID = 1
        self.circleID= 2
        self.reverseCircleSubmode = 1
        self.reverseComplexSubmode = 2
        self.reverseMidgroundSubmode = 3
        self.reverseForegroundSubmode = 4
        self.foregroundDepth = 3
        self.betweenForeAndMid = 4
        self.midgroundDepth = 5
        self.perceptDepth = 6
        self.backgroundColorDepth = 7
        self.ambiguousDepth = 2

    def createStimuli(self,app):            #Create Stimuli - Create stimuli called at beginning
        self.params = self.myTaskParams.check()
        params = self.params
        P = app.getcommon()
        self.myStims = list()
        self.numStim = 0
        self.myStimList = list()
        myFB = app.fb
        myX = params['RF_Center_X']
        myY = params['RF_Center_Y']
        fixX = P['fix_x']
        fixY = P['fix_y']
        myBG = params['bg_during']
        randomize_stims = params['randomize_stimuli']
        midgroundColor = params['MidgroundColor']
        foregroundColor = params['ForegroundColor']
        self.numPoints = params['numPoints']
        self.myBG = myBG
        self.myFB = myFB
        self.myX = myX
        self.myY = myY
        self.fixX = fixX
        self.fixY = fixY
        self.myBG = myBG
        self.midgroundColor = midgroundColor
        self.foregroundColor = foregroundColor
        self.randomize = randomize_stims
        stims = list()
        self.ecc = ( (myX-fixX)**2 + (myY-fixY)**2)**0.5
        if(params['RF Scale On Ecc']):
                self.size = int((P['mon_ppd'] * params['RF Offset']) +  (params['RF Scaling'] * self.ecc))
        else:
                self.size = 2*params['RF Radius']

        #self.size is diameter of receptive field, also width and height of bounding square
        self.diameter = self.size
        self.radius = self.size/2.0
        self.rots = params['NumRotations']
        self.rotVals = range(0,360+(360/self.rots)-(360/self.rots),(360/self.rots) )
        self.myForegroundXOffset = params['foregroundXOffset'] * self.size/2
        self.myForegroundYOffset = params['foregroundYOffset'] * self.size/2
        self.myMidgroundXOffset = params['circleXOffset'] * self.size/2
        self.myMidgroundYOffset = params['circleYOffset'] * self.size/2
        self.myMidgroundScaling = params['circleScaling']
        self.myForegroundScaling = params['foregroundScaling'] 
        self.barXOffset= params['barXOffset']  * self.size/2
        self.barYOffset= params['barYOffset']  * self.size/2
        self.barAspect = params['barAspect']
        self.barScaling = params['barScaling']
        self.hour_vert_curv = params['hour_vert_curv']
        self.hour_horiz_curv = params['hour_horiz_curv']
        self.myFactory = b8StimFactory_mm(self.diameter*2,self.radius)
        self.sampling = params['B8_Sampling']
        self.perceptShapes = eval(params['Percept Shapes to Use'])

        #Not sure why I am keeping this
        self.myComplexStimuli = (self.numB8Shapes+1)*[None] #list of all complex shape stimulus (Not Sprite!) objects
        self.myMidgroundStimuli = (self.numB8Shapes+1)*[None] #list of all midground shape stimulus (Not Sprite!) objects used to do temporal control
        self.myForeground = (self.numB8Shapes+1)*[None]  #list of all foreground sprites - for making complex shapes and midground
        self.myForegroundinBG = (self.numB8Shapes+1)*[None]  #list of all foreground stims drawn in background color for making and midground and position stims
        self.myRevForeground = (self.numB8Shapes+1)*[None] #list of all reverse color foreground stims - for making complex shapes and midground
        self.myPercepts = (self.numPerceptObjects+1)*[None]
        circleSprite = None
        revColorCircle = None

        #Mode 1 - Circle
        for k in arange(0, size(self.perceptShapes,0)):
            stimList,dummyVar = self.getPercept(self.perceptMode,1,self.perceptShapes[k], None, self.midgroundColor, None, self.rotVals)
            for i in arange(0,(params['PerceptsPerBlock'])):
                self.myStims.extend(stimList)
        if(params['UseAllComplexStims'] == 1):
            complexStims = self.B8ShapeSet
        else:           
            complexStims = eval(params['ComplexStimNums'])

        #Mode 2 - Complex Shape Mode AKA Occluded Mode
        if(params['PresentComplexStims']):
            for k in arange(0, size(self.perceptShapes,0)):
                for j in arange(0,len(complexStims)):
                    stimList = self.getComplex(self.complexShapeMode+self.perceptModeOffset[self.perceptShapes[k]],1, self.perceptShapes[k], complexStims[j], self.midgroundColor, self.foregroundColor, self.rotVals,cacheSprite=1, useCache=1)
                    self.myStims.extend(stimList)

        #Mode 3 - Midground Mode AKA Background Occluder Mode
        if(params['UsePreSelectedMidgrounds'] == 1):
            midgroundsStims = self.B8ShapeSet
        elif(params['UsePreSelectedMidgrounds'] == 2):
            midgroundsStims = self.B8ScreenSet
        elif(params['UsePreSelectedMidgrounds'] == 3):
            midgroundsStims = self.AIM1AlternateMidground
        else:           
            midgroundsStims = eval(params['MidgroundStimNums'])
        if(params['PresentMidgroundStims']):
            for k in arange(0, size(self.perceptShapes,0)):
                #print self.perceptShapes
                #print k
                #print self.perceptModeOffset[self.perceptShapes[k]]
                for j in arange(0,len(midgroundsStims)):
                    stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[k]],1, self.perceptShapes[k], midgroundsStims[j], self.midgroundColor, self.foregroundColor, self.rotVals,cacheSprite=1, useCache=1)
                    self.myStims.extend(stimList)

        #Mode 4 - Foreground AKA Occluder
        if(params['UsePreSelectedForegrounds'] == 1):
            foregroundStims = self.B8ShapeSet
        elif(params['UsePreSelectedForegrounds'] == 2):
            foregroundStims =self.B8ScreenSet
        elif(params['UsePreSelectedForegrounds'] == 3):
            foregroundStims = self.AIM1AlternateForeground
        elif(params['UsePreSelectedForegrounds'] == 4):
            foregroundStims = self.unionedAIM1AlternateForeground
        else:           
            foregroundStims = eval(params['ForegroundStimNums'])
        if(params['PresentForegroundStims']):
            for j in arange(0,len(foregroundStims)):
                stimList = self.getForeground(self.foregroundOnlyMode,1, None, foregroundStims[j], self.midgroundColor, self.foregroundColor, self.rotVals,cacheSprite=1, useCache=1)
                self.myStims.extend(stimList)

        ###End of Non-Blank Modes
        #Mode 1 Add blanks
        for j in arange(0,params['nBlanks']):
            stim = stimulus(self.blankMode,self.blankID,0)
            s = createBar(self.radius, self.radius, myFB,myBG, 0, myX, myY, myBG)
            stim.addSprite(s, myBG, 0)
            self.myStims.append(stim)
        numUniqueStims = len(self.myStims)
        stimNumbers = arange(0,numUniqueStims)

        for i in arange(0,params['nRepsPerStim']):
            if(randomize_stims):
                 shuffle(stimNumbers)
            self.myStimList.extend(stimNumbers)
            self.numStim = self.numStim + len(self.myStims)

    def createParamTable(self,app):         #The parameters for this class
        #create parameter table and window to go along with it
        self.myTaskButton = app.taskbutton(text=__name__, check=1)
        self.myTaskNotebook = DockWindow(title=__name__, checkbutton=self.myTaskButton)
        P = app.getcommon()
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
                ("RF_Params",None,None),
                ("RF_Center_X", "0",is_int,"X coordinate of the receptive field center in pixels"),
                ("RF_Center_Y", "0",is_int,"Y coordinate of the receptive field center in pixels"),
                ("RF Scale On Ecc", "1", is_boolean, "Whether or not to scale based on eccentricity"),
                ("RF Scaling", ".625", is_float, "If RF_Scale_On_Ecc is 1, Size of RF in degrees equals eccentricity * RF Scaling + RF Offset"),
                ("RF Offset", ".5", is_float, "If RF_Scale_On_Ecc is 1,Size of RF in degrees equals eccentricity * RF Scaling + RF Offset"),
                ("RF Radius", "100", is_int, "IF RF_Scale_On_Ecc is 0, this is the radius of the RF in pixels"),
                ("ShowRFSprite", "1", is_boolean, "If 1 display white circle around RF perimeter (use only during testing)"),
                ("Task Params", None, None),
                ("iti",	"1500", is_int, "Inter-trial interval"),
                ("IStime", "200", is_int, "Inter-stimulus interval"),
                ("AddExtraISI", "1", is_int, "Set to 1 to add another ISI after the last stimulus in a trial, 0 otherwise"),
                ("stimon", "300", is_int, "Stimulus presentation"),
                ("nstim", "4", is_int, "Number of stimuli"),
                ("Fixation Params", None, None, "Fixation Parameters"),
                ("fixcolor1", "(255,255,255)", is_color, 'Color of the fixation dot'),
                ("fixcolor2", "(128,128,128)",is_color),
                ("min_err", "0", is_int),
                ("max_err", "100", is_int),
                ("fixwait", "100", is_int),
                ("Record File Params", None, None, "Params for setting name of record file"),
                ("Use Special Name", "0", is_boolean, "If 1 then the record file name will be AnimalPrefixDate_TaskName_CellGroup_Iteration.rec"),
                ("RFDirectory", "\\home\\shapelab\\recordFiles\\", is_any, "Directory to use for Record Files"),               
                ("AnimalPrefix", "m", is_any, "Animal Prefix to use"),
                ("Date","080325", is_any, "Date to use "),
                ("TaskName","newAIM1", is_any, "TaskName"),
                ("CellGroup","01", is_int, "# of cell group encountered today"),
                ("Iteration","01", is_int, "# of times this task has been run on this cell group"),
                ("Stimulus Params", None, None),
                ("MidgroundColor", "(161, 34, 35)", is_color, "Color of the midground shape in rgb"),
                ("ForegroundColor", "(29, 34, 225)", is_color, "Color of the foreground shape in rgb"),
                ("NumRotations", "8", is_int, "Number of rotations to use"),
                ("B8_Sampling", "100",is_int,"Number of points in each b-spline"),
                ("Stimulus Pres Params", None, None),
                ("nRepsPerStim", "3", is_int, "Number of repetitions of each stimulus to present"),
                ("nBlanks", "3", is_int, "The number of blank stimuli to present per block"),
                ("PerceptsPerBlock", "3", is_int, "The number of each percept to present per block"),
                ("bg_during", "(35, 19, 14)", is_color, "The background color during stimulus presentation"),
                ("bg_before", "(35, 19, 14)", is_color, "The background color before stimulus presentation"),
                ("randomize_stimuli", 0, is_boolean, "Whether or not to randomize stimuli within repetitions."),
                ("Midground Mode Params", None, None),
                ("PresentMidgroundStims", "1", is_boolean, "If 1 then present midground stimuli"),
                ("UsePreSelectedMidgrounds", "1", is_int, "1 (all 51 shapes), 2 (29 shape b8 screen), 3 (5 midground shapes for 14 shape alternate aim1) anything else use what is in MidgroundStimNums"),
                ("MidgroundStimNums","[]",    is_any, "If UsePreSelectedMidgrounds is 0 then instead use only the midgrounds listed here(1-51)"),
                ("midgroundXOffset", "-.25",is_float,"Number of rf rads that the midground object is shifted to the right"),
                ("midgroundYOffset", "0.0",is_float,"Number of rf rads that the midground object is shifted up"),
                ("midgroundScaling", ".50",is_float,"Radius of the circle circumscribing the midground object divided by the rf radius"),
                ("Percept Mode Params", None, None),
                ("Percept Shapes to Use", "[1, 2, 3]", is_any, "List of shapes (1:circle, 2:bar, 3:hourglass) to use for percept and midground objects"),
                ("circleXOffset", "-.25",is_float,"Number of rf rads that the circle is shifted to the right"),
                ("circleYOffset", "0.0",is_float,"Number of rf rads that the circle is shifted up"),
                ("circleScaling", ".50",is_float,"Radius of the circle circumscribing the midground object divided by the rf radius"),
                ("barXOffset", "-.25",is_float,"Number of rf rads that the bar and hourglass are shifted to the right"),
                ("barYOffset", "0.0",is_float,"Number of rf rads that the bar and hourglass are shifted up"),
                ("barScaling", ".50",is_float,"Radius of the circle circumscribing the bar and hourglass divided by the rf radius"),
                ("barAspect", "2.0",is_float,"Aspect Ratio (width/height) of bar and hourglass stimuli"),
                ("hour_vert_curv", "1.67",is_float,"Curvature of arc on top and bottom of hourglass stimulus"),
                ("hour_horiz_curv", ".375",is_float,"Curvature of arc on left and right of hourglass stimulus"),
                ("numPoints", "8", is_int, "number of points in the star percept"),
                ("Foreground Mode Params", None, None),
                ("PresentForegroundStims", "1", is_boolean, "If 1 then present foreground stimuli"),
                ("UsePreSelectedForegrounds", "1", is_int, "1 (al 51 shapes), 2 (29 shape b8 screen), 3 (14 shape alternate aim1), 4 (union of 2 and 3) anything else use what is in ForegroundStimNums"),
                ("ForegroundStimNums","[]", is_any, "If UsePreSelectedForegrounds is not 1-3 then instead use only the foregrounds listed here(1-51)"),
                ("foregroundXOffset", ".25",is_float,"Number of rf rads that the foreground object is shifted to the right"),
                ("foregroundYOffset", "0",is_float,"Number of rf rads that the foreground object is shifted up"),
                ("foregroundScaling", ".5",is_float,"Radius of the circle circumscribing the foreground object divided by the rf radius"),
                ("Complex Mode Params", None, None),
                ("PresentComplexStims", "1", is_boolean, "If 1 then present complex stimuli"),
                ("UseAllComplexStims", "1", is_boolean, "If 1 then use all 51 complex shapes"),
                ("ComplexStimNums","[]", is_any, "If UseAllComplexStims is 0 then instead use only the complex shapes listed here(1-51)"),
                ("Reward Params", None, None),
                ("numdrops", "6", is_int, "Number of juice drops"),
                ("rmult", "1.0", is_float),
                ("Misc Params", None, None, "Miscelaneous Parameters"),
                ("RotCodeDelayTime", "30", is_int, "The amount of time in ms to wait between sending the rotation code and the mode code"),
                ("Recent Buffer Size", "50", is_int, "The number of trials to use to calculate recent performance"),
                ("pause_color", "(150,0,0)", is_color, "The screen will turn this color when the task is paused")
                ), file=parfile)

    def getRFSprite(self):
        if(self.params['ShowRFSprite']):
            circleSprite = Sprite(self.size, self.size, self.myX,self.myY,fb=self.myFB, depth=self.midgroundDepth+1, on=0,centerorigin=1)
            circleSprite.fill(self.myBG+(0,))
            circleSprite.circlefill((255,255,255),r=self.radius,x=0,y=0,width=1)
            return circleSprite
        else:
            return None

    def encodeTaskParameters(self,app):     #Encode task Params - Called at the beginning of the task
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
        app.encode_plex('add_extra_isi')
        app.encode('add_extra_isi')
        app.encode_plex(int(params['AddExtraISI'])+ app.globals.plexRotOffset)
        app.encode(int(params['AddExtraISI'])+ app.globals.plexRotOffset)
        app.encode_plex('radius')
        app.encode('radius')
        app.encode_plex(int(round(self.radius))+app.globals.yOffset)
        app.encode(int(round(self.radius))+app.globals.yOffset)

        #encode scaling parameter for RF?
        app.encode_plex('midground_info')
        app.encode_plex(int(round(params['midgroundXOffset']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode_plex(int(round(params['midgroundYOffset']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode_plex(int(round(params['midgroundScaling']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode('midground_info')
        app.encode(int(round(params['midgroundXOffset']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode(int(round(params['midgroundYOffset']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode(int(round(params['midgroundScaling']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode_plex('foreground_info')
        app.encode_plex(int(round(params['foregroundXOffset']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode_plex(int(round(params['foregroundYOffset']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode_plex(int(round(params['foregroundScaling']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode('foreground_info')
        app.encode(int(round(params['foregroundXOffset']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode(int(round(params['foregroundYOffset']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode(int(round(params['foregroundScaling']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
                

        #encode colors: bg midground foreground
        app.encode_plex('color')
        app.encode('color')
        colorTuple = self.myBG
        app.encode_plex(int(colorTuple[0] + app.globals.plexRotOffset))
        app.encode_plex(int(colorTuple[1] + app.globals.plexRotOffset))
        app.encode_plex(int(colorTuple[2] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[0] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[1] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[2] + app.globals.plexRotOffset))
        colorTuple = self.midgroundColor
        app.encode_plex(int(colorTuple[0] + app.globals.plexRotOffset))
        app.encode_plex(int(colorTuple[1] + app.globals.plexRotOffset))
        app.encode_plex(int(colorTuple[2] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[0] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[1] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[2] + app.globals.plexRotOffset))
        colorTuple = self.foregroundColor
        app.encode_plex(int(colorTuple[0] + app.globals.plexRotOffset))
        app.encode_plex(int(colorTuple[1] + app.globals.plexRotOffset))
        app.encode_plex(int(colorTuple[2] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[0] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[1] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[2] + app.globals.plexRotOffset))

    def encodeISI(self,app,myStim):                #Encode upcoming Stimlus Params - Called every ISI
        params = self.myTaskParams.check()
        rotCodeDelTime = params['RotCodeDelayTime']
        t = Timer()
        #t.reset()
        app.encode_plex('stimid')
        app.encode_plex(int(myStim.getStimulusID()+app.globals.plexStimIDOffset))
        app.encode_plex('rotid')
        app.encode_plex(int(myStim.getStimulusRotation()+app.globals.plexRotOffset))
        #print t.ms()
        t.reset()
        myTime = t.ms()
        newTime = myTime
        #print myTime
        while(newTime - myTime < rotCodeDelTime):
            #busy wait
            newTime= t.ms()
        #print newTime
        app.encode_plex('gen_mode')
        app.encode_plex(int(myStim.getStimulusMode()+app.globals.plexStimIDOffset))
        app.encode_plex('gen_submode')
        app.encode_plex(int(myStim.getStimulusSubmode()+app.globals.plexStimIDOffset))
        app.encode('stimid')
        app.encode(int(myStim.getStimulusID()+app.globals.plexStimIDOffset))
        app.encode('rotid')
        print 'encoding mode: %d for %d submode:%d for %d\n' % (int(myStim.getStimulusMode()+app.globals.plexStimIDOffset),myStim.getStimulusMode(),int(myStim.getStimulusSubmode()+app.globals.plexStimIDOffset),myStim.getStimulusSubmode())
        app.encode(int(myStim.getStimulusRotation()+app.globals.plexRotOffset))
        app.encode('gen_mode')
        app.encode(int(myStim.getStimulusMode()+app.globals.plexStimIDOffset))
        app.encode('gen_submode')
        app.encode(int(myStim.getStimulusSubmode()+app.globals.plexStimIDOffset))

    def encodeITI(self,app):                #Encode upcoming Trial info - Called every ITI
        pass

    def cleanup(self,app):                      #Cleanup after Task - Called at end
                #delete parameter table and anything else we created
        self.myTaskParams.save()
        self.myTaskButton.destroy()
        self.myTaskNotebook.destroy()
        #del app.globals
        #self.myTaskParams.destroy()
        #if(len(self.myStims) > 0):
        #   for i in arange(1,len(self.mySprites)):
        #       self.mySprites[i].__del__()

    def getRecordFileName(self): #gets the record file for this task 
        params = self.myTaskParams.check()
        if(params['Use Special Name']):
            filename = "%s%s%s_%s_%02d_%02d.rec" % (params['RFDirectory'],params['AnimalPrefix'],params['Date'],params['TaskName'],params['CellGroup'],params['Iteration'])
        else:
            filename = None
        return filename

    #note that this overwrites the current percept shapes that are stored in self.percepts if cacheSprite == 1

    def getPercept(self,modeToEncode, submode, mg_shape, fg_shape, mg_color, fg_color, rots,cacheSprite=1,newXOffset=None,newYOffset=None,newScale=None):
        myStims = list()
        perceptSprite = None
        if(mg_shape == 1):
            if(newXOffset is not None):
                xOffset = newXOffset
            else:
                xOffset = self.myMidgroundXOffset
            if(newYOffset is not None):
                yOffset = newYOffset
            else:
                yOffset = self.myMidgroundYOffset
            if(newScale is not None):
                scaling = newScale
            else:
                scaling = self.myMidgroundScaling
            circleSprite = Sprite(self.diameter, self.diameter, self.myX,self.myY,fb=self.myFB, depth=self.perceptDepth, on=0,centerorigin=1)
            circleSprite.fill(self.myBG+(0,))
            circleSprite.circlefill(mg_color,r=self.radius*scaling,x=xOffset,y=yOffset)
            perceptSprite = circleSprite
            if(cacheSprite):
                self.myPercepts[mg_shape] = circleSprite
        elif(mg_shape == 2):
            if(newXOffset is not None):
                xOffset = newXOffset
            else:
                xOffset = self.barXOffset  
            if(newYOffset is not None):
                yOffset = newYOffset
            else:
                yOffset = self.barYOffset
            if(newScale is not None):
                scaling = newScale
            else:
                scaling = self.barScaling
            barM =  Sprite(self.diameter, self.diameter, self.myX,self.myY,fb=self.myFB, depth=self.perceptDepth, on=0,centerorigin=1)
            barM.fill(self.myBG+(0,))
            xloc = xOffset  #this may need to just be xOffset
            yloc = yOffset #this may need to just be yOffse
            xDist = scaling*self.radius*2
            yDist = xDist/self.barAspect
            barM.rect(xloc,yloc, xDist, yDist, mg_color)
            #print scaling,self.radius,xloc, yloc, xDist, yDist, mg_color
            perceptSprite = barM
            if(cacheSprite):
                self.myPercepts[mg_shape] = barM
        elif(mg_shape == 3):
            if(newXOffset is not None):
                xOffset = newXOffset
            else:
                xOffset = self.barXOffset
            if(newYOffset is not None):
                yOffset = newYOffset
            else:
                yOffset = self.barYOffset
            if(newScale is not None):
                scaling = newScale
            else:
                scaling = self.barScaling
        # change this to be the star stimulus percept......
        xloc = xOffset  #this may need to just be xOffset
        yloc = yOffset #this may need to just be yOffset	    
        star = createOverlapStar(self.myFB, mg_color, mg_color, mg_color, self.myX, self.myY, self.myBG, 0, self.radius*scaling, self.radius*scaling/1.5, self.numPoints,depth=self.perceptDepth,xoffset=xloc, yoffset=yloc, radius=self.radius)
        perceptSprite = star
        if(cacheSprite):
            self.myPercepts[mg_shape] = star 
        else:
            return myStims,perceptSprite
        #for i in arange(0,(params['CirclePerceptsPerBlock'])):
        #print rots
        for k in arange(0,size(rots,0)):
            myRotation = (360 - rots[k]) 
            sp =  perceptSprite.clone()
            if(k != 0):
                sp.rotate(myRotation,0,1)
            stim = stimulus(modeToEncode,mg_shape+1,rots[k],submode)
            stim.addSprite(sp,mg_color,0)
            myStims.append(stim)
        return myStims,perceptSprite

    def getComplex(self,modeToEncode, submode, mg_shape, fg_shape, mg_color, fg_color, rots,cacheSprite=1, useCache=1):
        myStims = list()
        if(self.myForeground[fg_shape] is not None and useCache):
            s = self.myForeground[fg_shape]
        else:
            s = self.myFactory.getB8StimAsOccluder(fg_shape, self.sampling,self.myFB,fg_color,0,self.myX,self.myY,self.myBG+(0,),self.myForegroundXOffset, self.myForegroundYOffset, self.myForegroundScaling,self.foregroundDepth)
            if(cacheSprite):
                self.myForeground[fg_shape] = s
        if(self.myPercepts[mg_shape] is not None and useCache):
            per = self.myPercepts[mg_shape]
        else:
            #print 'getting new percept for reverse colors\n'
            tempObj,per = self.getPercept(modeToEncode,submode, mg_shape, fg_shape, mg_color, fg_color, [0], 0)
        for k in arange(0,size(rots,0)):
            myRotation = (360 - rots[k]) 
            sp = s.clone()
            if(k != 0):
                sp.rotate(myRotation,0,1)
            sp2 = per.clone()
            if(k != 0):
                sp2.rotate(myRotation,0,1)
            stim = stimulus(modeToEncode,fg_shape, rots[k],submode)
            stim.addSprite(sp,fg_color,0)
            stim.addSprite(sp2,mg_color,0)
            myStims.append(stim)
            self.myComplexStimuli[fg_shape] = stim
        return myStims

    def getMidground(self,modeToEncode, submode, mg_shape, fg_shape, mg_color, fg_color, rots,cacheSprite=1, useCache=1):
        #Mode 3 - Midground Mode AKA Background Occluder Mode
        myStims = list()
        if(self.myForegroundinBG[fg_shape] is None or not useCache):
            #should this be foreground depth?
            s = self.myFactory.getB8StimAsOccluder(fg_shape, self.sampling,self.myFB,self.myBG,0,self.myX,self.myY,self.myBG+(0,),self.myForegroundXOffset, self.myForegroundYOffset, self.myForegroundScaling,self.midgroundDepth)
            self.myForegroundinBG[fg_shape] = s
        else:
            if(cacheSprite):
                s = self.myForegroundinBG[fg_shape]
        if(self.myPercepts[mg_shape] is not None and useCache):
            per = self.myPercepts[mg_shape]
        else:
            tempObj,per = self.getPercept(modeToEncode,submode, mg_shape, fg_shape, mg_color, fg_color, [0], 0)
        for k in arange(0,size(rots,0)):
            myRotation = (360 - rots[k]) 
            sp = s.clone()
            if(k != 0):
                sp.rotate(myRotation,0,1)
            sp2 = per.clone()
            if(k != 0):
                sp2.rotate(myRotation,0,1)
            stim = stimulus(modeToEncode,fg_shape, rots[k],submode)
            stim.addSprite(sp,mg_color,0)
            stim.addSprite(sp2,mg_color,0)
            myStims.append(stim)
            self.myMidgroundStimuli[fg_shape] = stim
        return myStims
    
    def getForeground(self,modeToEncode, submode, mg_shape, fg_shape, mg_color, fg_color, rots,cacheSprite=1, useCache=1):
        myStims = list()
        #Mode 4 - Foreground AKA Occluder
        if(self.myForeground[fg_shape] is not None and useCache):
            s = self.myForeground[fg_shape]
        else:
            s = self.myFactory.getB8StimAsOccluder(fg_shape, self.sampling,self.myFB,fg_color,0,self.myX,self.myY,self.myBG+(0,),self.myForegroundXOffset, self.myForegroundYOffset, self.myForegroundScaling,self.foregroundDepth)
            if(cacheSprite):
                self.myForeground[fg_shape] = s
        for k in arange(0,size(rots,0)):
            myRotation = (360 - rots[k]) 
            stim = stimulus(modeToEncode,fg_shape,rots[k],submode)
            sp = s.clone()
            if(k != 0):
                sp.rotate(myRotation,0,1)
            stim.addSprite(sp,fg_color,0)
            myStims.append(stim)
        return myStims
