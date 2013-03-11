# USER ACTION PARSING

# Attempts to parse out a user action by:
#   - check_noun() to get the correct object reference
#       - e.g. 'get pretty chair' will look through all objects within the room + user's inventory and attempt to find an object
#       - that has a name or id of 'chair' and contains the adjective 'pretty'
#   - make_action() to try to call obj.verb()
#       - uses additional information (like adjectives or prepositions) to call an action on an object
# Currently does not work with actions larger than four words

def moving(action):
    """If action contains directional information, returns the direction, otherwise, returns False."""

    short_dir = ['n', 'ne', 'e', 'se', 's', 'sw', 'w', 'nw']
    long_dir = ['north', 'northeast', 'east', 'southeast', 'south', 'southwest', 'west', 'northwest']
    for d in long_dir:
        if d in action:
            return d
    for d in short_dir:
        if d in action:
            long_d = long_dir[short_dir.index(d)]
            return long_d
    return False

def check_noun(location, inventory, noun, adj=None):
    """Checks a noun to make sure it exists, and uses adjective to help identify which noun is being referred to
        in the case of a conflict. Returns an object or error string"""

    # all objects inside any open Container objects
    contained_objects = [contained \
                        for obj in location.objects \
                            for base in obj.__class__.__bases__ if base.__name__ == 'Container' \
                                for contained in obj.objects if obj.is_open]
    # objects in inventory and room.objects
    room_inv_objs = [obj for obj in location.objects + inventory]
    all_objs = contained_objects + room_inv_objs
    all_named_objs = [obj.name for obj in all_objs]
  
    # if there is only one match for the noun, return it
    if all_named_objs.count(noun) == 1:
        index = all_named_objs.index(noun)
        return all_objs[index]
    # is an adjective is passed in, use that to narrow things down
    if adj:
        # adj in obj's id is more relevant than adj in obj's description (e.g. brass_lamp > "The brass lamp is grungy.")
        adj_in_name = [obj for obj in all_objs if noun in obj.name and adj in obj.id]
        if len(adj_in_name) == 1:
            return adj_in_name[0]
        # but adj in description is second-best
        adj_in_desc = [obj for obj in all_objs if noun in obj.name and adj in str(obj)]
        if len(adj_in_desc) == 1:
            return adj_in_desc[0]
        # if the adjective does not narrow it down, return an error message
        if len(adj_in_name) > 1 or len(adj_in_desc) > 1:
            return "More than one object fits that name."
        return "That object does not exist."
    # if no adjective has been passed in, return an error message
    else:
        if all_named_objs.count(noun) > 1:
            return "More than one object fits that name."
        return "That object does not exist."

def make_action(location, inventory, noun, verb, preposition=None, noun2=None):
    """Attempts to call noun.verb() -- check_noun(noun) must have been called first.
        If preposition exists, will try both noun.verb() and noun.verb_preposition()
        If noun2 exists, will also try noun2.verb() and noun2.verb_preposition()"""

    # if the noun is an error string, return it
    if isinstance(noun, str):
        return noun
    # try to concatenate verb + preposition
    if preposition:
        verb_prep = verb + '_' + preposition
        # try to call verb_prep on noun, with noun2 as an argument if necessary
        if hasattr(noun, verb_prep):
            try:
                return getattr(noun, verb_prep)(location=location, inventory=inventory)
            except TypeError:
                return getattr(noun, verb_prep)(noun2, location=location, inventory=inventory)
    # otherwise, try to call verb on noun, with noun2 as an argument if necessary
    if hasattr(noun, verb):
        try:
            return getattr(noun, verb)(location=location, inventory=inventory)
        except TypeError:
            return getattr(noun, verb)(noun2, location=location, inventory=inventory)
    # also try to call verb_prep on noun2, with noun1 as an argument if necessary
    if preposition:
        verb_prep = verb + '_' + preposition
        if hasattr(noun2, verb_prep):
            try:
                return getattr(noun2, verb_prep)(location=location, inventory=inventory)
            except TypeError:
                return getattr(noun2, verb_prep)(noun, location=location, inventory=inventory)
    # and verb on noun2, with noun1 as an argument if necessary
    if hasattr(noun2, verb):
        try:
            return getattr(noun2, verb)(location=location, inventory=inventory)
        except TypeError:
            return getattr(noun2, verb)(noun, location=location, inventory=inventory)    
    # if none of those work, return a failure message
    else:
       return "That is not a valid action."


def parse(action, location, inventory):
    "Given an action, attempts to parse the action and call it where appropriate"
    
    prepositions = ['of', 'on', 'in', 'to', 'for', 'with', 'from', 'around', 'under', 'over', 'out', 'off', 'down']
    action = action.split()

    if len(action) == 1:
        # assume action is a room action (e.g. look, jump) and call it on the current room instance
        verb = action[0]
        move = moving(verb)
        if move: 
            return getattr(location, 'move')(move, inventory)
        try:
            return getattr(location, verb)(inventory=inventory)
        except AttributeError:
            return "That is not a valid action."

    if len(action) == 2:
        # assume action is in the form <verb noun> (e.g. get chair)
        # or a movement (e.g. go north)

        move = moving(action)
        if move:
            return getattr(location, 'move')(move, inventory)

        verb, noun = action
        obj = check_noun(location, inventory, noun)   
        return make_action(location, inventory, obj, verb)

    if len(action) == 3:
        # assume action is in the form <verb adjective noun> (e.g. get brass lamp, get my sword)
        # or in the form <verb preposition noun> (e.g. look in chest, stand on bed)
        # or in the form <verb_preposition noun> (e.g. turn on lamp)

        verb, adj, noun = action
        if adj in prepositions:
            obj = check_noun(location, inventory, noun)
            return make_action(location, inventory, obj, verb, adj)
        obj = check_noun(location, inventory, noun, adj)
        return make_action(location, inventory, obj, verb)


    if len(action) == 4:
        # assume action is in the form <verb preposition adjective noun> (e.g. stand on sturdy chair)
        # or in the form <verb preposition preposition noun> (e.g. get down from chair)
        # or in the form <verb noun preposition noun> (e.g. get key from chest, put chair in trunk)
        verb, two, three, noun = action
        if two in prepositions:
            verb, prep, adj, noun = action
            obj = check_noun(location, inventory, noun, adj)
            return make_action(location, inventory, obj, verb, prep)
        if three in prepositions:
            verb, noun, prep, noun2 = action
            obj_1 = check_noun(location, inventory, noun)
            obj_2 = check_noun(location, inventory, noun2)
            return make_action(location, inventory, obj_1, verb, prep, obj_2)
        else:
            return "I cannot parse this action."
            
    # if len(action) == 5:
    #     # assume action is in the form <verb adj noun preposition noun> (e.g. get large key from chest)
    #     # or <verb noun preposition adjective noun> (e.g. get key from locked chest)
    #     # or <verb preposition noun preposition noun> (e.g. turn on lamp inside cupboard)
    #     pass
        
    # if len(action) == 6:
    #     # assume action is in the form <verb adjective noun preposition adjective noun)        
    #     pass