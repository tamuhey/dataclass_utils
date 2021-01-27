from typing import Callable, Set
import pytest
from dataclass_utils.type_checker import is_error, check


def test_set():
    assert is_error(check({"foo", "bar", 1}, Set[str]))


def test_callable():
    assert is_error(check(1, Callable))
