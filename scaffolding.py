# Parent classes

class Room(object):
    def __init__(self, name, objects, description, exits={}):
        self.name = name
        self.objects = objects
        self.description = description
        self.exits = exits

    def look(self, **kwargs):
        return self.description

    def move(self, direction=None, inventory=None, **kwargs):
        for obj in self.objects + inventory:
            try:
                if obj.has_user:
                    return "You must climb down first."
            except AttributeError:
                pass
        if direction in self.exits:
            return self.exits[direction]
        else:
            return "You cannot go that way."

class Object(object):
    required_attrs = ['name', 'id', 'description']
    
    def __str__(self):
        return self.description

    def look(self, **kwargs):
        return str(self)

# define all possible verbs on Object to return an error message (You can't <verb> this object)
# properties can override these base verbs

VERBS = ['open', 'close', 'pull', 'push', 'shut', 'light', 'turn_on', 'snuff', 'turn_off', 'get', 'pickup', 'drop', 'climb',\
        'stand', 'get_on', 'get_off', 'get_down', 'put_in', 'look_in']

def set_methods(verbs):
    def make_func(verb):
        def verbage(self, *args, **kwargs):
            return "You can't {} this object.".format(verb)
        return verbage

    for v in verbs:
        setattr(Object, v, make_func(v))

set_methods(VERBS)
