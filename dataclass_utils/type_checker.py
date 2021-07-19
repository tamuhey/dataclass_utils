import dataclasses
import typing
from typing import (
    Any,
    Dict,
    FrozenSet,
    List,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

import typing_extensions
from typing_extensions import TypedDict, TypeGuard

from dataclass_utils.error import Error, Error0
from dataclass_utils.typing import Literal, get_args, get_origin

Result = Optional[Error]  # returns error context


def check(value: Any, ty: Type[Any]) -> Result:
    """

    # Examples

    >>> assert is_error(check(1, str))
    >>> assert not is_error(check(1, int))
    >>> assert is_error(check(1, list))
    >>> assert is_error(check(1.3, int))
    >>> assert is_error(check(1.3, Union[str, int]))
    """
    if not isinstance(value, type) and dataclasses.is_dataclass(ty):
        # dataclass
        return check_dataclass(value, ty)
    elif is_typeddict(ty):
        # should use `typing.is_typeddict` in future
        return check_typeddict(value, ty)
    else:
        to = get_origin(ty)
        if to is not None:
            # generics
            err = check(value, to)
            if is_error(err):
                return err

            if to is list or to is set or to is frozenset:
                err = check_mono_container(value, ty)
            elif to is dict:
                err = check_dict(value, ty)  # type: ignore
            elif to is tuple:
                err = check_tuple(value, ty)
            elif to is Literal:
                err = check_literal(value, ty)
            elif to is Union:
                err = check_union(value, ty)
            return err
        elif isinstance(ty, type):
            # concrete type
            if issubclass(ty, bool):
                if not isinstance(value, ty):
                    return Error0(ty=ty, value=value)
            elif issubclass(ty, int):  # For boolean
                return check_int(value, ty)
            elif not isinstance(value, ty):
                return Error0(ty=ty, value=value)

    return None


def check_int(value: Any, ty: Type[Any]) -> Result:
    if isinstance(value, bool) or not isinstance(value, ty):
        return Error0(ty=ty, value=value)
    return None


def check_literal(value: Any, ty: Type[Any]) -> Result:
    if all(value != t for t in get_args(ty)):
        return Error0(ty=ty, value=value)
    return None


def check_tuple(value: Any, ty: Type[Tuple[Any, ...]]) -> Result:
    types = get_args(ty)
    if len(value) != len(types):
        return Error0(ty=ty, value=value)
    for v, t in zip(value, types):
        err = check(v, t)
        if is_error(err):
            return err
    return None


def check_union(value: Any, ty: Type[Any]) -> Result:
    if any(not is_error(check(value, t)) for t in get_args(ty)):
        return None
    return Error0(ty=ty, value=value)


def check_mono_container(
    value: Any, ty: Union[Type[List[Any]], Type[Set[Any]], Type[FrozenSet[Any]]]
) -> Result:
    ty_item = get_args(ty)[0]
    for v in value:
        err = check(v, ty_item)
        if is_error(err):
            return err
    return None


def check_dict(value: Dict[Any, Any], ty: Type[Dict[Any, Any]]) -> Result:
    args = get_args(ty)
    ty_key = args[0]
    ty_item = args[1]
    for k, v in value.items():
        err = check(k, ty_key)
        if is_error(err):
            return err
        err = check(v, ty_item)
        if err is not None:
            err.path.append(k)
            return err
    return None


def check_dataclass(value: Any, ty: Type[Any]) -> Result:
    if not dataclasses.is_dataclass(value):
        return Error0(ty, value)
    for k, ty in typing.get_type_hints(ty).items():
        v = getattr(value, k)
        err = check(v, ty)
        if err is not None:
            err.path.append(k)
            return err
    return None


def check_typeddict(value: Any, ty: Type[Type[Any]]) -> Result:
    if not isinstance(value, dict):
        return Error0(ty, value)
    is_total: bool = ty.__total__  # type: ignore
    for k, ty in typing.get_type_hints(ty).items():
        if k not in value:
            if is_total:
                return Error0(ty, value, [k])
            else:
                continue
        v = value[k]
        err = check(v, ty)
        if err is not None:
            err.path.append(k)
            return err
    return None


def is_typevar(ty: Type[Any]) -> TypeGuard[TypeVar]:
    return isinstance(ty, TypeVar)


def is_error(ret: Result) -> TypeGuard[Error]:
    return ret is not None


def is_typeddict(ty: Type[Any]) -> TypeGuard[Type[TypedDict]]:  # type: ignore
    # TODO: Should use `typing.is_typeddict` in future
    #       or, use publich API
    T = "_TypedDictMeta"
    for mod in [typing, typing_extensions]:
        if hasattr(mod, T) and isinstance(ty, getattr(mod, T)):
            return True
    return False


def check_root(value: Any):
    """Check dataclass type recursively"""
    err = check_dataclass(value, type(value))
    if err is not None:
        raise err
