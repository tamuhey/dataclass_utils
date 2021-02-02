from typing import TypeVar
from dataclass_utils import check_type


T = TypeVar("T")


def check(kls: T) -> T:
    f = lambda self: check_type(self)
    setattr(kls, "__post_init__", f)
    return kls
