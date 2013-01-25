import scaffolding # sets base verbs on Object class

def play_game(game, action):
    """Takes a game dictionary and an action and attempts to call the action.  
    Returns a tuple of the updated game dictionary and any messages."""
    location = game['location']
    inventory = game['inv']
    message = None
    verb, obj = action.split()
    for item in location.objects + inventory:
        if obj == item.id:
            obj = item

    # global methods that need access to location and/or inventory
    if verb == 'get':
        message = obj.get(location, inventory)
    elif verb == 'drop':
        message = obj.drop(location, inventory)
    elif verb == 'move':
        new_location = location.move(obj)
        if isinstance(new_location, scaffolding.Room): # if moving to a room, update location and print the new room description
            game['location'] = new_location
        else:   
            message = new_location # otherwise return error string (location does not exist)
    elif verb == 'look':
        if obj == 'room':
            message = location.look()
        else:
            message = getattr(obj, verb)()

    # object-specific methods
    else:
        message = getattr(obj, verb)()

    return (game, message)

