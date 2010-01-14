####################################
### ------	TERMINAL	  ------ ###
####################################
# This is the terminal module.
# It handles terminal input and output.

class Class:
	def __init__(self):
		# Terminal access activitiy.
		self.active = 0

		# The contents of the terminal window (output)
		self.openingText = """Welcome to the terminal!
The game's programming is currently undergoing a revolution; many terminal commands will not function as described because we are currently working on their implementation.

Remember:
   Precede all python commands with a slash (/), otherwise it is regarded as a text message.

Important functions:
	/defaultOptions() # Use this whenever things seem to be not working.
	/listUserCommands()
	/help(cmd)
	/connect("YourName", stokes) # 'stokes' is the server, you can also use 'chase' or 'geoff'
	/disconnect() # disconnects you from the gameplay server.
	/users() # outputs a list of users in the game.
	/players() # outputs a list of players currently alive.
	/info() # gives you game information.

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
		
		



	######################################
	### ------ TERMINAL HISTORY ------ ###
	######################################
	
	class History:
		
		def __init__(self):
			# Variables for handling the history
			self.history = []
			self.slot = 0
			self.max = 10
			self.current_input = ""

		# Saves a string to the history
		def add(self, s):

			self.history.insert(0, s)
			self.slot = -1
			
			if len(self.history) > self.max:
				self.history.remove(self.history[-1])

		# Saves the current input so it can be recovered
		def saveCurrentInput(self, s):
			self.current_input = s

		# Gets the next item in the history

		def getNextItem(self, s):
			self.slot += 1
			
			if self.slot == 0:
				self.saveCurrentInput(s)
			elif self.slot > self.max:
				self.slot = 0
			elif (len(self.history)-1) < self.slot:
				self.slot = len(self.history) - 1
				
			
			return self.history[self.slot]

		# Gets the previous item in the history
		def getPrevItem(self):
			self.slot -= 1
			
			if self.slot < 0:
				self.slot = -1
				return self.current_input
			
			return self.history[self.slot]
		
		











	#########################################
	### ------ TERMINAL FORMATTING ------ ###
	#########################################

	# Trims a list from the beginning until it reaches the desired length.
	def limit(self, x, l=10):
		while len(x) > l:
			x = x[1:]
		return x

	# Formats lines (wraps them, trims them)
	def formatLines(self, lines):
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

	# runs input commands (maybe rename to run, or command?)
	def input(self, s, slab=None):
		isCommand = 0
		if s[0] == "/":
			isCommand = 1
		
		if isCommand and slab != None:
			self.output(" ")
			self.output(">> "+s)
			s = s[1:]
			
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
		
		else:
			self.output(s)

	# Outputs something to the terminal.
	def output(self, s):
		
		s = s.replace("\r", "")
		lines = s.split("\n")

		for line in lines:
			self.contents.append(line)

	# Clears terminal's contents.
	def clear(self):
		self.contents = []










	######################################
	### ------ TERMINAL HANDLER ------ ###
	######################################

	def runHandler(self, slab):
		
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