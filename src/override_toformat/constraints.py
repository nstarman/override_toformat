"""Classes for defining type constraints in |array_function|_.

|array_function| has an argument ``types``, which is a "collection
:class:`collections.abc.Collection` of unique argument types from the original
NumPy function call that implement |array_function|. The purpose of ``types`` is
to allow implementations of |array_function| to check if all arguments of a type
that the overload knows how to handle. Normally this is implemented inside of
|array_function|, but :mod:`override_toformat` gives overloading functions more
flexibility to set constrains on a per-overloaded function basis.
"""

##############################################################################
# IMPORTS

from __future__ import annotations

from abc import ABCMeta, abstractmethod
from dataclasses import dataclass

from mypy_extensions import mypyc_attr

__all__ = ["TypeConstraint", "Invariant", "Covariant", "Contravariant", "Between"]
__doctest_skip__ = ["*"]  # TODO: figure out weird dataclass error


##############################################################################
# CODE
##############################################################################


@mypyc_attr(allow_interpreted_subclasses=True)
class TypeConstraint(metaclass=ABCMeta):
    r"""ABC for constraining an argument type.

    .. warning::

        This class will be converted to a runtime-checkable `Protocol` when
        mypyc behaves nicely with runtime_checkable interpreted subclasses
        (see https://github.com/mypyc/mypyc/issues/909).

    Examples
    --------
    It's very easy to define a custom type constraint.

        >>> from dataclasses import dataclass
        >>> from override_toformat.constraints import TypeConstraint

        >>> @dataclass(frozen=True)
        ... class ThisOrThat(TypeConstraint):
        ...     this: type
        ...     that: type
        ...     def validate_type(self, arg_type: type, /) -> bool:
        ...         return arg_type is self.this or arg_type is self.that
    """

    @abstractmethod
    def validate_type(self, arg_type: type, /) -> bool:
        """Validate the argument type.

        This is used in :class:`override_toformat.mixin.NPArrayFuncOverloadMixin`
        and subclasses like :class:`override_toformat.mixin.NPArrayOverloadMixin`
        to ensure that the input is of the correct set of types to work
        with the |array_function|_ override.

        Parameters
        ----------
        arg_type : type, positional-only
            The type of the argument that must fit the type constraint.

        Returns
        -------
        bool
            Whether the type is valid.

        Examples
        --------
        The simplest built-in type constraint is
        :class:`override_toformat.constraints.Invariant`.

            >>> from override_toformat.constraints import Invariant
            >>> constraint = Invariant(int)
            >>> constraint.validate_type(int)  # exact type
            True
            >>> constraint.validate_type(bool)  # subclass
            False
        """

    def validate_object(self, arg: object, /) -> bool:
        """Validate an argument.

        This is used in :class:`override_toformat.mixin.NPArrayFuncOverloadMixin`
        and subclasses like :class:`override_toformat.mixin.NPArrayOverloadMixin`
        to ensure that the input is of the correct set of types to work
        with the |array_function|_ override.

        Parameters
        ----------
        arg : object, positional-only
            The argument that's type must fit the type constraint.

        Returns
        -------
        bool
            Whether the type is valid.

        Examples
        --------
        The simplest built-in type constraint is
        :class:`override_toformat.constraints.Invariant`.

            >>> from override_toformat.constraints import Invariant
            >>> constraint = Invariant(int)
            >>> constraint.validate_type(int)  # exact type
            True
            >>> constraint.validate_type(bool)  # subclass
            False
        """
        return self.validate_type(type(arg))


@mypyc_attr(allow_interpreted_subclasses=True)
@dataclass(frozen=True)
class Invariant(TypeConstraint):
    r"""Type constraint for invariance -- the exact type.

    This is equivalent to ``arg_type is bound``.

    Parameters
    ----------
    bound : type
        The exact type of the argument.

    Notes
    -----
    When compiled this class permits interpreted subclasses, see
    https://mypyc.readthedocs.io/en/latest/native_classes.html.

    Examples
    --------
    Construct the constraint object:

        >>> constraint = Invariant(int)

    This can be used to validate argument types:

        >>> constraint.validate_type(int)  # exact type
        True
        >>> constraint.validate_type(bool)  # subclass
        False
        >>> constraint.validate_type(object)  # superclass
        False
    """

    bound: type

    def validate_type(self, arg_type: type, /) -> bool:
        """Validate the argument type.

        Parameters
        ----------
        arg_type : type, positional-only
            The type of the argument that must fit the type constraint.

        Returns
        -------
        bool
            Whether the type is valid.
        """
        return arg_type is self.bound


