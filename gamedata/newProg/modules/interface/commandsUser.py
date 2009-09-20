helpText = """Welcome to the FPS Project's in game terminal. \
You can execute Python commands by typing them in and \
hitting enter. If the command fails to execute properly, it \
will attempt to send your input as a text message. \
You can precede your input with a forward slash (/) to \
explicitly designate your input as a python command (if it \
fails, it will not be sent as a text message, so you won't be \
embarassed when you fail)."""

def help():
    output(helpText)

def output(s):
    s = str(s)
    import modules
    modules.interface.terminal.output(s)

def fill():
    output(helpText*100)

def clear():
    import modules
    modules.interface.terminal.clear()






def defaultOptions():
    import modules
    options = modules.interface.options
    options.saveDefaults()
    output("Options have been set to defaults. I think.")

def setSetting(key, value):
    import modules
    options = modules.interface.options
    r = options.setSetting(key, value)
    output("Success value: %s"%(r))

def setControl(key, value):
    import modules
    options = modules.interface.options
    r = options.setControl(key, value)
    output("Success value: %s"%(r))

def loadOptions():
    import modules
    options = modules.interface.options
    r = options.load()
    output("Success value: %s"%(r))
