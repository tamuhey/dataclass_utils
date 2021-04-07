"""Convert dict into dataclass"""

import dataclasses
from typing import Any, Dict, Iterable, List, Literal, Sized, Type, TypeVar, Union, cast
import typing

from dataclass_utils.error import Error, type_error


T = TypeVar("T")
V = Union[Dict, List, int, float, str, bool]

Result = Union[T, Error]


def is_error(v: Result[Any]) -> bool:
    return isinstance(v, Error)


def into_root(value: V, kls: Type[T]) -> T:
    ret = into(value, kls)
    if isinstance(ret, Error):
        raise type_error(ret)
    return ret


def into(value: V, kls: Type[T]) -> Result[T]:
    if dataclasses.is_dataclass(kls):
        # dataclass
        return _into_dataclass(value, kls)
    elif (to := typing.get_origin(kls)) is not None:
        # generics
        if to is list or to is set or to is frozenset:
            ret = _into_mono_container(value, kls)
        elif to is dict:
            ret = _into_dict(value, kls)
        elif to is tuple:
            ret = _into_tuple(value, kls)
        elif to is Union:
            ret = _into_union(value, kls)
        elif to is Literal:
            ret = value
        else:
            if isinstance(value, to):
                ret = value
            else:
                ret = Error(kls, value)
        return ret  # type: ignore
    else:
        if isinstance(value, kls):
            return value
        return Error(kls, value)


def _is_sized_iterable(v: Any) -> bool:
    return isinstance(v, Iterable) and isinstance(v, Sized)


def _into_tuple(value: V, kls: Type[T]) -> Result[T]:
    if not _is_sized_iterable(value):
        return Error(kls, value)

    types = typing.get_args(kls)
    val0: Sized = value  # type: ignore (bug: https://github.com/microsoft/pyright/issues/1741)
    if len(types) != len(val0):
        return Error(ty=kls, value=val0)

    val1: Iterable = value  # type: ignore (bug: https://github.com/microsoft/pyright/issues/1741)
    ret = []
    for v, t in zip(val1, types):
        vr = into(v, t)  # type: ignore
        if is_error(vr):
            return vr
        ret.append(vr)
    ty_orig = typing.get_origin(kls)
    return ty_orig(ret)


def _into_dict(value: V, kls: Type[T]) -> Result[T]:
    if not isinstance(value, dict):
        return Error(kls, value)
    args = typing.get_args(kls)
    ty_key = args[0]
    ty_item = args[1]
    ret = typing.get_origin(kls)()
    for k, v in value.items():
        kr = into(k, ty_key)
        if is_error(kr):
            return kr
        vr = into(v, ty_item)
        if is_error(vr):
            vr.path.append(k)
            return vr
        ret[kr] = vr
    return ret


def _into_mono_container(value: V, kls: Type[T]) -> Result[T]:
    if not _is_sized_iterable(value):
        return Error(kls, value)
    ty_item = typing.get_args(kls)[0]
    ty_orig = typing.get_origin(kls)
    assert ty_orig
    ret = []
    for v in value:  # type: ignore
        w = into(v, ty_item)
        if is_error(w):
            return w
        ret.append(w)
    return ty_orig(ret)


def _into_union(value: V, kls: Type[T]) -> Result[T]:
    types = typing.get_args(kls)
    err = Error(ty=kls, value=value)
    for ty in types:
        ret = into(value, ty)
        if not is_error(ret):
            return ret
    return err


def _into_dataclass(value: V, kls: Type[T]) -> Result[T]:
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
    >>> bar = into_dataclass(data, Bar)
    >>> assert bar.foo == Foo(**data["foo"]) # field `foo` is instantiated as `Foo`, not dict
    """
    if not isinstance(value, dict):
        return Error(value=value, ty=dict)

    # convert values into dastaclass recursively
    d = dict()
    fields: Dict[str, Type] = kls.__annotations__
    for k, v in value.items():
        ty = fields[k]
        v = into(v, ty)
        if is_error(v):
            v.path.append(k)
            return v
        d[k] = v
    try:
        return kls(**d)  # type: ignore
    except:
        return Error(kls, value)
