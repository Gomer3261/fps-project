################################
### ------ inventory ------ ####
################################

# This module stores the INVENTORY class for managing items
from modules.items.data import *

class INVENTORY:
	"""Manages the player's items"""
	
	# Weapons
	primary = None
	secondary = None
	
	# Armor
	armor = None
	
	# Helmet
	helmet = None
	
	# Belt
	belt = None
	
	# Meds and grenades
	meds = []
	grenades = []
	
	# Ammo
	ammopile = AMMOPILE()
	
	def __init__(self):
		# We need a starting belt
		self.belt = BELT()
	
	def changePrimary(self, weapon):
		self.primary = weapon
		
	def changeSecondary(self, weapon):
		self.secondary = weapon
		
	def changeArmor(self, armor):
		self.armor = armor
		
	def changeHelmet(self, helm):
		self.helmet = helm
		
	def changeBelt(self, belt):
		self.belt = belt
		
	def addMed(self, med):
		if self.belt.medpackMax < len(self.belt.meds):
			self.meds.append(med)
		else:
			# Pass for now, but we need to raise an error
			pass 
		
	def addGrenade(self, gren):
		if self.belt.grenadeMax < len(self.belt.grenades):
			self.grenades.append(gren)
		else:
			# Pass for now, but we need to raise an error
			pass
			
	def addAmmo(self, bullet, number):
		name = self.bullet.name
		
		if name == "PTL":
			self.ammopile.ptl += number
		elif name == "STA":
			self.ammopile.sta += number
		elif name == "DMR":
			self.ammopile.dmr += number
		elif name == "AMR":
			self.ammopile.amr += number
