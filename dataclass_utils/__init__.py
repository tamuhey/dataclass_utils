r"""

# Example

## `check_type` function

>>> import dataclasses
>>> from typing import List
>>> @dataclasses.dataclass
... class Foo:
...     a: int
...     b: List[str]

>>> import pytest
>>> check_type(Foo(1, ["b"])) # OK
>>> with pytest.raises(TypeError):
...     check_type(Foo("a", [2]))

## `runtime_typecheck` decorator

>>> from typing import List
>>> @runtime_typecheck
... @dataclasses.dataclass
... class Foo:
...     a: int
...     b: List[str]


>>> foo = Foo(1, ["a"])  # ok
>>> assert isinstance(foo, Foo) # Still, it is an instance of `Foo`
>>> import pytest
>>> with pytest.raises(TypeError):
...     Foo("a", [])
>>> with pytest.raises(TypeError):
...     Foo(1, [1, 2])
"""

from typing import Type, TypeVar

from dataclass_utils.type_checker import check_root as check_type
from dataclass_utils.type_checker import runtime_typecheck_inner

T = TypeVar("T")


def runtime_typecheck(ty: Type[T]) -> Type[T]:
    return runtime_typecheck_inner(ty)  # type: ignore


__all__ = ["runtime_typecheck", "check_type"]
