############################
### ------ domain ------ ###
############################
### Copyright 2009 Geoffrey Gollmer
INIT = 0

domains = {}










####################
### --- FACE --- ###
####################
#This class is used to store, and calculate face data.
#To create the function is requires a list of 3 or 4 positions for vertices and a height value(int)
#The only real function that should be used outside of __init__() is contains()
#contains() takes a position and outputs 1 if it is within the polygon, 0 if it's not.

#the face class contains everything actually important to this module. I would suggest you just hide.
class FACE:
    
    vertices = []
    
    sides = 4

    extraheight = 10
    height = [0, 10]

    leftside = []
    rightside = []
    top = []
    bottom = []
    
    def __init__(self, vertices, height=10):
        self.vertices = vertices
        self.extraheight = height
        self.calcSides()
	
	
	
	#this is a faster algorythm for checking if a position is within a face.
	#It checks the bounding box rather than the actual 2D object.
	#this function is 7x faster last time I checked.
    def quickContains(self, position):
        #quick contains checks if the position is within the highest and lowest values on the x any y axis
        #essentially using a bounding box for the calculation, which should speed up the search dramatically.
        
        orgverts = self.orgverts
        verts = self.vertices
		
		

        #this detects if your object is within the height range, before anything else is calculated. It's a nice calculation saver when it's false.
        if position[2] < self.height[0] or position[2] > self.height[1]:
            return 0
			
			

        #4 sided polygon bounding box search.
        if len(self.vertices) == 4:
            if position[0] >= verts[orgverts[0][3]][0] and position[0] <= verts[orgverts[0][0]][0] and position[1] >= verts[orgverts[1][3]][1] and position[1] <= verts[orgverts[1][0]][1]:
                return 1
            else:
                return 0
				
				
				
        #3 sided polygon bounding box search.
        else:
            if position[0] >= verts[orgverts[0][2]][0] and position[0] <= verts[orgverts[0][0]][0] and position[1] >= verts[orgverts[1][2]][1] and position[1] <= verts[orgverts[1][0]][1]:
                return 1
            else:
                return 0
        


	#contains works by calculating the intercepts with the sides of the polygon
	#then it compares the position to the intercepts to figure out if it is within the polygon.
	#it can be very slow with large domains.
    def contains(self, position):
        #this is the function you need to worry about after creating the object.
        #calculating the top and bottom intercepts.
        toppoint = self.calcIntercept(self.top, position, 1)
        bottompoint = self.calcIntercept(self.bottom, position, 1)
		
		
		
        #this detects if your object is within the height range, before anything else is calculated. It's a nice calculation saver when it's false.
        if position[2] < self.height[0] or position[2] > self.height[1]:
            return 0
			
			

        #if it's a four sided polygon this finds if the point is inside the polygon.
        elif len(self.vertices) == 4:
			
			#calculating the left and right intercepts.
            rightpoint = self.calcIntercept(self.rightside, position, 0)
            leftpoint = self.calcIntercept(self.leftside, position, 0)
			
			

            #checking if the position is between the interception points.
			#top > position > bottom, right > position > left
            if (position[0] >= leftpoint[0] and position[0] <= rightpoint[0]) or (position[0] <= leftpoint[0] and position[0] >= rightpoint[0]):
                if (position[1] <= toppoint[1] and position[1] >= bottompoint[1]) or (position[1] >= toppoint[1] and position[1] <= bottompoint[1]):
                    return 1
                else:
                    return 0
            else:
                return 0
				
				
		
        #this is for 3 sided polygons.
        else:
		
		
		
            #if it's a regular triangle
            if self.rightside == []:
                leftpoint = self.calcIntercept(self.leftside, position, 0)
                
                if position[0] >= leftpoint[0]:
                    if (position[1] <= toppoint[1] and position[1] >= bottompoint[1]) or (position[1] >= toppoint[1] and position[1] <= bottompoint[1]):
                        return 1
                    else:
                        return 0
                else:
                    return 0
					
			
            #this is for when top or bottom end up vertical for one reason or another.
            else:
                rightpoint = self.calcIntercept(self.rightside, position, 0)

                if position[0] <= rightpoint[0]:
                    if (position[1] <= toppoint[1] and position[1] >= bottompoint[1]) or (position[1] >= toppoint[1] and position[1] <= bottompoint[1]):
                        return 1
                    else:
                        return 0
                else:
                    return 0

                

    def calcIntercept(self, side, position, direction):
        #calculating the interception point for each side (direction is weither it uses x or y co-ordinates)
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

    
	
	#figures out what verticies are used for each side.
    def calcSides(self):
        verts = self.vertices
        orgverts = [[], [], []]
        #organizing verts left-right, top-bottom
        orgverts = self.sortVerts(orgverts, 0)
        orgverts = self.sortVerts(orgverts, 1)
        orgverts = self.sortVerts(orgverts, 2)

        self.orgverts = orgverts

        if len(self.vertices) == 4:

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


        
        else:

            self.height = [verts[orgverts[2][2]][2], verts[orgverts[2][0]][2] + self.extraheight]
            
            #calculating sides if the polygon is 3 sided
            self.rightside = [verts[orgverts[0][0]],verts[orgverts[0][1]]]

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










######################
### --- DOMAIN --- ###
######################

#this class holds a group of FACE objects and tools to search them.
class DOMAIN():
    
    faces = []
    
    def __init__(self, name, FACE):
        self.name = name
        self.FACE = FACE
    
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
	
	#contains loops through all the FACE objects stored in faces and checks if te given position is in one of them.
    def contains(self, position):
        for face in self.faces:
            if face.contains(position) == 1:
                return 1
        return 0
	
	#quickcontains does the same thing as contains, but it uses a faster less accurate algorythm.
    def quickContains(self, position):
        for face in self.faces:
            if face.quickContains(position) == 1:
                return 1
        return 0










##########################
### --- initiate() --- ###
##########################

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
				
				
				
				
				
            




######################
### --- isIn() --- ###
######################
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


