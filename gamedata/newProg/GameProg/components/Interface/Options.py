#############################
### ------ OPTIONS ------ ###
#############################
### Copyright 2009 Chase Moskal!
# This object handles the saving/loading of options.

class Class:

	import traceback



	#the init function. Most modules have this.
	def __init__(self, inputs):
		"""Init the module."""
		self.sepchar = "\n=------ Settings Above / Controls Below ------=\n\n" #this can actually be anything, it's just more eye pleasing if you open the file directly.
		self.path = "FPS_options.txt" #the path for the options file (change it to something more game relative later?)
		self.settings = {}
		self.controls = {}
		
		self.inputs = inputs
		
		self.load()
		
		self.inputs.controller.setControls(self.controls)
		print("Options Initiated")











	####################################
	### ------ OPTIONS SYSTEM ------ ###
	####################################



	#Sets all controls and settings to default, then saves them all to the options file.
	def saveDefaults(self):
		
		try:
			settings = {}
			controls = {}
			
			# SETTINGS
			settings["mxsens"] = 5.0
			settings["mysens"] = 5.0
			settings["inverty"] = 0
			settings["invertx"] = 0
			settings["filter-hdr"] = 0
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
			
			
			self.settings = settings
			self.controls = controls
			
			# Requesting a SAVE operation
			result = self.save()
			
			return result
		except:
			self.traceback.print_exc()



	#sets the given setting to the given value, then saves the setting.
	def setSetting(self, key, value):
		key = key.lower()
		
		if key == "lens":
			if value > 25.0:
				value = 25.0
			elif value < 15.0:
				value = 15.0
		
		self.settings[key] = value
		

		
		r = self.save()
		return r



	#sets the given control to the given value, then saves the control.
	def setControl(self, key, value):
		
		key = key.lower()
		
		self.controls[key] = value
		r = save()
		return r



	#saves current controls to the options file.
	def save(self):
		
		import os
		
		try:
			#settings
			settingsfile = "// This is the options file for the FPS Project. You can reset these options to default by typing \"options default\" in the in-game terminal." + os.linesep + os.linesep
			for key in self.settings:
				settingsfile += key + ": " + repr(self.settings[key]) + os.linesep
			
			#controls
			controlsfile = ""
			for key in self.controls:
				controlsfile += key + ": " + repr(self.controls[key]) + os.linesep

			nativesepchar = self.sepchar.replace("\n", os.linesep)
			newfile = settingsfile + nativesepchar + controlsfile

			f = open(self.path, "w")
			f.write(newfile)
			f.close()

			print("Options Saved")

			#making changed options effect the game
			self.inputs.controller.setControls(self.controls)

			return 1
		except:
			self.traceback.print_exc()
			print("\n\n", self.settings, "\n\n", self.controls)
			return 0



	#loads all information from the options file.
	def load(self):
		
		try:
			f = open(self.path, "r")
			data = f.read()
			f.close()
			
			# Convert to clean
			data = data.replace("\r\n", "\n")
			data = data.replace("\r", "\n")
			
			# split into parts
			parts = data.split(self.sepchar)
			
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
			self.settings = statements
			
			# Controls
			lines = controlsfile.split("\n")
			statements = {}
			for line in lines:
				if line and not (line.find("//") != -1):
					parts = line.split(":")
					name = parts[0].strip().lower()
					value = parts[1].strip()
					statements[name] = eval(value)
			self.controls = statements
			
			print("Options Loaded")
			
			self.inputs.controller.setControls(self.controls)
			
			return 1
		except:
			self.traceback.print_exc()
			print("Error loading; will attempt to save defaults and use those")
			result = self.saveDefaults()
			if result:
				return 2 # This means the load failed, but the saving of defaults worked.
			return 0

