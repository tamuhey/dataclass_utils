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
    Foo(1, ["a"])
    with pytest.raises(AssertionError):
        Foo("a", 2)
