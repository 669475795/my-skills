# Google Java Style Guide - Key Standards

## Formatting

### Braces
- Use K&R style (opening brace on same line)
- Braces required even for single-statement blocks
- Empty blocks may be concise: `{}`

### Indentation
- 2 spaces (not tabs)
- Continuation indent: +4 spaces

### Line Length
- Column limit: 100 characters
- Exceptions: package/import statements, URLs, long literals

### Whitespace
- One blank line between class members (except consecutive fields)
- Vertical whitespace to improve readability
- Horizontal: one space after commas, keywords

## Naming Conventions

### Packages
- All lowercase, no underscores
- `com.example.deepspace` not `com.example.deepSpace`

### Classes
- UpperCamelCase
- Nouns or noun phrases
- Test classes: end with `Test`

### Methods
- lowerCamelCase
- Verbs or verb phrases
- JUnit test methods: `test<MethodUnderTest>_<State>_<ExpectedBehavior>`

### Constants
- CONSTANT_CASE
- `static final` immutable fields

### Variables
- lowerCamelCase
- Not Hungarian notation
- One variable per declaration

## Programming Practices

### @Override
- Always use when applicable
- Exception: deprecated method overriding deprecated method

### Caught Exceptions
- Never ignore without explanation
- Minimum: log or rethrow as AssertionError
- Comment required if truly nothing to do

### Static Members
- Qualify with class name, not instance: `Foo.method()` not `foo.method()`

### Finalizers
- Do not use `Object.finalize()`

### Imports
- No wildcard imports
- No unused imports
- Order: static imports, then non-static, alphabetically

## Javadoc

### Required For
- Every public class
- Every public or protected member (exceptions apply)

### Format
```java
/**
 * Multiple lines of Javadoc text,
 * wrapped normally...
 */
public int method(String p1) { }
```

### Content
- At least one sentence, ending with period
- `@param`, `@return`, `@throws` tags
- No `@author` tags

## Common Issues

### Array Style
- `String[] args` not `String args[]`

### Switch Statements
- Each group ends with break, continue, return, or throw
- Default case must be present or commented why omitted

### Annotations
- One per line for class/method level
- Multiple allowed on parameter level

### Numeric Literals
- Long-valued literals use uppercase `L` suffix: `3000000000L`

## Design Patterns

### Builder Pattern for Complex Objects
- Use when constructor has 4+ parameters

### Factory Methods
- Prefer `valueOf()` or `from()` to constructors

### Dependency Injection
- Prefer constructor injection
- Avoid field injection

## Performance Considerations

### String Concatenation
- Use `StringBuilder` for loops
- String literals okay for simple cases

### Collections
- Specify initial capacity when size known
- Use appropriate collection type

### Lazy Initialization
- Only when necessary for performance
- Document thread-safety implications
