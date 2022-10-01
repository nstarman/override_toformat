##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
from typing import TYPE_CHECKING, Any, Iterator, KeysView, Mapping, ValuesView, overload

# LOCAL
from override_toformat.dispatch import Dispatcher

if TYPE_CHECKING:
    # LOCAL
    from override_toformat.dispatch import All_Dispatchers
    from override_toformat.implementation import RegisterAssistsDecorator, RegisterImplementsDecorator
    from override_toformat.many import RegisterManyAssistsDecorator
    from override_toformat.constraints import TypeConstraint


__all__: list[str] = []


##############################################################################
# CODE
##############################################################################


# @dataclass(frozen=True)  # TODO: when https://github.com/python/mypy/issues/13304 fixed
class FormatOverloader(
    Mapping[
        type,
        Dispatcher[Any],
        # "| Dispatcher[Implements] | Dispatcher[Assists]"
        # Fix when py3.10+ https://bugs.python.org/issue42233
    ]
):
    """Overload for ``to_format``."""

    # self._reg: dict[str, "All_Dispatchers"] = field(default_factory={})

    def __init__(self) -> None:
        # Initialize by calling `__post_init__`, which is included for
        # `dataclasses.dataclass` subclasses.
        self.__post_init__()

    def __post_init__(self) -> None:
        # `_reg` is initialized here for `dataclasses.dataclass` ssubclasses.
        self._reg: dict[type, All_Dispatchers]
        object.__setattr__(self, "_reg", {})  # compatible with frozen dataclass
        # TODO  parametrization of Dispatcher.  Use All_Dispatchers

    # ===============================================================
    # Mapping

    def __getitem__(self, key: str | type, /) -> All_Dispatchers:
        return self._reg[key]

    def __contains__(self, o: object, /) -> bool:
        return o in self._reg

    def __iter__(self) -> Iterator[str | type]:
        return iter(self._reg)

    def __len__(self) -> int:
        return len(self._reg)

    def keys(self) -> KeysView[str | type]:
        return self._reg.keys()

    def values(self) -> ValuesView[All_Dispatchers]:
        return self._reg.values()

    # ===============================================================

    def implements(
        self, format: type, /, dispatch_on: type, *, constraint: type | TypeConstraint | None = None
    ) -> RegisterImplementsDecorator:
        """Register an implementation object."""
        # LOCAL
        from override_toformat.implementation import RegisterImplementsDecorator

        return RegisterImplementsDecorator(
            overloader=self, dispatch_on=dispatch_on, format=format, constraint=constraint
        )

    # ---------------------------------------------------------------

    @overload
    def assists(
        self, formats: type, /, dispatch_on: type, *, constraint: type | TypeConstraint | None = ...
    ) -> RegisterAssistsDecorator:
        ...

    @overload
    def assists(
        self, formats: set[type], /, dispatch_on: type, *, constraint: type | TypeConstraint | None = ...
    ) -> RegisterManyAssistsDecorator:
        ...

    def assists(
        self, formats: type | set[type], /, dispatch_on: type, *, constraint: type | TypeConstraint | None = None
    ) -> RegisterAssistsDecorator | RegisterManyAssistsDecorator:
        """Register an assistance function."""
        # LOCAL
        from override_toformat.implementation import RegisterAssistsDecorator

        if not isinstance(formats, set):
            # `methods` is ignored for funcs
            return RegisterAssistsDecorator(
                overloader=self, format=formats, dispatch_on=dispatch_on, constraint=constraint
            )

        else:
            # LOCAL
            from override_toformat.many import RegisterManyAssistsDecorator

            return RegisterManyAssistsDecorator(
                tuple(
                    (
                        RegisterAssistsDecorator(
                            overloader=self, dispatch_on=dispatch_on, format=fmt, constraint=constraint
                        )
                    )
                    for fmt in formats
                )
            )
