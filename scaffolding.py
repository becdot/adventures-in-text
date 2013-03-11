# ROOM AND PARENT OBJECT CLASSES

# Rooms inherit from the Room class
#    -- note: room exits must be set after rooms are created, since they contain references to each other
#
# All objects inherit from this parent Object class
# It defines basic functionality (e.g. 'look' common to all objects) and attributes required for all objects (e.g. name)
#   -- note: objects must inherit from Object LAST, after other mix-ins (actually, this might not be true)

class Room(object):
    def __init__(self, name, objects, description, exits={}):
        """name = string, used to identify the room; objects = list of objects; description = string, 
            exits = dictionary of directions and room instances (e.g. {'north': Bedroom})"""
        self.name = name
        self.objects = objects
        self.description = description
        self.exits = exits

    def __eq__(self, other):
        if len(self.objects) != len(other.objects):
            return False
        for i in range(len(self.objects)):
            if sorted(self.objects)[i] != sorted(other.objects)[i]:
                return False
        # return self.name == other.name and self.description == other.description
        if self.name != other.name:
            return False
        if self.description != other.description:
            return False
        return True

    def __ne__(self, other):
        if self.name != other.name or self.description != other.description:
            return True
        if len(self.objects) != len(other.objects):
            return True
        for i in range(len(self.objects)):
            if sorted(self.objects)[i] != sorted(other.objects)[i]:
                return True
        return False 

    def get_obj(self, obj_id):
        return [obj for obj in self.objects if obj.id == obj_id][0]

    def serialise(self):
        "Returns a dictionary with object ids as keys, and object serialisation dictionaries as values"
        return {'name': self.name, 'objects': [obj.serialise() for obj in self.objects]}

    def deserialise(self, data):
        "Given a serialised dictionary, calls object.deserialise() on each object in self.objects"
        map(lambda dic: self.get_obj(dic['id']).deserialise(dic), data['objects'])

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
    changeable_attrs = []
    
    def __str__(self):
        return self.description

    def look(self, **kwargs):
        return str(self)