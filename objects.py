# SPECIFIC OBJECTS

# Defines dictionaries of information necessary for creating the object, for each object
# Specific objects are created using create_object in creation.py, and defined at the bottom

from scaffolding import Object
from properties import Openable, Lightable, UnreachableLight, Gettable, Climbable, Container
from creation import create_object

def light_str(self):
    if self.is_lit:
        return '  '.join([self.description, self.on_description])
    else:
        return '  '.join([self.description, self.off_description])

def show_inside_str(self):
    if self.is_open:
        base = '  '.join([self.description, self.open_description])
        if self.look_in():
            return base + '  ' + self.look_in()
        return base
    else:
        return '  '.join([self.description, self.closed_description])


dresser_dict = {'bases': (Openable, Container, Object),
                'attributes': {'id': "dresser", 'name': "dresser", 'is_open': False, 'objects': [], 
                            'description': "A dresser made of blonde wood, with small brass handles.", 
                            'open_description': "The drawers hang open at a slight angle, indicating poor quality workmanship.", 
                            'closed_description': "All drawers are closed."},
                'methods': {'__str__': show_inside_str}}

bed_dict = {'bases': (Object,), 
            'attributes': {'description': "A handsome four-poster with a patchwork quilt and gauzy maroon canopy.",
                        'id': "bed", 'name': "bed"},
            'methods': {'climb': lambda self, *args, **kwargs: "Didn't your mother teach you anything?",
                        'stand': lambda self, *args, **kwargs: self.climb(*args, **kwargs)}}

lamp_dict = {'bases': (Lightable, Object),
            'attributes': {'id': "lamp", 'name': "lamp", 'is_lit': False, 
                'description': "The lamp is set high on the wall, its tawdry plaid shade almost out of reach.", 
                'on_description': "The object throws a soft light, illuminating the room.", 
                'off_description': "The bulb is cold and dusty."},
            'methods': {'__str__': light_str}}

u_lamp_dict = {'bases': (UnreachableLight, Object),
            'attributes': {'id': "unreachable_lamp", 'name': "lamp", 'block': True, 'is_lit': False, 
                'error_description': "You strain but cannot quite reach the switch.", 
                'description': "The lamp is set high on the wall, its tawdry plaid shade almost out of reach.", 
                'on_description': "The object throws a soft light, illuminating the room.", 
                'off_description': "The bulb is cold and dusty."},
            'methods': {'__str__': light_str}}

chair_dict = {'bases': (Climbable, Gettable, Object),
            'attributes': {'id': "chair", 'name': "chair", 'has_user': False, 
                'description': "A sturdy wooden chair with dark wooden slats."}}


Bed = create_object(**bed_dict)
Lamp = create_object(**lamp_dict)
UnreachableLamp = create_object(**u_lamp_dict)
Chair = create_object(**chair_dict)
Dresser = create_object(**dresser_dict)