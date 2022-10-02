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
    x: array

    FMT_OVERLOADS: ClassVar[ToFormatOverloader] = ToFormatOverloader()


a = ClassA(array("d", [1.0, 2.0, 3.14]))


# -------------------------------------------------------------------


@dataclass
class ClassB(ClassA):
    pass


b = ClassB(array("d", [1.0, 2.0, 3.14]))


# -------------------------------------------------------------------


@dataclass
class ClassC(ClassB):
    pass


c = ClassC(array("d", [1.0, 2.0, 3.14]))


# -------------------------------------------------------------------


@dataclass
class ClassD(ClassA):
    y: array


d = ClassD(array("d", [1.0, 2.0, 3.14]), array("d", [4.0, 5.0, 6.28]))


#####################################################################


@dataclass
class Class1(ToFormatOverloadMixin):
    attr1: array

    FMT_OVERLOADS: ClassVar[ToFormatOverloader] = ToFormatOverloader()


o1 = Class1(array("d", [1.0, 2.0, 3.14]))


# -------------------------------------------------------------------


@dataclass
class Class2(Class1):
    pass


o12 = Class2(array("d", [1.0, 2.0, 3.14]))
