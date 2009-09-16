############################
### ------ inputs ------ ###
############################
### Copyright 2009 Chase Moskal
INIT = 0
controller = None

def init(con):
    global controller, INIT
    controller = CONTROLLER(con)
    import modules
    controller.setControls(modules.interface.options.controls)
    INIT = 1
	
class CONTROLLER:
    events = {}

    keyboard = None
    
    other = {}
    
    other["LMB"] = None
    other["RMB"] = None
    other["MMB"] = None

    other["MWU"] = None
    other["MWD"] = None

    def __init__(self, con):
        
        KEYBOARD = con.sensors["KEYBOARD"]
        
        LMB = con.sensors["LMB"]
        RMB = con.sensors["RMB"]
        MMB = con.sensors["MMB"]

        MWU = con.sensors["MWU"]
        MWD = con.sensors["MWD"]
        
        ###
        
        self.keyboard = KEYBOARD
        
        self.other["LMB"] = LMB
        self.other["RMB"] = RMB
        self.other["MMB"] = MMB

        self.other["MWU"] = MWU
        self.other["MWD"] = MWD


    class EVENT:
        def __init__(self, controller, control, value=None):
            self.controller = controller

            self.control = control
            self.getValue(value)
            
            self.kind = ""
            self.lastpositive = 0

        def getValue(self, value=None):
            if not value:
                if control not in self.controller.controls:
                    return None
                value = self.controller.controls[self.control]
                
            value = value.replace("-", "")
            value = value.upper()

            self.value = value

            return value

        def getStatus(self):
            if self.value in self.controller.other:
                self.kind = "other"
                positive = self.controller.other[self.value].positive

                status = 0
                
                if positive:
                    if self.lastpositive:
                        status = 2 # being held
                    else:
                        status = 1 # just pressed
                else:
                    if self.lastpositive:
                        status = 3 # just released
                    else:
                        status = 0

                self.lastpositive = positive
                return status
            
            else:
                self.kind = "key"
                import GameKeys
                status = self.controller.keyboard.getKeyStatus(getattr(GameKeys, self.value))
                return status

        def isPositive(self):
            status = self.getStatus()
            if (status == 1) or (status == 2):
                return 1
            return 0


    def getEvent(self, control):
        if control in self.events:
            event = self.events[control]
            return event
        else:
            return None

    def getStatus(self, control):
        event = self.getEvent(control)
        if not event:
            return None
        status = event.getStatus()
        return status

    def isPositive(self, control):
        event = self.getEvent(control)
        if not event:
            return None
        positive = event.isPositive()
        return positive
    
    
    def setControls(self, controls):
        # controls is usually from options.py
        self.controls = {}
        self.events = {}
        
        self.controls = controls
        print "Controls set."

        for control in self.controls:
            value = self.controls[control]
            event = self.EVENT(self, control, value)
            self.events[control] = event
        #print "Events set."
