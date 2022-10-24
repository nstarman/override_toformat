"""`~functools.singledispatch`

.. todo::

    - mypyc compile when https://github.com/python/mypy/issues/13613 and
      https://github.com/python/mypy/issues/13304 are resolved.
"""

##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
from dataclasses import dataclass
from functools import singledispatch
from typing import TYPE_CHECKING, Any, Generic, TypeVar, cast, final

if TYPE_CHECKING:
    # STDLIB
    import functools
    from types import MappingProxyType

    # LOCAL
    from override_toformat.implementation import Implements

__all__: list[str] = []


##############################################################################
# TYPING

T = TypeVar("T")


##############################################################################
# CODE
##############################################################################


@final
class Dispatcher:
    """`~functools.singledispatch` instance."""

    def __init__(self) -> None:
        @singledispatch
        def dispatcher(obj: object, /, *args: Any, **kwargs: Any) -> Implements:
            raise NotImplementedError  # See Mixin for handling.

        self._dispatcher: functools._SingleDispatchCallable[Implements]
        self._dispatcher = dispatcher

    def __call__(self, obj: object, /) -> Implements:
        """
        Get correct wrapper for the calling object's type.

        Parameters
        ----------
        obj : object, positional-only
            object for calling the `~functools.singledispatch` .

        Returns
        -------
        `override_toformat.func.Implements`
        """
        return self._dispatcher(obj)

    def register(self, cls: type, impl: Implements, /) -> None:
        self._dispatcher.register(cls, DispatchWrapper(impl))
        return None


@dataclass(frozen=True)
class DispatchWrapper(Generic[T]):
    """
    `~functools.singledispatch` calls the dispatched functions.
    This wraps that function so the single-dispatch instead returns the function.

    Parameters
    ----------
    __wrapped__ : `Implements`
        The result of calling ``Dispatch``.
    """

    __wrapped__: T  # Dispatch wrapper

    def __call__(self, *_: Any, **__: Any) -> T:
        """Return ``__wrapped__``, ignoring input."""
        return self.__wrapped__  # `Dispatch` wrapper


@final
class FormatDispatcher:
    """`~functools.singledispatch` instance."""

    def __init__(self) -> None:
        @singledispatch
        def dispatcher(obj: object, /, *args: Any, **kwargs: Any) -> Dispatcher:
            raise NotImplementedError  # See Mixin for handling.

        self._dispatcher: functools._SingleDispatchCallable[Dispatcher]
        self._dispatcher = dispatcher

    def __call__(self, type: type, /) -> Dispatcher:
        return self._dispatcher.dispatch(type)()

    def register(self, cls: type, dispatcher: Dispatcher, /) -> None:
        self._dispatcher.register(cls, DispatchWrapper(dispatcher))
        return None

    @property
    def registry(self) -> MappingProxyType[type, DispatchWrapper[Dispatcher]]:
        return cast("MappingProxyType[type, DispatchWrapper[Dispatcher]]", self._dispatcher.registry)
