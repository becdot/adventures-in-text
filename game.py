from scaffolding import Room, Object, \
                        Bed, Dresser, Lamp, UnreachableLamp, Chair

global inventory
inventory = []
global location

bed = Bed()
lamp = UnreachableLamp()
dresser = Dresser()
chair = Chair()

Bedroom = Room(name='Bedroom', objects=[bed, lamp, dresser], description='A homey room with blue wallpaper \
and old-fashioned scenes hanging from brass frames.  There is a large four-poster against one wall \
and a small dresser in the corner.', exits={})
Closet = Room(name='Closet', objects=[chair], description='Significantly colder than the bedroom, \
the closet has a slanted roof that only makes it feel more cramped', exits={})

Bedroom.exits['west'] = Closet
Closet.exits['east'] = Bedroom
lamp._room = Bedroom

location = Bedroom

# GLOBAL METHODS
def get(obj):
    return obj.get(location, inventory)

def drop(obj):
    return obj.drop(location, inventory)

def move(direction):
    new_location = location.move(direction)
    if isinstance(new_location, Room):
        global location 
        location = new_location
        return location.look()
    else:   
        return new_location

def look(obj=None):
    if obj:
        return obj.look()
    else:
        return location.look()



import pdb;pdb.set_trace()