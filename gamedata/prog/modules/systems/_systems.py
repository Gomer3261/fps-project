####################################
### ------  TERMINAL      ------ ###
####################################
### Copyright 2009 Chase Moskal!
# This is the terminal class.
# It handles terminal input and output.

INIT = 1

class TERMINAL:
    def __init__(self):
        # Terminal access activitiy.
        self.active = 0

        # The contents of the terminal (output)
        self.contents = []

        # Terminal input
        self.inpipe = []

    # Trims a list from the beginning until it reaches the desired length.
    def limit(self, x, limit=10):
        while len(x) > limit:
            del x[0]
        return x

    # Limits the number of lines of contents it remembers.
    def limitContents(self, limit=10):
        self.contents = self.limit(self.contents, limit)

    # Takes a string and cuts it into n sized chunks (returns a list)
    def textwrap(self, s, n):
        return [s[x:x+n] for x in range (0, len(s), n)]

    # Formats contents into a string, and outputs it.
    def getContents(self, lines=10, wrap=50):
        data = []
        for line in self.contents:
            linestart = 1
            for x in self.textwrap(line, wrap):
                if linestart:
                    data.append(x)
                else:
                    data.append("    "+x)
                linestart = 0
        return "\n".join(self.limit(data, lines))

    # Outputs something to the terminal
    def output(self, s):
        s = s.replace("\r", "")
        lines = s.split("\n")

        for line in lines:
            self.contents.append(line)

    # Inputs a string to the inpipe
    def input(self, s):
        self.inpipe.append(s)

    # Enters something to the inpipe
    def enter(self, s):
        self.inpipe.append(s)

    def clearInpipe(self):
        self.inpipe = []

    # Clears terminal's output contents
    def clear(self):
        self.contents = []

terminal = TERMINAL()














#############################
### ------ OPTIONS ------ ###
#############################
### Copyright 2009 Chase Moskal!
# This object handles the saving/loading of options.
INIT = 1

class OPTIONS:
    import traceback
    sepchar = "\n=------ Settings Above / Controls Below ------=\n\n"
    def __init__(self):
        self.path = "FPS_options.txt"

        self.settings = {}
        self.controls = {}
    
    def saveDefaults(self):
        try:
            settings = {}
            controls = {}

            # SETTINGS
            settings["mxsens"] = 5.0
            settings["mysens"] = 5.0

            # CONTROLS
            controls["spawn"] = "space"
            controls["suicide"] = "delete"

            controls["forward"] = "w"
            controls["backward"] = "s"
            controls["left"] = "a"
            controls["right"] = "d"
            controls["jump"] = "space"
            controls["mod"] = "shift"

            controls["shoot"] = "lmb"
            controls["aim"] = "rmb"
            controls["reload"] = "r"

            controls["action"] = "e"

            controls["menu"] = "tab"

            
            
            self.settings = settings
            self.controls = controls

            
            
            # Requesting a SAVE operation
            result = self.save()

            import inputs
            inputs.controller.setControls()
            print("Controls Set")
            
            return result
        except:
            self.traceback.print_exc()
        
    def setSetting(self, key, value):
        self.settings[key] = value
        r = self.save()
        return r

    def setControl(self, key, value):
        self.controls[key] = value
        r = self.save()
        return r
    
    def save(self):
        try:
            settings = self.settings
            controls = self.controls
            
            settingsfile = ""
            for key in settings:
                settingsfile += key + ": " + repr(settings[key]) + "\n"

            controlsfile = ""
            for key in controls:
                controlsfile += key + ": " + repr(controls[key]) + "\n"

            newfile = settingsfile + self.sepchar + controlsfile
            
            f = open(self.path, "w")
            f.write(newfile)
            f.close()

            print("Options Saved")

            import inputs
            inputs.controller.setControls()
            print("Controls Set")
        
            return 1
        except:
            self.traceback.print_exc()
            print "\n\n", settings, "\n\n", controls
            return 0
    
    def load(self):
        try:
            f = open(self.path, "r")
            data = f.read()
            f.close()

            # Convert to clean
            data = data.replace("\r\n", "\n")
            data = data.replace("\r", "\n")

            # split into parts
            parts = data.split(self.sepchar)

            settingsfile = parts[0]
            controlsfile = parts[1]

            # Settings
            lines = settingsfile.split("\n")
            statements = {}
            for line in lines:
                if line and not (line.find("//") != -1):
                    parts = line.split(":")
                    name = parts[0].strip()
                    value = parts[1].strip()
                    statements[name] = eval(value)
            self.settings = statements

            # Controls
            lines = controlsfile.split("\n")
            statements = {}
            for line in lines:
                if line and not (line.find("//") != -1):
                    parts = line.split(":")
                    name = parts[0].strip()
                    value = parts[1].strip()
                    statements[name] = eval(value)
            self.controls = statements

            print("Options Loaded")

            import inputs
            controller = inputs.controller
            controller.setControls()

            print("Controls Set")
            
            return 1
        except:
            import traceback
            traceback.print_exc()
            print("Error loading; will attempt to save defaults and use those")
            result = self.saveDefaults()
            if result:
                return 2 # This means the load failed, but the saving of defaults worked.
            return 0

options = OPTIONS()

