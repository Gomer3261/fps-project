#############################
### ------ OPTIONS ------ ###
#############################
# This object handles the saving/loading of options.

class initializeOptions:
	"""
	The Options class collects, changes, and saves all user controlled settings & controls.
	It allows the user to change many aspects of the game to suit their personal preferences.
	"""
	import traceback
	


	#the init function. Most modules have this.
	def __init__(self, inputs):
		"""Init the module."""
		self.sepchar = "\n=------ Settings Above / Controls Below ------=\n\n" #this can actually be anything, it's just more eye pleasing if you open the file directly.
		self.path = "delta_options.txt" #the path for the options file (change it to something more game relative later?)
		self.settings = {}
		self.controls = {}
		
		self.inputs = inputs
		
		#####################
		### Defaults ########
		#####################
		
		defaultSettings = {}
		defaultControls = {}
		
		# SETTINGS
		defaultSettings["mxsens"] = 5.0
		defaultSettings["mysens"] = 5.0
		defaultSettings["inverty"] = 0
		defaultSettings["invertx"] = 0
		defaultSettings["filter-hdr"] = 0
		defaultSettings["lens"] = 15.0
		defaultSettings["crouch"] = "hold"
		defaultSettings["username"] = "-NoName-"
		
		# CONTROLS
		defaultControls["spawn"] = "space-key"
		defaultControls["suicide"] = "del-key"
		
		defaultControls["forward"] = "w-key"
		defaultControls["backward"] = "s-key"
		defaultControls["left"] = "a-key"
		defaultControls["right"] = "d-key"
		
		defaultControls["jump"] = "space-key"
		defaultControls["sprint"] = "leftshift-key"
		defaultControls["crouch"] = "leftctrl-key"
		
		defaultControls["rise"] = "e-key"
		defaultControls["sink"] = "q-key"

		defaultControls["use"] = "lmb"
		defaultControls["aim"] = "rmb"
		defaultControls["reload"] = "r-key"
		defaultControls["cock"] = "t-key"
		defaultControls["boltrelease"] = "f-key"

		defaultControls["interact"] = "e-key"
		
		defaultControls["menu"] = "tab-key"
		
		# Explorer Manipulation Mode
		defaultControls["remove-entity"] = "r-key"
		defaultControls["add-entity"] = "lmb"
		defaultControls["rotate-entity"] = "rmb"
		defaultControls["select-spawnpoint"] = "one-key"
		defaultControls["select-box"] = "two-key"
		
		self.defaultSettings = defaultSettings
		self.defaultControls = defaultControls
		
		#######################
		#######################
		#######################
		
		self.load()

	####################################
	### ------ OPTIONS SYSTEM ------ ###
	####################################
	
	def saveDefaults(self):
		"""
		Sets all controls and settings to default, then saves them all to the options file.
		"""
		try:
			self.settings = self.defaultSettings.copy()
			self.controls = self.defaultControls.copy()
			
			# Requesting a SAVE operation
			result = self.save()
			
			return result
		except:
			self.traceback.print_exc()

	def setSetting(self, key, value):
		"""
		sets the given setting to the given value, then saves the setting.
		"""
		key = key.lower()
		if key == "lens":
			if value > 25.0:
				value = 25.0
			elif value < 15.0:
				value = 15.0
		self.settings[key] = value
		r = self.save()
		return r

	def getSetting(self, key):
		key = key.lower()
		if key in self.settings:
			return self.settings[key]
		return None
	
	def defaultSetting(self, key):
		key = key.lower()
		if key in self.defaultSettings:
			self.settings[key] = self.defaultSettings[key]
			r = self.save()
			return r
		else:
			return -1

	def setControl(self, key, value):
		"""
		sets the given control to the given value, then saves the control.
		"""
		key = key.lower()
		self.controls[key] = value
		r = self.save()
		return r
	
	def getControl(self, key):
		key = key.lower()
		if key in self.controls:
			return self.controls[key]
		return None
		
	def defaultControl(self, key):
		key = key.lower()
		if key in self.defaultControls:
			self.controls[key] = self.defaultControls[key]
			r = self.save()
			return r
		else:
			return -1

	def save(self):
		"""
		saves current controls and settings to the options file.
		"""
		
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

			# Making changed options effect the game
			self.inputs.controller.setControls(self.controls)

			return 1
		except:
			self.traceback.print_exc()
			print("\n\n", self.settings, "\n\n", self.controls)
			return 0



	def load(self):
		"""
		loads all information from the options file.
		"""
		
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
			self.checkSettings()
			
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
			self.checkControls()
			
			self.inputs.controller.setControls(self.controls)
			
			return 1
		except:
			#self.traceback.print_exc()
			print("Interface/Options: Error loading; will attempt to save defaults and use those.")
			result = self.saveDefaults()
			if result:
				return 2 # This means the load failed, but the saving of defaults worked.
			return 0
	
	def checkSettings(self):
		for setting in self.defaultSettings:
			if not setting in self.settings:
				self.settings[setting] = self.defaultSettings[setting]

	def checkControls(self):
		for control in self.defaultControls:
			if not control in self.controls:
				self.controls[control] = self.defaultControls[control]
