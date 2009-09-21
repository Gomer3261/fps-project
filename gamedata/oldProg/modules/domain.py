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

class FACE:
    
    vertices = []
    
    sides = 4

    extraHeight = 10
    height = [0, 10]

    leftSide = []
    rightSide = []
    top = []
    bottom = []
    
    def __init__(self, vertices, height=10):
        self.vertices = vertices
        self.extraHeight = height
        self.calcSides()

    def quickContains(self, position):
        #quick contains checks if the position is within the highest and lowest values on the x any y axis
        #essentially using a bounding box for the calculation, which should speed up the search dramatically.
        
        orgVerts = self.orgVerts
        verts = self.vertices

        #this detects if your object is within the height range, before anything else is calculated. It's a nice calculation saver when it's false.
        if position[2] < self.height[0] or position[2] > self.height[1]:
            return 0

        #4 sided polygon bounding box search.
        if len(self.vertices) == 4:
            if position[0] >= verts[orgVerts[0][3]][0] and position[0] <= verts[orgVerts[0][0]][0] and position[1] >= verts[orgVerts[1][3]][1] and position[1] <= verts[orgVerts[1][0]][1]:
                return 1
            else:
                return 0
        #3 sided polygon bounding box search.
        else:
            if position[0] >= verts[orgVerts[0][2]][0] and position[0] <= verts[orgVerts[0][0]][0] and position[1] >= verts[orgVerts[1][2]][1] and position[1] <= verts[orgVerts[1][0]][1]:
                return 1
            else:
                return 0
        

    def contains(self, position):
        #this is the function you need to worry about after creating the object. No other function should ever need to be called.
        
        topPoint = self.calcIntercept(self.top, position, 1)
        bottomPoint = self.calcIntercept(self.bottom, position, 1)

        #this detects if your object is within the height range, before anything else is calculated. It's a nice calculation saver when it's false.
        if position[2] < self.height[0] or position[2] > self.height[1]:
            return 0

        #if it's a four sided polygon this finds if the point is inside the polygon.
        elif len(self.vertices) == 4:

            rightPoint = self.calcIntercept(self.rightSide, position, 0)
            leftPoint = self.calcIntercept(self.leftSide, position, 0)

            #checking if the position is between the interception points.
            if (position[0] >= leftPoint[0] and position[0] <= rightPoint[0]) or (position[0] <= leftPoint[0] and position[0] >= rightPoint[0]):
                if (position[1] <= topPoint[1] and position[1] >= bottomPoint[1]) or (position[1] >= topPoint[1] and position[1] <= bottomPoint[1]):
                    return 1
                else:
                    return 0
            else:
                return 0
        #this is for 3 sided polygons.
        else:
            #if it's a regular triangle
            if self.rightSide == []:
                leftPoint = self.calcIntercept(self.leftSide, position, 0)
                
                if position[0] >= leftPoint[0]:
                    if (position[1] <= topPoint[1] and position[1] >= bottomPoint[1]) or (position[1] >= topPoint[1] and position[1] <= bottomPoint[1]):
                        return 1
                    else:
                        return 0
                else:
                    return 0
            #this is for when top or bottom end up vertical for one reason or another.
            else:
                rightpoint = self.calcIntercept(self.rightSide, position, 0)

                if position[0] <= rightPoint[0]:
                    if (position[1] <= topPoint[1] and position[1] >= bottomPoint[1]) or (position[1] >= topPoint[1] and position[1] <= bottomPoint[1]):
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
            yInt = side[0][1] + ((0 - side[0][0]) * slope)
            #if we are calculating for x
            if direction == 0:
                xPos = (position[1]-yInt)/slope
                return [xPos, position[1], position[2]]
            #if we are calculating for y
            else:
                yPos = (slope*position[0]) + yInt
                return [position[0], yPos, position[2]]

            

    def sortVerts(self, orgVerts, pos):
        import operator
        #calculating verts according to position (orgverts is the vertice order pos is weither it's based on x or y co-ordinates)
        for i in range(len(self.vertices)):
            orgVerts[pos].append([self.vertices[i][pos], i])
        
        getCount = operator.itemgetter(0)
        orgVerts[pos] = sorted(orgVerts[pos], key=getCount)

        #sorted sorts from lowest to highest, I wanted highest to lowest, so I reverse the list.
        orgCerts[pos].reverse()

        #trust me this needs to happen, deal with it.
        for i in range(len(self.vertices)):
            orgVerts[pos][i] = orgVerts[pos][i][1]
        
        return orgVerts

    

    def calcSides(self):
        verts = self.vertices
        orgVerts = [[], [], []]
        #organizing verts left-right, top-bottom, high-low
        orgVerts = self.sortVerts(orgVerts, 0)
        orgVerts = self.sortVerts(orgVerts, 1)
        orgVerts = self.sortVerts(orgVerts, 2)

        self.orgVerts = orgVerts

        if len(self.vertices) == 4:

            self.height = [verts[orgVerts[2][3]][2], verts[orgVerts[2][0]][2] + self.extraHeight]
            
            #calculating sides if the polygon is 4 sided.
            self.top = [verts[orgVerts[1][0]],verts[orgVerts[1][1]]]
            self.bottom = [verts[orgVerts[1][3]],verts[orgVerts[1][2]]]

            if (orgVerts[0][0] == orgVerts[1][0] and orgVerts[0][1] == orgVerts[1][1]) or (orgVerts[0][0] == orgVerts[1][1] and orgVerts[0][1] == orgVerts[1][0]) or (orgVerts[0][0] == orgVerts[1][2] and orgVerts[0][1] == orgVerts[1][3]) or (orgVerts[0][0] == orgVerts[1][3] and orgVerts[0][1] == orgVerts[1][2]):
                self.leftSide = [verts[orgVerts[0][3]],verts[orgVerts[0][1]]]
                self.rightSide = [verts[orgVerts[0][0]],verts[orgVerts[0][2]]]

            else:
                self.leftSide = [verts[orgVerts[0][3]],verts[orgVerts[0][2]]]
                self.rightSide = [verts[orgVerts[0][0]],verts[orgVerts[0][1]]]


        
        else:

            self.height = [verts[orgVerts[2][2]][2], verts[orgVerts[2][0]][2] + self.extraHeight]
            
            #calculating sides if the polygon is 3 sided
            self.rightSide = [verts[orgVerts[0][0]],verts[orgVerts[0][1]]]

            if verts[orgVerts[0][0]][1] >= verts[orgVerts[0][1]][1]:
                self.top = [verts[orgVerts[0][0]],verts[orgVerts[0][2]]]
                self.bottom = [verts[orgVerts[0][1]],verts[orgVerts[0][2]]]
            else:
                self.top = [verts[orgVerts[0][1]],verts[orgVerts[0][2]]]
                self.bottom = [verts[orgVerts[0][0]],verts[orgVerts[0][2]]]

            #if top or bottom happen to be straight lines, it broke the script, this replaces the straight line with left side, and rightside becomes the replaced value.
            if self.top[0][0] == self.top[1][0]:
                self.leftSide = self.top
                self.top = self.rightSide
                self.rightSide = []

            elif self.bottom[0][0] == self.bottom[1][0]:
                self.leftSide = self.bottom
                self.bottom = self.Rightside
                self.rightside = []



