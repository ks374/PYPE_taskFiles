#!/usr/bin/python
# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-

"""
11/15/2019 PZ

This is a Neuropixels version of RT match-to-sample task with occluders.
"Swiss-cheese" occluder, line windows. Line width and number of lines can be varied.
Two objects are presented in succession. Targets are delayed. Match saccade right, non-match left.

3/5/2020 - added all.globals.init_motion_dir - to alternate between opposite motion angles

9/3/2020 - Erin
- removed old print statements
- added print statements to determine sizes of stimuli lists/variables

9/4/2020 - Erin
- removed dot occluder functionality, dots are not used for this task anymore
- removed occl_line_rots parameter, is not being used
- fixed stimreps and repblocks

9/10/2020 - Erin
- fixed how no_occl_reps was being used, removed occl_fract
- fixed how it decides when to show occlusion, now uses occl_show

9/11/2020 - Erin
- fixed division by 0 errors

10/2/20 - Erin
- fixed/clarified the locations of fixation, targets, RF1&2, and 2nd stimulus

10/16/20 - Erin
- added encoding of the second stim start and end location
- also calculates the average x and y speed of the stim over the trial and encodes them and the trial duration
- fixed the x and y lim of motion and the start location so that the second stimuli moves at the correct angle and travels directly down the center of the occluder

10/19/20 - Erin
- double checked/fixed all encoding lines so we should have all the info we need encoded now
"""

# Standard modules that are imported for every task.
import os, sys, types, math, time # Tomo NPX PZ 2/7/2020 - os needed to specify file location
from pype import *
from vectorops import *
from multi_matching_lookuptable import *
import random
import random as Randy
import b8stim_new as SV
from random import randint, choice
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

        #check that occl_num_lines and occl_line_widths are the same length
        if len(eval(P['occl_line_widths'])) != len(eval(P['occl_num_lines'])):
            if ask("pype", "occl_num_lines and occl_line_widths are not the same length, proceed?", ("yes", "no")) == 0:
                pass
            else:
                return

        #check if there are non matchs with the reference inside
        refVsNMatchCheck = 0
        test_ref_stims_list = eval(P['Ref_Stims'])
        test_nm_stims_list_temp = eval(P['Non_Match_List'])
        for i in range(len(test_ref_stims_list)):
                for j in range(len(test_nm_stims_list_temp[i])):
                        if((test_nm_stims_list_temp[i])[j] == test_ref_stims_list[i]):
                                refVsNMatchCheck = 1
        if(refVsNMatchCheck):
                if ask("pype", "There is a reference stim in the non-match list, this may confuse subject, continue?", ("yes", "no")) == 0:
                        pass
                else:
                        return

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
        app.globals.attempted_trial = 0
        
        # PZ aug 6, 2018 - calculate percents for slit or no slit instead of conditions
        app.globals.condition_occl = [] # overall
        app.globals.condition_nooccl = [] # overall
        app.globals.condition_occl_m = [] # match, slit 
        app.globals.condition_nooccl_m = [] # match, no slit
        app.globals.condition_occl_nm = [] # n-match, slit
        app.globals.condition_nooccl_nm = [] # n-match, no slit
        
        #setting up arrays to track recent behavior per condition and ramp reward accordingly
        # 04/04/17 - ramp reward stuff borrowed from Dinas task
        app.globals.condAA = []
        app.globals.condBB = []

        # 3/5/20 PZ - to alternate between two directions of motion, starting from RF1->RF2, on next trial RF2->RF1 and so on
        app.globals.init_motion_dir = (-1)**app.globals.ntrials ##starts as 1

		# 10/21/20 EK - will be used to check if there is any data on second stim motion to be encoded at the end of the trial
		app.globals.second_stim_shown = False

        # saccade targets are 8dva out;
        zpx = P['mon_dpyw']/2
        zpy = P['mon_dpyh']/2

        app.globals.plexStimIDOffset = pype_plex_code_dict('plexStimIDOffset')
        app.globals.plexRotOffset = pype_plex_code_dict('plexRotOffset')
        app.globals.plexYOffset = pype_plex_code_dict('plexYOffset')
        app.globals.plexFloatMult = pype_plex_code_dict('plexFloatMult')

        # Encode all task specific codes here. 
        shft8dva = int(8*P['mon_ppd'])
        app.encode_plex('mon_ppd')
        app.encode_plex(int(P['mon_ppd'])+app.globals.plexStimIDOffset)
        app.encode('mon_ppd')
        app.encode(int(P['mon_ppd'])+app.globals.plexStimIDOffset)
               
        # 10/2/20 EK
        #fixation location:
        app.globals.fx = P['fix_x']
        app.globals.fy = P['fix_y']
#        print 'fix_x = ', P['fix_x'], 'fix_y = ', P['fix_y']

        #RF locations:
        app.globals.RF1X = P['RF1_X'] + P['fix_x']
        app.globals.RF1Y = P['RF1_Y'] + P['fix_y']
        app.globals.RF2X = P['RF2_X'] + P['fix_x']
        app.globals.RF2Y = P['RF2_Y'] + P['fix_y']
#        print
#        print app.globals.RF1X, app.globals.RF1Y, app.globals.RF2X, app.globals.RF2Y

        #targets and Ref stim presentation locations:
        app.globals.xpos = [P['Ref_StimX'] + P['fix_x'], P['fix_x'] + shft8dva, P['fix_x'] - shft8dva]
        app.globals.ypos = [P['Ref_StimY'] + P['fix_y'], P['fix_y'], P['fix_y']]
#       print 'xpos = ', app.globals.xpos, ' ypos = ', app.globals.ypos

        #Second stim presentation location
        app.globals.xTestStim = int((app.globals.RF1X+app.globals.RF2X)/2)
        app.globals.yTestStim = int((app.globals.RF1Y+app.globals.RF2Y)/2)
#       print 'xtestStim = ',app.globals.xTestStim,', yTestStim = ',app.globals.yTestStim
        
        # encode fixation, RF1, RF2, and Ref stim locations
        app.encode_plex('fix_x')
        app.encode_plex(int(P['fix_x'])+app.globals.plexYOffset)
        app.encode_plex('fix_y')
        app.encode_plex(int(P['fix_y'])+app.globals.plexYOffset)
        app.encode_plex('rfx')
        app.encode_plex(int(P['RF1_X'])+app.globals.plexYOffset)
        app.encode_plex('rfy')
        app.encode_plex(int(P['RF1_Y'])+app.globals.plexYOffset)
        app.encode_plex('rfx')
        app.encode_plex(int(P['RF2_X'])+app.globals.plexYOffset)
        app.encode_plex('rfy')
        app.encode_plex(int(P['RF2_Y'])+app.globals.plexYOffset)
        app.encode_plex('rfx')
        app.encode_plex(int(P['Ref_StimX'])+app.globals.plexYOffset)
        app.encode_plex('rfy')
        app.encode_plex(int(P['Ref_StimY'])+app.globals.plexYOffset)
        app.encode('fix_x')
        app.encode(int(P['fix_x'])+app.globals.plexYOffset)
        app.encode('fix_y')
        app.encode(int(P['fix_y'])+app.globals.plexYOffset)
        app.encode('rfx')
        app.encode(int(P['RF1_X'])+app.globals.plexYOffset)
        app.encode('rfy')
        app.encode(int(P['RF1_Y'])+app.globals.plexYOffset)
        app.encode('rfx')
        app.encode(int(P['RF2_X'])+app.globals.plexYOffset)
        app.encode('rfy')
        app.encode(int(P['RF2_Y'])+app.globals.plexYOffset)
        app.encode('rfx')
        app.encode(int(P['Ref_StimX'])+app.globals.plexYOffset)
        app.encode('rfy')
        app.encode(int(P['Ref_StimY'])+app.globals.plexYOffset)

        # encode trial timing stuff
        app.encode_plex('iti')
        app.encode_plex(int(P['iti']))
        app.encode_plex('isi')
        app.encode_plex(int(P['istime']))
        app.encode_plex('stim_time')
        app.encode_plex(int(P['stimtime']))
        app.encode_plex('stim_time')
        app.encode_plex(int(P['maxrt']))
        app.encode_plex('stim_time')
        app.encode_plex(int(P['target_delaytime'])+app.globals.plexStimIDOffset)
        app.encode('iti')
        app.encode(int(P['iti']))
        app.encode('isi')
        app.encode(int(P['istime']))
        app.encode('stim_time')
        app.encode(int(P['stimtime']))   
        app.encode('stim_time')
        app.encode(int(P['maxrt']))
        app.encode('stim_time')
        app.encode(int(P['target_delaytime'])+app.globals.plexStimIDOffset)


        # Calculate stimulus eccentricity
        app.globals.ecc = ((app.globals.xTestStim**2)+(app.globals.yTestStim**2))**0.5
        
        # Figure out stim size in pixels
        if (P['RFscale'] == 1):
                app.globals.size = int(P['mon_ppd']+P['RFscalefactor']*app.globals.ecc)
                app.globals.size_RF1 = int(P['mon_ppd']+P['RFscalefactor']*((app.globals.RF1X**2)+(app.globals.RF1Y**2))**0.5) # PZ 2/14/20
                app.globals.size_RF2 = int(P['mon_ppd']+P['RFscalefactor']*((app.globals.RF2X**2)+(app.globals.RF2Y**2))**0.5) # PZ 2/14/20
        else:
                app.globals.size = int(P['SampleSize'])
                app.globals.size_RF1 = int(P['SampleSize'])
                app.globals.size_RF2 = int(P['SampleSize'])

        app.globals.RFdist = math.sqrt((P['RF1_X']-P['RF2_X'])**2+(P['RF1_Y']-P['RF2_Y'])**2)

        # Added functionality of making the stim size a percentage of the calculated RF
        xt1 = (SV.Xarr*app.globals.size*P['SampleSizeFract']/SV.spritesize)+0.5
        yt1 = (SV.Yarr*app.globals.size*P['SampleSizeFract']/SV.spritesize)+0.5
        xt2 = xt1.tolist()
        yt2 = yt1.tolist()

        # Encode the stim size and RF1 and RF2 sizes and SampleSizeFract
        app.encode_plex('radius')
        app.encode_plex(app.globals.size + app.globals.plexRotOffset)
        app.encode_plex('radius')
        app.encode_plex(app.globals.size_RF1 + app.globals.plexRotOffset)
        app.encode_plex('radius')
        app.encode_plex(app.globals.size_RF2 + app.globals.plexRotOffset)
        app.encode_plex('radius')
        app.encode_plex(int(round(P['SampleSizeFract']*app.globals.plexFloatMult + app.globals.plexFloatMult)))    
        app.encode('radius')
        app.encode(app.globals.size + app.globals.plexRotOffset)
        app.encode('radius')
        app.encode(app.globals.size_RF1 + app.globals.plexRotOffset)
        app.encode('radius')
        app.encode(app.globals.size_RF2 + app.globals.plexRotOffset)
        app.encode('radius')
        app.encode(int(round(P['SampleSizeFract']*app.globals.plexFloatMult + app.globals.plexFloatMult)))   


        print "RF1_X = ", P['RF1_X']
        print "RF1_Y = ", P['RF1_Y']
        print "RF2_X = ", P['RF2_X']
        print "RF2_Y = ", P['RF2_Y']
        print "fix_x = ", P['fix_x']
        print "fix_y = ", P['fix_y']
        print 'size_RF1 = ', app.globals.size_RF1
        print 'size_RF2 = ', app.globals.size_RF2
        print

   
        ##########################
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
        # Encode the reference stim rotations.
        ref_stims_rots_list = eval(P['Ref_Rots'])
        app.encode_plex('occl_info')
        app.encode_plex(len(ref_stims_rots_list)+app.globals.plexRotOffset)
        app.encode('occl_info')
        app.encode(len(ref_stims_rots_list)+app.globals.plexRotOffset)
        for i in range(len(ref_stims_rots_list)):
                app.encode_plex(ref_stims_rots_list[i]+app.globals.plexRotOffset)
                app.encode(ref_stims_rots_list[i]+app.globals.plexRotOffset)
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
        ########################
        # Encode the non-match stim rotations.
        nm_stims_rots_list_temp = eval(P['Non_Match_List'])
        nm_stims_rots_list = list()
        for i in range(len(nm_stims_rots_list_temp)):
            for j in range(len(nm_stims_rots_list_temp[i])):
                nm_stims_list.append((nm_stims_rots_list_temp[i])[j])
        app.encode_plex('occl_info')
        app.encode_plex(len(nm_stims_rots_list)+app.globals.plexStimIDOffset)
        app.encode('occl_info')
        app.encode(len(nm_stims_rots_list)+app.globals.plexStimIDOffset)
        for i in range(len(nm_stims_rots_list)):
                app.encode_plex(nm_stims_rots_list[i]+app.globals.plexStimIDOffset)
                app.encode(nm_stims_rots_list[i]+app.globals.plexStimIDOffset)                
        #########################
        # Encode colors of stimuli and occluder.
        stimcolorTuple = P['SampleStim1_color']
        occlcolorTuple = P['occl_clr']
        app.encode_plex('color')
        app.encode_plex(stimcolorTuple[0] + app.globals.plexRotOffset)
        app.encode_plex(stimcolorTuple[1] + app.globals.plexRotOffset)
        app.encode_plex(stimcolorTuple[2] + app.globals.plexRotOffset)
        app.encode_plex('color')
        app.encode_plex(occlcolorTuple[0] + app.globals.plexRotOffset)
        app.encode_plex(occlcolorTuple[1] + app.globals.plexRotOffset)
        app.encode_plex(occlcolorTuple[2] + app.globals.plexRotOffset)
        app.encode('color')
        app.encode(stimcolorTuple[0] + app.globals.plexRotOffset)
        app.encode(stimcolorTuple[1] + app.globals.plexRotOffset)
        app.encode(stimcolorTuple[2] + app.globals.plexRotOffset)
        app.encode('color')
        app.encode(occlcolorTuple[0] + app.globals.plexRotOffset)
        app.encode(occlcolorTuple[1] + app.globals.plexRotOffset)
        app.encode(occlcolorTuple[2] + app.globals.plexRotOffset)
        ##########################


        
        # Create the necessary sprites; one sprite per sample object
        # Use the multi_matching_lookup table to get the non-match stim list
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
        refnonMatch = eval(P['Non_Match_List'])
        nonMatchRotations = eval(P['Non_Match_Rotations'])
        useLookUpTable = P['useLookUpTable']
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
            app.globals.stim_arr.append(Sprite(app.globals.size*2, app.globals.size*2, app.globals.xTestStim,\
                                               app.globals.yTestStim,fb=app.fb, depth=3, on=0, centerorigin=1))
            # fill the square with bg color
            app.globals.stim_arr[app.globals.stimcount].fill(P['bg_during'])
            if(refStims[j] == 43):
                app.globals.stim_arr[app.globals.stimcount].rect(0, 0, 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), P['SampleStim1_color'] )
            elif(refStims[j] == 44):
                app.globals.stim_arr[app.globals.stimcount].circlefill(P['SampleStim1_color'], 0.8*app.globals.size*P['SampleSizeFract']/2, 0, 0)
            else:
                coords1 = transpose(reshape(concatenate([xt2[app.globals.pick_stims[app.globals.stimcount]-1]\
                                            [0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50],\
                                            yt2[app.globals.pick_stims[app.globals.stimcount]-1][0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50]]),\
                                            (2,50*SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1])))
                app.globals.stim_arr[app.globals.stimcount].polygon(P['SampleStim1_color'], coords1, width=0)
            app.globals.stim_arr[app.globals.stimcount].rotate(360-rotation)
            app.globals.stim_arr[app.globals.stimcount].off()
            app.globals.ref_pick_stims.append(element)
            app.globals.ref_pick_rots.append(rotation) #append the reference rotation
            app.globals.ref_stim_arr.append(Sprite(app.globals.size*2,app.globals.size*2, app.globals.xpos[0],\
                                               app.globals.ypos[0],fb=app.fb, depth=3, on=0, centerorigin=1))
            # fill the square with bg color
            app.globals.ref_stim_arr[app.globals.stimcount].fill(P['bg_during'])
            if(refStims[j] == 43):
                app.globals.ref_stim_arr[app.globals.stimcount].rect(0, 0, 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), P['SampleStim1_color'] )
            elif(refStims[j] == 44):
                app.globals.ref_stim_arr[app.globals.stimcount].circlefill(P['SampleStim1_color'], 0.8*app.globals.size*P['SampleSizeFract']/2, 0, 0)
            else:
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
                element = refnonMatch[i][j]
                rotation = nonMatchRotations[i][j]
                app.globals.pick_stims.append(element)
                app.globals.pick_rots.append(rotation) #append the reference rotation
                app.globals.stim_arr.append(Sprite(app.globals.size*2, app.globals.size*2, app.globals.xTestStim,\
                                               app.globals.yTestStim,fb=app.fb, depth=3, on=0, centerorigin=1))
                # fill the square with bg color
                app.globals.stim_arr[app.globals.stimcount].fill(P['bg_during'])
                if(element == 43):
                    app.globals.stim_arr[app.globals.stimcount].rect(0, 0, 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), P['SampleStim1_color'] )
                elif(element == 44):
                    app.globals.stim_arr[app.globals.stimcount].circlefill(P['SampleStim1_color'], 0.8*app.globals.size*P['SampleSizeFract']/2, 0, 0)
                else:
                    coords1 = transpose(reshape(concatenate([xt2[app.globals.pick_stims[app.globals.stimcount]-1]\
                                            [0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50],\
                                            yt2[app.globals.pick_stims[app.globals.stimcount]-1][0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50]]),\
                                            (2,50*SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1])))
                    app.globals.stim_arr[app.globals.stimcount].polygon(P['SampleStim1_color'], coords1, width=0)
                app.globals.stim_arr[app.globals.stimcount].rotate(360-rotation)
                app.globals.stim_arr[app.globals.stimcount].off()
                app.globals.stimcount = app.globals.stimcount + 1


        # set up occlusion
        app.globals.all_occl_line_widths = ([0]*P['no_occl_reps']) + eval(P['occl_line_widths'])
        app.globals.all_occl_num_lines = ([0]*P['no_occl_reps']) + eval(P['occl_num_lines'])
        maxSeed = 1000
        minSeed = 1
        app.globals.occl_count = 0
        occl_seeds = random
        app.globals.occl_arr = []
        app.globals.occl_seeds = []
        app.globals.occl_show = []
        app.globals.occl_centers_x_list = []
        app.globals.occl_centers_y_list = []
                       

        if P['RF1_X']==P['RF2_X'] and P['RF1_Y']==P['RF2_Y']: # one RF used
            if app.globals.yTestStim == 0:
                app.globals.rotate_angle_rad = 0
            else:
                app.globals.rotate_angle_rad = math.asin(app.globals.xTestStim/math.sqrt((P['Ref_StimX']-P['RF1_X'])**2+(P['Ref_StimY']-P['RF1_Y'])**2)) # asin gives radians
        else: # multiple RF
            if (P['RF1_Y']==P['RF2_Y']):
                app.globals.rotate_angle_rad = math.pi/2
            elif (P['RF1_X']==P['RF2_X']):
                app.globals.rotate_angle_rad = 0
            elif (P['RF2_Y']>P['RF1_Y']):
                app.globals.rotate_angle_rad = math.pi/2 - math.acos((P['RF2_X']-P['RF1_X'])/app.globals.RFdist) # acos gives radians
            elif (P['RF2_Y']<P['RF1_Y']):
                app.globals.rotate_angle_rad = math.pi/2 + math.acos((P['RF2_X']-P['RF1_X'])/app.globals.RFdist) # acos gives radians 
                                            
        app.globals.rotate_angle = math.degrees(app.globals.rotate_angle_rad) # rotate function requires degrees
        print 'app.globals.rotate_angle = ', app.globals.rotate_angle_rad, ' rad, ', app.globals.rotate_angle, ' deg'
        slit_w = max(app.globals.size_RF1,app.globals.size_RF2)
