import scaffolding # sets base verbs on Object class
from grammar import parse




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
            if obj == item.name:
                obj = item
    except ValueError:
        verb = action
        obj = None

    # global methods that need access to location and/or inventory
    new_location = moving(verb, location, inventory)
    if new_location:
        if isinstance(new_location, scaffolding.Room): # if moving to a room, update location and print the new room description
            game['location'] = new_location
        else:   
            message = new_location # otherwise return error string (location does not exist)
    elif verb == 'get':
        message = obj.get(location=location, inventory=inventory)
    elif verb == 'drop':
        message = obj.drop(location=location, inventory=inventory)
    elif verb == 'look':
        if obj == 'room' or obj == None:
            message = location.look()
        else:
            message = getattr(obj, verb)(location=location, inventory=inventory)
    elif verb == 'climb':
        message = obj.climb(location=location, inventory=inventory)

    # object-specific methods
    else:
        try:
            message = getattr(obj, verb)(location=location, inventory=inventory)
        except AttributeError:
            message = "That is not a valid action."

    return (game, message)

