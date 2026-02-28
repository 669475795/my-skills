---
name: code-standards
description: "Comprehensive code quality checker for Java and Python that ensures code meets industry standards including design patterns, code style, security best practices, and cyclomatic complexity thresholds. Use this skill when: (1) Writing new code (proactively check as you write), (2) User writes code and needs validation, (3) User requests manual/comprehensive code review or audit, (4) Refactoring existing code to improve quality, (5) User mentions any of these standards - Google Style Guide, Alibaba Java Guide, PEP 8, OWASP security, cyclomatic complexity, code quality, design patterns, or code review. The skill supports multiple standards and allows users to specify which standards to apply."
---

# Code Standards Checker

Ensure your Java and Python code meets industry-leading standards for quality, security, and maintainability.

## Supported Standards

### Java
- **Google Java Style Guide** - Formatting, naming, Javadoc conventions
- **Alibaba Java Development Guidelines** - Chinese industry best practices, database, concurrency
- **OWASP Security Standards** - Security vulnerabilities and prevention

### Python
- **Google Python Style Guide** - Style, documentation, best practices
- **PEP 8** - Official Python style guide
- **OWASP Security Standards** - Security vulnerabilities and prevention

### Cross-Language
- **Cyclomatic Complexity** - Code complexity metrics
- **Design Patterns** - Best practices for common problems

## When to Use This Skill

This skill is automatically invoked when:
1. You are writing code for the user
2. User is writing code and needs real-time validation
3. User requests a code review or quality check
4. Refactoring code to improve quality
5. User mentions specific standards (Google Style Guide, PEP 8, etc.)

## Usage Workflow

### Step 1: Determine Which Standards to Apply

**If user specifies standards:**
Use exactly what the user requested.

**If user doesn't specify:**
Apply all relevant standards for the language:
- Java: Google Style Guide + Alibaba Java Guide + OWASP Security + Complexity
- Python: Google Style Guide + PEP 8 + OWASP Security + Complexity

**Standard Priority (for conflicts):**

When multiple standards conflict on the same issue, use this priority order:

**Java:**
1. **Google Java Style Guide** (highest priority)
2. Alibaba Java Development Guidelines
3. OWASP Security Standards (always enforced for security issues)
4. Cyclomatic Complexity metrics

**Python:**
1. **PEP 8** (highest priority - official Python standard)
2. Google Python Style Guide
3. OWASP Security Standards (always enforced for security issues)
4. Cyclomatic Complexity metrics

**Known Conflicts (Java):**
- **Indentation**: Google (2 spaces) vs Alibaba (4 spaces) 鈫?Use Google (2 spaces)
- **Line length**: Google (100 chars) vs Alibaba (120 chars) 鈫?Use Google (100 chars)
- **Boolean POJO fields**: Both agree - don't use `is` prefix for Boolean wrapper types
- **Best practices**: When both provide guidance, prefer Google for style, Alibaba for domain-specific (DB, concurrency, Chinese context)

**Important:** Security violations from OWASP always take precedence regardless of style preferences.

### Step 2: Load Relevant References

Based on standards selected in Step 1, read the appropriate reference files:

- `references/google-style-guide-java.md` - For Google Java standards
- `references/google-style-guide-python.md` - For Google Python standards
- `references/alibaba-java-guide.md` - For Alibaba Java standards
- `references/pep8-guide.md` - For PEP 8 standards
- `references/owasp-security.md` - For security standards
- `references/complexity-metrics.md` - For complexity analysis

**Best Practice:** Only read the references you need for the current check to minimize context usage.

### Step 3: Analyze the Code

Perform systematic checks across these dimensions:

#### 3.1 Code Style & Formatting
- Naming conventions (classes, methods, variables, constants)
- Indentation and whitespace
- Line length limits
- Import organization
- Brace style and code layout

#### 3.2 Design Patterns & Best Practices
- Appropriate use of design patterns
- SOLID principles adherence
- Code smells and anti-patterns
- Proper use of language features

#### 3.3 Security Vulnerabilities
Check for OWASP Top 10 issues:
- SQL Injection
- XSS vulnerabilities
- Broken authentication
- Sensitive data exposure
- Security misconfigurations
- Unsafe deserialization
- Input validation issues

#### 3.4 Cyclomatic Complexity

**Automated Check:**
Use the provided script for automated complexity analysis:

```bash
# Check complexity with default thresholds (method: 10, file: 100)
python scripts/check_complexity.py <path>

# Custom thresholds
python scripts/check_complexity.py <path> --max-complexity 15

# Use configuration file
python scripts/check_complexity.py <path> --config scripts/config.yaml

# JSON output for CI/CD
python scripts/check_complexity.py <path> --format json --fail-on-violation
```

**Manual Review:**
If automated tools are not available, manually assess:
- Count decision points (if, while, for, case, &&, ||, catch, ternary)
- Calculate: CC = 1 + number of decision points
- Compare against thresholds:
  - Method: 鈮?10 (conservative), 鈮?15 (moderate), 鈮?20 (relaxed)
  - File: 鈮?100 (conservative), 鈮?150 (moderate), 鈮?200 (relaxed)

See `references/complexity-metrics.md` for detailed examples and refactoring strategies.

### Step 4: Report Findings

Structure your findings clearly:

