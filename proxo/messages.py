from __future__ import absolute_import, division, print_function


from functools import partial
from google.protobuf.message import Message

from .protobuf import dict_to_protobuf, protobuf_to_dict


class Map(dict):

    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            setattr(self, k, v)
            # self[k] = v

    @classmethod
    def cast(cls, v):
        if isinstance(v, Map):
            return v
        elif isinstance(v, dict):
            return Map(**v)
        elif hasattr(v, '__iter__'):
            return map(cls.cast, v)
        else:
            return v

    def __setitem__(self, k, v):
        # accidental __missing__ call will create a new node
        super(Map, self).__setitem__(k, self.cast(v))

    def __setattr__(self, k, v):
        prop = getattr(self.__class__, k, None)
        if isinstance(prop, property):  # property binding
            prop.fset(self, v)
        elif hasattr(v, '__call__'):  # method binding
            self.__dict__[k] = v
        else:
            self[k] = v

    def __getattr__(self, k):
        return self[k]

    # def __delattr__(self, k):
    #    del self[k]

    # def __missing__(self, k):
    #    # TODO: consider not using this, silents errors
    #    self[k] = Map()
    #    return self[k]

    def __hash__(self):
        return hash(tuple(self.items()))


class RegisterProxies(type):

    def __init__(cls, name, bases, nmspc):
        super(RegisterProxies, cls).__init__(name, bases, nmspc)
        if not hasattr(cls, 'registry'):
            cls.registry = []
        cls.registry.insert(0, (cls.proto, cls))
        # cls.registry -= set(bases) # Remove base classes

    # Metamethods, called on class objects:
    def __iter__(cls):
        return iter(cls.registry)


class MessageProxy(Map):
    __metaclass__ = RegisterProxies
    proto = Message


decode = partial(protobuf_to_dict, containers=MessageProxy.registry)
encode = partial(dict_to_protobuf, containers=MessageProxy.registry,
                 strict=False)
