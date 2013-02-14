import scaffolding # sets base verbs on Object class

def moving(action, location):
    """If action contains directional information, calls location.move(direction) 
    and returns either a new Room object or an error message.  Otherwise, returns False."""

    short_dir = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
    long_dir = ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest']
    for d in long_dir:
        if d in action.split():
            return location.move(d)
    for d in short_dir:
        if d in action.split():
            return location.move(long_dir[short_dir.index(d)])
    return False


def play_game(old_game, action):
    """Takes a game dictionary and an action and attempts to call the action.  
    Returns a tuple of the updated game dictionary and any messages."""
    game = old_game
    location = game['location']
    inventory = game['inv']
    message = None
    try:
        verb, obj = action.split()
        for item in location.objects + inventory:
            if obj == item.id:
                obj = item
    except ValueError:
        verb = action
        obj = None

    # global methods that need access to location and/or inventory
    if moving(verb, location):
        new_location = moving(verb, location)
        if isinstance(new_location, scaffolding.Room): # if moving to a room, update location and print the new room description
            game['location'] = new_location
        else:   
            message = new_location # otherwise return error string (location does not exist)
    elif verb == 'get':
        message = obj.get(location, inventory)
    elif verb == 'drop':
        message = obj.drop(location, inventory)
    elif verb == 'look':
        if obj == 'room' or obj == None:
            message = location.look()
        else:
            message = getattr(obj, verb)()

    # object-specific methods
    else:
        try:
            message = getattr(obj, verb)()
        except AttributeError:
            message = "That is not a valid action."

    return (game, message)

