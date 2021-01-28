from typing import Any, List, Optional, Tuple, Type
from dataclasses import dataclass, field


@dataclass
class Error:
    ty: Type[Any]
    value: Any
    path: List[str] = field(default_factory=list)


def type_error(err: Error):
    path = " -> ".join(reversed(err.path))
    return TypeError(
        f"Error in field '{path}'. Expected type {err.ty}, got {type(err.value)} (value: {err.value})"
    )
