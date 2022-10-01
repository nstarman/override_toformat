"""`~functools.singledispatch`

.. todo::

    - mypyc compile when https://github.com/python/mypy/issues/13613 and
      https://github.com/python/mypy/issues/13304 are resolved.
"""

##############################################################################
# IMPORTS

from __future__ import annotations
from dataclasses import dataclass

# STDLIB
from functools import singledispatch
from typing import TYPE_CHECKING, Any, Generic, TypeVar, final

if TYPE_CHECKING:
    # STDLIB
    import functools

    # LOCAL
    from override_toformat.implementation import Implements, Assists

__all__: list[str] = []


##############################################################################
# TYPING

WT = TypeVar("WT", "Implements", "Assists")


##############################################################################
# CODE
##############################################################################


@final
class Dispatcher(Generic[WT]):
    """`~functools.singledispatch` instance."""

    def __init__(self) -> None:
        @singledispatch
        def dispatcher(obj: object, /) -> WT:
            raise NotImplementedError  # See Mixin for handling.

        self._dispatcher: functools._SingleDispatchCallable[WT]
        self._dispatcher = dispatcher

    def __call__(self, obj: object, /) -> WT:
        """
        Get correct wrapper for the calling object's type.

        Parameters
        ----------
        obj : object, positional-only
            object for calling the `~functools.singledispatch` .

        Returns
        -------
        ``WT``
            One of `override_toformat.func.Implements`,
            `override_toformat.func.Assists`.
        """
        return self._dispatcher(obj)


@dataclass(frozen=True)
class DispatchWrapper(Generic[WT]):
    """
    `~functools.singledispatch` calls the dispatched functions.
    This wraps that function so the single-dispatch instead returns the function.

    Parameters
    ----------
    __wrapped__ : `Implements` or `Assists` or `ImplementsUFunc` or `AssistsUFunc`
        The result of calling ``Dispatch``.
    """

    __wrapped__: WT  # Dispatch wrapper

    def __call__(self, *_: Any, **__: Any) -> WT:
        """Return ``__wrapped__``, ignoring input."""
        return self.__wrapped__  # `Dispatch` wrapper


All_Dispatchers = Dispatcher[Any]  # TODO: parametrization of Dispatcher
