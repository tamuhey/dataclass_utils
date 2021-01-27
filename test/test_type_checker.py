from typing import Set
import pytest
import dataclass_utils.type_checker as type_checker


def test_set():
    assert type_checker.is_error(type_checker.check({"foo", "bar", 1}, Set[str]))
