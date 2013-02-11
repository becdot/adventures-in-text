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
    def pickup(self, room, inv):
        return self.get(room, inv)

    def drop(self, room, inv):
        if self in inv:
            room.objects.append(self)
            inv.remove(self)
        else:
            return "That item is not currently in your inventory."

class Climbable(object):
    # climb and stand are multipurpose 
    #(i.e. calling climb once will set has_user to True, while calling climb again will set has_user to False)
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

    def look_in(self):
        if self.is_open:
            if len(self.objects) > 1:
                description = "This object contains: " + "{}, " * (len(self.objects) - 1) + "{}."
                return description.format(*self.objects)
            elif len(self.objects) == 1:
                return "This object has a {} inside.".format(self.objects[0])
            else:
                return "This object is empty."
        else:
            return "You cannot look inside a closed object."
