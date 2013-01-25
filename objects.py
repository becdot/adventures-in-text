from scaffolding import Object
from properties import Openable, Lightable, UnreachableLight, Gettable, Climbable, Container

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