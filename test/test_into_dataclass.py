from dataclass_utils.into_dataclass import into_dataclass
import dataclasses
from typing import List


@dataclasses.dataclass
class A:
    a: int = 0
    b: List[str] = dataclasses.field(default_factory=list)


@dataclasses.dataclass
class B:
    a: int
    b: A


def test_basic():
    d = {"a": 1, "b": ["foo", "bar"]}
    assert A(**d) == into_dataclass(A, d)


def test_nest():
    d = {"a": 1, "b": {"a": 1, "b": ["foo"]}}
    b = into_dataclass(B, d)
    assert b.b == A(**d["b"])
