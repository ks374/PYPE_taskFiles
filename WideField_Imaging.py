# -*- coding: utf-8 -*-
"""
Created on Thu Apr 17, 2025

WideField_Imaging.py is a task for Widefield imaging for awake animal.
- Orientation selectivity & Color selectivity
- Red-Green or Black-White square wave
- Red and Green colors are equiluminant, and the luminance level is the same as the mean of Black/White luminance

Stimulus parameters
- Number of directions
- Color type (WK (0) or RG (1) or Both (2))
- Stimulus position (with full-screen option)
- Spatial frequency
- Temporal frequency
- Fixation hold time
- Stimulus delay time (from fixation hold to stimulus start)
- Stimulus duration

@author: Taekjun Kim
"""


#%%
import os, sys, types   ## os is needed to specify file location
from pype import *
#from Numeric import *   ## Numeric is needed for array computation. Possible to upgrade?
import numpy as np
import math
from random import *
from shapes import *   ## because of create bar for blank stimuli
import pandas as pd; 
import datetime; 
import pygame; 
#from tqdm import tqdm; 


#%%

def RunSet(app):
    app.taskObject.runSet(app)

def cleanup(app):
    app.taskObject.cleanup(app)

def main(app):
    print(sys.path)
    app.taskObject = WideField_Imaging(app)
    app.globals = Holder()
    app.idlefb()
    app.startfn = RunSet

# This is also something that all tasks have, and it's a python thing.
# Don't touch it.
if not __name__ == '__main__':
        loadwarn(__name__)
else:
        dump(sys.argv[1])


