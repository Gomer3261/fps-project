### 2D Filters! ###

def run(con):
    """
    Turns filters on and off based on options.settings
    """
    own = con.owner
    
    import modules
    options = modules.interface.options

    if "filter-hdr" in options.settings:
        if options.settings["filter-hdr"]:
            own["HDR"] = True
        else:
            own["HDR"] = False
    else:
        own["HDR"] = False








### Lum: A lovely companion to HDR ###

def runLum(con):
    if con.owner["HDR"]:
        doLum(con)

def doLum(cont):
    import GameLogic as G
    import BGL
    import Rasterizer as R

    scene = G.getCurrentScene()
    #cont = G.getCurrentController()
    objList = scene.objects
    own = cont.owner

    viewport = BGL.Buffer(BGL.GL_INT, 4)
    BGL.glGetIntegerv(BGL.GL_VIEWPORT, viewport);

    width = R.getWindowWidth()
    height = R.getWindowHeight()

    x = viewport[0] + width/2
    y = viewport[1] + height/2

    x1 = viewport[0] + width/3
    y1 = viewport[1] + height/3

    x2 = viewport[0] + width/3
    y2 = viewport[1] + height/2

    x3 = viewport[0] + width/2
    y3 = viewport[1] + height/2

    x4 = viewport[0] + width/2
    y4 = viewport[1] + height/3

    pixels = BGL.Buffer(BGL.GL_FLOAT, [1])
    pixels1 = BGL.Buffer(BGL.GL_FLOAT, [1])
    pixels2 = BGL.Buffer(BGL.GL_FLOAT, [1])
    pixels3 = BGL.Buffer(BGL.GL_FLOAT, [1])
    pixels4 = BGL.Buffer(BGL.GL_FLOAT, [1])

    BGL.glReadPixels(x, y, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixels)
    BGL.glReadPixels(x1, y1, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixels1)
    BGL.glReadPixels(x2, y2, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixels2)
    BGL.glReadPixels(x3, y3, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixels3)
    BGL.glReadPixels(x4, y4, 1, 1, BGL.GL_LUMINANCE, BGL.GL_FLOAT, pixels4)

    avgPixels = (pixels[0]+pixels1[0]+pixels2[0]+pixels3[0]+pixels4[0])/5.0

    #Slow adaptation
    own["avgL"] = (own["avgL"]*0.9 + avgPixels*0.1)

    avgPixels = own["avgL"]

