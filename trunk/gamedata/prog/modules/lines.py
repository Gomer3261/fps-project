################################
### ------ linesystem ------ ###
################################
### Copywright 2009 Geoffrey Gollmer

INIT = 0
    
class lineManager:
    
    lines = []
    
    def __init__(self, add):
        self.add = add
    
    def addLine(self, startPos, endPos, type="line", thickness=1):
        newLine = self.LINE(self, startPos, endPos, type, thickness)
        self.lines.append(newLine)
        return newLine
        
        
    def deleteLine(self, lineRef):
        lineRef.end()
        self.lines.remove(lineRef)
        
    def clearLines(self):
        for line in self.lines:
            line.end()
            self.lines.remove(line)
        
    class LINE():
        import GameLogic as gl
        import math
        import slab
        
        #You shouldn't need to touch these.
        baseOrientation = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        orientation = [[1, 0, 0], [0, 1, 0], [0, 0, 1]]
        uvDist = 0
        
        def __init__(self, lineManager, startPos, endPos, type="line", thickness=1):
    
            self.startPos = startPos
            self.endPos = endPos
            self.thickness = thickness
            self.type = type
            
            self.lineManager = lineManager
            
            
            self.lineManager.add.object = self.type
            self.lineManager.add.instantAddObject()
            self.object = self.lineManager.add.objectLastCreated
            
            self.refresh()
          
        def refresh(self):
            ##################################################
            # - this method refreshes the values on a line - #
            ##################################################
            orientation = self.baseOrientation
            
            startPos = self.startPos
            endPos = self.endPos
            cameraPos = self.gl.getCurrentScene().active_camera
            
            thickness = self.thickness
            type = self.type
            
            #recreating the 3D object if it doesn't match the settings.
            if type != self.object.name:
                self.object.endObject()
                self.lineManager.add.object = type
                self.lineManager.add.instantAddObject()
                self.object = self.lineManager.add.objectLastCreated
                self.uvDist = 0
            
            #get the distance between the 2 points
            dist = self.math.sqrt((endPos[0] - startPos[0])**2 + (endPos[1] - startPos[1])**2 + (endPos[2] - startPos[2])**2)
            
            #point the object towards it's target while aiming close to the camera
            orientation = self.pointTo(startPos, endPos, cameraPos)
            
            #extend the object to the point it's aiming at
            for i in range(0, 3):
                orientation[i][1] *= dist
            
            #set the objects width
            for i in range(0, 3):
                orientation[i][0] *= thickness
                orientation[i][2] *= thickness
            
            #apply values to the object itself
            self.object.position = startPos
            self.object.orientation = orientation
            
            
            #getting vertex data for UV adjustment.
##            mesh = self.object.meshes[0]
##            vArray = mesh.getVertexArrayLength(0)
##            
##            upper2 = []
##            
##            for i in range(4):
##                for j in range(i+1, 4):
##                    uv1 = mesh.getVertex(0, i)
##                    uv2 = mesh.getVertex(0, j)
##                    
##                    if uv1.getUV()[0] == uv2.getUV()[0]:
##                        uvDist = uv2.getUV()[1] - uv.getUV()[1]
##                        if uvDist < 0:
##                            uvDist *= -1
##                            
##                        if uv1.getUV()[1] >= uv2.getUV()[1]:
##                            upper2.append(uv1)
##                            lower = uv2.getUV()[1]
##                            upper = uv1.getUV()[1]
##                        else:
##                            upper2.append(uv2)
##                            lower = uv2.getUV()[1]
##                            upper = uv2.getUV()[1]
##                            
##            if self.uvDist == 0:
##                self.uvDist = uvDist
##                
##            for vert in upper2:
##                vert.setUV([vert.getUV()[0], lower + (self.uvDist * dist)])
            
        def end(self):
            self.object.endObject()
            
        ###################################################
        # - This just makes life easier, don't touch it - #
        ###################################################

        # We may or may not have taken these lovely
        # methods from Herman Tulleken
            
        def euclidSize(self, vec):
            return self.math.sqrt(vec[0]*vec[0]
                        + vec[1]*vec[1]
                        + vec[2]*vec[2])
        
        def cross(self, vec1, vec2):
            return [vec1[1]*vec2[2]-vec1[2]*vec2[1],
                    vec1[2]*vec2[0]-vec1[0]*vec2[2],
                    vec1[0]*vec2[1]-vec1[1]*vec2[0]]
        
        def pointTo(self, pos0, pos1, cameraPos):
            y = [pos1[0] - pos0[0],
                 pos1[1] - pos0[1],
                 pos1[2] - pos0[2]]
        
            size = self.euclidSize(y)
        
            for i in range(0, 3):
                y[i] = y[i] / size #nomalise size
        
            z = self.cross(self.cross(y, cameraPos), y)
        
            size = self.euclidSize(z)
            
            for i in range(0, 3):
                z[i] = z[i] / size #nomalise size
        
            x = self.cross(y, z)
        
            res = [[], [], []]
            
            for i in range(0, 3):
                res[i] = [x[i], y[i], z[i]]
        
            return res
