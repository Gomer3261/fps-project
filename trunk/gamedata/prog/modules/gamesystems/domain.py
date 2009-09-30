############################
### ------ domain ------ ###
############################
### Copyright 2009 Geoffrey Gollmer
INIT = 0

domains = {}









######   ####################   ######
####     ####################     ####
##       ### --- FACE --- ###       ##
###      ####################     ####
#####    ####################   ######


#The FACE class calculates a polygon based on four given 3D points.
#It contains functions that allow you to check if a 3D point is inside it's calculated polygon.
#use FACE.contains(position) to check if the position is inside the FACE object.
#use FACE.quickContains(position) to roughly check if the position is inside the FACE object. This function is 7x faster than contains().

class FACE:
	
	##  #################################  ##
	### ### --- Polygon variables --- ### ###
	##  #################################  ##
	
	
	
	#Vertex related variables.
	vertices = []
	
	#orgverts is a narsty little thing. It contains 3 lists of ordered numbers.
	#the first list is the vertices from highest to lowest x value.
	#the second list is the vertices from highest to lowest y value.
	#the third list is the vertices from highest to lowest z value.
	#
	#The given numbers from each list are the value for the vertex in vertices.
	#
	### --- so to get the highest x value I would use verts[orgverts[0][0]][0] --- ###
	#
	#I know it's gross, but it's the easiest way for me.
	orgverts = []
	
	#Side lists. Stores the two points that make up the sides.
	leftside = []
	rightside = []
	top = []
	bottom = []
	
	#Height variables.
	extraheight = 10
	height = [0, 10]
	
	#Polygon type variable (3 for tri, 4 for quad)
	sides = 4
	
	##  ########################  ##
	### ### --- __init__ --- ### ###
	##  ########################  ##
	
	#takes vertices and height values, and calculates the polygon. This saves a lot of processing power when using contains() and quickContains()
	def __init__(self, vertices, height=10):
		self.vertices = vertices
		self.extraheight = height
		self.calcSides()
	
	
	
	##  ##########################  ##
	### ### --- contains() --- ### ###
	##  ##########################  ##	
	
	#contains works by calculating intercepts from the given position to the sides of the polygon.
	#then it compares the given position to the intercepts to figure out if the given position is within the polygon.
	#it can cause slowdown when looping through many FACE objects.
	
	def contains(self, position):
		
		#calculating the top and bottom intercepts.
		toppoint = self.calcIntercept(self.top, position, 1)
		bottompoint = self.calcIntercept(self.bottom, position, 1)
		
		#this detects if your object is within the height range, before anything else is calculated. It's a nice calculation saver when it's false.	
		if not inRange(position[2], [self.height[0], self.height[1]]):
			return 0
		
		
		
		#if it's a four sided polygon this finds if the point is inside the polygon.
		elif self.sides == 4:
			#calculating the left and right intercepts.
			rightpoint = self.calcIntercept(self.rightside, position, 0)
			leftpoint = self.calcIntercept(self.leftside, position, 0)
			
			#checking if the position is between the interception points.
			#top > position > bottom and right > position > left	
			if inRange(position[0], [leftpoint[0], rightpoint[0]]) and inRange(position[0], [bottonpoint[1], toppoint[1]]):
				return 1
			else:
				return 0
		
		
		
		#this is for 3 sided polygons.
		else:
			#if it's a regular triangle
			if self.rightside == []:
				leftpoint = self.calcIntercept(self.leftside, position, 0)
				
				if inRange(position[1], [toppoint[1], bottompoint[1]]) and position[0] >= leftpoint[0]:
					return 1
				else:
					return 0
			
			#this is for when top or bottom end up vertical for one reason or another.
			else:
				rightpoint = self.calcIntercept(self.rightside, position, 0)
				
				if inRange(position[1], [toppoint[1], bottompoint[1]]) and position[0] <= rightpoint[0]:
					return 1
				else:
					return 0



					
	##  ###############################  ##
	### ### --- quickContains() --- ### ###
	##  ###############################  ##	
	
	#this is a faster algorythm for checking if a position is within a face.
	#It checks the bounding box rather than the actual 2D object.
	#this function is 7x faster last time I checked.
	
	def quickContains(self, position):
		
		#required variables.
		orgverts = self.orgverts
		verts = self.vertices
		
		#this detects if your object is within the height range, before anything else is calculated. It's a nice calculation saver when it's false.	
		if not inRange(position[2], [self.height[0], self.height[1]]):
			return 0
		
		#4 sided polygon bounding box search.
		if self.sides == 4:
			if inRange(position[0], [verts[orgverts[0][3]][0], verts[orgverts[0][0]][0]]) and inRange(position[1] [verts[orgverts[1][3]][1], verts[orgverts[1][0]][1]]):
				return 0
			else:
				return 1
		
		#3 sided polygon bounding box search.
		else:
			if inRange(position[0], [verts[orgverts[0][2]][0], verts[orgverts[0][0]][0]]) and inRange(position[1] [verts[orgverts[1][2]][1], verts[orgverts[1][0]][1]]):
				return 0
			else:
				return 1

		
				
				
	
	##  #########################################  ##
	### ### --- contain private functions --- ### ###
	##  #########################################  ##
	
	
	
	# ----------------------- #
	# --- calcIntercept() --- #
	# ----------------------- #
	#calculating the interception point for each side (direction is weither it uses x or y co-ordinates)
	
	def calcIntercept(self, side, position, direction):
		
		#if the line is straight
		if side[0][direction] == side[1][direction]:
			if direction == 0:
				return [side[0][direction], position[1], position[2]]
			else:
				return [position[0], side[0][direction], position[2]]
		
		#otherwise use slope y-intercept to figure it out.
		else:
			slope = (side[1][1]-side[0][1])/(side[1][0]-side[0][0])
			yint = side[0][1] + ((0 - side[0][0]) * slope)
			
			#if we are calculating for x
			if direction == 0:
				xpos = (position[1]-yint)/slope
				return [xpos, position[1], position[2]]
				
			#if we are calculating for y
			else:
				ypos = (slope*position[0]) + yint
				return [position[0], ypos, position[2]]
				
				
				
	# ----------------- #
	# --- inRange() --- #
	# ----------------- #
	#inRange() checks if a given value is between a list of 2 other given values.
	
	def inRange(value, range):
		if (value >= range[0] and value <= range[1]) or (value <= range[0] and value >= range[1]):
			return 1
		else:
			return 0
	
	
	
	##  ###########################  ##
	### ### --- calcSides() --- ### ###
	##  ###########################  ##
	
	#calcsSides sorts the verticies into self.orgverts
	#Then using orgverts calcSides check for certain polygon shapes that can ruin the basic algorythm.
	#Once that is done. calcSides find the left, right, top and bottom edges of the polygon, and saves them for later use.
	
	def calcSides(self):
		
		verts = self.vertices
		orgverts = [[], [], []]
		
		#organizing verts left-right, top-bottom
		orgverts = self.sortVerts(orgverts, 0)
		orgverts = self.sortVerts(orgverts, 1)
		orgverts = self.sortVerts(orgverts, 2)
		
		self.orgverts = orgverts
		
		#4 sided polygon.
		if len(self.vertices) == 4:
			self.sides = 4
			
			#calculating self.height based on the highest and lowest vertices in the polygon.
			self.height = [verts[orgverts[2][3]][2], verts[orgverts[2][0]][2] + self.extraheight]
			
			#calculating sides if the polygon is 4 sided.
			self.top = [verts[orgverts[1][0]],verts[orgverts[1][1]]]
			self.bottom = [verts[orgverts[1][3]],verts[orgverts[1][2]]]
			
			#this checks for a glitchy shape that used to ruin the algorythm.
			if (orgverts[0][0] == orgverts[1][0] and orgverts[0][1] == orgverts[1][1]) or (orgverts[0][0] == orgverts[1][1] and orgverts[0][1] == orgverts[1][0]) or (orgverts[0][0] == orgverts[1][2] and orgverts[0][1] == orgverts[1][3]) or (orgverts[0][0] == orgverts[1][3] and orgverts[0][1] == orgverts[1][2]):
				self.leftside = [verts[orgverts[0][3]],verts[orgverts[0][1]]]
				self.rightside = [verts[orgverts[0][0]],verts[orgverts[0][2]]]
			
			else:
				self.leftside = [verts[orgverts[0][3]],verts[orgverts[0][2]]]
				self.rightside = [verts[orgverts[0][0]],verts[orgverts[0][1]]]
		
		
		
		#3 sided polygon.
		else:
			self.sides = 3
			
			#calculating self.height based on the highest and lowest vertices in the polygon.
			self.height = [verts[orgverts[2][2]][2], verts[orgverts[2][0]][2] + self.extraheight]
			
			#calculating sides if the polygon is 3 sided
			self.rightside = [verts[orgverts[0][0]],verts[orgverts[0][1]]]
			
			#calculating top and bottom.
			if verts[orgverts[0][0]][1] >= verts[orgverts[0][1]][1]:
				self.top = [verts[orgverts[0][0]],verts[orgverts[0][2]]]
				self.bottom = [verts[orgverts[0][1]],verts[orgverts[0][2]]]
			else:
				self.top = [verts[orgverts[0][1]],verts[orgverts[0][2]]]
				self.bottom = [verts[orgverts[0][0]],verts[orgverts[0][2]]]
			
			#if top or bottom happen to be straight lines, it broke the script, this replaces the straight line with left side, and rightside becomes the replaced value.
			if self.top[0][0] == self.top[1][0]:
				self.leftside = self.top
				self.top = self.rightside
				self.rightside = []
			elif self.bottom[0][0] == self.bottom[1][0]:
				self.leftside = self.bottom
				self.bottom = self.rightside
				self.rightside = []
				
				
				
				
	##  ###########################################  ##
	### ### --- calcSides private functions --- ### ###
	##  ###########################################  ##
	
	# ----------------- #
	# --- sortVerts --- #
	# ----------------- #
	#sortVerts() calculates the 2nd value of a tuple from highest to lowest, then returns a list of the first terms in that order.
				
	#sorts the given list of tuples according to the second value of each.
	def sortVerts(self, orgverts, pos):
		import operator
		
		#calculating verts according to position (orgverts is the vertice order pos is weither it's based on x or y co-ordinates)
		for i in range(len(self.vertices)):
			orgverts[pos].append([self.vertices[i][pos], i])
		
		getcount = operator.itemgetter(0)
		orgverts[pos] = sorted(orgverts[pos], key=getcount)
		
		#sorted sorts from lowest to highest, I wanted highest to lowest, so I reverse the list.
		orgverts[pos].reverse()
		
		#trust me this needs to happen, deal with it.
		for i in range(len(self.vertices)):
			orgverts[pos][i] = orgverts[pos][i][1]
		
		return orgverts



