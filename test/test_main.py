import pytest
from typing import List
from dataclass_utils import runtime_typecheck
import dataclasses


@runtime_typecheck
@dataclasses.dataclass
class Foo:
    a: int
    b: List[str]


def test_main():
    foo = Foo(1, ["a"])
    isinstance(foo, Foo)
    with pytest.raises(AssertionError):
        Foo("a", 2)
    with pytest.raises(AssertionError):
        Foo(1, [1, 2])
