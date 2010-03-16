### Entities ###

entityClasses = {}

# --- importing all entity types, this needs to be changed each time a new entity is added --- #
import base_entity; entityClasses["base_entity"] = base_entity.Class
import director; entityClasses["director"] = director.Class
import test; entityClasses["test"] = test.Class
import explorer; entityClasses["explorer"] = explorer.Class
import player; entityClasses["player"] = player.Class
import nanoshooter; entityClasses["nanoshooter"] = nanoshooter.Class



# --- giving clean access to entity classes --- #
def getEntityClass(type):
	return entityClasses[type]


print("LocalGame Entites seem happy and ready.")