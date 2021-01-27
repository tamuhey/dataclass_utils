from dataclass_utils.error import Error
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

Result = Optional[Error]  # returns error context


def check(value: Any, ty: Type) -> Result:
    """

    # Examples

    >>> assert is_error(check(1, str))
    >>> assert not is_error(check(1, int))
    >>> assert is_error(check(1, list))
    >>> assert is_error(check(1.3, int))
    >>> assert is_error(check(1.3, Union[str, int]))
    """
    if isinstance(ty, type):
        if not isinstance(value, ty):
            return value, ty

    if hasattr(ty, "__origin__"):  # generics
        to = ty.__origin__
        err = check(value, to)
        if is_error(err):
            return err

        if to is list or to is set or to is frozenset:
            err = check_mono_container(value, ty)
        elif to is dict:
            err = check_dict(value, ty)
        elif to is Union:
            err = check_union(value, ty)

        if is_error(err):
            return err


def check_union(value: Any, ty) -> Result:
    if any(not is_error(check(value, t)) for t in ty.__args__):
        return None
    return (ty, value)


def check_mono_container(
    value: Any, ty: Union[Type[List], Type[Set], Type[FrozenSet]]
) -> Result:
    ty_item = next(iter(ty.__args__))  # type: ignore
    for v in value:
        err = check(v, ty_item)
        if is_error(err):
            return err
    return None


def check_dict(value: Dict, ty: Type[Dict]) -> Result:
    args = iter(ty.__args__)  # type: ignore
    ty_key = next(args)
    ty_item = next(args)
    for k, v in value.items():
        err = check(k, ty_key)
        if is_error(err):
            return err
        err = check(v, ty_item)
        if is_error(err):
            return err
    return None


def is_typevar(ty: Type) -> bool:
    return isinstance(ty, TypeVar)


def is_error(ret: Result) -> bool:
    return ret is not None
