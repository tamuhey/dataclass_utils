from typing import Any, Dict, List, Type, TypeVar


def check(value: Any, ty: Type):
    if hasattr(ty, "__origin__"):
        # generics
        assert isinstance(value, ty.__origin__)
        # no typevar
        if all(isinstance(t, TypeVar) for t in ty.__args__):
            return
        if ty.__origin__ is list or ty.__origin__ is set or ty is frozenset:
            assert len(ty.__args__) == 1
            check_mono_container(value, ty.__args__[0])
        elif ty.__origin__ is dict:
            assert len(ty.__args__) == 2
            check_dict(value, *ty.__args__)
    else:
        assert isinstance(value, ty)


def check_mono_container(value: List, ty_item: Type):
    for v in value:
        check(v, ty_item)


def check_dict(value: Dict, ty_key: Type, ty_value: Type):
    for k, v in value.items():
        check(k, ty_key)
        check(v, ty_value)
