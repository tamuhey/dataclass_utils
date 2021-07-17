from dataclass_utils.error import Error
from typing import TypeVar
from dataclass_utils import check_type
from contextlib import contextmanager
import pytest


T = TypeVar("T")


def check(kls: T) -> T:
    f = lambda self: check_type(self)
    setattr(kls, "__post_init__", f)
    return kls


@contextmanager
def check_error():
    with pytest.raises(Error) as e:
        yield
    assert e.type is not Error
