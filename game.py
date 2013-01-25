from scaffolding import Room, Object
from objects import Bed, Dresser, UnreachableLamp, Chair

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


game = {'rooms': [Bedroom, Closet], 'inv': [], 'location': Bedroom}