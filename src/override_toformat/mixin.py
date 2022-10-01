r"""Mixins for adding |to_format| methods."""

##############################################################################
# IMPORTS

from __future__ import annotations

# STDLIB
from typing import TYPE_CHECKING, Any, ClassVar

# THIRDPARTY
from mypy_extensions import mypyc_attr, trait

if TYPE_CHECKING:
    # LOCAL
    from override_toformat.overload import FormatOverloader


__all__: list[str] = []


##############################################################################
# CODE
##############################################################################


@mypyc_attr(allow_interpreted_subclasses=True)
@trait
class FormatOverloadMixin:
    """Mixin for adding |array_function|_ to a class.

    Attributes
    ----------
    FMT_OVERLOADS : |FormatOverloader|
        A class-attribute of an instance of |FormatOverloader|.
    """

    FMT_OVERLOADS: ClassVar[FormatOverloader]
    """A class-attribute of an instance of |FormatOverloader|."""

    def to_format(self, format: type, /, *args: Any, **kwargs: Any) -> Any:
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
        # dispatch on format, then on self-type. Call the resulting implementation.
        return self.FMT_OVERLOADS(format)(self)(self, format, *args, **kwargs)
