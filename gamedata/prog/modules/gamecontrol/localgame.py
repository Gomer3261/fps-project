### LOCAL GAME ###
"""
Creates and stores representatives of the objects described by the
GameState. The Replicator (in director) is what controls these classes.
"""

class REPS:
    name = "Rep"
    objName = "playerRep"
    reps = {}

    def add(self, con, ID, startPosition=[0.0, 0.0, 0.0]):
        import GameLogic
        scene = GameLogic.getCurrentScene()
        
        print "%s added: %s"%(self.name, ticket)
        rep = scene.addObject(self.objName, con.owner)
        
        rep.position = startPosition
        rep["ticket"] = ID
        rep["ID"] = ID
        self.reps[ID] = rep
        return 1

    def remove(self, ID):
        rep = self.reps[ID]
        rep.endObject()
        print "%s removed: %s"%(self.name, ID)
        del self.reps[ID]



class PLAYERS(REPS):
    name = "Player Representative"
    objName = "playerRep"
players = PLAYERS()

class BOTS(REPS):
    name = "Bot"
    objName = "bot"
bots = BOTS()
