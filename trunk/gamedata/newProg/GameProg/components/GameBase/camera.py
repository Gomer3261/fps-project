### The Camera Subcomponent ###
class Class:
	def __init__(self, GameBaseCont):
		self.ecam = GameBaseCont.actuators["ecam"].owner
	
	def run(self, LocalGame, Interface):
		"""
		
		Args:
			 - LocalGame component
			 - Interface component
		"""
		import GameLogic
		scene = GameLogic.getCurrentScene()
		
		# Getting the 
		player = LocalGame.players.getLocalPlayer()
		explorer = LocalGame.explorers.getExplorer()
		
		cam = self.ecam
		
		if explorer:
			if explorer.alive:
				cam = explorer.fpcam
				cam.lens = Interface.options.settings["lens"]
		
		if player:
			if player.alive:
				cam = player.fpcam
				cam.lens = Interface.options.settings["lens"]
		
		scene.active_camera = cam
