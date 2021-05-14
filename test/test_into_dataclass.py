import dataclasses
import sys
from typing import List, Optional, Tuple, Union

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
