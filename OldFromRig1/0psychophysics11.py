import sys, types
#import random
from pype import *
from Numeric import *
from random import *
from shapes import *
from colors import *
#from xPPTask import xFixationTask
from b8StimFactory import *
from stimulus import stimulus
from sets import *
#from numpy import *

# Beginning of xpptask
class xFixationTask:

    def __init__(self):	
        self.createParamTable(app)
        self.app = app
        self.myStims = list()
        self.numStim = 0
        self.myStimList = list()
	

    def createParamTable(self,app):
	parfile = app.taskname()
	# Look for an existing saved parameter file for this task
	if parfile:
		parfile = parfile + '.par'
        self.myTaskParams = ParamTable(self.myTaskNotebook, (
		("Stimulus Pres Params", None, None),
                ("bg_during", "(10, 10, 10)", is_color, "The background color during stimulus presentation"),
                ("bg_before", "(10, 10, 10)", is_color, "The background color before stimulus presentation"),
                ("RF_Params",None,None),
      		("RF_Center_X", "0",is_int,"X coordinate of the receptive field center in pixels"),
      		("RF_Center_Y", "0",is_int,"Y coordinate of the receptive field center in pixels"),
                ("RF Scale On Ecc", "1", is_boolean, "Whether or not to scale based on eccentricity"),
                ("RF Scaling", ".625",        is_float, "If RF_Scale_On_Ecc is 1, Size of RF in degrees equals eccentricity * RF Scaling + RF Offset"),
		("RF Offset", ".5", is_float, "If RF_Scale_On_Ecc is 1,Size of RF in degrees equals eccentricity * RF Scaling + RF Offset"),
		("RF Radius", "100", is_int, "IF RF_Scale_On_Ecc is 0, this is the radius of the RF in pixels"),
                ("Task Params", None, None),
                ("iti",	"2500",		   	is_int, "Inter-trial interval"),
		("IStime",	"200",		   	is_int, "Inter-stimulus interval"),
		("AddExtraISI",	"1",		   	is_int, "Set to 1 to add another ISI after the last stimulus in a trial, 0 otherwise"),
		("stimon",	"500",			is_int, "Stimulus presentation"),
		("nstim",	"5",			is_int, "Number of stimuli"),
      		("Fixation Params", None, None, "Fixation Parameters"),
       		("fixcolor1",	"(255,255,255)",is_color, 'Color of the fixation dot'),
		("fixcolor2",	"(128,128,128)",is_color),
		("min_err",		"0",		   	is_int),
		("max_err",		"100",		   	is_int),
		("fixwait",		"100",		   	is_int),
		("Reward Params", None, None),
		("numdrops",    "4",           is_int, "Number of juice drops"),
		("rmult",		"1.0",		   	is_float),
		("Misc Params", None, None, "Miscelaneous Parameters"),
		("Recent Buffer Size", "50", is_int, "The number of trials to use to calculate recent performance"),
		("pause_color", "(150,0,0)", is_color, "The screen will turn this color when the task is paused")
                ), file=parfile)

        #create parameter table and window to go along with it

    def encodeTaskParameters(self,app):
        #encode task parameters
	app.encode_plex('rfx')
	app.encode_plex(params['RF_Center_X'])
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
	app.encode('rfx')
	app.encode(params['RF_Center_X'])
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
    def encodeISI(self,app,myStim):
        pass
    def encodeITI(self,app):
        pass

    def createStimuli(self,app):
        #create stimuli and store in myStims
        pass
        
    def cleanup(self,app):
        #delete parameter table and anything else we created
        self.myTaskParams.destroy()

    def getStimulus(self, index):
	print 'lindaa lindaa 2'
	print index
	return self.myStims[index]
        #return self.myStims[self.myStimList[index]]

    def getNumStim(self):
        return self.numStim
        
    def runSet(self,app):
    	"""
	This is what is run when you hit the 'start' button (set as such in
	the 'main' function, defined at the end of this file).
	"""

	# tally collects the results of the last N trials and displays a
	# running tally at the bottom of the main pype control window
	app.tally(clear=1)
	
	# This erases any information printed to the console
	#app.console.clear()
	
	# Update the task's representation of all the parameters set in the
	# task parameter table, rig_params and monk_params - always called P
        #app.params = ParamTable(None, (), None)        
	P = app.getcommon()
	params = self.myTaskParams.check()

	# Save this version (in case you've made changes since the last time
	# the .par file was updated).

        #P.save()
	#params.save()


	#Set the record filename if the task wants to:
	rFileName = self.getRecordFileName()
	if(rFileName is not None):
            if(os.path.exists(rFileName)):
            	if ask("pype", "overwrite file: %s ?" % (rFileName), ("yes", "no")) == 0:
                    app.record_selectfile(fname=rFileName)
                else:
                    return
            else:
                app.record_selectfile(fname=rFileName)

        app.record_note('task_is', __name__)

	# Basic setup stuff, you shouldn't want to change this.
	app.paused = 0
	app.running = 1
	# Makes a little green light/red light on the main pype window
	app.led(1)
	
	# Set various counters and markers in app.globals.  globals is an
	# instance of the Holder class (initialized in function "main,"
	# below), which just lets you store a bunch of variables inside app
	# in a reasonably neat way.
	# - repnum: number of reps completed, 
	# - ncorrect: number of trials correct
	# - ntrials: number of trials completed
	# - seqcorrect: count of how many trials in a row have been correct
	# - uicount: how many trials have been uninitiated (use with uimax)
	# - number of stimuli that have been seen for complete stim time

	app.globals.repnum = -1
	app.globals.ncorrect = 0
	app.globals.natmpt = 0
	app.globals.ntrials = 0
	app.globals.seqcorrect = 0
	app.globals.uicount = 0
	app.globals.stimCorrect = 0
	app.globals.errorcounter = 0
        #app.globals.yOffset = 600
        app.globals.yOffset = pype_plex_code_dict('plexYOffset')
	app.globals.plexStimIDOffset = pype_plex_code_dict('plexStimIDOffset')
	app.globals.plexRotOffset = pype_plex_code_dict('plexRotOffset')
	#vinhs set
	#app.globals.datatable = empty((6), dtype=int)
	app.globals.datatable = array(['trial','gap','mg','c','ans','rt','locx', 'locy'])

	self.createStimuli(app)
        self.encodeTaskParameters(app)

	print 'Done creating Stimuli'

	#initialize ITI timer, we are now in the first ITI
	t = Timer()

	# This call intiates the first ITI before the first trial.
	# Calling encode will make a note in the data record
	# with the current timestamp and whatever comment you give it.

	app.encode_plex(START_ITI)
	app.encode(START_ITI)
        self.encodeITI(app)
	# Calls RunTrial, and calculates a running percentage correct.
	try:
		# I added this to keep a running "recent" percentage correct
		# because perfomance often changes during the task.
		pctbuffer = list()
		
		# Call Run trial only if there are still unshown stimuli in
		# the stimorder buffer
		app.globals.repcounter = 0
		while app.running and (app.globals.repcounter < params['nRepsPerStim']):
			#This task implements pause (f5) at the trial level
			was_paused = 0
			while(app.paused):
				if(was_paused == 0):
					app.encode_plex('pause')
					app.encode('pause')
					app.globals.dlist.bg = params['pause_color']
					# Update the dlist and flip the framebuffer
					app.globals.dlist.update()
					app.fb.flip()
					was_paused = 1
				app.idlefn()
			if(was_paused): #reset background color
				app.encode_plex('unpause')
				app.encode('unpause')
				app.globals.dlist.bg = params['bg_during']
				# Update the dlist and flip the framebuffer
				app.globals.dlist.update()
				app.fb.flip()
                        P = self.myTaskParams.check(mergewith=app.getcommon())
		
                       	params = self.myTaskParams.check()

			try:
				# RunTrial is a function defined below that runs a
				# single trial.
				result,t = self.RunTrial(app,t)
			except UserAbort:
				# The escape key will abort a trial while it's running.
				result=None
				t.reset()
				pass
			# This if statement avoids a divide-by-zero error if the
			# first trial is aborted before ntrials is incremented
			if (app.globals.ntrials > 0 and params['Recent Buffer Size'] > 0):
				pctbuffer.append(result)
				# Average the performance over the past X trials.
				if(app.globals.ntrials < params['Recent Buffer Size']) :
					recent=100*(app.globals.ncorrect/app.globals.ntrials)
				else:
					lastX = pctbuffer[len(pctbuffer) - params['Recent Buffer Size']::]
					recent=100*lastX.count(CORRECT_RESPONSE)/len(lastX)

				stimPerTrial =  float(app.globals.stimCorrect+(app.globals.repcounter*len(app.globals.stimidlistOrig)))/ float(app.globals.ntrials)
			else:
				stimPerTrial = 0.0
			# This call prints the overall and recent perf % to console
			if(app.globals.natmpt == 0):
                                over_beh = 0.0
                        else:
                                over_beh = 100.0*app.globals.ncorrect/app.globals.natmpt

			con(app, " %s:%d %d/%d %.0f%% beh: %.0f%%  (recent %.0f%%)\n %0.2f stims per trial" % \
				(now(), app.nreps(),app.globals.ncorrect, app.globals.ntrials, 100.0 * app.globals.ncorrect / app.globals.ntrials, over_beh, recent,stimPerTrial), 'black')
                        #update the behavioral history and tally
                        if(result is None):
                            app.tally(type=USER_ABORT)
                            app.history(USER_ABORT)
                        elif(iscorrect(result)):
                            app.tally(type=CORRECT_RESPONSE)
                            app.history(CORRECT_RESPONSE)
                        elif(result == BREAK_FIX):
                            app.tally(type=BREAK_FIX)
                            app.history(BREAK_FIX)
                        elif(isui(result)):
                            app.tally(type=UNINITIATED_TRIAL)
                            app.history(UNINITIATED_TRIAL)
                        else:
                            app.tally(NO_RESP)
                            app.history(NO_RESP)

                        
	except:
		# If there's an error generated inside the try statement,
		# it drops to here - reporterror tries to exit cleanly instead
		# of crashing the machine.
		reporterror()
	
	# More housekeeping stuff, also shouldn't change.
	app.repinfo()
	app.running = 0
	app.led(0)
	# standard beep sequence when you hit the "stop" button.
	app.warn_run_stop()
	# marks the data file as done so you know everything is complete.
	app.record_done()

        #Set the record filename back to '' so we don't overwrite things
	rFileName = self.getRecordFileName()
	if(rFileName is not None):
            app.record_selectfile(fname='')

	# This is the end of the RunSet function.
	return 1

    def RunTrial(self,app, t):
	"""
	RunTrial is called by RunSet.  It does housekeeping stuff associated
	with recording behavioral data for an individual trial, and calls the
	_RunTrial function which actually does the stimulus presentation and
	task control. 
	"""
	# On every trial, we check to see if any parameters have been updated
	# while the last trial was running
      	P = self.myTaskParams.check(mergewith=app.getcommon())
	params = self.myTaskParams.check()


        

	# Note the time that the trial started, again explicitly handled
	# in PypeFile class.
	# Do we need this?
	# Note that the comment above is not accurate.  the time is actually the time that RunTrial is called, the actual trial has not yet started, although the ITI has
	app.record_note('trialtime', (app.globals.ntrials, Timestamp()))

	
	# This call starts the data record for this trial. The datafile will
	# have a 'start' event encoded with timestamp = 0. Also plexon will 
	# have an event encoded - I think this doesn't happen anymore
	app.record_start()
	
	# This function will actually do the task control and stimulus display
	# and return its results back here for housekeeping.
	(result, rt,t) = self._RunTrial(app,t)
	
	# Stop recording for this trial, reset eye trace and signal trial stop
	# to Plexon- I think this doesn't happen anymore.  Encode 'stop' in the datafile, which is the very last
	# thing to get
	app.record_stop()
	
	# VERY IMPORTANT, this call actually writes all of the info collected
	# in this trial into the datafile.  Don't muck with it.
	app.record_write(result, rt, P, taskinfo=None)
	
	# Check to see whether we've exceeded the max allowable uninitiated
	# trials, and if so, pop up a little warning box that will stall the
	# task until the user clicks it.  Note result is one of the variables
	# returned by _RunTrial.
	if result == UNINITIATED_TRIAL:
		app.globals.uicount = app.globals.uicount + 1
		if app.globals.uicount > P['uimax']:
			warn('Warning',
				 'UI Count exceeded @ %s\nPlease intervene.\n' % now(), wait=1)
			app.globals.uicount = 0
	else:
		# Re-set the uicount after every good trial, so uimax can only
		# be exceeded by a number of ui trials in a row.  Otherwise,
		# the count would be cumulative
		app.globals.uicount = 0
	
	# This is the end of RunTrial.  In RunSet, the call to RunTrial expects
	# the 'result' variable to get returned, and this is how we do that:
	return result,t

    def _RunTrial(self,app, t):
	"""
	_RunTrial actually does the behavioral control for the task and shows
	whatever stimuli are specified, etc.  This is the meat of the task,
	and this is where you're going to make changes to make the task do
	what you want it to do. 
	"""
	
	# # # # # # # # # # # # # # # # # #
	# General setup stuff
	# # # # # # # # # # # # # # # # # #

	# Create a second instances of Timer class (also in pype.py), which counts 
	# milliseconds until it's reset. Can be queried without reset
	t2 = Timer()

	# Get the parameters again
      	P = self.myTaskParams.check(mergewith=app.getcommon())

	params = self.myTaskParams.check()

	# Draw a line at the beginning of every trial
	con(app,">---------------------------")
	# You can write anything you want to the console, and in color.
	con(app,"Next trial",'blue')
	
	# Initialize default reaction time in case trial is aborted
	rt = -1
	
	# Check for "testing" mode (rig params table; no eye or bar monitoring)
	TESTING = int(P['testing'])
	if TESTING:
		# put a big red note on the console so I don't forget
		con(app, 'TESTING','red')
	
	# Clear the user display before starting
	app.udpy.display(None)
	
	# The dlist manages what gets shown on the screen, it gets
	# re-initialized every trial.  app.fb is the framebuffer
	app.globals.dlist = DisplayList(app.fb)
	# set the background color - in this case, I've got a color defined
	# for the intertrial interval
	#app.globals.dlist.bg = params['bg_before']
        app.globals.dlist.bg = params['bg_before']
	# Update the dlist and flip the framebuffer
	app.globals.dlist.update()
	app.fb.flip()
	# At this point, screen color is bg_before, and otherwise blank.
	
	# # # # # # # # # # # # # # # # # #
	# Code for making a fixation spot
	# # # # # # # # # # # # # # # # # #
	 
	# Fixation position at P['fix_x'] and P['fix_y'], which are in the
	# monk_params table
	fx, fy = P['fix_x'], P['fix_y']

	# I'm not clear on what this does, but it has something to do with
	# aligning the user display, and you need it.
	app.looking_at(fx, fy)

	# Here is some basic fixation point code. Depth sets the layer of sprite
	# Always set fixspot to be layer 0; other stimuli to be layers below
	# i.e. set depth higher for other stimuli Note that fix_size and 
	# fix_ring are from monk_params, but fixspot color has to be 
	# specified by the task.
	
	if P['fix_ring'] > 0:
		# Create the sprite
		spot = Sprite(2*P['fix_ring'], 2*P['fix_ring'],
					  fx, fy, fb=app.fb, depth=0, on=0, centerorigin=1)
		# fill the square with bg color
		spot.fill(params['bg_during'])
		# make a black circle of radius fix_ring at the center of the
		# sprite
		spot.circlefill((1,1,1), r=P['fix_ring'], x=0, y=0)
		# and now for the actual fixation point...
		if P['fix_size'] > 1:
			# make another circle of radius fix_size
			spot.circlefill(params['fixcolor1'], r=P['fix_size'], x=0, y=0)
		else:
			# just color the center pixel - r=1 doesn't work well
			spot[0,0] = params['fixcolor1']
	else:
		# Create a sprite without the surrounding ring
		spot = Sprite(2*P['fix_size'], 2*P['fix_size'],
					  fx, fy, fb=app.fb, depth=0, on=0, centerorigin=1)
		spot.fill(params['bg_during'])
		if P['fix_size'] > 1:
			spot.circlefill(params['fixcolor1'], r=P['fix_size'], x=0, y=0)
		else:
			spot[0,0] = params['fixcolor1']
	
	# This is redundant with on=0 above, but make sure the sprite is off
	spot.off()
	# Add spot to the dlist
	app.globals.dlist.add(spot)
	
	# # # # # # # # # # # # # # # # # #
	# Code for making the fixation window
	# # # # # # # # # # # # # # # # # #
	
	# This is the virtual boundary that defines a "good" fixation,
	# again only necessary if yours is a fixation task.
	
	# Adjust fixation window size for target eccentricity, since it's
	# harder to fixate on more eccentric points and there's more
	# eye tracker error too.  The min and max error parameters are
	# task-specific.
	min_e, max_e = params['min_err'], params['max_err']
	r = ((fx**2)+(fy**2))**0.5
	z = min_e + (max_e - min_e) * r / ((app.fb.w+app.fb.h)/4.0)
	
	# Set a parameter value that's the actual window size to use
	# this trial, so it's saved in data file.
	P['_winsize'] = int(round(P['win_size'] + z))
	
	# Create an instance of the FixWin class (defined in pype.py) that
	# will actually keep track of the eye position for you
	fixwin = FixWin(fx, fy, P['_winsize'], app)
	fixwin.draw(color='grey') #draws the fixwin radius on user display

    ##### Now create the visual stimuli
	stm_start = app.globals.stimCorrect
	print 'beforemakestim'
	print 'stm_start'
	print stm_start
	print 'error counter'
	print app.globals.errorcounter
	print 'length of stimidlist'
	print len(app.globals.stimidlist)
	print 'length of mystims'
	print len(self.myStims)
	print 'rep counter'
	print app.globals.repcounter
	#print app.globals.stimidlist[stm_start+1]
	#print app.globals.mglist[stm_start+1]
	#print app.globals.xandylist[stm_start+1]
	#print app.globals.gaplist[stm_start+1]
	#print self.diameter[stm_start+1]
	#print self.myForegroundXOffset[stm_start+1]
	#print self.myForegroundYOffset[stm_start+1]
	#print self.myMidgroundXOffset[stm_start+1]
	#print self.myMidgroundYOffset[stm_start+1]
	#print self.barXOffset[stm_start+1]
	#print self.barYOffset[stm_start+1]
	#print self.myFactory[stm_start]

	#if(len(app.globals.stimidlist)!= stm_start+1): #and (len(self.myStims)==(2*stm_start)+2):
	
		#if(params['ReverseOrder']):
			#if(params['MGonly']):
				#stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.mglist[stm_start+1], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start+1], self.diameter[stm_start+1], self.myForegroundXOffset[stm_start+1], self.myForegroundYOffset[stm_start+1], self.myMidgroundXOffset[stm_start+1], self.myMidgroundYOffset[stm_start+1], self.barXOffset[stm_start+1], self.barYOffset[stm_start+1], self.myFactory[stm_start+1], self.rotVals,cacheSprite=1, useCache=1)
				#self.myStims.extend(stimList)
				#stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.stimidlist[stm_start+1], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start+1], self.diameter[stm_start+1], self.myForegroundXOffset[stm_start+1], self.myForegroundYOffset[stm_start+1], self.myMidgroundXOffset[stm_start+1], self.myMidgroundYOffset[stm_start+1], self.barXOffset[stm_start+1], self.barYOffset[stm_start+1], self.myFactory[stm_start+1], self.rotVals,cacheSprite=1, useCache=1)
				#self.myStims.extend(stimList)
			#else:
				#stimList = self.getComplex(self.gapMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.mglist[stm_start+1], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start+1], self.diameter[stm_start+1], self.myForegroundXOffset[stm_start+1], self.myForegroundYOffset[stm_start+1], self.myMidgroundXOffset[stm_start+1], self.myMidgroundYOffset[stm_start+1], self.barXOffset[stm_start+1], self.barYOffset[stm_start+1], self.myFactory[stm_start+1], self.myForegroundXOffset[stm_start+1] + app.globals.gaplist[stm_start+1], self.rotVals,cacheSprite=1, useCache=0)
				#self.myStims.extend(stimList)
				#stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.stimidlist[stm_start+1], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start+1], self.diameter[stm_start+1], self.myForegroundXOffset[stm_start+1], self.myForegroundYOffset[stm_start+1], self.myMidgroundXOffset[stm_start+1], self.myMidgroundYOffset[stm_start+1], self.barXOffset[stm_start+1], self.barYOffset[stm_start+1], self.myFactory[stm_start+1], self.rotVals,cacheSprite=1, useCache=1)
				#self.myStims.extend(stimList)
		#else:
			#if(params['MGonly']):
				#print 'lindaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
				#stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.stimidlist[stm_start+1], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start+1], self.diameter[stm_start+1], self.myForegroundXOffset[stm_start+1], self.myForegroundYOffset[stm_start+1], self.myMidgroundXOffset[stm_start+1], self.myMidgroundYOffset[stm_start+1], self.barXOffset[stm_start+1], self.barYOffset[stm_start+1], self.myFactory[stm_start+1], self.rotVals,cacheSprite=1, useCache=0)
				#self.myStims.extend(stimList)
				#stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.mglist[stm_start+1], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start+1], self.diameter[stm_start+1], self.myForegroundXOffset[stm_start+1], self.myForegroundYOffset[stm_start+1], self.myMidgroundXOffset[stm_start+1], self.myMidgroundYOffset[stm_start+1], self.barXOffset[stm_start+1], self.barYOffset[stm_start+1], self.myFactory[stm_start+1], self.rotVals,cacheSprite=1, useCache=0)
				#self.myStims.extend(stimList)
				#print len(self.myStims)
			#else:
				#print 'lindaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa'
				#stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.stimidlist[stm_start+1], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start+1], self.diameter[stm_start+1], self.myForegroundXOffset[stm_start+1], self.myForegroundYOffset[stm_start+1], self.myMidgroundXOffset[stm_start+1], self.myMidgroundYOffset[stm_start+1], self.barXOffset[stm_start+1], self.barYOffset[stm_start+1], self.myFactory[stm_start+1], self.rotVals,cacheSprite=1, useCache=0)
				#self.myStims.extend(stimList)
				#stimList = self.getComplex(self.gapMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.mglist[stm_start+1], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start+1], self.diameter[stm_start+1], self.myForegroundXOffset[stm_start+1], self.myForegroundYOffset[stm_start+1], self.myMidgroundXOffset[stm_start+1], self.myMidgroundYOffset[stm_start+1], self.barXOffset[stm_start+1], self.barYOffset[stm_start+1], self.myFactory[stm_start+1], self.myForegroundXOffset[stm_start+1] + app.globals.gaplist[stm_start+1], self.rotVals,cacheSprite=1, useCache=0)
				#self.myStims.extend(stimList)
				#print len(self.myStims)
	#else:
	if(params['ReverseOrder']):
			if(params['MGonly']):
				stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.mglist[stm_start], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start], self.diameter[stm_start], self.myForegroundXOffset[stm_start], self.myForegroundYOffset[stm_start], self.myMidgroundXOffset[stm_start], self.myMidgroundYOffset[stm_start], self.barXOffset[stm_start], self.barYOffset[stm_start], self.myFactory[stm_start], self.rotVals,cacheSprite=1, useCache=1)
				self.myStims.extend(stimList)
				stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.stimidlist[stm_start], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start], self.diameter[stm_start], self.myForegroundXOffset[stm_start], self.myForegroundYOffset[stm_start], self.myMidgroundXOffset[stm_start], self.myMidgroundYOffset[stm_start], self.barXOffset[stm_start], self.barYOffset[stm_start], self.myFactory[stm_start], self.rotVals,cacheSprite=1, useCache=1)
				self.myStims.extend(stimList)
			else:
				stimList = self.getComplex(self.gapMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.mglist[stm_start], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start], self.diameter[stm_start], self.myForegroundXOffset[stm_start], self.myForegroundYOffset[stm_start], self.myMidgroundXOffset[stm_start], self.myMidgroundYOffset[stm_start], self.barXOffset[stm_start], self.barYOffset[stm_start], self.myFactory[stm_start], self.myForegroundXOffset[stm_start] + app.globals.gaplist[stm_start], self.rotVals,cacheSprite=1, useCache=0)
				self.myStims.extend(stimList)
				stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.stimidlist[stm_start], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start], self.diameter[stm_start], self.myForegroundXOffset[stm_start], self.myForegroundYOffset[stm_start], self.myMidgroundXOffset[stm_start], self.myMidgroundYOffset[stm_start], self.barXOffset[stm_start], self.barYOffset[stm_start], self.myFactory[stm_start], self.rotVals,cacheSprite=1, useCache=1)
				self.myStims.extend(stimList)
	else:
			if(params['MGonly']):
				
				stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.stimidlist[stm_start], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start], self.diameter[stm_start], self.myForegroundXOffset[stm_start], self.myForegroundYOffset[stm_start], self.myMidgroundXOffset[stm_start], self.myMidgroundYOffset[stm_start], self.barXOffset[stm_start], self.barYOffset[stm_start], self.myFactory[stm_start], self.rotVals,cacheSprite=1, useCache=0)
				self.myStims.extend(stimList)
				stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.mglist[stm_start], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start], self.diameter[stm_start], self.myForegroundXOffset[stm_start], self.myForegroundYOffset[stm_start], self.myMidgroundXOffset[stm_start], self.myMidgroundYOffset[stm_start], self.barXOffset[stm_start], self.barYOffset[stm_start], self.myFactory[stm_start], self.rotVals,cacheSprite=1, useCache=0)
				self.myStims.extend(stimList)
				
			else:
				
				stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.stimidlist[stm_start], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start], self.diameter[stm_start], self.myForegroundXOffset[stm_start], self.myForegroundYOffset[stm_start], self.myMidgroundXOffset[stm_start], self.myMidgroundYOffset[stm_start], self.barXOffset[stm_start], self.barYOffset[stm_start], self.myFactory[stm_start], self.rotVals,cacheSprite=1, useCache=0)
				self.myStims.extend(stimList)
				stimList = self.getComplex(self.gapMode+self.perceptModeOffset[self.perceptShapes[0]],None, self.perceptShapes[0], app.globals.mglist[stm_start], self.midgroundColor, self.foregroundColor, app.globals.xandylist[stm_start], self.diameter[stm_start], self.myForegroundXOffset[stm_start], self.myForegroundYOffset[stm_start], self.myMidgroundXOffset[stm_start], self.myMidgroundYOffset[stm_start], self.barXOffset[stm_start], self.barYOffset[stm_start], self.myFactory[stm_start], self.myForegroundXOffset[stm_start] + app.globals.gaplist[stm_start], self.rotVals,cacheSprite=1, useCache=0)
				self.myStims.extend(stimList)
				
			#numUniqueStims = len(self.myStims)
        		#stimNumbers = arange(0,numUniqueStims)
        		#self.myStimList.extend(stimNumbers)
        		#self.numStim = self.numStim + len(self.myStims)
			#print self.myStimList
			#print self.numStim

	stim_arr = [] #empty list
	####This is for multiple stimulus presentation; number of stimuli to
        ####be shown in this run is min of P['nstim'] and the number of
	####stimuli left
	
	con(app,"%d stimuli presented, %d stimuli remaining" % (((stm_start+(len(app.globals.stimidlistOrig)*app.globals.repcounter))-app.globals.errorcounter),(self.getNumStim()/2)-((stm_start-app.globals.errorcounter)+(app.globals.repcounter*len(app.globals.stimidlistOrig)))),"Black")
	#sshow = min(params['nstim'], self.getNumStim()-stm_start)
	sshow = 2
	print 'aftermakestim'
	print 'stm_start'
	print stm_start
	print 'error counter'
	print app.globals.errorcounter
	print 'length of stimidlist'
	print len(app.globals.stimidlist)
	print 'length of mystims'
	print len(self.myStims)
	print 'rep counter'
	print app.globals.repcounter

        for i in arange(0,sshow):
            spr = self.getStimulus((2*stm_start)+i)
            stim_arr.append(spr)
 #           #app.globals.dlist.add(stim_arr[i])
            stim_arr[i].off()
            app.globals.dlist.update()
									
	
	# # # # # # # # # # # # # # # # # #
	# Initiate the trial
	# # # # # # # # # # # # # # # # # #

	# Start monitoring the eye trace.  This encodes an 'eye_start' event
	# in the datafile that will always be equal to the first timestamp
	# at which eyetrace data are collected.
	app.eyetrace(1)

	# set background color to the color defined for during the trial
	app.globals.dlist.bg = params['bg_during']
	app.globals.dlist.update()
	
	# Note that we haven't flipped the framebuffer yet...
	
	# We put the entire trial inside a try statement 
	# with exceptions to stop trial(correct, incorrect, aborted).
	try:
		# The idlefn method just lets the program do background
		# maintenance stuff.  You can give idlefn an argument that
		# specifies a number of milliseconds to wait
		# Timer t was set at the very beginning of the trial,
		# I want to know how long it's been since then.)
		app.idlefn(params['iti']-t.ms())
		app.encode_plex(END_ITI)
		app.encode(END_ITI)

		#remember we already encoded START_ITI

		# Reset this timer to zero
		t.reset()
		
		# Flip the framebuffer to show the current dlist
		app.fb.flip()

		fixwin.draw(color='red')
		ttt = fixwin.on()
		# Now the background color is bg_during
		# set a little dummy flag to keep track of stuff
		spot_on=0
		# When we get here either the bar has been grabbed or we're not
		# monitoring it.  If the fixation point is not already
		# on, we'll turn it on now.
		if not spot_on:
			spot.on()
			app.globals.dlist.update()
			app.fb.flip()
			app.udpy.display(app.globals.dlist)
			spot_on=1
		# Now we're waiting for the subject to acquire the fixation point
		info(app, "waiting fix acquisition")
		app.idlefn()
		t.reset()
		# Again, a dummy flag to help with task control
		go_on = 0
		while not go_on:
			# We are waiting for the eye position to move inside the
			# fixation window.  Whether this is the case is one of
			# the things that the FixWin class keeps track of.
			while not fixwin.inside() and not TESTING:
				# We use the same abortafter limit again
				if P['abortafter'] > 0 and t.ms() > P['abortafter']:
					info(app, "no acquisition")
					con(app, "no acquisition", 'blue')
					#app.encode_plex(UNINITIATED_TRIAL)
					#app.encode(UNINITIATED_TRIAL)
					beep(2000,100)
					result = UNINITIATED_TRIAL
					raise MonkError
				app.idlefn()
			# At this point, the fixwin.inside returned 1 (meaning eye
			# is inside window).  Sometimes if the spot has just come
			# on and the subject is in the process of saccading across
			# the screen, the eye position will go through the fixwin.
			# Only count this as acquiring fixation if the eye stays in
			# the window for "fixwait" milliseconds.
			t2.reset()
			# First, assume we will continue if eye stays in window
			go_on = 1
			while t2.ms() < params['fixwait']:
				if not fixwin.inside() and not TESTING:
					# If at any time during the fixwait the eye
					# moves back out of the window, go back to waiting
					# for the eye to enter the window again.
					info(app, "passthrough")
					go_on = 0
					# This resets fixwin.inside back to zero
					fixwin.reset()
					# This exits the innermost while loop, and sends
					# us back to the top of the "while not go_on"
					# loop
					break

		# # # # # # # # # # # # # # # # # #
		# Do real trial stuff
		# # # # # # # # # # # # # # # # # #
	
		# Now, fixation has been acquired.  We can start timing the
		# length of the fixation.
		t.reset() # Reset the timer to monitor fixation length for each stim
		t2.reset() #We will now use t2 as an absolute timer for this trial

		app.encode_plex(FIX_ACQUIRED)
		app.encode(FIX_ACQUIRED) # Standard event encoding
		fixwin.draw(color='blue') # Blue is our "active" fixwin color

		####This is for multiple stimulus presentation; number of stimuli to
		####be shown in this run is min of P['nstim'] and the number of
		####stimuli left
		scount = 0

		#print 'scount'
		#print scount
		#print 'sshow'
		#print sshow

		while scount < sshow:
			#print 'scount2'
			#print scount
                    	P = self.myTaskParams.check(mergewith=app.getcommon())
                        self.encodeISI(app,stim_arr[scount])

                        #Find stimuli that appear after onset of stimulus
			sp_onsets = stim_arr[scount].getSpriteOnsets()
			nextSpriteOnTime = params['stimon']
			donePresenting = 0
			for spriteNum in range(0,len(sp_onsets)):
                            if(sp_onsets[spriteNum] >= 1 and sp_onsets[spriteNum] < nextSpriteOnTime):
                                nextSpriteOnTime = sp_onsets[spriteNum]

			while t.ms() < params['IStime']:
			#vinh edit
			#c = 'b'
		
			#while not c == 'a':
				#while c:
					#(c, ev) = app.keyque.pop()
				#(c, ev) = app.keyque.pop()
				if fixwin.broke() and not TESTING:
					app.encode_plex(FIX_LOST)
					app.encode(FIX_LOST) #standard event code
					info(app, "early break")
					con(app, "early break at %d, %d ms into ISI of stim %d, fixwin time of %d" % (t2.ms(),t.ms(),scount, fixwin.break_time()), 'red')
					#app.encode('exact_fix_lost=%d' % fixwin.break_time())
					result = BREAK_FIX
					# Auditory feedback
					app.warn_trial_incorrect(flash=None)
					# Skip to end of trial
					raise MonkError
				# Again, a call to idlefn lets the computer catch up
				# and monitor for key presses.
				app.idlefn()

			#con(app, "Response Time (%d ms)" % t.ms(), 'red')

			# now display stimulus 
			# now turn on all sprites in stimulus with onset times of 0 and put them on the dlist
			stimSprites = stim_arr[scount].getSpritesWithOnsetLessThan(1)
                        for spriteNum in range(0,len(stimSprites)):
                            app.globals.dlist.add(stimSprites[spriteNum])
                            stimSprites[spriteNum].on()
                        #now if the task wants to display some sort of sprite representing the rf display it
                        rfSprite = self.getRFSprite()
                        if(rfSprite is not None):
                            app.globals.dlist.add(rfSprite)
                            rfSprite.on()

			#update and flip buffer
			self.toggle_photo_diode(app) #note: toggle_photo_diode updates the dlist
			app.encode_plex(SAMPLE_ON)
			app.encode(SAMPLE_ON)
			app.fb.flip()

			app.udpy.display(app.globals.dlist)
			
			t.reset()
			while not donePresenting:
                            # wait until we need to reveal another sprite or we are done
                            curr_t_time = t.ms()
                            while curr_t_time < nextSpriteOnTime:
			    #vinh edit
			    #c = 'b'
			    #while not c == 'a':
				    #while c:
					#(c, ev) = app.keyque.pop()
				    #(c, ev) = app.keyque.pop()
                                    if fixwin.broke() and not TESTING:
                                        app.encode_plex(FIX_LOST)
                                        app.encode(FIX_LOST) #standard event code
                                        info(app, "early break")
                                        con(app, "early break at %d, %d ms into presentation of stim %d, fixwin time of %d" % (t2.ms(),t.ms(), scount,fixwin.break_time()), 'red')
                                        #app.encode('exact_fix_lost=%d' % fixwin.break_time())
                                        result = BREAK_FIX
                                        app.warn_trial_incorrect(flash=None)
                                        #turn off stimuli
                                        stim_arr[scount].off()
                                        app.fb.flip()
                                        # Skip to end of trial
                                        raise MonkError
                                    # Again, a call to idlefn lets the computer catch up
                                    # and monitor for key presses.
                                    app.idlefn()
                                    curr_t_time = t.ms()
			    #con(app, "Response Time (%d ms)" % t.ms(), 'red')
                            #turn on any sprites that need to be turned on now
                            stimSprites = stim_arr[scount].getSpritesWithOnsetEqualTo(nextSpriteOnTime)
                            for spriteNum in range(0,len(stimSprites)):
                                app.globals.dlist.add(stimSprites[spriteNum])
                                stimSprites[spriteNum].on()

                            #get nextSpriteOnTime if there are no more set donePresenting to 1
                            prevSpriteOnTime = nextSpriteOnTime
                            nextSpriteOnTime = params['stimon']
                            if(curr_t_time >= nextSpriteOnTime):
                                donePresenting = 1
                            for spriteNum in range(0,len(sp_onsets)):
                                if(sp_onsets[spriteNum] > prevSpriteOnTime and sp_onsets[spriteNum] < nextSpriteOnTime):
                                    #make sure we haven't already passed the ontime for this stim, if so put it on
                                    if(curr_t_time >= sp_onsets[spriteNum]):
                                        sp = getSprite(spriteNum)
                                        app.globals.dlist.add(sp)
                                        sp.on()
                                        # if we haven't reached the end of the trial set donePresenting to 0

                                        if(params['stimon'] > curr_t_time):
                                            donePresenting = 0
                                    #otherwise make it the nextSpriteOnTime and set donePresenting to 0
                                    else:
                                        nextSpriteOnTime = sp_onsets[spriteNum]
                                        donePresenting = 0
                            #update dlist, flip frame buffer and update udpy dlist
                            app.globals.dlist.update()
                            app.udpy.display(app.globals.dlist)  
                            app.fb.flip()

                                    
			# now turn off each sprite in stimulus
			stimSprites = stim_arr[scount].getSprites()
                        for spriteNum in range(0,len(stimSprites)):
                            #this could cause an error if the sprite hasn't been added to dlist
                            #app.globals.dlist.delete(stimSprites[spriteNum])
                            stimSprites[spriteNum].off()
                        if(rfSprite is not None):
                            rfSprite.off()
			self.toggle_photo_diode(app) #note: toggle_photo_diode updates the dlist
			app.fb.flip()

			t.reset() # Reset the timer to start ISI timer
			app.encode_plex(SAMPLE_OFF)
			app.encode(SAMPLE_OFF)
                        #if(not self.includedOnlyCompletedTrials()):
                            #app.globals.stimCorrect = app.globals.stimCorrect + 1
			scount = scount+1

                ## If we want to add another ISI at the end of the trial
                if(params['AddExtraISI']):
                    while t.ms() < params['IStime']:
                        if fixwin.broke() and not TESTING:
                                app.encode_plex(FIX_LOST)
                                app.encode(FIX_LOST) #standard event code
                                info(app, "early break")
                                con(app, "early break at %d, %d ms into ISI of stim %d, fixwin time of %d" % (t2.ms(),t.ms(),scount, fixwin.break_time()), 'red')
                                #app.encode('exact_fix_lost=%d' % fixwin.break_time())
                                result = BREAK_FIX
                                # Auditory feedback
                                app.warn_trial_incorrect(flash=None)
                                # Skip to end of trial
                                raise MonkError
                        # Again, a call to idlefn lets the computer catch up
                        # and monitor for key presses.
                        app.idlefn()

		## If we want to add another ISI at the end of the trial
                #if(params['AddExtraISI']):
                    #while t.ms() < params['IStime']:
		    #vinh edit
		    c = 'b'
		    pptest = 'notdone'
		    gap1 = app.globals.gaplist
		    stimid1 = app.globals.stimidlist
		    mgid1 = app.globals.mglist
		    locatid = app.globals.xandylist
		    # Just rotating the list here...
		    print stimid1
		    print app.globals.gaplist[stm_start]
		    print app.globals.stimidlist[stm_start]
		    print app.globals.mglist[stm_start]
		    print app.globals.xandylist[stm_start]

	    	    #gap1[:] = gap1[1:]+gap1[0:1]
		    gap2 = app.globals.gaplist[stm_start]
		    #stimid1[:] = stimid1[1:]+stimid1[0:1]
		    stimid2 = app.globals.stimidlist[stm_start]
		    #mgid1[:] = mgid1[1:]+mgid1[0:1]
		    mgid2 = app.globals.mglist[stm_start]
		    #locatid[:] = locatid[1:]+locatid[0:1]
		    locatid2 = app.globals.xandylist[stm_start]
		    #print gap1
		    print gap2
		    app.encode('test0')
		    app.encode(gap2)
		    #print mgid1
		    print mgid2
		    app.encode(mgid2)
		    #print stimid1
		    print stimid2
		    app.encode(stimid2)
		    #print locatid
		    #print locatid
		    print locatid2
		    app.encode(locatid2)
		    #while not c == 'a' or not c == 'l':
		    #app.globals.stimCorrect = app.globals.stimCorrect + 1
		    #app.globals.natmpt = app.globals.natmpt+1
		    while not pptest == 'done':
			while c:
				(c, ev) = app.keyque.pop()
			(c, ev) = app.keyque.pop()
			pptest = 'notdone'

                        #if fixwin.broke() and not TESTING:
                                #app.encode_plex(FIX_LOST)
                                #app.encode(FIX_LOST) #standard event code
                                #info(app, "early break")
                                #con(app, "early break at %d, %d ms into ISI of stim %d, fixwin time of %d" % (t2.ms(),t.ms(),scount, fixwin.break_time()), 'red')
                                ##app.encode('exact_fix_lost=%d' % fixwin.break_time())
                                #result = BREAK_FIX
                                ## Auditory feedback
                                #app.warn_trial_incorrect(flash=None)
                                ## Skip to end of trial
                                #raise MonkError
                        # Again, a call to idlefn lets the computer catch up
                        # and monitor for key presses.
			
			if c == 'm':
				if stimid2 == mgid2:
					responsetime = t.ms()
					print responsetime
					con(app, "Correct, match", 'blue')
					#app.globals.datatablepre = array([app.globals.ntrials + 1, gap2, mgid2, stimid2, 1, t.ms(), locatid2[0], locatid2[1]], dtype=int)
					#app.globals.datatable = vstack((app.globals.datatable, app.globals.datatablepre))
					con(app, "Response Time (%d ms)" % t.ms(), 'red')
					app.encode(responsetime)
					#print app.globals.datatable
					raise NoProblem
				else:
					responsetime = t.ms()
					print responsetime
					con(app, "Incorrect, not match", 'blue')
					#app.globals.datatablepre = array([app.globals.ntrials + 1, gap2, mgid2, stimid2, 0, t.ms(), locatid2[0], locatid2[1]], dtype=int)
					#app.globals.datatable = vstack((app.globals.datatable, app.globals.datatablepre))
					con(app, "Response Time (%d ms)" % t.ms(), 'red')
					app.encode(responsetime)
					#print app.globals.datatable

					result = WRONG_RESP
                                	# Auditory feedback
                                	app.warn_trial_incorrect(flash=None)
					raise MonkError
				#app.globals.datatable.apprend(app.globals.datatablepre)
				
				pptest = 'done'
			elif c == 'n':
				if not stimid2 == mgid2:
					responsetime = t.ms()
					print responsetime
					con(app, "Correct, not match", 'blue')
					#app.globals.datatablepre = array([app.globals.ntrials + 1, gap2, mgid2, stimid2, 1, t.ms(), locatid2[0], locatid2[1]], dtype=int)
					#app.globals.datatable = vstack((app.globals.datatable, app.globals.datatablepre))
					con(app, "Response Time (%d ms)" % t.ms(), 'red')
					app.encode(responsetime)
					#print app.globals.datatable
					raise NoProblem
				else:
					responsetime = t.ms()
					print responsetime
					con(app, "Incorrect, match", 'blue')
					#app.globals.datatablepre = array([app.globals.ntrials + 1, gap2, mgid2, stimid2, 0, t.ms(), locatid2[0], locatid2[1]], dtype=int)
					#app.globals.datatable = vstack((app.globals.datatable, app.globals.datatablepre))
					con(app, "Response Time (%d ms)" % t.ms(), 'red')
					app.encode(responsetime)
					#print app.globals.datatable

					result = WRONG_RESP
                                	# Auditory feedback
                                	app.warn_trial_incorrect(flash=None)
					raise MonkError
				pptest = 'done'
			elif c:
				con(app, "WRONG KEY", 'blue')
				app.encode_plex(FIX_LOST)
                                app.encode(FIX_LOST) #standard event code
                                info(app, "early break")
                                con(app, "You pressed the wrong button at %d, %d ms into ISI of stim %d, fixwin time of %d" % (t2.ms(),t.ms(),scount, fixwin.break_time()), 'red')
                                #app.encode('exact_fix_lost=%d' % fixwin.break_time())
                                result = NO_RESP
                                # Auditory feedback
                                app.warn_trial_incorrect(flash=None)
                                # Skip to end of trial
                                raise MonkError
			elif P['maxrt'] > 0 and t.ms() > P['maxrt']:
				info(app, "no target saccade")
                                con(app, "Time limit exceeded (%d ms)" % t.ms(), 'red')
                                result = NO_RESP
                                app.encode_plex(NO_RESP)
                                app.encode(NO_RESP)
                                beep(2000,100)
                                #app.globals.natmpt = app.globals.natmpt+1 #attempt only counts if it is either error response or correct.
                                raise MonkError
                        app.idlefn()
 
                #if(self.includedOnlyCompletedTrials()):
                	#app.globals.stimCorrect = app.globals.stimCorrect + scount
