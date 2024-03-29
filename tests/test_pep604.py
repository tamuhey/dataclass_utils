import dataclasses
import sys
import pytest
from dataclass_utils import check_type
import dataclass_utils

if sys.version_info < (3, 10):
    pytestmark = pytest.mark.skip()
else:
    @dataclasses.dataclass
    class Foo:
        bar: str | int = "foo"


    def test_union():
        check_type(Foo())
        with pytest.raises(TypeError):
            check_type(Foo({}))


    def test_union2():
        dataclass_utils.into({"bar": "foo"}, Foo)
