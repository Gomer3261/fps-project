### 2D Filters! ###
# WIP!

FILTER_SYSTEM = False # Filter system is OFF. This code doesn't do anything right now.




HDR_active = False
HDR_step = 0
HDR_pixels = [0.0, 0.0, 0.0, 0.0, 0.0]
HDR_pass = 0
HDR_code = """
uniform sampler2D bgl_LuminanceTexture;
uniform sampler2D bgl_RenderedTexture;

uniform float avgL;
uniform float HDRamount;

vec2 texcoord = vec2(gl_TexCoord[0]).st;

void main(void)
{
	float contrast = avgL;
	float brightness = avgL * HDRamount;
	
	vec4 value =  texture2D(bgl_RenderedTexture, texcoord);
	
	gl_FragColor = (value/contrast)-brightness;
	gl_FragColor.a = 1.0;

}
"""








def run(con):
	global FILTER_SYSTEM
	if FILTER_SYSTEM:
		refreshFilterActivity(con)
		#own = con.owner
		#if own["HDR"]:
		if HDR_active:
			doLum(con)

def refreshFilterActivity(con):
	"""
	Turns filters on and off based on options.settings
	"""
	global HDR_active
	
	own = con.owner
	
	filterOn = con.actuators["filterOn"]
	filterOff = con.actuators["filterOff"]

	import modules
	options = modules.interface.options
	
	##########################################
	###======------ HDR FILTER ------======###
	##########################################
	
	if "filter-hdr" in options.settings:
		if options.settings["filter-hdr"]:
			### HDR needs to be activated ###
			#own["HDR"] = True
			if not HDR_active:
				print "ACTIVATING HDR"
				filterOn.shaderText = HDR_code
				filterOn.passNumber = HDR_pass
				con.activate(filterOn)
				HDR_active = True
		else:
			### HDR needs to be deactivated ###
			#own["HDR"] = False
			if HDR_active:
				print "DEACTIVATING HDR"
				filterOff.passNumber = HDR_pass
				con.activate(filterOff)
				HDR_active = False
	else:
		### HDR needs to be deactivated ###
		#own["HDR"] = False
		if HDR_active:
			print "DEACTIVATING HDR"
			filterOff.passNumber = HDR_pass
			con.activate(filterOff)
			HDR_active = False








### Lum: A lovely companion to HDR ###

def doLum(cont):
	print "LUM"
	import GameLogic as G
	import BGL
	import Rasterizer as R

	global HDR_step
	global HDR_pixels

	scene = G.getCurrentScene()
	objList = scene.objects
	own = cont.owner

	viewport = BGL.Buffer(BGL.GL_INT, 4)
	BGL.glGetIntegerv(BGL.GL_VIEWPORT, viewport);

	width = R.getWindowWidth()
	height = R.getWindowHeight()


	#this calculates the average pixel luminosity, calculating the luminosity
	#step 0 is an initiation step, it calculates all 5 pixels luminosity to give the filter a start point.
	if HDR_step == 0 or HDR_step == 1:
		x = viewport[0] + width/2
		y = viewport[1] + height/2

		pixel = BGL.Buffer(BGL.GL_FLOAT, [1])
		BGL.glReadPixels(x, y, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixel)

		HDR_pixels[0] = pixel[0]



	if HDR_step == 0 or HDR_step == 2:
		x = viewport[0] + width/3
		y = viewport[1] + height/3

		pixel = BGL.Buffer(BGL.GL_FLOAT, [1])
		BGL.glReadPixels(x, y, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixel)

		HDR_pixels[1] = pixel[0]



	if HDR_step == 0 or HDR_step == 3:
		x = viewport[0] + width/3
		y = viewport[1] + height/2

		pixel = BGL.Buffer(BGL.GL_FLOAT, [1])
		BGL.glReadPixels(x, y, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixel)

		HDR_pixels[2] = pixel[0]



	if HDR_step == 0 or HDR_step == 4:
		x = viewport[0] + width/2
		y = viewport[1] + height/2

		pixel = BGL.Buffer(BGL.GL_FLOAT, [1])
		BGL.glReadPixels(x, y, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixel)

		HDR_pixels[3] = pixel[0]



	if HDR_step == 0 or HDR_step == 5:
		x = viewport[0] + width/2
		y = viewport[1] + height/3

		pixel = BGL.Buffer(BGL.GL_FLOAT, [1])
		BGL.glReadPixels(x, y, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixel)

		HDR_pixels[4] = pixel[0]

		
	#step progression
	if HDR_step < 5:
		HDR_step += 1
	else:
		HDR_step = 1

		

	avgPixels = (HDR_pixels[0]+HDR_pixels[1]+HDR_pixels[2]+HDR_pixels[3]+HDR_pixels[4])/5.0

	#Slow adaptation
	eyeAdapt = 0.01
	own["avgL"] = (own["avgL"]*(1.0-eyeAdapt) + avgPixels*eyeAdapt)

	avgPixels = own["avgL"]

