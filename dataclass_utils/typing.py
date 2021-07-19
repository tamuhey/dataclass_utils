import sys

from typing_extensions import Literal, OrderedDict, get_args, get_origin  # type: ignore

if sys.version_info >= (3, 10, 0):
    from typing import _TypedDictMeta  # type: ignore
else:
    from typing_extensions import _TypedDictMeta  # type: ignore
