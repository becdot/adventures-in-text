from scaffolding import Object
from properties import Openable, Lightable, UnreachableLight, Gettable, Climbable, Container

def validate_attrs(bases):
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
        return {attr: getattr(self, attr) for base in bases for attr in base.changeable_attrs}

    def deserialise(self, data):
        for attr, value in data.items():
            if hasattr(self, attr):
                setattr(self, attr, value)

    methods['__init__'] = init
    methods['serialise'] = serialise
    methods['deserialise'] = deserialise
    methods['__eq__'] = equals
    methods['__ne__'] = not_equal

    return type(cls_name, bases, methods)