################################
		# If you are here then the trial is correct
		#print "Before raising NoProblem at %d abs time = %d" % (t.ms(), t2.ms())
		con(app, "Response Time (%d ms)" % t.ms(), 'red')
		raise NoProblem

	# # # # # # # # # # # # # # # # # #
	# Handling exceptions generated in the trial
	# # # # # # # # # # # # # # # # # #
	
	except UserAbort:
		# If you pressed the escape key at any time to abort the trial
		# you will end up here.  No counters are incremented or
		# reset basically because this was not the subject's fault.

		# Turn off the fixation spot and tracker dot
		spot.off()
		#app.encode(FIX_OFF)
		#app.encode_plex(FIX_OFF)

		# Stop monitoring eye position, encode 'eye_stop' in the datafile
		# which will always be the last timestamp at which eyetrace data
		# were collected.
		fixwin.clear()
		app.eyetrace(0)
		#app.encode_plex(EYE_STOP)
		#app.encode(EYE_STOP)

		# Re-set the background for the intertrial interval
		app.globals.dlist.bg = params['bg_before']
		self.turn_off_photo_diode(app)
		app.fb.flip()

		result = USER_ABORT
		app.encode_plex(result)
		app.encode(result)
		t.reset()
		app.encode_plex(START_ITI)
		app.encode(START_ITI)
		con(app, "Aborted.", 'red')
                return (result, rt, t)
            
	except MonkError:
		# Any of the MonkError exceptions will land you here.  The
		# trial counter is incremented and the seqcorrect counter
		# is reset.

		# Turn off the fixation spot and tracker dot
		spot.off()
		#app.encode(FIX_OFF)
		#app.encode_plex(FIX_OFF)

		# Stop monitoring eye position, encode 'eye_stop' in the datafile
		# which will always be the last timestamp at which eyetrace data
		# were collected.
		fixwin.clear()
		app.eyetrace(0)
		#app.encode_plex(EYE_STOP)
		#app.encode(EYE_STOP)

		# Re-set the background for the intertrial interval
		app.globals.dlist.bg = params['bg_before']
		app.globals.dlist.update()
		self.turn_off_photo_diode(app)
		app.fb.flip()
		#vinh note plex needed?
		app.encode_plex(result)
		app.encode(result)
		t.reset()
		app.encode_plex(START_ITI)
		app.encode(START_ITI)

		app.globals.ntrials = app.globals.ntrials + 1
		app.globals.stimCorrect = app.globals.stimCorrect + 1
		app.globals.seqcorrect = 0

		if(result != WRONG_RESP):
			app.globals.errorcounter = app.globals.errorcounter+1 
			app.globals.stimidlist.append(app.globals.stimidlist[stm_start])
			app.globals.mglist.append(app.globals.mglist[stm_start])
			app.globals.xandylist.append(app.globals.xandylist[stm_start])
			app.globals.gaplist.append(app.globals.gaplist[stm_start])
			self.diameter.append(self.diameter[stm_start])
			self.myForegroundXOffset.append(self.myForegroundXOffset[stm_start])
			self.myForegroundYOffset.append(self.myForegroundYOffset[stm_start])
			self.myMidgroundXOffset.append(self.myMidgroundXOffset[stm_start])
			self.myMidgroundYOffset.append(self.myMidgroundYOffset[stm_start])
			self.barXOffset.append(self.barXOffset[stm_start])
			self.barYOffset.append(self.barYOffset[stm_start])
			self.myFactory.append(self.myFactory[stm_start])
		else:
			app.globals.natmpt = app.globals.natmpt+1

		#if((app.globals.stimCorrect-app.globals.errorcounter) == len(app.globals.stimidlistOrig)):
		if((app.globals.stimCorrect+1) > len(app.globals.stimidlist)):
			app.globals.repcounter = app.globals.repcounter + 1
			app.globals.errorcounter = 0
			app.globals.stimCorrect = 0
			app.globals.stimidlist = []
			app.globals.stimidlist.extend(app.globals.stimidlistOrig)
			app.globals.mglist = []
			app.globals.mglist.extend(app.globals.mglistOrig)
			app.globals.xandylist = []
			app.globals.xandylist.extend(app.globals.xandylistOrig)
			app.globals.gaplist = []
			app.globals.gaplist.extend(app.globals.gaplistOrig)
			self.myStims = []
			self.diameter = []
			self.diameter.extend(self.diameterOrig)
			self.myForegroundXOffset = []
			self.myForegroundXOffset.extend(self.myForegroundXOffsetOrig)
			self.myForegroundYOffset = []
			self.myForegroundYOffset.extend(self.myForegroundYOffsetOrig)
			self.myMidgroundXOffset = []
			self.myMidgroundXOffset.extend(self.myMidgroundXOffsetOrig)
			self.myMidgroundYOffset = []
			self.myMidgroundYOffset.extend(self.myMidgroundYOffsetOrig)
			self.barXOffset = []
			self.barXOffset.extend(self.barXOffsetOrig)
			self.barYOffset = []
			self.barYOffset.extend(self.barYOffsetOrig)
			self.myFactory = []
			self.myFactory.extend(self.myFactoryOrig)
                	

                return (result, rt, t)
		
	except NoProblem:
		# Having an exception for a correct trial is handy because
		# there are a number of ways of getting the trial correct
		# depending on whether we're monitoring the eye position or
		# touch bar or dot dimming, and we can put all the reward
		# code in one place.

		# Turn off the fixation spot and tracker dot
		spot.off()
		#app.encode(FIX_OFF)
		#app.encode_plex(FIX_OFF)

		# Stop monitoring eye position, encode 'eye_stop' in the datafile
		# which will always be the last timestamp at which eyetrace data
		# were collected.
		fixwin.clear()
		app.eyetrace(0)
		#app.encode_plex(EYE_STOP)

		# Re-set the background for the intertrial interval
		app.globals.dlist.bg = params['bg_before']
		app.globals.dlist.update()
		self.turn_off_photo_diode(app)
		app.fb.flip()

		result = CORRECT_RESPONSE
		app.encode_plex(CORRECT_RESPONSE)
		app.encode(CORRECT_RESPONSE)

		

		# Without arguments this call dispenses a reward of size
                # 'dropsize' with a variance of 'dropvar' (both specified
		# in monk_params). The multiplier argument multiplies the
		# "standard" reward by whatever value is passed in.
		clk_num = params['numdrops']
		while clk_num > 0:
			app.reward(multiplier=params['rmult'])
			app.idlefn(50)#time between juice drops
			clk_num = clk_num-1

		# Reset the timer and Start the next ITI as soon as the reward for this trial has been dispensed.

		app.warn_trial_correct() #Standard "correct" beep
		#app.encode_plex(REWARD)

		t.reset()
		app.encode_plex(START_ITI)
		app.encode(START_ITI)

		# Increment the sequence correct counter
		app.globals.seqcorrect=app.globals.seqcorrect + 1
		# Reporting stuff, variables returned to RunTrial
		app.globals.ncorrect = app.globals.ncorrect + 1
		app.globals.ntrials = app.globals.ntrials + 1
		app.globals.natmpt = app.globals.natmpt+1
		app.globals.stimCorrect = app.globals.stimCorrect + 1

		if((app.globals.stimCorrect+1) > len(app.globals.stimidlist)):
			app.globals.repcounter = app.globals.repcounter + 1
			app.globals.errorcounter = 0
			app.globals.stimCorrect = 0
			app.globals.stimidlist = []
			app.globals.stimidlist.extend(app.globals.stimidlistOrig)
			app.globals.mglist = []
			app.globals.mglist.extend(app.globals.mglistOrig)
			app.globals.xandylist = []
			app.globals.xandylist.extend(app.globals.xandylistOrig)
			app.globals.gaplist = []
			app.globals.gaplist.extend(app.globals.gaplistOrig)
			self.myStims = []
			self.diameter = []
			self.diameter.extend(self.diameterOrig)
			self.myForegroundXOffset = []
			self.myForegroundXOffset.extend(self.myForegroundXOffsetOrig)
			self.myForegroundYOffset = []
			self.myForegroundYOffset.extend(self.myForegroundYOffsetOrig)
			self.myMidgroundXOffset = []
			self.myMidgroundXOffset.extend(self.myMidgroundXOffsetOrig)
			self.myMidgroundYOffset = []
			self.myMidgroundYOffset.extend(self.myMidgroundYOffsetOrig)
			self.barXOffset = []
			self.barXOffset.extend(self.barXOffsetOrig)
			self.barYOffset = []
			self.barYOffset.extend(self.barYOffsetOrig)
			self.myFactory = []
			self.myFactory.extend(self.myFactoryOrig)
			
                return (result, rt, t)
	
   
    def toggle_photo_diode(self,app):
            app.globals.dlist.update()
            app.fb.sync_toggle()

    def turn_off_photo_diode(self,app):
            app.fb.sync(0)

    def getRFSprite(self):
        return None

    def getRecordFileName(self): #gets the record file for this task
        return None

    def includedOnlyCompletedTrials(self):
        return 0
