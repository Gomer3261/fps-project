### ################################## ###
### ### ------ THE DIRECTOR ------ ### ###
### ################################## ###
INIT = 1

"""
There are two jobs that the Director is in charge of:
    - Modifying the Gamestate with changes
    - Replicating the gamestate to the local game
"""

def run(con):
    global router
    global replicator

    router.run(con)
    replicator.run(con)





### ======------ The Router ------====== ###

class ROUTER:
    """
    Takes requests to make changes to the gamestate,
    and either sends it straight to the local gamestate (when you are host),
    or sends it to a remote gamestate over the internet.
    """
    sendRequests = []
    throwRequests = []

    def reset(self):
        self.sendRequests = []
        self.throwRequests = []

    def weAreGamestateOwner(self):
        import info
        owner = 0
        if info.mode == "online":
            owner = 0
        else:
            owner = 1
        return owner

    def send(self, change):
        self.sendRequests.append(change)

    def throw(self, change):
        self.throwRequests.append(change)

    def run(self, con):
        if self.sendRequests or self.throwRequests:
            if self.weAreGamestateOwner():
                # Send stuff directly to our local gamestate
                import gamestate
                gamestate = gamestate.gamestate
                if self.sendRequests:
                    gamestate.applyChanges(self.sendRequests)
                if self.throwRequests:
                    gamestate.applyChanges(self.throwRequests)
            else:
                # Send the requests to the remote host
                print "Supposed to be sending stuff to remote host..."
            
            self.reset()

router = ROUTER()




### ======------ The Replicator ------====== ###

class REPLICATOR:
    """
    Reproduces the world depicted in the gamestate.
    """

    def run(self, con):
        self.replicatePlayers(con)
        self.replicateBots(con)

    def replicatePlayers(self, con):
        import gamestate
        import info
        import localgame

        gamestate = gamestate.gamestate

        # So, if we're in the game, and we've got a ticket
        if info.inGame and info.ticket:

            # Then we're gonna loop through each player in the gamestate
            for ticket in gamestate.contents["P"]:

                # If the player isn't me, and they aren't already in the localgame, and they are alive,
                if (ticket != info.ticket) and (ticket not in localgame.players.reps) and gamestate.playerIsAlive(ticket):
                    # Then we add them!
                    localgame.players.add(con, ticket)

                # They delete themselves, so we don't need to worry about that :D

        # Job done!

    def replicateBots(self, con):
        import gamestate
        import info
        import localgame

        gamestate = gamestate.gamestate

        # So, if we're in the game
        if info.inGame:

            # We're gonna loop through each bot in the gamestate
            for ID in gamestate.contents["B"]:

                # If the bot isn't already in the localgame, add them.
                if ID not in localgame.bots.reps:
                    localgame.bots.add(con, ID)

                # They delete themselves, so we don't worry about that.
        # Job done!

        
replicator = REPLICATOR()
