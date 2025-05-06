## Yoshito Kosai and Yasmine El-Shamayleh (4/2011)
## size x curvature x position experiment
## task file is based off of xFixationTask and newAIM1 structure.



import sys, types
from pype import *
from Numeric import *
from random import *
from shapes import *
from colors import *
from xFixationTask import xFixationTask
#from yesStimFactory import *				#YES stim factory
from b8StimFactory_pz import *				#YES stim factory
from stimulus import stimulus				
from sets import *

def RunSet(app):
    app.taskObject.runSet(app)

def cleanup(app):
    app.taskObject.cleanup(app)

def main(app):
    app.taskObject = yes_screen(app)
    app.globals = Holder()
    app.idlefb()
    app.startfn = RunSet

# This is also something that all tasks have, and it's a python thing.
# Don't touch it.

if not __name__ == '__main__':
        loadwarn(__name__)
else:
        dump(sys.argv[1])

class yes_screen(xFixationTask):
    def __init__(self, app):
        self.createParamTable(app)
        self.app = app
        self.myStims = list()
        self.numStim = 0
        self.myStimList = list()
        self.numYesShapes = 9
        self.blankMode = 1
        self.YesShapeSet = arange(1,self.numYesShapes+1)
        self.blankID = 1

    #Create Stimuli - Create stimuli called at beginning
    def createStimuli(self,app):            
        self.params = self.myTaskParams.check()
        params = self.params
        P = app.getcommon()
        self.myStims = list()
	self.myScaleFactors = list()		
        self.numStim = 0
        self.myStimList = list()
        myFB = app.fb
        myX = params['RF_Center_X']
        myY = params['RF_Center_Y']
        fixX = P['fix_x']
        fixY = P['fix_y']
        myBG = params['bg_during']
        randomize_stims = params['randomize_stimuli']
	scalefactors = eval(params['Scale Factors'])
	if(scalefactors == []):
	    scalefactors = [0.5,0.75,1.0,1.25,1.5]		#default scale factors - removed 0.25 on 5/3/11
        color = params['Color']
        self.myBG = myBG
        self.myFB = myFB
        self.myX = myX
        self.myY = myY
        self.fixX = fixX
        self.fixY = fixY
        self.color = color
        self.randomize = randomize_stims
        stims = list()
 	#self.size is diameter of receptive field, also width and height of bounding square
        self.size = 2*params['RF Radius']
	# made this 2times basestimsize on 5/1/2011 - so base size is entered in as a radius (what we get from handmap)
        self.baseStimSize = 2*params['Base Stim Size']
        self.diameter = self.size
        self.radius = self.size/2.0
	self.stimIDs = eval(params['Stim IDs'])
	if(self.stimIDs == []):
	    self.stimIDs = list(arange(1,self.numYesShapes+1))	#default shape IDs 1-9
        self.rots = eval(params['Rotations'])
	if(self.rots == []):
	    self.rots = [0,45,90,135,180,225,270,315]		#default rotations
        #self.myFactory = yesStimFactory(self.diameter*2,self.radius)
        self.myFactory = b8StimFactory_pz(self.diameter*2,self.radius)
        self.sampling = params['Sampling']
        self.myYesStimuli = (self.numYesShapes+1)*[None]        #list of all complex shape stimulus (Not Sprite!) objects
	self.scaleList = list()
	self.scaleList = scalefactors
	self.sizeList = list()
	self.positionList = []
	for i in arange(0,len(self.stimIDs)):
		self.positionList.append([])

	# Check if all stimuli are within the RF
        sanityCheck = 0
        for i in range(len(scalefactors)):
        	if(scalefactors[i]*self.baseStimSize > self.size):
                	sanityCheck = 1
	temp = array(scalefactors)*self.baseStimSize
	message1 = 'Sizes presented:\n' + str(temp) + '\nSome stimuli are outside RF'
        message2 = 'Sizes presented:\n ' + str(temp) + '\nAll stimuli are within RF'
	if(sanityCheck):
                if ask("pype", message1, ("continue", "cancel")) == 0:
                        pass
                else:
                        return
	else:
		if ask("pype", message2, ("continue", "cancel")) == 0:
			pass
		else: 
			return

	posLocList = []
	testPosLocList = []
	for i in arange(0,len(self.stimIDs)):
		posLocList.append([])
		if (self.stimIDs[i] <= 5):
			testPosLocList.append([])
	baseScaleIndex = 0
        #Mode 2 - Create stimuli at different scale factors (scale exp)
	self.scaleMode = 2
	for i in arange(0,len(scalefactors)):
	    if(scalefactors[i] == 1):
		baseScaleIndex = i
	    #self.myFactory = yesStimFactory(int(round(self.baseStimSize*2*scalefactors[i])),int(round(self.baseStimSize/2*scalefactors[i])))
	    self.myFactory = b8StimFactory_pz(int(round(self.baseStimSize*2*scalefactors[i])),int(round(self.baseStimSize/2*scalefactors[i])))
	    self.sizeList.append(int(round(self.baseStimSize*scalefactors[i])))
	    for j in arange(0,len(self.stimIDs)):
            	if(self.stimIDs[j] == 5): #for circle shape (number 5) don't do rotations 
			[stim,maxY] = self.getYesStimuli(self.scaleMode, i, self.stimIDs[j], self.color, [0],0, cacheSprite=1, useCache=0) 
            	else: 
			[stim,maxY] = self.getYesStimuli(self.scaleMode, i, self.stimIDs[j], self.color, self.rots,0, cacheSprite=1, useCache=0) 
			
		self.myStims.extend(stim)
		posLocList[j].append(maxY)
		self.positionList[j].append(0)

	#Mode 3 - Create base size stimuli at different offsets based on scale factors (position controls)
	# only show position controls at scale factors that are not 1
	self.positionMode = 3
	if(params['Do Position Control']):
	    for i in arange(0,len(scalefactors)):
		if (scalefactors[i]!=1): 			#REMOVE REDUNDANCY OF PRESENTING AT SCALE FACTOR 1
			if(scalefactors[i] >= 1):		#SO SPRITE DOESN"T CUT OFF FOR BIG SHAPES
	    			#self.myFactory = yesStimFactory(int(round(self.baseStimSize*2*scalefactors[i])),int(round(self.baseStimSize/2)))
	    			self.myFactory = b8StimFactory_pz(int(round(self.baseStimSize*2*scalefactors[i])),int(round(self.baseStimSize/2)))
	    		else:
				#self.myFactory = yesStimFactory(int(round(self.baseStimSize*2)),int(round(self.baseStimSize/2)))
				self.myFactory = b8StimFactory_pz(int(round(self.baseStimSize*2)),int(round(self.baseStimSize/2)))
	    		for j in arange(0,len(self.stimIDs)):
				difference = (posLocList[j][i] - posLocList[j][baseScaleIndex])
				self.positionList[j][i] = difference
				if (self.stimIDs[j] <= 5): #only do position controls for concave shapes + circle (stimID 0-4, shapes 1-5)
            				[stim, maxY] = self.getYesStimuli(self.positionMode, i, self.stimIDs[j], self.color, self.rots, difference, cacheSprite=1, useCache=0) 
	    				self.myStims.extend(stim)
					testPosLocList[j].append(maxY)
