### GameProg Initiations ###
"""
These functions initiate components, saving their instances to the slab.
It's okay if they are called multiple times; it only works the first time anyway.
"""

def GameGoodies(cont):
	from components import GameGoodies
	import slab
	if not hasattr(slab, "GameGoodies"): slab.GameGoodies = GameGoodies.Class(cont)

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

def Networking(cont):
	from components import Networking
	import slab
	if not hasattr(slab, "Networking"): slab.Networking = Networking.Class(cont)

def Resources(cont):
	from components import Resources
	import slab
	if not hasattr(slab, "Resources"): slab.Resources = Resources.Class(cont)