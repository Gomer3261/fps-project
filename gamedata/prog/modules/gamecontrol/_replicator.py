### ======------ The Replicator ------====== ###
INIT = 1

class REPLICATOR:
    """
    Reproduces the world depicted in the gamestate.
    """

    def run(self, con):
        import info
        if info.inGame:
            self.replicateLocalPlayer(con)
            self.replicatePlayers(con)
            self.replicateBots(con)

    def replicateLocalPlayer(self, con):
        import gamestate
        import info

        # Remember, the localPlayer doesn't delete themselves;
        # we have to do it here as a part of the replication.

        gamestate = gamestate.gamestate

        import modules.gamesystems.player as player

        playerIsAliveInGamestate = 0

        if gamestate.playerIsInGame(info.ticket):
            if gamestate.playerIsAlive(info.ticket):
                playerIsAliveInGamestate = 1
            else:
                playerIsAliveInGamestate = 0
        else:
            playerIsAliveInGamestate = 0

        if playerIsAliveInGamestate:
            if not player.handler:
                # Spawn player
                player.spawn(con)
        else:
            # Player is not alive in gamestate
            if player.handler:
                # player is alive in localgame
                # kill player.
                player.kill()
            

    def replicatePlayers(self, con):
        import gamestate
        import info
        import localgame

        gamestate = gamestate.gamestate

        # So, if we're in the game, and we've got a ticket
        if info.ticket:

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

        # We're gonna loop through each bot in the gamestate
        for ID in gamestate.contents["B"]:

            # If the bot isn't already in the localgame, add them.
            if ID not in localgame.bots.reps:
                localgame.bots.add(con, ID)

            # They delete themselves, so we don't worry about that.
        # Job done!

        
replicator = REPLICATOR()
