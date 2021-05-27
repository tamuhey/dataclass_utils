import dataclasses
import sys
from typing import Any, List, Optional, Tuple, Union

import pytest

from dataclass_utils import check_type, into
from dataclass_utils.error import Error

if sys.version_info < (3, 8, 0):
    from typing_extensions import Literal
else:
    from typing import Literal


def test0():
    into(1, int)
    into({"d": 1}, dict)
    into(1, Literal[1])


def test_literal():
    into("a", Literal["a"])
    into(1, Literal[1, 2])
    into("b", Literal["a", "b", "c"])
    with pytest.raises(TypeError):
        into(1, Literal["a"])
    with pytest.raises(TypeError):
        into("c", Literal["a"])

    ty = Tuple[Literal["a", "b"], int]
    into(("a", 10), ty)
    with pytest.raises(TypeError):
        into((1, 2), ty)
    with pytest.raises(TypeError):
        into(("c", 10), ty)

    ty = Optional[Tuple[Literal["a", "b"], int]]
    into(None, ty)
    with pytest.raises(TypeError):
        into((1, 2), ty)


def test_str():
    with pytest.raises(TypeError):
        into("foo", List[str])


def test_any():
    assert into(1, Any) == 1


@dataclasses.dataclass
class A0:
    a: int = 0


def test_invalid_dict():
    d = {"a": 1, 1: 2}
    with pytest.raises(TypeError):
        into(d, A0)


def test1():
    d = {"a": 1}
    a = into(d, A)
    check_type(a)


@dataclasses.dataclass
class A:
    a: int = 0
    b: List[str] = dataclasses.field(default_factory=list)


def test_verb_key():
    with pytest.raises(TypeError):
        into({"c": 1}, A)


def test_basic():
    d = {"a": 1, "b": ["foo", "bar"]}
    a = into(d, A)
    check_type(a)


@dataclasses.dataclass
class B:
    a: int
    b: A


def test_nest():
    d = {"a": 1, "b": {"a": 1, "b": ["foo"]}}
    b = into(d, B)
    check_type(b)


@dataclasses.dataclass
class C:
    a: Union[A, bool]


def test_nest_union():
    d = {"a": True}
    c = into(d, C)
    check_type(c)

    d = {"a": {"a": 0, "b": ["foo"]}}
    c = into(d, C)
    check_type(c)


@dataclasses.dataclass
class D:
    a: Tuple[A, B]


def test_nest_tuple():
    with pytest.raises(TypeError):
        into({"a": (A(), B(1, A()))}, D)
    v = into({"a": ({}, {"a": 1, "b": {}})}, D)
    check_type(v)
