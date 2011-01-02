####################################
### ------	TERMINAL	  ------ ###
####################################
# This is the terminal module.
# It handles terminal input and output.

class initializeTerminal:
	
	import engine.interface.bgui as bgui
	
	def __init__(self, bgui):
		
		import engine.interface.terminal.commandsUser as commandsUser
		self.commandsUser = commandsUser
		import engine.interface.terminal.commandsAdmin as commandsAdmin
		self.commandsAdmin = commandsAdmin
		
		self.bgui = bgui
	
		# Terminal access activitiy.
		self.active = 0

		# The contents of the terminal window (output)
		self.openingText = """Welcome to the terminal!

Remember:
   Precede all python commands with a slash (/), otherwise it is regarded as a text message.

Important functions:
	/restoreDefaults() # Use this whenever things seem to be not working.
	/setSetting("username", "Stewart Walton") # Set your username.

================================================================"""

		self.openingText = self.openingText.replace("\r", "")
		self.contents = self.openingText.split("\n")
		self.oldcontents = []

		#history Object
		self.history = self.initializeHistory()

		self.wraplen = 100
		self.maxlines = 50
		
		self.gui = self.initializeGui(self.bgui)
		self.gui.display.text = '\n'.join(self.contents)
	
	##################################
	### ------ TERMINAL GUI ------ ###
	##################################
	
	class initializeGui(bgui.System):
		"""
		A bgui object created to display the terminal
		"""
		def __init__(self, bgui):
			bgui.System.__init__(self)
			
			self.frame = bgui.Frame(self, 'terminal', border=0)
			self.frame.colors = [(1, 1, 1, .8) for i in range(4)]
			
			self.display = bgui.TextBlock(self.frame, 'textblock', text="Error: empty text widget", color=(0, 0, 0, 1), pt_size=20, size=[0.95, 0.95], pos=[0, 0], options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
			
			self.input = bgui.TextInput(self.frame, 'input', text="", color=(0, 0, 0, 1), pt_size=20, size=[0.95, 0.05], pos=[.025, .05], options = bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX)
			
			self.focused_widget = self.input
			
			import bge
			self.keymap = {getattr(bge.events, val): getattr(bgui, val) for val in dir(bge.events) if val.endswith('KEY') or val.startswith('PAD')}
			
		def main(self):
			"""Method to be ran every frame"""
			import bge
			# Handle the keyboard
			keyboard = bge.logic.keyboard
			
			key_events = keyboard.events
			is_shifted = key_events[bge.events.LEFTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE or \
						key_events[bge.events.RIGHTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE
						
			for key, state in keyboard.events.items():
				if state == bge.logic.KX_INPUT_JUST_ACTIVATED:
					self.update_keyboard(self.keymap[key], is_shifted)
					
			bge.logic.getCurrentScene().post_draw = [self.render]
	
	######################################
	### ------ TERMINAL HISTORY ------ ###
	######################################
	
	class initializeHistory:
		"""
		Used to save and browse a list of strings without losing current data.
		The list is limited a certain number of strings, which can be changed.
		Primary use is for saving command history for the terminal.
		"""
		
		def __init__(self):
			# Variables for handling the history
			self.history = []
			self.slot = 0
			self.max = 10
			self.current_input = ""

		def add(self, s):
			"""
			Adds a string to the list of saved history.
			
			If there is too many strings stored in history, the oldest string is removed.
			"""

			self.history.insert(0, s)
			self.slot = -1
			
			if len(self.history) > self.max:
				self.history.remove(self.history[-1])

		def saveCurrentInput(self, s):
			"""
			Saves the current string so it can be recovered.
			"""
			self.current_input = s
		

		def getNextItem(self, s):
			"""
			Gets the next item in the history.
			"""
			self.slot += 1
			
			if self.slot == 0:
				self.saveCurrentInput(s)
			elif self.slot > self.max:
				self.slot = 0
			elif (len(self.history)-1) < self.slot:
				self.slot = len(self.history) - 1
				
			
			return self.history[self.slot]

		def getPrevItem(self):
			"""
			Gets the previous item in the history
			"""
			self.slot -= 1
			
			if self.slot < 0:
				self.slot = -1
				return self.current_input
			
			return self.history[self.slot]
			










	#########################################
	### ------ TERMINAL FORMATTING ------ ###
	#########################################

	def limit(self, x, l=10):
		"""
		Trims a list from the beginning until it reaches the desired length.
		"""
		while len(x) > l:
			x = x[1:]
		return x

	def formatLines(self, lines):
		"""
		Formats lines (wraps them, trims them)
		"""
		import textwrap
		newlines = []

		for line in lines:
			new = textwrap.fill(line, self.wraplen).split("\n")
			for n in new:
				newlines.append(n)

		newlines = self.limit(newlines, self.maxlines)

		return newlines










	########################################
	### ------ TERMINAL FUNCTIONS ------ ###
	########################################

	def input(self, s):
		"""
		runs input commands (maybe rename to run, or command?)
		"""
		isCommand = 0
		if s[0] == "/":
			isCommand = 1
		
		if isCommand:
			self.output(" ")
			self.output(">> "+s)
			s = s[1:]
			
			modules = [self.commandsUser, self.commandsAdmin]

			namespace = {}
			
			for module in modules:
				for variableName in dir(module):
					namespace[variableName] = getattr(module, variableName)

			import sys
			import traceback
			try:
				exec(s, namespace)
			except:
				exc_type, exc_value, exc_traceback = sys.exc_info()
				error = traceback.format_exception_only(exc_type, exc_value)
				error = error[len(error)-1]
				self.output(error)
				traceback.print_exc()
		
		else:
			#Network = self.slab
			#self.slab.Network.sendText(self.slab.Admin.UID, s)
			self.output(s)
			# Now we assume this is a text message....
			pass
			

	def output(self, s):
		"""
		Outputs something to the terminal.
		"""
		
		s = s.replace("\r", "")
		lines = s.split("\n")

		for line in lines:
			self.contents.append(line)

	def clear(self):
		"""
		Clears terminal's contents.
		"""
		self.contents = []










	###################################
	### ------ TERMINAL MAIN ------ ###
	###################################
	
	def main(self):
		import bge
		if self.active:
			self.gui.main()
			self.runTerminal()
		
		self.handleOpenClose()

		
			
	def handleOpenClose(self):
		"""
		This function handles opening and closing the terminal.
		Its called externally by a script running in the main scene.
		"""
		
		import bge

		if bge.logic.keyboard.events[bge.events.ACCENTGRAVEKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED:
			if self.active:
				self.gui.frame.visible = 0
				self.active = 0
				
			else:
				self.gui.frame.visible = 1
				self.gui.input.text = ""
				self.active = 1
				self.oldcontents = []



	def runTerminal(self):
		"""
		This function handles all actions to do with the terminal while it's open.
		Its called externally by a script running in the terminal scene.
		"""
		import bge
		
		enterKey = bge.logic.keyboard.events[bge.events.ENTERKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED
		upKey = bge.logic.keyboard.events[bge.events.UPARROWKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED
		downKey = bge.logic.keyboard.events[bge.events.DOWNARROWKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED
		delKey = bge.logic.keyboard.events[bge.events.DELKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED

		### INPUT HANDLING ###

		# Delete key clears input field
		if delKey:
			self.gui.input.text = ""
		
		# A = Input String
		s = self.gui.input.text
		
		if s and enterKey:
			self.input(s)
			self.gui.input.text = ""
			
			# Add the last input into the history
			self.history.add(s)

			
			
		elif upKey:
			self.gui.input.text = self.history.getNextItem(s)
		elif downKey:
			self.gui.input.text = self.history.getPrevItem()
		
		if self.oldcontents != self.contents:
			### OUTPUT HANDLING ###
			self.contents = self.formatLines(self.contents)
			output = "\n".join(self.contents)
			
			output = output.replace("\r", "")
			
			self.gui.display.text = output
			self.oldcontents = self.contents[:]