######################
### --- DOMAIN --- ###
######################

class DOMAIN():
    
    faces = []
    
    def __init__(self, name, FACE):
        self.name = name
        self.FACE = FACE
    
    def addMesh(self, obj, height):
        mesh = obj.meshes[0]
        for i in range(mesh.numPolygons):
            verts = []
           
            poly = mesh.getPolygon(i)
            for v in range(poly.getNumVertex()):
                vIndex = poly.getVertexIndex(v)
                vertex = mesh.getVertex(0, vIndex)
                vertPos = [vertex.x + obj.position[0], vertex.y + obj.position[1], vertex.z + obj.position[2]]
                verts.append(vertPos)
            face = self.FACE(verts, height)
            self.faces.append(face)

    def contains(self, position):
        for face in self.faces:
            if face.contains(position) == 1:
                return 1
        return 0

    def quickContains(self, position):
        for face in self.faces:
            if face.quickContains(position) == 1:
                return 1
        return 0

##########################
### --- initiate() --- ###
##########################

def initiate(scene):
    objects = scene.objects

    for obj in objects:
        if "domain" in obj.getPropertyNames():
            if obj["domain"] in domains:
                domains[obj["domain"]].addMesh(obj, obj["height"])
            else:
                domain = DOMAIN(obj["domain"], FACE)
                domain.addMesh(obj, obj["height"])
                domains[obj["domain"]] = domain
            

######################
### --- isIn() --- ###
######################
#data can be a position (list of 3 floats) or a GameObject.
#if domain is left blank, a list of domains containing the object will be returned.

def isIn(data, domain="", quick=0):
    try:
        if data.isA("KX_GameObject"):
            position = data.position
    except:
        position = data

    if domain != "":
        if domain in domains:
            if quick == 0:
                return domains[domain].contains(position)
            else:
                return domains[domain].quickContains(position)
        else:
            return 0
    else:
        domainList = []
        for domain in domains:
            if quick == 0:
                if domains[domain].contains(position) == 1:
                    domainList.append(domain)
            else:
                if domains[domain].quickContains(position) == 1:
                    domainList.append(domain)
        return domainList