@mypyc_attr(allow_interpreted_subclasses=True)
@dataclass(frozen=True)
class Covariant(TypeConstraint):
    r"""A covariant constraint -- permitting subclasses.

    This is the most common constraint, equivalent to ``issubclass(arg_type,
    bound)``.

    Parameters
    ----------
    bound : type
        The parent type of the argument.

    Notes
    -----
    When compiled this class permits interpreted subclasses, see
    https://mypyc.readthedocs.io/en/latest/native_classes.html.

    Examples
    --------
    Construct the constraint object:

        >>> constraint = Covariant(int)

    This can be used to validate argument types:

        >>> constraint.validate_type(int)  # exact type
        True
        >>> constraint.validate_type(bool)  # subclass
        True
        >>> constraint.validate_type(object)  # superclass
        False
    """

    bound: type

    def validate_type(self, arg_type: type, /) -> bool:
        """Validate the argument type.

        Parameters
        ----------
        arg_type : type, positional-only
            The type of the argument that must fit the type constraint.

        Returns
        -------
        bool
            Whether the type is valid.
        """
        return issubclass(arg_type, self.bound)


@mypyc_attr(allow_interpreted_subclasses=True)
@dataclass(frozen=True)
class Contravariant(TypeConstraint):
    r"""A contravariant constraint -- permitting superclasses.

    An uncommon constraint. See examples for why.

    Parameters
    ----------
    bound : type
        The child type of the argument.

    Notes
    -----
    When compiled this class permits interpreted subclasses, see
    https://mypyc.readthedocs.io/en/latest/native_classes.html.

    Examples
    --------
    Construct the constraint object:

        >>> constraint = Contravariant(int)

    This can be used to validate argument types:

        >>> constraint.validate_type(int)  # exact type
        True
        >>> constraint.validate_type(bool)  # subclass
        False
        >>> constraint.validate_type(object)  # superclass
        True
    """

    bound: type

    def validate_type(self, arg_type: type, /) -> bool:
        """Validate the argument type.

        Parameters
        ----------
        arg_type : type, positional-only
            The type of the argument that must fit the type constraint.

        Returns
        -------
        bool
            Whether the type is valid.
        """
        return issubclass(self.bound, arg_type)


@mypyc_attr(allow_interpreted_subclasses=True)
@dataclass(frozen=True)
class Between(TypeConstraint):
    r"""Type constrained between two types.

    This combines the functionality of
    :class:`~override_toformat.constraints.Covariant` and
    :class:`~override_toformat.constraints.Contravariant`.

    Parameters
    ----------
    lower_bound : type
        The child type of the argument.
    upper_bound : type
        The parent type of the argument.

    Notes
    -----
    When compiled this class permits interpreted subclasses, see
    https://mypyc.readthedocs.io/en/latest/native_classes.html

    Examples
    --------
    For this example we need a type hierarchy:

        >>> class A: pass
        >>> class B(A): pass
        >>> class C(B): pass
        >>> class D(C): pass
        >>> class E(D): pass

    Construct the constraint object:

        >>> constraint = Between(D, B)

    This can be used to validate argument types:

        >>> constraint.validate_type(A)
        False
        >>> constraint.validate_type(B)
        True
        >>> constraint.validate_type(C)
        True
        >>> constraint.validate_type(D)
        True
        >>> constraint.validate_type(E)
        False
    """

    lower_bound: type
    upper_bound: type

    def validate_type(self, arg_type: type, /) -> bool:
        """Validate the argument type.

        Parameters
        ----------
        arg_type : type
            The type of the argument.

        Returns
        -------
        bool
        """
        return issubclass(self.lower_bound, arg_type) & issubclass(arg_type, self.upper_bound)

    @property
    def bounds(self) -> tuple[type, type]:
        """Return tuple of (lower, upper) bounds.

        The lower bound is contravariant, the upper bound covariant.

        Examples
        --------
        For this example we need a type hierarchy:

            >>> class A: pass
            >>> class B(A): pass
            >>> class C(B): pass

            >>> constraint = Between(C, B)
            >>> constraint.bounds
            (C, B)
        """
        return (self.lower_bound, self.upper_bound)
