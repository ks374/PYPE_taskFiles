## WILSON TASK IMAGER
## jkb, 6/20/08

from pype import *
from Numeric import *
from random import *
from shapes import *
from wilson_shapes import *
from b8points import *
from fixationTask import fixationTask
from wilsonTask import *

def RunSet(app):
	app.taskObject.runSet(app)

def cleanup(app):
	app.taskObject.cleanup(app)

def main(app):
	app.taskObject = wilsonTask_imager(app)
	app.globals = Holder()
	app.idlefb()
	app.startfn = RunSet

class wilsonTask_imager(wilsonTask):       	# imager as subclass of wilsontask
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
		
		
		fbh = 200
		fbw = 200
		sqr_color = (255,255,255)
		sqr = 0
		circ = 0
		fb = quickinit(dpy=":0.0", w=fbw, h=fbh, bpp=32, flags=0)
		fb.clear(self.myBG)
		
		for j in arange(0,len(self.mySprites)):
			sprite = self.mySprites[j]
			subtended = self.subtended_idlist[j]
			rot = self.rot_idlist[j]
			mode = self.mode_idlist[j]
			
			print subtended
			print rot
			print mode
			
			imageName = "%s%s%s%03d_rot_%03d_mode_%02d%s" %(dir_name,dir_sep,file_pre,subtended,rot,mode,file_post)
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
