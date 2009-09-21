#################################
### ------ Pathfinding ------ ###
#################################
### Copyright 2009 Chase Moskal!
# This contains the PATHFINDER class,
# which contains classes for NODE and PATH.
# It's for A* pathfinding.

# Starts initiated...
INIT = 1




class PATHFINDER:
    import math

    class NODE:
        def __init__(self, PATHFINDER, position, adjacentpos):
            self.PATHFINDER = PATHFINDER

            self.position = position
            self.adjacentpos = adjacentpos
            self.parent = None
            self.adjacent = []
            
            self.G = 0
            self.H = 0
            self.F = 0

        def getG(self):
            PATHFINDER = self.PATHFINDER
            
            node = self
            G = 0.0
            run = 1
            while run:
                if node.parent:
                    G += PATHFINDER.getRealDistance(node.position, node.parent.position)
                    node = node.parent
                else:
                    run = 0
            return G

        def evaluate(self, targetNode):
            PATHFINDER = self.PATHFINDER
            
            G = self.getG()
            H = PATHFINDER.getRealDistance(self.position, targetNode.position)
            F = G+H
            
            self.G = G
            self.H = H
            self.F = F
            
            return F, G, H
                
        
        def fastEvaluate(self, startNode, targetNode):
            PATHFINDER = self.PATHFINDER
            G = PATHFINDER.getRealDistance(startNode.position, self.position)
            H = PATHFINDER.getRealDistance(self.position, targetNode.position)
            F = G+H
            
            self.G = G
            self.H = H
            self.F = F
            
            return F, G, H


    
    class PATH:
        def __init__(self, startpos, targetpos, startNode, targetNode, OPEN, CLOSED):
            self.OPEN = OPEN
            self.CLOSED = CLOSED

            self.startpos = startpos
            self.targetpos = targetpos
            
            self.nodes = []
            
            self.nodes.append(targetNode)
            node = targetNode
            
            run = 1
            while run == 1:
                if node.parent:
                    node = node.parent
                    self.nodes.append(node)
                else:
                    run = 0
            
            self.nodes.reverse()
            
            self.path = self.getPath()
            
        def getPath(self):
            path = []
            path.append(self.startpos)
            for node in self.nodes:
                path.append(node.position)
            path.append(self.targetpos)
            return path


    # Compiles the adjacents for each node in a list.
    def compileAdjacents(self, nodes):
        for node in nodes:
            adjacent = []
            for targetnode in nodes:
                if targetnode.position in node.adjacentpos:
                    adjacent.append(targetnode)
            node.adjacent = adjacent
            

    

    # Takes in a vertinfolist and converts it into a list of node objects.
    def NodemeshToNodes(self, nodemesh):
        nodes = []
        for vertinfo in nodemesh:
            position = vertinfo[0]
            adjacentpos = vertinfo[1]
            node = self.NODE(self, position, adjacentpos)
            nodes.append(node)
        self.compileAdjacents(nodes)
        return nodes


    # Evaluates vertinfolist from string form.
    def stringToNodemesh(self, string):
        # Converting to unix flavor...
        string = string.replace("\r\n", "\n")

        nodemesh = []
        
        lines = string.split("\n")
        for line in lines:
            if line:
                try:
                    vertinfo = eval(line)
                    nodemesh.append(vertinfo)
                except:
                    pass

        return nodemesh


    def makeNodes(self, string):
        nodemesh = self.stringToNodemesh(string)
        nodes = self.NodemeshToNodes(nodemesh)
        return nodes


    def cleanNodes(self, nodes):
        for node in nodes:
            node.parent = None
            node.G = 0
            node.H = 0
            node.F = 0


    # Gets the distance between positions A and B.
    def getRealDistance(self, A, B):
        math = self.math
        X = abs(A[0] - B[0])
        Y = abs(A[1] - B[1])
        Z = abs(A[2] - B[2])
        Ds = (X*X)+(Y*Y)+(Z*Z)
        D = math.sqrt(Ds)
        return D


    def getManhattanDistance(self, A, B):
        math = self.math
        X = abs(A[0] - B[0])
        Y = abs(A[1] - B[1])
        Z = abs(A[2] - B[2])
        D = X+Y+Z
        return D

    
    # Returns the nearest node, given a position and a list of nodes.
    def getNearestNode(self, position, nodes):
        best = []
        for node in nodes:
            if best:
                bestnode = best[0]
                bestdistance = best[1]
                distance = self.getRealDistance(position, node.position)
                if distance < bestdistance:
                    best = [node, distance]
            else:
                distance = self.getRealDistance(position, node.position)
                best = [node, distance]
        return best[0]

    # Returns the nearest visible node, given a position, list of nodes, and a gameobj (for raycasting)
    # btw, this is pretty expensive, it does a lot of raycasting (to each node).
    def getNearestVisibleNode(self, position, nodes, gameobj):
        best = []
        for node in nodes:
            if best:
                bestnode = best[0]
                bestdistance = best[1]

                obj, point, normal = gameobj.rayCast(node.position, position)
                # If the position can see the node...
                if not obj:
                    # And the distance is less then the current best's distance...
                    distance = self.getRealDistance(position, node.position)
                    if distance < bestdistance:
                        # Then this node is the new bestest node!
                        best = [node, distance]
            # If there is no current best
            else:
                obj, point, normal = gameobj.rayCast(node.position, position)
                # If the position can see the node...
                if not obj:
                    # Then this node is our best so far.
                    distance = self.getRealDistance(position, node.position)
                    best = [node, distance]
        
        # This must mean there are no visible nodes!?
        if not best:
            print "No visible nodes!"
            # We'll just go with the nearest one then.
            best = [self.getNearestNode(position, nodes), None]
        
        return best[0]
        
    

    # Returns the node with the best F score: doesn't evaluate F.
    def getBestF(self, nodes):
        best = []
        for node in nodes:
            if best:
                bestnode = best[0]
                bestF = best[1]
                if node.F < bestF:
                    best = [node, node.F]
            else:
                best = [node, node.F]
        return best[0]
    



    ####################################
    ###### ------ findPath ------ ######
    ####################################
    # Given a list of nodes, start position, target position, gameobject,
    # and max number of steps, this method will return a path object.
    # This will find a more accurate path, but at the expense of computation speed.
    def findPath(self, nodes, start, target, gameobj, steps=500):
        self.cleanNodes(nodes)
        
        PATHFOUND = 0

        startNode = self.getNearestVisibleNode(start, nodes, gameobj)
        targetNode = self.getNearestVisibleNode(target, nodes, gameobj)

        OPEN = [startNode]
        CLOSED = []

        for i in range(steps):

            # Get node in OPEN with lowest F
            currentNode = self.getBestF(OPEN)

            # Switch it to CLOSED
            OPEN.remove(currentNode)
            CLOSED.append(currentNode)

            # For each adjacent node
            adjacentNodes = currentNode.adjacent
            for node in adjacentNodes:

                # If it's not in CLOSED
                if not (node in CLOSED):
                    # Get F Score
                    origParent = node.parent
                    node.parent = currentNode
                    F, G, H = node.evaluate(targetNode)

                    if not (node in OPEN):
                        node.parent = currentNode
                        OPEN.append(node)
                    else:
                        if node.G < currentNode.G:
                            # Already in the OPEN list, revert to origParent
                            node.parent = origParent
                        else:
                            node.parent = currentNode

            # Stop when we found the target node or if there are no more open nodes.
            if targetNode in OPEN:
                targetNode.parent = currentNode
                PATHFOUND = 1
                break
            if not OPEN:
                break

        if PATHFOUND:
            path = self.PATH(start, target, startNode, targetNode, OPEN, CLOSED)
            return path
        else:
            return 0


    ########################################
    ###### ------ fastFindPath ------ ######
    ########################################
    # Given a list of nodes, start position, target position, and
    # max number of steps, this method will return a path object.
    # This will usually find a path faster, but at the expense of accuracy.
    def fastFindPath(self, nodes, start, target, steps=500):
        self.cleanNodes(nodes)
        
        PATHFOUND = 0

        startNode = self.getNearestNode(start, nodes)
        targetNode = self.getNearestNode(target, nodes)

        OPEN = [startNode]
        CLOSED = []

        for i in range(steps):

            # Get node in OPEN with lowest F
            currentNode = self.getBestF(OPEN)

            # Switch it to CLOSED
            OPEN.remove(currentNode)
            CLOSED.append(currentNode)

            # For each adjacent node
            adjacentNodes = currentNode.adjacent
            for node in adjacentNodes:

                # If it's not in CLOSED
                if not (node in CLOSED):
                    # Get F Score
                    F, G, H = node.fastEvaluate(startNode, targetNode)

                    if not (node in OPEN):
                        node.parent = currentNode
                        OPEN.append(node)
                    else:
                        if node.G < currentNode.G:
                            # No change to parent, and already in the OPEN list.
                            pass
                        else:
                            node.parent = currentNode

            # Stop when we found the target node or if there are no more open nodes.
            if targetNode in OPEN:
                targetNode.parent = currentNode
                PATHFOUND = 1
                break
            if not OPEN:
                break

        if PATHFOUND:
            path = self.PATH(start, target, startNode, targetNode, OPEN, CLOSED)
            return path
        else:
            return 0


pathfinder = PATHFINDER
