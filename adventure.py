class Room(object):

    def __init__(self, exits={}, objects=[], name='', description=''):
        self.exits = exits
        self.objects = objects
        self.name = name
        self.description = description

        for object in self.objects: 
            object.location = self

    def __str__(self):
        return self.name

    def build_description(self, base, **object):
        for obj, desc in object.iteritems():
            if str(obj) in map(str, self.objects):
                base += '  ' + desc
        return base 

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

    def status(self):
        print '   - current location: {}\n   - inventory: {}'.format(str(self.location), map(str, [object for object in self.inventory]))


