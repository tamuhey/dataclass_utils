"""Convert dict into dataclass"""

from typing import Any, Dict, Type, TypeVar
import dataclasses
from dataclass_utils.error import type_error


T = TypeVar("T")


def into_dataclass(kls: Type[T], value: Dict[str, Any]) -> T:
    if not isinstance(value, dict):
        raise type_error((value, dict))
    if not dataclasses.is_dataclass(kls):
        raise TypeError(f"Expected dataclass type, got {kls}")

    # convert values into dastaclass recursively
    d = dict()
    fields: Dict[str, Type] = kls.__annotations__
    for k in value.keys():
        if dataclasses.is_dataclass(fields[k]):
            d[k] = into_dataclass(fields[k], value[k])
        else:
            d[k] = value[k]
    return kls(**d)  # type: ignore
