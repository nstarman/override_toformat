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
from typing import TYPE_CHECKING, Any, final

if TYPE_CHECKING:
    # STDLIB
    import functools

    # LOCAL
    from override_toformat.implementation import Implements

__all__: list[str] = []


##############################################################################
# CODE
##############################################################################


@final
class Dispatcher:
    """`~functools.singledispatch` instance."""

    def __init__(self) -> None:
        @singledispatch
        def dispatcher(obj: object, /) -> Implements:
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


@dataclass(frozen=True)
class DispatchWrapper:
    """
    `~functools.singledispatch` calls the dispatched functions.
    This wraps that function so the single-dispatch instead returns the function.

    Parameters
    ----------
    __wrapped__ : `Implements`
        The result of calling ``Dispatch``.
    """

    __wrapped__: Implements  # Dispatch wrapper

    def __call__(self, *_: Any, **__: Any) -> Implements:
        """Return ``__wrapped__``, ignoring input."""
        return self.__wrapped__  # `Dispatch` wrapper