#        print 'slit_w = ', slit_w
#        print app.globals.RFdist

        # PZ 3/26/18 encode motion direction, in degrees
        app.encode_plex('extra') 
        app.encode_plex(int(round(math.degrees(app.globals.rotate_angle_rad)*app.globals.plexFloatMult + app.globals.plexFloatMult)))
        app.encode('extra') 
        app.encode(int(round(math.degrees(app.globals.rotate_angle_rad)*app.globals.plexFloatMult + app.globals.plexFloatMult)))

        # Create the occluder sprites            
        for i in range(len(app.globals.all_occl_line_widths)):
#           print 'width = ',app.globals.all_occl_line_widths[i]
            app.globals.occl_arr.append(Sprite(app.globals.size*5, int(app.globals.size*5), app.globals.xTestStim, app.globals.yTestStim, fb=app.fb, depth=2, on=0, centerorigin=1))
            app.globals.occl_seeds.append(0)
            app.globals.occl_arr[app.globals.occl_count].fill(P['bg_during']+(0,)) # make sprite transparent
            if app.globals.all_occl_line_widths[i] != 0:
                    #app.globals.occl_arr[app.globals.occl_count].rect(0, 0, app.globals.size*1.2, app.globals.size*2.5, P['occl_clr']+(255,))
                    app.globals.occl_arr[app.globals.occl_count].rect(0, 0, slit_w*1.25, (app.globals.RFdist+app.globals.size_RF1/2+app.globals.size_RF2/2+app.globals.size), P['occl_clr']+(255,))
                    w = round(app.globals.all_occl_line_widths[i]*(app.globals.RFdist/10),0)
#                   print 'w = ',w
                    spacing = (app.globals.RFdist)/float(app.globals.all_occl_num_lines[i])
#                   print 'spacing = ', spacing
                    app.globals.occl_seeds[app.globals.occl_count] = occl_seeds.randint(minSeed,maxSeed+1)
                    randomizer = random
                    randomizer.seed(app.globals.occl_seeds[app.globals.occl_count])
                    centersx = []
                    centersy = []
                    for j in range(app.globals.all_occl_num_lines[i]):
                        x = randomizer.choice([-1,1])*randomizer.randint(0,int(app.globals.RFdist/3))
                        y = -spacing*(app.globals.all_occl_num_lines[i]-1)/2.0+spacing*j
                        centersx.append(x)
                        centersy.append(y)
                        app.globals.occl_arr[app.globals.occl_count].rect(x, y, app.globals.size*1.5,w, P['occl_clr']+(0,))                                 
                    app.globals.occl_arr[app.globals.occl_count].rotate(app.globals.rotate_angle)
                    app.globals.occl_show.append(1)
                    app.globals.occl_centers_x_list.append(centersx)
                    app.globals.occl_centers_y_list.append(centersy)
            else:
                    app.globals.occl_show.append(0)
                    app.globals.occl_centers_x_list.append([])
                    app.globals.occl_centers_y_list.append([])                     
            app.globals.occl_count += 1
        
#        print app.globals.occl_seeds
        print app.globals.xTestStim, app.globals.yTestStim    
        print app.globals.occl_centers_x_list
        print app.globals.occl_centers_y_list
        

        ###########################
        # Encode the occluder line widths.
        line_widths = eval(P['occl_line_widths'])
        if P['no_occl_reps'] > 0:
            no_occl = [0]
            line_widths = no_occl + line_widths
        total_line_widths = len(line_widths)
        app.encode_plex('occl_info')
        app.encode_plex(total_line_widths+app.globals.plexStimIDOffset)
        app.encode('occl_info')
        app.encode(total_line_widths+app.globals.plexStimIDOffset)
        
        for i in range(len(line_widths)):
                app.encode_plex(int(round(line_widths[i]*app.globals.plexFloatMult + app.globals.plexFloatMult)))    
                app.encode(int(round(line_widths[i]*app.globals.plexFloatMult + app.globals.plexFloatMult)))    
        ########################
        # Encode the occluder numbers of lines.
        line_numbers = eval(P['occl_num_lines'])
        if P['no_occl_reps'] > 0:
            no_occl = [0]
            line_numbers = no_occl + line_numbers
        total_line_numbers = len(line_numbers)
        app.encode_plex('occl_info')
        app.encode_plex(total_line_numbers+app.globals.plexStimIDOffset)
        app.encode('occl_info')
        app.encode(total_line_numbers+app.globals.plexStimIDOffset)
        for i in range(len(line_numbers)):
                app.encode_plex(line_numbers[i]+app.globals.plexStimIDOffset)
                app.encode(line_numbers[i]+app.globals.plexStimIDOffset)   
        ########################
        # Encode the occluder seeds.
        seeds = []
        for i in range(len(app.globals.occl_seeds)):
            if app.globals.occl_seeds[i] != 0:
                seeds.append(app.globals.occl_seeds[i])
        if P['no_occl_reps'] > 0:
            no_occl = [0]
            seeds = no_occl + seeds
        total_occl_seeds = len(seeds)
        app.encode_plex('occl_info')
        app.encode_plex(total_occl_seeds+app.globals.plexStimIDOffset)
        app.encode('occl_info')
        app.encode(total_occl_seeds+app.globals.plexStimIDOffset)
        for i in range(len(seeds)):
                app.encode_plex(seeds[i]+app.globals.plexStimIDOffset)
                app.encode(seeds[i]+app.globals.plexStimIDOffset)  
        ########################
        # Encode the stepsizes.
        #app.globals.stepsizeList = [0,0.8,1.2,1.6,2.0,2.4]
        # PZ 2/21/20 - no stable condition any longer
        app.globals.stepsizeList = [0.6,1.0,1.4,1.8,2.2]
        app.encode_plex('occl_info')
        app.encode_plex(len(app.globals.stepsizeList)+app.globals.plexStimIDOffset)
        app.encode('occl_info')
        app.encode(len(app.globals.stepsizeList)+app.globals.plexStimIDOffset)
        for i in range(len(app.globals.stepsizeList)):
                app.encode_plex(int(round(app.globals.stepsizeList[i]*app.globals.plexFloatMult + app.globals.plexFloatMult)))
                app.encode(int(round(app.globals.stepsizeList[i]*app.globals.plexFloatMult + app.globals.plexFloatMult)))   
        ##########################


#        print 'occl_num_lines = ', P['occl_num_lines']
#        print 'occl_line_widths = ', P['occl_line_widths']
#        print 'no_occl_reps = ', P['no_occl_reps']
#        print 'all widths = ',app.globals.all_occl_line_widths
#        print 'all lines = ', app.globals.all_occl_num_lines
#        
#        print 'occl_count = ', app.globals.occl_count
#        
#        print 'occl_seeds = ', app.globals.occl_seeds
#        print 'occl_arr = ', app.globals.occl_arr
#        print 'occl_show = ', app.globals.occl_show
                        
        #Set up the trial buffers. For each trial, we need to a stimulus number, target location
        #(1:match,2:non-match) and occluder id
        addRefStims = range(len(refStims))*len(refnonMatch[0])
