import pytest

# LOCAL
from override_toformat.constraints import Invariant
from .data import Class1, Class2, ClassA, a


@ClassA.FMT_OVERLOADS.implements(from_format=ClassA, to_format=Class1, from_constraint=Invariant(ClassA), to_constraint=Invariant(Class1))
def letter_to_number(cls, obj):
    return cls(obj.x)


def test_A_to_1():
    got = a.to_format(Class1)

    assert isinstance(got, Class1)
    assert got.attr1 is a.x


def test_A_to_2():
    with pytest.raises(ValueError, match="format 'Class2' is not compatible with to_constraint"):
        a.to_format(Class2)
