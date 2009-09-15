#############################################
### ------ COMMUNICATION FUNCTIONS ------ ###
#############################################



import cPickle as pickle

packsep = "\x11" # DC1
flagsep = "\x12" # DC2

elementsep = "\x13" # DC3
unitsep = "\x14" # DC4





def pack(flag, data):
    pdata = pickle.dumps(data)
    contents = flag + flagsep + pdata + packsep
    return contents

def unpack(package):
    halves = package.split(flagsep)
    flag = halves[0]
    pdata = halves[1]
    data = pickle.loads(pdata)
    return flag, data

def packUDP(name, flag, data):
    pdata = pickle.dumps(data)
    contents = name + flagsep + flag + flagsep + pdata + packsep
    return contents

def unpackUDP(package):
    triple = package.split(flagsep)
    name = triple[0]
    flag = triple[1]
    pdata = triple[2]
    
    data = pickle.loads(pdata)
    return name, flag, data

def unpackList(packages):
    items = []

    for package in packages:
        flag, data = unpack(package)
        items.append( (flag, data) )

    return items


class STREAM:
    content = ""

    def add(self, data):
        self.content += data

    def push(self, data):
        self.content += data

    def extract(self):
        packs = []
        
        chunks = self.content.split(packsep)
        lastchunk = chunks[len(chunks)-1]
        chunks = chunks[:len(chunks)-1]
        for chunk in chunks:
            if chunk:
                packs.append(chunk+packsep)
        self.content = lastchunk
        return packs

    def clear(self):
        self.content = ""