#        print
#        print
#        print 'len(refStims) = ', len(refStims)
#        print 'len(refnonMatch) = ', len(refnonMatch)*len(refnonMatch[0])
#        print 'stimcount = ', app.globals.stimcount
#        print 'addRefStims = ', addRefStims
#        print 'len(addRefStims) = ', len(addRefStims) 
#        print
        app.globals.sampid = (list(range(len(refStims), app.globals.stimcount))) + addRefStims
        app.globals.sampid.sort()
        
        app.globals.steps = eval(P['motion_speed'])

        app.globals.stepid = app.globals.occl_count*len(app.globals.sampid)*app.globals.steps #edited for speeds
        app.globals.stepid.sort()
        
        app.globals.occlid = range(app.globals.occl_count)*len(app.globals.sampid) #edited for speeds
        app.globals.occlid.sort()
        app.globals.occlid = app.globals.occlid*len(app.globals.steps)
        
        app.globals.sampid = app.globals.occl_count*len(app.globals.steps)*app.globals.sampid #edited for speeds

        app.globals.stimorder = range(len(app.globals.sampid))*P['stimreps']
        if(P['randomize'] == 1):
            random.shuffle(app.globals.stimorder)

#        a = range(len(app.globals.sampid))
#        for i in range(P['stimreps']):
#            if(P['randomize'] == 1):
#                random.shuffle(a)
#            app.globals.stimorder = app.globals.stimorder+a

#       print 'len(occlid) = ', len(app.globals.occlid)
#       print 'len(stepid) = ', len(app.globals.stepid)
#       print 'len(sampid) = ', len(app.globals.sampid)
#       print 'occlid = ',app.globals.occlid,', stepid = ',app.globals.stepid,', sampid = ',app.globals.sampid
#       print                                                
        app.globals.blockLength = len(app.globals.stimorder)
#        print "len(stimorder) = ", len(app.globals.stimorder)
#        print "blockLength = ", app.globals.blockLength        

#        print

        
        # This plays a standard beep sequence (defined in pype.py) at the
        # start of the task.  Pretty much all tasks use it.
        app.warn_run_start()
        # Calls RunTrial, and calculates a running percentage correct.
        saveEvents(app)

        try:
                # I added this to keep a running "recent" percentage correct
                # because performance often changes during the task.
                ###repnum is not being used currently. Also, number of corrects doesn't 
                ###differentiate between fixbreaks and saccade errors - change these. Anitha

                app.globals.pctbuffer=[0]*P['Recent Buffer Size']
                app.globals.pctbuffer2=[0]*P['Reward Buffer Size']
                # Call Run trial only if there are still unshown stimuli in
                # the stimorder buffer
                app.globals.repblock = 0
                while (app.running and (app.globals.repblock < P['repblocks'])):
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
                                saveEvents(app)
                        except UserAbort:
                                # The escape key will abort a trial while it's running.
                                result=None
                                pass
                        # This if statement avoids a divide-by-zero error if the
                        # first trial is aborted before ntrials is incremented
                        if app.globals.ntrials > 0:
                                app.globals.pctbuffer.append(result)
                                # Average the performance over the past X trials.
                                if(app.globals.ntrials < P['Recent Buffer Size']) :
                                        recent=100*app.globals.ncorrect/app.globals.ntrials
                                        attmpt_num = app.globals.pctbuffer.count(CORRECT_RESPONSE)+app.globals.pctbuffer.count(WRONG_RESP)#+ \
                                                                #app.globals.pctbuffer.count(EARLY_RELEASE)
                                        if attmpt_num > 0:
                                                recentbeh = 100*app.globals.pctbuffer.count(CORRECT_RESPONSE)/attmpt_num
                                                app.globals.recentbeh = recentbeh
                                        else:
                                                recentbeh = 0.0
                                                app.globals.recentbeh = recentbeh
                                else:
                                        app.globals.lastX = app.globals.pctbuffer[len(app.globals.pctbuffer) - P['Recent Buffer Size']::]
                                        recent=100*app.globals.lastX.count(CORRECT_RESPONSE)/len(app.globals.lastX)
                                        rec_attmpt = (app.globals.lastX.count(CORRECT_RESPONSE)+app.globals.lastX.count(WRONG_RESP)+ \
                                                                app.globals.lastX.count(EARLY_RELEASE)-app.globals.lastX.count(EARLY_RELEASE))
                                        if rec_attmpt > 0:
                                                recentbeh = 100*app.globals.lastX.count(CORRECT_RESPONSE)/rec_attmpt
                                                app.globals.recentbeh = recentbeh
                                        else:
                                                recentbeh = 0.0
                                                app.globals.recentbeh = recentbeh
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
#        print "___New trial___"
        # # # # # # # # # # # # # # # # # #
        # General setup stuff
        # # # # # # # # # # # # # # # # # #
        if(app.globals.stimorder == []):
            app.globals.stimorder = range(len(app.globals.sampid))*P['stimreps']
            if(P['randomize'] == 1):
                random.shuffle(app.globals.stimorder)

#            a = range(len(app.globals.sampid))
#            for i in range(P['stimreps']):
#                if(P['randomize'] == 1):
#                    random.shuffle(a)
#                app.globals.stimorder = app.globals.stimorder+a

        # The intertrial interval is at the start of each trial
        # (arbitrary).  Calling encode will make a note in the data record
        # with the current timestamp and whatever comment you give it.
        app.encode_plex(START_ITI)
        app.encode(START_ITI)
        #saveEvents(app) # Tomo NPX - added PZ 2/7/20

        # Create instances of Timer class (also in pype.py), which counts 
        # milliseconds until it's reset. Can be queried without reset
        t = Timer()
        t.reset()
        t2 = Timer()
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

        ###where creating occl sprites used to be # 9/10/20 Erin

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
        
        # align the user display, this is important for zeroing
        app.looking_at(app.globals.fx, app.globals.fy)

        # Here is some basic fixation point code. It either makes a dot
        # or a dot surrounded by a black ring. Note that fix_size and 
        # fix_ring are from monk_params, but fixspot color has to be 
        # specified by the task.
        
        if P['fix_ring'] > 0:
                # Create the sprite
                spot = Sprite(2*P['fix_ring'], 2*P['fix_ring'],
                                          app.globals.fx, app.globals.fy, fb=app.fb, depth=1, on=0, centerorigin=1)
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
                                          app.globals.fx, app.globals.fy, fb=app.fb, depth=1, on=0, centerorigin=1)
                spot.fill(P['bg_during'])
                if P['fix_size'] > 1:
                        spot.circlefill(P['fixcolor1'], r=P['fix_size'], x=0, y=0)
                else:
                        spot[0,0] = P['fixcolor1']
        
        # This is redundant with on=0 above, but make sure the sprite is off
        spot.off()
        # Add spot to the dlist
        app.globals.dlist.add(spot)
##        print "repblocks = ", P['repblocks']
##        print "total stimuli = ", (P['repblocks']*app.globals.blockLength)
        con(app,"%d stimuli presented, %d stimuli remaining" % (app.globals.natmpt,(P['repblocks']*app.globals.blockLength)-(app.globals.blockLength-len(app.globals.stimorder))-(app.globals.blockLength*app.globals.repblock)),"Black")
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
        r = ((app.globals.fx**2)+(app.globals.fy**2))**0.5
        z = min_e + (max_e - min_e) * r / ((app.fb.w+app.fb.h)/2.0)
        # Set a parameter value that's the actual window size to use
        # this trial, so it's saved in data file.
        P['_winsize'] = int(round(P['win_size'] + z))

        # Create an instance of the FixWin class (defined in pype.py) that
        # will actually keep track of the eye position for you
        fixwin = FixWin(app.globals.fx, app.globals.fy, P['_winsize'], app)
        fixwin.draw(color='grey') #draws the fixwin radius on user display

        # Get the stimuli to be presented
#        print 'stimorder = ', app.globals.stimorder    
        location = app.globals.stimorder.pop(0)
        samp_loc2 = app.globals.sampid[location]
        refStims = eval(P['Ref_Stims'])
        t_loc = 2 #if non-match case
        if(samp_loc2 >= 0 and samp_loc2 < len(refStims)):
            samp_loc = samp_loc2
            t_loc = 1 #if match case
        elif(samp_loc2 >= 0):
            samp_loc = int(math.floor((samp_loc2 - len(refStims))/app.globals.numNonMatch))

        if(t_loc == 1): #the match case
            currentcase = 1
        else: #the non-match case - 04/04/17 borrowed from ramp reward task
            currentcase = 2
                
        app.globals.dlist.add(app.globals.ref_stim_arr[samp_loc]) #sample1    
        app.globals.dlist.add(app.globals.stim_arr[samp_loc2])#sample2
        
        
        # add occluder (either an actual occluder or a transparent sprite) #EK changed 10/12/20 because it makes the speed of stim presentation much more consistent between trials to always add an occluder sprite
        occl_loc = app.globals.occlid[location]
        app.globals.dlist.add(app.globals.occl_arr[occl_loc])
        step_loc = app.globals.stepid[location]
  
