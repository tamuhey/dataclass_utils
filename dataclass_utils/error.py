from typing import Any, List, Optional, Type


class Error(TypeError):
    def __init__(self, ty: Type[Any], value: Any, path: List[str] = []):
        if type(self) == Error:
            raise ValueError(
                "Internal Error: `Error` must not be instantiated directly"
            )
        self.ty = ty
        self.value = value
        self.path = path

    def __str__(self) -> str:
        raise NotImplementedError()


def _path_to_str(path: List[str]) -> str:
    return " -> ".join(reversed(path))


class Error0(Error):
    def __init__(
        self,
        ty: Type[Any],
        value: Any,
        path: List[str] = [],
        exception: Optional[Any] = None,
    ):
        self.ty = ty
        self.value = value
        self.path = path
        self.exception = exception

    def __str__(self):
        path = _path_to_str(self.path)
        msg = f"Error in field '{path}'. Expected type {self.ty}, got {type(self.value)} (value: {self.value})"
        if self.exception is not None:
            msg += f"\n{type(self.exception)}: {self.exception}"
        return msg


class MissingKeyError(Error):
    def __init__(self, ty: Type[Any], value: Any, key: Any, path: List[str] = []):
        self.ty = ty
        self.key = key
        self.value = value
        self.path = path

    def __str__(self):
        path = _path_to_str(self.path)
        return f"Key Error in '{path}': Got '{self.key}' in '{self.value}' but doesn't exist in '{self.ty}'"


class UnsupportedTypeError(Error):
    def __init__(self, ty: Type[Any], value: Any, path: List[str] = []):
        self.ty = ty
        self.value = value
        self.path = path

    def __str__(self) -> str:
        path = _path_to_str(self.path)
        return f"UnsupportedType in '{path}': {self.ty}"
