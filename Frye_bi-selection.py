import sys, types,os
from pype import *
import pygame as pg
import numpy as np
import random
import datetime

"""
	Show one picture in left or right. 
    Not show anything if the monkey's hand is left on the screen. 
    Delete line: self.myTaskParams.destroy(), which may prevent further task loading. 

	9/5/2025
	Chenghang
"""
def RunSet(app):
    app.taskObject.RunSet(app)

def cleanup(app):
    app.taskObject.cleanup(app)
    
def main(app):
    app.taskObject = TouchTask(app)
    app.globals = Holder() #A dummy object to hold parameters. 
    app.idlefb()
    app.startfn = RunSet

def gettouch(wait=999999):
    t = Timer()
    touch_x = None
    while touch_x is None:
        events = pg.event.get([FINGERDOWN])
        if len(events) > 0:
            event = events[0]
            touch_x = event.x * 1280-640
            touch_y = 360-event.y*720
        elif t.ms()>wait:
            touch_x = -9999
            touch_y = -9999
    return touch_x,touch_y

def touch_check(touch_x,touch_y,s,w,ref_is_left):
    #s for image size, w for window_size
    if ref_is_left == 1:
        Pos = (-300,0)
    elif ref_is_left == 0:
        Pos - (300,0)
    Pos = (0,0)
    image_size_half = (s/2,s/2)
    
    if (touch_x > (Pos[0]-image_size_half[0]-w)) and (touch_x <= (Pos[0]+image_size_half[0]+w)) and (touch_y > (Pos[1]-image_size_half[1]-w)) and (touch_y <= (Pos[1]+image_size_half[1]+w)):
        return 1
    else: 
        return 0
        

