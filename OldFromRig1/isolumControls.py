import sys, types
from pype import *
from Numeric import *
from random import *
from shapes import *
from colors import *
from fixationTask import fixationTask
from b8StimFactory import *

def RunSet(app):
    app.taskObject.runSet(app)

def cleanup(app):
    app.taskObject.cleanup(app)

def main(app):
    app.taskObject = isolumControls(app)
    app.globals = Holder()
    app.idlefb()
    app.startfn = RunSet

# This is also something that all tasks have, and it's a python thing.
# Don't touch it.

if not __name__ == '__main__':
        loadwarn(__name__)
else:
        dump(sys.argv[1])

class isolumControls(fixationTask):

    def __init__(self, app):
        self.createParamTable(app)
        self.lumDicts = colorDicts
        self.app = app
        self.mySprites = list()
        self.numStim = 0
        self.mySpriteList = list()
        self.spriteColors = list()
	self.mystimid = list()
	self.mymodeid = list()
	self.myrotid = list()
        self.achromaticI = 13
        self.minLum = 4

    def createStimuli(self,app):
        self.params = self.myTaskParams.check()
        params = self.params
        self.mySprites = list()
        self.numStim = 0
        self.mySpriteList = list()

        myWidth = eval(params['Length'])
        aspect = eval(params['Aspect_Ratio'])
        orientation = eval(params['Orientation'])
        myShape = eval(params['Shape'])
	mymodes = eval(params['shape_modes'])
	mycirc_sizes = eval(params['Circle_sizes'])
	mycirc_modes = eval(params['circle_modes'])

	if(params['show_fuzzy_ellipse'] == 1):
	    my_ell_wid = params['ellipse_Length']
	    my_ell_len = params['ellipse_Length']/params['ellipse_aspect']
	    my_ell_rot = eval(params['ellipse_rots'])

        myFB = app.fb
        myX = params['RF_Center_X']
        myY = params['RF_Center_Y']
        randomize_stims = params['randomize_stimuli']
        myBG = params['bg_during']
        useGratings = params['use_gratings']
        useMoreLums = params['use_more_lums']
        sampling = params['sampling']
        occl_H_offset = params['occl_H_offset']
        sprites = []
        use_standard_lums = params['use_standard_lums']
        gratingReps = params['gratingsPerRep']
        colorList = list()
        use_all_colors = params['use_all_colors']
        if(use_standard_lums):
            for dictValue in colorDicts.items():
                if(use_all_colors):
                    for colorValue in dictValue[1].items():
                        colorList.append(colorValue[1])
                else:
                    color_select_list = eval(params['colors_to_use'])
                    for i in range(0, size(color_select_list, 0)):
                        try:
                            for colorValue in dictValue[1].items():
                                if(colorValue[0] == colorIndex[color_select_list[i]]):
                                    colorList.append(colorValue[1])
                        except:
                            print 'Problem with color %s...moving on\n' % color_select_list[i]
        else:
            standard_lum_list = eval(params['standard_lums_to_use'])
            for i in range(0, size(standard_lum_list,0)):
                if(use_all_colors):
                    try:
                        for colorValue in colorDicts[standard_lum_list[i]].items():
                            colorList.append(colorValue[1])
                    except:
                        print 'Problem with luminance %s...moving on\n' % standard_lum_list[i]
                else:
                    color_select_list = eval(params['colors_to_use'])
                    for j in range(0, size(color_select_list, 0)):
                        try:
                            for colorValue in colorDicts[standard_lum_list[i]].items():
                                if(colorValue[0] == colorIndex[color_select_list[j]]):
                                    colorList.append(colorValue[1])
                        except:
                            print 'Problem with color %s...moving on\n' % color_select_list[j]
        if(useMoreLums):
            lumsToUse = eval(params['more lums to use'])
            for i in range(0,size(lumsToUse,0)):
                try:
                    dict = moreColorDicts[lumsToUse[i]]
                    if(use_all_colors):
                        for colorValue in dict.items():
                            colorList.append(colorValue[1])
                    else:
                        color_select_list = eval(params['colors_to_use'])
                        for j in range(0, size(color_select_list, 0)):
                            try:
                                for colorValue in dict.items():
                                    if(colorValue[0] == colorIndex[color_select_list[j]]):
                                        colorList.append(colorValue[1])
                            except:
                                print 'Problem with color %s...moving on\n' % color_select_list[j]
                except:
                    print 'Problem with luminance %s...moving on\n' % lumsToUse[i]

	#color list is made; now make every stim we need in every color in the color list
	print colorList

        for i in range(0, size(colorList,0)):
            myColor = colorList[i]
	    for j in range(0, len(myShape)):
		if(myShape[j] >= 801 and myShape[j] <= 851):
                    myFac = b8StimFactory(myWidth[j]*4,myWidth[j])
                    s = myFac.getB8Stim(myShape[j]-800, sampling,myFB, myColor,0, myX, myY,myBG+(0,))
		    s.rotate(360-orientation[j])
                elif(myShape[j] >= 901 and myShape[j] <= 951):
                    myFac = b8StimFactory(myWidth[j]*4,myWidth[j])
                    s = myFac.getB8StimAsOccluder(myShape[j]-900, sampling,myFB,myBG,0, myX, myY,  myColor,sp_h_offset=myWidth*occl_H_offset)
                    s.alpha_aperture(myWidth[j], x=0, y=0)
		    s.rotate(360-orientation[j])
            	else:
                    s = shapeDict.get(myShape[j],0)(myWidth[j], myWidth[j]/aspect[j], myFB,  myColor, 360-orientation[j], myX, myY, myBG)
		
	    	for k in range(0, len(mymodes)):
		    if(k == 1):
			#implement a fuzzy 
			s.fuzzy_image(params['fuzz_pixs'])
		    self.mySprites.append(s)
		    self.mystimid.append(myShape[j])
		    self.myrotid.append(orientation[j])
		    self.mymodeid.append(k)
		    cv = sprite._C(myColor)
            	    self.spriteColors.append([cv[0],cv[1],cv[2]])
            
	    #Now the fuzzy ellipses
	    if(params['show_fuzzy_ellipse'] == 1):
		for j in range(0, len(my_ell_rot)):
		    #grab an ellipse twice as large, fuzzy it and then rotate the whole thing
		    s = shapeDict.get(4,0)(my_ell_wid*2.5, my_ell_wid*2.5, myFB,  myColor, 0, myX, myY, myBG)
		    s.alpha_gradient_ellipse(my_ell_wid, my_ell_len, myBG)
		    s.rotate(360-my_ell_rot[j])
		    self.mySprites.append(s)
		    self.mymodeid.append(0)
		    self.mystimid.append(21)
		    self.myrotid.append(my_ell_rot[j])
		    cv = sprite._C(myColor)
            	    self.spriteColors.append([cv[0],cv[1],cv[2]])

	    #Next circles of various sizes
	    for j in range(0, len(mycirc_sizes)):
		for k in range(0,len(mycirc_modes)):
		    if(k == 0):
			s = shapeDict.get(4,0)(mycirc_sizes[j],mycirc_sizes[j],myFB,myColor,0,myX,myY,myBG)
		    if(k == 1):
			s = shapeDict.get(4,0)(mycirc_sizes[j]*2.5,mycirc_sizes[j]*2.5,myFB,myColor,0,myX,myY,myBG)
		    	s.alpha_gradient2(mycirc_sizes[j]*0.75, 1.25*mycirc_sizes[j], myBG)
		    self.mySprites.append(s)
		    self.mymodeid.append(k)
		    self.mystimid.append(11+j)
		    self.myrotid.append(0)
		    cv = sprite._C(myColor)
            	    self.spriteColors.append([cv[0],cv[1],cv[2]])

	    #Sheets of color with a contour mode    
  	    if(params['full_screen_contour'] == 1):
		s = shapeDict.get(0,0)(3200, 2400, myFB,  myColor, 0, myX, myY, myBG)
		closed = 1
		verts0 = [[0,-myWidth[0]/2.0],[myWidth[0]/2.0,0],[0,myWidth[0]/2.0],[-myWidth[0]/2.0,0]]
		s.unassumingpolygon((0,0,0),closed,verts0,5)
		self.mySprites.append(s)
		self.mymodeid.append(0)
		self.mystimid.append(22)
		self.myrotid.append(0)
		cv = sprite._C(myColor)
            	self.spriteColors.append([cv[0],cv[1],cv[2]])
        
        for j in arange(0,params['nBlanks']):
            s = createBar(30, 30, myFB,myBG, 0, myX, myY, myBG)
            self.mySprites.append(s)
            self.spriteColors.append(myBG)	    self.mymodeid.append(0)
	    self.mystimid.append(0)
	    self.myrotid.append(0)

        numUniqueStims = len(self.mySprites)
        stimNumbers = arange(0,numUniqueStims)
        for i in arange(0,params['nRepsPerStim']):
            if(randomize_stims):
                shuffle(stimNumbers)
            self.mySpriteList.extend(stimNumbers)
            self.numStim = self.numStim + len(self.mySprites)

	#these are the stim params that need to be encoded before start of task
        self.myWidth = myWidth
        self.myAspect = aspect
	self.circsizes = mycirc_sizes
	if(params['show_fuzzy_ellipse'] == 1):
            self.ellwid = my_ell_wid
	    self.ell_len = my_ell_len
        self.myFB = myFB
        self.myX = myX
        self.myY = myY
        self.myBG = myBG
 
    def createParamTable(self,app):
        #create parameter table and window to go along with it
        P = app.getcommon()
        self.myTaskButton = app.taskbutton(text=__name__, check = 1)
        self.myTaskNotebook = DockWindow(title=__name__, checkbutton=self.myTaskButton)
        parfile = "%s.%s" % (app.taskname(), P['subject'])
        # Look for an existing saved parameter file for this task
        if parfile:
                parfile = parfile + '.par'

        # Initialization and default values for the parameters.  Each row is one parameter.  The first value is the name of the parameter, the
        # second is its default value, the third defines the type of the value (more on that later) and the fourth is optional and
        # is a descriptive label that pops up when you hold the mouse over that entry in the table.  There are numerous standard parameter
        # types, the most common are self-explanatory. is_color needs to be 3 or 4 numbers in tuple format, e.g. (255,1,1) for red; the 4th
        # number is optional and is an alpha value (if left off, assumed to be 255).  (0,0,0) is a special code for transparent or for
        # white noise fill pattern, depending on the task, so use (1,1,1) for black.  is_any just gets passed as a string, this is what
        # to use if you need a list of numbers.  is_iparam can take a variance value as either a percentage or an actual number of
        # units, so you'd have "1000+-10%" or "150+-50".  There are a ton of others defined in ptable.py.  Values of None for default value and
        # type make that row into a heading of sorts that can be helpful for organizing a large number of parameters.

        self.myTaskParams = ParamTable(self.myTaskNotebook, (
                ("Stimulus Pres Params", None, None),
	
                ("Shape", [0,1], is_any, "select shape: 0:rectangle, 4: ellipse, 5: diamond, 6: star 801-851: B8 stims 1-51 901-951: newAim1 Midground stims 1-51"),
                ("Aspect_Ratio", [1.0,1.0], is_any, "Aspect Ratio (Width/Height) as many as shapes above"),
                ("Length", [1,1], is_any, "Length  of stimulus in pixels, as many as shapes above"),
		("Orientation", [0,0], is_any, "Orientation in degrees(as many as number of shapes). Note that stims rotation clockwise."),
                ("shape_modes", [0,1], is_any, "0:normal shape, 1:fuzzy boundary"),
		("fuzz_pixs",	20,    is_int, "Pix width for fuzzing"),
		
		("Circle_sizes", [25, 65, 150], is_any, "Size of circle stimuli to test in pixels (stimid:11-20)"),
		("circle_modes", [0,1], is_any, "0:normal shape, 1:fuzzy boundary"),
	
		("show_fuzzy_ellipse", 1, is_boolean, "show an elliptical blur stimulus (21)"),
		("ellipse_aspect", 1.0, is_float, "Aspect Ratio (Length/width; must be > 1.0)"),
                ("ellipse_Length", 1, is_int, "Length  of stimulus in pixels (long axis)"),
		("ellipse_rots", [0,0], is_any, "Orientation in degrees(can input multiple orientations). Note that stims rotation clockwise."),
	
		("full_screen_contour", "1", is_int, "1 if you want to try full screen with a circle contour within (stimid 22)"), 
		
		("nRepsPerStim", "3", is_int, "Number of repetitions of each stimulus to present"),
                ("nBlanks", "3", is_int, "The number of blank stimuli to present per block"),              
                ("bg_during", "(10, 10, 10)", is_color, "The background color during stimulus presentation"),
                ("bg_before", "(10, 10, 10)", is_color, "The background color before stimulus presentation"),
                ("randomize_stimuli", 0, is_boolean, "Whether or not to randomize stimuli within repetitions."),
                ("Luminances",None,None),
                ("use_standard_lums", 1, is_boolean, "Whether to use the standard lums (4,8,12,18)"),
                ("standard_lums_to_use", [4,8,12,18], is_any, "If use_standard_lums is 0, then use these lums"),
                ("use_more_lums", 0, is_boolean, "Whether to use additional Luminances"),
                ("more lums to use", [7.8,8.2], is_any, "If use_more_lums is 1 then use these luminances"),
                ("Colors", None, None),
                ("use_all_colors", 1, is_boolean, "Whether to use all the 25 colors"),
                ("colors_to_use", [1,2,3,4,5],is_any, 'Colors of Stimuli'),
                ("Stimulus Specific Parameters",None,None),
                ("use_gratings", 1, is_boolean, "Whether or not to use spatial frequency gratings."),
                ("gratingsPerRep", 3, is_int, "Number of each grating in each rep"),
                ("grating radius", "100", is_int, "Radius of circular grating (or circle inscribed by sqaure grating"),
                ("grating orientation", "0", is_int, "Grating Orientation in degrees of the stimulus. Note that stims rotation clockwise."),
                ("spatial frequency", "1.0", is_float, "Spatial Frequency of grating (shape 7) in cycles/stimulus"),
                ("phase", "90.0", is_float, "Phase of grating (shape 7) in degrees"),
                ("contrast", "[5, 10, 25, 50]", is_any, "List of contrasts of gratings in percent"),
                ("bg_lum", "8", is_int, "Luminance of background (4,8,12 or 18)"),
                ("isCircle", 0, is_int, "if 1 then draw the sinusoidal gratings as circles"),
                ("sampling", "100", is_int, "# of pixels between each control point when using shapes 801-851 or 901-951."),
                ("occl_H_offset", ".66", is_float, "Fraction of RF to displace occluder for shapes 901-951"),
                ("RF_Params",None,None),
                ("RF_Center_X", "0",is_int,"X coordinate of the receptive field center in pixels"),
                ("RF_Center_Y", "0",is_int,"Y coordinate of the receptive field center in pixels"),
                ("Task Params", None, None),
                ("iti", "2500", is_int, "Inter-trial interval"),
                ("IStime", "200", is_int, "Inter-stimulus interval"),
                ("stimon", "300", is_int, "Stimulus presentation"),
                ("nstim", "5", is_int, "Number of stimuli"),
                ("Fixation Params", None, None, "Fixation Parameters"),
                ("fixcolor1", "(255,255,255)",is_color, 'Color of the fixation dot'),
                ("fixcolor2", "(128,128,128)",is_color),
                ("min_err", "0", is_int),
                ("max_err", "100", is_int),
                ("fixwait", "100", is_int),
                ("Reward Params", None, None),
                ("numdrops", "8", is_int, "Number of juice drops"),
                ("rmult", "1.0", is_float),
                ("Record File Params", None, None, "Params for setting name of record file"),
                ("Use Special Name", "0", is_boolean, "If 1 then the record file name will be AnimalPrefixDate_TaskName_CellGroup_Iteration.rec"),
                ("RFDirectory", "/home/shapelab/recordFiles/", is_any, "Directory to use for Record Files"),               
                ("AnimalPrefix", "m", is_any, "Animal Prefix to use"),
                ("Date","080325", is_any, "Date to use "),
                ("TaskName","isolumcontrol", is_any, "TaskName"),
                ("CellGroup","01", is_int, "# of cell group encountered today"),
                ("Iteration","01", is_int, "# of times this task has been run on this cell group"),
                ("Misc Params", None, None, "Miscelaneous Parameters"),
                ("Recent Buffer Size", "50", is_int, "The number of trials to use to calculate recent performance"),
                ("pause_color", "(150,0,0)", is_color, "The screen will turn this color when the task is paused")
                ), file=parfile)
                
    def cleanup(self, app):
        #delete parameter table and anything else we created
        self.myTaskParams.save()
        self.myTaskButton.destroy()
        self.myTaskNotebook.destroy()
        del app.globals
        #self.myTaskParams.destroy()
