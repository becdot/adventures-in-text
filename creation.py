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
            if v == None:
                setattr(self, k, [])
            else:
                setattr(self, k, v)

    methods['__init__'] = init

    return type(cls_name, bases, methods)