#        print 'location = ', location
#        print 'samp_loc2 = ', samp_loc2
#        print 'samp_loc = ', samp_loc
#        print 'occl_loc = ', occl_loc
#        print 'step_loc = ', step_loc
#        print 't_loc = ', t_loc
            
         # # # # # # # # # # # # # # # # # #
        # Code for making the target spot
        # # # # # # # # # # # # # # # # # #
        # First location of target 1
        # Here is some basic target point code. Note that targ_size is 
        # targ_color has to be specified by the task.

        # Create a sprite 
        target1 = Sprite(2*P['targ_size'], 2*P['targ_size'],
                                          app.globals.xpos[t_loc], app.globals.ypos[t_loc], fb=app.fb, depth=1, on=0, centerorigin=1)
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
                                          app.globals.xpos[3-t_loc], app.globals.ypos[3-t_loc], fb=app.fb, depth=1, on=0, centerorigin=1)
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
        targwin = FixWin(app.globals.xpos[t_loc], app.globals.ypos[t_loc], P['targ_winsize'], app)
        targwin.draw(color='grey') #draws the targwin radius on user display

        # Now non-targ window
        nontargwin = FixWin(app.globals.xpos[3-t_loc], app.globals.ypos[3-t_loc], P['targ_winsize'], app)
        nontargwin.draw(color='black') #draws the targwin radius on user display

        # TN added 09/16/17 
        # Create an instance of the FixWin class (defined in pype.py) that
        # will actually keep track of the eye position for you
        sacwin = FixWin(app.globals.fx, app.globals.fy, 2*P['_winsize'], app)
        sacwin.draw(color='grey') #draws the fixwin radius on user display

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
                app.encode_plex(END_ITI)
                app.encode(END_ITI) 
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
                        if (P['ShowTargWithFix']):
                            target1.on()
                            target2.on()
                        app.globals.dlist.update()
                        app.fb.flip()
                        app.encode_plex(FIX_ON)
                        app.encode(FIX_ON)
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
                                        info(app, "no acquisition")
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
                app.encode_plex(FIX_ACQUIRED)
                app.encode(FIX_ACQUIRED) # Standard event encoding
                fixwin.draw(color='blue') # Blue is our "active" fixwin color                    
 
                app.encode_plex('stimid')
                app.encode_plex(app.globals.ref_pick_stims[samp_loc]+app.globals.plexStimIDOffset)
                app.encode_plex('rotid')
                app.encode_plex(app.globals.ref_pick_rots[samp_loc]+app.globals.plexRotOffset)
                app.encode_plex('occl_info') #using to pass occl seed
                app.encode_plex(0+app.globals.plexStimIDOffset)
                app.encode_plex('occlmode') #0 for none, 1 for lines
                app.encode_plex(0+app.globals.plexStimIDOffset) 
                app.encode_plex('occlshape') #using for occluder number (number of lines)
                app.encode_plex(0+app.globals.plexStimIDOffset)
                app.encode_plex('line_width')#occluder line width
                app.encode_plex(0+app.globals.plexStimIDOffset)
                app.encode('stimid')
                app.encode(app.globals.ref_pick_stims[samp_loc]+app.globals.plexStimIDOffset)
                app.encode('rotid')
                app.encode(app.globals.ref_pick_rots[samp_loc]+app.globals.plexRotOffset)
                app.encode('occl_info') #using to pass occl seed
                app.encode(0+app.globals.plexStimIDOffset)
                app.encode('occlmode') #0 for none, 1 for lines
                app.encode(0+app.globals.plexStimIDOffset) 
                app.encode('occlshape') #using for occluder number (number of lines)
                app.encode(0+app.globals.plexStimIDOffset)
                app.encode('line_width')#occluder line width
                app.encode(0+app.globals.plexStimIDOffset)                               
                                 
                # PZ 11/6/2017: add a flag to give breakfix timeout only on breaks on 2nd stim   
                breakfix_flag = 0
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
                rfSprites = getRFSprites(app,P)
                if(rfSprites is not None):
                        app.globals.dlist.add(rfSprites[0])
                        app.globals.dlist.add(rfSprites[1])
                        rfSprites[0].on()
                        rfSprites[1].on()
                        app.globals.dlist.update()
                app.globals.ref_stim_arr[samp_loc].on()
                app.fb.sync(1)
                app.globals.dlist.update()
                app.fb.flip()
                app.encode_plex(SAMPLE_ON)
                app.encode(SAMPLE_ON)
                app.udpy.display(app.globals.dlist)
                
                #app.fb.snapshot_PZ(getRecordFileName_pz(app))
                
                # wait for stimulus time
                t.reset()
                while t.ms() < P['stimtime']:
                        if fixwin.broke(0) and not TESTING:
                                info(app, "early break")
                                con(app, "early break (%d ms)" % t2.ms(), 'red')
                                result = BREAK_FIX
                                app.warn_trial_incorrect(flash=None)
                                #turn off stimuli
                                app.globals.ref_stim_arr[samp_loc].off()
                                if(rfSprites is not None):
                                        rfSprites[0].off()
                                        rfSprites[1].off()
                                app.fb.sync(0)
                                app.globals.dlist.update()
                                app.fb.flip()
                                app.encode_plex(SAMPLE_OFF)
                                app.encode(SAMPLE_OFF)
                                app.encode_plex(FIX_LOST)
                                app.encode(FIX_LOST)
                                # Skip to end of trial
                                raise MonkError
                        # Again, a call to idlefn lets the computer catch up
                        # and monitor for key presses.
                        app.idlefn()

                '''ndrops_fix = P['numdrops_fix']                
                #ndrops_fix = 3                
                #a = int(P['rew_prob']*100)*[1]+(100-int(P['rew_prob']*100))*[0]
                #juice_go = random.choice(a)
                #con(app, "juice_go ::: %d" % (juice_go), 'black')
                while ndrops_fix > 0:
                        #if juice_go == 1:
                        app.reward(multiplier=P['rmult'],dobeep=1,dojuice=1)
                        #else:
                        #    app.reward(multiplier=P['rmult'],dobeep=1,dojuice=0)
                        app.idlefn(50)#time between juice drops
                        ndrops_fix = ndrops_fix-1'''

                # now turn off stimulus
                app.globals.ref_stim_arr[samp_loc].off()
                if(rfSprites is not None):
                        rfSprites[0].off()
                        rfSprites[1].off()
                app.fb.sync(0)
                app.globals.dlist.update()
                app.fb.flip()
                app.encode_plex(SAMPLE_OFF)
                app.encode(SAMPLE_OFF)
                t.reset() # Reset timer to start second is timer   
                
                # print 'show occl = ',app.globals.occl_show[occl_loc]
                app.encode_plex('stimid')
                app.encode_plex(app.globals.pick_stims[samp_loc2]+app.globals.plexStimIDOffset)
                app.encode_plex('rotid')
                app.encode_plex(app.globals.pick_rots[samp_loc2]+app.globals.plexRotOffset)                    
                app.encode_plex('occl_info') #using to pass occl seed
                app.encode_plex(app.globals.occl_seeds[occl_loc]+app.globals.plexStimIDOffset)
                app.encode_plex('occlmode') #0 for none, 1 for lines
                if app.globals.occl_show[occl_loc] == 1:
                    app.encode_plex(1+app.globals.plexStimIDOffset)
                    app.encode_plex('occlshape')
                    app.encode_plex(int(app.globals.all_occl_num_lines[occl_loc])+app.globals.plexStimIDOffset)
                    app.encode_plex('line_width')#occluder line width
                    app.encode_plex(int(round(app.globals.all_occl_line_widths[occl_loc]*app.globals.plexFloatMult + app.globals.plexFloatMult)))                             
                else:
                    app.encode_plex(0+app.globals.plexStimIDOffset)
                    app.encode_plex('occlshape')
                    app.encode_plex(0+app.globals.plexStimIDOffset)
                    app.encode_plex('line_width')#occluder line width
                    app.encode_plex(0+app.globals.plexStimIDOffset)

                app.encode('stimid')
                app.encode(app.globals.pick_stims[samp_loc2]+app.globals.plexStimIDOffset)
                app.encode('rotid')
                app.encode(app.globals.pick_rots[samp_loc2]+app.globals.plexRotOffset)
                app.encode('occl_info') #using to pass occl seed
                app.encode(app.globals.occl_seeds[occl_loc]+app.globals.plexStimIDOffset)
                app.encode('occlmode') #0 for none, 1 for lines
                if app.globals.occl_show[occl_loc] == 1:
                    app.encode(1+app.globals.plexStimIDOffset)
                    app.encode('occlshape')
                    app.encode(int(app.globals.all_occl_num_lines[occl_loc])+app.globals.plexStimIDOffset)
                    app.encode('line_width')#occluder line width
                    app.encode(int(round(app.globals.all_occl_line_widths[occl_loc]*app.globals.plexFloatMult + app.globals.plexFloatMult)))                              
                else:
                    app.encode(0+app.globals.plexStimIDOffset)
                    app.encode('occlshape')
                    app.encode(0+app.globals.plexStimIDOffset)
                    app.encode('line_width')#occluder line width
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
                # this should adjust the second stim window based on eccentricity 
                # if stim2winsz was not entered manually
                # (for foveal RFs, may be necessary to manually select this window)
                if P['stim2winsz'] == 0:
                    rfx,rfy = app.globals.xTestStim, app.globals.yTestStim
                    rfr = ((rfx**2)+(rfy**2))**0.5
                    rfz = min_e + (100 - min_e) * rfr / ((app.fb.w+app.fb.h)/2.0)
                    # Set a parameter value that's the actual window size to use
                    # this trial, so it's saved in data file.
                    P['stim2_winsize'] = int(round(P['win_size'] + rfz))
                    stim2win = FixWin(app.globals.xTestStim, app.globals.yTestStim, P['stim2_winsize'], app)
                    stim2win.draw(color='green')
                    aa = stim2win.on(4)# aa = stim2win.on(3) TN changed 09162017
                else:
                    stim2win = FixWin(app.globals.xTestStim, app.globals.yTestStim, P['stim2winsz'], app)
                    stim2win.draw(color='green')
                    aa = stim2win.on(4)# aa = stim2win.on(3) TN changed 09162017
                        
                app.encode_plex('extra')
                app.encode_plex(step_loc+app.globals.plexStimIDOffset)
                app.encode('extra') 
                app.encode(step_loc+app.globals.plexStimIDOffset)

                stepsize = app.globals.stepsizeList[step_loc]

                # 9/15/20 Erin - added to fix divide by 0 errors when using one RF or RF Xs or Ys are the same 
                if P['RF1_X']==P['RF2_X']:
                    direction_x = 0
                else:
                    direction_x = (P['RF2_X']-P['RF1_X'])/abs(P['RF2_X']-P['RF1_X'])
                if P['RF1_Y']==P['RF2_Y']:
                    direction_y = 0
                else:
                    direction_y = (P['RF2_Y']-P['RF1_Y'])/abs(P['RF2_Y']-P['RF1_Y'])
                
                # a bit smaller to account for stim size, it should not move out of the slit_w
                moveto_x_total = abs(math.sin(app.globals.rotate_angle_rad))*(app.globals.RFdist+min(app.globals.size_RF1,app.globals.size_RF2))
                moveto_y_total = abs(math.cos(app.globals.rotate_angle_rad))*(app.globals.RFdist+min(app.globals.size_RF1,app.globals.size_RF2))
                if (P['RF1_X']>=P['RF2_X']):
                    x_lim_right = app.globals.xTestStim+moveto_x_total/2
                    x_lim_left = app.globals.xTestStim-moveto_x_total/2
                else:
                    x_lim_right = app.globals.xTestStim-moveto_x_total/2
                    x_lim_left = app.globals.xTestStim+moveto_x_total/2
                if (P['RF1_Y']>=P['RF2_Y']):
                    y_lim_top = app.globals.yTestStim+moveto_y_total/2
                    y_lim_bottom = app.globals.yTestStim-moveto_y_total/2
                else:
                    y_lim_top = app.globals.yTestStim-moveto_y_total/2
                    y_lim_bottom = app.globals.yTestStim+moveto_y_total/2
                

                # find how much to move at a time               
                moveto_x = abs(math.sin(app.globals.rotate_angle_rad))*stepsize*direction_x*app.globals.init_motion_dir
                moveto_y = abs(math.cos(app.globals.rotate_angle_rad))*stepsize*direction_y*app.globals.init_motion_dir

                # print 'motion dir now = ',app.globals.init_motion_dir 
                #print 'rf1 = ',app.globals.size_RF1,', rf2 = ',app.globals.size_RF2,', rf = ',app.globals.size
                #print 'moveto_x = ', moveto_x, ', moveto_y = ', moveto_y
                print 'xlim: ', x_lim_left, x_lim_right, ', ylim: ',y_lim_top,y_lim_bottom
                #print 'angle = ', app.globals.rotate_angle_rad
                        
                # print 'dist = ', dist, ', moveto_x_total = ', moveto_x_total, ', moveto_y_total', moveto_y_total

                app.globals.movingstim = app.globals.stim_arr[samp_loc2].clone() 

                # PZ 2.11.2020 - this *should* be RF1, and accountnig for stim size, it should not move out of the slit
                app.globals.movingstim.rmove((-1)*moveto_x_total/2*direction_x*app.globals.init_motion_dir, (-1)*moveto_y_total/2*direction_y*app.globals.init_motion_dir) 


                
                newlist = []
                newlist.append(app.globals.movingstim)
                app.globals.dlist.add(app.globals.movingstim)
                app.globals.dlist.update()
                delaytime = 0

                if(rfSprites is not None):
                        app.globals.dlist.add(rfSprites[0])
                        app.globals.dlist.add(rfSprites[1])
                        rfSprites[0].on()
                        rfSprites[1].on()
                        app.globals.dlist.update()
                
                app.globals.movingstim.on()
                
                app.globals.occl_arr[occl_loc].on()

                # moved here from lines 1216... by PZ 9/5/17 
                #turn on target windows at the same time
                targwin.draw(color='red')
                l = targwin.on(1)
                p = nontargwin.on(2)
                tj = sacwin.on(3)#09182017 TN
                #This is when secondstimulus gets shown. AP commented.20170915
                #STIM IS ON
                app.fb.sync(1)
                app.globals.dlist.update()
                app.fb.flip()
                app.udpy.display(app.globals.dlist)

                app.encode_plex(SAMPLE_ON)
                app.encode(SAMPLE_ON)

                x1=app.globals.movingstim.x
                y1=app.globals.movingstim.y
                t1=0
                t.reset()
                x_speeds = []
                y_speeds = []                

                print "trial", app.globals.ntrials
                #print "init x =", app.globals.movingstim.x
                #print "init y =", app.globals.movingstim.y

                # added to encode initial stim location EK 10/7/20
                app.encode_plex('rfx')
                app.encode_plex(int(app.globals.movingstim.x)+app.globals.plexYOffset)
                app.encode_plex('rfy')
                app.encode_plex(int(app.globals.movingstim.y)+app.globals.plexYOffset)
                app.encode('rfx')
                app.encode(int(app.globals.movingstim.x)+app.globals.plexYOffset)
                app.encode('rfy')
                app.encode(int(app.globals.movingstim.y)+app.globals.plexYOffset)
                
                print "init x = ", app.globals.movingstim.x, "init y = ", app.globals.movingstim.y

                t.reset() # PZ 9/5/2017 - reset RT timer right after 2nd stim on
                trial_duration = -1
                # timer for test stim fix reward PZ 10/11/2017
                """if P['Give_rew_for_fix_on_test?'] == 1:
                        tstim2rew = Timer ()
                        tstim2rew.reset()
                        stim2fixrew_time = P['stim2_fix_reward']
                        JuiceTimer = Timer ()# TN
                        Wait_JuiceOn = 0# TN"""
                 
                """if not (P['ShowTargWithFix']): ####Comment out .TN 20170915
                    #wait for the delay period
                    delaytime = P['delay']  
                    # wait for 2nd stimulus time (delay set by user)
                    while t.ms() < delaytime:
                        #just hold fixation for this time period
                        # if break fix, 
                        if fixwin.broke(0):
                            #turn off stimuli
                            #this next line should turn off pdiode
                            app.fb.sync(0)
                            app.globals.dlist.update()
                            #DVP took out "+ coloroffset" - ??
                            spot.off()
                            if(rfSprites is not None):
                                rfSprites[0].off()
                                rfSprites[1].off()
                            app.globals.occl_arr[occl_loc].off()
                            app.globals.dlist.update()
                            app.fb.flip()
                            app.encode_plex(EARLY_RELEASE)
                            app.encode(EARLY_RELEASE)
                            info(app, "early break")
                            con(app, "early break (%d ms)" % t2.ms(), 'red')
                            result = EARLY_RELEASE
                            app.warn_trial_incorrect(flash=None)
                            # Skip to end of trial
                            raise MonkError
                        app.idlefn()"""
                        
                    #if nothing goes on (i.e. no break fix) in the above section, go on with regular monitoring for saccades and turn on targets


                '''if P['hold_sd']>0:
                    dt=floor(random.gauss(0,P['hold_sd']))#Tomo: hold time can be flexible. TN on Oct 5 2017
                else:
                    dt=0
                if (app.globals.occl_dot_widths[occl_loc]) == max(app.globals.occl_dot_widths):# TN added 20170927
                    wait_time=(P['hold_longest']*P['fix_hold'])+dt# TN changed 20170928
                else:# Holding time corelates with increasing level of occlusion. TN on Oct 5 2017
                    wait_time=((P['hold_longest']*P['fix_hold']-P['fix_hold'])*(app.globals.occl_dot_widths[occl_loc]/max(app.globals.occl_dot_widths))+P['fix_hold'])+dt
                print(wait_time)'''
                #else:
                wait_time=P['fix_hold']

                # PZ 11/09/2017 - wait for delaytime before turning on targets - 
                # this pretty much comes from aim2behRXT_AF task
                if P['target_delaytime'] > 0:
                        while t.ms() < P['target_delaytime']:
                                # dummy flag to help with task control
                                go_on = 0
                                while not go_on and t.ms() < P['target_delaytime']:
                                    # We are waiting for the eye position to move inside the
                                    # target or nontarget windows.
                                    
                                    # 10/11/2017 PZ: give reward every X msec for fixation on 2nd stim before saccading
                                    #TN 10112017 modified. It looks that app.reward stops process. Instead of this,                     #juice_on was used. 
                                    """if P['Give_rew_for_fix_on_test?'] == 1:
                                        if tstim2rew.ms() >= stim2fixrew_time and Wait_JuiceOn == 0 and P['r_ms_test']>0 :
                                            # valve open
                                            #app.juice_drip(1,1,1)
                                            con(app, "EXTRA REWARD DROP (%d ms after 2nd stim on)" % tstim2rew.ms(), 'black') #PZ 10/16/2017
                                            app.juice_on(dobeep=1,dojuice=1) #TN 10112017
                                            JuiceTimer.reset() # Duration for valve open.
                                            Wait_JuiceOn=1 # Flag for valve open.
                                            #app.reward(multiplier=P['rmult'],dobeep=1,dojuice=1)
                                            tstim2rew.reset()
                                        app.idlefn(fast=1)
                                        JuiceT=JuiceTimer.ms()
                                        if JuiceT >= P['r_ms_test'] and Wait_JuiceOn == 1 and P['r_ms_test']>0 :
                                            # valve close
                                            app.juice_off(dobeep=0,dojuice=1)
                                            Wait_JuiceOn=0 # Flag for valve open turned off.
                                            #print 'Reward on'
                                            #print JuiceT
                                        app.idlefn(fast=1)"""
        
                                    #STIM IS MOVING
                                    app.globals.movingstim.off()
                                    newstim = newlist[len(newlist)-1].clone()
                                    #print 'newstim.x = ', newstim.x, ', newstim.y = ', newstim.y
                                    #print 'x_lim_left = ',x_lim_left,', x_lim_right = ',x_lim_right,', y_lim_bottom = ',y_lim_bottom,', y_lim_top = ',y_lim_top
                                    if newstim.x < x_lim_left or newstim.x > x_lim_right or newstim.y < y_lim_bottom or newstim.y > y_lim_top:
                                            moveto_x = (-1)*moveto_x
                                            moveto_y = (-1)*moveto_y
                                            print "turning time ", t.ms()
                                    newstim.rmove(moveto_x,moveto_y)    

                                    app.globals.dlist.add(newstim)
                                    newlist.append(newstim)                     
                                    newstim.on()
                                    app.globals.dlist.update()
                                    app.fb.flip()
                                    newstim.off()

                                    x2=newstim.x
                                    y2=newstim.y
                                    t2=t.ms()
                                    x_speeds.append(abs((x2-x1)/(t2-t1)))
                                    y_speeds.append(abs((y2-y1)/(t2-t1)))
                                    x1=x2
                                    y1=y2
                                    t1=t2
                                    
									app.globals.second_stim_shown = True #there is now data on the stim motion that we can encode at the end of the trial
                                    if fixwin.broke(0) and not TESTING:
                                            #STIM IS OFF
                                            newstim.off() # PZ 10/6/2017
                                            spot.off() ##DVP
                                            app.globals.occl_arr[occl_loc].off() #DVPDVP
                                            if(rfSprites is not None):
                                                    rfSprites[0].off()
                                                    rfSprites[1].off()
                                            app.fb.sync(0)
                                            app.globals.dlist.update()
                                            app.fb.flip()
                                            app.encode_plex(SAMPLE_OFF)
                                            app.encode(SAMPLE_OFF)
                                            
                                            final_x = newstim.x
                                            final_y = newstim.y
                                            trial_duration = t.ms()

                                            app.encode_plex(FIX_LOST)
                                            app.encode(FIX_LOST)

                                            #breakfix_flag = 1
                                            if P['breakfix_timeout_flag']==1: 
                                                    breakfix_flag = 1
                                            info(app, "early break")
                                            con(app, "EARLY BREAK (%d ms) AFTER 2ND STIM ON BEFORE TARGETS ON" % t.ms(), 'red')
                                            con(app, "SPEED = %d" % step_loc, 'black') # PZ 9/25/17
                                            con(app, "WIDTH = %f" % app.globals.all_occl_line_widths[occl_loc], 'black') # PZ 9/25/17
                                            con(app, "NUM = %f" % app.globals.all_occl_num_lines[occl_loc], 'black') # PZ 9/25/17
                                            result = BREAK_FIX
                                            app.warn_trial_incorrect(flash=None)
                                            go_on = 1
                                            raise MonkError
                                                # Skip to end of t  % to here TN added 09162017 From
                                    app.idlefn(fast=1)#TN. 09162017
        
        
                # PZ 11/09/2017 - after delaytime is over, turn the targets and proceed with task
                        t2_on = 0 #TN added Nov132017
                else:   
                    target1.on()#Moved one step left .TN
                    target2.on()#Moved one step left .TN
                    t2_on = 1#Moved one step left .TN
                    app.globals.dlist.update()#Moved one step left .TN
                    app.fb.flip()#Moved one step left .TN
                    app.encode_plex('targets_on')#Moved one step left .TN
                    app.encode('targets_on')#Moved one step left .TN
                    app.udpy.display(app.globals.dlist)#Moved one step left .TN
                    info(app, "waiting target acquisition")#Moved one step left .TN
                    app.idlefn()#Moved one step left .TN

                # dummy flag to help with task control
                go_on = 0

                while not go_on:
                    # We are waiting for the eye position to move inside the
                    # target or nontarget windows.

                    # 10/11/2017 PZ: give reward every X msec for fixation on 2nd stim before saccading
                    #TN 10112017 modified. It looks that app.reward stops process. Instead of this,                     #juice_on was used. 
                    """if P['Give_rew_for_fix_on_test?'] == 1:
                        if tstim2rew.ms() >= stim2fixrew_time and Wait_JuiceOn == 0 and P['r_ms_test']>0 :
                        # valve open
                        #app.juice_drip(1,1,1)
                        con(app, "EXTRA REWARD DROP (%d ms after 2nd stim on)" % tstim2rew.ms(), 'black') #PZ 10/16/2017
                        app.juice_on(dobeep=1,dojuice=1) #TN 10112017
                        JuiceTimer.reset() # Duration for valve open.
                        Wait_JuiceOn=1 # Flag for valve open.
                        #app.reward(multiplier=P['rmult'],dobeep=1,dojuice=1)
                        tstim2rew.reset()
                    app.idlefn(fast=1)
                    JuiceT=JuiceTimer.ms()
                    if JuiceT >= P['r_ms_test'] and Wait_JuiceOn == 1 and P['r_ms_test']>0 :
                        # valve close
                        app.juice_off(dobeep=0,dojuice=1)
                        Wait_JuiceOn=0 # Flag for valve open turned off.
                        #print 'Reward on'
                        #print JuiceT
                    app.idlefn(fast=1)"""

                    #STIM IS MOVING
                    app.globals.movingstim.off()
                    newstim = newlist[len(newlist)-1].clone()
                    #print 'newstim.x = ', newstim.x, ', newstim.y = ', newstim.y
                    #print 'x_lim_left = ',x_lim_left,', x_lim_right = ',x_lim_right,', y_lim_bottom = ',y_lim_bottom,', y_lim_top = ',y_lim_top

                    if newstim.x < x_lim_left or newstim.x > x_lim_right or newstim.y < y_lim_bottom or newstim.y > y_lim_top:
                            moveto_x = (-1)*moveto_x
                            moveto_y = (-1)*moveto_y
                            print "turning time ", t.ms()
                    newstim.rmove(moveto_x,moveto_y) 

                    app.globals.dlist.add(newstim)
                    newlist.append(newstim)                     
                    newstim.on()
                    if t2_on==0: #TN added Nov132017
                        target1.on()#
                        target2.on()#
                        t2_on = 1#
                        app.encode_plex('targets_on')#
                        app.encode('targets_on')#
                        info(app, "waiting target acquisition")#

                    app.globals.dlist.update()                     
                    app.fb.flip()
                    newstim.off()

                    x2=newstim.x
                    y2=newstim.y
                    t2=t.ms()
                    #print "x speed", (x2-x1)/(t2-t1)
                    #print "y speed", (y2-y1)/(t2-t1)
                    x_speeds.append(abs((x2-x1)/(t2-t1)))
                    y_speeds.append(abs((y2-y1)/(t2-t1)))
                    x1=x2
                    y1=y2
                    t1=t2
					app.globals.second_stim_shown = True #there is now data on the stim motion that we can encode at the end of the trial                         
   
                    if fixwin.broke(0):
                        # turn off the 2nd stimulus stimulus #
                        pstime = t.ms()# Store possible saccade start time. # TN added 09162017 From here
                        pbtime = t2.ms()# Store possible break time. # TN added 09162017 From here                      
                        #STIM IS OFF
                        newstim.off() # PZ 10/6/2017
                        spot.off() ##DVP
                        app.globals.occl_arr[occl_loc].off() #DVPDVP
                        if(rfSprites is not None):
                            rfSprites[0].off()
                            rfSprites[1].off()
                        app.fb.sync(0)
                        app.globals.dlist.update()
                        app.fb.flip()
                        app.encode_plex(SAMPLE_OFF)
                        app.encode(SAMPLE_OFF)
                        
                        final_x = newstim.x
                        final_y = newstim.y
                        trial_duration = t.ms()

                        if P['fix_hold'] > 0 and pstime < wait_time:# Fixation failure. TN added 09162017 From here
                            app.encode_plex(FIX_LOST)
                            app.encode(FIX_LOST)
                            breakfix_flag = 1
                            info(app, "early break")
                            con(app, "early break after stim on (%d ms)" % pstime, 'red')
                            con(app, "SPEED = %d" % step_loc, 'black') # PZ 9/25/17
                            con(app, "WIDTH = %f" % app.globals.all_occl_line_widths[occl_loc], 'black') # PZ 9/25/17
                            con(app, "NUM = %f" % app.globals.all_occl_num_lines[occl_loc], 'black') # PZ 9/25/17
                            result = BREAK_FIX
                            app.warn_trial_incorrect(flash=None)
                            raise MonkError
                            # Skip to end of t  % to here TN added 09162017 From
                        go_on = 1
                    #We use the maxrt line here
                    if P['maxrt'] > 0 and t.ms() > P['maxrt']:
                        info(app, "no target saccade in max rt")
                        con(app, "no saccade in max rt", 'blue')
                        con(app, "SPEED = %d" % step_loc, 'black') # PZ 9/25/17 
                        con(app, "WIDTH = %f" % app.globals.all_occl_line_widths[occl_loc], 'black') # PZ 9/25/17
                        con(app, "NUM = %f" % app.globals.all_occl_num_lines[occl_loc], 'black') # PZ 9/25/17
                        result = NO_RESP
                        
                        #STIM IS OFF
                        newstim.off() # PZ 10/6/2017
                        spot.off() ##DVP
                        app.globals.occl_arr[occl_loc].off() #DVPDVP
                        if(rfSprites is not None):
                            rfSprites[0].off()
                            rfSprites[1].off()
                        app.fb.sync(0)
                        app.globals.dlist.update()
                        app.fb.flip()
                        app.encode_plex(SAMPLE_OFF)
                        app.encode(SAMPLE_OFF)

                        final_x = newstim.x
                        final_y = newstim.y
                        trial_duration = t.ms()
                        
                        app.encode_plex(NO_RESP)
                        app.encode(NO_RESP)
                        beep(2000,100)
                        app.globals.natmpt = app.globals.natmpt+1 #attempt only counts if it is either error response or correct.
                        raise MonkError

                    app.idlefn(fast=1)#TN. 09162017
                go_on3 = 1# At this moment, we don't know that is current status a fixation break or saccade start. TN added 09162017 From here
                while not go_on3:
                    if P['travel_t'] == 0:#Just let it go. 
                        go_on3 = 1
                        break # Now we know this is saccade.
                    if sacwin.broke(3):# quick eyemovement
                        # Test that this break is deviated fixation or saccadic eye movement
                        # If eye goes over outerwindow within 50ms #
                        if (t.ms()<(pstime+P['travel_t'])):
                            go_on3 = 1
                
                            break # Now we know this is saccade.
                        app.encode_plex(FIX_LOST)
                        app.encode(FIX_LOST)
                        info(app, "early break")
                        con(app, "miss detection (%d ms)" % t.ms(), 'red')
                        con(app, "SPEED = %d" % step_loc, 'black') # PZ 9/25/17 
                        con(app, "WIDTH = %f" % app.globals.all_occl_line_widths[occl_loc], 'black') # PZ 9/25/17
                        con(app, "NUM = %f" % app.globals.all_occl_num_lines[occl_loc], 'black') # PZ 9/25/17
                        result = BREAK_FIX
                        app.warn_trial_incorrect(flash=None)
                        raise MonkError#
                        # Skip to end of t
                    app.idlefn(fast=1)# 09162017## To here. TN
                go_on2 = 0  

                while not go_on2:
                    while not targwin.inside(1) and not nontargwin.inside(2) and not TESTING:
                        ###DVP ADDITIONS TO HANDLE SACCADE TO STIM ON THE WAY TO TARGET
                        if fixwin.broke(0):
                            #print 'fix broken!!'
                            if stim2win.inside(4):  #<- This code does not allow us to put test stimulus arooud horizontal meridian.  TN commented out 09162017 From here
                                # print 'inside 2nd stim window!!'
                                app.encode_plex(EARLY_RELEASE)
                                app.encode(EARLY_RELEASE)
                                info(app, "early break to stim")
                                con(app, "early break to stim (%d ms)" % t2.ms(), 'red')
                                result = EARLY_RELEASE
                                app.warn_trial_incorrect(flash=None)
                                # Skip to end of trial
                                raise MonkError
                        # Turn on target 2 after the hint duration
                        app.idlefn()     ## To here. TN'''
                        #We use the maxrt line here
                        if P['maxrt'] > 0 and t.ms() > P['maxrt']:
                            info(app, "no target saccade")
                            con(app, "no saccade", 'blue')
                            con(app, "SPEED = %d" % step_loc, 'black') # PZ 9/25/17 
                            con(app, "WIDTH = %f" % app.globals.all_occl_line_widths[occl_loc], 'black') # PZ 9/25/17
                            con(app, "NUM = %f" % app.globals.all_occl_num_lines[occl_loc], 'black') # PZ 9/25/17
                            result = NO_RESP
                            app.encode_plex(NO_RESP)
                            app.encode(NO_RESP)
                            beep(2000,100)
                            app.globals.natmpt = app.globals.natmpt+1
                            raise MonkError
                        app.idlefn(fast=1)#TN. 09162017
                    # At this point, the targwin.inside or nontargwin.inside returned 1 
                    # (meaning eye is inside window).  
                    # if nontargwin is the one that the animal saccaded to its an error
                    if nontargwin.inside(2)== 1:
                        #import pdb; pdb.set_trace()

                        rxtime = t.ms()#-target_delaytime
                        app.encode_plex(rxtime + app.globals.plexStimIDOffset)
                        app.encode(rxtime + app.globals.plexStimIDOffset)
                        info(app, "Reaction Time")
                        con(app, "Reaction Time (%d ms)" % rxtime, 'black')
                        con(app, "SPEED = %d" % step_loc, 'black') # PZ 9/25/17 
                        con(app, "WIDTH = %f" % app.globals.all_occl_line_widths[occl_loc], 'black') # PZ 9/25/17
                        con(app, "NUM = %f" % app.globals.all_occl_num_lines[occl_loc], 'black') # PZ 9/25/17
                        info(app, "Wrong target saccade")
                        con(app, "Wrong saccade", 'blue')
                        result = WRONG_RESP
                        app.encode_plex(WRONG_RESP)
                        app.encode(WRONG_RESP)
                        beep(2000,100)
                        app.globals.natmpt = app.globals.natmpt+1
                        # DVP commented out nov 2015, different buffers in this task
                        #if currentcase == 1:
                        #   app.globals.nmatchtrials = app.globals.nmatchtrials + 1
                        #else:
                        #   app.globals.nnonmatchtrials = app.globals.nnonmatchtrials + 1
                        raise MonkError
                    app.idlefn(fast=1)#TN. 09162017
                    # Sometimes if the spot has just come
                    # on and the subject is in the process of saccading across
                    # the screen, the eye position will go through the targwin.
                    # Only count this as acquiring fixation if the eye stays in
                    # the window for "targwait" milliseconds.
                    t2.reset()
                    # First, assume we will continue if eye stays in window
                    #import pdb; pdb.set_trace()
                    go_on2 = 1

                    while t2.ms() < P['targwait']:
                        # app.idlefn() TN commented out 09162017
                        if not targwin.inside(1) and not TESTING:
                            # If at any time during the targwait the eye
                            # moves back out of the window, go back to waiting
                            # for the eye to enter the window again.
                            info(app, "passthrough")
                            go_on2 = 0 # TN. changed 20170915
                            # This resets targwin.inside back to zero
                            targwin.reset(0)
                            # This exits the innermost while loop, and sends
                            # us back to the top of the "while not go_on"
                            # loop
                            break
                        app.idlefn(fast=1)#TN. 09162017
                # Now, target has been acquired.        
                targwin.draw(color='blue') # Blue is our "active" color
                nontargwin.clear()
                target2.off()
                app.globals.dlist.update()
                app.fb.flip()

                # Now hold target for target hold duration
                rxtime = t.ms()-P['targwait']#-target_delaytime
                app.encode_plex(rxtime + app.globals.plexStimIDOffset)
                app.encode(rxtime + app.globals.plexStimIDOffset)
                info(app, "Reaction Time")
                con(app, "Reaction Time (%d ms)" % rxtime, 'black')
                con(app, "SPEED = %d" % step_loc, 'black') # PZ 9/25/17 
                con(app, "WIDTH = %f" % app.globals.all_occl_line_widths[occl_loc], 'black') # PZ 9/25/17
                con(app, "NUM = %f" % app.globals.all_occl_num_lines[occl_loc], 'black') # PZ 9/25/17
                '''t.reset()
                while t.ms() < P['targ_hold']:
                    if targwin.broke(1) and not TESTING:
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
                    app.idlefn()'''

                ################################
                # If you are here then the trial is correct
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
                app.encode(USER_ABORT)
                app.fb.sync(0)
        except MonkError:
                # Any of the MonkError exceptions will land you here.  The
                # trial counter is incremented and the seqcorrect counter
                # is reset.
                app.globals.ntrials = app.globals.ntrials + 1
                
                app.globals.init_motion_dir = (-1)**app.globals.ntrials
                app.globals.seqcorrect = 0
                if((result != WRONG_RESP and result != NO_RESP) and P['redo_breakfix'] == 1):
                        if(P['redo_immediately'] == 1):
                                app.globals.stimorder.insert(0,location)
                        elif (P['redo_immediately'] == 2): # PZ 10/19/2017 added option to redo immediately on about half of the trials at random
                                x = random.choice([0,1])    
                                if x == 1:
                                        app.globals.stimorder.insert(0,location)
                                        con(app, ":::will re-do immediately:::", 'red')
                                else:
                                        app.globals.stimorder.append(location)
                                        random.shuffle(app.globals.stimorder)
                                        con(app, ":::will not re-do immediately:::", 'red')
                        else:
                                app.globals.stimorder.append(location)
                                random.shuffle(app.globals.stimorder)
                                #print location
                                #print app.globals.stimorder
                if result == WRONG_RESP:
                        """if samp_loc2 == 0:
                            app.globals.condition1.append(0)
                            if len(app.globals.condition1) > P['Reward Buffer Size']:
                                app.globals.condition1.pop(0)
                            app.globals.condAA.append(0) # 04/04/17 ramp reward stuff
                            if len(app.globals.condAA) > P['Reward Buffer Size']:
                                app.globals.condAA.pop(0)
                        if samp_loc2 == 1:
                            app.globals.condition2.append(0)
                            if len(app.globals.condition2) > P['Reward Buffer Size']:
                                app.globals.condition2.pop(0)
                            app.globals.condAA.append(0) # 04/04/17 ramp reward stuff
                            if len(app.globals.condAA) > P['Reward Buffer Size']:
                                app.globals.condAA.pop(0)
                        if samp_loc2 == 2:
                            app.globals.condition3.append(0)
                            if len(app.globals.condition3) > P['Reward Buffer Size']:
                                app.globals.condition3.pop(0)
                            app.globals.condBB.append(0) # 04/04/17 ramp reward stuff
                            if len(app.globals.condBB) > P['Reward Buffer Size']:
                                app.globals.condBB.pop(0)
                        if samp_loc2 == 3:
                            app.globals.condition4.append(0)
                            if len(app.globals.condition4) > P['Reward Buffer Size']:
                                app.globals.condition4.pop(0)
                            app.globals.condBB.append(0) # 04/04/17 ramp reward stuff
                            if len(app.globals.condBB) > P['Reward Buffer Size']:
                                app.globals.condBB.pop(0)"""
                                
                        # PZ aug 6 2018 - percents for slit vs no slit
                        if (app.globals.occl_show[occl_loc] == 1):
                            app.globals.condition_occl.append(0)
                            if len(app.globals.condition_occl) > P['Reward Buffer Size']:
                                app.globals.condition_occl.pop(0)
                        else:
                            app.globals.condition_nooccl.append(0)
                            if len(app.globals.condition_nooccl) > P['Reward Buffer Size']:
                                app.globals.condition_nooccl.pop(0)                           

                        # PZ aug 16 2018 - percents for M/NM for slit vs no slit
                        if (app.globals.occl_show[occl_loc] == 0):
                            if t_loc == 1:
                                app.globals.condition_occl_m.append(0)
                                if len(app.globals.condition_occl_m) > P['Reward Buffer Size']:
                                    app.globals.condition_occl_m.pop(0)
                            else:
                                app.globals.condition_occl_nm.append(0)
                                if len(app.globals.condition_occl_nm) > P['Reward Buffer Size']:
                                    app.globals.condition_occl_nm.pop(0)
                        else:
                            if t_loc == 1:
                                app.globals.condition_nooccl_m.append(0)
                                if len(app.globals.condition_nooccl_m) > P['Reward Buffer Size']:
                                    app.globals.condition_nooccl_m.pop(0)
                            else:
                                app.globals.condition_nooccl_nm.append(0)
                                if len(app.globals.condition_nooccl_nm) > P['Reward Buffer Size']:
                                    app.globals.condition_nooccl_nm.pop(0)

                        # PZ aug 9 2018 - calculate M/NM overall
                        if t_loc == 1:
                            app.globals.condAA.append(0) # 04/04/17 ramp reward stuff
                            if len(app.globals.condAA) > P['Reward Buffer Size']:
                                app.globals.condAA.pop(0)
                        else:
                            app.globals.condBB.append(0) # 04/04/17 ramp reward stuff
                            if len(app.globals.condBB) > P['Reward Buffer Size']:
                                app.globals.condBB.pop(0)
                                
                        if(P['redo_errors'] == 1):
                                if(P['redo_immediately'] == 1):
                                        app.globals.stimorder.insert(0,location)
                                elif (P['redo_immediately'] == 2): # PZ 10/19/2017 added option to redo immediately on about half of the trials at random
                                        x = random.choice([0,1])    
                                        if x == 1:
                                                app.globals.stimorder.insert(0,location)
                                        else:
                                                app.globals.stimorder.append(location)
                                                random.shuffle(app.globals.stimorder)
                                else:
                                        app.globals.stimorder.append(location)
                                        random.shuffle(app.globals.stimorder)
                        app.globals.attempted_trial = 0
                        if(t_loc == 1):
                                clk_num = P['numdrops_err_match']
                        else:
                                clk_num = P['numdrops_err_non_match']
                        if app.globals.ntrials > -1:
                                app.globals.pctbuffer2.append(result)
                                # Average the performance over the past X trials.
                                if((app.globals.ntrials+1) < P['Reward Buffer Size']) :
                                        #recent2=100*app.globals.ncorrect/app.globals.ntrials
                                        attmpt_num2 = app.globals.pctbuffer2.count(CORRECT_RESPONSE)+app.globals.pctbuffer2.count(WRONG_RESP)+ \
                                                                app.globals.pctbuffer2.count(EARLY_RELEASE)
                                        if attmpt_num2 > 0:
                                                recentbeh2 = 100*app.globals.pctbuffer2.count(CORRECT_RESPONSE)/attmpt_num2
                                        else:
                                                recentbeh2 = 0.0
                                else:
                                        app.globals.lastX2 = app.globals.pctbuffer2[len(app.globals.pctbuffer2) - P['Reward Buffer Size']::]
                                        #recent2=100*app.globals.lastX2.count(CORRECT_RESPONSE)/len(app.globals.lastX2)
                                        attmpt_num2 = (app.globals.lastX2.count(CORRECT_RESPONSE)+app.globals.lastX2.count(WRONG_RESP)+ \
                                                                app.globals.lastX2.count(EARLY_RELEASE))
                                        if attmpt_num2 > 0:
                                                recentbeh2 = 100*app.globals.lastX2.count(CORRECT_RESPONSE)/attmpt_num2
                                        else:
                                                recentbeh = 0.0
                        a = int(P['rew_prob']*100)*[1]+(100-int(P['rew_prob']*100))*[0]
                        juice_go = random.choice(a)
                        while clk_num > 0:
                                if juice_go == 1:
                                   app.reward(multiplier=P['rmult'],dobeep=1,dojuice=1)
                                else:
                                    app.reward(multiplier=P['rmult'],dobeep=1,dojuice=0)
                                app.idlefn(50)#time between juice drops
                                clk_num = clk_num-1
                                
                con(app, "Current condition: %d" % (samp_loc2+1), 'black')

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
                app.encode_plex(REWARD)
                app.encode(REWARD)
                # Increment the sequence correct counter
                app.globals.seqcorrect=app.globals.seqcorrect + 1
                app.globals.attempted_trial = 0
                if app.globals.ntrials > -1:
                                app.globals.pctbuffer2.append(result)
                                # Average the performance over the past X trials.
                                if((app.globals.ntrials+1) < P['Reward Buffer Size']) :
                                        #recent2=100*app.globals.ncorrect/app.globals.ntrials
                                        attmpt_num2 = app.globals.pctbuffer2.count(CORRECT_RESPONSE)+app.globals.pctbuffer2.count(WRONG_RESP)+ \
                                                                app.globals.pctbuffer2.count(EARLY_RELEASE)
                                        if attmpt_num2 > 0:
                                                recentbeh2 = 100*app.globals.pctbuffer2.count(CORRECT_RESPONSE)/attmpt_num2
                                        else:
                                                recentbeh2 = 0.0
                                else:
                                        app.globals.lastX2 = app.globals.pctbuffer2[len(app.globals.pctbuffer2) - P['Reward Buffer Size']::]
                                        #recent2=100*app.globals.lastX2.count(CORRECT_RESPONSE)/len(app.globals.lastX2)
                                        attmpt_num2 = (app.globals.lastX2.count(CORRECT_RESPONSE)+app.globals.lastX2.count(WRONG_RESP)+ \
                                                                app.globals.lastX2.count(EARLY_RELEASE))
                                        if attmpt_num2 > 0:
                                                recentbeh2 = 100*app.globals.lastX2.count(CORRECT_RESPONSE)/attmpt_num2
                                        else:
                                                recentbeh2 = 0.0

                # PZ aug 6 2018 - percents for slit vs no slit

                if (app.globals.occl_show[occl_loc] == 1):
                    app.globals.condition_occl.append(1)
                    if len(app.globals.condition_occl) > P['Reward Buffer Size']:
                        app.globals.condition_occl.pop(0)
                else:
                    app.globals.condition_nooccl.append(1)
                    if len(app.globals.condition_nooccl) > P['Reward Buffer Size']:
                        app.globals.condition_nooccl.pop(0)
                
                condition_occl = [0] * 2
                cond_sum_occl = [0] * 2

                if len(app.globals.condition_occl) == 0:
                        condition_occl[0] = 0
                else:
                        for i in range(len(app.globals.condition_occl)):
                                cond_sum_occl[0] = cond_sum_occl[0] + app.globals.condition_occl[i]
                        condition_occl[0] = 100 * cond_sum_occl[0] / len(app.globals.condition_occl)

                if len(app.globals.condition_nooccl) == 0:
                        condition_occl[1] = 0
                else:
                        for i in range(len(app.globals.condition_nooccl)):
                                cond_sum_occl[1] = cond_sum_occl[1] + app.globals.condition_nooccl[i]
                        condition_occl[1] = 100 * cond_sum_occl[1] / len(app.globals.condition_nooccl)


                # PZ aug 9 2018 - calculate M/NM overall
                if t_loc == 1:
                    app.globals.condAA.append(1) # 04/04/17 ramp reward stuff
                    if len(app.globals.condAA) > P['Reward Buffer Size']:
                        app.globals.condAA.pop(0)
                else:
                    app.globals.condBB.append(1) # 04/04/17 ramp reward stuff
                    if len(app.globals.condBB) > P['Reward Buffer Size']:
                        app.globals.condBB.pop(0)

                # PZ aug 6 2018 - percents for M/NM for slit vs no slit

                if (app.globals.occl_show[occl_loc] == 1):
                    if t_loc == 1:
                        app.globals.condition_occl_m.append(1)
                        if len(app.globals.condition_occl_m) > P['Reward Buffer Size']:
                            app.globals.condition_occl_m.pop(0)
                    else:
                        app.globals.condition_occl_nm.append(1)
                        if len(app.globals.condition_occl_nm) > P['Reward Buffer Size']:
                            app.globals.condition_occl_nm.pop(0)
                else:
                    if t_loc == 1:
                        app.globals.condition_nooccl_m.append(1)
                        if len(app.globals.condition_nooccl_m) > P['Reward Buffer Size']:
                            app.globals.condition_nooccl_m.pop(0)
                    else:
                        app.globals.condition_nooccl_nm.append(1)
                        if len(app.globals.condition_nooccl_nm) > P['Reward Buffer Size']:
                            app.globals.condition_nooccl_nm.pop(0)
                condition4_occl = [0] * 4
                cond4_sum_occl = [0] * 4
                if len(app.globals.condition_occl_m) == 0:
                        condition4_occl[0] = 0
                else:
                        for i in range(len(app.globals.condition_occl_m)):
                                cond4_sum_occl[0] = cond4_sum_occl[0] + app.globals.condition_occl_m[i]
                        condition4_occl[0] = 100 * cond4_sum_occl[0] / len(app.globals.condition_occl_m)
                if len(app.globals.condition_occl_nm) == 0:
                        condition4_occl[1] = 0
                else:
                        for i in range(len(app.globals.condition_occl_nm)):
                                cond4_sum_occl[1] = cond4_sum_occl[1] + app.globals.condition_occl_nm[i]
                        condition4_occl[1] = 100 * cond4_sum_occl[1] / len(app.globals.condition_occl_nm)
                if len(app.globals.condition_nooccl_m) == 0:
                        condition4_occl[2] = 0
                else:
                        for i in range(len(app.globals.condition_nooccl_m)):
                                cond4_sum_occl[2] = cond4_sum_occl[2] + app.globals.condition_nooccl_m[i]
                        condition4_occl[2] = 100 * cond4_sum_occl[2] / len(app.globals.condition_nooccl_m)
                if len(app.globals.condition_nooccl_nm) == 0:
                        condition4_occl[3] = 0
                else:
                        for i in range(len(app.globals.condition_nooccl_nm)):
                                cond4_sum_occl[3] = cond4_sum_occl[3] + app.globals.condition_nooccl_nm[i]
                        condition4_occl[3] = 100 * cond4_sum_occl[3] / len(app.globals.condition_nooccl_nm)



                con(app, "Current condition: %d" % (samp_loc2+1), 'black')

                # PZ aug 6 2018
                con(app, "Length of buffers: %d %d" % (len(app.globals.condition_occl),len(app.globals.condition_nooccl)), 'black')
                con(app, "Correct in buffer: %d %d" % (cond_sum_occl[0],cond_sum_occl[1]), 'black')
                #con(app, "Overall: Slit:%.0f%% No Slit:%.0f%%"  % (condition_slit[0],condition_slit[1]), 'black')

                # show M/NM performance as well PZ
                condition_mnm = [0] * 2
                cond_sum_mnm = [0] * 2
                if len(app.globals.condAA) == 0:
                    condition_mnm[0] = 0
                else:
                    for i in range(len(app.globals.condAA)):
                        cond_sum_mnm[0] = cond_sum_mnm[0] + app.globals.condAA[i]
                    condition_mnm[0] = 100 * cond_sum_mnm[0] / len(app.globals.condAA)
                if len(app.globals.condBB) == 0:
                    condition_mnm[1] = 0
                else:
                    for i in range(len(app.globals.condBB)):
                        cond_sum_mnm[1] = cond_sum_mnm[1] + app.globals.condBB[i]
                    condition_mnm[1] = 100 * cond_sum_mnm[1] / len(app.globals.condBB)
                con(app, "Overall: Match:%.0f%% N-Match:%.0f%%" % (condition_mnm[0],condition_mnm[1]), 'black')

                # PZ 8/16/18 show m/nm performance for slit/no slit
                con(app, "Occl: Overall:%.0f%% (M:%.0f%% N-M:%.0f%%)" % (condition_occl[0],condition4_occl[0],condition4_occl[1]), 'black')
                con(app, "No Occl: Overall:%.0f%% (M:%.0f%% N-M:%.0f%%)" % (condition_occl[1],condition4_occl[2],condition4_occl[3]), 'black')


                #setting up different reward modes:
                #mode 1: standard (set match/nonmatch rewards)
                #if P['reward_mode'] == 1:
                if(t_loc == 1):
                    if (app.globals.occl_show[occl_loc] == 1):
                        clk_num = P['numdrops_match_occl']
                    else:
                        clk_num = P['numdrops_match_nooccl']
                else:
                    if (app.globals.occl_show[occl_loc] == 1):
                        clk_num = P['numdrops_non_match_occl']
                    else:
                        clk_num = P['numdrops_non_match_nooccl']

                # If needed, increase reward with occlusion PZ 10/27/17
