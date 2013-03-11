# GAME WORLD

# Creates all rooms and objects for the game in a dictionary
#    self.game = {'rooms' = [<room1>, <room2>], 'inventory': [<obj1>], 'location': <room1>}

from scaffolding import Room, Object
from objects import Bed, Dresser, UnreachableLamp, Chair

class TestGame:

    def __init__(self):

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

        self.all_objs = [bed, lamp, dresser, chair]
        self.game = {'rooms': [Bedroom, Closet], 'inv': [], 'location': Bedroom}