#	f = open('/home/shapelab/testfile1','w') #difference between position of max of shape and position of max of translated shape
#	f.write(str(array(self.positionList)))
#	f = open('/home/shapelab/testfile2','w') #position of max of translated base shape
#	f.write(str(array(testPosLocList)))
#	f = open('/home/shapelab/testfile3','w') #position of max of scaled shapes
#	f.write(str(array(posLocList)))
        
	#Mode1 - Blanks 
        for j in arange(0,params['nBlanks']):
            stim = stimulus(self.blankMode,self.blankID,0)
            s = createBar(self.radius, self.radius, myFB,myBG, 0, myX, myY, myBG)
            stim.addSprite(s, myBG, 0)
            self.myStims.append(stim)
	
        numUniqueStims = len(self.myStims)
        stimNumbers = arange(0,numUniqueStims)

        for i in arange(0,params['nReps']):
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

        self.myTaskParams = ParamTable(self.myTaskNotebook, (
                ("RF Params",None,None),   					
                ("RF_Center_X", "0",is_int,"X coordinate of RF in pixels"),
                ("RF_Center_Y", "0",is_int,"Y coordinate of RF in pixels"),
                ("RF Radius", "100", is_int, "Radius of the RF in pixels"),
                ("ShowRFSprite", "1", is_boolean, "If 1 display white circle around RF (for testing)"),
		("Stimulus Params", None, None),      				
		("Base Stim Size", "100", is_int, "Radius of base stimulus in pixels"),
		("Stim IDs", "[]", is_any, "Shape ids that will be presented"),
		("Scale Factors", "[]", is_any, "Fraction determining the size of shape"),
		("Rotations", "[]", is_any, "Rotations to use (in degrees)"),
                ("Color", "(161, 34, 35)", is_color, "Color shape in rgb"),
                ("Do Position Control", 1, is_boolean, "Do position control experiment?"),
                ("Sampling", "100",is_int,"Number of points in each b-spline"),                
                ("Task Params", None, None),
		("nstim", "5", is_int, "Number of stimuli per trial"),
 		("nBlanks", "3", is_int, "Number of blanks presented per block"),			
                ("nReps", "20", is_int, "Number of repetitions of each stimulus"),
          	("randomize_stimuli", 0, is_boolean, "Whether or not to randomize stimuli within repetitions."),
                ("bg_during", "(35, 19, 14)", is_color, "The background color during stimulus presentation"),
                ("bg_before", "(35, 19, 14)", is_color, "The background color before stimulus presentation"),				
                ("iti",	"1500", is_int, "Inter-trial interval"),
                ("IStime", "200", is_int, "Inter-stimulus interval"),
                ("AddExtraISI", "1", is_int, "If 1 add another ISI after the last stimulus in a trial, otherwise 0"),
                ("stimon", "300", is_int, "Stimulus presentation"),
		("Fixation Params", None, None),				
                ("fixcolor1", "(255,255,255)", is_color, 'Color of fixation dot'),
                ("min_err", "0", is_int),
                ("max_err", "100", is_int),
                ("fixwait", "100", is_int),                
		("Reward Params", None, None),	      				
                ("numdrops", "14", is_int, "Number of juice drops"),
		("Misc Params", None, None, "Miscelaneous Parameters"),  
		("rmult", "1.0", is_float),	
                ("RotCodeDelayTime", "30", is_int, "Time in ms to wait between sending the rotation code and the mode code"),
                ("Recent Buffer Size", "50", is_int, "Number of trials used to calculate recent performance"),
                ("pause_color", "(150,0,0)", is_color, "Screen color when the task is paused"),
		("Record File Params", None, None),    				
                ("Use Special Name", "0", is_boolean, "If 1 record file name will be AnimalPrefixDate_TaskName_CellGroup_Iteration.rec"),
                ("RFDirectory", "\\home\\shapelab\\recordFiles\\", is_any, "File directory"),               
                ("AnimalPrefix", "o", is_any, "Animal prefix"),
                ("Date","110425", is_any, "Date YYMMDD"),
                ("TaskName","yes_screen", is_any, "TaskName"),
                ("CellGroup","01", is_int, "# of cell group encountered today"),
                ("Iteration","01", is_int, "# of times this task has been run on this cell group")
                ), file=parfile)

    def getRFSprite(self):
        if(self.params['ShowRFSprite']):
            circleSprite = Sprite(self.size*2, self.size*2, self.myX,self.myY,fb=self.myFB, depth=1, on=0,centerorigin=1)
            circleSprite.fill(self.myBG+(0,))
            circleSprite.circlefill((255,255,255),r=self.radius,x=0,y=0,width=1)
            return circleSprite
        else:
            return None

    def encodeTaskParameters(self,app):     #Encode task Params - Called at the beginning of the task
        #encode task parameters
        #Kept all of encoding task parameters the same as newAIM1 so that the parse file will match easier
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
	
	##################### yes specfic codes 

	app.encode_plex('radius') #Just base size - based on sprite size
	app.encode('radius')
	app.encode_plex(self.baseStimSize+app.globals.yOffset)
	app.encode(self.baseStimSize+app.globals.yOffset)

       	app.encode_plex('stimid')
	app.encode('stimid')
	app.encode_plex(len(self.stimIDs)+app.globals.plexStimIDOffset)
	app.encode(len(self.stimIDs)+app.globals.plexStimIDOffset)
	for i in range(len(self.stimIDs)):
		app.encode_plex(self.stimIDs[i]+app.globals.plexStimIDOffset)
		app.encode(self.stimIDs[i]+app.globals.plexStimIDOffset)

	app.encode_plex('rotid')
	app.encode('rotid')
	app.encode_plex(len(self.rots)+app.globals.plexRotOffset)
	app.encode(len(self.rots)+app.globals.plexRotOffset)
	for i in range(len(self.rots)):
		app.encode_plex(self.rots[i]+app.globals.plexRotOffset)
		app.encode(self.rots[i]+app.globals.plexRotOffset)

	app.encode_plex('radius') #All sizes being tested
	app.encode('radius')
	app.encode_plex(len(self.sizeList)+app.globals.yOffset)
	app.encode(len(self.sizeList)+app.globals.yOffset)
	for i in range(len(self.sizeList)):
		app.encode_plex(int(self.sizeList[i]+app.globals.yOffset))
		app.encode(int(self.sizeList[i]+app.globals.yOffset))

        app.encode_plex('position') #All position offsets relative to max of spline
	app.encode('position')
	app.encode_plex(len(self.positionList[0])+app.globals.yOffset)
	app.encode(len(self.positionList[0])+app.globals.yOffset)
	for j in arange(0,len(self.stimIDs)):	
		for i in range(len(self.positionList[0])):
			app.encode_plex(int(self.positionList[j][i]+app.globals.yOffset))
			app.encode(int(self.positionList[j][i]+app.globals.yOffset))

        #encode colors: bg, shape
        app.encode_plex('color')
        app.encode('color')
        colorTuple = self.myBG
        app.encode_plex(int(colorTuple[0] + app.globals.plexRotOffset))
        app.encode_plex(int(colorTuple[1] + app.globals.plexRotOffset))
        app.encode_plex(int(colorTuple[2] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[0] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[1] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[2] + app.globals.plexRotOffset))
        colorTuple = self.color
        app.encode_plex(int(colorTuple[0] + app.globals.plexRotOffset))
        app.encode_plex(int(colorTuple[1] + app.globals.plexRotOffset))
        app.encode_plex(int(colorTuple[2] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[0] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[1] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[2] + app.globals.plexRotOffset))

	#YES added on 5/12/2011 - encode RF radius
	app.encode_plex('radius') 
        app.encode('radius')
        app.encode_plex(params['RF Radius']+ app.globals.yOffset)
        app.encode(params['RF Radius']+ app.globals.yOffset)

	#YES added on 5/16/2011 - encode pix2dva conversion
	P = app.getcommon()
        pix2dva = int(P['mon_ppd'])
        app.encode_plex('mon_ppd')
        app.encode('mon_ppd')
        app.encode_plex(int(P['mon_ppd'])+app.globals.plexStimIDOffset)
        app.encode(int(P['mon_ppd']))

    def encodeISI(self,app,myStim):                #Encode upcoming Stimlus Params - Called every ISI
        params = self.myTaskParams.check()
        rotCodeDelTime = params['RotCodeDelayTime']
        t = Timer()
	index = int(myStim.getStimulusSubmode())
	if(myStim.getStimulusMode() == 1): #blank mode
	    app.encode_plex('stimid')
	    app.encode_plex(int(app.globals.plexStimIDOffset))
	    app.encode_plex('rotid')
	    app.encode_plex(int(app.globals.plexRotOffset))
	    app.encode_plex('position')
	    app.encode_plex(int(app.globals.plexStimIDOffset))
	    app.encode_plex('radius') #This will be size in pixels
	    app.encode_plex(int(app.globals.plexStimIDOffset))
	    		
	elif(myStim.getStimulusMode() == 2): #scale mode	
	    app.encode_plex('stimid')
	    app.encode_plex(int(myStim.getStimulusID()+app.globals.plexStimIDOffset))
	    app.encode_plex('rotid')
	    app.encode_plex(int(myStim.getStimulusRotation()+app.globals.plexRotOffset))
	    app.encode_plex('position')
	    app.encode_plex(int(0+app.globals.plexStimIDOffset))
	    app.encode_plex('radius') #This will be size in pixels
	    app.encode_plex(int(self.sizeList[index]+app.globals.plexStimIDOffset))
	    
	elif(myStim.getStimulusMode() == 3): #position mode
 	    app.encode_plex('stimid')
	    app.encode_plex(int(myStim.getStimulusID()+app.globals.plexStimIDOffset))
	    app.encode_plex('rotid')
	    app.encode_plex(int(myStim.getStimulusRotation()+app.globals.plexRotOffset))
	    app.encode_plex('position')
	    app.encode_plex(int(self.positionList[self.stimIDs.index(myStim.getStimulusID())][index]+app.globals.plexStimIDOffset))
	    app.encode_plex('radius') #This will be size in pixels
	    app.encode_plex(int(self.baseStimSize+app.globals.plexStimIDOffset))
	    
        t.reset()
        myTime = t.ms()
        newTime = myTime
        while(newTime - myTime < rotCodeDelTime):
            newTime= t.ms()
 	if(myStim.getStimulusMode() == 1):
	    app.encode('stimid')
	    app.encode(int(app.globals.plexStimIDOffset))
	    app.encode('rotid')
	    app.encode(int(app.globals.plexRotOffset))
	    app.encode('position')
	    app.encode(int(app.globals.plexStimIDOffset))
	    app.encode('radius') #This will be size in pixels
	    app.encode(int(app.globals.plexStimIDOffset))
	    
	elif(myStim.getStimulusMode() == 2):	
	    app.encode('stimid')
	    app.encode(int(myStim.getStimulusID()+app.globals.plexStimIDOffset))
	    app.encode('rotid')
	    app.encode(int(myStim.getStimulusRotation()+app.globals.plexRotOffset))
	    app.encode('position')
	    app.encode(int(0+app.globals.plexStimIDOffset))
	    app.encode('radius') #This will be size in pixels
	    app.encode(int(self.sizeList[index]+app.globals.plexStimIDOffset))
	   
	elif(myStim.getStimulusMode() == 3):
 	    app.encode('stimid')
	    app.encode(int(myStim.getStimulusID()+app.globals.plexStimIDOffset))
	    app.encode('rotid')
	    app.encode(int(myStim.getStimulusRotation()+app.globals.plexRotOffset))
	    app.encode('position')
	    app.encode(int(self.positionList[self.stimIDs.index(myStim.getStimulusID())][index]+app.globals.plexStimIDOffset))
	    app.encode('radius') #This will be size in pixels
	    app.encode(int(self.baseStimSize+app.globals.plexStimIDOffset))
	    

    def encodeITI(self,app):                #Encode upcoming Trial info - Called every ITI
        pass

    def cleanup(self,app):                      #Cleanup after Task - Called at end
        #delete parameter table and anything else we created
        self.myTaskParams.save()
        self.myTaskButton.destroy()
        self.myTaskNotebook.destroy()

    def getRecordFileName(self): #gets the record file for this task 
        params = self.myTaskParams.check()
        if(params['Use Special Name']):
            filename = "%s%s%s_%s_%02d_%02d.rec" % (params['RFDirectory'],params['AnimalPrefix'],params['Date'],params['TaskName'],params['CellGroup'],params['Iteration'])
        else:
            filename = None
        return filename

    #note that this overwrites the current percept shapes that are stored in self.percepts if cacheSprite == 1
    def getYesStimuli(self, mode, index, shape, color, rots, difference, cacheSprite=1, useCache=1):
        myStims = list()
        if(self.myYesStimuli[shape] is not None and useCache):
            s = self.myYesStimuli[shape]
        else:
            [s,maxY] = self.myFactory.getYesStim(shape, self.sampling,self.myFB, color,0,self.myX,self.myY,self.myBG+(0,),0,difference,1.0,1)
	    s.fuzzy_image(7)
	    if(cacheSprite):
                self.myYesStimuli[shape] = s
        for k in arange(0,size(rots,0)):
            myRotation = (360 - rots[k]) 
            stim = stimulus(mode,shape,rots[k],index)
            sp = s.clone()
            sp.rotate(myRotation,0,1)
            stim.addSprite(sp,color,0)
            myStims.append(stim)
        return myStims, maxY
