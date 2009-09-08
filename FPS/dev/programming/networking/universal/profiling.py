##################################
### ------ profiling.py ------ ###
##################################
### Copyright 2009 Chase Moskal
# For profiling; measuring execution times of scripts.
INIT = 1

class PROFILE:
    import time
    def __init__(self, name):
        self.name = name
        self.data = {}
        self.totalms = 0.0

    class CLOCK:
        def __init__(self, profile, name):
            self.profile = profile
            self.name = name
            self.time = profile.time
            
            self.start = self.time.time()
            self.end = self.time.time()

            # adding itself to the profile
            self.profile.data[name] = self
        
        def restart(self):
            self.start = self.time.time()

        def stop(self):
            self.end = self.time.time()
            return (self.time.time() - self.start)

        def get(self):
            return (self.time.time() - self.start)

    def clock(self, name):
        clock = self.CLOCK(self, name)
        return clock

    def output(self):
        print "Profile of "+self.name
        totalms = 0.0
        for clockname in self.data:
            ms = self.data[clockname].get() * 1000.0
            print "    "+clockname+": "+repr(ms)+"ms"
            totalms += ms
        print "Total: "+repr(totalms)+"ms\n"
        self.totalms = totalms

    def getTotalms(self):
        self.totalms = 0.0
        for clockname in self.data:
            ms = self.data[clockname].get() * 1000
            self.totalms += ms
        return self.totalms

### HOW TO PROFILE YOUR SCRIPT ###
# myprofile = PROFILE("myprofile")
# clockA = myprofile.clock("A")
# #<Script to be measured goes here>#
# clockA.stop()
# myprofile.output()


class SUPERPROFILE:
    profiles = {}

    def add(self, profile):
        self.profiles[profile.name] = profile

    def output(self):
        for profilename in self.profiles:
            self.profiles[profilename].output()

    def outputshort(self):
        totalms = 0.0
        print "Superprofile:"
        for profilename in self.profiles:
            ms = self.profiles[profilename].getTotalms()
            print "    "+profilename+": "+repr(ms)+"ms"
            totalms += ms
        print "Total: "+repr(totalms)+"ms\n"



superprofile = SUPERPROFILE()
