class Room(object):
    def __init__(self, name, objects, description, exits):
        self.name = name
        self.objects = objects
        self.description = description
        self.exits = exits

class Object(object):
    def __str__(self):
        return self.description

    def look(self):
        return str(self)

class Climbable(object):
    
    def stand(self):
        pass

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

class Bed(Object):

    def __init__(self):
        self.description = "A handsome four-poster with a patchwork quilt and gauzy maroon canopy."

    # TODO make this not hardcoded?
    def stand(self):
        return "Didn't your mother teach you anything?"

    def climb(self):
        return self.stand()

class Dresser(Object, Openable):

    def __init__(self):
        self.is_open = False
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
        self.is_lit = False
        self.description = "The lamp is set high on the wall, its tawdry plaid shade almost out of reach."
        self.on_description = "The object throws a soft light, illuminating the room."
        self.off_description = "The bulb is cold and dusty."

    def __str__(self):
        if self.is_lit:
            return '  '.join([self.description, self.on_description])
        else:
            return '  '.join([self.description, self.off_description])



bed = Bed()
dresser = Dresser()
lamp = Lamp()



bedroom = Room(name='Bedroom', objects=[bed, dresser, lamp], description='A small blue room with homey furnishings.', \
            exits={})

