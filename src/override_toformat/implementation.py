"""Implementation decorator."""

from __future__ import annotations

# STDLIB
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, TypeVar

# LOCAL
from override_toformat.constraints import Covariant, TypeConstraint
from override_toformat.dispatch import Dispatcher

if TYPE_CHECKING:
    # LOCAL
    from override_toformat.overload import ToFormatOverloader

__all__: list[str] = []


##############################################################################
# TYPING

C = TypeVar("C", bound="Callable[..., Any]")


##############################################################################
# CODE
##############################################################################


@dataclass(frozen=True)
class Implements:
    """A class that implements an overload."""

    converter: Callable[..., Any]
    from_format: type
    to_format: type
    from_constraint: TypeConstraint
    to_constraint: TypeConstraint

    def __call__(
        self, from_obj: object, to_format: type, /, *args: Any, **kwargs: Any
    ) -> Any:  # TODO: parametrize return type?
        """Call the converter.

        Parameters
        ----------
        from_obj : object, positional-only
            object to convert from.
        to_format : type, positional-only
            format to convert to.
        *args : Any
            positional arguments to pass to the converter.
        **kwargs : Any
            keyword arguments to pass to the converter.

        Returns
        -------
        Any
            The converted object.

        Raises
        ------
        ValueError
            If the object or format is not compatible with the constraints.
        """
        if not self.from_constraint.validate_type(from_obj.__class__):
            msg = f"object {from_obj!r} is not compatible with from_constraint {self.from_constraint}"
            raise ValueError(msg)
        elif not self.to_constraint.validate_type(to_format):
            msg = f"format {to_format.__qualname__!r} is not compatible with to_constraint {self.to_constraint}"
            raise ValueError(msg)

        return self.converter(to_format, from_obj, *args, **kwargs)

    @property
    def formats(self) -> tuple[type, type]:
        """Return the from-to format tuple."""
        return (self.from_format, self.to_format)


class RegisterImplementsDecorator:
    """Decorator to register an ``implements`` overload."""

    def __init__(
        self,
        *,
        from_format: type,
        to_format: type,
        overloader: ToFormatOverloader,
        from_constraint: type | TypeConstraint | None,
        to_constraint: type | TypeConstraint | None,
    ) -> None:
        self.from_format = from_format
        self.to_format = to_format
        self.from_constraint = (
            from_constraint
            if isinstance(from_constraint, TypeConstraint)
            else Covariant(from_format if from_constraint is None else from_constraint)
        )
        self.to_constraint = (
            to_constraint
            if isinstance(to_constraint, TypeConstraint)
            else Covariant(to_format if to_constraint is None else to_constraint)
        )
        self.__post_init__(overloader)

    def __post_init__(self, overloader: ToFormatOverloader) -> None:
        # Make single-dispatcher for format
        if not overloader.__contains__(self.to_format):
            dispatcher = Dispatcher()
            overloader._dispatcher.register(self.to_format, dispatcher)
        else:
            dispatcher = overloader._dispatcher.registry[self.to_format]()

        self.dispatcher: Dispatcher
        object.__setattr__(self, "dispatcher", dispatcher)

    def __call__(self, converter: C, /) -> C:
        """Register an format overload."""
        # Adding a new format
        implementation = Implements(
            from_format=self.from_format,
            to_format=self.to_format,
            converter=converter,
            from_constraint=self.from_constraint,
            to_constraint=self.to_constraint,
        )
        # Register the function
        self.dispatcher.register(self.from_format, implementation)
        return converter
