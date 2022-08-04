from __future__ import annotations
import dataclasses
import sys
import pytest
from dataclass_utils import check_type

if sys.version_info < (3, 10):
    pytestmark = pytest.mark.skip()


@dataclasses.dataclass
class Foo:
    bar: str | int = "foo"


def test_union():
    check_type(Foo())
    with pytest.raises(TypeError):
        check_type(Foo({}))
