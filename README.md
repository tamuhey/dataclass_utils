# Runtime typechecker for dataclass

`$ pip install dataclass_utils`

## Example

### `check_type` function

```python
>>> from dataclass_utils import check_type
>>> import dataclasses
>>> from typing import List

>>> @dataclasses.dataclass
... class Foo:
...     a: int
...     b: List[str]

>>> import pytest

>>> check_type(Foo(1, ["b"])) # OK

>>> with pytest.raises(TypeError):
...     check_type(Foo("a", [2]))

```

### `runtime_typecheck` decorator

```python
>>> from dataclass_utils import runtime_typecheck
>>> from typing import List

>>> @runtime_typecheck
... @dataclasses.dataclass
... class Foo:
...     a: int
...     b: List[str]

>>> foo = Foo(1, ["a"])  # ok

>>> import pytest

>>> with pytest.raises(TypeError):
...    Foo("a", [])

>>> with pytest.raises(TypeError):
...    Foo(1, [1, 2])

```
