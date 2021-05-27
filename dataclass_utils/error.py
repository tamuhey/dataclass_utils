from typing import Any, List, Type
import abc


class Error(TypeError):
    @abc.abstractmethod
    def __init__(self, ty: Type[Any], value: Any, path: List[str] = []):
        self.ty = ty
        self.value = value
        self.path = path


def _path_to_str(path: List[str]) -> str:
    return " -> ".join(reversed(path))


class Error0(Error):
    def __init__(self, ty: Type[Any], value: Any, path: List[str] = []):
        self.ty = ty
        self.value = value
        self.path = path

    def __str__(self):
        path = _path_to_str(self.path)
        return f"Error in field '{path}'. Expected type {self.ty}, got {type(self.value)} (value: {self.value})"


class MissingKeyError(Error):
    def __init__(self, ty: Type[Any], value: Any, key: Any, path: List[str] = []):
        self.ty = ty
        self.key = key
        self.value = value
        self.path = path

    def __str__(self):
        path = _path_to_str(self.path)
        return f"Key Error in '{path}': Got '{self.key}' in 'self.value' but doesn't exist in '{self.ty}'"
