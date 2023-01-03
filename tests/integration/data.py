"""Integration test data."""

from __future__ import annotations

# STDLIB
from array import array
from dataclasses import dataclass
from typing import ClassVar

# LOCAL
from override_toformat.mixin import ToFormatOverloadMixin
from override_toformat.overload import ToFormatOverloader


@dataclass
class ClassA(ToFormatOverloadMixin):
    """Class A."""

    x: array

    FMT_OVERLOADS: ClassVar[ToFormatOverloader] = ToFormatOverloader()


a = ClassA(array("d", [1.0, 2.0, 3.14]))


# -------------------------------------------------------------------


@dataclass
class ClassB(ClassA):
    """Class B."""


b = ClassB(array("d", [1.0, 2.0, 3.14]))


# -------------------------------------------------------------------


@dataclass
class ClassC(ClassB):
    """Class C."""


c = ClassC(array("d", [1.0, 2.0, 3.14]))


# -------------------------------------------------------------------


@dataclass
class ClassD(ClassA):
    """Class D."""

    y: array


d = ClassD(array("d", [1.0, 2.0, 3.14]), array("d", [4.0, 5.0, 6.28]))


#####################################################################


@dataclass
class Class1(ToFormatOverloadMixin):
    """Class 1."""

    attr1: array

    FMT_OVERLOADS: ClassVar[ToFormatOverloader] = ToFormatOverloader()


o1 = Class1(array("d", [1.0, 2.0, 3.14]))


# -------------------------------------------------------------------


@dataclass
class Class2(Class1):
    """Class2."""


o12 = Class2(array("d", [1.0, 2.0, 3.14]))
