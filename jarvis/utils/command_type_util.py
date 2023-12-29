def is_spotify_command(action): 
    if action.lower().startswith("play ") or action.lower().startswith("pause") or action.lower().startswith("stop") or action.lower().startswith("resume") or action.lower().startswith("play") or action.lower().startswith("wake up") or action.lower().startswith("raise spotify volume") or action.lower().startswith("lower spotify volume") or action.lower().startswith("play playlist ") or action.lower().startswith("play artist "):
        return True
    else:
        return False
    
def is_open_command(action): 
    if action.lower().startswith("open "):
        return True
    else:
        return False
    
def is_calendar_command(action):
    if action.lower().startswith("calendar this week") or action.lower().startswith("calendar today") or action.lower().startswith("calendar tomorrow") or action.lower().startswith("calendar on ") or action.lower().startswith("add event") or action.lower().startswith("find event"):
        return True
    else:
        return False
    
def is_gmail_command(action):
    if action.lower().startswith("recent emails"):
        return True
    else:
        return False