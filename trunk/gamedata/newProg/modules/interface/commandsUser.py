helpText = """Welcome to the FPS Project's in game terminal. \
You can execute Python commands by typing them in and \
hitting enter. If the command fails to execute properly, it \
will attempt to send your input as a text message. \
You can precede your input with a forward slash (/) to \
explicitly designate your input as a python command (if it \
fails, it will not be sent as a text message."""

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
