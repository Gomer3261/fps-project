### ############################### ###
### ### ------ TIMETOOLS ------ ### ###
### ############################### ###
### # The FPS Project
INIT = 1

def perFrame(ticrate=60.0):
    return 1.0/ticrate

class TIMER():
    import time
    last = 0.0
    def __init__(self):
        self.reset()

    def reset(self):
        self.last = self.time.time()

    def get(self):
        dif = self.time.time() - self.last
        return dif
    
    def do(self, interval=1.0):
        # This is useful for an interval timer.
        # If you want something to happen every
        # interval seconds, call this function
        # and if it returns 1, then do it.
        # In other words, this returns 1 after
        # the given interval time has elapsed since
        # 1 was last returned. Get it?
        dif = self.get()
        if dif > interval:
            self.reset()
            return 1 # Do
        else:
            return 0 # Don't.
