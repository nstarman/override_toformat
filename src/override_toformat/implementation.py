##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any, Callable, ClassVar, Generic, TypeVar, cast

# LOCAL
from override_toformat.dispatch import Dispatcher, DispatchWrapper
from override_toformat.constraints import TypeConstraint, Covariant  # noqa: TC002

if TYPE_CHECKING:
    # LOCAL
    from override_toformat.overload import FormatOverloader

__all__: list[str] = []


##############################################################################
# TYPING

FT = TypeVar("FT", "Implements", "Assists")
C = TypeVar("C", bound="Callable[..., Any]")


##############################################################################
# CODE
##############################################################################

# @dataclass(frozen=True)  # TODO: when https://github.com/python/mypy/issues/13304 fixed
class RegisterOverrideDecoratorBase(Generic[FT]):
    OverrideCls: ClassVar[type]

    # TODO: rm when https://github.com/python/mypy/issues/13304 fixed
    def __init__(
        self, *, dispatch_on: type, format: type, overloader: FormatOverloader, constraint: type | TypeConstraint | None
    ) -> None:
        self.dispatch_on = dispatch_on
        self.format = format
        self.constraint = (
            constraint
            if isinstance(constraint, TypeConstraint)
            else Covariant(dispatch_on if constraint is None else constraint)
        )
        self.__post_init__(overloader)

    def __post_init__(self, overloader: FormatOverloader) -> None:
        # Make single-dispatcher for numpy function
        if not overloader.__contains__(self.format):
            overloader._reg[self.format] = dispatcher = Dispatcher[FT]()
        else:
            dispatcher = cast("Dispatcher[FT]", overloader._reg[self.format])

        self.dispatcher: Dispatcher[FT]
        object.__setattr__(self, "dispatcher", dispatcher)

    def __call__(self, func: C, /) -> C:
        """Register an format overload."""
        # Adding a new numpy function
        implementation = self.OverrideCls(
            func=func, implements=self.format, dispatch_on=self.dispatch_on, constraint=self.constraint
        )

        # Register the function
        self.dispatcher._dispatcher.register(self.dispatch_on, DispatchWrapper(implementation))
        return func


##############################################################################


@dataclass(frozen=True)
class Implements:
    implements: type
    func: Callable[..., Any]
    dispatch_on: type
    constraint: TypeConstraint

    def __call__(
        self, calling_obj: object, _: type, /, *args: Any, **kwargs: Any
    ) -> Any:  # TODO: parametrize return type?
        if not self.constraint.validate_type(calling_obj.__class__):
            raise ValueError(f"object {calling_obj} is not compatible with constraint {self.constraint}")

        return self.func(calling_obj, *args, **kwargs)


# @dataclass(frozen=True)  # TODO: when https://github.com/python/mypy/issues/13304 fixed
class RegisterImplementsDecorator(RegisterOverrideDecoratorBase[Implements]):

    OverrideCls: ClassVar[type[Implements]] = Implements


# ============================================================================


@dataclass(frozen=True)
class Assists:
    implements: type
    func: Callable[..., Any]
    dispatch_on: type
    constraint: TypeConstraint

    def __call__(
        self, calling_obj: object, format: type, /, *args: Any, **kwargs: Any
    ) -> Any:  # TODO: parametrize return type?
        print(calling_obj)
        if not self.constraint.validate_type(calling_obj.__class__):
            raise ValueError(f"object {calling_obj} is not compatible with constraint {self.constraint}")

        return self.func(format, calling_obj, *args, **kwargs)


# @dataclass(frozen=True)  # TODO: when https://github.com/python/mypy/issues/13304 fixed
class RegisterAssistsDecorator(RegisterOverrideDecoratorBase[Assists]):
    OverrideCls: ClassVar[type[Assists]] = Assists
