# Runtime typechecker for dataclass

`$ pip install dataclass_utils`

## Example

### `check_type` function

Check dataclass type recursively

```python
from dataclass_utils import check_type
import dataclasses
from typing import List

@dataclasses.dataclass
class Foo:
    a: int
    b: List[str]

import pytest

check_type(Foo(1, ["b"])) # OK

with pytest.raises(TypeError):
    check_type(Foo("a", [2]))
```

### `into_dataclass` function

Recursively constructs dataclass from dict

```python
@dataclasses.dataclass
class Foo:
    a: int

@dataclasses.dataclass
class Bar:
    foo: Foo
    b: str

data = {"foo": {"a": 1}, "b": "foo"}
bar = into_dataclass(Bar, data)
assert bar.foo == Foo(**data["foo"]) # field `foo` is instantiated as `Foo`, not dict
```
