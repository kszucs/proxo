from __future__ import absolute_import, division, print_function

import pytest

from proxo.messages import RegisterProxies, MessageProxy, Map


@pytest.fixture
def d():
    return {'a': 1,
            'b': [{'j': 9},
                  {'g': 7, 'h': 8}],
            'c': {'d': 4,
                  'e': {'f': 6}}}


def test_map_init(d):
    m = Map(**d)
    assert isinstance(m, Map)
    assert isinstance(m, dict)


def test_map_get(d):
    m = Map(**d)
    assert m['a'] == 1
    assert m['c']['e']['f'] == 6
    assert m['b'][0]['j'] == 9
    assert m['b'][1]['g'] == 7
    assert isinstance(m['b'], list)
    assert isinstance(m['b'][1], Map)


def test_map_dot_get(d):
    m = Map(**d)
    assert m.a == 1
    assert m.c.e.f == 6
    assert m.b[0].j == 9
    assert m.b[1].g == 7
    assert isinstance(m.b, list)
    assert isinstance(m.b[1], Map)


def test_map_set(d):
    m = Map(**d)
    m['A'] = 11
    m['a'] = 'one'
    m['z'] = {'Z': {'omega': 20}}
    assert m['a'] == 'one'
    assert m['A'] == 11
    assert m['z']['Z']['omega'] == 20
    assert isinstance(m['z'], Map)
    assert isinstance(m['z']['Z'], Map)


def test_map_dot_set(d):
    m = Map(**d)
    m.A = 11
    m.a = 'one'
    m.z = {'Z': {'omega': 20}}
    assert m.a == 'one'
    assert m.A == 11
    assert m.z.Z.omega == 20
    assert isinstance(m.z, Map)
    assert isinstance(m.z.Z, Map)


def test_hash():
    d1 = Map(a=Map(b=3), c=5)
    d2 = Map(a=Map(b=3), c=5)
    d3 = Map(a=Map(b=6), c=5)

    assert hash(d1) == hash(d2)
    assert hash(d1) != hash(d3)
    assert hash(d2) != hash(d3)


def test_dict_hashing():
    d2 = Map(a=Map(b=3), c=5)
    d3 = Map(a=Map(b=6), c=5)

    c = {}
    c[d2.a] = d2
    c[d3.a] = d3

    assert c[d2.a] == d2
    assert c[d3.a] == d3


def test_register_proxies():
    class Base(object):
        __metaclass__ = RegisterProxies
        proto = 'base'

    class First(Base):
        proto = 'first'

    class Second(Base):
        proto = 'second'

    class Third(Base):
        proto = 'third'

    assert Base.registry == [('third', Third),
                             ('second', Second),
                             ('first', First),
                             ('base', Base)]
