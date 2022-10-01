# STDLIB
from array import array
from dataclasses import dataclass
from typing import ClassVar

# LOCAL
from override_toformat import FormatOverloader, FormatOverloadMixin


@dataclass
class ClassA(FormatOverloadMixin):
    x: array

    FMT_OVERLOADS: ClassVar[FormatOverloader] = FormatOverloader()


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
class Class1(FormatOverloadMixin):
    attr1: array

    FMT_OVERLOADS: ClassVar[FormatOverloader] = FormatOverloader()


o1 = Class1(array("d", [1.0, 2.0, 3.14]))


# -------------------------------------------------------------------


@dataclass
class Class2(Class1):
    pass


o12 = Class2(array("d", [1.0, 2.0, 3.14]))
