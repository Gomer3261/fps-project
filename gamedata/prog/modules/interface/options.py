#############################
### ------ OPTIONS ------ ###
#############################
### Copyright 2009 Chase Moskal!
# This object handles the saving/loading of options.

INIT = 0

import traceback

sepchar = "\n=------ Settings Above / Controls Below ------=\n\n"
path = "FPS_options.txt"
settings = {}
controls = {}

def init():
    """Init the module."""
    global INIT
    load()
    INIT = 1
    print "Options Initiated"

def initLoop(con):
    global INIT
    if not INIT:
        init()







def saveDefaults():
    global sepchar
    global path
    global settings
    global controls
    global traceback
    
    try:
        settings = {}
        controls = {}

        # SETTINGS
        settings["mxsens"] = 5.0
        settings["mysens"] = 5.0
        settings["inverty"] = 0
        settings["invertx"] = 0
        settings["filter-hdr"] = 1

        # CONTROLS
        controls["spawn"] = "space-key"
        controls["suicide"] = "del-key"

        controls["forward"] = "w-key"
        controls["backward"] = "s-key"
        controls["left"] = "a-key"
        controls["right"] = "d-key"
        controls["jump"] = "space-key"
        controls["sprint"] = "leftshift-key"

        controls["use"] = "lmb"
        controls["aim"] = "rmb"
        controls["reload"] = "r-key"

        controls["interact"] = "e-key"

        controls["menu"] = "tab-key"

        
        
        # Requesting a SAVE operation
        result = save()
        
        return result
    except:
        traceback.print_exc()
    
def setSetting(key, value):
    global sepchar
    global path
    global settings
    global controls
    global traceback

    key = key.lower()
    
    settings[key] = value
    r = save()
    return r

def setControl(key, value):
    global sepchar
    global path
    global settings
    global controls
    global traceback

    key = key.lower()
    
    controls[key] = value
    r = save()
    return r

def save():
    global sepchar
    global path
    global settings
    global controls
    global traceback

    import os
    
    try:
        settingsfile = "// This is the options file for the FPS Project. You can reset these options to default by typing \"options default\" in the in-game terminal." + os.linesep + os.linesep
        for key in settings:
            settingsfile += key + ": " + repr(settings[key]) + os.linesep

        controlsfile = ""
        for key in controls:
            controlsfile += key + ": " + repr(controls[key]) + os.linesep

        nativesepchar = sepchar.replace("\n", os.linesep)
        newfile = settingsfile + nativesepchar + controlsfile
        
        f = open(path, "w")
        f.write(newfile)
        f.close()

        print("Options Saved")

        import inputs
        if inputs.INIT:
            inputs.controller.setControls(controls)
    
        return 1
    except:
        traceback.print_exc()
        print "\n\n", settings, "\n\n", controls
        return 0

def load():
    global sepchar
    global path
    global settings
    global controls
    global traceback
    
    try:
        f = open(path, "r")
        data = f.read()
        f.close()

        # Convert to clean
        data = data.replace("\r\n", "\n")
        data = data.replace("\r", "\n")

        # split into parts
        parts = data.split(sepchar)

        settingsfile = parts[0]
        controlsfile = parts[1]

        # Settings
        lines = settingsfile.split("\n")
        statements = {}
        for line in lines:
            if line and not (line.find("//") != -1):
                parts = line.split(":")
                name = parts[0].strip().lower()
                value = parts[1].strip()
                statements[name] = eval(value)
        settings = statements

        # Controls
        lines = controlsfile.split("\n")
        statements = {}
        for line in lines:
            if line and not (line.find("//") != -1):
                parts = line.split(":")
                name = parts[0].strip().lower()
                value = parts[1].strip()
                statements[name] = eval(value)
        controls = statements

        print "Options Loaded"

        import inputs
        if inputs.INIT:
            inputs.controller.setControls(controls)
        
        return 1
    except:
        traceback.print_exc()
        print "Error loading; will attempt to save defaults and use those"
        result = saveDefaults()
        if result:
            return 2 # This means the load failed, but the saving of defaults worked.
        return 0

