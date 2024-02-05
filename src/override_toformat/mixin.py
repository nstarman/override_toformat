r"""Mixins for adding |to_format| methods."""

##############################################################################
# IMPORTS

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from mypy_extensions import mypyc_attr

if TYPE_CHECKING:
    from override_toformat.overload import ToFormatOverloader


__all__: list[str] = []


##############################################################################
# CODE
##############################################################################


@mypyc_attr(allow_interpreted_subclasses=True)
class ToFormatOverloadMixin:
    """Mixin for adding |array_function|_ to a class.

    Attributes
    ----------
    FMT_OVERLOADS : |ToFormatOverloader|
        A class-attribute of an instance of |ToFormatOverloader|.

    """

    FMT_OVERLOADS: ClassVar[ToFormatOverloader]
    """A class-attribute of an instance of |ToFormatOverloader|."""

    def to_format(self, format: type, /, *args: Any, **kwargs: Any) -> Any:  # noqa: A002
        """Transform width to specified format.

        Parameters
        ----------
        format : type, positional-only
            The format type to which to transform this width.
        *args : Any
            Arguments into ``to_format``.
        **kwargs : Any
            Keyword-arguments into ``to_format``.

        Returns
        -------
        object
            Width transformed to specified type.

        Raises
        ------
        ValueError
            If format is not one of the recognized types.

        """
        return self.FMT_OVERLOADS(format)(self)(self, format, *args, **kwargs)
