### Accounts Manager ###

import os
import sys

currentpath = sys.path[0]
indexpath = currentpath+"/database/accounts/"

def getIndex():
    index = os.listdir(indexpath)
    cleanIndex = []
    for item in index:
        if item[0] != ".":
            item = item.split(".")[0]
            cleanIndex.append(item)
    return cleanIndex


def inIndex(name):
    name = name.lower()
    index = getIndex()
    if name in index:
        return 1
    else:
        return 0
    


# Takes some stuff, creates a account (dictionary)
def createAccount(name, password, email):
    info = {}
    info["name"] = name
    info["password"] = password
    info["email"] = email

    stats = {}
    stats["kills"] = 0
    stats["deaths"] = 0

    social = {} # No, not social from Blender Artists...
    social["friends"] = []
    social["inbox"] = []

    social["inbox"].append( ("Welcome!", "Welcome to the FPS Project!\nThis is your inbox.\nYou should know what an inbox is.", "Chase") )

    account = {}
    account["info"] = info
    account["stats"] = stats
    account["social"] = social

    return account



# This takes a account (dictionary) and saves it to a file with cPickle.
def saveAccount(account):
    import cPickle
    import traceback
    
    pAccount = cPickle.dumps(account)
    
    username = account["info"]["name"]
    username = username.lower()

    try:
        f = open(indexpath+username+".account", "w")
        f.write(pAccount)
        f.close()
    except:
        traceback.print_exc()
        return 0

    return 1



def loadAccount(name):
    name = name.lower()
    try:
        f = open(indexpath+name+".account", "r")
        data = f.read()
        f.close()
        import cPickle
        account = cPickle.loads(data)
        return account
    except:
        return None



def getAccount(name):
    if inIndex(name):
        account = loadAccount(name)
        return account
    return None

