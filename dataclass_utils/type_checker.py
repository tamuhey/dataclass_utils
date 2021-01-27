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

Result = Optional[Tuple[Any, Type]]  # returns error context


def check(value: Any, ty: Type) -> Result:
    if isinstance(ty, type):
        if not isinstance(value, ty):
            return value, ty

    if hasattr(ty, "__origin__"):  # generics
        to = ty.__origin__
        check(value, to)
        if to in {list, set, frozenset}:
            check_mono_container(value, ty)
        elif to is dict:
            check_dict(value, ty)
        elif to is Union:
            check_union(value, ty)


def check_union(value: Any, ty: Type[Union]) -> Result:
    if any(check(value, t) for t in ty.__args__):
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
