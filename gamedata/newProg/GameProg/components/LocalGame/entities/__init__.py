### Entities Subcomponent ###

import player

def spawnEntity(type, EID):
	entity = None
	if type == 'player':
		entity = player.Class(EID)
	return entity
