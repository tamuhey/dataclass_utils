from typing import Any, Tuple, Type

Error = Tuple[Any, Type]


def type_error(err: Error):
    value, expected = err
    return TypeError(f"Expected type {expected}, got {type(value)} (value: {value})")
