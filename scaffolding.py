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

# Properties

class Openable(object):
    # TODO make messages not hardcoded?
    
    def open(self):
        if self.is_open:
            return "That object is as open as it can get!"
        else:
            self.is_open = True
            return self.open_description

    def pull(self):
        return self.open()

    def close(self):
        if self.is_open:
            self.is_open = False
            return self.closed_description
        else:
            return "That object can't get any more closed."

    def shut(self):
        return self.close()

    def push(self):
        return self.close()

class Lightable(object):

    def light(self):
        if self.is_lit:
            return "The object is already glowing brightly"
        else:
            self.is_lit = True
            return self.on_description

    def turn_on(self):
        return self.light()

    def snuff(self):
        if self.is_lit:
            self.is_lit = False
            return "The glow fades into blackness."
        else:
            return "The object cannot get any darker."

    def turn_off(self):
        return self.snuff()

class UnreachableLight(Lightable):
    # Unreachable object must have self._room defined
    def _is_standing(self, room):
        self.block = True
        if room:
            for obj in room.objects:
                try:
                    if obj.has_user:
                        self.block = False
                except AttributeError:
                    pass

    def light(self):
        self._is_standing(self._room)
        if self.block:
            return self.error_description
        else:
            return super(UnreachableLight, self).light()

    def turn_on(self):
        return self.light()

    def snuff(self):
        self._is_standing(self._room)
        if self.block:
            return self.error_description
        else:
            return super(UnreachableLight, self).snuff()

    def turn_off(self):
        return self.snuff()

class Gettable(object):
    # room can be an actual room or a Container object
    def get(self, room, inv):
        if self.gettable:
            if self in room.objects:
                if room.__class__.__name__ == 'Room':
                    inv.append(self)
                    room.objects.remove(self)
                else: # room is a Container object
                    if room.is_open:
                        inv.append(self)
                        room.objects.remove(self)
                    else:
                        return "The object is closed."
            elif self in inv:
                return "You already have that object."
            else:
                return "That object does not exist."
        else:
            return "You cannot pick up that object."
    def pickup(self, room, inv):
        return self.get(room, inv)

    def drop(self, room, inv):
        if self in inv:
            room.objects.append(self)
            inv.remove(self)
        else:
            return "That item is not currently in your inventory."

class Climbable(object):
    
    # climb and stand are multipurpose (i.e. calling climb the first time will set has_user to True, 
    # while calling climb again will set has_user to False)
    def climb(self):
        if self.has_user:
            self.has_user = False
            return "You step carefully back down."
        else:
            self.has_user = True
            return "You clamber onto the object."
    def stand(self):
        return self.climb()
    # get_on, get_off, and get_down are single-purpose
    def get_on(self):
        if self.has_user:
            return "You are already standing on that object!"
        else:
            self.has_user = True
            return "You clamber onto the object."
    def get_off(self):
        if self.has_user:
            self.has_user = False
            return "You step carefully back down."
        else:
            return "You are not standing on anything."
    def get_down(self):
        return self.get_off()

class Container(object):

    # get is defined in Gettable (allows an object to be 'gotten' from a room or open object)

    def put_in(self, object, inv):
        if self.is_open:
            self.objects.append(object)
            inv.remove(object)
            return "You place the object inside the open container."
        else:
            return "Try opening the container first."



# Specific Objects

class Bed(Object):

    def __init__(self):
        self.description = "A handsome four-poster with a patchwork quilt and gauzy maroon canopy."
        self.id = "bed"

    # TODO make this not hardcoded?
    def stand(self):
        return "Didn't your mother teach you anything?"

    def climb(self):
        return self.stand()

class Dresser(Object, Openable, Container):

    def __init__(self, *objs):
        self.id = "dresser"
        self.is_open = False
        self.objects = [obj for obj in objs]
        self.description = "A dresser made of blonde wood, with small brass handles."
        self.open_description = "The drawers hang open at a slight angle, indicating poor quality workmanship."
        self.closed_description = "All drawers are closed."

    def __str__(self):
        if self.is_open:
            return '  '.join([self.description, self.open_description])
        else:
            return '  '.join([self.description, self.closed_description])

class Lamp(Object, Lightable):
    def __init__(self):
        self.id = "lamp"
        self.is_lit = False
        self.description = "The lamp is set high on the wall, its tawdry plaid shade almost out of reach."
        self.on_description = "The object throws a soft light, illuminating the room."
        self.off_description = "The bulb is cold and dusty."

    def __str__(self):
        if self.is_lit:
            return '  '.join([self.description, self.on_description])
        else:
            return '  '.join([self.description, self.off_description])

class UnreachableLamp(Object, UnreachableLight):

    def __init__(self, room=None):
        self.id = "unreachable_lamp"
        self._room = room
        self.block = True
        self.is_lit = False
        self.error_description = "You strain but cannot quite reach the switch."
        self.description = "The lamp is set high on the wall, its tawdry plaid shade almost out of reach."
        self.on_description = "The object throws a soft light, illuminating the room."
        self.off_description = "The bulb is cold and dusty."

    def __str__(self):
        if self.is_lit:
            return '  '.join([self.description, self.on_description])
        else:
            return '  '.join([self.description, self.off_description])

class Chair(Object, Climbable, Gettable):
    def __init__(self):
        self.id = "chair"
        self.has_user = False
        self.gettable = True
        self.description = "A sturdy wooden chair with dark wooden slats."


# Bedroom = Room(name='Bedroom', objects=[Bed, Lamp, Dresser], description='A homey room with blue wallpaper 
#            and old-fashioned scenes hanging from brass frames.  There is a large four-poster against one wall
#            and a small dresser in the corner.', exits={'west': 'Closet'})
# Closet = Room(name='Closet', objects=[Chair], description='Significantly colder than the bedroom, 
#            the closet has a slanted roof that only makes it feel more cramped.', exits: {'east': 'Bedroom'})
