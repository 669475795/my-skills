# Google Python Style Guide - Key Standards

## Formatting

### Indentation
- 4 spaces (never tabs)
- Hanging indents: align with opening delimiter or use 4-space indent

### Line Length
- Maximum 80 characters
- Exceptions: long imports, URLs, comments with long URLs

### Blank Lines
- Two blank lines between top-level definitions
- One blank line between method definitions
- Use blank lines sparingly within functions

### Whitespace
- No trailing whitespace
- Two spaces before inline comment
- One space after comma, colon, semicolon

### Shebang
- `#!/usr/bin/env python3` for executable files

## Naming Conventions

### Modules
- lowercase_with_underscores
- Short, avoid dashes

### Packages
- lowercase without underscores
- Short names preferred

### Classes
- CapWords (PascalCase)
- Exception classes end with "Error"

### Functions & Methods
- lowercase_with_underscores
- Use descriptive names

### Constants
- CAPS_WITH_UNDERSCORES
- Module level only

### Variables
- lowercase_with_underscores
- Single letter okay for iterators: `i`, `j`, `k`

### Private
- Single leading underscore for internal use
- Double leading underscore for name mangling (rare)

## Imports

### Order
1. Standard library imports
2. Related third party imports
3. Local application imports
- Blank line between each group
- Alphabetical within groups

### Format
```python
import os
import sys
from typing import Dict, List

import numpy as np
import tensorflow as tf

from myapp import utils
```

### Rules
- One import per line for regular imports
- Multiple imports okay for `from x import y, z`
- No relative imports (use absolute)
- Import modules, not individual names (exceptions for typing)

## Comments & Docstrings

### Docstrings
- Use `"""triple double quotes"""`
- Required for public modules, functions, classes, methods

### Module Docstring
```python
"""One line summary.

More detailed description if needed.
"""
```

### Function Docstring
```python
def function(arg1: int, arg2: str) -> bool:
    """Summary line.

    Args:
        arg1: Description of arg1
        arg2: Description of arg2

    Returns:
        Description of return value

    Raises:
        ValueError: Description of when raised
    """
```

### Class Docstring
```python
class MyClass:
    """Summary of class.

    Attributes:
        attr1: Description of attr1
        attr2: Description of attr2
    """
```

### Inline Comments
- Use sparingly, explain "why" not "what"
- Complete sentences, proper capitalization

## Programming Practices

### Type Hints
- Use for all public APIs
- Prefer type hints over comments
```python
def func(x: int) -> str:
    return str(x)
```

### Default Argument Values
- Do not use mutable objects as defaults
```python
# Wrong
def func(a, b=[]):
    ...

# Right
def func(a, b=None):
    if b is None:
        b = []
```

### Properties
- Use for accessing or setting data where normally use simple attributes
```python
@property
def width(self):
    return self._width

@width.setter
def width(self, value):
    self._width = value
```

### True/False Evaluations
- Use implicit false when possible
```python
# Yes
if not users:
if foo:

# No
if len(users) == 0:
if foo != []:
```

### Context Managers
- Use `with` for resources
```python
with open('file.txt') as f:
    data = f.read()
```

### Generators
- Use for large datasets
- More memory efficient than lists

### Comprehensions
- Okay for simple cases
- Avoid multiple for-clauses or filters

### Lambda Functions
- Okay for one-liners
- Use `def` for anything complex

### String Methods
- Use string methods instead of string module
- Use f-strings for formatting (Python 3.6+)
```python
name = "world"
greeting = f"Hello, {name}!"
```

## Exception Handling

### Raise Specific Exceptions
```python
# Yes
raise ValueError('message')

# No
raise Exception('message')
```

### Minimize Try/Except Blocks
- Keep try clause as small as possible

### Re-raise Exceptions
```python
try:
    ...
except SomeException as e:
    logger.error(f"Error: {e}")
    raise
```

## Design Patterns

### Use Built-in Types
- Prefer list, dict, set over custom collections

### Main Function
```python
def main():
    ...

if __name__ == '__main__':
    main()
```

### Abstract Base Classes
- Use ABC for interfaces
```python
from abc import ABC, abstractmethod

class Base(ABC):
    @abstractmethod
    def method(self):
        pass
```

## Performance

### List Comprehensions
- Faster than for loops for simple operations

### String Concatenation
- Use `''.join(list)` for many strings
- f-strings for few strings

### Local Variables
- Faster than globals
- Cache method lookups in loops

### avoid
- `global` keyword
- `eval()` and `exec()`
- Wildcard imports (`from x import *`)