######   ######################   ######
####     ######################     ####
##       ### --- DOMAIN --- ###       ##
###      ######################     ####
#####    ######################   ######

#this class holds a group of FACE objects and tools to search them.
class DOMAIN():
	
	faces = []
		
	def __init__(self, name, FACE):
		self.name = name
		self.FACE = FACE
	
	
	
	##  #######################  ##
	### ### --- addMesh --- ### ###
	##  #######################  ##
	
	#addMesh loops through all the faces in a MeshProxy, and converts them into FACE objects.
	def addMesh(self, obj, height):
		mesh = obj.meshes[0]
		for i in range(mesh.numPolygons):
			verts = []
			
			poly = mesh.getPolygon(i)
			for v in range(poly.getNumVertex()):
				vindex = poly.getVertexIndex(v)
				vertex = mesh.getVertex(0, vindex)
				vertpos = [vertex.x + obj.position[0], vertex.y + obj.position[1], vertex.z + obj.position[2]]
			verts.append(vertpos)
			face = self.FACE(verts, height)
		self.faces.append(face)
	
	
	
	##  ########################  ##
	### ### --- contains --- ### ###
	##  ########################  ##
	
	#contains loops through all the FACE objects stored in faces and checks if te given position is in one of them.
	def contains(self, position):
		for face in self.faces:
			if face.contains(position) == 1:
				return 1
		return 0
	
	
	
	##  #############################  ##
	### ### --- quickContains --- ### ###
	##  #############################  ##
	
	#quickcontains does the same thing as contains, but it uses a faster less accurate algorythm.
	def quickContains(self, position):
		for face in self.faces:
			if face.quickContains(position) == 1:
				return 1
		return 0




