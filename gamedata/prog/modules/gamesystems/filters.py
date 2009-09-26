### 2D Filters! ###

#HDR globals
HDRstep = 0
HDRpixels = [0.0, 0.0, 0.0, 0.0, 0.0]

def run(con):
	"""
	Turns filters on and off based on options.settings
	"""
	own = con.owner

	import modules
	options = modules.interface.options

	if "filter-hdr" in options.settings:
		if options.settings["filter-hdr"]:
			own["HDR"] = True
		else:
			own["HDR"] = False
	else:
		own["HDR"] = False








### Lum: A lovely companion to HDR ###

def runLum(con):
	if con.owner["HDR"]:
		doLum(con)

def doLum(cont):
	import GameLogic as G
	import BGL
	import Rasterizer as R

	global HDRstep
	global HDRpixels

	scene = G.getCurrentScene()
	objList = scene.objects
	own = cont.owner

	viewport = BGL.Buffer(BGL.GL_INT, 4)
	BGL.glGetIntegerv(BGL.GL_VIEWPORT, viewport);

	width = R.getWindowWidth()
	height = R.getWindowHeight()


	#this calculates the average pixel luminosity, calculating the luminosity
	#step 0 is an initiation step, it calculates all 5 pixels luminosity to give the filter a start point.
	if HDRstep == 0 or HDRstep == 1:
		x = viewport[0] + width/2
		y = viewport[1] + height/2

		pixel = BGL.Buffer(BGL.GL_FLOAT, [1])
		BGL.glReadPixels(x, y, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixel)

		HDRpixels[0] = pixel[0]



	if HDRstep == 0 or HDRstep == 2:
		x = viewport[0] + width/3
		y = viewport[1] + height/3

		pixel = BGL.Buffer(BGL.GL_FLOAT, [1])
		BGL.glReadPixels(x, y, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixel)

		HDRpixels[1] = pixel[0]



	if HDRstep == 0 or HDRstep == 3:
		x = viewport[0] + width/3
		y = viewport[1] + height/2

		pixel = BGL.Buffer(BGL.GL_FLOAT, [1])
		BGL.glReadPixels(x, y, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixel)

		HDRpixels[2] = pixel[0]



	if HDRstep == 0 or HDRstep == 4:
		x = viewport[0] + width/2
		y = viewport[1] + height/2

		pixel = BGL.Buffer(BGL.GL_FLOAT, [1])
		BGL.glReadPixels(x, y, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixel)

		HDRpixels[3] = pixel[0]



	if HDRstep == 0 or HDRstep == 5:
		x = viewport[0] + width/2
		y = viewport[1] + height/3

		pixel = BGL.Buffer(BGL.GL_FLOAT, [1])
		BGL.glReadPixels(x, y, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixel)

		HDRpixels[4] = pixel[0]

		
	#step progression
	if HDRstep < 5:
		HDRstep += 1
	else:
		HDRstep = 1

		

	avgPixels = (HDRpixels[0]+HDRpixels[1]+HDRpixels[2]+HDRpixels[3]+HDRpixels[4])/5.0

	#Slow adaptation
	eyeAdapt = 0.01
	own["avgL"] = (own["avgL"]*(1.0-eyeAdapt) + avgPixels*eyeAdapt)

	avgPixels = own["avgL"]

