from typing import Optional
from .utils import check
import dataclasses


@dataclasses.dataclass
@check
class A:
    b: list[str] = dataclasses.field(default_factory=list)
    c: list[list[dict[str, int]]] = dataclasses.field(default_factory=list)
    opt: Optional[frozenset[str]] = None


def test_list():
    A(b=["a"])
