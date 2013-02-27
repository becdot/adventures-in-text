from scaffolding import Room, Object
from objects import Bed, Dresser, UnreachableLamp, Chair
from grammar import parse

class Game:

    def __init__(self, data=None):

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

        self.game = {'rooms': [Bedroom, Closet], 'inv': [], 'location': Bedroom}

        if data:
            self.update(self.game, data)

    def play_game(self, action):
        """Takes an action and attempts to call it on the game instance.  
        Returns any message that might have been generated."""
        location = self.game['location']
        inventory = self.game['inv']
        message = None

        update = parse(action, location, inventory)
        if isinstance(update, Room):
            self.game['location'] = update
            return None
        return update

    def serialise_game(self):
        """Turns self.game into a dictionary and returns that
        Only serialises changeable aspects of objects and rooms"""
        data = {'rooms': {room.name: room.serialise() for room in self.game['rooms']}}
        data['inv'] = {obj.id: obj.serialise() for obj in self.game['inv']}
        data['location'] = self.game['location'].name
        return data

    

    def get_all_objects(self):
        "Returns a list of all objects in self.game"
        contained_objects = [contained for room in self.game['rooms']
                                for obj in room.objects if hasattr(obj, 'objects')
                                        for contained in obj.objects]
        room_objs = [obj for obj in room.objects for room in self.game['rooms']]
        return contained_objects + room_objs + self.game['inv']

    def update(self, data):
        "Takes a serialised game and updates game instance"

        # set inventory
        self.game['inv'] = [obj for obj in self.get_all_objects() 
                            if obj.id in [obj_id for obj_id in data['inv']]]

        # update rooms
        print data
        for rooms, rooms_dict in data['rooms'].iteritems():
            for obj, obj_dict in rooms_dict.items():
                for attr, value in obj_dict.items():
                    room_objects = [room.objects for room in self.game['rooms'] if room.name == rooms][0]
                    print [obj.id for obj in room_objects]
                    print repr(obj), obj_dict
                    i = [str(obj.id) for obj in room_objects].index[obj]
                    setattr(room_objects[i], attr, value)

        # set location
        self.location = [room for room in self.game['rooms'] if room.name == data['location']][0]

        