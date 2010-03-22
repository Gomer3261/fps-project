### Entities ###

entityClasses = {}

# --- importing all entity types, this needs to be changed each time a new entity is added --- #
import base_entity; entityClasses["base_entity"] = base_entity.Class
import director; entityClasses["director"] = director.Class
import explorer; entityClasses["explorer"] = explorer.Class
import nanoshooter; entityClasses["nanoshooter"] = nanoshooter.Class



# --- giving clean access to entity classes --- #
def getEntityClass(type):
	return entityClasses[type]


print("LocalGame Entities seem happy and ready.")