#        if(len(self.mySprites) > 0):
#            for i in arange(1,len(self.mySprites)):
#                self.mySprites[i].__del__()

    def encodeISI(self,app,sIndex):
        sColorIndex = self.mySpriteList[sIndex]
        myColor = self.spriteColors[sColorIndex]
	mystimid = self.mystimid[sColorIndex]
	mymodeid = self.mymodeid[sColorIndex]
	myrotid = self.myrotid[sColorIndex]
	
	app.encode_plex('stimid')
        app.encode_plex(int(mystimid+app.globals.plexStimIDOffset))
        app.encode_plex('rotid')
        app.encode_plex(int(myrotid+app.globals.plexRotOffset))
        app.encode_plex('gen_mode')
        app.encode_plex(int(mymodeid+app.globals.plexStimIDOffset))

	app.encode('stimid')
        app.encode(int(mystimid+app.globals.plexStimIDOffset))
        app.encode('rotid')
        app.encode(int(myrotid+app.globals.plexRotOffset))
        app.encode('gen_mode')
        app.encode(int(mymodeid+app.globals.plexStimIDOffset))

        #print myColor
        app.encode_plex('color')
        app.encode_plex(myColor[0] + app.globals.plexRotOffset)
        app.encode_plex(myColor[1] + app.globals.plexRotOffset)
        app.encode_plex(myColor[2] + app.globals.plexRotOffset)

        app.encode('color')
        app.encode(myColor[0] + app.globals.plexRotOffset)
        app.encode(myColor[1] + app.globals.plexRotOffset)
        app.encode(myColor[2] + app.globals.plexRotOffset)
        #print '%d,%d,%d:' %(myColor[0],myColor[1], myColor[2])

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
        colorTuple = self.myBG
        app.encode_plex(int(colorTuple[0] + app.globals.plexRotOffset))
        app.encode_plex(int(colorTuple[1] + app.globals.plexRotOffset))
        app.encode_plex(int(colorTuple[2] + app.globals.plexRotOffset))

 	#encode circle size info and other stim parameter info
        sizes = eval(params['Circle_sizes'])
        app.encode_plex('radius')
        app.encode_plex(len(self.circsizes))
        for i in arange(0,len(self.circsizes)):
            app.encode_plex(self.circsizes[i]+app.globals.yOffset)
	app.encode_plex(params['show_fuzzy_ellipse'])
	if(params['show_fuzzy_ellipse'] == 1):
	    app.encode_plex(self.ellwid+app.globals.yOffset)
	    app.encode_plex(int(self.ell_len)+app.globals.yOffset)
	app.encode_plex(len(self.myWidth))
	if(len(self.myWidth) > 0):
	    for i in arange(0,len(self.myWidth)):
            	app.encode_plex(self.myWidth[i]+app.globals.yOffset)
	    for i in arange(0,len(self.myAspect)):
            	app.encode(int(self.myWidth[i]/self.myAspect[i])+app.globals.yOffset)

        app.encode('rfx')
        app.encode(params['RF_Center_X']+ app.globals.yOffset)
        app.encode('rfy')
        app.encode(params['RF_Center_Y'] + app.globals.yOffset)
        app.encode('iti')
        app.encode(int(params['iti']))
        app.encode('stim_time')
        app.encode(int(params['stimon']))
        app.encode('isi')
        app.encode(int(params['IStime']))
        app.encode('numstim')
        app.encode(int(params['nstim']))
        app.encode(int(colorTuple[0] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[1] + app.globals.plexRotOffset))
        app.encode(int(colorTuple[2] + app.globals.plexRotOffset))
	app.encode('radius')
        app.encode(len(self.circsizes))
	for i in arange(0,len(self.circsizes)):
            app.encode(self.circsizes[i]+app.globals.yOffset)
	app.encode(params['show_fuzzy_ellipse'])
	if(params['show_fuzzy_ellipse'] == 1):
	    app.encode(self.ellwid+app.globals.yOffset)
	    app.encode(int(self.ell_len)+app.globals.yOffset)
	app.encode(len(self.myWidth))
	if(len(self.myWidth) > 0):
	    for i in arange(0,len(self.myWidth)):
            	app.encode(self.myWidth[i]+app.globals.yOffset)
	    for i in arange(0,len(self.myAspect)):
            	app.encode(int(self.myWidth[i]/self.myAspect[i])+app.globals.yOffset)

        useGratings = params['use_gratings']
        grat_rad = params['grating radius']
        spat_freq = params['spatial frequency']
        phase = params['phase']
        contrasts = eval(params['contrast'])
        bg_lum = params['bg_lum']
        isCircle = params['isCircle']
        app.encode_plex(useGratings)
        app.encode(useGratings)
        app.encode_plex(grat_rad)
        app.encode(grat_rad)
        app.encode_plex(int(round(spat_freq*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode(int(round(spat_freq*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        app.encode_plex(int(phase))
        app.encode(int(phase))
        app.encode_plex(bg_lum)
        app.encode(bg_lum)
        app.encode_plex(isCircle)
        app.encode(isCircle)
        for i in range(0, size(contrasts,0)):
            app.encode_plex(int(contrasts[i]))
            app.encode(int(contrasts[i]))
            #app.encode_plex(int(round(contrasts[i]*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
            #app.encode(int(round(contrasts[i]*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        
     
    def encodeITI(self,app):
        pass

    def getSprite(self, index):
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