class WideField_Imaging:

    def __init__(self, app):
        self.createParamTable(app)
        self.app = app
        self.stim_table = [];  
        self.mySprites = list()
        self.myid = list()
        self.id_shuffled = list()
        self.shift_per_frame = 0; 
        self.numStim = 0
        self.taskparam = 0    # will be checked in saveEvents. NeuroPixel-related

    def createStimuli(self,app):

        ## global parameters
        gParam = app.getcommon()

        ## parameters defined in this task
        self.params = self.myTaskParams.check()
        params = self.params

        randomize_stims = params['randomize_stimuli']
        myBG = params['bg_during']
        BGlist = list(myBG)

        myFB = app.fb  ## framebuffer
        ### Determines the duration of movie     
        self.mon_Hz = 60;    
        self.Numframes = int(self.mon_Hz*params['stimon']/1000);   

        ### Stimulus parameters
        PixPerDeg = int(gParam['mon_ppd']); # monitor pixel per degree
        myX = params['Stim_centerX']; 
        myY = params['Stim_centerY']; 
        stimsize_pix = params['Stim_Size_pix']; 

        color_type = params['ColorType']; # 0: WK, 1: RG, 2: Both
        if color_type==2:
            color_type_list = np.array([0,1]); 
        else:
            color_type_list = np.array([color_type]);             

        N_direction = params['N_direction']; 
        SF = params['SF']; 
        TF = params['TF']; 

        ### Stimulus generation

        # Make a large vertical square-wave grating
        square_width = 1500; 
        square_height = 1000; 
        xwidth = np.linspace(-square_width/2,square_width/2,square_width); 
        ywidth = np.linspace(-square_height/2,square_height/2,square_height);                    					
        [xx, yy] = np.meshgrid(xwidth,ywidth); 

        PixPerCyc = int(PixPerDeg/SF); 
        RadPerPix = (1.0/PixPerCyc) * 2.0*np.pi; 

        self.PixPerCyc = PixPerCyc; 
        self.shift_per_frame = PixPerCyc * TF / self.mon_Hz; 

        gratingMtx = np.cos(RadPerPix*xx); 
        mask_pos = gratingMtx > 0
        mask_neg = gratingMtx < 0
        #row_c1, col_c1 = np.where(gratingMtx>0); 
        #row_c2, col_c2 = np.where(gratingMtx<0); 

        WK_mtx = 255*np.ones((square_height, square_width, 3), dtype=np.uint8);  # RGBA
        WK_mtx[mask_neg] = 0; 
        #WK_mtx[row_c1, col_c1, :3] = 255; 
        #WK_mtx[row_c2, col_c2, :3] = 0; 

        RG_mtx = np.zeros((square_height, square_width, 3), dtype=np.uint8); 
        RG_mtx[mask_pos, 0] = 255  # Red
        RG_mtx[mask_neg, 1] = 255  # Green

        """
        # give Red color
        RG_mtx[row_c1, col_c1, 0] = 255; 
        RG_mtx[row_c1, col_c1, 1] = 0; 
        RG_mtx[row_c1, col_c1, 2] = 0;                 
        # give Green color        
        RG_mtx[row_c2, col_c2, 0] = 0; 
        RG_mtx[row_c2, col_c2, 1] = 255; 
        RG_mtx[row_c2, col_c2, 2] = 0;                 
        RG_mtx = RG_mtx.astype(np.uint8); 
        """
        
        ### WK_mtx, RG_mtx to WK_s, RG_s
        uniq_frames = int(self.mon_Hz/TF); 

        WK_s = []; 
        RG_s = [];  
        base_sprite = Sprite(
                width=stimsize_pix, height=stimsize_pix, 
                x = myX+eval(params['FixationShift'])[0], 
                y = myY+eval(params['FixationShift'])[1], 
                fb=myFB, depth=1, on=0,centerorigin=1
        ); 
        for k in np.arange(0,uniq_frames):
            x_offset = int(self.shift_per_frame*k); 
            slice_x = slice(x_offset, stimsize_pix + x_offset)

            if color_type!=1:
                frame_wk = WK_mtx[:stimsize_pix, slice_x].transpose((1, 0, 2)); 
                wk_sprite = base_sprite.clone()
                wk_sprite.array[:] = frame_wk.tolist()
                wk_sprite.alpha_gradient(stimsize_pix / 2 - 3, stimsize_pix / 2, x=0, y=0)
                WK_s.append(wk_sprite)

            if color_type!=0:
                frame_rg = RG_mtx[:stimsize_pix, slice_x].transpose((1, 0, 2));             
                rg_sprite = base_sprite.clone()
                rg_sprite.array[:] = frame_rg.tolist()
                rg_sprite.alpha_gradient(stimsize_pix / 2 - 3, stimsize_pix / 2, x=0, y=0)
                RG_s.append(rg_sprite)

        self.mySprites.extend([WK_s, RG_s]);  
        print('WK & RG sprites were created'); 

        ### Make Stim Table
        stim_table = pd.DataFrame(); 
        stim_table['id'] = np.nan; 
        stim_table['dir'] = np.nan; 
        stim_table['color_type'] = pd.Series(dtype='object'); 
        stim_table['sf'] = np.nan; 
        stim_table['tf'] = np.nan; 
        stim_table['stim_size_pix'] = np.nan;         
        idNow = 0; 
        for c in color_type_list:
            for d in np.arange(N_direction):
                dir = (360/N_direction)*d; 
                stim_table.at[idNow, 'id'] = idNow; 
                stim_table.at[idNow, 'dir'] = dir; 
                if c==0:
                    stim_table.at[idNow, 'color_type'] = 'WK';             
                elif c==1:
                    stim_table.at[idNow, 'color_type'] = 'RG';             
                stim_table.at[idNow, 'sf'] = SF; 
                stim_table.at[idNow, 'tf'] = TF; 
                stim_table.at[idNow, 'stim_size_pix'] = stimsize_pix;         

                self.myid.append(idNow); 
                idNow += 1;                                                             

        BGlist = None        
        for j in np.arange(0,params['nBlanks']):
            stim_table.at[idNow, 'id'] = idNow; 
            stim_table.at[idNow, 'dir'] = np.nan; 
            stim_table.at[idNow, 'color_type'] = np.nan;         
            stim_table.at[idNow, 'sf'] = np.nan; 
            stim_table.at[idNow, 'tf'] = np.nan; 
            stim_table.at[idNow, 'stim_size_pix'] = np.nan; 

            s = [None]*uniq_frames          
            for k in np.arange(0,uniq_frames):
                s[k] = createBar(30, 30, myFB,myBG, 0, myX, myY, myBG)

            self.mySprites.append(s);              
            self.myid.append(idNow)
            idNow += 1; 

        self.stim_table = stim_table;          
        print('idNum = 0 to '+ str(idNow-1));   
        print('Stim_table was created'); 

        numUniqueStims = np.shape(stim_table)[0]; 
        stimNumbers = np.arange(0,numUniqueStims); 
        for i in np.arange(0,params['nRepsPerStim']):
            if (randomize_stims):
                shuffle(stimNumbers)
            self.id_shuffled.extend(stimNumbers)
            self.numStim = self.numStim + len(stimNumbers); 

        ## these are the stim params that need to be encoded before start of task
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
            ("Stim Presentation Params", None, None), 
            ("Stim_centerX", "0", is_int,"X coordinate of the stimulus center in pixels"),
            ("Stim_centerY", "0", is_int,"Y coordinate of the stimulus field center in pixels"),
            ("Stim_Size_pix", 1000, is_int, "Stimulus size in pix (max = 1000)"),                        
            ("ColorType", 0, is_int, "Color type of the square wave (0: WK, 1: RG, 2: Both)"),                                    
            ("N_direction", 0, is_int, "Number of tested directions (step size = 360/N_direction)"),                                                
            ("SF", 0, is_float, "Spatial frequency (cycles/deg)"),                                                            
            ("TF", 0, is_float, "Temporal frequency (cycles/sec)"),            
            ("randomize_stimuli", 1, is_boolean, "Whether or not to randomize stimuli within repetitions."),                                                                   
            ("nRepsPerStim", "10", is_int, "Number of repetitions of each stimulus to present"),
            ("Task Params", None, None),            
            ("bg_before", "(50, 50, 50)", is_color, "The background color before stimulus presentation"),            
            ("bg_during", "(50, 50, 50)", is_color, "The background color during stimulus presentation"),
            ("iti", "2000", is_int, "Inter-trial interval"),
            ("stimon", "2000", is_int, "Inter-trial interval"),            
            ("IStime", "1000", is_int, "Inter-stimulus interval"),
            ("nstim", "1", is_int, "Number of stimuli per trial"),
            ("nBlanks", "1", is_int, "The number of blank stimuli to present per block"),          
            ("FixationShift", "[0,0]", is_any, "Entire screen coordinate shift"),                       
            ("Reward Params", None, None),
            ("numdrops", "0", is_int, "Number of juice drops"),
            ("rmult", "1.0", is_float),
            ("Fixation Params", None, None, "Fixation Parameters"),
            ("fixcolor1", "(255,255,255)",is_color, 'Color of the fixation dot'),
            ("fixcolor2", "(128,128,128)",is_color),
            ("fixwait", "100", is_int),
            ("Stim_delay", "100", is_int),            
            ("min_err", "0", is_int),
            ("max_err", "100", is_int),
            ("Record File Params", None, None, "Params for setting name of record file"),
            ("Use Special Name", "0", is_boolean, "If 1 then the record file name will be AnimalPrefixDate_TaskName_CellGroup_Iteration.rec"),
            ("RFDirectory", "/home/shapelab/recordFiles/", is_any, "Directory to use for Record Files"),               
            ("AnimalPrefix", "m", is_any, "Animal Prefix to use"),
            #("Date","080325", is_any, "Date to use "),
            ("TaskName","WideField_Imaging", is_any, "TaskName"),
            #("CellGroup","01", is_int, "# of cell group encountered today"),
            #("Iteration","01", is_int, "# of times this task has been run on this cell group"),
            ("Misc Params", None, None, "Miscelaneous Parameters"),
            ("Recent Buffer Size", "50", is_int, "The number of trials to use5 to calculate recent performance"),
            ("pause_color", "(40,40,40)", is_color, "The screen will turn this color when the task is paused")
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
        sIDIndex = self.id_shuffled[sIndex]; 
        myid = self.myid[sIDIndex]
    
        app.encode_plex('stimid')
        app.encode_plex(int(myid+app.globals.plexStimIDOffset))

        app.encode('stimid')
        app.encode(int(myid+app.globals.plexStimIDOffset))


    def encodeTaskParameters(self,app):
        #encode task parameters
        params = self.myTaskParams.check()
        app.encode_plex('rfx')
        app.encode_plex(params['Stim_centerX']+ app.globals.yOffset)
        app.encode_plex('rfy')
        app.encode_plex(params['Stim_centerY'] + app.globals.yOffset)
        app.encode_plex('iti')
        app.encode_plex(int(params['iti']))
        app.encode_plex('stim_time')
        app.encode_plex(int(params['stimon']))
        app.encode_plex('isi')
        app.encode_plex(int(params['IStime']))
        app.encode_plex('numstim')
        app.encode_plex(int(params['nstim']))

        app.encode('rfx')
        app.encode(params['Stim_centerX']+ app.globals.yOffset)
        app.encode('rfy')
        app.encode(params['Stim_centerY'] + app.globals.yOffset)
        app.encode('iti')
        app.encode(int(params['iti']))
        app.encode('stim_time')
        app.encode(int(params['stimon']))
        app.encode('isi')
        app.encode(int(params['IStime']))
        app.encode('numstim')
        app.encode(int(params['nstim']))

     
    def encodeITI(self,app):
        pass


    def runSet(self,app):
        """
        This is what is run when you hit the 'start' button (set as such in
        the 'main' function, defined at the end of this file).
        """

        # tally collects the results of the last N trials and displays a
        # running tally at the bottom of the main pype control window
        pygame.event.pump()
        app.tally(clear=1)
    
        # This erases any information printed to the console
        #app.console.clear()
    
        # Update the task's representation of all the parameters set in the
        # task parameter table, rig_params and monk_params - always called P
        #app.params = ParamTable(None, (), None)        
        P = self.myTaskParams.check(mergewith=app.getcommon())
        params = self.myTaskParams.check()

        # Save this version (in case you've made changes since the last time
        # the .par file was updated).

        #P.save()
        #params.save()

        self.createStimuli(app)
        print('Done creating Stimuli')
        
        if (self.warnNumStim()):
            if ask("pype", "%d stimuli, proceed?" % self.getNumStim(), ("yes", "no")) == 0:
               pass
            else:
               return

        #Set the record filename if the task wants to:
        rFileName = self.getRecordFileName()
        if (rFileName is not None):
            if (os.path.exists(rFileName)):
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
        app.globals.ntrials = 0
        app.globals.seqcorrect = 0
        app.globals.uicount = 0
        app.globals.stimCorrect = 0
        app.globals.yOffset = 600
        #app.globals.yOffset = pype_plex_code_dict('plexYOffset')
        app.globals.plexStimIDOffset = pype_plex_code_dict('plexStimIDOffset')
        app.globals.plexRotOffset = pype_plex_code_dict('plexRotOffset')

        self.encodeTaskParameters(app)

        
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
           while app.running and (app.globals.stimCorrect < self.getNumStim()):
                #This task implements pause (f5) at the trial level
                was_paused = 0
                while (app.paused):
                      if (was_paused == 0):
                         app.encode_plex('pause')
                         app.encode('pause')
                         app.globals.dlist.bg = params['pause_color']
                         # Update the dlist and flip the framebuffer
                         app.globals.dlist.update()
                         app.fb.flip()
                         was_paused = 1
                      app.idlefn()
                if (was_paused): #reset background color
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
                   if (app.globals.ntrials < params['Recent Buffer Size']) :
                      recent=100*app.globals.ncorrect/app.globals.ntrials
                   else:
                      lastX = pctbuffer[len(pctbuffer) - params['Recent Buffer Size']::]
                      recent=100*lastX.count(CORRECT_RESPONSE)/len(lastX)
                   stimPerTrial =  float(app.globals.stimCorrect)/ float(app.globals.ntrials)
                else:
                   stimPerTrial = 0.0

                # This call prints the overall and recent perf % to console
                con(app, " %s:%d %d/%d %.0f%% (recent %.0f%%)\n %0.2f stims per trial" % \
                    (now(), app.nreps(),app.globals.ncorrect, app.globals.ntrials, 100.0 * app.globals.ncorrect / app.globals.ntrials, recent, stimPerTrial), 'black')
                                                                                     
                #update the behavioral history and tally
                if (result is None):
                   app.tally(type=USER_ABORT)
                   app.history(USER_ABORT)
                elif (iscorrect(result)):
                   app.tally(type=CORRECT_RESPONSE)
                   app.history(CORRECT_RESPONSE)
                elif (result == BREAK_FIX):
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
        if (rFileName is not None):
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
        pygame.event.pump()
        P = self.myTaskParams.check(mergewith=app.getcommon())
        params = self.myTaskParams.check()

        # Note the time that the trial started, again explicitly handled
        # in PypeFile class.
        # Do we need this?
        # Note that the comment above is not accurate.  the time is actually the time that RunTrial is called, the actual trial has not yet started, although the ITI has
        app.record_note('trialtime', (app.globals.ntrials, Timestamp()))

        # This call starts the data record for this trial. The datafile will
        # have a 'start' event encoded with timestamp = 0. Also plexon will 
        # have an event encoded
        app.record_start()
    
        # This function will actually do the task control and stimulus display
        # and return its results back here for housekeeping.
        (result, rt,t) = self._RunTrial(app,t)

        # Stop recording for this trial, reset eye trace and signal trial stop
        # to Plexon.  Encode 'stop' in the datafile, which is the very last
        # thing to get
        app.record_stop()

        self.saveEvents(app);   ### Edited for Neuropixel. Test 2/9/2022, Taekjun
    
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
        fx = fx + eval(params['FixationShift'])[0]; 
        fy = fy + eval(params['FixationShift'])[1];        

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
        #min_e, max_e = params['min_err'], params['max_err']
        #r = ((fx**2)+(fy**2))**0.5
        #z = min_e + (max_e - min_e) * r / ((app.fb.w+app.fb.h)/4.0)
        z = 0
        # Set a parameter value that's the actual window size to use
        # this trial, so it's saved in data file.
        P['_winsize'] = int(round(P['win_size'] + z))
    
        # Create an instance of the FixWin class (defined in pype.py) that
        # will actually keep track of the eye position for you
        fixwin = FixWin(fx, fy, P['_winsize'], app)
        fixwin.draw(color='grey') #draws the fixwin radius on user display

        ##### Now create the visual stimuli

        ####This is for multiple stimulus presentation; number of stimuli to
        ####be shown in this run is min of P['nstim'] and the number of
        ####stimuli left
        stm_start = app.globals.stimCorrect
        con(app,"%d stimuli presented, %d stimuli remaining" % (stm_start,self.getNumStim()-stm_start),"Black")
        sshow = np.min([params['nstim'], self.getNumStim()-stm_start])

        stim_arr = [] #empty sprite list

        #import pdb; pdb.set_trace(); 
        N_frames = int(self.mon_Hz*params['stimon']/1000);         
        xy_offset = np.empty((sshow, N_frames, 2));         
        for i in np.arange(0,sshow):
            idNow = self.myid[self.id_shuffled[stm_start+i]]; 
            rowNum = np.where(self.stim_table['id'] == idNow)[0][0]; 

            dir = self.stim_table.at[rowNum,'dir']; 
            color_type = self.stim_table.at[rowNum,'color_type']; 
            sf = self.stim_table.at[rowNum,'sf']; 
            tf = self.stim_table.at[rowNum,'tf']; 
            uniq_frames = len(self.mySprites[2]);   # there always exist blank sprites 

            if np.isnan(sf)==0:
                spr = []; 
                for j in np.arange(0,uniq_frames):
                    if color_type=='WK':
                        spr.append(self.mySprites[0][j].clone()); 
                    elif color_type=='RG':
                        spr.append(self.mySprites[1][j].clone()); 
                    spr[j].rotate(-dir); 
            else:                
                spr = self.mySprites[2]; 
            stim_arr.append(spr); 

            for j in np.arange(0,uniq_frames):
                stim_arr[i][j].off()
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
            p_info(app, "waiting fix acquisition")
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
                        p_info(app, "no acquisition")
                        con(app, "no acquisition", 'blue')
                        #app.encode_plex(UNINITIATED_TRIAL)
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
                        p_info(app, "passthrough")
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
            #app.encode(FIX_ACQUIRED) # Standard event encoding

            app.encode_plex(FIX_ACQUIRED)
            app.encode(FIX_ACQUIRED)
            fixwin.draw(color='blue') # Blue is our "active" fixwin color

            ####This is for multiple stimulus presentation; number of stimuli to
            ####be shown in this run is min of P['nstim'] and the number of
            ####stimuli left
            scount = 0
            while scount < sshow:
                P = self.myTaskParams.check(mergewith=app.getcommon())
                self.encodeISI(app,scount+stm_start)
                while t.ms() < params['IStime']:
                    if fixwin.broke() and not TESTING:
                        #app.encode(FIX_LOST) #standard event code
                        app.encode_plex(FIX_LOST)
                        app.encode(FIX_LOST)
                        p_info(app, "early break")
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

                # now display stimulus 
                # now turn it on put it on the dlist; update and flip buffer
                app.globals.dlist.add(stim_arr[scount][0:uniq_frames]); 
                stim_arr[scount][0].on() #turn on first frame
                foff = 0                  #this is the frame number currently on
                self.toggle_photo_diode(app) #note: toggle_photo_diode updates the dlist
                app.encode_plex(SAMPLE_ON)
                app.encode(SAMPLE_ON)
                app.fb.flip()                                 
                #app.udpy.display(app.globals.dlist)

                # wait for stimulus time
                t.reset()
                fon = 0
                while fon < self.mon_Hz*params['stimon']/1000-1:
                    if fixwin.broke() and not TESTING:
                        app.encode(FIX_LOST) #standard event code
                        app.encode_plex(FIX_LOST)
                        app.encode(FIX_LOST)

                        p_info(app, "early break")
                        con(app, "early break at %d, %d ms into presentation of stim %d, fixwin time of %d" % (t2.ms(),t.ms(), scount,fixwin.break_time()), 'red')
                        #app.encode('exact_fix_lost=%d' % fixwin.break_time())
                        result = BREAK_FIX
                        app.warn_trial_incorrect(flash=None)
                        #turn off stimuli
                        stim_arr[scount][foff%uniq_frames].off()
                        app.fb.flip()
                        # Skip to end of trial
                        raise MonkError
                    foff = fon; 
                    fon = fon + 1; 
                    stim_arr[scount][foff%uniq_frames].off();                     
                    stim_arr[scount][fon%uniq_frames].on(); 
                    app.globals.dlist.update()                    
                    app.fb.flip()                        
                    
                # Again, a call to idlefn lets the computer catch up
                # and monitor for key presses.
                app.idlefn()
                # now turn off stimulus
                stim_arr[scount][foff%uniq_frames].off()
                app.globals.dlist.delete(stim_arr[scount]); 
                self.toggle_photo_diode(app) #note: toggle_photo_diode updates the dlist
                app.fb.flip()
                print(t.ms(),fon)                 
                t.reset() # Reset the timer to start ISI timer
                #app.encode(SAMPLE_OFF)
                app.encode_plex(SAMPLE_OFF)
                app.encode(SAMPLE_OFF)
                app.globals.stimCorrect = app.globals.stimCorrect + 1
                scount = scount+1

            ################################
            # If you are here then the trial is correct
            #print "Before raising NoProblem at %d abs time = %d" % (t.ms(), t2.ms())
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

            # Re-set the background for the intertrial interval
            app.globals.dlist.bg = params['bg_before']
            app.globals.dlist.update()
            self.turn_off_photo_diode(app)
            app.fb.flip()

            app.encode_plex(result)
            app.encode(result)
            t.reset()
            app.encode_plex(START_ITI)
            app.encode(START_ITI)

            app.globals.ntrials = app.globals.ntrials + 1
            app.globals.seqcorrect = 0
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

            return (result, rt, t)


    def toggle_photo_diode(self,app):
        app.globals.dlist.update()
        app.fb.sync_toggle()

    def turn_off_photo_diode(self,app):
        app.fb.sync(0)

    def warnNumStim(self):
        return 0

    #def getSprite(self, index):
    #    return self.mySprites[self.mySpriteList[index]]

    def getNumStim(self):
        return self.numStim

    def getRecordFileName(self): #gets the record file for this task 
        params = self.myTaskParams.check()
        if(params['Use Special Name']):
            filename = "%s%s%s_%s_%02d_%02d.rec" % (params['RFDirectory'],params['AnimalPrefix'],params['Date'],params['TaskName'],params['CellGroup'],params['Iteration'])
        else:
            filename = None
        filename = None;  ## added to avoid conflict with Neuropixel. 02/09/2022. Taekjun    
        return filename

    def saveEvents(self,app):# Tomo Neuropixles Mar 8 2019 # edited for Neuropixel 08/08/2020 Taekjun

        if self.taskparam==0:
            from datetime import datetime; 
            params = self.myTaskParams.check()        
            tNow = datetime.now().strftime("_%y%m%d_%H%M%S"); 
            event_filename = "%s%s%s_%s.dat" % (params['RFDirectory'],params['AnimalPrefix'],tNow,params['TaskName'])
            self.event_filename = event_filename; 

            fid = open(event_filename,'w'); 
            ## make header: TaskParameters, and first start ITI
            Header = ['stim_x',int(params['Stim_centerX']),'stim_y',int(params['Stim_centerY']),
                      'num_cond',np.shape(self.stim_table)[0],'stim_size_pix',int(params['Stim_Size_pix']),
                      'stimon',int(params['stimon']),'isi',int(params['IStime']),
                      'start_iti']; 
            fid.write(str(Header)+"\n"); 
            fid.close();

            df = self.stim_table; 
            df_filename = "%s%s%s_%s_stimTable.csv" % (params['RFDirectory'],params['AnimalPrefix'],
                                                tNow,params['TaskName'])
            #save array to csv file
            df.to_csv(df_filename)        
            self.taskparam = 1; 

        data=app.record_buffer #Tomo Neuropixels
        EventNow = [];
        
        # need to remove START, STOP, EYE_STOP, EYE_START which are not sent to plexon
        for item in data:
            if item[1] not in ['start','stop','eye_stop','eye_start']:
                EventNow.append(item[1]);

        #print app.record_buffer
        app.record_buffer=[]
        event_filename = self.event_filename; 

        fid=open(event_filename,'a'); 
        fid.write(str(EventNow)+"\n"); 
        fid.close()	


