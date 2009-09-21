### Filters! ###

def run(con):
    """
    Turns filters on and off based on options.settings
    """
    own = con.owner
    
    import modules
    options = modules.interface.options

    if "filter-hdr" in options.settings:
        if options.settings["filter-hdr"]:
            own["HDR"] = True
        else:
            own["HDR"] = False
    else:
        own["HDR"] = False
