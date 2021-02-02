from __future__ import annotations
from typing import Optional
import pytest
from .utils import check
import dataclasses
import sys

if sys.version_info < (3, 9):
    pytestmark = pytest.mark.skip()


@dataclasses.dataclass
@check
class A:
    b: list[str] = dataclasses.field(default_factory=list)
    c: list[list[dict[str, int]]] = dataclasses.field(default_factory=list)
    opt: Optional[frozenset[str]] = None


def test_list():
    A(b=["a"])
