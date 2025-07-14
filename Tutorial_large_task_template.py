import sys, types,os
from pype import *
import pygame as pg

"""
	The purpose of this file is to get a task template inlcuding most functions. 
    
    Everytime you need to develop a task from scratch, you may need to refer to this template. 

	7/7/2024
	Chenghang
"""
def RunSet(app):
    app.taskObject.RunSet(app)

def cleanup(app):
    app.taskObject.cleanup(app)
    
def main(app):
    app.taskObject = fixationTask(app)
    app.globals = Holder() #A dummy object to hold parameters. 
    app.idlefb()
    app.startfn = RunSet
	



class fixationTask:
"""
    We use fixation task as an example here. 
    After clicking Start, runSet will be called to setup the task. 
    Then it will call runTrial, which is the mainloop. 
    _runTrial will contain task content for each loop. 
    You will also need a set of functions to save the outcome of each file. 
"""

    def __init__(self,app):
        self.createParamTable(app)
        self.app = app
        self.mySprites = list() #You want a variable to save your sprites. 
        self.stimid = list() #And manage them properly. 
        self.numStim = 0
        
    def createStimuli(self,app):
    """
        You will want to prepare your stimuli spirtes into a list or dictionary and save them properly in the memory. 
        So that you can fetch them quickly in the mainloop. 
        After this fucntion you need to update self.mySprites, self.stimid, and self.numStim. 
    """
        #Something you usually need: 
        gParam = app.getcommon() #You usually need this to get the ppd value. 
        self.params = self.myTaskParams.check()
        #myBG = self.params['bg_during']
        #myX = self.params['RF_center_X']
        s = Sprite(XXX)
        for i in range(Your_total_stimulus_numner):
            self.mySprites.append(s)
            self.stimid.append(i)
            self.numStim += 1
            
        #Don't forget to deal with nBlanks and randomizations. 
        
    def createParamTable(self,app):
    """
        You need a well labeled and organized parameter table. 
    """
        

    def cleanup(self):
        #delete parameter table and anything else we created
        self.myTaskParams.destroy()

    def RunSet(self,app):
    	"""
	This is what is run when you hit the 'start' button (set as such in
	the 'main' function, defined at the end of this file).
	"""
	con(app,"Experiment start...\n")
	while True:
		UserInput = input("Num_drop = ")
		if UserInput > 0:
			for i in range(UserInput):
				app.reward(multiplier=5)
				app.idlefn(50)#time between juice drops
			UserInput = 0
		else:
			break;

