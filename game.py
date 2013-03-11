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
        data = {'rooms': [room.serialise() for room in self.game['rooms']]}
        data['inv'] = [obj.serialise() for obj in self.game['inv']]
        data['location'] = self.game['location'].name
        return data

    def get_obj(self, obj_id):
        "Returns an object, given that object's id"
        return [obj for obj in self.all_objs if obj.id == obj_id][0]

    def assign_objects(self, obj_dict):
        """If an object contains other objects, assigns them to container_obj.objects.
        container.serialise() = 
            {'id': 'dresser', 'attrs': {'is_open': False, 'objects': [{'id': 'chair', 'attrs': {has_user: False}}]}
        This function sets dresser.objects = [chair] so that dresser.deserialise() can apply updates to chair if appropriate"""

        outer_obj = self.get_obj(obj_dict['id'])
        outer_obj.objects = []
        for attr, value in obj_dict['attrs'].items():
            # if value is a list of objects, assign to obj.objects
            if value and isinstance(value, list):
                for inner_dic in value:
                    inner_obj = self.get_obj(inner_dic['id'])
                    print "assigning {} to {}.objects".format(inner_obj.id, outer_obj.id)
                    outer_obj.objects.append(inner_obj)
                    self.assign_objects(inner_dic)

    def get_room(self, room_name):
        "Returns an object, given that object's id"
        return [room for room in self.game['rooms'] if room.name == room_name][0]

    def deserialise(self, data):
        """Given a dictionary of serialised information, updates each_room.objects and calls each_room.deserialise()
            which updates any changes for the individual objects."""
        for room_dict in data['rooms']:
            room = self.get_room(room_dict['name'])
            room.objects = []
            for obj_dict in room_dict['objects']:
                print "{} in room".format(obj_dict['id'])
                self.assign_objects(obj_dict) 
                obj = self.get_obj(obj_dict['id'])
                room.objects.append(obj)
            room.deserialise(room_dict)

        self.game['inv'] = []
        for obj_dict in data['inv']:
            self.assign_objects(obj_dict) 
            obj = self.get_obj(obj_dict['id'])
            obj.deserialise(obj_dict)
            self.game['inv'].append(obj)

        self.game['location'] = self.get_room(data['location'])
        