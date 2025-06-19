from neomodel import StringProperty, IntegerProperty

from src.generator.models import MetaInfo


class ObjectMetaMixin:
    name = StringProperty(required=True)
    path = StringProperty(required=True)
    start_line = IntegerProperty()
    end_line = IntegerProperty()
    docstring = StringProperty()


a = set(filter(lambda x: '__' not in x, ObjectMetaMixin.__dict__))
b = set(MetaInfo.__dataclass_fields__.keys())

assert a == b, f"Fields do not match! (ObjectMetaMixin, MetaInfo). Difference: {a - b}"
