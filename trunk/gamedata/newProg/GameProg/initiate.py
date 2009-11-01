### GameProg Initiations ###
"""
These functions initiate components, saving their instances to the slab.
It's okay if they are called multiple times; it only works the first time anyway.
"""

def Ai(cont):
	from components import Ai
	import slab
	if not hasattr(slab, "Ai"): slab.Ai = Ai.Class(cont)

def Director(cont):
	from components import Director
	import slab
	if not hasattr(slab, "Director"): slab.Director = Director.Class(cont)

def GameBase(cont):
	from components import GameBase
	import slab
	if not hasattr(slab, "GameBase"): slab.GameBase = GameBase.Class(cont)

def GameState(cont):
	from components import GameState
	import slab
	if not hasattr(slab, "GameState"): slab.GameState = GameState.Class(cont)

def Gui(cont):
	from components import Gui
	import slab
	if not hasattr(slab, "Gui"): slab.Gui = Gui.Class(cont)

def Interface(cont):
	from components import Interface
	import slab
	if not hasattr(slab, "Interface"): slab.Interface = Interface.Class(cont)

def LocalGame(cont):
	from components import LocalGame
	import slab
	if not hasattr(slab, "LocalGame"): slab.LocalGame = LocalGame.Class(cont)

def Networking(cont):
	from components import Networking
	import slab
	if not hasattr(slab, "Networking"): slab.Networking = Networking.Class(cont)

def Resources(cont):
	from components import Resources
	import slab
	if not hasattr(slab, "Resources"): slab.Resources = Resources.Class(cont)

def Tools(cont):
	from components import Tools
	import slab
	if not hasattr(slab, "Tools"): slab.Tools = Tools.Class(cont)
