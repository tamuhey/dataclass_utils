from typing import Dict, List
import pytest
from dataclasses import dataclass
from dataclass_utils import check_type
import sys

if sys.version_info >= (3, 9):

    @dataclass
    class Foo:
        a: int
        b: List[Dict[str, int]]  # supports nested container type

    @dataclass
    class Bar:
        foo: List[Foo]  # supports nested dataclass

    with pytest.raises(TypeError):
        check_type(Foo(a="a", b=[]))  # `a` has invalid type

    with pytest.raises(TypeError):
        check_type(Foo(a=1, b=[{"a": "b"}]))  # `b` has invalid type

    foo = Foo(1, [])
    check_type(foo)  # Ok
    check_type(Bar(foo=[foo]))  # Ok

    invalid_foo = Foo(1, [{1: {}}])
    with pytest.raises(TypeError):
        check_type(Bar(foo=[foo, invalid_foo]))  # foo has invalid type