```markdown
## Code Standards Review Report

### Summary
- **Language**: Java/Python
- **Standards Applied**: [list of standards]
- **Total Issues**: X
- **Severity Breakdown**: X errors, Y warnings, Z info

### Issues Found

#### 1. [Category] - [Severity]
**Location**: `file.java:123`
**Standard**: Google Java Style Guide
**Issue**: [Description of what's wrong]
**Current Code**:
```java
// problematic code here
```
**Recommendation**:
```java
// fixed code here
```
**Explanation**: [Why this matters and how to fix it]

[Repeat for each issue...]

### Cyclomatic Complexity Analysis

| File | Function | Line | CC | Threshold | Status |
|------|----------|------|----|-----------|----- --|
| Foo.java | processOrder | 45 | 12 | 10 | 鈿狅笍 Warning |

**High Complexity Functions**:
- `Foo.processOrder()` (CC=12): Consider extracting methods or using strategy pattern

### Security Concerns

[List any OWASP violations found]

### Positive Findings

[Mention things done well to encourage good practices]

### Overall Assessment

[Summary and recommendations]
```

### Step 5: Offer to Fix Issues

After reporting, offer to fix the issues:

**Options:**
1. **Fix all issues automatically** - Apply all recommendations
2. **Fix specific issues** - User selects which to fix
3. **Provide detailed guidance** - Explain how user can fix manually

## Configuration

Users can customize thresholds and settings by modifying `scripts/config.yaml`:

```yaml
thresholds:
  method: 10   # Cyclomatic complexity for methods
  class: 50    # Cyclomatic complexity for classes
  file: 100    # Cyclomatic complexity for files

exclude_patterns:
  - "*/test/*"
  - "*Test.java"
```

Show users this file if they want to customize behavior.

## Handling Different Scenarios

### Scenario 1: Real-time Code Writing
- Apply checks as code is written
- Provide immediate feedback
- Fix issues before moving forward

### Scenario 2: Comprehensive Review
- Analyze entire files or directories
- Generate detailed report
- Prioritize issues by severity

### Scenario 3: Specific Standard Check
User says: "Check this against PEP 8"
- Only load `references/pep8-guide.md`
- Focus review on PEP 8 compliance
- Skip other standards unless issues are critical

### Scenario 4: Security Audit
User says: "Check for security issues"
- Load `references/owasp-security.md`
- Focus on OWASP Top 10
- Report all security vulnerabilities
- Provide immediate fixes for critical issues

### Scenario 5: Complexity Reduction
User says: "This code is too complex"
- Run complexity analysis
- Load `references/complexity-metrics.md`
- Suggest refactoring strategies
- Provide before/after examples

## Best Practices for Using This Skill

1. **Be Specific**: If checking for specific standards, mention them to avoid unnecessary analysis
2. **Prioritize**: Focus on errors first, then warnings, then style suggestions
3. **Context Matters**: Legacy code may need relaxed thresholds
4. **Automated Checks**: Use the complexity script in CI/CD pipelines
5. **Incremental Improvement**: For large codebases, fix high-priority issues first

## Examples

### Example 1: Quick Style Check
```
User: "Check this Java code for style issues"
Assistant:
1. Determines: Google Java Style Guide + Alibaba Java Guide
2. Reads: google-style-guide-java.md, alibaba-java-guide.md
3. Analyzes code for style violations
4. Reports findings with fixes
5. Offers to apply fixes
```

### Example 2: Security Review
```
User: "Review this code for security vulnerabilities"
Assistant:
1. Determines: OWASP Security Standards
2. Reads: owasp-security.md
3. Scans for SQL injection, XSS, auth issues, etc.
4. Reports security findings with severity
5. Provides secure code examples
6. Offers to fix critical issues immediately
```

### Example 3: Complexity Refactoring
```
User: "This function is too complex, help me simplify it"
Assistant:
1. Runs: scripts/check_complexity.py on the function
2. Reads: complexity-metrics.md
3. Identifies high CC and root causes
4. Suggests refactoring strategies (extract method, strategy pattern, etc.)
5. Provides refactored code
6. Verifies reduced complexity
```

## Severity Levels

**Error (馃敶)**: Must fix
- Security vulnerabilities
- Code that violates language specifications
- Complexity far exceeding thresholds (CC > 20)

**Warning (鈿狅笍)**: Should fix
- Style violations
- Moderate complexity (CC 11-20)
- Missing documentation
- Code smells

**Info (鈩癸笍)**: Consider fixing
- Style preferences
- Optimization suggestions
- Alternative patterns

## Integration with Development Workflow

### Pre-commit Hook
```bash
# Run complexity check before commit
python scripts/check_complexity.py src --fail-on-violation
```

### CI/CD Pipeline
```yaml
# Example GitHub Actions
- name: Check Code Standards
  run: |
    pip install lizard radon
    python scripts/check_complexity.py src --format json --fail-on-violation
```

### IDE Integration
- Use with VS Code, IntelliJ IDEA
- Run on save or manually
- Get immediate feedback

## Troubleshooting

**Issue**: Complexity script not working
- **Solution**: Install required packages: `pip install lizard radon PyYAML`

**Issue**: Too many false positives
- **Solution**: Adjust thresholds in `config.yaml` or use exclude patterns

**Issue**: Different standards conflict
- **Solution**: User should specify which standard takes precedence

## Notes

- This skill uses progressive disclosure: only relevant reference files are loaded
- For large codebases, consider checking modified files only
- Complexity thresholds are guidelines, not absolute rules
- Context matters: algorithm implementations may legitimately have higher complexity
- Security checks are not exhaustive - use dedicated security tools for comprehensive audits
