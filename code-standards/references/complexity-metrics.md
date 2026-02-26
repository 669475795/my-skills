# Cyclomatic Complexity and Code Metrics

## Cyclomatic Complexity

### Definition
Cyclomatic Complexity (CC) is a software metric used to indicate the complexity of a program. It measures the number of linearly independent paths through a program's source code.

### Formula
```
CC = E - N + 2P
```
Where:
- E = number of edges in the control flow graph
- N = number of nodes
- P = number of connected components (usually 1 for a single method)

### Simplified Calculation
```
CC = 1 + number of decision points
```

Decision points include:
- `if` statements
- `while` and `for` loops
- `case` in switch statements
- `&&` and `||` operators
- `catch` clauses
- Ternary operators (`? :`)

### Complexity Ratings

| CC Score | Risk Level | Maintainability |
|----------|------------|-----------------|
| 1-10     | Low        | Simple, easy to test |
| 11-20    | Moderate   | More complex, acceptable |
| 21-50    | High       | Complex, hard to test |
| 51+      | Very High  | Very complex, error-prone |

### Recommended Thresholds

#### Conservative (Recommended)
- **Method level**: CC ≤ 10
- **Class level**: CC ≤ 50
- **File level**: CC ≤ 100

#### Moderate
- **Method level**: CC ≤ 15
- **Class level**: CC ≤ 80
- **File level**: CC ≤ 150

#### Relaxed (Legacy Code)
- **Method level**: CC ≤ 20
- **Class level**: CC ≤ 100
- **File level**: CC ≤ 200

## Examples

### Java Example

#### High Complexity (CC = 8)
```java
public String processOrder(Order order) {
    if (order == null) {  // +1
        return "Invalid order";
    }

    if (order.getStatus() == Status.PENDING) {  // +1
        if (order.isPaid()) {  // +1
            if (order.hasStock()) {  // +1
                return "Processing";
            } else {
                return "Out of stock";
            }
        } else if (order.isExpired()) {  // +1
            return "Payment expired";
        } else {
            return "Awaiting payment";
        }
    } else if (order.getStatus() == Status.SHIPPED) {  // +1
        return "Already shipped";
    } else {
        return "Unknown status";
    }
}
```

#### Refactored (Lower Complexity)
```java
public String processOrder(Order order) {
    if (order == null) {
        return "Invalid order";
    }

    return switch (order.getStatus()) {
        case PENDING -> processPendingOrder(order);
        case SHIPPED -> "Already shipped";
        default -> "Unknown status";
    };
}

private String processPendingOrder(Order order) {  // CC = 3
    if (!order.isPaid()) {
        return order.isExpired() ? "Payment expired" : "Awaiting payment";
    }
    return order.hasStock() ? "Processing" : "Out of stock";
}
```

### Python Example

#### High Complexity (CC = 7)
```python
def calculate_discount(customer, amount):
    discount = 0

    if customer.is_vip:  # +1
        discount = 0.2
    elif customer.years > 5:  # +1
        discount = 0.15
    elif customer.years > 2:  # +1
        discount = 0.1

    if amount > 10000:  # +1
        discount += 0.05
    elif amount > 5000:  # +1
        discount += 0.03

    if customer.has_coupon and discount < 0.3:  # +2
        discount = 0.3

    return amount * (1 - discount)
```

#### Refactored (Lower Complexity)
```python
def calculate_discount(customer, amount):
    base_discount = get_customer_discount(customer)  # CC = 3
    amount_discount = get_amount_discount(amount)    # CC = 2

    total_discount = base_discount + amount_discount

    if customer.has_coupon:  # CC = 1
        total_discount = max(total_discount, 0.3)

    return amount * (1 - total_discount)
```

## Reducing Cyclomatic Complexity

### Strategy 1: Extract Methods
Break down complex methods into smaller, focused methods.

### Strategy 2: Replace Nested Conditionals
Use early returns or guard clauses.

```java
// Before (CC = 4)
public void process(Order order) {
    if (order != null) {
        if (order.isValid()) {
            if (order.isPaid()) {
                ship(order);
            }
        }
    }
}

// After (CC = 3)
public void process(Order order) {
    if (order == null) return;
    if (!order.isValid()) return;
    if (!order.isPaid()) return;

    ship(order);
}
```

