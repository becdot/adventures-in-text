# Parent classes

class Room(object):
    def __init__(self, name, objects, description, exits={}):
        self.name = name
        self.objects = objects
        self.description = description
        self.exits = exits

    def look(self):
        return self.description

    def move(self, direction):
        if direction in self.exits:
            return self.exits[direction]
        else:
            return "You cannot go that way."

class Object(object):
    def __str__(self):
        return self.description

    def look(self):
        return str(self)


# Bedroom = Room(name='Bedroom', objects=[Bed, Lamp, Dresser], description='A homey room with blue wallpaper 
#            and old-fashioned scenes hanging from brass frames.  There is a large four-poster against one wall
#            and a small dresser in the corner.', exits={'west': 'Closet'})
# Closet = Room(name='Closet', objects=[Chair], description='Significantly colder than the bedroom, 
#            the closet has a slanted roof that only makes it feel more cramped.', exits: {'east': 'Bedroom'})
