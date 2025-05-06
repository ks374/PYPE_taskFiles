#!/usr/bin/python
# -*- Mode: Python; tab-width: 4; py-indent-offset: 4; -*-


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

	#check if there are non matchs with the reference inside
	test_pref_stims_list = eval(P['Pref_Stims'])
	test_nm_stims_list_temp = eval(P['NonPref_Stims'])

	# Set various counters and markers in app.globals.  globals is an
	# instance of the Holder class (initialized in function "main,"
	# below), which just lets you store a bunch of variables inside app
	# in a reasonably neat way.
	# - repnum: number of reps completed,
	# - ncorrect: number of trials correct
	# - ntrials: number of trials completed
	# - seqcorrect: count of how many trials in a row have been correct
	# - uicount: how many trials have been uninitiated (use with uimax)
	# - natmpt: number of successful attempts - updated when trial gets up to
	# - the final delay before response
	app.globals.ncorrect = 0
	app.globals.natmpt = 0
	app.globals.ntrials = 0
	app.globals.uicount = 0
	app.globals.seqcorrect = 0
	app.globals.trnum = 0
	app.globals.repblock = 0

	#DVP add's 8/18/11
	#ntrialsAA: number of completed match trials with PS/PC vs PS.PC
	#ntrialsAB: number of completed nonmatch trials with PS/PC vs NS/NC
	#ntrialsBA: number of completed nonmatch trials with NS/NC vs. PS/PC
	#ntrialsBB: number of completed match trials with NS/NC vs. NS/NC
	#ncorrAA: number of correct match trials with PS/PC vs PS.PC
	#ncorrAB: number of correct nonmatch trials with PS/PC vs NS/NC
	#ncorrBA: number of correct nonmatch trials with NS/NC vs. PS/PC
	#ncorrBB: number of correct match trials with NS/NC vs. NS/NC
	
	app.globals.currcase = 0

	app.globals.ntrialsAA = 0
	app.globals.ntrialsAB = 0
	app.globals.ntrialsBA = 0
	app.globals.ntrialsBB = 0
	app.globals.ncorrAA = 0
	app.globals.ncorrAB = 0
	app.globals.ncorrBA = 0
	app.globals.ncorrBB = 0

	# saccade targets are 8dva out;
	zpx = P['mon_dpyw']/2
	zpy = P['mon_dpyh']/2
	app.globals.plexStimIDOffset = pype_plex_code_dict('plexStimIDOffset')
	# Encode all task specific codes here. 
	shft8dva = int(8*P['mon_ppd'])
	app.encode_plex('mon_ppd')
	app.encode('mon_ppd')
	app.encode_plex(int(P['mon_ppd'])+app.globals.plexStimIDOffset)
	app.encode(int(P['mon_ppd']))
	app.globals.xpos = [P['StimX'], shft8dva, -shft8dva]
	app.globals.ypos = [P['StimY'], 0, 0]
	app.globals.plexRotOffset = pype_plex_code_dict('plexRotOffset')
	app.globals.plexYOffset = pype_plex_code_dict('plexYOffset')
	fx,fy = P['fix_x'], P['fix_y']
	#app.encode_plex('size_fract')
	#app.encode('size_fract')
	#app.encode_plex(int(round(P['SampleSizeFract']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
	#app.encode(int(round(P['SampleSizeFract']*pype_plex_code_dict('plexFloatMult') + pype_plex_code_dict('plexFloatMult'))))
	app.encode_plex('fix_x')
	app.encode_plex(fx+app.globals.plexYOffset)
	app.encode_plex('fix_y')
	app.encode_plex(fy+app.globals.plexYOffset)
	app.encode_plex('rfx')
	app.encode_plex(P['StimX']+app.globals.plexYOffset)
	app.encode_plex('rfy')
	app.encode_plex(P['StimY']+app.globals.plexYOffset)
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
	app.encode('iti')
	app.encode(int(P['iti']))
	app.encode('isi')
	app.encode(int(P['istime']))
	app.encode('stim_time')
	app.encode(int(P['stimtime']))
	##########################
	########################
	# Encode the reference stim numbers.
	pref_stims_list = eval(P['Pref_Stims'])
	app.encode_plex(len(pref_stims_list)+app.globals.plexStimIDOffset)
	app.encode(len(pref_stims_list)+app.globals.plexStimIDOffset)
	for i in range(len(pref_stims_list)):
		app.encode_plex(pref_stims_list[i]+app.globals.plexStimIDOffset)
		app.encode(pref_stims_list[i]+app.globals.plexStimIDOffset)
	########################
	# Encode the non-match stim numbers.
	nonpref_stims_list = eval(P['NonPref_Stims'])
	app.encode_plex(len(nonpref_stims_list)+app.globals.plexStimIDOffset)
	app.encode(len(nonpref_stims_list)+app.globals.plexStimIDOffset)
	for i in range(len(nonpref_stims_list)):
		app.encode_plex(nonpref_stims_list[i]+app.globals.plexStimIDOffset)
		app.encode(nonpref_stims_list[i]+app.globals.plexStimIDOffset)
	#########################
	# Encode the preferred rotations
	app.encode('rotid')
	app.encode_plex('rotid')
	pref_rots_list = eval(P['Pref_Rots'])
	app.encode_plex(len(pref_rots_list) + app.globals.plexRotOffset)
	app.encode(len(pref_rots_list) + app.globals.plexRotOffset)
	for i in range(len(pref_rots_list)):
		app.encode_plex(pref_rots_list[i]+app.globals.plexRotOffset)
		app.encode(pref_rots_list[i]+app.globals.plexRotOffset)
	# Encode the nonpreferred rotations
	nonpref_rots_list = eval(P['NonPref_Rots'])
	app.encode_plex(len(nonpref_rots_list) + app.globals.plexRotOffset)
	app.encode(len(nonpref_rots_list) + app.globals.plexRotOffset)
	for i in range(len(nonpref_rots_list)):
		app.encode_plex(nonpref_rots_list[i]+app.globals.plexRotOffset)
		app.encode(nonpref_rots_list[i]+app.globals.plexRotOffset)
	#########################
	# Encode colors of stimuli.  This may not belong here as colors can change during a trial, however that is a rarity and shouldn't happen outside of training
	app.encode_plex('color')
	app.encode('color')
	stimColorName = 'Pref_color'
	if(P.has_key(stimColorName)):
		colorTuple = P[stimColorName]
		app.encode_plex(colorTuple[0] + app.globals.plexRotOffset)
		app.encode_plex(colorTuple[1] + app.globals.plexRotOffset)
		app.encode_plex(colorTuple[2] + app.globals.plexRotOffset)
		app.encode(colorTuple[0] + app.globals.plexRotOffset)
		app.encode(colorTuple[1] + app.globals.plexRotOffset)
		app.encode(colorTuple[2] + app.globals.plexRotOffset)
	stimColorName = 'NonPref_color'
	if(P.has_key(stimColorName)):
		colorTuple = P[stimColorName]
		app.encode_plex(colorTuple[0] + app.globals.plexRotOffset)
		app.encode_plex(colorTuple[1] + app.globals.plexRotOffset)
		app.encode_plex(colorTuple[2] + app.globals.plexRotOffset)
		app.encode(colorTuple[0] + app.globals.plexRotOffset)
		app.encode(colorTuple[1] + app.globals.plexRotOffset)
		app.encode(colorTuple[2] + app.globals.plexRotOffset)
	stimColorName = 'bg_before'
	if(P.has_key(stimColorName)):
		colorTuple = P[stimColorName]
		app.encode_plex(colorTuple[0] + app.globals.plexRotOffset)
		app.encode_plex(colorTuple[1] + app.globals.plexRotOffset)
		app.encode_plex(colorTuple[2] + app.globals.plexRotOffset)
		app.encode(colorTuple[0] + app.globals.plexRotOffset)
		app.encode(colorTuple[1] + app.globals.plexRotOffset)
		app.encode(colorTuple[2] + app.globals.plexRotOffset)
	stimColorName = 'bg_during'
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
	print app.globals.size, SV.spritesize
	# Create the necessary sprites; one sprite per sample object
	# Use the multi_matching_lookup table to get the non-match stim list
	app.globals.attempted_trial = 0
	app.globals.numNonMatch = 0
	app.globals.shape_arr = []
	app.globals.pick_stims = []
	app.globals.pick_rots = []
	app.globals.mylookuptable = []
	prefStims = eval(P['Pref_Stims'])
	prefRots = eval(P['Pref_Rots'])
	useLookUpTable = P['useLookUpTable']
	nonPrefStims = eval(P['NonPref_Stims'])
	nonPrefRots = eval(P['NonPref_Rots'])
	myList = list(arange(len(SV.stmlist)))
	if(useLookUpTable == 1):
		for j in range(len(prefStims)):
			for i in lookuptable.items():
				if(i[0] == prefStims[j]):
					app.globals.mylookuptable.append(i[1]) #maybe keep a list of lookup table stuff
	app.globals.stimcount = 0

	# shape_arr will contain 4 possible stimuli, in the following order:
	# preferred shape (prefStims) of preferred color (pref_color) = A/1
	# nonpreferred shape (nonPrefStims) of nonpreferred color (nonpref_color) = B/2
	# preferred shape of nonpreferred color = C/3
	# nonpreferred shape of preferred color = D/4

	for j in range(len(prefStims)):
		# make stim of preferred shape and preferred color in fixation spot (A/1)
		element = prefStims[j]
		rotation = prefRots[j]
		app.globals.pick_stims.append(element)
		app.globals.pick_rots.append(rotation) #append the reference rotation
		app.globals.shape_arr.append(Sprite(app.globals.size*2, app.globals.size*2, P['fix_x'],\
						P['fix_y'],fb=app.fb, depth=2, on=0, centerorigin=1))
		# fill the square with bg color
		app.globals.shape_arr[app.globals.stimcount].fill(P['bg_during'])
		#if(prefStims[j] == 45):
			#app.globals.shape_arr[app.globals.stimcount].rect(0, 0, 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), P['Pref_color'] )
		#else: ##indent next two lines for else to work
		coords1 = transpose(reshape(concatenate([xt2[app.globals.pick_stims[app.globals.stimcount]-1]\
						[0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50],\
						yt2[app.globals.pick_stims[app.globals.stimcount]-1][0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50]]),\
						(2,50*SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1])))
		app.globals.shape_arr[app.globals.stimcount].polygon(P['Pref_color'], coords1, width=0)
		app.globals.shape_arr[app.globals.stimcount].rotate(360-rotation)
		app.globals.shape_arr[app.globals.stimcount].off()

		app.globals.stimcount = app.globals.stimcount + 1

		#######
		# make stim of preferred shape and preferred color in RF center (A/2)
		element = prefStims[j]
		rotation = prefRots[j]
		app.globals.pick_stims.append(element)
		app.globals.pick_rots.append(rotation) #append the reference rotation
		app.globals.shape_arr.append(Sprite(app.globals.size*2,app.globals.size*2, P['StimX'],\
							P['StimY'],fb=app.fb, depth=2, on=0, centerorigin=1))
		# fill the square with bg color
		app.globals.shape_arr[app.globals.stimcount].fill(P['bg_during'])
		#if(prefStims[j] == 45):
			#app.globals.shape_arr[app.globals.stimcount].rect(0, 0, 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), P['Pref_color'] )
		#else: ##indent next two lines for else to work
		coords1 = transpose(reshape(concatenate([xt2[app.globals.pick_stims[app.globals.stimcount]-1]\
						[0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50],\
						yt2[app.globals.pick_stims[app.globals.stimcount]-1][0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50]]),\
						(2,50*SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1])))
		app.globals.shape_arr[app.globals.stimcount].polygon(P['Pref_color'], coords1, width=0)
		app.globals.shape_arr[app.globals.stimcount].rotate(360-rotation)
		app.globals.shape_arr[app.globals.stimcount].off()

		app.globals.stimcount = app.globals.stimcount + 1



	for i in range(len(nonPrefStims)):
		# make non preferred shape of non preferred color in fixation spot (B/3)
		app.globals.numNonMatch = len(nonPrefStims)
		element = (nonPrefStims[i])
		rotation = (nonPrefRots[i])
		app.globals.pick_stims.append(element)
		app.globals.pick_rots.append(rotation) #append the reference rotation
		app.globals.shape_arr.append(Sprite(app.globals.size*2, app.globals.size*2, P['fix_x'],\
							P['fix_y'],fb=app.fb, depth=2, on=0, centerorigin=1))
		# fill the square with bg color
		app.globals.shape_arr[app.globals.stimcount].fill(P['bg_during'])
		#if(element == 45):
			#app.globals.shape_arr[app.globals.stimcount].rect(0, 0, 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), P['NonPref_color'] )
		#else:
		coords1 = transpose(reshape(concatenate([xt2[app.globals.pick_stims[app.globals.stimcount]-1]\
							[0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50],\
							yt2[app.globals.pick_stims[app.globals.stimcount]-1][0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50]]),\
							(2,50*SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1])))
		app.globals.shape_arr[app.globals.stimcount].polygon(P['NonPref_color'], coords1, width=0)
		app.globals.shape_arr[app.globals.stimcount].rotate(360-rotation)
		app.globals.shape_arr[app.globals.stimcount].off()
		app.globals.stimcount = app.globals.stimcount + 1


		# make non preferred shape of non preferred color in RF center (B/4)
		app.globals.numNonMatch = len(nonPrefStims)
		element = (nonPrefStims[i])
		rotation = (nonPrefRots[i])
		app.globals.pick_stims.append(element)
		app.globals.pick_rots.append(rotation) #append the reference rotation
		app.globals.shape_arr.append(Sprite(app.globals.size*2,app.globals.size*2, P['StimX'],\
							P['StimY'],fb=app.fb, depth=2, on=0, centerorigin=1))
		# fill the square with bg color
		app.globals.shape_arr[app.globals.stimcount].fill(P['bg_during'])
		#if(element == 45):
			#app.globals.shape_arr[app.globals.stimcount].rect(0, 0, 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), P['NonPref_color'] )
		#else:
		coords1 = transpose(reshape(concatenate([xt2[app.globals.pick_stims[app.globals.stimcount]-1]\
							[0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50],\
							yt2[app.globals.pick_stims[app.globals.stimcount]-1][0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50]]),\
							(2,50*SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1])))
		app.globals.shape_arr[app.globals.stimcount].polygon(P['NonPref_color'], coords1, width=0)
		app.globals.shape_arr[app.globals.stimcount].rotate(360-rotation)
		app.globals.shape_arr[app.globals.stimcount].off()
		app.globals.stimcount = app.globals.stimcount + 1

	# this should print '2' at this point
	print app.globals.stimcount

	for j in range(len(prefStims)):
		# make stim of preferred shape and nonpreferred color in RF center (C/5)
		element = prefStims[j]
		rotation = prefRots[j]
		app.globals.pick_stims.append(element)
		app.globals.pick_rots.append(rotation) #append the reference rotation
		app.globals.shape_arr.append(Sprite(app.globals.size*2, app.globals.size*2, P['StimX'],\
						P['StimY'],fb=app.fb, depth=2, on=0, centerorigin=1))
		# fill the square with bg color
		app.globals.shape_arr[app.globals.stimcount].fill(P['bg_during'])
		#if(prefStims[j] == 45):
			#app.globals.shape_arr[app.globals.stimcount].rect(0, 0, 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), P['NonPref_color'] )
		#else:
		coords1 = transpose(reshape(concatenate([xt2[app.globals.pick_stims[app.globals.stimcount]-1]\
						[0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50],\
						yt2[app.globals.pick_stims[app.globals.stimcount]-1][0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50]]),\
						(2,50*SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1])))
		app.globals.shape_arr[app.globals.stimcount].polygon(P['NonPref_color'], coords1, width=0)
		app.globals.shape_arr[app.globals.stimcount].rotate(360-rotation)
		app.globals.shape_arr[app.globals.stimcount].off()

		app.globals.stimcount = app.globals.stimcount + 1

	# for non preferred shapes
	for i in range(len(nonPrefStims)):
		# make nonpreferred shape of preferred color (D/6)
		app.globals.numNonMatch = len(nonPrefStims)
		element = (nonPrefStims[i])
		rotation = (nonPrefRots[i])
		app.globals.pick_stims.append(element)
		app.globals.pick_rots.append(rotation) #append the reference rotation
		app.globals.shape_arr.append(Sprite(app.globals.size*2, app.globals.size*2, P['StimX'],\
						P['StimY'],fb=app.fb, depth=2, on=0, centerorigin=1))
		# fill the square with bg color
		app.globals.shape_arr[app.globals.stimcount].fill(P['bg_during'])
		#if(element == 45):
			#app.globals.shape_arr[app.globals.stimcount].rect(0, 0, 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), 0.8*app.globals.size*P['SampleSizeFract']/sqrt(2), P['Pref_color'] )
		#else:
		coords1 = transpose(reshape(concatenate([xt2[app.globals.pick_stims[app.globals.stimcount]-1]\
						[0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50],\
						yt2[app.globals.pick_stims[app.globals.stimcount]-1][0:SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1]*50]]),\
						(2,50*SV.nvrt[app.globals.pick_stims[app.globals.stimcount]-1])))
		app.globals.shape_arr[app.globals.stimcount].polygon(P['Pref_color'], coords1, width=0)
		app.globals.shape_arr[app.globals.stimcount].rotate(360-rotation)
		app.globals.shape_arr[app.globals.stimcount].off()
		app.globals.stimcount = app.globals.stimcount + 1

	# this should print '4' at this point
	print app.globals.stimcount

	##################################
	# Generate arrays for stimulus presentation
	##################################


	# if training:
	# stim1list: [1,1,2,2] stim2list [1,2,1,2]
	# caselist: [1,2,3,4] [M,NM,NM,M]
	# if testing:
	# stim1list: [1,1,1,2,2,2]
	# stim2list: [1,2,4,1,2,3]
	# & if always showing novel combos
	# caselist: [1,2,3,4,5,6,1,5] [M,NM,NM,NM,M,NM,M,M]
	# if not showing novel combos, same as train set

	app.globals.blockLength = P['Block length']
	showNovel = P['ShowNovel']
	show2combos = P['Show2Combos']

	app.globals.stim1list = []
	app.globals.stim2list = []
	app.globals.caselist = []

	if showNovel == 1:
		#stim1list and stim2list should not change from here on
		#manipulations over caselist will take care of any adjustments in frequency of stim generation
		app.globals.stim1list = [1,3,1,3,1,3]
		app.globals.stim2list = [2,4,4,2,6,5]
		#app.globals.caselist = [1,2,3,4,5,6][M,M,NM,NM,NVNM,NVNM]
		#calculate half a block to split between match/nonmatches evenly
		halfblock = app.globals.blockLength/2
		print 'halfblock', halfblock
		#calculate how many nonmatches will be replaced with novel combos (also nonmatches)
		toreplace = ((P['% Novel Stims in Block'])*app.globals.blockLength)/100
		print 'toreplace', toreplace
		x = 1
		while x < halfblock+1:
			#add nonmatches to caselist for first half of block
			#if x is odd, add 1/4/3 (stim1/stim2/case)
			if x%2 == 1:
				app.globals.caselist.append(3)
			#if x is even, add 3/2/4
			else:
				app.globals.caselist.append(4)
			x = x+1
		y = halfblock+1
		while y < app.globals.blockLength+1:
			#add matches to caselist for second half of block
			#if y is odd, add 1/2/1
			if y%2 == 1:
				app.globals.caselist.append(1)
			#if y is even, add 3/4/2
			else:
				app.globals.caselist.append(2)
			y = y+1
		z1 = 1
		while z1 <= toreplace:
			#pop the first element from caselist
			app.globals.caselist.pop(0)
			z1 = z1+1
		z2 = 1
		while z2 <= toreplace:
			#if z is odd, add 1/6/5
			if z2%2 == 1:
				app.globals.caselist.append(5)
			#if z is even, add 3/5/6
			else:
				app.globals.caselist.append(6)
			z2 = z2+1



	else:
		#stim1list and stim2list should not change from here on
		#manipulations over caselist will take care of any adjustments in frequency of stim generation
		app.globals.stim1list = [1,3,1,3]
		app.globals.stim2list = [2,4,4,2]


		if show2combos == 0:
			#generates the following case:
			#4 combinations:
			#A/A, B/B, B/A, A/B (A = prefshape, prefcolor; B = nonprefshape, nonprefcolor)

			#calculate half a block to split between match/nonmatches evenly
			halfblock = app.globals.blockLength/2
			x = 1
			while x < halfblock+1:
				#add nonmatches to caselist for first half of block
				#if x is odd, add 1/4/3
				if x%2 == 1:
					app.globals.caselist.append(3)
				#if x is even, add 3/2/4
				else:
					app.globals.caselist.append(4)
				x = x+1
			y = halfblock+1
			while y < app.globals.blockLength+1:
				#add matches to caselist for second half of block
				#if y is odd, add 1/2/1
				if y%2 == 1:
					app.globals.caselist.append(1)
				#if y is even, add 3/4/2
				else:
					app.globals.caselist.append(2)
				y = y+1


		else:
			#generates the following cases:
			#if show2combos = 1:
			#A/A, B/B (matches only)
			#if show2combos = 2:
			#A/B, B/A (nonmatches only)
			#if show2combos = 3:
			#A/A, A/B (prefshape/prefcolor as ref stim only)
			#if show2combos = 4:
			#B/A, B/B (nonprefshape/nonprefcolor as ref stim only)

			
			if show2combos == 1:
				#calculate half a block to split between A/A,B/B evenly
				halfblock = app.globals.blockLength/2
				x = 1
				while x < halfblock+1:
					#add A/A to caselist for first half of block
					app.globals.caselist.append(1)
					x = x+1
				
				y = halfblock+1
				while y < app.globals.blockLength+1:
					#add B/B to caselist for second half of block
					app.globals.caselist.append(2)
					y = y+1

			if show2combos == 2:
				#calculate half a block to split between A/B,B/A evenly
				halfblock = app.globals.blockLength/2
				x = 1
				while x < halfblock+1:
					#add A/B to caselist for first half of block
					app.globals.caselist.append(3)
					x = x+1
				y = halfblock+1
				while y < app.globals.blockLength+1:
					#add B/A to caselist for second half of block
					app.globals.caselist.append(4)
					y = y+1

			if show2combos == 3:
				#calculate half a block to split between A/A,A/B evenly
				halfblock = app.globals.blockLength/2
				x = 1
				while x < halfblock+1:
					#add A/A to caselist for first half of block
					app.globals.caselist.append(1)
					x = x+1
				y = halfblock+1
				while y < app.globals.blockLength+1:
					#add A/B to caselist for second half of block
					app.globals.caselist.append(3)
					y = y+1

			if show2combos == 4:
				#calculate half a block to split between B/A,B/B evenly
				halfblock = app.globals.blockLength/2
				x = 1
				while x < halfblock+1:
					#add B/A to caselist for first half of block
					app.globals.caselist.append(4)
					x = x+1
				y = halfblock+1
				while y < app.globals.blockLength+1:
					#add B/B to caselist for second half of block
					app.globals.caselist.append(2)
					y = y+1


	#else:
		#con(app, "Something is wrong with the setup - not training and not testing")
		#raise UserAbort

	print app.globals.stim1list, app.globals.stim2list, app.globals.caselist



	#Set up the trial buffers. For each trial, we need to a stimulus number, target location
	#(1:match,2:non-match) and occluder id
	#print app.globals.stimcount
	nct = 0

	app.globals.stimorder = []
	#a = range(len(app.globals.caselist))
	a = app.globals.caselist
	while nct < (P['repblocks']):
		if(P['randomize'] == 1):
			random.shuffle(a)
		app.globals.stimorder = app.globals.stimorder+a
		nct = nct+1
	#app.encode('stimorder')
	#app.encode(app.globals.stimorder)
	#app.encode_plex('stimorder')
	#app.encode_plex(app.globals.stimorder)
	#app.globals.blockLength = len(app.globals.stimorder)

	print app.globals.stimcount,app.globals.stimorder
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
		#while (app.running and (app.globals.repblock*P['repblocks']) < P['stimreps']):
		while (app.running and app.globals.repblock < P['repblocks']):
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
				AA_beh = 0.0
				AB_beh = 0.0
				BA_beh = 0.0
				BB_beh = 0.0
			else:
				over_beh = 100.0*app.globals.ncorrect/app.globals.natmpt
				if app.globals.ntrialsAA > 0:
					AA_beh = 100.0*app.globals.ncorrAA/app.globals.ntrialsAA
				else:
					AA_beh = 0.0
				if app.globals.ntrialsAB > 0:
					AB_beh = 100.0*app.globals.ncorrAB/app.globals.ntrialsAB
				else:
					AB_beh = 0.0
				if app.globals.ntrialsBA > 0:
					BA_beh = 100.0*app.globals.ncorrBA/app.globals.ntrialsBA
				else:
					BA_beh = 0.0
				if app.globals.ntrialsBB > 0:
					BB_beh = 100.0*app.globals.ncorrBB/app.globals.ntrialsBB
				else:
					BB_beh = 0.0
			con(app, " %s: %d/%d %.0f%% beh: %.0f%% (recent %.0f%%  recentbeh %.0f%%)" % \
					(now(), \
					app.globals.ncorrect, app.globals.ntrials, \
					100.0 * app.globals.ncorrect / app.globals.ntrials, \
					over_beh, \
					recent, recentbeh), 'black')
			con(app, "behAA: %.0f%% behAB: %.0f%% behBA: %.0f%% behBB: %.0f%%)" % \
					(AA_beh, AB_beh, BA_beh, BB_beh), 'black')

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
		#a = range(len(app.globals.caselist))
		a = app.globals.caselist
		nct = 0
		while nct < (P['repblocks']):
			if(P['randomize'] == 1):
				random.shuffle(a)
			app.globals.stimorder = app.globals.stimorder+a
			nct = nct+1
	#app.encode('stim order')
	#app.encode(app.globals.stimorder)
	#app.encode_plex('stim order')
	#app.encode_plex(app.globals.stimorder)
	# The intertrial interval is at the start of each trial
	# (arbitrary).  Calling encode will make a note in the data record
	# with the current timestamp and whatever comment you give it.
	app.encode(START_ITI)
	app.encode_plex(START_ITI)

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
		spot = Sprite(2*P['fix_ring'], 2*P['fix_ring'], fx, fy, fb=app.fb, depth=1, on=0, centerorigin=1)
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
		spot = Sprite(2*P['fix_size'], 2*P['fix_size'], fx, fy, fb=app.fb, depth=1, on=0, centerorigin=1)
		spot.fill(P['bg_during'])
		if P['fix_size'] > 1:
			spot.circlefill(P['fixcolor1'], r=P['fix_size'], x=0, y=0)
		else:
			spot[0,0] = P['fixcolor1']

	# This is redundant with on=0 above, but make sure the sprite is off
	spot.off()
	# Add spot to the dlist
	app.globals.dlist.add(spot)
	#con(app,"%d stimuli presented, %d stimuli remaining" % (app.globals.natmpt,(P['stimreps']*app.globals.blockLength)-(app.globals.blockLength-len(app.globals.stimorder))-(app.globals.blockLength*app.globals.repblock)),"Black")
	con(app,"%d pairs of stimuli presented, %d pairs of stimuli remaining" % (app.globals.natmpt,len(app.globals.stimorder)),"Black")
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

	##################################
	# HERE IS WHERE STIMULI ARE POPPED
	##################################
	# Get the stimuli to be presented
	# this refers to index of case in stim1/2 arrays
	currentcase = app.globals.stimorder.pop(0)
	app.globals.currcase = currentcase
	# this temporarily stores the stimuli (A/1, B/2, etc) based on the case
	currstim1 = app.globals.stim1list[currentcase-1]
	currstim2 = app.globals.stim2list[currentcase-1]

	#print currstim1, currstim2

	# default correct decision is leftward saccade/match_id 2
	t_loc = 2
	match_id = 2

	# for A/A and B/B, set correct decision to rightward saccade/match_id to 1
	if (currentcase == 1 or currentcase == 2):
		t_loc = 1
		match_id = 1

	if (currstim1 > 0):
		# then assign samp_loc to index of preferred shape
		samp_loc = currstim1 - 1
	else:
		print 'Something is wrong with the generated stim1array.'
		raise UserAbort

	if (currstim2 > 0):
		# then assign samp_loc to index of preferred shape
		samp_loc2 = currstim2 - 1
	else:
		print 'Something is wrong with the generated stim2array.'
		raise UserAbort

	app.globals.dlist.add(app.globals.shape_arr[samp_loc]) #sample1
	app.globals.dlist.add(app.globals.shape_arr[samp_loc2])#sample2


	# # # # # # # # # # # # # # # # # #
	# Code for making the target spot
	# # # # # # # # # # # # # # # # # #
	# First location of target 1
	# Here is some basic target point code. Note that targ_size is
	# targ_color has to be specified by the task.
	"""
	#this section not needed for human task - use button press, not saccade
	# Create a sprite
	target1 = Sprite(2*P['targ_size'], 2*P['targ_size'], app.globals.xpos[t_loc], fy, fb=app.fb, depth=1, on=0, centerorigin=1)
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
	target2 = Sprite(2*P['targ_size'], 2*P['targ_size'], app.globals.xpos[3-t_loc], fy, fb=app.fb, depth=1, on=0, centerorigin=1)
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
	"""
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
		app.encode(FIX_ACQUIRED) # Standard event encoding
		app.encode_plex(FIX_ACQUIRED)
		fixwin.draw(color='blue') # Blue is our "active" fixwin color

		# encode the first stimulus to be presented
		app.encode_plex('stimid')
		app.encode_plex(currstim1+app.globals.plexStimIDOffset)


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
		# now turn on the first stimulus
		rfSprite = getRFSprite(app,P)
		if(rfSprite is not None):
			app.globals.dlist.add(rfSprite)
			rfSprite.on()
			app.globals.dlist.update()
		app.fb.sync_toggle() #note: toggle_photo_diode updates the dlist
		app.globals.shape_arr[samp_loc].on()
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
				app.globals.shape_arr[samp_loc].off()
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
		app.globals.shape_arr[samp_loc].off()
		if(rfSprite is not None):
			rfSprite.off()
		app.globals.dlist.update()
		app.fb.sync_toggle() #note: toggle_photo_diode updates the dlist
		app.fb.flip()
		app.encode_plex(SAMPLE_OFF)
		app.encode(SAMPLE_OFF)
		t.reset() # Reset timer to start second is timer

		#encode 2nd stim to be presented
		app.encode_plex('stimid')
		app.encode_plex(currstim2+app.globals.plexStimIDOffset)


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
		# now turn on the 2nd stimulus
		if(rfSprite is not None):
			app.globals.dlist.add(rfSprite)
			rfSprite.on()
			app.globals.dlist.update()
		app.globals.shape_arr[samp_loc2].on()

		app.globals.dlist.update() #DVP comment out
		app.fb.sync_toggle() #DVP comment out
		app.fb.flip() #DVP comment out
		app.encode_plex(SAMPLE_ON)
		app.encode(SAMPLE_ON)
		#app.udpy.display(app.globals.dlist)
		#if(P['variable_second_stimtime'] == 1):
			#secondStimTime = random.gauss(P['mu_stimtime'], P['std_stimtime'])
			#if(secondStimTime > P['max_stimtime'] or secondStimTime < P['min_stimtime']):
				#secondStimTime = P['stimtime']
		#else:
			#secondStimTime = P['stimtime']

		# set second stim time to as long as we will wait for a saccade
		secondStimTime = P['maxrt']

		if(P['variable_delaytime'] == 1):
			delaytime = random.gauss(P['mu_delaytime'], P['std_delaytime'])
			if(delaytime > P['mu_delaytime']):
				delaytime = P['mu_delaytime']
		else:
			delaytime = P['mu_delaytime']
		app.encode_plex(int(round(delaytime+app.globals.plexStimIDOffset)))
		app.encode(int(round(delaytime+app.globals.plexStimIDOffset)))

		tstim2 = Timer()
		tstim2.reset()

		t.reset() #timer reset to monitor rxn time DVP add 8/18/11

		###the following section not needed for true reaction time task
		"""
		while tstim2.ms() < delaytime:
			# Again, a dummy flag to help with task control
			go_on = 0
			while not go_on and tstim2.ms() < delaytime:
				# We are waiting for the eye position to move outside the
				# fixation window to make a decision (so we can turn off the 2nd stim)
				if fixwin.broke(0):
					# turn off the 2nd stimulus stimulus
					app.globals.shape_arr[samp_loc2].off()
					spot.off() ##DVP
					if(rfSprite is not None):
						rfSprite.off()
					app.globals.dlist.update()
					app.fb.sync_toggle() #note: toggle_photo_diode updates the dlist
					app.fb.flip()
					app.encode_plex(SAMPLE_OFF)
					app.encode(SAMPLE_OFF)
					go_on = 1
				app.idlefn()
			go_on2 = 0
		"""

		##################
		##################
		#This portion needs to be altered to wait for keypress instead of saccade
		##################
		##################
		c = 'b'
		testvar = 'notdone'
		while not testvar == 'done':
			while c:
				(c, ev) = app.keyque.pop()
			(c, ev) = app.keyque.pop()
			testvar = 'notdone'
			if fixwin.broke() and not TESTING:
				app.encode_plex(FIX_LOST)
				app.encode(FIX_LOST)
				info(app, "lost target fix")
				con(app, "lost target fix (%d ms)" % t2.ms(), 'red')
				result = BREAK_FIX
				# Auditory feedback
				app.warn_trial_incorrect(flash=None)
				raise MonkError
			# Again, a call to idlefn lets the computer catch up
			# and monitor for key presses.
			app.idlefn()
			if c == 'm':
				##double check the stim is off once decision is made
				app.globals.shape_arr[samp_loc2].off()
				spot.off() ##DVP
				if(rfSprite is not None):
					rfSprite.off()
				app.globals.dlist.update()
				app.fb.sync_toggle() #note: toggle_photo_diode updates the dlist
				app.fb.flip()
				app.encode_plex(SAMPLE_OFF)
				app.encode(SAMPLE_OFF)

				##then check if that was the correct decision
				##matchid 1: match, 2: nonmatch
				if match_id == 1:
					#correctly chose match
					rxtime = t.ms() #time since 2nd stim turned on
					app.encode_plex(rxtime + app.globals.plexStimIDOffset)
					app.encode(rxtime + app.globals.plexStimIDOffset)
					con(app, "Correct choice (M)", 'blue')
					info(app, "Reaction Time")
					con(app, "Reaction Time (%d ms)" % rxtime, 'black')
					t.reset()
					raise NoProblem
				else:
					#incorrectly chose match
					rxtime = t.ms() #time since 2nd stim turned on
					app.encode_plex(rxtime + app.globals.plexStimIDOffset)
					app.encode(rxtime + app.globals.plexStimIDOffset)
					con(app, "Incorrect choice (M)", 'red')
					info(app, "Reaction Time")
					con(app, "Reaction Time (%d ms)" % rxtime, 'black')
					t.reset()
					app.globals.natmpt = app.globals.natmpt+1 #attempt only counts if it is either error response or correct.
					result = WRONG_RESP
					raise MonkError
				testvar = 'done'
			elif c == 'n':
				##double check the stim is off once decision is made
				app.globals.shape_arr[samp_loc2].off()
				spot.off() ##DVP
				if(rfSprite is not None):
					rfSprite.off()
				app.globals.dlist.update()
				app.fb.sync_toggle() #note: toggle_photo_diode updates the dlist
				app.fb.flip()
				app.encode_plex(SAMPLE_OFF)
				app.encode(SAMPLE_OFF)

				##then check if that was the correct decision
				##matchid 1: match, 2: nonmatch
				if match_id == 2:
					#correctly chose nonmatch
					rxtime = t.ms() #time since 2nd stim turned on
					app.encode_plex(rxtime + app.globals.plexStimIDOffset)
					app.encode(rxtime + app.globals.plexStimIDOffset)
					con(app, "Correct choice (NM)", 'blue')
					info(app, "Reaction Time")
					con(app, "Reaction Time (%d ms)" % rxtime, 'black')
					t.reset()
					raise NoProblem
				else:
					#incorrectly chose nonmatch
					rxtime = t.ms() #time since 2nd stim turned on
					app.encode_plex(rxtime + app.globals.plexStimIDOffset)
					app.encode(rxtime + app.globals.plexStimIDOffset)
					con(app, "Incorrect choice (NM)", 'red')
					info(app, "Reaction Time")
					con(app, "Reaction Time (%d ms)" % rxtime, 'black')
					t.reset()
					app.globals.natmpt = app.globals.natmpt+1 #attempt only counts if it is either error response or correct.
					result = WRONG_RESP
					raise MonkError
				testvar = 'done'
			elif c:
				##double check the stim is off once decision is made
				app.globals.shape_arr[samp_loc2].off()
				spot.off() ##DVP
				if(rfSprite is not None):
					rfSprite.off()
				app.globals.dlist.update()
				app.fb.sync_toggle() #note: toggle_photo_diode updates the dlist
				app.fb.flip()
				app.encode_plex(SAMPLE_OFF)
				app.encode(SAMPLE_OFF)
					##pressed wrong key
				con (app, "WRONG KEY", 'blue')
				app.encode_plex(FIX_LOST)
				app.encode(FIX_LOST)
				info(app, "early break")
				con(app, "Pressed the wrong button at %d ms into presentation of stim2" % (t.ms()), 'red')
				result = NO_RESP
				#Auditory feedback
				app.warn_trial_incorrect(flash=None)
				# Skip to end of trial
				raise MonkError
			elif P['maxrt'] > 0 and t.ms() > P['maxrt']:
				#turn off stimuli
				app.globals.shape_arr[samp_loc2].off()
				spot.off() ##DVP
				if(rfSprite is not None):
					rfSprite.off()
				app.globals.dlist.update()
				app.fb.sync_toggle() #note: toggle_photo_diode updates the dlist
				app.fb.flip()
				app.encode_plex(SAMPLE_OFF)
				app.encode(SAMPLE_OFF)
				info(app, "no target saccade")
				con(app, "Time limit exceeded (%d ms)" % t.ms(), 'red')
				result = NO_RESP
				app.encode_plex(NO_RESP)
				app.encode(NO_RESP)
				beep(2000,100)
				app.globals.natmpt = app.globals.natmpt+1 #attempt only counts if it is either error response or correct.
				raise MonkError
			app.idlefn()


	# # # # # # # # # # # # # # # # # #
	# Handling exceptions generated in the trial
	# # # # # # # # # # # # # # # # # #

	except UserAbort:
		# If you pressed the escape key at any time to abort the trial
		# you will end up here.  No counters are incremented or
		# reset basically because this was not the subject's fault.
		con(app, "Aborted.", 'red')
		# Stop monitoring eye position, encode 'eye_stop' in the datafile
		# which will always be the last timestamp at which eyetrace data
		# were collected.
		fixwin.clear()
		app.eyetrace(0)
		# These variables will be returned to RunTrial.
		result = USER_ABORT
		app.encode_plex(USER_ABORT)
		app.fb.sync(0)
	except MonkError:
		# Any of the MonkError exceptions will land you here.  The
		# trial counter is incremented and the seqcorrect counter
		# is reset.

		# Stop monitoring eye position, encode 'eye_stop' in the datafile
		# which will always be the last timestamp at which eyetrace data
		# were collected.
		fixwin.clear()
		app.eyetrace(0)
		#Auditory feedback
		app.warn_trial_incorrect(flash=None)

		app.globals.ntrials = app.globals.ntrials + 1

		#DVP add 8/18/11
		if app.globals.currcase == 1:
			app.globals.ntrialsAA = app.globals.ntrialsAA + 1
		if app.globals.currcase == 2:	
			app.globals.ntrialsBB = app.globals.ntrialsBB + 1
		if app.globals.currcase == 3:	
			app.globals.ntrialsAB = app.globals.ntrialsAB + 1
		if app.globals.currcase == 4:	
			app.globals.ntrialsBA = app.globals.ntrialsBA + 1	

		app.globals.seqcorrect = 0
		if((result != WRONG_RESP and result != NO_RESP) and P['redo_breakfix'] == 1):
			if(P['redo_immediately'] == 1):
				app.globals.stimorder.insert(0,currentcase)
			else:
				app.globals.stimorder.append(currentcase)
				random.shuffle(app.globals.stimorder)
				#print currentcase
				#print app.globals.stimorder
		if result == WRONG_RESP:
			if(P['redo_errors'] == 1):
				if(P['redo_immediately'] == 1):
					app.globals.stimorder.insert(0,currentcase)
				else:
					app.globals.stimorder.append(currentcase)
					random.shuffle(app.globals.stimorder)
			app.globals.attempted_trial = 0
		app.fb.sync(0)
	except NoProblem:
		# Having an exception for a correct trial is handy because
		# there are a number of ways of getting the trial correct
		# depending on whether we're monitoring the eye position or
		# touch bar or dot dimming, and we can put all the reward
		# code in one place.

		# Stop monitoring eye position, encode 'eye_stop' in the datafile
		# which will always be the last timestamp at which eyetrace data
		# were collected.
		fixwin.clear()
		app.eyetrace(0)

		result = CORRECT_RESPONSE
		app.encode_plex(CORRECT_RESPONSE)
		app.encode(CORRECT_RESPONSE)
		app.warn_trial_correct() #Standard "correct" beep

		# Increment the sequence correct counter
		app.globals.seqcorrect=app.globals.seqcorrect + 1
		app.globals.attempted_trial = 0

		app.fb.sync(0)
		# Reporting stuff, variables returned to RunTrial
		app.globals.natmpt = app.globals.natmpt+1
		app.globals.ncorrect = app.globals.ncorrect + 1
		app.globals.ntrials = app.globals.ntrials + 1

		#DVP add 8/18/11
		if app.globals.currcase == 1:
			app.globals.ntrialsAA = app.globals.ntrialsAA + 1
			app.globals.ncorrAA = app.globals.ncorrAA + 1
		if app.globals.currcase == 2:	
			app.globals.ntrialsBB = app.globals.ntrialsBB + 1
			app.globals.ncorrBB = app.globals.ncorrBB + 1
		if app.globals.currcase == 3:	
			app.globals.ntrialsAB = app.globals.ntrialsAB + 1
			app.globals.ncorrAB = app.globals.ncorrAB + 1
		if app.globals.currcase == 4:	
			app.globals.ntrialsBA = app.globals.ntrialsBA + 1
			app.globals.ncorrBA = app.globals.ncorrBA + 1


	# # # # # # # # # # # # # # # # # #
	# Cleanup
	# # # # # # # # # # # # # # # # # #

	# This code runs no matter what the result was, it is after all the
	# exception handling
	spot.off()
	# Turn off the fixation spot and tracker dot
	#target1.off()
	#target2.off()
	app.encode(FIX_OFF)
	app.encode_plex(FIX_OFF)
	# Stop monitoring eye position, encode 'eye_stop' in the datafile
	# which will always be the last timestamp at which eyetrace data
	# were collected.
	#targwin.clear()
	#nontargwin.clear() #DVP ADD
	app.eyetrace(0)
	app.encode_plex(EYE_STOP)
	app.encode(EYE_STOP)
	app.globals.shape_arr[samp_loc].off()#the sample
	app.globals.shape_arr[samp_loc2].off()#the 2nd sample
	#if t_loc == 2:
		#app.globals.shape_arr[samp_loc2].off()#the 2nd sample
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

	if result == WRONG_RESP:
		if(timeout == 1):
			if P['timeout'] > 0:
				app.globals.dlist.bg = P['error_color']
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
		("usebar",	"1",	is_boolean,),
		("trial_tone",	"1",	is_boolean, "tone at every trial"),
		("grabbeep",	"1",	is_boolean, "beep at bar grab"),
		("barfirst",	"1",	is_boolean, "grab bar before fixspot"),
		("Reward Params", None, None),
		("numdrops_match",	"0",	is_int, "Number of juice drops"),
		("numdrops_non_match",	"0",	is_int, "Number of juice drops"),
		("numdrops_err_match","0",	is_int, "Number of juice drops on an error"),
		("numdrops_err_non_match","0",	is_int, "Number of juice drops on an error"),
		("rew_prob",	"1.0",	is_float, "Probability of reward"),
		("rmult",	"1.0",	is_float),
		("seqcor",	"2",	is_int),
		("seqcor_reset","1",	is_boolean),
		("allornone",	"1",	is_float, "0->1, prob of drop"),
		("secondstim_juice", "0", is_boolean),
		("stim_juice_time", "300", is_int),
		("stim_juice_time_min", "100", is_int),
		("stim_juice_time_max", "600", is_int),
		("std_stim_juice_time", "20", is_int),
		("Second_Stim_Prob", "1.0",	is_float, "Probability of second stim reward"),
		("Dot Dimming Params", None, None),
		("dim",	"1",	is_boolean, "do dot dimming?"),
		("fixcolor1",	"(255,255,255)",is_color),
		("fixcolor2",	"(255,255,255)",is_color),
		("maxrt",	"1500",	is_int),
		("targ_size",	"5",	is_int, "size of target"),
		("targ_color",	"(255,255,255)",	is_color, "Target color"),
		("Task Params", None, None),
		("istime",	"200",	is_int, "Inter-stimulus time"),
		("stimtime", "600",	is_int, "Stimulus duration"),
		("variable_second_stimtime", "0",	is_boolean, "If 1 then second stimulus duration is picked from a gaussian distribution"),
		("mu_stimtime", "400",	is_int, "Mu in a Gaussian Distribution to select random second stim time"),
		("min_stimtime", "200",	is_int, "Min in a Gaussian Distribution to select random second stim time"),
		("max_stimtime", "600",	is_int, "Max in a Gaussian Distribution to select random second stim time"),
		("std_stimtime", "10",	is_int, "Std in a Gaussian Distribution to select random second stim time"),
		("variable_delaytime", "0",	is_boolean, "If 1 then second stimulus duration is picked from a gaussian distribution"),
		("mu_delaytime", "275",	is_int, "Mu in a Gaussian Distribution to select random delay to target onset"),
		("std_delaytime", "25",	is_int, "Std in a Gaussian Distribution to select random delay to target onset"),
		("targ_hold",	"50",	is_int, "Duration to fixate at target"),
		("min_err",	"0",	is_int),
		("max_err",	"10000",	is_int),
		("bg_before",	"(50,40,34)",is_color),
		("bg_during",	"(50,40,34)",is_color),
		("fixlag",	"50",	is_int),
		("fixwait",	"100",	is_int),
		("targ_winsize","70",	is_int,	"Target window size"),
		("targwait",	"50",	is_int,	"Duration to wait for passing through saccades"),
		("stim2winsz",	"30",	is_int, "Change this if you want to manually define the window for stim2"),
		("useLookUpTable", "1", is_int, "1:Use preselected non-match; 0:Use selected non-match"),
		("Pref_Stims", "[]", is_any, "Preferred stim number"),
		("Pref_Rots", "[]", is_any, "Preferred stim rotation"),
		("NonPref_Stims", "[]", is_any, "Non-preferred stim number"), 
		("NonPref_Rots", "[]", is_any, "Non-preferred stim rotation"),
		("StimX",	"0",	is_int, "RF X location"),
		("StimY",	"0",	is_int, "RF Y location"),
		("RFscale",	"0",	is_boolean, "1:Scale stimulus size by RF size; 0:Use SampleSize"),
		("RFscalefactor",	"0.625",	is_float, "If scale by RF size, what's the scale factor?"),
		("SampleSize",	"100",	is_int, "Sample stimulus size in pixels"),
		("SampleSizeFract", ".9", is_float, "Fraction of RF that the size of the stimulus is suppose to be."),
		("Pref_color", "(255,1,1)",	is_color, "Preferred color"),
		("NonPref_color", "(255,1,1)",	is_color, "Non-preferred color"),
		("Saccade_trial_prob","1.0",	is_float, "Fraction of trials on which saccade target is presented"),
		("Eye Params", None, None),
		("innerwin",	"0",	is_int),
		("track",	"0",	is_boolean),
		("track_xo",	"0",	is_int, "offset of track point"),
		("track_yo",	"0",	is_int, "offset of track point"),
		("track_color", "(255,255,0)",	is_color),
		("Misc Params", None, None, "Miscellaneous Parameters"),
		("Recent Buffer Size", "50", is_int, "The number of trials to use to calculate recent performance"),
		("pause_color", "(150,0,0)", is_color, "The screen will turn this color when the task is paused"),
		("breakerror_color", "(150,0,0)", is_color, "The screen will turn this color when breakfix on second stim"),
		("error_color", "(150,0,0)", is_color, "The screen will turn this color when animal gets error"),
		("repblocks", "10", is_int, "Total number of repetitions of each block of stims (length specified below)"),
		("redo_errors", "0", is_int,	"0: do not repeat error trials, 1:repeat errors"),
		("redo_breakfix", "1", is_int, "0:do not repeat breakfix trials, 1:repeat breakfix"),
		("redo_immediately", "0", is_int, "0:do not repeat immediately, 1:repeat immediately"),
		("ShowRFSprite", "0", is_boolean, "if 1 show the rf"),
		("randomize",	"1", is_int,	"randomize?"),
		("ShowNovel",	"0", is_int,	"Present novel shape/color combos in test mode (1), otherwise train mode (0)"),
		("Show2Combos",	"0", is_int,	"0: all combinations, 1: M only, 2: NM only, 3: PS/PC as ref, 4: NPS/NPC as ref"),
		("Block length", "100", is_int, "Length of block to be repeated (even numbers only)"),
		("% Novel Stims in Block", "0", is_int, "If testing, how much of the block should be novel stims?"),
		("Record File Params", None, None, "Params for setting name of record file"),
		("Use Special Name", "0", is_boolean, "If 1 then the record file name will be AnimalPrefixDate_TaskName_CellGroup_Iteration.rec"),
		("RFDirectory", "//home//shapelab//recordFiles//", is_any, "Directory to use for Record Files"),
		("AnimalPrefix", "o", is_any, "Animal Prefix to use"),
		("Date","080325", is_any, "Date to use "),
		("TaskName","aim2behrxthuman", is_any, "TaskName"),
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