#               if P['Incr_rew_with_occl?'] == 1:
                    # if yes, use m/nm correct reward as reward for unoccluded
                    # and, increase by 1 drop for 0.1 occl level, by 2 drops for 0.2, and so on
#                   clk_num = clk_num + int(app.globals.occl_dot_widths[occl_loc]*10)
                    # print 'new # drops = ', clk_num

                # Without arguments this call dispenses a reward of size
                # 'dropsize' with a variance of 'dropvar' (both specified
                # in monk_params). The multiplier argument multiplies the
                # "standard" reward by whatever value is passed in.
                a = int(P['rew_prob']*100)*[1]+(100-int(P['rew_prob']*100))*[0]
                juice_go = random.choice(a)
                con(app, "juice_go ::: %d" % (juice_go), 'black')
                # print '# drops = ', clk_num
                while clk_num > 0:
                    if juice_go == 1:
                        app.reward(multiplier=P['rmult'],dobeep=1,dojuice=1)
                    else:
                        app.reward(multiplier=P['rmult'],dobeep=1,dojuice=0)
                    app.idlefn(50)#time between juice drops
                    clk_num = clk_num-1

                # PZ 10/10/2017 give extra reward for unoccluded stims
                #if app.globals.occl_dot_widths[occl_loc] == 0.0:
                    #clk_num_2 = P['extra_numdrops_unoccluded']
                    #while clk_num_2 > 0:
                        #if juice_go == 1:
                            #app.reward(multiplier=P['rmult'],dobeep=1,dojuice=1)
                        #else:
                            #app.reward(multiplier=P['rmult'],dobeep=1,dojuice=0)
                        #app.idlefn(50)#time between juice drops
                        #clk_num_2 = clk_num_2-1


                # Reporting stuff, variables returned to RunTrial
                app.globals.natmpt = app.globals.natmpt+1
                app.globals.ncorrect = app.globals.ncorrect + 1
                app.globals.ntrials = app.globals.ntrials + 1
                
                app.globals.init_motion_dir = (-1)**app.globals.ntrials # 3/5/20 PZ

        
        # # # # # # # # # # # # # # # # # #
        # Cleanup
        # # # # # # # # # # # # # # # # # #
   #      if app.globals.occl_show[occl_loc] == 1:
            # print "occlusion"
   #      if app.globals.occl_show[occl_loc] == 0:
            # print "no occlusion"
        #print "min", time_min
        #print "max", time_max
        #print "avg", sum(times)/(len(times))
		if app.globals.second_stim_shown == True:
	        avg_x_speed = sum(x_speeds)/(len(x_speeds))
    	    avg_y_speed = sum(y_speeds)/(len(y_speeds))
    	    print "final x =", final_x, "final y =", final_y
    	    print "trial duration =", trial_duration
    	    print "speed =", stepsize
    	    print "avg x speed", avg_x_speed
    	    print "avg y speed", avg_y_speed
    	    print

    	    # added to encode final stim location EK 10/7/20
    	    app.encode_plex('rfx')
    	    app.encode_plex(int(final_x)+app.globals.plexYOffset)
    	    app.encode_plex('rfy')
    	    app.encode_plex(int(final_y)+app.globals.plexYOffset)
    	    app.encode('rfx')
    	    app.encode(int(final_x)+app.globals.plexYOffset)
    	    app.encode('rfy')
    	    app.encode(int(final_y)+app.globals.plexYOffset)
    	    # encode average x and y speed EK 10/19/20
    	    app.encode_plex('extra')
    	    app.encode_plex(int(round(avg_x_speed*app.globals.plexFloatMult + app.globals.plexFloatMult)))    
    	    app.encode_plex('extra')
    	    app.encode_plex(int(round(avg_y_speed*app.globals.plexFloatMult + app.globals.plexFloatMult)))    
     	    app.encode('extra')
     	    app.encode(int(round(avg_x_speed*app.globals.plexFloatMult + app.globals.plexFloatMult)))    
     	    app.encode('extra')
     	    app.encode(int(round(avg_y_speed*app.globals.plexFloatMult + app.globals.plexFloatMult)))   
     	    # encode second stim duration EK 10/19/20
     	    app.encode_plex('stimdur')
     	    app.encode_plex(int(trial_duration)+app.globals.plexYOffset)
     	    app.encode('stimdur')
     	    app.encode(int(trial_duration)+app.globals.plexYOffset)

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
        #app.globals.stim_arr[samp_loc].off()#the sample
        app.globals.ref_stim_arr[samp_loc].off()
        app.globals.occl_arr[occl_loc].off() #DVPDVP
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
                
        if result == BREAK_FIX: # PZ 10/19/2017 added breakfix timeout
                if breakfix_flag == 1: # PZ 11/06/2017 - give breakfix timeout only for breaks on 2nd stim
                        if P['breakfix_timeout'] > 0:
                                app.globals.dlist.bg = P['breakerror_color']
                                app.globals.dlist.update()
                                app.fb.flip()
                                info(app, "breakfix timeout..")
                                app.idlefn(ms=P['breakfix_timeout'])
                                info(app, "done.")

        """if result == BREAK_FIX:
                if(timeout == 1):
                        if P['timeout'] > 0:
                                app.globals.dlist.bg = P['breakerror_color']
                                app.globals.dlist.update()
                                app.fb.flip()
                                info(app, "error timeout..")
                                app.idlefn(ms=P['timeout'])
                                info(app, "done.")"""

        if result == WRONG_RESP:
                if(P['error_timeout_flag'] == 1):
                        if P['error_timeout'] > 0:
                                app.globals.dlist.bg = P['breakerror_color']
                                app.globals.dlist.update()
                                app.fb.flip()
                                info(app, "error timeout..")
                                app.idlefn(ms=P['error_timeout'])
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
                ("usebar",        "1",               is_boolean,), #NOT USED
                ("trial_tone",    "1",               is_boolean, "tone at every trial"),
                ("grabbeep",    "1",               is_boolean, "beep at bar grab"), #NOT USED
                ("barfirst",    "1",               is_boolean, "grab bar before fixspot"), #NOT USED
                ("Reward Params", None, None),
                ("Reward Buffer Size", "15", is_int, "The number of trials to use to calculate reward ramping"),
                ("numdrops_fix",    "0",           is_int, "Number of juice drops"), # PZ 12/7/2016  #NOT USED
                #("extra_numdrops_unoccluded",    "4",           is_int, "How many more drops for unoccluded than occluded"), # PZ 10/10/2017
                ("Incr_rew_with_occl?","0",is_int,"If 1 then reward is proportional to occl., with numdrops match/nonmatch being reward for unoccl"), # PZ 10/27/2017
                ("Give_rew_for_fix_on_test?","0",is_int,"Give a drop for fixating on 2nd stim?"), # PZ 7/24/2019 #NOT USED
                ("stim2_fix_reward","1000",is_int,"Intervals for giving a drop for fixating on 2nd stim"), # PZ 10/11/2017 #NOT USED
                ("numdrops_match_occl",    "15",           is_int, "Number of juice drops"),
                ("numdrops_non_match_occl",    "15",           is_int, "Number of juice drops"),
                ("numdrops_match_nooccl",    "15",           is_int, "Number of juice drops"), # PZ 2/11/2019
                ("numdrops_non_match_nooccl",    "15",           is_int, "Number of juice drops"), # PZ 2/11/2019
                ("numdrops_err_match","2",            is_int, "Number of juice drops on an error"),
                ("numdrops_err_non_match","2",            is_int, "Number of juice drops on an error"),   
                ("rew_prob",    "1.0",            is_float, "Probability of reward"),
                ("rmult",        "1.0",               is_float),
                ("r_ms_test",        "0.5",               is_float), #NOT USED
                ("seqcor",      "2",            is_int), #NOT USED
                ("seqcor_reset","1",            is_boolean), #NOT USED
                ("allornone",   "1",            is_float, "0->1, prob of drop"), #NOT USED
                ("secondstim_juice", "0", is_boolean), #NOT USED
                ("stim_juice_time", "300", is_int), #NOT USED
                ("stim_juice_time_min", "100", is_int), #NOT USED
                ("stim_juice_time_max", "600", is_int), #NOT USED
                ("std_stim_juice_time", "20", is_int), #NOT USED
                ("Second_Stim_Prob", "1.0",            is_float, "Probability of second stim reward"), #NOT USED
                ("Dot Dimming Params", None, None),
                ("dim",            "1",            is_boolean, "do dot dimming?"), #NOT USED
                ("fixcolor1",    "(255,255,255)",is_color),
                ("fixcolor2",    "(255,255,255)",is_color), #NOT USED
                ("maxrt",       "500",          is_int),
                ("targ_size",    "5",            is_int, "size of target"),
                ("targ_color",     "(255,255,255)",    is_color, "Target color"),
                ("Task Params", None, None),
                ("istime",    "200",               is_int, "Inter-stimulus time"),
                ("stimtime", "600",            is_int, "Stimulus duration"),
                ("ShowTargWithFix", "1", is_boolean, "if 1 show targets as soon as fixation spot appears"),
                ("delay",    "0",            is_int, "if above is zero then this specifies delay between second stim and target"), #NOT USED
                ("travel_t",    "50",        is_int, "Duration to reach outer fixation ring (3 times larger than fix-win)"), #TN 09162017
                ("fix_hold",    "50",        is_int, "Duration to fixate at fixation before making saccade"), #TN 09162017
                ("hold_longest",    "1.5",        is_float, "xx times longer duration will be used for largest occluders"), #TN 09282017  #NOT USED
                ("hold_sd",    "10",        is_int, "Standard deviation (ms) of hold time"), #TN 10052017  #NOT USED
                ("target_delaytime","0",is_int,"Delay between second stim onset and targets onset"), # PZ 11/09/2017
                ("targ_hold",    "50",        is_int, "Duration to fixate at target"),  #NOT USED
                ("min_err",        "0",               is_int),
                ("max_err",        "10000",               is_int),
                ("bg_before",    "(25,25,25)",           is_color),
                ("bg_during",    "(25,25,25)",is_color),
                ("fixlag",        "50",               is_int), #NOT USED
                ("fixwait",        "100",               is_int),
                ("targ_winsize","70",            is_int,    "Target window size"),
                ("stim2winsz",  "30",   is_int, "Change this if you want to manually define the window for stim2"),
                ("targwait",    "50",            is_int,    "Duration to wait for passing through saccades"),
                ("useLookUpTable", "1", is_int, "1:Use preselected non-match; 0:Use selected non-match"),   
                #("Manual_speed_setup","0",is_boolean,"0: cover all slit in 500ms; 1: set below"),
                ("motion_speed","[]",is_any,"0 - 0.6 px/refresh, 1 - 1.0, 2 - 1.4, 3 - 1.8, 4 - 2.2"), ##PZ    
                ("Ref_Stims", "[]", is_any, "Reference Stim Numbers; 1-44, 44 is circle"),
                ("Ref_Rots", "[]", is_any, "Reference Stim Rotations"),
                ("Non_Match_List", "[[],[]]", is_any, "Non-match stims for Reference Stims- Put into list of lists"), 
                ("Non_Match_Rotations", "[[],[]]", is_any, "Non-match stim rotations for Reference Stims - Must match Non_Match_List"),
                #("StimX",            "0",            is_int, "Stimulus X location"),
                #("StimY",            "0",             is_int, "Stimulus Y location"),
                ("RF1_X",            "0",            is_int, "Cell1 X location"),# PZ 11/15/2019
                ("RF1_Y",            "0",             is_int, "Cell1 Y location"),# PZ 11/15/2019
                ("RF2_X",            "0",            is_int, "Cell2 X location"),# PZ 11/15/2019
                ("RF2_Y",            "0",             is_int, "Cell2 Y location"), # PZ 11/15/2019               
                ("Ref_StimX",            "0",            is_int, "Reference Stimulus X location"),
                ("Ref_StimY",            "0",             is_int, "Reference Stimulus Y location"),
                ("RFscale",        "0",                is_boolean, "1:Scale stimulus size by RF size; 0:Use SampleSize"), 
                ("RFscalefactor",    "0.625",        is_float, "If scale by RF size, what's the scale factor?"),
                ("SampleSize",        "100",            is_int, "Sample stimulus size in pixels"),
                ("SampleSizeFract", ".9", is_float, "Fraction of RF that the size of the stimulus is suppose to be."),
                ("SampleStim1_color", "(255,1,1)",    is_color),
                ("Saccade_trial_prob","0.5",        is_float, "Fraction of trials on which saccade target is presented"), #NOT USED
                ("Occluder parameters", None, None),
                ("occl_num_lines", "[]",                is_any, "Number of lines for each type of occluder -- MAKE SURE SAME SIZE AS OCCL_LINES_WIDTHS"),
                ("occl_line_widths", "[]",                is_any, "Width of lines for each type of occluder -- MAKE SURE SAME SIZE AS OCCL_NUM_LINES"),
                ("no_occl_reps", "5", is_int, "Total number of repetitions for no occluders per condition"),
                ("occl_clr",    "(55,55,1)",    is_color, "Occluder color"),
                ("Eye Params", None, None),
                ("innerwin",    "0",               is_int), #NOT USED
                ("track",        "0",               is_boolean), #NOT USED
                ("track_xo",       "0",               is_int, "offset of track point"), #NOT USED
                ("track_yo",       "0",               is_int, "offset of track point"), #NOT USED
                ("track_color", "(255,255,0)",     is_color), #NOT USED
                ("Misc Params", None, None, "Miscellaneous Parameters"),
                ("Recent Buffer Size", "50", is_int, "The number of trials to use to calculate recent performance"),
                ("pause_color", "(150,0,0)", is_color, "The screen will turn this color when the task is paused"),
                ("breakerror_color", "(150,0,0)", is_color, "The screen will turn this color when breakfix on second stim"),   
                ("error_color", "(150,0,0)", is_color, "The screen will turn this color when animal gets error"), #NOT USED
                ("stimreps", "3", is_int, "Total number of repetitions per stimulus/response combination"),
                ("repblocks", "10", is_int, "Total number of times to repeat each block of stimuli"),
                ("redo_errors", "0", is_int,    "0: do not repeat error trials, 1:repeat errors"),
                ("redo_breakfix", "0", is_int,  "0:do not repeat breakfix trials, 1:repeat breakfix"),
                ("redo_immediately", "0", is_int,  "0:do not repeat immediately, 1:repeat immediately, 2: repeat immediately or not, at random"),
                ("error_timeout_flag","0",is_int,"Give error timeout?"), # PZ 2/3/2019
                ("error_timeout","5000",is_int,"Timeout for error if above = 1, ms"), # PZ 2/3/2019
                ("breakfix_timeout_flag","0",is_int,"Give breakfix timeout?"), # PZ 2/3/2019
                ("breakfix_timeout","5000",is_int,"Timeout for break fix, ms"), # PZ 10/19/2017
                ("ShowRFSprites", "0", is_boolean, "if 1 show the rf"),
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

