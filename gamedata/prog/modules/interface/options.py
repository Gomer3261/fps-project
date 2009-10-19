#############################
### ------ OPTIONS ------ ###
#############################
### Copyright 2009 Chase Moskal!
# This object handles the saving/loading of options.

INIT = 0

import traceback

sepchar = "\n=------ Settings Above / Controls Below ------=\n\n" #this can actually be anything, it's just more eye pleasing if you open the file directly.
path = "FPS_options.txt" #the path for the options file (change it to something more game relative later?)
settings = {}
controls = {}

#the init function. Most modules have this.
def init():
	"""Init the module."""
	global INIT
	load()
	INIT = 1
	print "Options Initiated"

#checks if the module is initiated, ignoring it if it is, and initating it if it isn't.
def initLoop(con):
	global INIT
	if not INIT:
		init()











####################################
### ------ OPTIONS SYSTEM ------ ###
####################################



#Sets all controls and settings to default, then saves them all to the options file.
def saveDefaults():
	global sepchar
	global path
	global settings
	global controls
	global traceback
	
	try:
		settings = {}
		controls = {}
		
		# SETTINGS
		settings["mxsens"] = 5.0
		settings["mysens"] = 5.0
		settings["inverty"] = 0
		settings["invertx"] = 0
		settings["filter-hdr"] = 1
		settings["lens"] = 15.0
		settings["crouch"] = "Hold" # should be changed to lowercase
		
		# CONTROLS
		controls["spawn"] = "space-key"
		controls["suicide"] = "del-key"
		
		controls["forward"] = "w-key"
		controls["backward"] = "s-key"
		controls["left"] = "a-key"
		controls["right"] = "d-key"
		
		controls["jump"] = "space-key"
		controls["sprint"] = "leftshift-key"
		controls["crouch"] = "leftctrl-key"
		
		controls["rise"] = "e-key"
		controls["sink"] = "q-key"
	
		controls["use"] = "lmb"
		controls["aim"] = "rmb"
		controls["reload"] = "r-key"
		controls["cock"] = "t-key"
		controls["boltrelease"] = "f-key"
	
		controls["interact"] = "e-key"
		
		controls["menu"] = "tab-key"
		
		
		
		# Requesting a SAVE operation
		result = save()
		
		return result
	except:
		traceback.print_exc()



#sets the given setting to the given value, then saves the setting.
def setSetting(key, value):
	global sepchar
	global path
	global settings
	global controls
	global traceback
	
	key = key.lower()
	
	if key == "lens":
		if value > 25.0:
			value = 25.0
		elif value < 15.0:
			value = 15.0
		settings[key] = value
	
	else:
		settings[key] = value
	
	r = save()
	return r



#sets the given control to the given value, then saves the control.
def setControl(key, value):
	global sepchar
	global path
	global settings
	global controls
	global traceback
	
	key = key.lower()
	
	controls[key] = value
	r = save()
	return r



#saves current controls to the options file.
def save():
	global sepchar
	global path
	global settings
	global controls
	global traceback
	
	import os
	
	try:
		#settings
		settingsfile = "// This is the options file for the FPS Project. You can reset these options to default by typing \"options default\" in the in-game terminal." + os.linesep + os.linesep
		for key in settings:
			settingsfile += key + ": " + repr(settings[key]) + os.linesep
		
		#controls
		controlsfile = ""
		for key in controls:
			controlsfile += key + ": " + repr(controls[key]) + os.linesep

		nativesepchar = sepchar.replace("\n", os.linesep)
		newfile = settingsfile + nativesepchar + controlsfile

		f = open(path, "w")
		f.write(newfile)
		f.close()

		print("Options Saved")

		#making changed options effect the game
		import inputs
		if inputs.INIT:
			inputs.controller.setControls(controls)

		return 1
	except:
		traceback.print_exc()
		print "\n\n", settings, "\n\n", controls
		return 0



#loads all information from the options file.
def load():
	global sepchar
	global path
	global settings
	global controls
	global traceback
	
	try:
		f = open(path, "r")
		data = f.read()
		f.close()
		
		# Convert to clean
		data = data.replace("\r\n", "\n")
		data = data.replace("\r", "\n")
		
		# split into parts
		parts = data.split(sepchar)
		
		settingsfile = parts[0]
		controlsfile = parts[1]
		
		# Settings
		lines = settingsfile.split("\n")
		statements = {}
		for line in lines:
			if line and not (line.find("//") != -1):
				parts = line.split(":")
				name = parts[0].strip().lower()
				value = parts[1].strip()
				statements[name] = eval(value)
		settings = statements
		
		# Controls
		lines = controlsfile.split("\n")
		statements = {}
		for line in lines:
			if line and not (line.find("//") != -1):
				parts = line.split(":")
				name = parts[0].strip().lower()
				value = parts[1].strip()
				statements[name] = eval(value)
		controls = statements
		
		print "Options Loaded"
		
		import inputs
		if inputs.INIT:
			inputs.controller.setControls(controls)
		
		return 1
	except:
		traceback.print_exc()
		print "Error loading; will attempt to save defaults and use those"
		result = saveDefaults()
		if result:
			return 2 # This means the load failed, but the saving of defaults worked.
		return 0

