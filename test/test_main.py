import pytest
from typing import (
    Any,
    AnyStr,
    Callable,
    Dict,
    FrozenSet,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Union,
)
from dataclass_utils import check_type, runtime_typecheck
import dataclasses


@runtime_typecheck
@dataclasses.dataclass
class A:
    a: int
    b: List[str]
    c: List[List[Dict[str, int]]] = dataclasses.field(default_factory=list)
    d: Union[int, str, None] = None
    e: Optional[int] = None
    tup: Tuple[int, str] = (1, "foo")
    opt: Optional[FrozenSet[str]] = None
    any_: Any = "foo"
    call: Callable[[int], str] = lambda x: "foo"
    lit: Literal["a", 1] = 1
    anystr: AnyStr = "foo"


@runtime_typecheck
@dataclasses.dataclass
class B:
    foo: A


@dataclasses.dataclass
class C:
    x: int
    y: Set[str]


@dataclasses.dataclass
class D:
    c: C
    d: int


def test_check_type_nested():
    with pytest.raises(TypeError):
        check_type(D(C(1, {"foo", 1}), 1))
    with pytest.raises(TypeError):
        check_type(C(1, []))


def test_check_type():
    check_type(C(1, set()))
    with pytest.raises(TypeError):
        check_type(C(1, []))


def test_nest_dataclass():
    foo = A(1, [])
    B(foo)
    with pytest.raises(TypeError):
        B(1)


def test_basic():
    x0 = A(1, ["a"])
    x1 = A(a=1, b=["a"])
    x2 = A(1, b=["a"])
    isinstance(x0, A)
    isinstance(x1, A)
    isinstance(x2, A)
    assert x0 == x1
    assert x0 == x2

    with pytest.raises(TypeError):
        A("a", 2)


def test_generic():
    A(1, ["foo", "bar"])
    with pytest.raises(TypeError):
        A(1, [1, 2])
    with pytest.raises(TypeError):
        A(1, [1, "foo"])


def test_nested_generic():
    A(1, [], [[{"a": 2}]])
    with pytest.raises(TypeError):
        A(1, [], [[{"a": "b"}]])


def test_union():
    A(1, [], d=None)
    A(1, [], d=1)
    with pytest.raises(TypeError):
        A(1, [], d=1.2)


def test_tuple():
    with pytest.raises(TypeError):
        A(1, [], tup=(1, 1))


def test_optional():
    with pytest.raises(TypeError):
        A(1, [], opt=frozenset([1]))


def test_callable():
    with pytest.raises(TypeError):
        A(1, [], call=1)


def test_literal():
    with pytest.raises(TypeError):
        A(1, [], lit=12)


def test_anystr():
    A(1, [], anystr=b"foo")
    with pytest.raises(TypeError):
        A(1, [], anystr=1)
