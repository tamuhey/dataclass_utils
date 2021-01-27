from dataclass_utils.error import type_error
import dataclass_utils.type_checker as type_checker
import dataclasses
from typing import Any, Dict, Generic, List, Protocol, Type, TypeVar


T = TypeVar("T")


class _runtime_typecheck_inner(Generic[T]):
    def __init__(self, ty: Type[T]):
        assert dataclasses.is_dataclass(ty)
        self.ty = ty
        self.fields = dataclasses.fields(self.ty)
        self.fields_dict: Dict[str, dataclasses.Field] = self.ty.__dataclass_fields__  # type: ignore

    def __call__(self, *args, **kwargs) -> T:
        for arg, field in zip(args, self.fields):
            err = type_checker.check(arg, field.type)
            if err is not None:
                raise type_error(err)

        for k, v in kwargs.items():
            err = type_checker.check(v, self.fields_dict[k].type)
            if err is not None:
                raise type_error(err)

        ret = self.ty(*args, **kwargs)  # type: ignore
        return ret

    def __instancecheck__(self, instance: Any) -> bool:
        return self.ty.__instancecheck__(instance)

    def __subclasscheck__(self, subclass: type) -> bool:
        return self.ty.__subclasscheck__(subclass)


def runtime_typecheck(ty: Type[T]) -> Type[T]:
    """

    # Example

    >>> @runtime_typecheck
    ... @dataclasses.dataclass
    ... class Foo:
    ...     a: int
    ...     b: List[str]


    >>> foo = Foo(1, ["a"])  # ok
    >>> assert isinstance(foo, Foo) # Still, it is an instance of `Foo`
    >>> import pytest
    >>> with pytest.raises(TypeError):
    ...     Foo("a", [])
    >>> with pytest.raises(TypeError):
    ...     Foo(1, [1, 2])
    """
    return _runtime_typecheck_inner(ty)  # type: ignore
