# Parent classes

class Room(object):
    def __init__(self, name, objects, description, exits={}):
        self.name = name
        self.objects = objects
        self.description = description
        self.exits = exits

    def __eq__(self, other):
        if len(self.objects) != len(other.objects):
            print "len of objects !="
            return False
        for i in range(len(self.objects)):
            if sorted(self.objects)[i] != sorted(other.objects)[i]:
                print "{} and {} not equal".format(self.objects[i], other.objects[i])
                return False
        # return self.name == other.name and self.description == other.description
        if self.name != other.name:
            print "names !="
            return False
        if self.description != other.description:
            print "descriptions !="
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

    def serialise(self):
        "Returns a dictionary with object ids as keys, and object serialisation dictionaries as values"
        return {obj.id: obj.serialise() for obj in self.objects}

    def deserialise(self, data):
        "Given a serialised dictionary, calls object.deserialise() on each object in self.objects"
        obj_data = (obj_dic for obj_id, obj_dic in data.items())
        map(lambda obj, dic: obj.deserialise(dic), self.objects, obj_data)

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