def getRFSprites(app,P): #10/16/20 edited to draw two RF sprites for each RF
        if(P['ShowRFSprites']):
                #circleSprite = Sprite(app.globals.size*2, app.globals.size*2, P['StimX'],P['StimY'],fb=app.fb, depth=1, on=0,centerorigin=1)
                RF1Sprite = Sprite(app.globals.size_RF1*2, app.globals.size_RF1*2, app.globals.RF1X,app.globals.RF1Y,fb=app.fb, depth=1, on=0,centerorigin=1)
                RF2Sprite = Sprite(app.globals.size_RF2*2, app.globals.size_RF2*2, app.globals.RF2X,app.globals.RF2Y,fb=app.fb, depth=1, on=0,centerorigin=1)
                RF1Sprite.fill(P['bg_during']+(0,))
                RF1Sprite.circlefill((255,255,255),r=app.globals.size_RF1/2.0,x=0,y=0,width=1)
                RF2Sprite.fill(P['bg_during']+(0,))
                RF2Sprite.circlefill((255,255,255),r=app.globals.size_RF2/2.0,x=0,y=0,width=1)
                return [RF1Sprite,RF2Sprite]
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

# PZ 3/23/20
#def snapshot_PZ(self, filename, size = None):
#       from PIL import Image
#       pil = Image.frombytes('RGBA', self.screen.get_size(),
#                              pygame.image.tobytes(self.screen, 'RGBA'))
#       pil.save(filename)
#       sys.stdout.write("Wrote screen to: %s\n" % filename)
#def getRecordFileName_pz(app): #gets the record file for this task 
#       filename = "%s%s%s_%s_%02d_%02d.tif" % (params['RFDirectory'],params['AnimalPrefix'],params['Date'],params['TaskName'],params['CellGroup'],params['Iteration'])
#        return filename

