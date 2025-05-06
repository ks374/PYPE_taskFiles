## CUE TASK IMAGER
## jkb, 6/20/08

from pype import *
from Numeric import *
from random import *
from shapes import *
from cue_shapes import *
from b8points import *
from colors import *
from fixationTask import fixationTask
from cueTask import *

def RunSet(app):
	app.taskObject.runSet(app)

def cleanup(app):
	app.taskObject.cleanup(app)

def main(app):
	app.taskObject = cueTask_imager(app)
	app.globals = Holder()
	app.idlefb()
	app.startfn = RunSet

class cueTask_imager(cueTask):       	# imager as subclass of cuetask
	def __init__(self, app):         	# constructor stuff. this happens as soon as instantiated.
		self.createParamTable(app)
		self.app = app
		self.mySprites = list()      	# this will be list of sprite objects
		self.numStim = 0				# WHAT IS THIS? num stim?
		self.mySpriteList = list()   	# spritelist is index into sprite lists
		self.spriteColors = list()
	
	def runSet(self,app):
		params = self.myTaskParams.check()
		dir_name = "./images/extra"
		file_pre = "stim_"
		file_post = ".tif"
		dir_sep = "/"
	
		self.createStimuli(app)
		
		
		fbh = 175
		fbw = 175
		sqr_color = (255,255,255)
		sqr = 0
		circ = 0
		fb = quickinit(dpy=":0.0", w=fbw, h=fbh, bpp=32, flags=0)
		fb.clear(self.myBG)
		
		for j in arange(0,len(self.mySprites)):
			sprite = self.mySprites[j]
			mode = self.cue_idlist[j]
			submode = self.perispace_idlist[j]
			rot = self.rot_idlist[j]
			stimIDtemp = self.b8_idlist[j]
			list51= list([5,6,7,10,11] + range(14,40) +[41,42,46,47,50])
			stimID=list51[stimIDtemp]
# 			if(mode == 0):
# 				modeDir = "Contour"
# 			elif(mode == 1):
# 				modeDir = "Dots"
# 			elif(mode == 2):
# 				modeDir = "Tlines"
# 			else:
# 				modeDir = "Unknown"
			print rot
			print mode
			print submode
			print stimID
			imageName = "%s%s%s%03d_rot_%03d_mode_%02d_submode_%04d%s" % (dir_name,dir_sep,file_pre,stimID,rot,mode,submode,file_post)
			print imageName
			sprite.moveto(0,0)
			sprite.on()
			sprite.blit(fb=fb)
			if(sqr):
				fb.rectangle(0,0,self.radius-1,self.radius-1, sqr_color,1)
			if(circ):
				fb.circle(0,0,self.radius,sqr_color,1)
			fb.flip()
			fb.snapshot(imageName)
			fb.flip()
			sprite.off()
			fb.clear(self.myBG)


# This is also something that all tasks have, and it's a python thing.
# Don't touch it.
if not __name__ == '__main__':
	loadwarn(__name__)
else:
	dump(sys.argv[1])
