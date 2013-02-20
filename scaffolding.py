# Parent classes

class Room(object):
    def __init__(self, name, objects, description, exits={}):
        self.name = name
        self.objects = objects
        self.description = description
        self.exits = exits

    def look(self):
        return self.description

    def move(self, inventory, direction):
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
    def __str__(self):
        return self.description

    def look(self):
        return str(self)

# define all possible verbs on Object to return an error message (You can't <verb> this object)
# properties can override these base verbs

VERBS = ['open', 'close', 'pull', 'push', 'shut', 'light', 'turn_on', 'snuff', 'turn_off', 'get', 'pickup', 'drop', 'climb',\
        'stand', 'get_on', 'get_off', 'get_down', 'put_in', 'look_in']

def set_methods(verbs):
    def make_func(verb):
        def verbage(self, *args):
            return "You can't {} this object.".format(verb)
        return verbage

    for v in verbs:
        setattr(Object, v, make_func(v))

set_methods(VERBS)


# Bedroom = Room(name='Bedroom', objects=[Bed, Lamp, Dresser], description='A homey room with blue wallpaper 
#            and old-fashioned scenes hanging from brass frames.  There is a large four-poster against one wall
#            and a small dresser in the corner.', exits={'west': 'Closet'})
# Closet = Room(name='Closet', objects=[Chair], description='Significantly colder than the bedroom, 
#            the closet has a slanted roof that only makes it feel more cramped.', exits: {'east': 'Bedroom'})
