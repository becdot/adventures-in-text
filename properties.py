# Properties

class Openable(object):
    # TODO make messages not hardcoded?
    
    def open(self, **kwargs):
        if self.is_open:
            return "That object is as open as it can get!"
        else:
            self.is_open = True
            return self.open_description

    def pull(self, **kwargs):
        return self.open(**kwargs)

    def close(self, **kwargs):
        if self.is_open:
            self.is_open = False
            return self.closed_description
        else:
            return "That object can't get any more closed."

    def shut(self, **kwargs):
        return self.close(**kwargs)

    def push(self, **kwargs):
        return self.close(**kwargs)

class Lightable(object):

    def light(self, **kwargs):
        if self.is_lit:
            return "The object is already glowing brightly"
        else:
            self.is_lit = True
            return self.on_description

    def turn_on(self, **kwargs):
        return self.light(**kwargs)

    def snuff(self, **kwargs):
        if self.is_lit:
            self.is_lit = False
            return "The glow fades into blackness."
        else:
            return "The object cannot get any darker."

    def turn_off(self, **kwargs):
        return self.snuff(**kwargs)

class UnreachableLight(Lightable):
    def _is_standing(self, room):
        self.block = True
        for obj in room.objects:
            try:
                if obj.has_user:
                    self.block = False
            except AttributeError:
                pass

    def light(self, location=None, **kwargs):
        if not location:
            raise Exception('location must be provided')
        self._is_standing(location)
        if self.block:
            return self.error_description
        else:
            return super(UnreachableLight, self).light()

    def turn_on(self, **kwargs):
        return self.light(*args, **kwargs)

    def snuff(self, location=None, **kwargs):
        if not location:
            raise Exception('location must be provided')
        self._is_standing(location)
        if self.block:
            return self.error_description
        else:
            return super(UnreachableLight, self).snuff()

    def turn_off(self, **kwargs):
        return self.snuff(*args, **kwargs)

class Gettable(object):
    # room can be an actual room or a Container object
    def get(self, location=None, inventory=None, **kwargs):
        if not location:
            raise Exception('location must be provided')
        if inventory == None:
            raise Exception('inventory must be provided')

        for obj in location.objects:
            try:
                if self in obj.objects:
                    if obj.is_open:
                        inventory.append(self)
                        obj.objects.remove(self)
                    else:
                        return "The object is closed."
            except AttributeError:
                pass
        if self in location.objects:
            inventory.append(self)
            location.objects.remove(self)
        elif self in inventory:
            return "You already have that object."
        else:
            return "That object does not exist."

    def pickup(self, **kwargs):
        return self.get(**kwargs)

    def drop(self, location=None, inventory=None, **kwargs):
        if not location:
            raise Exception('location must be provided')
        if inventory == None:
            raise Exception('inventory must be provided')

        if self in inventory:
            location.objects.append(self)
            inventory.remove(self)
        else:
            return "That item is not currently in your inventory."

class Climbable(object):
    # climb and stand are multipurpose 
    #(i.e. calling climb once will set has_user to True, while calling climb again will set has_user to False)
    def climb(self, inventory=None, **kwargs):
        if inventory == None:
            raise Exception('inventory must be provided')

        if self in inventory:
            return "You cannot climb that while still holding it."
        if self.has_user:
            self.has_user = False
            return "You step carefully back down."
        else:
            self.has_user = True
            return "You clamber onto the object."
    def stand(self, **kwargs):
        return self.climb(**kwargs)

    # get_on, get_off, and get_down are single-purpose
    def get_on(self, inventory=None, **kwargs):
        if inventory == None:
            raise Exception('inventory must be provided')

        if self in inventory:
            return "You cannot climb that while still holding it."
        if self.has_user:
            return "You are already standing on that object!"
        else:
            self.has_user = True
            return "You clamber onto the object."
    def get_off(self, inventory=None, **kwargs):
        if inventory == None:
            raise Exception('inventory must be provided')

        if self.has_user:
            self.has_user = False
            return "You step carefully back down."
        else:
            return "You are not standing on anything."
    def get_down(self, **kwargs):
        return self.get_off(**kwargs)

class Container(object):

    # get is defined in Gettable (allows an object to be 'gotten' from a room or open object)

    def put_in(self, obj, inventory=None, **kwargs):
        if inventory == None:
            raise Exception('inventory must be provided')

        if self.is_open:
            self.objects.append(obj)
            inventory.remove(obj)
            return "You place the object inside the open container."
        else:
            return "Try opening the container first."

    def look_in(self, **kwargs):
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

