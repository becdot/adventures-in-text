def build_description(room, base, **object):
    for obj, desc in object.iteritems():
        print obj, desc
        if obj in map(str, room.objects):
            base += '  ' + desc
    return base 

class Room(object):

    def __init__(self, exits={}, objects=[], name='', base_description='', **objdesc):
        self.exits = exits
        self.objects = objects
        self.name = name
        self.description = build_description(self, base_description, objdesc)

        for object in self.objects: 
            object.location = self

    def __str__(self):
        return self.name


class Object(object):

    def __init__(self, name=''):
        self.name = name

    def __str__(self):
        return self.name

    def move(self, user):
        room = user.location
        if isinstance(self.location, User): # drop
            user.inventory.remove(self)
            room.objects.append(self)
            self.location = room
        else: # pickup
            room.objects.remove(self)
            user.inventory.append(self)
            self.location = user

class User(object):

    def __init__(self, name='', inventory=[], location=None):
        self.name = name
        self.inventory = inventory
        self.location = location

        for object in self.inventory: 
            object.location = self

    def status(self):
        print '   - current location: {}\n   - inventory: {}'.format(str(self.location), map(str, [object for object in self.inventory]))