### Strategy 3: Use Polymorphism
Replace type codes or switch statements with polymorphism.

```java
// Before (High CC)
public double calculatePrice(String productType, double basePrice) {
    if (productType.equals("BOOK")) {
        return basePrice * 0.9;
    } else if (productType.equals("ELECTRONICS")) {
        return basePrice * 1.1;
    } else if (productType.equals("CLOTHING")) {
        return basePrice * 1.05;
    }
    return basePrice;
}

// After (Lower CC per method)
interface PricingStrategy {
    double calculate(double basePrice);
}

class BookPricing implements PricingStrategy {
    public double calculate(double basePrice) {
        return basePrice * 0.9;
    }
}
```

### Strategy 4: Use Lookup Tables
Replace complex conditionals with data structures.

```python
# Before (CC = 5)
def get_status_message(code):
    if code == 200:
        return "OK"
    elif code == 404:
        return "Not Found"
    elif code == 500:
        return "Internal Server Error"
    elif code == 403:
        return "Forbidden"
    else:
        return "Unknown"

# After (CC = 1)
STATUS_MESSAGES = {
    200: "OK",
    404: "Not Found",
    500: "Internal Server Error",
    403: "Forbidden"
}

def get_status_message(code):
    return STATUS_MESSAGES.get(code, "Unknown")
```

### Strategy 5: Simplify Boolean Logic
Use De Morgan's laws and combine conditions.

```java
// Before
if (!(a && b)) {
    // ...
}

// After
if (!a || !b) {
    // ...
}
```

## Other Code Metrics

### Lines of Code (LOC)
- **Recommended**: Methods < 50 lines, Classes < 500 lines
- Measure of code size and potential complexity

### Nesting Depth
- **Recommended**: Maximum depth of 3-4 levels
- Deep nesting indicates high complexity

### Number of Parameters
- **Recommended**: ≤ 4 parameters per method
- Too many parameters suggest need for parameter objects

### Coupling Metrics
- **Afferent Coupling (Ca)**: Number of classes that depend on this class
- **Efferent Coupling (Ce)**: Number of classes this class depends on
- **Instability**: I = Ce / (Ce + Ca)
  - I = 0: Completely stable
  - I = 1: Completely unstable
  - **Recommended**: I = 0.3 - 0.7 for most classes

### Maintainability Index
```
MI = 171 - 5.2 * ln(HV) - 0.23 * CC - 16.2 * ln(LOC)
```
Where:
- HV = Halstead Volume
- CC = Cyclomatic Complexity
- LOC = Lines of Code

Scale:
- **85-100**: Good maintainability
- **65-85**: Moderate maintainability
- **< 65**: Difficult to maintain

## Tools for Measuring Complexity

### Java
- **PMD**: Static code analyzer
- **SonarQube**: Continuous code quality platform
- **Checkstyle**: Code style checker
- **JaCoCo**: Code coverage tool with complexity metrics

### Python
- **radon**: Cyclomatic complexity calculator
- **mccabe**: McCabe complexity checker
- **pylint**: Code analyzer
- **SonarQube**: Also supports Python

### Usage Examples

#### Java (PMD)
```bash
pmd -d src/main/java -R rulesets/java/codesize.xml -f text
```

#### Python (radon)
```bash
# Show complexity
radon cc mycode.py -s

# Show maintainability index
radon mi mycode.py -s

# Set threshold
radon cc mycode.py -nc 10  # Fail if CC > 10
```

## Best Practices

1. **Set Team Standards**: Agree on complexity thresholds
2. **Automate Checks**: Integrate into CI/CD pipeline
3. **Review Regular**: Monitor complexity trends
4. **Refactor Proactively**: Don't wait until CC is very high
5. **Focus on Hot Spots**: Prioritize frequently changed, high-complexity code
6. **Balance Metrics**: Don't optimize for one metric at expense of others
7. **Use with Context**: High CC acceptable for algorithms, state machines

## When High Complexity is Acceptable

- Algorithm implementations (sorting, searching)
- State machines with many states
- Parser logic
- Configuration validation with many rules
- Legacy code (refactor gradually)

In these cases:
- Add comprehensive tests
- Document the complexity
- Keep the complex code isolated
- Consider generating code from specifications
