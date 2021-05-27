"""Convert dict into dataclass"""

import dataclasses
from typing import Any, Dict, Iterable, List, Sized, Type, TypeVar, Union, cast

from dataclass_utils.error import Error, MissingKeyError
from dataclass_utils.typing import Literal, get_args, get_origin


T = TypeVar("T")
V = Union[Dict[Any, Any], List[Any], int, float, str, bool, Any]

Result = Union[T, Error]


def is_error(v: Result[Any]) -> bool:
    return isinstance(v, Error)


def into_root(value: V, kls: Type[T]) -> T:
    ret = into(value, kls)
    if isinstance(ret, Error):
        raise ret
    return ret


def into(value: V, kls: Type[T]) -> Result[T]:
    if dataclasses.is_dataclass(kls):
        # dataclass
        return _into_dataclass(value, kls)
    else:
        to = get_origin(kls)
        if to is not None:
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
                ret = _into_literal(value, kls)
            elif isinstance(value, to):
                ret = cast(T, value)
            else:
                ret = Error(kls, value)
            return ret
        else:
            try:
                if isinstance(value, kls):
                    return value
            except TypeError:
                if kls is Any:
                    return value  # type: ignore
        return Error(kls, value)


def _into_literal(value: V, kls: Type[T]) -> Result[T]:
    literals = get_args(kls)
    if value not in literals:
        return Error(kls, value)
    return value  # type: ignore


def _is_sized_iterable(v: Any) -> bool:
    return isinstance(v, Iterable) and isinstance(v, Sized)  # type: ignore
    # bug: https://github.com/microsoft/pyright/issues/1856


def _into_tuple(value: V, kls: Type[T]) -> Result[T]:
    if not _is_sized_iterable(value):
        return Error(kls, value)

    types = get_args(kls)
    val0: Sized = value  # type: ignore
    if len(types) != len(val0):
        return Error(ty=kls, value=val0)

    val1: Iterable[T] = value  # type: ignore
    ret: List[T] = []
    for v, t in zip(val1, types):
        vr = into(v, t)  # type: ignore
        if isinstance(vr, Error):
            return vr
        ret.append(vr)
    ty_orig = get_origin(kls)
    assert ty_orig is not None
    return ty_orig(ret)


def _into_dict(value: V, kls: Type[T]) -> Result[T]:
    if not isinstance(value, dict):
        return Error(kls, value)
    args = get_args(kls)
    ty_key = args[0]
    ty_item = args[1]
    orig = get_origin(kls)
    assert orig is not None
    ret = orig()
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
    if isinstance(value, str):
        return Error(kls, value)
    if not _is_sized_iterable(value):
        return Error(kls, value)
    ty_item = get_args(kls)[0]
    ty_orig = get_origin(kls)
    assert ty_orig
    ret: List[T] = []
    for v in cast(Iterable[T], value):
        w = into(v, ty_item)  # type: ignore
        if isinstance(w, Error):
            return w
        ret.append(w)
    return ty_orig(ret)


def _into_union(value: V, kls: Type[T]) -> Result[T]:
    types = get_args(kls)
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
    >>> bar = _into_dataclass(data, Bar)
    >>> assert bar.foo == Foo(**data["foo"]) # field `foo` is instantiated as `Foo`, not dict
    """
    if not isinstance(value, dict):
        return Error(value=value, ty=dict)

    # convert values into dastaclass recursively
    d: Dict[str, Any] = dict()
    fields: Dict[str, Type[Any]] = kls.__annotations__
    for k, v in value.items():
        if not isinstance(k, str):
            return Error(str, k)
        if k not in fields:
            return MissingKeyError(kls, value, k)
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
