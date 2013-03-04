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

        self.all_objs = [bed, lamp, dresser, chair]
        self.game = {'rooms': [Bedroom, Closet], 'inv': [], 'location': Bedroom}

        if data:
            self.deserialise(data)

    def __eq__(self, other):
        if self.game['location'] != other.game['location']:
            return False
        for i in range(len(self.game['inv'])):
            if sorted(self.game['inv'])[i] != sorted(other.game['inv'])[i]:
                return False
        for i in range(len(self.game['rooms'])):
            if sorted(self.game['rooms'])[i] != sorted(other.game['rooms'])[i]:
                return False
        return True

    def __ne__(self, other):
        if self.game['location'] != other.game['location']:
            return True
        for i in range(len(self.game['inv'])):
            if sorted(self.game['inv'])[i] != sorted(other.game['inv'])[i]:
                return True
        for i in range(len(self.game['rooms'])):
            if sorted(self.game['rooms'])[i] != sorted(other.game['rooms'])[i]:
                return True
        return False

    def play(self, action):
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

    def serialise(self):
        """Turns self.game into a dictionary and returns that.
        Only serialises changeable aspects of objects and rooms"""
        data = {'rooms': {room.name: room.serialise() for room in self.game['rooms']}}
        data['inv'] = {obj.id: obj.serialise() for obj in self.game['inv']}
        data['location'] = self.game['location'].name
        return data

    def get_obj(self, obj_id):
        "Returns an object, given that object's id"
        return [obj for obj in self.all_objs if obj.id == obj_id][0]

    def deserialise(self, data):
        """Given a dictionary of serialised information, updates each_room.objects and calls each_room.deserialise()
            which updates any changes for the individual objects."""
        for room in self.game['rooms']:
            room_data = data['rooms'][room.name]
            room.objects = [self.get_obj(obj_id) for obj_id in room_data.keys()]
            room.deserialise(room_data)
        self.game['inv'] = [self.get_obj(obj_id) for obj_id in data['inv'].keys()]
        self.game['location'] = [room for room in self.game['rooms'] if room.name == data['location']][0]
        