# End of xpptask

def RunSet(app):
    app.taskObject.runSet(app)

def cleanup(app):
    app.taskObject.cleanup(app)

def main(app):
    app.taskObject = pyschophysics(app)
    app.globals = Holder()
    app.idlefb()
    app.startfn = RunSet

# This is also something that all tasks have, and it's a python thing.
# Don't touch it.

if not __name__ == '__main__':
        loadwarn(__name__)
else:
        dump(sys.argv[1])

class pyschophysics(xFixationTask):

    def __init__(self, app):
        self.createParamTable(app)
        self.app = app
        self.myStims = list()
        self.numStim = 0
        self.myStimList = list()
        self.circleMode = 1
        self.perceptMode = 1
        self.blankMode = 1
        self.gapMode = 1
	self.midgroundOnlyMode = 1
        self.perceptModeOffset = list()
        self.perceptModeOffset.append(None)
        self.perceptModeOffset.append(0)
        self.perceptModeOffset.append(30)
        self.perceptModeOffset.append(60)
        #self.numB8Shapes = 76
	self.numB8Shapes = 51
        self.numPerceptObjects = 3
        #self.B8ShapeSet = arange(1,self.numB8Shapes+1)
	self.B8ShapeSet = [x+1 for x in range(self.numB8Shapes)]
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

