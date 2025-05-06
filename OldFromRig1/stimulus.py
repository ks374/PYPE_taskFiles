## This is a general stimulus class for pype.
## Each stimulus object consists of a series of pype sprite objects
## each sprite has the following attributes:
##        1. Time of Onset
##            The time relative to the presentation of the stimulus
##            that the sprite becomes visible in ms.
##        2. Color
##            The RGB values for this sprite in list form
##
## Note that not all tasks that use these stimuli care about these values
##
## Stimulus objects can have the following attributes:
##        1. Mode
##            The Mode number associated with this stimulus type
##
##
## This class consists of a constructor and getter and setter methods
## for the variables in the class and the sprites.

## 03-12-08 Created Class - Phil


import sys, types
from pype import *

class stimulus:

    def __init__(self,mode,ID,rotation,submode=1):
        self.mySprites = list()
        self.mySpriteColors = list()
        self.mySpriteOnsets = list()
        self.myMode = mode
        self.myID = ID
        self.myRotation = rotation
        self.mySubmode = submode

    #creates a new stimulus object with *CLONES* of sprites
    def clone(self):
        stim = stimulus(self.myMode,self.myID,self.myRotation,self.mySubmode)
        for i in arange(0,self.numSprites()):
            s = self.getSprite(i)
            if(s is not None):
                stim.addSprite(s.clone(), self.getSpriteColor(i), self.getSpriteOnset(i))
        return stim

    def numSprites(self):
        return len(self.mySprites)

    #set sprite number i to sp
    #returns 1 if successful, None otherwise
    def setSprite(self,i, sp, sp_color, sp_onset):
        try:
            self.mySprites[i] = sp
            self.mySpriteColors[i] = sp_color
            self.mySpriteOnsets[i] = sp_onset
            return 1
        except:
            return None
            
    #add a sprite to this stimulus
    def addSprite(self,sp, sp_color, sp_onset=0):
        self.mySprites.append(sp)
        self.mySpriteColors.append(sp_color)
        self.mySpriteOnsets.append(sp_onset)

    def getSprite(self,i):
        try:
            return self.mySprites[i]

        except:
            return None

    def getSprites(self):
        try:
            return self.mySprites
        except:
            return None

    def getSpriteColor(self,i):
        try:
            return self.mySpriteColors[i]

        except:
            return None

    def getSpriteColors(self):
        try:
            return self.mySpriteColors

        except:
            return None
        
    def getSpriteOnset(self,i):
        try:
            return self.mySpriteOnsets[i]
        except:
            return None

    def getSpriteOnsets(self):
        try:
            return self.mySpriteOnsets
        except:
            return None

    def setSpriteOnset(self,i,new_onset):
        try:
            self.mySpriteOnsets[i] = new_onset
        except:
            pass

    def getSpritesWithOnsetLessThan(self,onset_time):
        spList = list()

        for spriteNum in range(0,self.numSprites()):
            if(self.mySpriteOnsets[spriteNum] < onset_time):
                spList.append(self.mySprites[spriteNum])

        return spList

    def getSpritesWithOnsetEqualTo(self,onset_time):
        spList = list()
        for spriteNum in range(0,self.numSprites()):
            if(self.mySpriteOnsets[spriteNum] == onset_time):
                spList.append(self.mySprites[spriteNum])

        return spList

    #rotates all sprites around themselves by rotation
    def rotateSprites(self,rotation):
        for i in arange(0,len(self.mySprites)):
            s = self.mySprites[i]
            s.rotate(rotation,0,1)

        

    def getStimulusMode(self):
        return self.myMode

    def getStimulusID(self):
        return self.myID

    def getStimulusRotation(self):
        return self.myRotation

    def getStimulusSubmode(self):
        return self.mySubmode


    def setStimulusMode(self,newVal):
        self.myMode = newVal

    def setStimulusID(self,newVal):
        self.myID = newVal

    def setStimulusRotation(self,newVal):
        self.myRotation = newVal

    def setStimulusSubmode(self,newVal):
        self.mySubmode = newVal


    #Turn all sprites off
    #returns 1 if successful, None otherwise
    def off(self):
        try:
            for i in range(0,self.numSprites()):
                self.mySprites[i].off()
            return 1
        except:
            return None

    #Turn all sprites on
    #returns 1 if successful, None otherwise
    def on(self):
        try:
            for i in range(1,self.numSprites()):
                self.mySprites[i].on()
            return 1
        except:
            return None

    #Turn sprite i off
    #returns 1 if successful, None otherwise
    def off_index(self,i):
        try:
            self.mySprites[i].off()
            return 1
        except:
            return None

    #Turn sprite i on
    #returns 1 if successful, None otherwise
    def on_index(self,i):
        try:
            self.mySprites[i].on()
            return 1
        except:
            return None

    def to_string(self):
        prtStr =  "Stimulus ID %d Mode %d Submode %d Rotation %d NumSprites%d" %(self.myID,self.myMode,self.mySubmode, self.myRotation, self.numSprites())
        return prtStr
