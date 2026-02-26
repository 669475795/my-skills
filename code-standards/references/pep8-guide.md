# PEP 8 - Python Style Guide

## Code Layout

### Indentation
- Use 4 spaces per indentation level
- Never mix tabs and spaces
- Python 3 disallows mixing tabs and spaces

### Line Length
- Limit all lines to 79 characters
- For docstrings or comments, limit to 72 characters
- Long lines can be broken using Python's implied line continuation inside parentheses, brackets, and braces

### Line Breaks
```python
# Aligned with opening delimiter
foo = long_function_name(var_one, var_two,
                         var_three, var_four)

# Hanging indent
foo = long_function_name(
    var_one, var_two,
    var_three, var_four)
```

### Blank Lines
- Surround top-level function and class definitions with two blank lines
- Method definitions inside a class are surrounded by a single blank line
- Use blank lines in functions sparingly to indicate logical sections

### Imports
- Imports should usually be on separate lines
```python
# Yes
import os
import sys

# No
import os, sys
```

- Imports are always at the top of the file
- Import order:
  1. Standard library imports
  2. Related third party imports
  3. Local application/library specific imports
- Blank line between each group

### Module Level Dunder Names
- Module level "dunders" (i.e. names with two leading and two trailing underscores) such as `__all__`, `__author__`, `__version__`, etc. should be placed after the module docstring but before any import statements

## Whitespace

### Avoid Extraneous Whitespace
```python
# Yes
spam(ham[1], {eggs: 2})

# No
spam( ham[ 1 ], { eggs: 2 } )
```

### Trailing Whitespace
- Avoid trailing whitespace anywhere

### Binary Operators
```python
# Yes
i = i + 1
submitted += 1
x = x*2 - 1
hypot2 = x*x + y*y
c = (a+b) * (a-b)

# No
i=i+1
submitted +=1
x = x * 2 - 1
hypot2 = x * x + y * y
c = (a + b) * (a - b)
```

### Keyword Arguments
```python
# Yes
def complex(real, imag=0.0):
    return magic(r=real, i=imag)

# No
def complex(real, imag = 0.0):
    return magic(r = real, i = imag)
```

## Comments

### Block Comments
- Block comments generally apply to some (or all) code that follows them
- Each line of a block comment starts with a # and a single space
- Paragraphs inside a block comment are separated by a line containing a single #

### Inline Comments
- Use inline comments sparingly
- Inline comments should be separated by at least two spaces from the statement
- Start with a # and a single space
```python
x = x + 1  # Compensate for border
```

### Documentation Strings
- Write docstrings for all public modules, functions, classes, and methods
- Docstrings that fit on one line:
```python
"""Return a foobang."""
```

- Multi-line docstrings:
```python
"""Summary line.

Extended description of function.

Args:
    arg1: Description
    arg2: Description

Returns:
    Description of return value
"""
```

## Naming Conventions

### Overriding Principle
- Names visible to the user as public parts of the API should follow conventions that reflect usage rather than implementation

### Prescriptive Naming Conventions

#### Package and Module Names
- Modules should have short, all-lowercase names
- Underscores can be used if it improves readability
- Packages should also have short, all-lowercase names, preferably without underscores

#### Class Names
- Class names should use CapWords convention
```python
class MyClass:
    pass
```

#### Type Variable Names
- Use CapWords preferring short names: T, AnyStr, Num

#### Exception Names
- Use class naming convention
- Suffix exception names with "Error" if the exception is an error
```python
class ValidationError(Exception):
    pass
```

#### Function and Variable Names
- Function names should be lowercase, with words separated by underscores
- Variable names follow the same convention as function names
```python
def my_function():
    my_variable = 1
```

#### Function and Method Arguments
- Always use `self` for the first argument to instance methods
- Always use `cls` for the first argument to class methods

#### Method Names and Instance Variables
- Use the function naming rules: lowercase with words separated by underscores
- Use one leading underscore only for non-public methods and instance variables

#### Constants
- Constants are usually defined on a module level
- Written in all capital letters with underscores separating words
```python
MAX_OVERFLOW = 100
TOTAL_COUNT = 0
```

### Names to Avoid
- Never use the characters 'l' (lowercase letter el), 'O' (uppercase letter oh), or 'I' (uppercase letter eye) as single character variable names
- In some fonts, these characters are indistinguishable from the numerals one and zero

## Programming Recommendations

### Comparisons
- Comparisons to singletons like None should always be done with `is` or `is not`, never the equality operators
```python
# Yes
if foo is None:

# No
if foo == None:
```

### Boolean Comparisons
- Don't compare boolean values to True or False using ==
```python
# Yes
if greeting:

# No
if greeting == True:

# Worse
if greeting is True:
```

### Context Managers
- Use `with` statement to simplify resource management
```python
with open('file.txt') as f:
    data = f.read()
```

### Be Consistent in Return Statements
- If any return statement returns an expression, any return statements where no value is returned should explicitly state this as `return None`

### String Methods
- Use string methods instead of the string module
- String methods are always much faster

### String Prefixes
- Use `.startswith()` and `.endswith()` instead of string slicing
```python
# Yes
if foo.startswith('bar'):

# No
if foo[:3] == 'bar':
```

### Object Type Comparisons
- Use `isinstance()` instead of comparing types directly
```python
# Yes
if isinstance(obj, int):

# No
if type(obj) is type(1):
```

### Sequences
- For sequences, (strings, lists, tuples), use the fact that empty sequences are false
```python
# Yes
if not seq:
if seq:

# No
if len(seq):
if not len(seq):
```

### String Literals
- Use `.format()` method or f-strings instead of the `%` operator
```python
# Python 3.6+
name = "World"
greeting = f"Hello, {name}"

# Python 2.6+
greeting = "Hello, {}".format(name)
```

## Function Annotations

### Type Hints (PEP 484)
```python
def greeting(name: str) -> str:
    return f'Hello {name}'
```

### Variable Annotations (PEP 526)
```python
code: int
class Point:
    coords: tuple[int, int]
    label: str = '<unknown>'
```

## Best Practices

### Default Arguments
- Never use mutable default arguments
```python
# No
def append_to(element, to=[]):
    to.append(element)
    return to

# Yes
def append_to(element, to=None):
    if to is None:
        to = []
    to.append(element)
    return to
```

### Lambda Functions
- Avoid assigning lambdas to a name, use `def` instead
```python
# Yes
def f(x):
    return 2*x

# No
f = lambda x: 2*x
```

### Exception Handling
- Derive exceptions from Exception rather than BaseException
- Minimize the amount of code in a try/except block
- Use `finally` for cleanup actions

### Return Consistency
- Be consistent in return statements
- Either all return statements in a function should return an expression, or none of them should

### Generator Expressions
- For simple cases, use generator expressions instead of list comprehensions when dealing with large datasets
```python
# More memory efficient
sum(x**2 for x in range(1000000))

# vs
sum([x**2 for x in range(1000000)])
```
