"""Convert dict into dataclass"""

import dataclasses
from typing import Any, Dict, Type, TypeVar
from .error import Error

from dataclass_utils.error import type_error

T = TypeVar("T")


def into_dataclass(kls: Type[T], value: Dict[str, Any]) -> T:
    """Recursively constructs dataclass from dict

    # Example

    >>> @dataclasses.dataclass
    ... class Foo:
    ...     a: int
    >>> @dataclasses.dataclass
    ... class Bar:
    ...     foo: Foo
    ...     b: str
    >>> data = {"foo": {"a": 1}, "b": "foo"}
    >>> bar = into_dataclass(Bar, data)
    >>> assert bar.foo == Foo(**data["foo"]) # field `foo` is instantiated as `Foo`, not dict
    """
    if not isinstance(value, dict):
        raise type_error(Error(value=value, ty=dict))
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
