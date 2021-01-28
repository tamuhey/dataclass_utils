from dataclass_utils.error import type_error
from typing import Callable, Dict, Set
import pytest
from dataclass_utils.type_checker import check_dataclass, is_error, check
from dataclasses import dataclass, field


def test_set():
    assert is_error(check({"foo", "bar", 1}, Set[str]))


def test_callable():
    assert is_error(check(1, Callable))


@dataclass
class B:
    a: int = 0
    b: Dict[str, int] = field(default_factory=dict)


@dataclass
class A:
    a: int = 0
    b: str = ""
    c: B = field(default_factory=B)


def test_error():
    a = A("foo")
    err = check_dataclass(a, A)
    assert is_error(err)
    assert "a" in err.path


def test_error_dataclass():
    a = A(c=B(a="foo"))
    err = check_dataclass(a, A)
    assert is_error(err)
    assert "c" in err.path


def test_error_dict_value():
    a = A(c=B(b={"foo": "bar"}))
    err = check_dataclass(a, A)
    assert is_error(err)
    assert "c" in err.path
    assert "b" in err.path
    assert "foo" in err.path


def test_error_dict_key():
    a = A(c=B(b={1: 1}))
    err = check_dataclass(a, A)
    assert is_error(err)
    assert "c" in err.path
    assert "b" in err.path
    assert 1 not in err.path
