##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
from typing import TYPE_CHECKING, Iterator, KeysView, Mapping, ValuesView, overload

# LOCAL
from override_toformat.dispatch import Dispatcher, FormatDispatcher
from override_toformat.implementation import RegisterImplementsDecorator
from override_toformat.many import RegisterManyImplementsDecorator

if TYPE_CHECKING:
    # LOCAL
    from override_toformat.constraints import TypeConstraint


__all__: list[str] = []


##############################################################################
# CODE
##############################################################################


# @dataclass(frozen=True)  # TODO!
class ToFormatOverloader(Mapping[type, Dispatcher]):
    """Overload for ``to_format``."""

    # self._reg: dict[str, "All_Dispatchers"] = field(default_factory={})

    def __init__(self) -> None:
        # Initialize by calling `__post_init__`, which is included for
        # `dataclasses.dataclass` subclasses.
        self.__post_init__()

    def __post_init__(self) -> None:
        self._dispatcher: FormatDispatcher
        object.__setattr__(self, "_dispatcher", FormatDispatcher())

    def __call__(self, key: type, /) -> Dispatcher:
        return self._dispatcher(key)

    # ===============================================================
    # Mapping

    def __getitem__(self, key: type, /) -> Dispatcher:
        return self._dispatcher.registry[key]()

    def __contains__(self, o: object, /) -> bool:
        return o in self._dispatcher.registry

    def __iter__(self) -> Iterator[type]:
        return iter(self._dispatcher.registry)

    def __len__(self) -> int:
        return len(self._dispatcher.registry)

    def keys(self) -> KeysView[type]:
        return self._dispatcher.registry.keys()

    def values(self) -> ValuesView[Dispatcher]:
        return {k: v() for k, v in self._dispatcher.registry.items()}.values()

    # ===============================================================

    @overload
    def implements(
        self,
        to_format: type,
        from_format: type,
        *,
        from_constraint: type | TypeConstraint | None = ...,
        to_constraint: type | TypeConstraint | None = ...,
    ) -> RegisterImplementsDecorator:
        ...

    @overload
    def implements(
        self,
        to_format: set[type],
        from_format: type,
        *,
        from_constraint: type | TypeConstraint | None = ...,
        to_constraint: type | TypeConstraint | None = ...,
    ) -> RegisterManyImplementsDecorator:
        ...

    def implements(
        self,
        to_format: type | set[type],
        from_format: type,
        *,
        from_constraint: type | TypeConstraint | None = None,
        to_constraint: type | TypeConstraint | None = None,
    ) -> RegisterImplementsDecorator | RegisterManyImplementsDecorator:
        """Register an assistance function."""
        if not isinstance(to_format, set):
            # `methods` is ignored for funcs
            return RegisterImplementsDecorator(
                overloader=self,
                to_format=to_format,
                from_format=from_format,
                from_constraint=from_constraint,
                to_constraint=to_constraint,
            )

        else:
            return RegisterManyImplementsDecorator(
                tuple(
                    (
                        RegisterImplementsDecorator(
                            overloader=self,
                            from_format=from_format,
                            to_format=fmt,
                            from_constraint=from_constraint,
                            to_constraint=to_constraint,
                        )
                    )
                    for fmt in to_format
                )
            )
