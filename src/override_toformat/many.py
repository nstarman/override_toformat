"""Class for registering `~override_toformat.ToFormatOverloader.assists` funcs."""

from __future__ import annotations

# STDLIB
from dataclasses import dataclass
from typing import Any, Callable, TypeVar

# LOCAL
from override_toformat.implementation import RegisterImplementsDecorator

__all__: list[str] = []

##############################################################################
# TYPING

C = TypeVar("C", bound=Callable[..., Any])
Self = TypeVar("Self", bound="RegisterManyImplementsDecorator")


##############################################################################
# CODE
##############################################################################


@dataclass(frozen=True)
class RegisterManyImplementsDecorator:
    """Class for registering `~override_toformat.ToFormatOverloader.assists` funcs.

    Parameters
    ----------
    decorators : tuple[RegisterImplementsDecorator, ...]
        `tuple` of ``RegisterImplementsDecorator``.

    __wrapped__ : Callable[..., Any] | None
        The assistance function which this object wraps. ``__call__`` must be
        used before this is not `None`.
    """

    decorators: tuple[RegisterImplementsDecorator, ...]
    """`tuple` of ``RegisterImplementsDecorator``."""

    def __post_init__(self) -> None:
        self.__wrapped__: Callable[..., Any]
        object.__setattr__(self, "__wrapped__", None)  # set in `__call__`

        self._is_set: bool
        object.__setattr__(self, "_is_set", False)  # set in `__call__`

    def __call__(self: Self, assists_func: Callable[..., Any], /) -> Self:
        """Register ``assists_func`` with for all overloads.

        This function can only be called once.

        Parameters
        ----------
        assists_func : Callable[..., R]
            Assistance function.

        Returns
        -------
        RegisterManyImplementsDecorator
        """
        if self._is_set:
            raise ValueError

        object.__setattr__(self, "__wrapped__", assists_func)

        # Iterate through, evaluating the contained decorator. Just evaluating
        # the decorator is enough to activate it.
        for dec in self.decorators:
            dec(assists_func)

        object.__setattr__(self, "_is_set", True)  # prevent re-calling
        return self
