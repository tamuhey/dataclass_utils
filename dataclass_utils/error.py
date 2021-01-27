from typing import Any, Type


def type_error(expected: Type, value: Any):
    return TypeError(f"Expected type {expected}, got {type(value)} (value: {value})")
