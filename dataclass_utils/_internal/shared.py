import types
from typing import Any, Type
import sys


def is_pep604_union(ty: Type[Any]) -> bool:
    return sys.version_info >= (3, 10) and ty is types.UnionType  # types: ignore
