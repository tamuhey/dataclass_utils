import dataclasses
from typing import (
    Any,
    AnyStr,
    Dict,
    FrozenSet,
    Generic,
    List,
    Literal,
    Optional,
    Set,
    Tuple,
    Type,
    TypeVar,
    Union,
)

from dataclass_utils.error import Error, type_error

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

    # Decorated dataclass
    if isinstance(ty, runtime_typecheck_inner):
        if not isinstance(value, ty.ty):  # type: ignore
            return value, ty

    if ty is AnyStr:
        err = check_anystr(value, ty)
        if is_error(err):
            return err

    if hasattr(ty, "__origin__"):  # generics
        to = ty.__origin__
        err = check(value, to)
        if is_error(err):
            return err

        if to is list or to is set or to is frozenset:
            err = check_mono_container(value, ty)
        elif to is dict:
            err = check_dict(value, ty)
        elif to is tuple:
            err = check_tuple(value, ty)
        elif to is Literal:
            err = check_literal(value, ty)
        elif to is Union:
            err = check_union(value, ty)

        if is_error(err):
            return err

    if dataclasses.is_dataclass(value):
        err = check_dataclass(value, ty)
        if is_error(err):
            return err
    return None


def check_anystr(value: Any, ty: Type) -> Result:
    if all(not isinstance(value, t) for t in ty.__constraints__):
        return (value, ty)
    return None


def check_literal(value: Any, ty: Type) -> Result:
    if all(value != t for t in ty.__args__):
        return (value, ty)
    return None


def check_tuple(value: Any, ty: Type[Tuple]) -> Result:
    types = ty.__args__  # type: ignore
    if len(value) != len(types):
        return (value, ty)
    for v, t in zip(value, types):
        err = check(v, t)
        if is_error(err):
            return err
    return None


def check_union(value: Any, ty) -> Result:
    if any(not is_error(check(value, t)) for t in ty.__args__):
        return None
    return (value, ty)


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


def check_dataclass(value: Any, ty: Type) -> Result:
    for k, ty in value.__annotations__.items():
        v = getattr(value, k)
        err = check(v, ty)
        if err is not None:
            return err
    return None


def is_typevar(ty: Type) -> bool:
    return isinstance(ty, TypeVar)


def is_error(ret: Result) -> bool:
    return ret is not None


def check_root(value: Any):
    err = check_dataclass(value, type(value))
    if err is not None:
        raise type_error(err)


T = TypeVar("T")

# This is here because of dependency
class runtime_typecheck_inner(Generic[T]):
    def __init__(self, ty: Type):
        assert dataclasses.is_dataclass(ty)
        self.ty = ty

    def __call__(self, *args, **kwargs) -> T:
        ret = self.ty(*args, **kwargs)  # type: ignore
        check_root(ret)
        return ret

    def __instancecheck__(self, instance: Any) -> bool:
        return self.ty.__instancecheck__(instance)

    def __subclasscheck__(self, subclass: type) -> bool:
        return self.ty.__subclasscheck__(subclass)
