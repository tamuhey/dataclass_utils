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
            assert isinstance(arg, _get_field_type(field))
        for k, v in kwargs.items():
            assert isinstance(v, _get_field_type(self.fields_dict[k]))
        ret = self.ty(*args, **kwargs)  # type: ignore
        return ret


def _get_field_type(field: dataclasses.Field) -> Type:
    ty = field.type
    if hasattr(ty, "__origin__"):
        # generics
        return ty.__origin__
    return ty


def runtime_typecheck(ty: Type[T]) -> Type[T]:
    """

    # Example

    >>> @runtime_typecheck
    ... @dataclasses.dataclass
    ... class Foo:
    ...     a: int
    ...     b: List[str]


    >>> foo = Foo(1, ["a"]) # ok
    >>> import pytest
    >>> with pytest.raises(AssertionError):
    ...     bar = Foo("a", [])
    """
    return _runtime_typecheck_inner(ty)  # type: ignore
