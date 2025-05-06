#!/usr/bin/python
# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-

"""
This task is the extension of multi_matching_codes - included are
some modifications on occlusion and the reference vs. non-match stims.

This is a match to sample task with occluders.
Its line or dot occluders. Occluder density and number of lines/dots can be varied.
Two objects are presented in succession. Match saccade right, non-match left.
"""

# Standard modules that are imported for every task.
import sys, types, math
from pype import *
from vectorops import *
from multi_matching_lookuptable import *
import random
import b8stim_new as SV
def RunSet(app):
        """
        This is what is run when you hit the 'start' button (set as such in
        the 'main' function, defined at the end of this file).
        """
        #Set the record filename if the task wants to:
        rFileName = getRecordFileName(app)
        if(rFileName is not None):
                if(os.path.exists(rFileName)):
                        if ask("pype", "overwrite file: %s ?" % (rFileName), ("yes", "no")) == 0:
                                app.record_selectfile(fname=rFileName)
                        else:
                                return
                else:
                        app.record_selectfile(fname=rFileName)

        # tally collects the results of the last N trials and displays a
        # running tally at the bottom of the main pype control window
        app.tally(clear=1)
        # This erases any information printed to the console
        app.console.clear()
        # Update the task's representation of all the parameters set in the
        # task parameter table, rig_params and monk_params - always called P
        P = app.params.check(mergewith=app.getcommon())
        # Save this version (in case you've made changes since the last time
        # the .par file was updated).
        app.params.save()
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
        # - natmpt: number of successful attempts - updated when trial gets upto
        # - the final delay before response
        app.globals.ncorrect = 0
        app.globals.natmpt = 0
        app.globals.ntrials = 0
        app.globals.uicount = 0
        app.globals.seqcorrect = 0
        app.globals.trnum = 0
        app.globals.repblock = 0        
        # saccade targets are 8dva out;
        zpx = P['mon_dpyw']/2
        zpy = P['mon_dpyh']/2
        
        # Encode all task specific codes here. 
        shft8dva = int(8*P['mon_ppd'])
        app.encode_plex('mon_ppd')
        app.encode('mon_ppd')
        app.encode_plex(int(P['mon_ppd']))
        app.encode(int(P['mon_ppd']))
        app.globals.xpos = [P['StimX'], shft8dva, -shft8dva]
        app.globals.ypos = [P['StimY'], 0, 0]
        app.globals.plexStimIDOffset = pype_plex_code_dict('plexStimIDOffset')
        app.globals.plexRotOffset = pype_plex_code_dict('plexRotOffset')
        app.globals.plexYOffset = pype_plex_code_dict('plexYOffset')
        fx,fy = P['fix_x'], P['fix_y']
        app.encode_plex('fix_x')
        app.encode_plex(fx+app.globals.plexYOffset)
        app.encode_plex('fix_y')
        app.encode_plex(fy+app.globals.plexYOffset)
        app.encode_plex('rfx')
        app.encode_plex(P['StimX']+app.globals.plexYOffset)
        app.encode_plex('rfy')
        app.encode_plex(P['StimY']+app.globals.plexYOffset)
        app.encode_plex('rfx')
        app.encode_plex(P['Ref_StimX']+app.globals.plexYOffset)
        app.encode_plex('rfy')
        app.encode_plex(P['Ref_StimY']+app.globals.plexYOffset)
        app.encode_plex('iti')
        app.encode_plex(int(P['iti']))
        app.encode_plex('isi')
        app.encode_plex(int(P['istime']))
        app.encode_plex('stim_time')
        app.encode_plex(int(P['stimtime']))
        app.encode('fix_x')
        app.encode(fx+app.globals.plexYOffset)
        app.encode('fix_y')
        app.encode(fy+app.globals.plexYOffset)
        app.encode('rfx')
        app.encode(P['StimX']+app.globals.plexYOffset)
        app.encode('rfy')
        app.encode(P['StimY']+app.globals.plexYOffset)
        app.encode('rfx')
        app.encode(P['Ref_StimX']+app.globals.plexYOffset)
        app.encode('rfy')
        app.encode(P['Ref_StimY']+app.globals.plexYOffset)
        app.encode('iti')
        app.encode(int(P['iti']))
        app.encode('isi')
        app.encode(int(P['istime']))
        app.encode('stim_time')
        app.encode(int(P['stimtime']))
        ###########################
        # Encode the occluder densities.
        
        line_widths = eval(P['occl_line_widths'])
        no_occl = [0]*len(line_widths)
        line_widths = line_widths + no_occl
        dot_widths = eval(P['occl_dot_widths'])
        no_occl = [0]*len(dot_widths)
        dot_widths = dot_widths + no_occl
        total_densities = len(line_widths) + len(dot_widths)
        app.encode_plex('occl_info')
        app.encode_plex(total_densities+app.globals.plexStimIDOffset)
        app.encode('occl_info')
        app.encode(total_densities+app.globals.plexStimIDOffset)
        for i in range(len(line_widths)):
                app.encode_plex(int(round(line_widths[i]*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))    
                app.encode(int(round(line_widths[i]*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))    
        for i in range(len(dot_widths)):
                app.encode_plex(int(round(dot_widths[i]*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
                app.encode(int(round(dot_widths[i]*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
        #########################
        # Encode the occluder numbers.
        line_numbers = eval(P['occl_num_lines'])
        no_occl = [0]*len(line_numbers)
        line_numbers = line_numbers + no_occl
        dot_numbers = eval(P['occl_num_dots'])
        no_occl = [0]*len(dot_numbers)
        dot_numbers = dot_numbers + no_occl
        total_numbers = len(line_numbers) + len(dot_numbers)
        app.encode_plex('occl_info')
        app.encode_plex(total_numbers+app.globals.plexStimIDOffset)
        app.encode('occl_info')
        app.encode(total_numbers+app.globals.plexStimIDOffset)
        for i in range(len(line_numbers)):
                app.encode_plex(line_numbers[i]+app.globals.plexStimIDOffset)
                app.encode(line_numbers[i]+app.globals.plexStimIDOffset)   
        for i in range(len(dot_numbers)):
                app.encode_plex(dot_numbers[i]+app.globals.plexStimIDOffset)
                app.encode(dot_numbers[i]+app.globals.plexStimIDOffset)
        ########################
        # Encode the reference stim numbers.
        ref_stims_list = eval(P['Ref_Stims'])
        app.encode_plex('occl_info')
        app.encode_plex(len(ref_stims_list)+app.globals.plexStimIDOffset)
        app.encode('occl_info')
        app.encode(len(ref_stims_list)+app.globals.plexStimIDOffset)
        for i in range(len(ref_stims_list)):
                app.encode_plex(ref_stims_list[i]+app.globals.plexStimIDOffset)
                app.encode(ref_stims_list[i]+app.globals.plexStimIDOffset)
        ########################
        # Encode the non-match stim numbers.
        nm_stims_list_temp = eval(P['Non_Match_List'])
        nm_stims_list = list()
        for i in range(len(nm_stims_list_temp)):
            for j in range(len(nm_stims_list_temp[i])):
                nm_stims_list.append((nm_stims_list_temp[i])[j])
        app.encode_plex('occl_info')
        app.encode_plex(len(nm_stims_list)+app.globals.plexStimIDOffset)
        app.encode('occl_info')
        app.encode(len(nm_stims_list)+app.globals.plexStimIDOffset)
        for i in range(len(nm_stims_list)):
                app.encode_plex(nm_stims_list[i]+app.globals.plexStimIDOffset)
                app.encode(nm_stims_list[i]+app.globals.plexStimIDOffset)
        #########################
        # Encode colors of stimuli.  This may not belong here as colors can change during a trial, however that is a rarity and shouldn't happen outside of training
        app.encode_plex('color')
        app.encode('color')
        stimColorName = 'SampleStim1_color'
        if(P.has_key(stimColorName)):
                colorTuple = P[stimColorName]
                app.encode_plex(colorTuple[0] + app.globals.plexRotOffset)
                app.encode_plex(colorTuple[1] + app.globals.plexRotOffset)
                app.encode_plex(colorTuple[2] + app.globals.plexRotOffset)
                app.encode(colorTuple[0] + app.globals.plexRotOffset)
                app.encode(colorTuple[1] + app.globals.plexRotOffset)
                app.encode(colorTuple[2] + app.globals.plexRotOffset)
        stimColorName = 'occl_clr'
        if(P.has_key(stimColorName)):
                colorTuple = P[stimColorName]
                app.encode_plex(colorTuple[0] + app.globals.plexRotOffset)
                app.encode_plex(colorTuple[1] + app.globals.plexRotOffset)
                app.encode_plex(colorTuple[2] + app.globals.plexRotOffset)
                app.encode(colorTuple[0] + app.globals.plexRotOffset)
                app.encode(colorTuple[1] + app.globals.plexRotOffset)
                app.encode(colorTuple[2] + app.globals.plexRotOffset)
        ##########################
        
        # Calculate stimulus eccentricity
        app.globals.ecc = ((P['StimX']**2)+(P['StimY']**2))**0.5
        # Figure out stim size in pixels
        if (P['RFscale'] == 1):
                app.globals.size = int(P['mon_ppd']+P['RFscalefactor']*app.globals.ecc)
        else:
                app.globals.size = P['SampleSize']
        # Added functionality of making the stim size a percentage of the calculated RF
        xt1 = (SV.Xarr*app.globals.size*P['SampleSizeFract']/SV.spritesize)+0.5
        yt1 = (SV.Yarr*app.globals.size*P['SampleSizeFract']/SV.spritesize)+0.5
        xt2 = xt1.tolist()
        yt2 = yt1.tolist()
        
        # Create the necessary sprites; one sprite per sample object
        # Use the multi_matching_lookup table to get the non-match stim list
        app.globals.attempted_trial = 0
        app.globals.numNonMatch = 0
        app.globals.stim_arr = []
        app.globals.pick_stims = []
        app.globals.pick_rots = []
        app.globals.ref_stim_arr = []
        app.globals.ref_pick_stims = []
        app.globals.ref_pick_rots = []
        app.globals.mylookuptable = []
        refStims = eval(P['Ref_Stims'])
        refRots = eval(P['Ref_Rots'])
        useLookUpTable = P['useLookUpTable']
        refnonMatch = eval(P['Non_Match_List'])
        nonMatchRotations = eval(P['Non_Match_Rotations'])
        myList = list(arange(len(SV.stmlist)))
        if(useLookUpTable == 1):
            for j in range(len(refStims)):
                for i in lookuptable.items():
                    if(i[0] == refStims[j]):
                        app.globals.mylookuptable.append(i[1]) #maybe keep a list of lookup table stuff
        app.globals.stimcount = 0
        # First add all the Reference Stimuli to the Stimuli List
        for j in range(len(refStims)):
            element = refStims[j]
            rotation = refRots[j]
            app.globals.pick_stims.append(element)
            app.globals.pick_rots.append(rotation) #append the reference rotation
            app.globals.stim_arr.append(Sprite(app.globals.size*2, app.globals.size*2, app.globals.xpos[0],\
                                               app.globals.ypos[0],fb=app.fb, depth=2, on=0, centerorigin=1))
            # fill the square with bg color
            app.globals.stim_arr[app.globals.stimcount].fill(P['bg_during'])
            coords1 = transpose(reshape(concatenate([xt2[app.globals.pick_stims[app.globals.stimcount]-1]\
                                            [0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50],\
                                            yt2[app.globals.pick_stims[app.globals.stimcount]-1][0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50]]),\
                                            (2,50*SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1])))
            app.globals.stim_arr[app.globals.stimcount].polygon(P['SampleStim1_color'], coords1, width=0)
            app.globals.stim_arr[app.globals.stimcount].rotate(360-rotation)
            app.globals.stim_arr[app.globals.stimcount].off()
            app.globals.ref_pick_stims.append(element)
            app.globals.ref_pick_rots.append(rotation) #append the reference rotation
            app.globals.ref_stim_arr.append(Sprite(app.globals.size*2,app.globals.size*2, P['Ref_StimX'],\
                                               P['Ref_StimY'],fb=app.fb, depth=2, on=0, centerorigin=1))
            # fill the square with bg color
            app.globals.ref_stim_arr[app.globals.stimcount].fill(P['bg_during'])
            coords1 = transpose(reshape(concatenate([xt2[app.globals.ref_pick_stims[app.globals.stimcount]-1]\
                                            [0:SV.nvrt[app.globals.ref_pick_stims[app.globals.stimcount]-1]*50],\
                                            yt2[app.globals.ref_pick_stims[app.globals.stimcount]-1][0:SV.nvrt[app.globals.ref_pick_stims[app.globals.stimcount]-1]*50]]),\
                                            (2,50*SV.nvrt[app.globals.ref_pick_stims[app.globals.stimcount]-1])))
            app.globals.ref_stim_arr[app.globals.stimcount].polygon(P['SampleStim1_color'], coords1, width=0)
            app.globals.ref_stim_arr[app.globals.stimcount].rotate(360-rotation)
            app.globals.ref_stim_arr[app.globals.stimcount].off()
            app.globals.stimcount = app.globals.stimcount + 1
            
        # Then add all the Non-Match in order to the Stimuli List
        for i in range(len(refnonMatch)):
            app.globals.numNonMatch = len(refnonMatch[i])
            for j in range(len(refnonMatch[i])):
                element = (refnonMatch[i])[j]
                rotation = (nonMatchRotations[i])[j]
                app.globals.pick_stims.append(element)
                app.globals.pick_rots.append(rotation) #append the reference rotation
                app.globals.stim_arr.append(Sprite(app.globals.size*2, app.globals.size*2, app.globals.xpos[0],\
                                               app.globals.ypos[0],fb=app.fb, depth=2, on=0, centerorigin=1))
                # fill the square with bg color
                app.globals.stim_arr[app.globals.stimcount].fill(P['bg_during'])
                coords1 = transpose(reshape(concatenate([xt2[app.globals.pick_stims[app.globals.stimcount]-1]\
                                            [0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50],\
                                            yt2[app.globals.pick_stims[app.globals.stimcount]-1][0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50]]),\
                                            (2,50*SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1])))
                app.globals.stim_arr[app.globals.stimcount].polygon(P['SampleStim1_color'], coords1, width=0)
                app.globals.stim_arr[app.globals.stimcount].rotate(360-rotation)
                app.globals.stim_arr[app.globals.stimcount].off()
                app.globals.stimcount = app.globals.stimcount + 1
        
        #Set up the trial buffers. For each trial, we need to a stimulus number, target location
        #(1:match,2:non-match) and occluder id
        #print app.globals.stimcount
        nct = 0      
        addRefStims = range(len(refStims))*((app.globals.stimcount - len(refStims))/len(refStims))
        app.globals.sampid = (list(range(len(refStims), app.globals.stimcount))) + addRefStims
        app.globals.sampid.sort()
        app.globals.occlid = [0]*(app.globals.stimcount-len(refStims))*2# this is for no occluders

        #now we need one for separate look up tables
        ### If occluders are to be shown then:
        if (P['occl_fract'] > 0.0):
            app.globals.occlid = range(((len(eval(P['occl_num_lines']))* len(eval(P['occl_line_rots'])))*2) + (len(eval(P['occl_num_dots']))*2))*len(app.globals.sampid)
            app.globals.occlid.sort()
            app.globals.sampid = (((len(eval(P['occl_num_lines']))* len(eval(P['occl_line_rots'])))*2) + (len(eval(P['occl_num_dots']))*2))*app.globals.sampid

        app.globals.stimorder = []
        a = range(len(app.globals.sampid))
        while nct < (P['repblocks']):
                if(P['randomize'] == 1):
                        random.shuffle(a)
                app.globals.stimorder = app.globals.stimorder+a
                nct = nct+1
        
        app.globals.blockLength = len(app.globals.stimorder)
        app.globals.show_occl = []
        #Now occluders on a fraction of the trials
        occltrials = int(P['occl_fract']*(len(app.globals.stimorder)/P['repblocks']*P['stimreps']))
        for i in range(occltrials):
                app.globals.show_occl.append(1)
        for i in range(len(app.globals.stimorder)-occltrials):
                app.globals.show_occl.append(0)
        random.shuffle(app.globals.show_occl)
        
        print app.globals.stimcount, addRefStims, app.globals.sampid, app.globals.stimorder
        # This plays a standard beep sequence (defined in pype.py) at the
        # start of the task.  Pretty much all tasks use it.
        app.warn_run_start()
        # Calls RunTrial, and calculates a running percentage correct.

        try:
                # I added this to keep a running "recent" percentage correct
                # because performance often changes during the task.
                ###repnum is not being used currently. Also, number of corrects doesn't 
                ###differentiate between fixbreaks and saccade errors - change these. Anitha

                pctbuffer=[0]*P['Recent Buffer Size']
                # Call Run trial only if there are still unshown stimuli in
                # the stimorder buffer
                app.globals.repblock = 0
                while (app.running and (app.globals.repblock*P['repblocks']) < P['stimreps']):
                #This task implements pause (f5) at the trial level
                        was_paused = 0
                        while(app.paused):
                                if(was_paused == 0):
                                        app.encode_plex('pause')
                                        app.encode('pause')
                                        app.globals.dlist.bg = P['pause_color']
                                        # Update the dlist and flip the framebuffer
                                        app.globals.dlist.update()
                                        app.fb.flip()
                                        was_paused = 1
                                app.idlefn()
                        if(was_paused): #reset background color
                                app.encode_plex('unpause')
                                app.encode('unpause')
                                app.globals.dlist.bg = P['bg_during']
                                # Update the dlist and flip the framebuffer
                                app.globals.dlist.update()
                                app.fb.flip()

                        try:
                                # RunTrial is a function defined below that runs a
                                # single trial.
                                result=RunTrial(app)
                        except UserAbort:
                                # The escape key will abort a trial while it's running.
                                result=None
                                pass
                        # This if statement avoids a divide-by-zero error if the
                        # first trial is aborted before ntrials is incremented
                        if app.globals.ntrials > 0:
                                pctbuffer.append(result)
                                # Average the performance over the past X trials.
                                if(app.globals.ntrials < P['Recent Buffer Size']) :
                                        recent=100*app.globals.ncorrect/app.globals.ntrials
                                        attmpt_num = pctbuffer.count(CORRECT_RESPONSE)+pctbuffer.count(WRONG_RESP)+ \
                                                                pctbuffer.count(EARLY_RELEASE)
                                        if attmpt_num > 0:
                                                recentbeh = 100*pctbuffer.count(CORRECT_RESPONSE)/attmpt_num
                                        else:
                                                recentbeh = 0.0
                                else:
                                        lastX = pctbuffer[len(pctbuffer) - P['Recent Buffer Size']::]
                                        recent=100*lastX.count(CORRECT_RESPONSE)/len(lastX)
                                        rec_attmpt = (lastX.count(CORRECT_RESPONSE)+lastX.count(WRONG_RESP)+ \
                                                                lastX.count(EARLY_RELEASE))
                                        if rec_attmpt > 0:
                                                recentbeh = 100*lastX.count(CORRECT_RESPONSE)/rec_attmpt
                                        else:
                                                recentbeh = 0.0
                        P = app.params.check(mergewith=app.getcommon())
                        if (P['redo_breakfix'] == 0 and P['redo_errors'] == 0):
                                app.globals.trnum = app.globals.ntrials
                        elif (P['redo_errors'] == 0 and P['redo_breakfix'] == 1):
                                app.globals.trnum = app.globals.natmpt
                        elif (P['redo_errors'] == 1 and P['redo_breakfix'] == 1):
                                app.globals.trnum = app.globals.ncorrect
                        elif (P['redo_errors'] == 1 and P['redo_breakfix'] == 0):
                                app.globals.trnum = app.globals.ncorrect + (app.globals.ntrials - app.globals.natmpt)
                        # This call prints the overall and recent perf % to console
                        #added on 9-22-08 by Phil to fix divide  by 0 error if first trial is a break fix
                        if(app.globals.natmpt == 0):
                                over_beh = 0.0
                        else:
                                over_beh = 100.0*app.globals.ncorrect/app.globals.natmpt
                        con(app, " %s: %d/%d %.0f%% beh: %.0f%% (recent %.0f%%  recentbeh %.0f%%)" % \
                                (now(), \
                                 app.globals.ncorrect, app.globals.ntrials, \
                                 100.0 * app.globals.ncorrect / app.globals.ntrials, \
                                 over_beh, \
                                 recent, recentbeh), 'black')
                        
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
        # This is the end of the RunSet function.
        return 1

def RunTrial(app):
        """
        RunTrial is called by RunSet.  It does housekeeping stuff associated
        with recording behavioral data for an individual trial, and calls the
        _RunTrial function which actually does the stimulus presentation and
        task control. 
        """
        # On every trial, we check to see if any parameters have been updated
        # while the last trial was running
        P = app.params.check(mergewith=app.getcommon())
        # Note the time that the trial started, again explicitly handled
        # in PypeFile class.
        app.record_note('trialtime', (app.globals.ntrials, Timestamp()))
        
        # This call starts the data record for this trial. The datafile will
        # have a 'start' event encoded with timestamp = 0. Also plexon will 
        # have and event encoded
        app.record_start()
        
        # This function will actually do the task control and stimulus display
        # and return its results back here for housekeeping.
        (result, rt, P) = _RunTrial(app, P)
        
        # Stop recording for this trial, reset eye trace and signal trial stop
        # to Plexon.  Encode 'stop' in the datafile, which is the very last
        # thing to get timestamped.
        app.record_stop()
        
        # VERY IMPORTANT, this call actually writes all of the info collected
        # in this trial into the datafile.  Don't muck with it.
        app.record_write(rt, P, taskinfo=None)
        
        # Check to see whether we've exceeded the max allowable uninitiated
        # trials, and if so, pop up a little warning box that will stall the
        # task until the user clicks it.  Note rinfo is one of the variables
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
        return result

def _RunTrial(app, P):

        """
        _RunTrial actually does the behavioral control for the task and shows
        whatever stimuli are specified, etc.  This is the meat of the task,
        and this is where you're going to make changes to make the task do
        what you want it to do. 
        """

        # # # # # # # # # # # # # # # # # #
        # General setup stuff
        # # # # # # # # # # # # # # # # # #
        if(app.globals.stimorder == []):
                a = range(len(app.globals.sampid))
                nct = 0
                while nct < (P['repblocks']):
                        if(P['randomize'] == 1):
                                random.shuffle(a)
                        app.globals.stimorder = app.globals.stimorder+a
                        nct = nct+1
        print app.globals.stimorder
        # The intertrial interval is at the start of each trial
        # (arbitrary).  Calling encode will make a note in the data record
        # with the current timestamp and whatever comment you give it.
        app.encode(START_ITI)
        app.encode_plex(START_ITI)
        app.encode(app.globals.ntrials)
        app.encode_plex(app.globals.ntrials)

        # Create instances of Timer class (also in pype.py), which counts 
        # milliseconds until it's reset. Can be queried without reset
        t = Timer()
        t.reset()
        t2 = Timer()
        thint = Timer()
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
        # Create the occluder sprites if necessary
		import pdb; pdb.set_trace()
        if P['occl_fract'] > 0.0:
                app.globals.occl_count = 0
                app.globals.occl_arr = []
                app.globals.occl_density = []
                app.globals.occl_line_widths = eval(P['occl_line_widths']) + ([0]*len(eval(P['occl_line_widths'])))
                app.globals.occl_num_lines = eval(P['occl_num_lines']) + ([0]*len(eval(P['occl_num_lines'])))
                app.globals.occl_line_rots = eval(P['occl_line_rots'])
                app.globals.occl_dot_widths = eval(P['occl_dot_widths']) + ([0]*len(eval(P['occl_dot_widths'])))
                app.globals.occl_num_dots = eval(P['occl_num_dots']) + ([0]*len(eval(P['occl_num_dots'])))
                for k in range(len(eval(P['occl_line_rots']))):
                        for i in range(len(app.globals.occl_line_widths)):
                                app.globals.occl_arr.append(Sprite(app.globals.size/sqrt(2), app.globals.size/sqrt(2), app.globals.xpos[0],\
                                        app.globals.ypos[0], fb=app.fb, depth=1, on=0, centerorigin=1))
                                app.globals.occl_arr[app.globals.occl_count].fill(P['bg_during']+(0,)) # make sprite transparent
                                w = round(app.globals.occl_line_widths[i]*(app.globals.size/sqrt(2)/10),0)
                                spacing = app.globals.size/sqrt(2)/float(app.globals.occl_num_lines[i])
                                for j in range(app.globals.occl_num_lines[i]):
                                        app.globals.occl_arr[app.globals.occl_count].rect(0, -spacing*(app.globals.occl_num_lines[i]-1)/2.0+spacing*j, app.globals.size/sqrt(2),w, P['occl_clr']+(255,))                    
                                app.globals.occl_arr[app.globals.occl_count].rotate(360-app.globals.occl_line_rots[k], preserve_size=0)
                                app.globals.occl_count = app.globals.occl_count + 1
                for i in range(len(app.globals.occl_dot_widths)):
                        app.globals.occl_arr.append(Sprite(app.globals.size/sqrt(2), app.globals.size/sqrt(2), app.globals.xpos[0],app.globals.ypos[0], fb=app.fb, depth=1, on=0, centerorigin=1))
                        app.globals.occl_arr[app.globals.occl_count].fill(P['bg_during']+(0,)) # make sprite transparent
                        spacing = app.globals.size/sqrt(2)/float(sqrt(81))
                        patrnwidth = round(app.globals.occl_dot_widths[i]*(app.globals.size/(sqrt(2)*10)),0)
                        #print int(patrnwidth)
                        w = patrnwidth # linewidth
                        a = int(app.globals.occl_num_dots[i])*[1]+(81-int(app.globals.occl_num_dots[i]))*[0]
                        random.shuffle(a)
                        count = 0
                        #trying pseudorandom dots
                        #for j in range(int(sqrt(app.globals.occl_num_dots[i]))):
                        for j in range(9):
                                #xpos = -spacing*(sqrt(app.globals.occl_num_dots[i])-1)/2.0+spacing*j
                                xpos = -spacing*(sqrt(81)-1)/2.0+spacing*j
                                for k in range(9):
                                        draw = a.pop(0)
                                        ypos = -spacing*(sqrt(81)-1)/2.0+spacing*k
                                        #random xy jitter
                                        rndx = int(spacing*(random.random()-0.5)/2.0)
                                        rndy = int(spacing*(random.random()-0.5)/2.0)
                                        if(draw == 1 and int(w) != 0):
                                                app.globals.occl_arr[app.globals.occl_count].circlefill((P['occl_clr']+(255,)),int(w),int(xpos+rndx), int(ypos+rndy))
                                                count = count + 1
                        app.globals.occl_density.append(app.globals.occl_dot_widths[i])
                        app.globals.occl_count = app.globals.occl_count + 1
                        #print count

        # The dlist manages what gets shown on the screen, it gets
        # re-initialized every trial.  app.fb is the framebuffer
        app.globals.dlist = DisplayList(app.fb)
        # set the background color - in this case, I've got a color defined
        # for the intertrial interval
        app.globals.dlist.bg = P['bg_before']
        
        # Update the dlist and flip the framebuffer
        app.globals.dlist.update()
        app.fb.flip()
        # At this point, screen color is bg_before, and otherwise blank.
        
        # # # # # # # # # # # # # # # # # #
        # Code for making a fixation spot
        # # # # # # # # # # # # # # # # # #

        # Set fx fy from P['fix_x']
        # and P['fix_y'] from the monk_params table, see comment above.
        fx,fy = P['fix_x'], P['fix_y']
        
        # align the user display, this is important for zeroing
        app.looking_at(fx, fy)

        # Here is some basic fixation point code. It either makes a dot
        # or a dot surrounded by a black ring. Note that fix_size and 
        # fix_ring are from monk_params, but fixspot color has to be 
        # specified by the task.
        
        if P['fix_ring'] > 0:
                # Create the sprite
                spot = Sprite(2*P['fix_ring'], 2*P['fix_ring'],
                                          fx, fy, fb=app.fb, depth=1, on=0, centerorigin=1)
                # fill the square with bg color
                spot.fill(P['bg_during'])
                # make a black circle of radius fix_ring at the center of the
                # sprite
                spot.circlefill((1,1,1), r=P['fix_ring'], x=0, y=0)
                # and now for the actual fixation point...
                if P['fix_size'] > 1:
                        # make another circle of radius fix_size
                        spot.circlefill(P['fixcolor1'], r=P['fix_size'], x=0, y=0)
                else:
                        # just color the center pixel - r=1 doesn't work well
                        spot[0,0] = P['fixcolor1']
        else:
                # Create a sprite without the surrounding ring
                spot = Sprite(2*P['fix_size'], 2*P['fix_size'],
                                          fx, fy, fb=app.fb, depth=1, on=0, centerorigin=1)
                spot.fill(P['bg_during'])
                if P['fix_size'] > 1:
                        spot.circlefill(P['fixcolor1'], r=P['fix_size'], x=0, y=0)
                else:
                        spot[0,0] = P['fixcolor1']
        
        # This is redundant with on=0 above, but make sure the sprite is off
        spot.off()
        # Add spot to the dlist
        app.globals.dlist.add(spot)
        con(app,"%d stimuli presented, %d stimuli remaining" % (app.globals.natmpt,(P['stimreps']*app.globals.blockLength)-(app.globals.blockLength-len(app.globals.stimorder))-(app.globals.blockLength*app.globals.repblock)),"Black")
        # # # # # # # # # # # # # # # # # #
        # Code for making the fixation window
        # # # # # # # # # # # # # # # # # #
        
        # This is the virtual boundary that defines a "good" fixation,
        # again only necessary if yours is a fixation task.
        # Adjust fixation window size for target eccentricity, since it's
        # harder to fixate on more eccentric points and there's more
        # eye tracker error too.  The min and max error parameters are
        # task-specific.
        min_e, max_e = P['min_err'], P['max_err']
        r = ((fx**2)+(fy**2))**0.5
        z = min_e + (max_e - min_e) * r / ((app.fb.w+app.fb.h)/2.0)
        # Set a parameter value that's the actual window size to use
        # this trial, so it's saved in data file.
        P['_winsize'] = int(round(P['win_size'] + z))

        # Create an instance of the FixWin class (defined in pype.py) that
        # will actually keep track of the eye position for you
        fixwin = FixWin(fx, fy, P['_winsize'], app)
        fixwin.draw(color='grey') #draws the fixwin radius on user display

        # Get the stimuli to be presented    
        location = app.globals.stimorder.pop(0)
        samp_loc2 = app.globals.sampid[location]
        refStims = eval(P['Ref_Stims'])
        t_loc = 2
        if(samp_loc2 >= 0 and samp_loc2 < len(refStims)):
            samp_loc = samp_loc2
            t_loc = 1
        elif(samp_loc2 >= 0):
            samp_loc = int(math.floor((samp_loc2 - len(refStims))/app.globals.numNonMatch))
        print samp_loc, samp_loc2
        app.globals.dlist.add(app.globals.ref_stim_arr[samp_loc]) #sample1    
        app.globals.dlist.add(app.globals.stim_arr[samp_loc2])#sample2
        
        # If its an occluder trial add occluder
        if app.globals.show_occl[app.globals.trnum] == 1:
            occl_loc = app.globals.occlid[location]
            app.globals.dlist.add(app.globals.occl_arr[occl_loc])
            
         # # # # # # # # # # # # # # # # # #
        # Code for making the target spot
        # # # # # # # # # # # # # # # # # #
        # First location of target 1
        # Here is some basic target point code. Note that targ_size is 
        # targ_color has to be specified by the task.

        # Create a sprite 
        target1 = Sprite(2*P['targ_size'], 2*P['targ_size'],
                                          app.globals.xpos[t_loc], fy, fb=app.fb, depth=1, on=0, centerorigin=1)
        target1.fill(P['bg_during'])
        if P['targ_size'] > 1:
                target1.circlefill(P['targ_color'], r=P['targ_size'], x=0, y=0)
        else:
                target1[0,0] = P['targ_color']
        
        # This is redundant with on=0 above, but make sure the sprite is off
        target1.off()
        # Add target1 to the dlist
        app.globals.dlist.add(target1)
        
        # Now the non-target spot 
        target2 = Sprite(2*P['targ_size'], 2*P['targ_size'],
                                          app.globals.xpos[3-t_loc], fy, fb=app.fb, depth=1, on=0, centerorigin=1)
        target2.fill(P['bg_during'])
        if P['targ_size'] > 1:
                target2.circlefill(P['targ_color'], r=P['targ_size'], x=0, y=0)
        else:
                target2[0,0] = P['targ_color']
        target2.off()
        app.globals.dlist.add(target2)

        # # # # # # # # # # # # # # # # # #
        # Code for making the target window
        # # # # # # # # # # # # # # # # # #
        
        # Create an instance of the FixWin class (defined in pype.py) that
        # will actually keep track of the eye position for you
        targwin = FixWin(app.globals.xpos[t_loc], fy, P['targ_winsize'], app)
        targwin.draw(color='grey') #draws the targwin radius on user display

        # Now non-targ window
        nontargwin = FixWin(app.globals.xpos[3-t_loc], fy, P['targ_winsize'], app)
        nontargwin.draw(color='black') #draws the targwin radius on user display
        # # # # # # # # # # # # # # # # # #
        # Initiate the trial
        # # # # # # # # # # # # # # # # # #

        # Start monitoring the eye trace.  This encodes an 'eye_start' event
        # in the datafile that will always be equal to the first timestamp
        # at which eyetrace data are collected.
        app.eyetrace(1)
        app.encode_plex(EYE_START)
        app.encode(EYE_START)
        # set background color to the color defined for during the trial
        app.globals.dlist.bg = P['bg_during']
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
                app.idlefn(P['iti']-t.ms())
                app.encode(END_ITI) 
                app.encode_plex(END_ITI)
                #remember we already encoded START_ITI
                # I set a flag that lets you use the start tone or not.
                if P['trial_tone']:
                        # standard tone at the start of every trial
                        app.start_tone()
                # Reset this timer to zero
                t.reset()
                
                # Flip the framebuffer to show the current dlist
                app.fb.flip() ### bg color is bg_during

                fixwin.draw(color='red')
                ttt = fixwin.on(0)
                spot_on=0
                timeout = 0
                # When we get here either the bar has been grabbed or we're not
                # monitoring it.  If the fixation point is not already
                # on, we'll turn it on now.
                if not spot_on:
                        spot.on()
                        app.globals.dlist.update()
                        app.fb.flip()
                        app.encode(FIX_ON)
                        app.encode_plex(FIX_ON)
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
                        while not fixwin.inside(0) and not TESTING:
                                # We use the same abortafter limit again
                                if P['abortafter'] > 0 and t.ms() > P['abortafter']:
                                        info(app, "no acquisition %d" % UNINITIATED_TRIAL)
                                        con(app, "no acquisition", 'blue')
                                        result = UNINITIATED_TRIAL
                                        app.encode_plex(UNINITIATED_TRIAL)
                                        app.encode(UNINITIATED_TRIAL)
                                        beep(2000,100)
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
                        while t2.ms() < P['fixwait']:
                                if not fixwin.inside(0) and not TESTING:
                                        # If at any time during the fixwait the eye
                                        # moves back out of the window, go back to waiting
                                        # for the eye to enter the window again.
                                        info(app, "passthrough")
                                        go_on = 0
                                        # This resets fixwin.inside back to zero
                                        fixwin.reset(0)
                                        # This exits the innermost while loop, and sends
                                        # us back to the top of the "while not go_on"
                                        # loop
                                        break
                                    
                # # # # # # # # # # # # # # # # # #
                # Do real trial stuff
                # # # # # # # # # # # # # # # # # #
        
                # Now, fixation has been acquired.  We can start timing the
                # length of the fixation.
                t.reset() # Reset the timer to monitor fixation length
                app.encode(FIX_ACQUIRED) # Standard event encoding
                app.encode_plex(FIX_ACQUIRED)
                fixwin.draw(color='blue') # Blue is our "active" fixwin color                    
 
                app.encode_plex('stimid')
                app.encode_plex(app.globals.ref_pick_stims[samp_loc]+app.globals.plexStimIDOffset)
                app.encode_plex('rotid')
                app.encode_plex(app.globals.ref_pick_rots[samp_loc]+app.globals.plexRotOffset)
                app.encode_plex('occlmode') #0 for none, 1 for lines, 2 for dots
                app.encode_plex(0+app.globals.plexStimIDOffset) 
                app.encode_plex('occlshape') #using for occluder number (number of lines or dots)
                app.encode_plex(0+app.globals.plexStimIDOffset)
                app.encode_plex('occl_info') #using as occluder rotation for lines
                app.encode_plex(0+app.globals.plexRotOffset)
                app.encode_plex('line_width')#occluder line width
                app.encode_plex(0+app.globals.plexStimIDOffset)
                app.encode_plex('dot_rad')#occluder dot radius
                app.encode_plex(0+app.globals.plexStimIDOffset)
                app.encode('stimid')
                app.encode(app.globals.ref_pick_stims[samp_loc]+app.globals.plexStimIDOffset)
                app.encode('rotid')
                app.encode(app.globals.ref_pick_rots[samp_loc]+app.globals.plexRotOffset)
                app.encode('occlmode') #0 for none, 1 for lines, 2 for dots
                app.encode(0+app.globals.plexStimIDOffset) 
                app.encode('occlshape') #using for occluder number (number of lines or dots)
                app.encode(0+app.globals.plexStimIDOffset)
                app.encode('occl_info') #using as occluder rotation for lines
                app.encode(0+app.globals.plexRotOffset)
                app.encode('line_width')#occluder line width
                app.encode(0+app.globals.plexStimIDOffset)
                app.encode('dot_rad')#occluder dot radius
                app.encode(0+app.globals.plexStimIDOffset)                                   
                                    
                ####Now wait for istime
                while t.ms() < P['istime']:
                        if fixwin.broke(0) and not TESTING:
                                app.encode_plex(FIX_LOST)
                                app.encode(FIX_LOST)
                                info(app, "early break")
                                con(app, "early break (%d ms)" % t2.ms(), 'red')
                                result = BREAK_FIX
                                # Auditory feedback
                                app.warn_trial_incorrect(flash=None)
                                # Skip to end of trial
                                raise MonkError
                        # Again, a call to idlefn lets the computer catch up
                        # and monitor for key presses.
                        app.idlefn()
                # now turn on the stimulus
                rfSprite = getRFSprite(app,P)
                if(rfSprite is not None):
                        app.globals.dlist.add(rfSprite)
                        rfSprite.on()
                        app.globals.dlist.update()
                app.fb.sync_toggle() #note: toggle_photo_diode updates the dlist
                app.globals.ref_stim_arr[samp_loc].on()
                app.globals.dlist.update()
                app.fb.flip()
                app.encode_plex(SAMPLE_ON)
                app.encode(SAMPLE_ON)
                app.udpy.display(app.globals.dlist)
                # wait for stimulus time
                t.reset()
                while t.ms() < P['stimtime']:
                        if fixwin.broke(0) and not TESTING:
                                app.encode_plex(FIX_LOST)
                                app.encode(FIX_LOST)
                                info(app, "early break")
                                con(app, "early break (%d ms)" % t2.ms(), 'red')
                                result = BREAK_FIX
                                app.warn_trial_incorrect(flash=None)
                                #turn off stimuli
                                app.globals.stim_arr[samp_loc].off()
                                if(rfSprite is not None):
                                        rfSprite.off()
                                app.globals.dlist.update()
                                app.fb.flip()
                                # Skip to end of trial
                                raise MonkError
                        # Again, a call to idlefn lets the computer catch up
                        # and monitor for key presses.
                        app.idlefn()
                # now turn off stimulus
                app.globals.ref_stim_arr[samp_loc].off()
                if(rfSprite is not None):
                        rfSprite.off()
                app.globals.dlist.update()
                app.fb.sync_toggle() #note: toggle_photo_diode updates the dlist
                app.fb.flip()
                app.encode_plex(SAMPLE_OFF)
                app.encode(SAMPLE_OFF)
                t.reset() # Reset timer to start second is timer   
                
                app.encode_plex('stimid')
                app.encode_plex(app.globals.pick_stims[samp_loc2]+app.globals.plexStimIDOffset)
                app.encode_plex('rotid')
                app.encode_plex(app.globals.pick_rots[samp_loc2]+app.globals.plexRotOffset)
                #app.encode_plex('occlshape') #using for occluder number (number of lines or dots)
                #app.encode_plex(occl_loc+app.globals.plexStimIDOffset)
                app.encode_plex('occlmode') #0 for none, 1 for lines, 2 for dots
                if(occl_loc > -1 and occl_loc >= (len(eval(P['occl_num_lines']))* len(eval(P['occl_line_rots'])))):
                        app.encode_plex(2+app.globals.plexStimIDOffset)
                        app.encode_plex('occlshape')
                        app.encode_plex(app.globals.occl_num_dots[occl_loc - (len(eval(P['occl_line_rots'])) * len(eval(P['occl_num_lines'])))]+app.globals.plexStimIDOffset)
                        app.encode_plex('occl_info') #using as occluder rotation for lines
                        app.encode_plex(0+app.globals.plexRotOffset)
                        app.encode_plex('line_width')#occluder line width
                        app.encode_plex(0+app.globals.plexStimIDOffset)
                        app.encode_plex('dot_rad')#occluder dot radius
                        app.encode_plex(int(round(app.globals.occl_dot_widths[occl_loc - (len(eval(P['occl_line_rots'])) * len(eval(P['occl_num_lines'])))]*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
                elif(occl_loc > -1 and occl_loc < (len(eval(P['occl_num_lines']))* len(eval(P['occl_line_rots'])))):
                        app.encode_plex(1+app.globals.plexStimIDOffset)
                        app.encode_plex('occlshape')
                        app.encode_plex(app.globals.occl_num_lines[occl_loc%len(eval(P['occl_num_lines']))]+app.globals.plexStimIDOffset)
                        app.encode_plex('occl_info') #using as occluder rotation for lines
                        app.encode_plex(app.globals.occl_line_rots[occl_loc/len(eval(P['occl_num_lines']))]+app.globals.plexRotOffset)            
                        app.encode_plex('line_width')#occluder line width
                        app.encode_plex(int(round(app.globals.occl_line_widths[occl_loc%len(eval(P['occl_num_lines']))]*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))    
                        app.encode_plex('dot_rad')#occluder dot radius
                        app.encode_plex(0+app.globals.plexStimIDOffset)
                else:
                        app.encode_plex(0+app.globals.plexStimIDOffset)
                        app.encode_plex('occlshape')
                        app.encode_plex(0+app.globals.plexStimIDOffset)
                        app.encode_plex('occl_info') #using as occluder rotation for lines
                        app.encode_plex(0+app.globals.plexRotOffset)
                        app.encode_plex('line_width')#occluder line width
                        app.encode_plex(0+app.plexStimIDOffset)
                        app.encode_plex('dot_rad')#occluder dot radius
                        app.encode_plex(0+app.plexStimIDOffset)
                app.encode('stimid')
                app.encode(app.globals.pick_stims[samp_loc2]+app.globals.plexStimIDOffset)
                app.encode('rotid')
                app.encode(app.globals.pick_rots[samp_loc2]+app.globals.plexRotOffset)
                app.encode('occlmode') #0 for none, 1 for lines, 2 for dots
                if(occl_loc > -1 and occl_loc >= (len(eval(P['occl_num_lines']))* len(eval(P['occl_line_rots'])))):
                        app.encode(2+app.globals.plexStimIDOffset)
                        app.encode('occlshape')
                        app.encode(app.globals.occl_num_dots[occl_loc - (len(eval(P['occl_line_rots'])) * len(eval(P['occl_num_lines'])))]+app.globals.plexStimIDOffset)
                        app.encode('occl_info') #using as occluder rotation for lines
                        app.encode(0+app.globals.plexRotOffset)
                        app.encode('line_width')#occluder line width
                        app.encode(0+app.globals.plexStimIDOffset)
                        app.encode('dot_rad')#occluder dot radius
                        app.encode(int(round(app.globals.occl_dot_widths[occl_loc - (len(eval(P['occl_line_rots'])) * len(eval(P['occl_num_lines'])))]*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
                elif(occl_loc > -1 and occl_loc < (len(eval(P['occl_num_lines']))* len(eval(P['occl_line_rots'])))):
                        app.encode(1+app.globals.plexStimIDOffset)
                        app.encode('occlshape')
                        app.encode(app.globals.occl_num_lines[occl_loc%len(eval(P['occl_num_lines']))]+app.globals.plexStimIDOffset)
                        app.encode('occl_info') #using as occluder rotation for lines
                        app.encode(app.globals.occl_line_rots[occl_loc/len(eval(P['occl_num_lines']))]+app.globals.plexRotOffset)            
                        app.encode('line_width')#occluder line width
                        app.encode(int(round(app.globals.occl_line_widths[occl_loc%len(eval(P['occl_num_lines']))]*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
                        app.encode('dot_rad')#occluder dot radius
                        app.encode(0+app.globals.plexStimIDOffset)
                else:
                        app.encode(0+app.globals.plexStimIDOffset)
                        app.encode('occlshape')
                        app.encode(0+app.globals.plexStimIDOffset)
                        app.encode('occl_info') #using as occluder rotation for lines
                        app.encode(0+app.globals.plexRotOffset)
                        app.encode('line_width')#occluder line width
                        app.encode(0+app.globals.plexStimIDOffset)
                        app.encode('dot_rad')#occluder dot radius
                        app.encode(0+app.globals.plexStimIDOffset)               
                
               ####Now wait for 2nd istime
                while t.ms() < P['istime']:
                        if fixwin.broke(0) and not TESTING:
                                app.encode_plex(FIX_LOST)
                                app.encode(FIX_LOST)
                                info(app, "early break")
                                con(app, "early break (%d ms)" % t2.ms(), 'red')
                                result = BREAK_FIX
                                # Auditory feedback
                                app.warn_trial_incorrect(flash=None)
                                # Skip to end of trial
                                raise MonkError
                        # Again, a call to idlefn lets the computer catch up
                        # and monitor for key presses.
                        app.idlefn()
                # now turn on the stimulus
                if(rfSprite is not None):
                        app.globals.dlist.add(rfSprite)
                        rfSprite.on()
                        app.globals.dlist.update()
                app.globals.stim_arr[samp_loc2].on()
                if app.globals.show_occl[app.globals.trnum] == 1:
                        app.globals.occl_arr[occl_loc].on()
                app.globals.dlist.update()
                app.fb.sync_toggle()
                app.fb.flip()
                app.encode_plex(SAMPLE_ON)
                app.encode(SAMPLE_ON)
                app.udpy.display(app.globals.dlist)
                if(P['variable_second_stimtime'] == 1):
                        secondStimTime = random.gauss(P['mu_stimtime'], P['std_stimtime'])
                        if(secondStimTime > P['max_stimtime'] or secondStimTime < P['min_stimtime']):
                            secondStimTime = P['stimtime']
                else:
                        secondStimTime = P['stimtime']
                # wait for stimulus time
                t.reset()
                app.encode_plex(secondStimTime+app.globals.plexStimIDOffset)
                app.encode(secondStimTime+app.globals.plexStimIDOffset)
                juice_done = 0
                while t.ms() < secondStimTime:
                        stim_juice_time = random.gauss(P['stim_juice_time'], P['std_stim_juice_time'])
                        if((t.ms() <= (stim_juice_time + 4) and t.ms() >= (stim_juice_time - 4)) and (P['secondstim_juice'] == 1) and juice_done == 0 and stim_juice_time >= P['stim_juice_time_min'] and stim_juice_time <= P['stim_juice_time_max']):
                                a = int(P['Second_Stim_Prob']*100)*[1]+(100-int(P['Second_Stim_Prob']*100))*[0]
                                secondstimjuice_go = random.choice(a)
                                if(secondstimjuice_go == 1):
                                        app.reward(multiplier=P['rmult'],dobeep=1,dojuice=1)
                                        #print 'juice'
                                juice_done = 1
                        if fixwin.broke(0) and not TESTING:
                                app.encode_plex(FIX_LOST)
                                app.encode(FIX_LOST)
                                info(app, "early break")
                                con(app, "early break (%d ms)" % t2.ms(), 'red')
                                result = BREAK_FIX
                                app.warn_trial_incorrect(flash=None)
                                #turn off stimuli
                                app.globals.stim_arr[samp_loc2].off()
                                #end_of_list = app.globals.stimorder.pop(samp_loc2)
                                #app.globals.stimorder.append(end_of_list)
                                if(rfSprite is not None):
                                        rfSprite.off()
                                if app.globals.show_occl[app.globals.trnum] == 1:
                                        app.globals.occl_arr[occl_loc].off()
                                app.globals.dlist.update()
                                app.fb.flip()
                                timeout = 1
                                """
                                This is stuff for the two breakfixes and its considered wrong stuff
                                #if(app.globals.attempted_trial==0):
                                #        app.globals.attempted_trial = 1
                                #elif (app.globals.attempted_trial == 1):
                                #        app.globals.attempted_trial = 0
                                #        result == WRONG_RESP
                                #        app.globals.natmpt = app.globals.natmpt+1
                                #else:
                                #        print 'error with the attempted trial stuff'
                                # Skip to end of trial
                                """
                                raise MonkError
                        # Again, a call to idlefn lets the computer catch up
                        # and monitor for key presses.
                        app.idlefn()
                # now turn off stimulus
                app.globals.stim_arr[samp_loc2].off()
                if(rfSprite is not None):
                        rfSprite.off()
                if app.globals.show_occl[app.globals.trnum] == 1:
                        app.globals.occl_arr[occl_loc].off()
                app.globals.dlist.update()
                app.fb.sync_toggle() #note: toggle_photo_diode updates the dlist
                app.fb.flip()
                app.encode_plex(SAMPLE_OFF)
                app.encode(SAMPLE_OFF)
                t.reset() # Reset timer to start delay timer
                ####Now wait for delay
                if(P['variable_delaytime'] == 1):
                        delaytime = random.gauss(P['mu_delaytime'], P['std_delaytime'])
                        if(delaytime > P['max_delaytime'] or delaytime < P['min_delaytime']):
                            delaytime = P['delay']
                else:
                        delaytime = P['delay']
                app.encode_plex(int(round(delaytime+app.globals.plexStimIDOffset)))
                app.encode(int(round(delaytime+app.globals.plexStimIDOffset)))
                while t.ms() < delaytime:
                        if fixwin.broke(0) and not TESTING:
                                app.encode_plex(EARLY_RELEASE)
                                app.encode(EARLY_RELEASE)
                                info(app, "early response")
                                con(app, "early response (%d ms)" % t2.ms(), 'red')
                                result = EARLY_RELEASE
                                # Auditory feedback
                                app.warn_trial_incorrect(flash=None)
                                # Skip to end of trial
                                raise MonkError
                        # Again, a call to idlefn lets the computer catch up
                        # and monitor for key presses.
                        app.idlefn()
                ## if we are here the fixation duration is done. 
                ## Now turn on target window, nontargwin and turn off fixwin
                targwin.draw(color='red')
                fixwin.clear()
                l = targwin.on(0)
                p = nontargwin.on(1)
                # Turn spot off, turn target on
                spot.off()
                a = int(P['Saccade_trial_prob']*100)*[1]+(100-int(P['Saccade_trial_prob']*100))*[0]
                saccade_go = random.choice(a)
                if saccade_go == 0:
                        raise NoProblem
                # now turn on the target stimulus and the target spot
                target1.on()
                target2.on()
                t2_on = 1
                app.globals.dlist.update()
                app.fb.flip()
                app.encode_plex('targets_on')
                app.encode('targets_on')
                app.udpy.display(app.globals.dlist)
                info(app, "waiting target acquisition")
                app.idlefn()
                t.reset()
                # Again, a dummy flag to help with task control
                go_on = 0
                while not go_on:
                        # We are waiting for the eye position to move inside the
                        # target or nontarget windows.
                        while not targwin.inside(0) and not nontargwin.inside(1) and not TESTING:
                                # Turn on target 2 after the hint duration
                                app.idlefn()    
                                #We use the maxrt line here
                                if P['maxrt'] > 0 and t.ms() > P['maxrt']:
                                        info(app, "no target saccade")
                                        con(app, "no saccade", 'blue')
                                        result = NO_RESP
                                        app.encode_plex(NO_RESP)
                                        app.encode(NO_RESP)
                                        beep(2000,100)
                                        app.globals.natmpt = app.globals.natmpt+1 #attempt only counts if it is either error response or correct.
                                        raise MonkError
                                app.idlefn()
                        # At this point, the targwin.inside or nontargwin.inside returned 1 
                        # (meaning eye is inside window).  
                        # if nontargwin is the one that the animal saccaded to its an error and the attempt counts
                        if nontargwin.inside(1)== 1:
                                rxtime = t.ms()
                                app.encode_plex(rxtime + app.globals.plexStimIDOffset)
                                info(app, "Reaction Time")
                                con(app, "Reaction Time (%d ms)" % rxtime, 'black')
                                info(app, "Wrong target saccade")
                                con(app, "Wrong saccade", 'blue')
                                result = WRONG_RESP
                                app.encode_plex(WRONG_RESP)
                                app.encode(WRONG_RESP)
                                beep(2000,100)
                                app.globals.natmpt = app.globals.natmpt+1 #attempt only counts if it is either error response or correct. 
                                raise MonkError
                        app.idlefn()
                        # Sometimes if the spot has just come
                        # on and the subject is in the process of saccading across
                        # the screen, the eye position will go through the targwin.
                        # Only count this as acquiring fixation if the eye stays in
                        # the window for "targwait" milliseconds.
                        t2.reset()
                        # First, assume we will continue if eye stays in window
                        go_on = 1
                        while t2.ms() < P['targwait']:
                                app.idlefn()
                                if not targwin.inside(0) and not TESTING:
                                        # If at any time during the targwait the eye
                                        # moves back out of the window, go back to waiting
                                        # for the eye to enter the window again.
                                        info(app, "passthrough")
                                        go_on = 0
                                        # This resets targwin.inside back to zero
                                        targwin.reset(0)
                                        # This exits the innermost while loop, and sends
                                        # us back to the top of the "while not go_on"
                                        # loop
                                        break
                                app.idlefn()
                # Now, target has been acquired.
                targwin.draw(color='blue') # Blue is our "active" color
                #nontargwin.clear()
                target2.off()
                app.globals.dlist.update()
                app.fb.flip()
                # Now hold target for target hold duration
                rxtime = t.ms()-P['targwait']
                app.encode_plex(rxtime + app.globals.plexStimIDOffset)
                app.encode(rxtime + app.globals.plexStimIDOffset)
                info(app, "Reaction Time")
                con(app, "Reaction Time (%d ms)" % rxtime, 'black')
                t.reset()
                while t.ms() < P['targ_hold']:
                        if targwin.broke(0) and not TESTING:
                                app.encode_plex(FIX_LOST)
                                app.encode(FIX_LOST)
                                info(app, "early break")
                                con(app, "early break (%d ms)" % t2.ms(), 'red')
                                result = BREAK_FIX
                                # Auditory feedback
                                app.warn_trial_incorrect(flash=None)
                                """
                                This is for the two errors and it is wrong stuff
                                # Skip to end of trial
                                #if(app.globals.attempted_trial==0):
                                #        app.globals.attempted_trial = 1
                                #elif (app.globals.attempted_trial == 1):
                                #        app.globals.attempted_trial = 0
                                #        result == WRONG_RESP
                                #        app.globals.natmpt = app.globals.natmpt+1
                                #else:
                                #        print 'error with the attempted trial stuff'
                                """
                                raise MonkError
                        # Again, a call to idlefn lets the computer catch up
                        # and monitor for key presses.
                        app.idlefn()
                        ################################
                # If you are here then the trial is correct and counts as a attempt
                raise NoProblem                
                                                
        # # # # # # # # # # # # # # # # # #
        # Handling exceptions generated in the trial
        # # # # # # # # # # # # # # # # # #
        
        except UserAbort:
                # If you pressed the escape key at any time to abort the trial
                # you will end up here.  No counters are incremented or
                # reset basically because this was not the subject's fault.
                con(app, "Aborted.", 'red')
                # These variables will be returned to RunTrial.
                result = USER_ABORT
                app.encode_plex(USER_ABORT)
                app.fb.sync(0)
        except MonkError:
                # Any of the MonkError exceptions will land you here.  The
                # trial counter is incremented and the seqcorrect counter
                # is reset.
                app.globals.ntrials = app.globals.ntrials + 1
                app.globals.seqcorrect = 0
                if((result != WRONG_RESP and result != NO_RESP) and P['redo_breakfix'] == 1):
                        if(P['redo_immediately'] == 1):
                                app.globals.stimorder.insert(0,location)
                        else:
                                app.globals.stimorder.append(location)
                                random.shuffle(app.globals.stimorder)
                                #print location
                                #print app.globals.stimorder
                if result == WRONG_RESP:
                        if(P['redo_errors'] == 1):
                                if(P['redo_immediately'] == 1):
                                        app.globals.stimorder.insert(0,location)
                                else:
                                        app.globals.stimorder.append(location)
                                        random.shuffle(app.globals.stimorder)
                        app.globals.attempted_trial = 0
                        if(t_loc == 1):
                                clk_num = P['numdrops_err_match']
                        else:
                                clk_num = P['numdrops_err_non_match']
                        a = int(P['rew_prob']*100)*[1]+(100-int(P['rew_prob']*100))*[0]
                        juice_go = random.choice(a)
                        while clk_num > 0:
                                if juice_go == 1:
                                    app.reward(multiplier=P['rmult'],dobeep=1,dojuice=1)
                                else:
                                    app.reward(multiplier=P['rmult'],dobeep=1,dojuice=0)
                                app.idlefn(50)#time between juice drops
                                clk_num = clk_num-1
                app.fb.sync(0)
        except NoProblem:
                # Having an exception for a correct trial is handy because
                # there are a number of ways of getting the trial correct
                # depending on whether we're monitoring the eye position or
                # touch bar or dot dimming, and we can put all the reward
                # code in one place.
                result = CORRECT_RESPONSE
                app.encode_plex(CORRECT_RESPONSE)
                app.encode(CORRECT_RESPONSE)
                app.warn_trial_correct() #Standard "correct" beep
                app.encode(REWARD)
                app.encode_plex(REWARD)
                # Increment the sequence correct counter
                app.globals.seqcorrect=app.globals.seqcorrect + 1
                app.globals.attempted_trial = 0
                # Without arguments this call dispenses a reward of size
                # 'dropsize' with a variance of 'dropvar' (both specified
                # in monk_params). The multiplier argument multiplies the
                # "standard" reward by whatever value is passed in.
                if(t_loc == 1):
                        clk_num = P['numdrops_match']
                else:
                        clk_num = P['numdrops_non_match']
                a = int(P['rew_prob']*100)*[1]+(100-int(P['rew_prob']*100))*[0]
                juice_go = random.choice(a)
                con(app, "juice_go ::: %d" % (juice_go), 'black')
                while clk_num > 0:
                        if juice_go == 1:
                            app.reward(multiplier=P['rmult'],dobeep=1,dojuice=1)
                        else:
                            app.reward(multiplier=P['rmult'],dobeep=1,dojuice=0)
                        app.idlefn(50)#time between juice drops
                        clk_num = clk_num-1
                app.fb.sync(0)            
                # Reporting stuff, variables returned to RunTrial
                app.globals.natmpt = app.globals.natmpt+1
                app.globals.ncorrect = app.globals.ncorrect + 1
                app.globals.ntrials = app.globals.ntrials + 1

        
        # # # # # # # # # # # # # # # # # #
        # Cleanup
        # # # # # # # # # # # # # # # # # #
        
        # This code runs no matter what the result was, it is after all the
        # exception handling
        spot.off()
        # Turn off the fixation spot and tracker dot
        target1.off()
        target2.off()
        app.encode(FIX_OFF)
        app.encode_plex(FIX_OFF)
        # Stop monitoring eye position, encode 'eye_stop' in the datafile
        # which will always be the last timestamp at which eyetrace data
        # were collected.
        targwin.clear()
        app.eyetrace(0)
        app.encode_plex(EYE_STOP)
        app.encode(EYE_STOP)
        app.globals.stim_arr[samp_loc].off()#the sample
        if t_loc == 2:
                app.globals.stim_arr[samp_loc2].off()#the 2nd sample
        # Re-set the background for the intertrial interval
        app.globals.dlist.bg = P['bg_before']
        app.globals.dlist.update()
        app.fb.flip()
        # Clear the user display
        app.udpy.display(None)
        # update behavioral history log on GUI window
        app.history(result[0])

        # If this was an incorrect trial, wait for the timeout period
        # (we do this now so that everything has been shut off and the
        # background is not the "active" color during the timeout
        # period).
        
        if(app.globals.stimorder == []):
                app.globals.repblock = app.globals.repblock + 1
                
        if result == BREAK_FIX:
                if(timeout == 1):
                        if P['timeout'] > 0:
                                app.globals.dlist.bg = P['breakerror_color']
                                app.globals.dlist.update()
                                app.fb.flip()
                                info(app, "error timeout..")
                                app.idlefn(ms=P['timeout'])
                                info(app, "done.")

        # Don't know what this does.  Don't touch.
        app.looking_at()
        
        # Update the performance tally on the pype control window.
        app.tally(type=result)

        # Return variables to RunTrial for housekeeping.
        return (result, rt, P)                              

def main(app):
        """
        Every python program with multiple functions needs to have a main
        function.  This sets up the parameter table, initializes app.globals,
        and defines RunSet as the start function.  You will need to mess
        with the parameter table to add new parameters for your task and
        remove useless ones, but beyond that don't change things in this
        function unless you're *really* sure you know what you're doing.
        """

        # Initialize things
        app.globals = Holder()
        app.idlefb()
        app.startfn = RunSet
        app.mybutton = app.taskbutton(text=__name__, check=1)
        app.notebook = DockWindow(title=__name__, checkbutton=app.mybutton)
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
        
        app.params = ParamTable(app.notebook, (
                ("Subject Params", None, None),
                ("usebar",        "1",               is_boolean,),
                ("trial_tone",    "1",               is_boolean, "tone at every trial"),
                ("grabbeep",    "1",               is_boolean, "beep at bar grab"),
                ("barfirst",    "1",               is_boolean, "grab bar before fixspot"),
                ("Reward Params", None, None),
                ("numdrops_match",    "15",           is_int, "Number of juice drops"),
                ("numdrops_non_match",    "15",           is_int, "Number of juice drops"),
                ("numdrops_err_match","2",            is_int, "Number of juice drops on an error"),
                ("numdrops_err_non_match","2",            is_int, "Number of juice drops on an error"),   
                ("rew_prob",    "1.0",            is_float, "Probability of reward"),
                ("rmult",        "1.0",               is_float),
                ("seqcor",      "2",            is_int),
                ("seqcor_reset","1",            is_boolean),
                ("allornone",   "1",            is_float, "0->1, prob of drop"),
                ("secondstim_juice", "0", is_boolean),
                ("stim_juice_time", "300", is_int),
                ("stim_juice_time_min", "100", is_int),
                ("stim_juice_time_max", "600", is_int),
                ("std_stim_juice_time", "20", is_int),
                ("Second_Stim_Prob", "1.0",            is_float, "Probability of second stim reward"),
                ("Dot Dimming Params", None, None),
                ("dim",            "1",            is_boolean, "do dot dimming?"),
                ("fixcolor1",    "(255,255,255)",is_color),
                ("fixcolor2",    "(255,255,255)",is_color),
                ("maxrt",       "500",          is_int),
                ("targ_size",    "5",            is_int, "size of target"),
                ("targ_color",     "(255,255,255)",    is_color, "Target color"),
                ("Task Params", None, None),
                ("istime",    "200",               is_int, "Inter-stimulus time"),
                ("stimtime", "600",            is_int, "Stimulus duration"),
                ("variable_second_stimtime", "0",            is_boolean, "If 1 then second stimulus duration is picked from a gaussian distribution"),
                ("mu_stimtime", "400",            is_int, "Mu in a Gaussian Distribution to select random second stim time"),
                ("min_stimtime", "200",            is_int, "Min in a Gaussian Distribution to select random second stim time"),
                ("max_stimtime", "600",            is_int, "Max in a Gaussian Distribution to select random second stim time"),
                ("std_stimtime", "10",            is_int, "Std in a Gaussian Distribution to select random second stim time"),
                ("delay",    "10",            is_int, "Delay period"),
		("variable_delaytime", "0",            is_boolean, "If 1 then second stimulus duration is picked from a gaussian distribution"),
                ("mu_delaytime", "50",            is_int, "Mu in a Gaussian Distribution to select random second stim time"),
                ("min_delaytime", "10",            is_int, "Min in a Gaussian Distribution to select random second stim time"),
                ("max_delaytime", "100",            is_int, "Max in a Gaussian Distribution to select random second stim time"),
                ("std_delaytime", "40",            is_int, "Std in a Gaussian Distribution to select random second stim time"),
                ("targ_hold",    "50",        is_int, "Duration to fixate at target"),
                ("min_err",        "0",               is_int),
                ("max_err",        "10000",               is_int),
                ("bg_before",    "(25,25,25)",           is_color),
                ("bg_during",    "(25,25,25)",is_color),
                ("fixlag",        "50",               is_int),
                ("fixwait",        "100",               is_int),
                ("targ_winsize","70",            is_int,    "Target window size"),
                ("targwait",    "50",            is_int,    "Duration to wait for passing through saccades"),
                ("useLookUpTable", "1", is_int, "1:Use preselected non-match; 0:Use selected non-match"),        
                ("Ref_Stims", "[]", is_any, "Reference Stim Numbers"),
                ("Ref_Rots", "[]", is_any, "Reference Stim Rotations"),
                ("Non_Match_List", "[]", is_any, "Non-match stims for Reference Stims- Put into list of lists"), 
                ("Non_Match_Rotations", "[]", is_any, "Non-match stim rotations for Reference Stims - Must match Non_Match_List"),
                ("StimX",            "0",            is_int, "Stimulus X location"),
                ("StimY",            "0",             is_int, "Stimulus Y location"),
                ("Ref_StimX",            "0",            is_int, "Reference Stimulus X location"),
                ("Ref_StimY",            "0",             is_int, "Reference Stimulus Y location"),
                ("RFscale",        "0",                is_boolean, "1:Scale stimulus size by RF size; 0:Use SampleSize"), 
                ("RFscalefactor",    "0.625",        is_float, "If scale by RF size, what's the scale factor?"),
                ("SampleSize",        "100",            is_int, "Sample stimulus size in pixels"),
                ("SampleSizeFract", ".9", is_float, "Fraction of RF that the size of the stimulus is suppose to be."),
                ("SampleStim1_color", "(255,1,1)",    is_color),
                ("Saccade_trial_prob","0.5",        is_float, "Fraction of trials on which saccade target is presented"),
                ("Occluder parameters", None, None),
                ("occl_num_lines", "[]",                is_any, "Number of lines for each type of occluder -- MAKE SURE SAME SIZE AS OTHER PARAMS"),
                ("occl_line_widths", "[]",                is_any, "Width of lines/dots for each type of occluder -- MAKE SURE SAME SIZE AS OTHER PARAMS"),
                ("occl_line_rots", "[]",         is_any, "rotations of line occluders"),
                ("occl_num_dots", "[]",         is_any, "Number of Dots for each dot occluder"),
                ("occl_dot_widths", "[]",         is_any, "Widths of dots."),
                ("occl_fract",  "1.0",            is_float, "Fraction of trials on which to present the occluder"),
                ("occl_clr",    "(55,55,1)",    is_color, "Occluder color"),
                ("Eye Params", None, None),
                ("innerwin",    "0",               is_int),
                ("track",        "0",               is_boolean),
                ("track_xo",       "0",               is_int, "offset of track point"),
                ("track_yo",       "0",               is_int, "offset of track point"),
                ("track_color", "(255,255,0)",     is_color),
                ("Misc Params", None, None, "Miscellaneous Parameters"),
                ("Recent Buffer Size", "50", is_int, "The number of trials to use to calculate recent performance"),
                ("pause_color", "(150,0,0)", is_color, "The screen will turn this color when the task is paused"),
                ("breakerror_color", "(150,0,0)", is_color, "The screen will turn this color when breakfix on second stim"),
                ("stimreps", "250", is_int, "Total number of repetitions per stimulus/response combination"),
                ("repblocks", "250", is_int, "Total number of repetitions per stimulus/response combination"),
                ("redo_errors", "0", is_int,    "0: do not repeat error trials, 1:repeat errors"),
                ("redo_breakfix", "0", is_int,  "0:do not repeat breakfix trials, 1:repeat breakfix"),
                ("redo_immediately", "0", is_int,  "0:do not repeat immediately, 1:repeat immediately"),
                ("ShowRFSprite", "0", is_boolean, "if 1 show the rf"),
                ("randomize",    "1", is_int,    "randomize?"),
                ("Record File Params", None, None, "Params for setting name of record file"),
                ("Use Special Name", "0", is_boolean, "If 1 then the record file name will be AnimalPrefixDate_TaskName_CellGroup_Iteration.rec"),
                ("RFDirectory", "\\home\\shapelab\\recordFiles\\", is_any, "Directory to use for Record Files"),               
                ("AnimalPrefix", "m", is_any, "Animal Prefix to use"),
                ("Date","080325", is_any, "Date to use "),
                ("TaskName","newAIM1", is_any, "TaskName"),
                ("CellGroup","01", is_int, "# of cell group encountered today"),
                ("Iteration","01", is_int, "# of times this task has been run on this cell group")
                ), file=parfile)

def getRFSprite(app,P):
        if(P['ShowRFSprite']):
                circleSprite = Sprite(app.globals.size*2, app.globals.size*2, P['StimX'],P['StimY'],fb=app.fb, depth=1, on=0,centerorigin=1)
                circleSprite.fill(P['bg_during']+(0,))
                circleSprite.circlefill((255,255,255),r=app.globals.size/2.0,x=0,y=0,width=1)
                return circleSprite
        else:
                return None

def cleanup(app):
        """
        This is not run from within the program anywhere, but I believe
        it is necessary because every task has one.  Perhaps it is called
        by pype itself when the task is unloaded.
        """
        app.params.save()
        app.mybutton.destroy()
        app.notebook.destroy()
        # The dlist should get deleted as part of cleanup, or else all
        # the sprites remain in memory when the task is unloaded.  In
        # this task dlist is part of app.globals.  In tasks where users
        # have chosen not to use app.globals, they need to add a line
        # here to delete the dlist explicitly.
        del app.globals

def toggle_photo_diode(self,app):
        app.globals.dlist.update()
        app.fb.sync_toggle()

def turn_off_photo_diode(self,app):
        app.fb.sync(0)

def getRecordFileName(app): #gets the record file for this task 
        params = app.params.check()
        if(params['Use Special Name']):
                filename = "%s%s%s_%s_%02d_%02d.rec" % (params['RFDirectory'],params['AnimalPrefix'],params['Date'],params['TaskName'],params['CellGroup'],params['Iteration'])
        else:
                filename = None
        return filename

def includedOnlyCompletedTrials(self):
        return 0

# This is also something that all tasks have, and it's a python thing.
# Don't touch it.

if not __name__ == '__main__':
        loadwarn(__name__)
else:
        dump(sys.argv[1])