##        self.modeFuncDict = {
##            1: getPercept
##            2: getComplex
##            3: getMidground
##            4: getForeground
##            }

    def createStimuli(self,app):            #Create Stimuli - Create stimuli called at beginning
        self.params = self.myTaskParams.check()
        params = self.params
        P = app.getcommon()
        #P = self.myTaskParams.check(mergewith=app.getcommon())
        self.myStims = list()
        self.numStim = 0
        self.myStimList = list()
        myFB = app.fb
        myX = params['RF_Center_X']
        myY = params['RF_Center_Y']
	myXandY = eval(params['RF_Center'])
        fixX = P['fix_x']
        fixY = P['fix_y']
        myBG = params['bg_during']
        randomize_stims = params['randomize_stimuli']
        midgroundColor = params['MidgroundColor']
        foregroundColor = params['ForegroundColor']
        self.myBG = myBG
        self.myFB = myFB
        self.myX = myX
        self.myY = myY
	self.myXandY = myXandY
        self.fixX = fixX
        self.fixY = fixY
        self.myBG = myBG
        self.midgroundColor = midgroundColor
        self.foregroundColor = foregroundColor
        self.randomize = randomize_stims
        stims = list()
        #self.ecc = ( (myX-fixX)**2 + (myY-fixY)**2)**0.5
        #if(params['RF Scale On Ecc']):
        #        self.size = int((P['mon_ppd'] * params['RF Offset']) +  (params['RF Scaling'] * self.ecc))
        #else:
        #        self.size = 2*params['RF Radius']

        #self.size is diameter of receptive field, also width and height of bounding square
        #self.diameter = self.size
        #self.radius = self.size/2.0
        self.rots = params['NumRotations']
        self.rotVals = range(0,360+(360/self.rots)-(360/self.rots),(360/self.rots) )
        #self.myForegroundXOffset = params['foregroundXOffset'] * self.size/2
        #self.myForegroundYOffset = params['foregroundYOffset'] * self.size/2
        #self.myMidgroundXOffset = params['circleXOffset'] * self.size/2
        #self.myMidgroundYOffset = params['circleYOffset'] * self.size/2
        self.myMidgroundScaling = params['circleScaling']
        self.myForegroundScaling = params['foregroundScaling'] 
        #self.barXOffset= params['barXOffset']  * self.size/2
        #self.barYOffset= params['barYOffset']  * self.size/2
        self.barAspect = params['barAspect']
        self.barScaling = params['barScaling']
        self.hour_vert_curv = params['hour_vert_curv']
        self.hour_horiz_curv = params['hour_horiz_curv']
        #self.myFactory = b8StimFactory(self.diameter*2,self.radius)
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
        #for k in arange(0, size(self.perceptShapes,0)):
        #    stimList,dummyVar = self.getPercept(self.perceptMode,None,self.perceptShapes[k], None, self.midgroundColor, None, self.rotVals)
        #    for i in arange(0,(params['PerceptsPerBlock'])):
        #        self.myStims.extend(stimList)
	app.globals.gaplistpre = list()
	app.globals.gaplistpre2 = list()
	app.globals.gaplist = list()
	app.globals.stimidlistpre = list()
	app.globals.stimidlistpre2 = list()
	app.globals.stimidlist = list()
	app.globals.mglistpre = list()
	app.globals.mglist = list()
	app.globals.xandylistpre = list()
	app.globals.xandylistpre2 = list()
	app.globals.xandylist = list()
	app.globals.xandylist2 = list()
        #if(params['UseAllComplexStims'] == 1):
            #complexStims = self.B8ShapeSet
        #else:           
        if(params['Reference_Mode'] == 3):
		mpicklist = self.B8ShapeSet
		complexStims = []
		for j in arange(0,params['RandomStimNum']):
			complexStims.append(choice(self.B8ShapeSet))
	else:
        	complexStims = eval(params['ComplexStimNums'])
	    #if(randomize_stims):
		    	#shuffle(complexStims)
        #Mode 2 - Complex Shape Mode AKA Occluded Mode
	
        if(params['Present_Gap_Mode']):
	    for l in arange(0,len(myXandY)):
            	for k in arange(0, size(self.perceptShapes,0)):
		    app.globals.gapLengths = eval(params['GapDistance'])
                    for i in arange(0,len(app.globals.gapLengths)):
		    	
		    	#print app.globals.gapLengths
		    	#if(randomize_stims):
		    		#shuffle(app.globals.gapLengths)
		    	#app.globals.gaplist = app.globals.gapLengths
		    	#Making gap and stim lists here
		    	for j in arange(0,len(complexStims)):
				app.globals.gaplistpre.append(app.globals.gapLengths[i])
				app.globals.stimidlistpre.append(complexStims[j])
				app.globals.xandylistpre.append(myXandY[l])
	    #print app.globals.gaplistpre
	    

        #Mode 1 Add blanks
        for j in arange(0,params['nBlanks']):
            stim = stimulus(self.blankMode,self.blankID,0)
            s = createBar(self.radius, self.radius, myFB,myBG, 0, myX, myY, myBG)
            stim.addSprite(s, myBG, 0)
            self.myStims.append(stim)

	#for i in arange(0,params['nRepsPerStim']):
	for i in arange(0,1):
	    app.globals.gaplistpre2.extend(app.globals.gaplistpre)
	    app.globals.stimidlistpre2.extend(app.globals.stimidlistpre)
	    app.globals.xandylistpre2.extend(app.globals.xandylistpre)
	
	app.globals.gaplist.extend(app.globals.gaplistpre2)
	app.globals.stimidlist.extend(app.globals.stimidlistpre2)
	app.globals.xandylist.extend(app.globals.xandylistpre2)

	app.globals.gaplist.extend(app.globals.gaplistpre2)
	app.globals.stimidlist.extend(app.globals.stimidlistpre2)
	app.globals.xandylist.extend(app.globals.xandylistpre2)
	print 'test1'
	print app.globals.gaplist
	print app.globals.stimidlist
	print app.globals.xandylist

	matchselect1 = [1] * len(app.globals.stimidlistpre2)
	matchselect2 = [0] * len(app.globals.stimidlistpre2)
	matchselect = list()
	matchselect.extend(matchselect1)
	matchselect.extend(matchselect2)
	print matchselect

	for j in arange(0,len(app.globals.stimidlist)):
	    #matchselect = randint(0,1)
	    #print matchselect
	    if matchselect[j] == 1:
	    	app.globals.mglist.append(app.globals.stimidlist[j])
	    else:
		if(params['Reference_Mode'] == 0):
			nmpicklist = eval(params['ComplexStimNums'])
		if(params['Reference_Mode'] == 1):
            		nmpicklist = eval(params['Non_Match_List'])
        	elif(params['Reference_Mode'] == 2 ) or (params['Reference_Mode'] == 3):
            		nmpicklist = self.B8ShapeSet
		
		nmpicklist[:] = (value for value in nmpicklist if value != app.globals.stimidlist[j])
		app.globals.mglist.append(choice(nmpicklist))

	#app.globals.mglist.extend(app.globals.stimidlist)
	
	mixerguy = []
	for j in arange(0,len(app.globals.stimidlist)):
	    mixerguy.append([])
	    mixerguy[j].append(app.globals.gaplist[j])
	    mixerguy[j].append(app.globals.stimidlist[j])
	    mixerguy[j].append(app.globals.mglist[j])
   	    mixerguy[j].append(app.globals.xandylist[j][0])
	    mixerguy[j].append(app.globals.xandylist[j][1])
	print mixerguy
	
	if(randomize_stims):	    #shuffle(app.globals.gaplist)
	    #shuffle(app.globals.stimidlist)
	    #shuffle(app.globals.xandylist)
	    #shuffle(mixerguy)
	    #shuffle(mixerguy)
	    #print mixerguy
	    shuffle(mixerguy)
	print mixerguy
	stupid = list()
	for j in arange(0,len(app.globals.stimidlist)):
	    app.globals.gaplist[j] = mixerguy[j][0]
	    app.globals.stimidlist[j] = mixerguy[j][1]
	    app.globals.mglist[j] = mixerguy[j][2]
	    stupid = [mixerguy[j][3],mixerguy[j][4]]
	    app.globals.xandylist2.append(stupid)
   	    #app.globals.xandylist[j][0] = mixerguy[j][3]
	    print 'test1b'
	    print stupid
	    print app.globals.xandylist2
	    #app.globals.xandylist[j][1] = mixerguy[j][4]
	app.globals.xandylist = app.globals.xandylist2
	
	print 'test2'
	print app.globals.stimidlist
	print app.globals.mglist
	print app.globals.xandylist
	app.globals.stimidlistOrig = []
	app.globals.stimidlistOrig.extend(app.globals.stimidlist)
	app.globals.mglistOrig = []
	app.globals.mglistOrig.extend(app.globals.mglist)
	app.globals.xandylistOrig = []
	app.globals.xandylistOrig.extend(app.globals.xandylist)
	app.globals.gaplistOrig = []
	app.globals.gaplistOrig.extend(app.globals.gaplist)

	#for j in arange(0,len(app.globals.stimidlist)):
	    #matchselect = randint(0,1)
	    #print matchselect
	    #if matchselect == 1:
	    	#app.globals.mglist.append(app.globals.stimidlist[j])
	    #else:
	    	#nmpicklist = eval(params['ComplexStimNums'])
		#nmpicklist[:] = (value for value in nmpicklist if value != app.globals.stimidlist[j])
		#app.globals.mglist.append(choice(nmpicklist))
		
	#Making ecc, size, diameter, radius, and myoffsets stuff
	self.ecc = list()
	self.size = list()
	self.diameter = list()
	self.radius = list()
	self.myForegroundXOffset = list()
	self.myForegroundYOffset = list()
	self.myMidgroundXOffset = list()
	self.myMidgroundYOffset = list()
	self.barXOffset = list()
	self.barYOffset = list()
	self.myFactory = list()

	self.diameterOrig = list()
	self.myForegroundXOffsetOrig = list()
	self.myForegroundYOffsetOrig = list()
	self.myMidgroundXOffsetOrig = list()
	self.myMidgroundYOffsetOrig = list()
	self.barXOffsetOrig = list()
	self.barYOffsetOrig = list()
	self.myFactoryOrig = list()

	for j in arange(0,len(app.globals.stimidlist)):
		
		self.ecc.append( ( (app.globals.xandylist[j][0]-fixX)**2 + (app.globals.xandylist[j][1]-fixY)**2)**0.5)
		if(params['RF Scale On Ecc']):
                	self.size.append( int((P['mon_ppd'] * params['RF Offset']) +  (params['RF Scaling'] * self.ecc[j])) )
        	else:
                	self.size.append( 2*params['RF Radius'] )
		self.diameter.append(self.size[j])
        	self.radius.append(self.size[j]/2.0)
        	self.myForegroundXOffset.append(params['foregroundXOffset'] * self.size[j]/2)
        	self.myForegroundYOffset.append(params['foregroundYOffset'] * self.size[j]/2)
        	self.myMidgroundXOffset.append(params['circleXOffset'] * self.size[j]/2)
        	self.myMidgroundYOffset.append(params['circleYOffset'] * self.size[j]/2) 
		self.barXOffset.append(params['barXOffset']  * self.size[j]/2)
        	self.barYOffset.append(params['barYOffset']  * self.size[j]/2)
		self.myFactory.append(b8StimFactory(self.diameter[j]*2,self.radius[j]))

	self.diameterOrig.extend(self.diameter)
	self.myForegroundXOffsetOrig.extend(self.myForegroundXOffset)
	self.myForegroundYOffsetOrig.extend(self.myForegroundYOffset)
	self.myMidgroundXOffsetOrig.extend(self.myMidgroundXOffset)
	self.myMidgroundYOffsetOrig.extend(self.myMidgroundYOffset)
	self.barXOffsetOrig.extend(self.barXOffset)
	self.barYOffsetOrig.extend(self.barYOffset)
	self.myFactoryOrig.extend(self.myFactory)

	#Making stims here using the lists
	#for k in arange(0, size(self.perceptShapes,0)):
         #       for j in arange(0,1):
	#	    #app.globals.gapLengths = eval(params['GapDistance'])
	#	    #print app.globals.gapLengths
	#	    #if(randomize_stims):
	#	    	#shuffle(app.globals.gapLengths)
	#	    #app.globals.gaplist = app.globals.gapLengths
	#	    if(params['ReverseOrder']):
	#		if(params['MGonly']):
	#			stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[k]],None, self.perceptShapes[k], app.globals.mglist[j], self.midgroundColor, self.foregroundColor, app.globals.xandylist[j], self.diameter[j], self.myForegroundXOffset[j], self.myForegroundYOffset[j], self.myMidgroundXOffset[j], self.myMidgroundYOffset[j], self.barXOffset[j], self.barYOffset[j], self.myFactory[j], self.rotVals,cacheSprite=1, useCache=1)
	#			self.myStims.extend(stimList)
	#			stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[k]],None, self.perceptShapes[k], app.globals.stimidlist[j], self.midgroundColor, self.foregroundColor, app.globals.xandylist[j], self.diameter[j], self.myForegroundXOffset[j], self.myForegroundYOffset[j], self.myMidgroundXOffset[j], self.myMidgroundYOffset[j], self.barXOffset[j], self.barYOffset[j], self.myFactory[j], self.rotVals,cacheSprite=1, useCache=1)
	#			self.myStims.extend(stimList)
	#		else:
	#	    		#for i in arange(0,len(app.globals.gapLengths)):
	#			stimList = self.getComplex(self.gapMode+self.perceptModeOffset[self.perceptShapes[k]],None, self.perceptShapes[k], app.globals.mglist[j], self.midgroundColor, self.foregroundColor, app.globals.xandylist[j], self.diameter[j], self.myForegroundXOffset[j], self.myForegroundYOffset[j], self.myMidgroundXOffset[j], self.myMidgroundYOffset[j], self.barXOffset[j], self.barYOffset[j], self.myFactory[j], self.myForegroundXOffset[j] + app.globals.gaplist[j], self.rotVals,cacheSprite=1, useCache=0)
	#			self.myStims.extend(stimList)
	#			stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[k]],None, self.perceptShapes[k], app.globals.stimidlist[j], self.midgroundColor, self.foregroundColor, app.globals.xandylist[j], self.diameter[j], self.myForegroundXOffset[j], self.myForegroundYOffset[j], self.myMidgroundXOffset[j], self.myMidgroundYOffset[j], self.barXOffset[j], self.barYOffset[j], self.myFactory[j], self.rotVals,cacheSprite=1, useCache=1)
	#			self.myStims.extend(stimList)
	#			#app.globals.gaplistpre.append(app.globals.gapLengths[i])
	#			#app.globals.stimidlistpre.append(complexStims[j])
	#	    else:
	#		if(params['MGonly']):
	#			stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[k]],None, self.perceptShapes[k], app.globals.stimidlist[j], self.midgroundColor, self.foregroundColor, app.globals.xandylist[j], self.diameter[j], self.myForegroundXOffset[j], self.myForegroundYOffset[j], self.myMidgroundXOffset[j], self.myMidgroundYOffset[j], self.barXOffset[j], self.barYOffset[j], self.myFactory[j], self.rotVals,cacheSprite=1, useCache=0)
	#			self.myStims.extend(stimList)
	#			stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[k]],None, self.perceptShapes[k], app.globals.mglist[j], self.midgroundColor, self.foregroundColor, app.globals.xandylist[j], self.diameter[j], self.myForegroundXOffset[j], self.myForegroundYOffset[j], self.myMidgroundXOffset[j], self.myMidgroundYOffset[j], self.barXOffset[j], self.barYOffset[j], self.myFactory[j], self.rotVals,cacheSprite=1, useCache=0)
	#			self.myStims.extend(stimList)
	#		else:
	#	    		#for i in arange(0,len(app.globals.gapLengths)):
	#			stimList = self.getMidground(self.midgroundOnlyMode+self.perceptModeOffset[self.perceptShapes[k]],None, self.perceptShapes[k], app.globals.stimidlist[j], self.midgroundColor, self.foregroundColor, app.globals.xandylist[j], self.diameter[j], self.myForegroundXOffset[j], self.myForegroundYOffset[j], self.myMidgroundXOffset[j], self.myMidgroundYOffset[j], self.barXOffset[j], self.barYOffset[j], self.myFactory[j], self.rotVals,cacheSprite=1, useCache=0)
	#			self.myStims.extend(stimList)
	#			stimList = self.getComplex(self.gapMode+self.perceptModeOffset[self.perceptShapes[k]],None, self.perceptShapes[k], app.globals.mglist[j], self.midgroundColor, self.foregroundColor, app.globals.xandylist[j], self.diameter[j], self.myForegroundXOffset[j], self.myForegroundYOffset[j], self.myMidgroundXOffset[j], self.myMidgroundYOffset[j], self.barXOffset[j], self.barYOffset[j], self.myFactory[j], self.myForegroundXOffset[j] + app.globals.gaplist[j], self.rotVals,cacheSprite=1, useCache=0)
	#			self.myStims.extend(stimList)
	#			#app.globals.gaplistpre.append(app.globals.gapLengths[i])
	#			#app.globals.stimidlistpre.append(complexStims[j])

        #numUniqueStims = len(self.myStims)
	numUniqueStims = 2*len(app.globals.stimidlist)
        stimNumbers = arange(0,numUniqueStims)
        #for i in arange(0,params['nRepsPerStim']):
            #if(randomize_stims):
                 #shuffle(stimNumbers)
        self.myStimList.extend(stimNumbers)
        self.numStim = self.numStim + (2*params['nRepsPerStim']*len(app.globals.stimidlist))
	#app.globals.gaplist.extend(app.globals.gaplistpre)
	#app.globals.stimidlist.extend(app.globals.stimidlistpre)
        
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
		("RF_Center", "[[200,200],[200,-200]]", is_any, "X and Y coordinate of the receptive field center in pixels"),
                ("RF_Center_X", "200",is_int,"X coordinate of the receptive field center in pixels"),
                ("RF_Center_Y", "200",is_int,"Y coordinate of the receptive field center in pixels"),
                ("RF Scale On Ecc", "1", is_boolean, "Whether or not to scale based on eccentricity"),
                ("RF Scaling", ".625", is_float, "If RF_Scale_On_Ecc is 1, Size of RF in degrees equals eccentricity * RF Scaling + RF Offset"),
                ("RF Offset", ".5", is_float, "If RF_Scale_On_Ecc is 1,Size of RF in degrees equals eccentricity * RF Scaling + RF Offset"),
                ("RF Radius", "100", is_int, "IF RF_Scale_On_Ecc is 0, this is the radius of the RF in pixels"),
                ("ShowRFSprite", "0", is_boolean, "If 1 display white circle around RF perimeter (use only during testing)"),
                ("Task Params", None, None),
                ("iti",	"1500", is_int, "Inter-trial interval"),
                ("IStime", "200", is_int, "Inter-stimulus interval"),
                ("AddExtraISI", "1", is_int, "Set to 1 to add another ISI after the last stimulus in a trial, 0 otherwise"),
                ("stimon", "300", is_int, "Stimulus presentation"),
                ("nstim", "2", is_int, "Number of stimuli. Dont change this."),
                ("Fixation Params", None, None, "Fixation Parameters"),
                ("fixcolor1", "(255,255,255)", is_color, 'Color of the fixation dot'),
                ("fixcolor2", "(128,128,128)",is_color),
		("maxrt",       "2000",          is_int),
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
                ("NumRotations", "1", is_int, "Number of rotations to use"),
                ("B8_Sampling", "100",is_int,"Number of points in each b-spline"),
                ("Stimulus Pres Params", None, None),
                ("nRepsPerStim", "2", is_int, "Number of repetitions of each stimulus to present"),
                ("nBlanks", "0", is_int, "The number of blank stimuli to present per block"),
                ("PerceptsPerBlock", "0", is_int, "The number of each percept to present per block"),
                ("bg_during", "(35, 19, 14)", is_color, "The background color during stimulus presentation"),
                ("bg_before", "(35, 19, 14)", is_color, "The background color before stimulus presentation"),
                ("randomize_stimuli", 1, is_boolean, "Whether or not to randomize stimuli within repetitions."),
                ("Percept Mode Params", None, None),
                ("Percept Shapes to Use", "[1]", is_any, "List of shapes (1:circle, 2:bar, 3:hourglass) to use for percept and midground objects"),
                ("circleXOffset", "-.25",is_float,"Number of rf rads that the circle is shifted to the right"),
                ("circleYOffset", "0.0",is_float,"Number of rf rads that the circle is shifted up"),
                ("circleScaling", ".50",is_float,"Radius of the circle circumscribing the midground object divided by the rf radius"),
                ("barXOffset", "-.25",is_float,"Number of rf rads that the bar and hourglass are shifted to the right"),
                ("barYOffset", "0.0",is_float,"Number of rf rads that the bar and hourglass are shifted up"),
                ("barScaling", ".50",is_float,"Radius of the circle circumscribing the bar and hourglass divided by the rf radius"),
                ("barAspect", "2.0",is_float,"Aspect Ratio (width/height) of bar and hourglass stimuli"),
                ("hour_vert_curv", "1.67",is_float,"Curvature of arc on top and bottom of hourglass stimulus"),
                ("hour_horiz_curv", ".375",is_float,"Curvature of arc on left and right of hourglass stimulus"),
                ("Foreground Mode Params", None, None),
                ("PresentForegroundStims", "1", is_boolean, "If 1 then present foreground stimuli"),
                ("UsePreSelectedForegrounds", "1", is_int, "1 (al 51 shapes), 2 (29 shape b8 screen), 3 (14 shape alternate aim1), 4 (union of 2 and 3) anything else use what is in ForegroundStimNums"),
                ("ForegroundStimNums","[]", is_any, "If UsePreSelectedForegrounds is not 1-3 then instead use only the foregrounds listed here(1-51)"),
                ("foregroundXOffset", ".25",is_float,"Number of rf rads that the foreground object is shifted to the right"),
                ("foregroundYOffset", "0",is_float,"Number of rf rads that the foreground object is shifted up"),
                ("foregroundScaling", ".5",is_float,"Radius of the circle circumscribing the foreground object divided by the rf radius"),
                ("Gap Mode Params", None, None),
                ("Present_Gap_Mode", 1, is_boolean, "Turn on the gap test."),
                #("UseAllComplexStims", "0", is_boolean, "If 1 then use all 51 complex shapes"),
                ("ComplexStimNums","[4,8,10]", is_any, "If UseAllComplexStims is 0 then instead use only the complex shapes listed here(1-51)"),
		("GapDistance", "[0,20,60]", is_any, "gaps"),
		("Reference_Mode", 0, is_int, "1 Nonmatch stims selected randomly from list below. 2 Nonmatch stim selected from 51 shapes 3 Both match and nonmatch stim selected from 51 shapes"),
		("RandomStimNum", 4, is_int, "For Reference mode 3"),
		("Non_Match_List","[4,8,10]", is_any, "Non-match stims for Reference Stims"),
		("ReverseOrder", 0, is_boolean, "Show complex stim first."),
		("MGonly", 0, is_boolean, "Second stims are midgrounds instead of complex stims."),
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
        #app.encode_plex(int(round(self.radius))+app.globals.yOffset)
        #app.encode(int(round(self.radius))+app.globals.yOffset)
            
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
    def getPercept(self,modeToEncode, submode, mg_shape, fg_shape, mg_color, fg_color, myXmyY, diameter, myMidgroundXOffset, myMidgroundYOffset, barXOffset, barYOffset, rots,cacheSprite=1,newXOffset=None,newYOffset=None,newScale=None):
        myStims = list()
        perceptSprite = None
        if(mg_shape == 1):
            if(newXOffset is not None):
                xOffset = newXOffset
            else:
                xOffset = myMidgroundXOffset
            if(newYOffset is not None):
                yOffset = newYOffset
            else:
                yOffset = myMidgroundYOffset
            if(newScale is not None):
                scaling = newScale
            else:
                scaling = self.myMidgroundScaling
            circleSprite = Sprite(diameter, diameter, myXmyY[0], myXmyY[1],fb=self.myFB, depth=self.perceptDepth, on=0,centerorigin=1)
            circleSprite.fill(self.myBG+(0,))
            circleSprite.circlefill(mg_color,r=(diameter/2)*scaling,x=xOffset,y=yOffset)
            perceptSprite = circleSprite
            if(cacheSprite):
                self.myPercepts[mg_shape] = circleSprite
        elif(mg_shape == 2):
            if(newXOffset is not None):
                xOffset = newXOffset
            else:
                xOffset = barXOffset  
            if(newYOffset is not None):
                yOffset = newYOffset
            else:
                yOffset = barYOffset
            if(newScale is not None):
                scaling = newScale
            else:
                scaling = self.barScaling
            barM =  Sprite(diameter, diameter, myXmyY[0], myXmyY[1],fb=self.myFB, depth=self.perceptDepth, on=0,centerorigin=1)
            barM.fill(self.myBG+(0,))
            xloc = xOffset  #this may need to just be xOffset
            yloc = yOffset #this may need to just be yOffset
            xDist = scaling*(diameter/2)*2
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
                xOffset = barXOffset
            if(newYOffset is not None):
                yOffset = newYOffset
            else:
                yOffset = barYOffset
            if(newScale is not None):
                scaling = newScale
            else:
                scaling = self.barScaling
            hour =  Sprite(diameter, diameter, myXmyY[0], myXmyY[1],fb=self.myFB, depth=self.perceptDepth, on=0,centerorigin=1)
            hour.fill(self.myBG+(0,))
            xloc = xOffset  #this may need to just be xOffset
            yloc = yOffset #this may need to just be yOffset
            xDist = scaling*(diameter/2)*2
            yDist = xDist/self.barAspect
            hour.rect(xloc,yloc, xDist, yDist, mg_color)
            vert_rad = (diameter/2) * self.hour_vert_curv
            horiz_rad = (diameter/2) * self.hour_horiz_curv
            b = (vert_rad)**2 - (xDist/2)**2
            bprime = (horiz_rad)**2 - (yDist/2)**2
            yoffset =  yDist/2.0 - vert_rad + sqrt(b)
            xoffset = xDist/2.0 - horiz_rad + sqrt(bprime)
            hour.circlefill(self.myBG,vert_rad, x=xloc,y=yoffset+vert_rad, width=0)
            hour.circlefill(self.myBG,vert_rad, x=xloc,y=-yoffset-vert_rad, width=0)
            hour.circlefill(self.myBG,horiz_rad, x=xloc-xoffset-horiz_rad,y=yloc, width=0)
            hour.circlefill(self.myBG,horiz_rad, x=xloc+xoffset+horiz_rad,y=yloc, width=0)
            perceptSprite = hour
            if(cacheSprite):
                self.myPercepts[mg_shape] = hour 
        else:
            return myStims,perceptSprite
        #for i in arange(0,(params['CirclePerceptsPerBlock'])):
        #print rots
        for k in arange(0,size(rots,0)):
            myRotation = (360 - rots[k]) 
            sp =  perceptSprite.clone()
            if(k != 0):
                sp.rotate(myRotation,0,1)
            stim = stimulus(modeToEncode,mg_shape+1,rots[k])
            stim.addSprite(sp,mg_color,0)
            myStims.append(stim)
        return myStims,perceptSprite

    def getComplex(self,modeToEncode, submode, mg_shape, fg_shape, mg_color, fg_color, myXmyY, diameter, myForegroundXOffset, myForegroundYOffset, myMidgroundXOffset, myMidgroundYOffset, barXOffset, barYOffset, myFactory, gap, rots,cacheSprite=1, useCache=1):
        myStims = list()
        if(self.myForeground[fg_shape] is not None and useCache):
            s = self.myForeground[fg_shape]
        else:
            s = myFactory.getB8StimAsOccluder(fg_shape, self.sampling,self.myFB,self.myBG,0,myXmyY[0],myXmyY[1],self.myBG+(0,),myForegroundXOffset, myForegroundYOffset, self.myForegroundScaling,self.betweenForeAndMid)
            if(cacheSprite):
                self.myForeground[fg_shape] = s
        if(self.myPercepts[mg_shape] is not None and useCache):
            per = self.myPercepts[mg_shape]
        else:
            #print 'getting new percept for reverse colors\n'
            tempObj,per = self.getPercept(modeToEncode,submode, mg_shape, fg_shape, mg_color, fg_color, myXmyY, diameter, myMidgroundXOffset, myMidgroundYOffset, barXOffset, barYOffset, [0], 0)
        s2 = myFactory.getB8StimAsOccluder(fg_shape, self.sampling,self.myFB,fg_color,0,myXmyY[0],myXmyY[1],self.myBG+(0,),gap, myForegroundYOffset, self.myForegroundScaling,self.foregroundDepth)
        for k in arange(0,size(rots,0)):
            myRotation = (360 - rots[k]) 
            sp = s.clone()
            sp3 = s2.clone()
            if(k != 0):
                sp.rotate(myRotation,0,1)
                sp3.rotate(myRotation,0,1)
            sp2 = per.clone()
            if(k != 0):
                sp2.rotate(myRotation,0,1)
            stim = stimulus(modeToEncode,fg_shape, rots[k])
            stim.addSprite(sp,self.myBG,0)
            stim.addSprite(sp2,mg_color,0)
	    stim.addSprite(sp3, fg_color,0)
            myStims.append(stim)
            self.myComplexStimuli[fg_shape] = stim
        return myStims

    def getMidground(self,modeToEncode, submode, mg_shape, fg_shape, mg_color, fg_color, myXmyY, diameter, myForegroundXOffset, myForegroundYOffset, myMidgroundXOffset, myMidgroundYOffset, barXOffset, barYOffset, myFactory, rots,cacheSprite=1, useCache=1):
        #Mode 3 - Midground Mode AKA Background Occluder Mode

        myStims = list()

        if(self.myForegroundinBG[fg_shape] is None or not useCache):
            #should this be foreground depth?
            s = myFactory.getB8StimAsOccluder(fg_shape, self.sampling,self.myFB,self.myBG,0,myXmyY[0],myXmyY[1],self.myBG+(0,),myForegroundXOffset, myForegroundYOffset, self.myForegroundScaling,self.midgroundDepth)
            self.myForegroundinBG[fg_shape] = s
        else:
            if(cacheSprite):
                s = self.myForegroundinBG[fg_shape]

        if(self.myPercepts[mg_shape] is not None and useCache):
            per = self.myPercepts[mg_shape]
        else:
            tempObj,per = self.getPercept(modeToEncode,submode, mg_shape, fg_shape, mg_color, fg_color, myXmyY, diameter, myMidgroundXOffset, myMidgroundYOffset, barXOffset, barYOffset, [0], 0)

        for k in arange(0,size(rots,0)):
            myRotation = (360 - rots[k]) 
            sp = s.clone()
            if(k != 0):
                sp.rotate(myRotation,0,1)

            sp2 = per.clone()
            if(k != 0):
                sp2.rotate(myRotation,0,1)
            stim = stimulus(modeToEncode,fg_shape, rots[k])
            stim.addSprite(sp,mg_color,0)
            stim.addSprite(sp2,mg_color,0)
            myStims.append(stim)
            self.myMidgroundStimuli[fg_shape] = stim

        return myStims
