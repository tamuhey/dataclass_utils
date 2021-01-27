import pytest
from typing import Dict, List, Optional, Union
from dataclass_utils import runtime_typecheck
import dataclasses


@runtime_typecheck
@dataclasses.dataclass
class Foo:
    a: int
    b: List[str]
    c: List[List[Dict[str, int]]] = dataclasses.field(default_factory=list)
    d: Union[int, str, None] = None
    e: Optional[int] = None


@runtime_typecheck
@dataclasses.dataclass
class Bar:
    foo: Foo


def test_basic():
    x0 = Foo(1, ["a"])
    x1 = Foo(a=1, b=["a"])
    x2 = Foo(1, b=["a"])
    isinstance(x0, Foo)
    isinstance(x1, Foo)
    isinstance(x2, Foo)
    assert x0 == x1
    assert x0 == x2

    with pytest.raises(TypeError):
        Foo("a", 2)


def test_generic():
    Foo(1, ["foo", "bar"])
    with pytest.raises(TypeError):
        Foo(1, [1, 2])
    with pytest.raises(TypeError):
        Foo(1, [1, "foo"])


def test_nested_generic():
    Foo(1, [], [[{"a": 2}]])
    with pytest.raises(TypeError):
        Foo(1, [], [[{"a": "b"}]])


def test_union():
    # Union
    Foo(1, [], d=None)
    Foo(1, [], d=1)
    with pytest.raises(TypeError):
        Foo(1, [], d=1.2)