class TouchTask:
    def __init__(self,app):
        self.createParamTable(app)
        self.app = app
        self.mySprites = list() 
        self.stimid = list() 
        self.numStim = 0
        
    def createStimuli(self,app):
        gParam = app.getcommon() 
        self.params = self.myTaskParams.check()
        #Coordinate: 
        #X and Y full size is 1280*720. XY should be (X,Y), where (640,360) is the right bottom corner. 
        #Then the starting pixel coordinate for the compared picture is (-150,-330)
        #4 option pictures are (-624,31),(-308,31),(8,31),(324,31)
        
        stim_type = self.params['rand stimulus?']
        if stim_type == 0:
            stim_path = self.params['stim_path_blue']
        elif stim_type == 1:
            stim_path = self.params['stim_path_both']
        elif stim_type == 2:
            stim_path = self.params['stim_path_rand']
        else:
            con(app,"Error: Unknown stim_type!!!Using blue ball stim only","red")
            stim_path = self.params['stim_path_blue']
        
        stim_filenames = []
        stim_ids = []
        for file in os.listdir(stim_path):
            if file.endswith('.png'):
                stim_filenames.append(os.path.join(stim_path,file))
        if len(stim_filenames)==0:
            print('warning: no images loaded/n')
        stim_ids = np.unique(stim_filenames)
        self.numStim = len(stim_ids)
        con(app,f"Found {self.numStim} stimulus")
        
        #For N stimulus, we will have 3N sprites for each, the first one will be the 
        #reference location and the other 2 will be listed left and right. 
        #Currently all positions are hardcoded. 
        Cur_id = 0
        Pos_0 = (0,0)
        Pos_1 = (-300,0)
        Pos_2 = (300,0)
        
        for stim_filename in stim_filenames:
            img = Sprite(1,1,Pos_0[0],Pos_0[1],fb=app.fb,depth=1,on=0,centerorigin=1,fname=stim_filename)
            self.mySprites.append(img)
            self.stimid.append(Cur_id)
            Cur_id += 1
            img = Sprite(1,1,Pos_1[0],Pos_1[1],fb=app.fb,depth=1,on=0,centerorigin=1,fname=stim_filename)
            self.mySprites.append(img)
            self.stimid.append(Cur_id)
            Cur_id += 1
            img = Sprite(1,1,Pos_2[0],Pos_2[1],fb=app.fb,depth=1,on=0,centerorigin=1,fname=stim_filename)
            self.mySprites.append(img)
            self.stimid.append(Cur_id)
            Cur_id += 1
        con(app,f"Final Sprite list len is {len(self.mySprites)}")
            
        
    def createParamTable(self,app):
        P = app.getcommon()
        self.myTaskButton = app.taskbutton(text=__name__, check = 1)
        self.myTaskNotebook = DockWindow(title=__name__, checkbutton=self.myTaskButton)
        parfile = "%s.%s" % (app.taskname(), P['subject'])
        
        if parfile:
            parfile = parfile + '.par'
        
        self.myTaskParams = ParamTable(self.myTaskNotebook, (        
            ("Stim Presentation Params", None, None), 
            ("bg_before", "(10, 10, 10)", is_color, "The background color before stimulus presentation"),            
            ("bg_during", "(10, 10, 10)", is_color, "The background color during stimulus presentation"),
            ("stim_path_blue", "/home/shapelab/.pyperc/Tasks/Kiani_Stimuli/300/", is_any, "Directory where stimuli are stored"),    
            ("stim_path_both", "/home/shapelab/.pyperc/Tasks/Kiani_Stimuli/300/", is_any, "Directory where stimuli are stored"),
            ("stim_path_rand", "/home/shapelab/.pyperc/Tasks/Kiani_Stimuli/300/", is_any, "Directory where stimuli are stored"),    #MARK: need to correct this
            ("rand_stimulus?", "1", is_int, "0 for single blue ball image, 1 for random stimulus with blue ball, 2 for random stimulus without blue ball"),

            
            ("Task Params", None, None),
            ("Need_ref?", "0", is_int, "If 1, there will be ref first and then selection. Use 0 for early phase training. "),
            ("Ref_duration", "300", is_int, "During for the reference image to show up, default 300"),
            ("Ref_Stim_interval", "300", is_int, "Duration between reference image and stimulus showing up, default 300"),
            ("iti", "1500", is_int, "Inter-trial interval"),
            ("wait_duration","5000",is_int,"Monkey has to react during this period or no reward"),
            ("window_size","-10",is_int,"Tolerance window size for touch precision, positive=easy"),
            ("img_size","300",is_int,"Size of the stimulus image in pixel size, default 300"),
            #"stim_duration", "300", is_int, "Stimulus presentation time"),
            
            ("Reward Params", None, None),
            ("numdrops", "8", is_int, "Number of juice drops")
            ), file=parfile)

    def cleanup(self):
        #delete parameter table and anything else we created
        self.myTaskParams.save()
        self.myTaskButton.destroy()
        self.myTaskNotebook.destroy()
        #self.myTaskParams.destroy()
        del self.mySprites
    
    def toggle_photo_diode(self,app):
        app.globals.dlist.update()
        app.fb.sync_toggle()
    def turn_off_photo_diode(self,app):
        app.fb.sync(0)
    
    def RunSet(self,app):
        app.tally(clear=1)
        P = self.myTaskParams.check(mergewith=app.getcommon())
        parames = self.myTaskParams.check()
        
        self.total_num = 0
        self.suc_num = 0
        current_time = datetime.datetime.now()
        con(app,"Task start time = " + current_time.strftime("%H:%M:%S"))
        
        self.createStimuli(app)
        
        app.paused = 0
        app.running = 1
        app.led(1)
        
        app.globals.repnum = -1
        app.globals.ncorrect = 0
        app.globals.ntrials = 0
        app.globals.seqcorrect = 0
        #app.globals.uicount = 0
        #app.globals.stimCorrect = 0
        #app.globals.stimSeen = 0
        #pp.globals.yOffset = 600
        
        t = Timer()
        
            #Save recent success rate. 
        try:
            _,t = self.RunTrial(app,t)
        except UserAbort: 
            pass
        
        return 1
    
    def RunTrial(self,app,t):
        #P = self.myTaskParams.check(mergewith=app.getcommon())
        #params = self.myTaskParams.check()
        
        while app.running == 1:
            while app.paused == 1:
                app.idlefn(1000)
            _,t = self._RunTrial(app,t)
        
        return 1,t
        
    def _RunTrial(self,app,t):
        P = self.myTaskParams.check(mergewith=app.getcommon())
        self.params = self.myTaskParams.check()
        
        try:
            con(app,">------------------------------")
            con(app,"Next trial",'blue')
            
            app.udpy.display(None)
            
            app.globals.dlist = DisplayList(app.fb) #dlist manage all elements that will be shown on the screen. 
            
            app.globals.dlist.bg = self.params['bg_before']
            app.globals.dlist.update()
            app.fb.flip()
            
            #Then start the trial. 
            app.globals.dlist.bg = self.params['bg_during']
            app.globals.dlist.update()
            
            t.reset()
            app.idlefn(self.params['iti']-t.ms())
            
            app.fb.flip()
            
            #Now there should be nothing on the screen. The program should wait if the monkey is touching the screen. 
            pygame.event.clear()
            is_touching = 1
            while is_touching:
                touch_x,touch_y = gettouch(100)
                if touch_x == -9999:
                    is_touching = 0
                else:
                    con(app,"The monkey keeps his hand on the screen. Stop him! ", 'red')
                    app.idlefn(1000)

            pygame.event.clear()
            #Show reference image first: 
            if self.params['Need_ref?'] == 1:
                ref_id = random.randint(1,self.numStim)
            elif self.params['Need_ref?']==0:
                ref_id = 0
            else:
                con(app,"Rrong Need_ref? parameter, will not use reference image")
                ref_id = 0
            if ref_id != 0:
                #Render reference image first: 
                ref_id_present = ref_id*3-2
                self.mySprites[ref_id_present].scale(self.params['img_size'],self.params['img_size'])
                self.mySprites[ref_id_present].on()
                app.globals.dlist.update()
                app.fb.flip()

                app.idlefn(self.params['Ref_duration'])
                self.mySprites[ref_id_present].off()
                app.globals.dlist.update()
                app.fb.flip()

                touch_x,touch_y = gettouch(100)
                if touch_x != -9999:
                    con(app,"The monkey probably incorrectly touched the reference image",'red')

                app.idlefn(self.params['Ref_Stim_interval'])
                

            #Stimulus showing up
            if ref_id == 0: #Note: this is a temp solution. Show the ref pic if there is one. 
                ref_id = random.randint(1,self.numStim)
            stim_is_left = random.randint(1,2)-1
            ref_id_present = ref_id*3 - stim_is_left
            self.mySprites[ref_id_present].scale(self.params['img_size'],self.params['img_size'])
            self.mySprites[ref_id_present].on()
            app.globals.dlist.update()

            pygame.event.clear()
            app.fb.flip()
            
            result = None

            touch_x,touch_y = gettouch(self.params['wait_duration'])
            self.mySprites[ref_id_present].off()
            app.globals.dlist.update()
            app.fb.flip()
            result = touch_check(touch_x,touch_y,self.params['img_size'],self.params['window_size'],stim_is_left)

            app.globals.dlist = DisplayList(app.fb) #Reset the displaylist. This is unnecessary but just in case somebody change the code without carefully manage the dlist. 
            app.globals.dlist.bg = self.params['bg_before']
            app.globals.dlist.update()
            app.fb.flip()
            if result == 1:
                con(app,"Giving reward...")
                clk_num = self.params['numdrops']
                while clk_num > 0:
                    app.reward(multiplier = 1)
                    app.idlefn(100)
                    clk_num -= 1
                self.suc_num += 1
            else:
                con(app,"Wrong, no reward",'red')

            self.total_num  += 1
            con(app,f"Success number / total number: {self.suc_num}/{self.total_num}")
            return result,t
        except UserAbort: 
            app.globals.dlist.bg = params['bg_before']
            app.fb.flip()
            con(app,"Aborted. ",'red')
            return result,t
