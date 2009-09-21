helpText = """Welcome to the FPS Project's in game terminal. \
You can execute Python commands by typing them in and \
hitting enter. If the command fails to execute properly, it \
will attempt to send your input as a text message. \
You can precede your input with a forward slash (/) to \
explicitly designate your input as a python command (if it \
fails, it will not be sent as a text message, so you won't be \
embarassed when you fail). Use listUserCommands() and \
use help(command) to learn more about a specific command."""

# ----------------------------
# Terminal Specific Commands
# ----------------------------

def help(cmd = None):
    """
    Usage: help(terminalCommand)
        Prints out text that should help you use the requested terminal command. If left blank, general help information is printed.
    """
    if cmd:
        output(cmd.__doc__)
    else:
        output(helpText)

        

def output(s):
    """
    Usage: output(string)
        prints the given value in the terminal window.
    """
    s = str(s)
    import modules
    modules.interface.terminal.output(s)

    

def fill():
    """
    Usage: fill()
        Fills the terminal window with text. Good for testing terminal changes.
    """
    output(helpText*100)

    

def clear():
    """
    Usage: clear()
        Clears the terminal window of all text.
    """
    import modules
    modules.interface.terminal.clear()

    

def listUserCommands():
    """
    Usage: listUserCommands()
        Displays a list of commands available to the user.
    """
    import modules
    for i in dir(modules.interface.commandsUser):
        # Filter out the python module stuff so we only get our commands
        if not i.startswith("__"):
            output(i)
            
            








# -----------------
# Option Commands
# -----------------

def defaultOptions():
    """
    Usage: defaultOptions()
        Resets the games options to the default values.
    """
    import modules
    options = modules.interface.options
    options.saveDefaults()
    output("Options have been set to defaults. I think.")

    

def setSetting(key, value):
    """
    Usage: setSetting(setting, value)
        Sets the given setting to the given value.
    """
    import modules
    options = modules.interface.options
    r = options.setSetting(key, value)
    output("Success value: %s"%(r))

    
    
def getSetting(key):
    """
    Usage: getSetting(setting)
        prints the value of the requested setting.
    """
    import modules
    options = modules.interface.options
    output("Setting %s is set to %s" % (key, options.settings[key]))

    
    
def setControl(key, value):
    """
    Usage: setControl(control, value)
        Sets the given control to the given value.
    """
    import modules
    options = modules.interface.options
    r = options.setControl(key, value)
    output("Success value: %s"%(r))

    
    
def getControl(key):
    """
    Usage: getControl(control)
        Prints the value of the requested control.
    """
    import modules
    options = modules.interface.options
    output("Control %s is set to %s" % (key, options.controls[key]))

    

def loadOptions():
    """
    Usage: loadOptions()
        Loads the options from FPS_options.txt
    """
    import modules
    options = modules.interface.options
    r = options.load()
    output("Success value: %s"%(r))

    
