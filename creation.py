# OBJECT CREATION

# Dynamically creates objects from a dictionary in the form {'bases': [], 'attributes': {}, 'methods': {}}
# During creation, checks to make sure that all attributes specified in required_attrs 
# for each of the object's bases have been provided

from scaffolding import Object
from properties import Openable, Lightable, UnreachableLight, Gettable, Climbable, Container

def validate_attrs(bases):
    """Decorator for an object's init method to check that all attributes 
    specified in required_attrs for each of the object's bases have been provided"""
    def decorator(init):
        def decorated(self, *args, **kwargs):
            init(self, *args, **kwargs)
            failed = []
            for base in bases:
                for required_attr in base.required_attrs:
                    try:
                        getattr(self, required_attr)
                    except AttributeError:
                        failed.append(required_attr)
            if failed:
                raise Exception("Missing required attributes: {}".format(', '.join(failed)))
        return decorated
    return decorator


def create_object(bases=(), attributes={}, methods={}):
    "Dynamically creates a new class given a dictionary of information (must contain bases, attributes, and methods)."

    cls_name = attributes['name'].title()

    @validate_attrs(bases)
    def init(self, *args, **kwargs):
        for k, v in attributes.items():
            if v == []:
                setattr(self, k, [])
            else:
                setattr(self, k, v)

    def equals(self, other):
        if self.__class__ != other.__class__:
            return False
        required_attrs = [required for base in bases for required in base.required_attrs]
        attrs = {attr: getattr(self, attr) for attr in required_attrs}
        other_attrs = {attr: getattr(other, attr) for attr in required_attrs}
        return attrs == other_attrs and attrs.values() == other_attrs.values()

    def not_equal(self, other):
        if self.__class__ != other.__class__:
            return True
        required_attrs = [required for base in bases for required in base.required_attrs]
        attrs = {attr: getattr(self, attr) for attr in required_attrs}
        other_attrs = {attr: getattr(other, attr) for attr in required_attrs}
        return attrs != other_attrs or attrs.values() != other_attrs.values()

    def serialise(self):
        """Returns a dictionary of attributes and values for every attribute listed in changeable_attrs in the object's bases
            e.g. {'id': 'dresser', 'attrs': {'is_open': False, 'objects': [{'id': 'chair', 'attrs': {has_user: False}}]}"""
        attrs_dic = {}
        changeable_attrs = [attr for base in bases for attr in base.changeable_attrs]
        for attr in changeable_attrs:
            # if obj.attr is a list of objects, call serialise on each of those objects
            # and store the resulting dictionaries in attrs_dic
            if getattr(self, attr) and isinstance(getattr(self, attr), list):
                objects = getattr(self, attr)
                attrs_dic[attr] = [obj.serialise() for obj in objects]
            # otherwise, obj.attr is a string or boolean and can be put in attrs_dic directly
            else:
                attrs_dic[attr] = getattr(self, attr)
        return {'id': self.id, 'attrs': attrs_dic}

    def get_obj(self, obj_id):
        """Returns nested_object contained within self.objects, given nested_object's id.  
            If it does not exists, returns False"""
        if hasattr(self, 'objects'):
            return [obj for obj in self.objects if obj.id == obj_id][0]
        return None

    def deserialise(self, data):
        """Updates object's attributes to match those in data, which is a serialised dictionary 
            of changeable attributes for that object"""
        for attr, value in data['attrs'].items():
            # if obj.attr is a list of objects, call deserialise on each of those objects
            if hasattr(self, attr) and value and isinstance(value, list):
                for obj_dic in value:
                    obj = self.get_obj(obj_dic['id'])
                    obj.deserialise(obj_dic)
            # otherwise, just update the obj.attr with the new value
            else:
                setattr(self, attr, value)

    # need to set each of the defined methods on the object
    methods['__init__'] = init
    methods['__eq__'] = equals
    methods['__ne__'] = not_equal
    methods['get_obj'] = get_obj
    methods['serialise'] = serialise
    methods['deserialise'] = deserialise

    # and actually create the object
    return type(cls_name, bases, methods)
    