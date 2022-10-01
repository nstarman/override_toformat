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
        # Check if can be dispatched.
        # we work up the MRO if it's a type.
        if self.FMT_OVERLOADS.__contains__(format):  # type
            key = format
        else:
            for kls in format.mro():
                if self.FMT_OVERLOADS.__contains__(kls):
                    key = kls
                    break
            else:
                raise ValueError(f"format {format} is not known -- {self.FMT_OVERLOADS.keys()}")

        # get Assists/Implements from single-dispatch on type of self.
        fmtwrap = self.FMT_OVERLOADS[key](self)

        print(fmtwrap)

        return fmtwrap(self, format, *args, **kwargs)
