from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Dict, List, Set

from dataclass_utils.error import Error
from dataclass_utils.type_checker import check, check_dataclass, is_error


def test_set():
    assert is_error(check({"foo", "bar", 1}, Set[str]))


def test_str():
    assert is_error(check("foo", List[str]))


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

    err = check_dataclass("foo", A)
    assert is_error(err)
    assert str(err)
    assert "a" in err.path


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


def test_bool():
    assert is_error(check(1, bool))
    assert not is_error(check(1, int))

    assert not is_error(check(False, bool))
    assert is_error(check(False, int))


class ENUM(Enum):
    a = "a"


def test_enum():
    assert is_error(check("a", ENUM))
    assert not is_error(check(ENUM.a, ENUM))
