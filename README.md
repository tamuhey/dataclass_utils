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

See [examples](./example) directory for more examples.
