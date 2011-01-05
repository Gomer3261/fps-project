####################################
### ------	TERMINAL	  ------ ###
####################################
# This is the terminal module.
# It handles terminal input and output.
import engine.interface.bgui as bgui

class initializeTerminal(bgui.System):
	
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

================================================================\n"""

		self.openingText = self.openingText.replace("\r", "")

		##Bgui initialization
		bgui.System.__init__(self)
			
		self.frame = bgui.Frame(self, 'terminal', border=0)
		self.frame.colors = [(1, 1, 1, .8) for i in range(4)]
			
		self.display = bgui.TextBlock(self.frame, 'textblock', text=self.openingText, color=(0, 0, 0, 1), pt_size=20, size=[0.95, 0.94], pos=[0, 0.035],
			options=bgui.BGUI_DEFAULT | bgui.BGUI_CENTERX, overflow=bgui.BGUI_OVERFLOW_REPLACE)
			
		self.input = bgui.TextInput(self.frame, 'input', text="", prefix=">>>", color=(0, 0, 0, 1), pt_size=20, size=[0.95, 0.025], pos=[0.025, 0.025], options = bgui.BGUI_DEFAULT)
		self.input.on_enter = self.on_enter
		
		import bge
		self.keymap = {getattr(bge.events, val): getattr(bgui, val) for val in dir(bge.events) if val.endswith('KEY') or val.startswith('PAD')}
		
		#history Object
		self.history = self.initializeHistory()
	
	
	
	
	
	
	
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









	########################################
	### ------ TERMINAL FUNCTIONS ------ ###
	########################################
	
	def output(self, s):
		"""
		Outputs something to the terminal.
		"""
		
		s = s.replace("\r", "")
		self.display.text += s

	def clear(self):
		"""
		Clears terminal's contents.
		"""
		self.display.text = self.openingText









	###################################
	### ------ TERMINAL MAIN ------ ###
	###################################
	
	def main(self):
		"""
		Main terminal script, renders the terminal, handles actions, and opens/closes the terminal.
		"""
		if self.active:
			
			self.handleGui()
			self.handleActions()
		
		self.handleOpenClose()

	def handleGui(self):
		"""
		Renders the terminal and handle inputs.
		"""
		import bge
		self.focused_widget = self.input
		# Handle the keyboard
		keyboard = bge.logic.keyboard
		
		key_events = keyboard.events
		is_shifted = key_events[bge.events.LEFTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE or \
					key_events[bge.events.RIGHTSHIFTKEY] == bge.logic.KX_INPUT_ACTIVE
					
		for key, state in keyboard.events.items():
			if state == bge.logic.KX_INPUT_JUST_ACTIVATED:
				self.update_keyboard(self.keymap[key], is_shifted)
				
		bge.logic.getCurrentScene().post_draw = [self.render]
			
	def handleOpenClose(self):
		"""
		This function handles opening and closing the terminal.
		Its called externally by a script running in the main scene.
		"""
		
		import bge

		if bge.logic.keyboard.events[bge.events.ACCENTGRAVEKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED:
			if self.active:
				self.frame.visible = 0
				self.active = 0
				
			else:
				self.frame.visible = 1
				self.input.text = ""
				self.active = 1

	def handleActions(self):
		"""
		This function handles all custom actions to do with the terminal while it's open.
		"""
		import bge
		
		upKey = bge.logic.keyboard.events[bge.events.UPARROWKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED
		downKey = bge.logic.keyboard.events[bge.events.DOWNARROWKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED
		delKey = bge.logic.keyboard.events[bge.events.DELKEY] == bge.logic.KX_INPUT_JUST_ACTIVATED

		# Delete key clears input field
		if delKey:
			self.input.text = ""
		elif upKey:
			self.input.text = self.history.getNextItem(self.input.text)
			self.input.pos = len(self.input.text)
		elif downKey:
			self.input.text = self.history.getPrevItem()
			self.input.pos = len(self.input.text)







	####################################
	### ------ BGUI CALLBACKS ------ ###
	####################################

	def on_enter(self, input):
		"""
		runs when enter key is hit in input from bgui
		"""
		if input.text != "":
			self.output("\n ")
			self.output(">>> "+input.text+"\n")
			
			modules = [self.commandsUser, self.commandsAdmin]

			namespace = {}
			
			for module in modules:
				for variableName in dir(module):
					namespace[variableName] = getattr(module, variableName)

			import sys
			import traceback
			try:
				exec(input.text, namespace)
			except:
				exc_type, exc_value, exc_traceback = sys.exc_info()
				error = traceback.format_exception_only(exc_type, exc_value)
				error = error[len(error)-1]
				self.output(error)
				traceback.print_exc()
			
			self.history.add(input.text)
			input.text = ""
				
			