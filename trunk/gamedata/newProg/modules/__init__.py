import ai
import gamecontrol
import gamesystems
import interface
import items
import networking

import profiling
import time

def initLoop(con):
    gamesystems.mousetools.initLoop(con)
    gamesystems.ballistics.initLoop(con)
    interface.options.initLoop(con)
    interface.inputs.initLoop(con)
