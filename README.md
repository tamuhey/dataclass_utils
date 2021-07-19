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
    b: List[List[int]]

import pytest

check_type(Foo(1, ["b"])) # OK

with pytest.raises(TypeError):
    check_type(Foo(1, [[2, "foo"]])) # NG
```

See [examples](./examples) directory for more examples.

## Features

- Recursively check type for each fields in dataclass
    - `check_type` can be applied for nested dataclass, nested containers
- No dependencies

## Development

- `make publish` to test and publish
