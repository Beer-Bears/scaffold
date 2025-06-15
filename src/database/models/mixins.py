from neomodel import StringProperty, IntegerProperty


class ObjectMetaMixin:
    name = StringProperty(required=True)
    lineno = IntegerProperty()
    docstring = StringProperty()
