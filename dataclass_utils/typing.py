import sys

if sys.version_info >= (3, 8, 0):
    from typing import Literal, get_origin, get_args, OrderedDict  # type: ignore
else:
    from typing_extensions import Literal, get_origin, get_args, OrderedDict  # type: ignore
