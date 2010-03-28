####################################
### ------	TERMINAL	  ------ ###
####################################
# This is the terminal module.
# It handles terminal input and output.

class Class:
	"""
	The Terminal class represents the programming side of the in game terminal.
	"""
	def __init__(self, slab):
		self.slab = slab
		# Terminal access activitiy.
		self.active = 0

		# The contents of the terminal window (output)
		self.openingText = """Welcome to the terminal!

Remember:
   Precede all python commands with a slash (/), otherwise it is regarded as a text message.

Important functions:
	/listUserCommands() # Lists the commands you can use.
	/help(cmd) # Use this to get help on a particular command.
	/defaultOptions() # Use this whenever things seem to be not working.
	/startServer() -- you should end the server before you hit escape.
	/endServer()
	/spawn('explorer') or /spawn('nanoshooter') or just spawn() -- which defaults to explorer.

================================================================"""

		self.openingText = self.openingText.replace("\r", "")
		self.contents = self.openingText.split("\n")
		self.oldcontents = []


		#History Object
		self.History = self.History()


		# For opening and closing the terminal (detects single presses)
		self.termkeyLast = 0

		self.wraplen = 100
		self.maxlines = 60
		
		print("Terminal's prepared.")
		
		



	######################################
	### ------ TERMINAL HISTORY ------ ###
	######################################
	
	class History:
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

	def input(self, s, slab=None):
		"""
		runs input commands (maybe rename to run, or command?)
		"""
		isCommand = 0
		if s[0] == "/":
			isCommand = 1
		
		if isCommand and slab != None:
			self.output(" ")
			self.output(">> "+s)
			s = s[1:]
			
			if not hasattr(self, "CommandsUser"):
				import CommandsUser as CommandsModuleUser; self.CommandsUser = CommandsModuleUser.Class(slab)
				import CommandsAdmin as CommandsModuleAdmin; self.CommandsAdmin = CommandsModuleAdmin.Class(slab)
			modules = [self.CommandsUser, self.CommandsAdmin]

			namespace = {}
			
			for module in modules:
				for variableName in dir(module):
					namespace[variableName] = getattr(module, variableName)

			import sys
			import traceback
			try:
				exec(s, namespace)
			except:
				error = traceback.format_exception_only(sys.exc_type, sys.exc_value)
				error = error[len(error)-1]
				self.output(error)
				traceback.print_exc()
		
		else:
			#Network = self.slab
			self.slab.Network.sendText(self.slab.Admin.UID, s)
			#self.output(s)
			# Now we assume this is a text message....
			#pass
			

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










	######################################
	### ------ TERMINAL HANDLER ------ ###
	######################################

	def runHandler(self, slab):
		"""
		This function handles all actions to do with the terminal while it's open.
		Its called externally by a script running in the terminal scene.
		"""
		
		if self.active:
			import GameLogic as gl
			
			con = gl.getCurrentController()
			
			returnKey = con.sensors["RETURN"]
			upKey = con.sensors["UP"]
			downKey = con.sensors["DOWN"]
			deleteKey = con.sensors["DELETE"]
		
			inTextObj = gl.getCurrentScene().objects["OBTerminal-inText"]
			outTextObj = gl.getCurrentScene().objects["OBTerminal-outText"]


			### INPUT HANDLING ###

			# Delete key clears input field
			if deleteKey.positive:
				inTextObj["input"] = ""
			
			# A = Input String
			A = inTextObj["input"]
			A = A.replace("\r", "")
			A = A.replace("\n", "")
			inTextObj["Text"] = A + "|"

			
			if A and returnKey.positive:
				self.input(A, slab)
				inTextObj["input"] = ""
				inTextObj["Text"] = ""
				
				# Add the last input into the history
				self.History.add(A)

				
				
			elif upKey.positive:
				inTextObj["input"] = self.History.getNextItem(A)
			elif downKey.positive:
				inTextObj["input"] = self.History.getPrevItem()
			
			if self.oldcontents != self.contents:
				### OUTPUT HANDLING ###
				self.contents = self.formatLines(self.contents)
				output = "\n".join(self.contents)
				
				output = output.replace("\r", "")
				
				outTextObj["Text"] = output
				self.oldcontents = self.contents[:]



	def handleOpenClose(self):
		"""
		This function handles opening and closing the terminal.
		Its called externally by a script running in the terminal scene.
		"""
		
		import GameLogic as gl
		con = gl.getCurrentController()
		
		termkey = con.sensors["TERMKEY"]

		if termkey.positive and (not self.termkeyLast):
			if self.active:
				closeTerminal = con.actuators["REMOVESCENE"]
				closeTerminal.scene = "Terminal"
				con.activate(closeTerminal)
				
				self.active = 0
			else:
				openTerminal = con.actuators["ADDOVERLAY"]
				openTerminal.scene = "Terminal"
				con.activate(openTerminal)
				
				self.active = 1
				self.oldcontents = []

		self.termkeyLast = termkey.positive