######   ##########################   ######
####     ##########################     ####
##       ### --- initiate() --- ###       ##
###      ##########################     ####
#####    ##########################   ######

#initiate is called at the beginning of the game. It searches the current scene for domain objects and creates python based domains out of it.
def initiate(scene):
	objects = scene.objects
	
	#for each object in the scene
	for obj in objects:
	
		#if the object is a domain
		if "domain" in obj.getPropertyNames():
		
			#if the domain exhists
			if obj["domain"] in domains:
			
				#add the objects mesh to domains.
				domains[obj["domain"]].addMesh(obj, obj["height"])
			
			else:
				#create a new domain for the object.
				domain = DOMAIN(obj["domain"], FACE)
				domain.addMesh(obj, obj["height"])
				domains[obj["domain"]] = domain




######   ######################   ######
####     ######################     ####
##       ### --- isIn() --- ###       ##
###      ######################     ####
#####    ######################   ######

#data can be a position (list of 3 floats) or a GameObject.
#if domain is left blank, a list of domains containing the object will be returned.

#isIn() is used to check if a position or an object is within the given domain name
def isIn(data, domain="", quick=0):
	
	#checks if data is a game object
	try:
		if data.isA("KX_GameObject"):
			position = data.position
	except:
		position = data
	
	#returns 1 if the object is in the domain, else returns 0
	if domain != "":
		if domain in domains:
			if quick == 0:
				return domains[domain].contains(position)
			else:
				return domains[domain].quickContains(position)
		else:
			return 0	
	
	#returns a list of domains the object is in.
	else:
		domainlist = []
		for domain in domains:
			if quick == 0:
				if domains[domain].contains(position) == 1:
					domainlist.append(domain)
			else:
				if domains[domain].quickContains(position) == 1:
					domainlist.append(domain)
		return domainlist