def getRecordFileName(app): #gets the record file for this task 
        params = app.params.check()
        if(params['Use Special Name']):
                filename = "%s%s%s_%s_%02d_%02d.rec" % (params['RFDirectory'],params['AnimalPrefix'],params['Date'],params['TaskName'],params['CellGroup'],params['Iteration'])
        else:
                #filename = None
                filename = 'defaultRec.rec' # Tomo NPX - added PZ 2/7/20
        file4Events(app)        
        return filename
        
def file4Events(app): # Tomo NPX - added PZ 2/7/20
        params = app.params.check()
        if(params['Use Special Name']):
                filename = "%s%s%s_%s_g%d_t%d.dat" % (params['RFDirectory'],params['AnimalPrefix'],params['Date'],params['TaskName'],params['CellGroup'],params['Iteration'])
        else:
                filename = 'defaultRec.dat'
                
def saveEvents(app): # Tomo NPX - added PZ 2/7/20
        data = app.record_buffer
        app.record_buffer = []
        params = app.params.check()                 
        if(params['Use Special Name']):
                filename = "%s%s%s_%s_g%d_t%d.dat" % (params['RFDirectory'],params['AnimalPrefix'],params['Date'],params['TaskName'],params['CellGroup'],params['Iteration'])
        else:
                filename = 'defaultRec.dat'
        Newlist = ([[x[1] for x in el] for el in [data]])
        fid = open(filename,'a')
#       if app.globals.param_encoded == 0: # PZ what is this doing at all?? bugs the task, commented out.
#               print 'lololo'
#               app.globals.param_encoded = 1
        for x in Newlist:
                fid.write(str(x)+"\n")
        fid.close()             

def includedOnlyCompletedTrials(self):
        return 0

# This is also something that all tasks have, and it's a python thing.
# Don't touch it.

if not __name__ == '__main__':
        loadwarn(__name__)
else:
        dump(sys.argv[1])


