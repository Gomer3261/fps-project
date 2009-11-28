### Entities ###

entityClasses = {}

# --- importing all entity types, this needs to be changed each time a new entity is added --- #
import BaseEntity; entityClasses["BaseEntity"] = BaseEntity.Class
import test; entityClasses["test"] = test.Class



# --- giving clean access to entity classes --- #
def getEntityClass(type):
	return entityClasses[type]