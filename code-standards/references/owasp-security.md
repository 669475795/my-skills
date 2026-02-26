# OWASP Security Standards

## OWASP Top 10 (2021)

### A01:2021 - Broken Access Control

#### Vulnerabilities
- Bypassing access control checks
- Viewing or editing someone else's account
- Acting as a user without being logged in
- Elevation of privilege
- CORS misconfiguration allowing unauthorized API access

#### Prevention
```java
// Check authorization for every request
@PreAuthorize("hasRole('ADMIN') or #userId == authentication.principal.id")
public void updateUser(Long userId, UserDto user) {
    // ...
}

// Deny by default
public boolean hasAccess(User user, Resource resource) {
    return accessControlList.contains(user, resource);
}
```

```python
# Use decorator to enforce access control
@require_permission('admin')
def delete_user(user_id):
    # ...

# Check ownership
def update_profile(user_id, data):
    if current_user.id != user_id and not current_user.is_admin:
        raise PermissionError("Access denied")
```

### A02:2021 - Cryptographic Failures

#### Vulnerabilities
- Transmitting data in clear text (HTTP, FTP, SMTP)
- Using old or weak cryptographic algorithms
- Not using encryption for sensitive data
- Weak key generation or management
- Missing or improper certificate validation

#### Prevention
```java
// Use strong algorithms
Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");

// Don't hardcode secrets
String apiKey = System.getenv("API_KEY");

// Use bcrypt for passwords
BCryptPasswordEncoder encoder = new BCryptPasswordEncoder(12);
String hashedPassword = encoder.encode(password);

// Always use HTTPS
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) {
        return http
            .requiresChannel()
            .anyRequest()
            .requiresSecure()
            .and()
            .build();
    }
}
```

```python
# Use strong hashing for passwords
from werkzeug.security import generate_password_hash, check_password_hash

hashed = generate_password_hash(password, method='pbkdf2:sha256', salt_length=16)

# Encrypt sensitive data
from cryptography.fernet import Fernet

key = Fernet.generate_key()
cipher = Fernet(key)
encrypted = cipher.encrypt(data.encode())

# Use environment variables for secrets
import os
SECRET_KEY = os.environ.get('SECRET_KEY')
```

### A03:2021 - Injection

#### SQL Injection

```java
// Vulnerable
String query = "SELECT * FROM users WHERE username = '" + username + "'";
Statement stmt = connection.createStatement();
ResultSet rs = stmt.executeQuery(query);

// Secure - Use PreparedStatement
String query = "SELECT * FROM users WHERE username = ?";
PreparedStatement pstmt = connection.prepareStatement(query);
pstmt.setString(1, username);
ResultSet rs = pstmt.executeQuery();

// Secure - Use JPA
@Query("SELECT u FROM User u WHERE u.username = :username")
User findByUsername(@Param("username") String username);
```

```python
# Vulnerable
cursor.execute(f"SELECT * FROM users WHERE username = '{username}'")

# Secure - Use parameterized queries
cursor.execute("SELECT * FROM users WHERE username = %s", (username,))

# Secure - Use ORM
user = User.query.filter_by(username=username).first()
```

#### Command Injection

```java
// Vulnerable
Runtime.getRuntime().exec("ls " + userInput);

// Secure - Validate and sanitize
if (userInput.matches("[a-zA-Z0-9]+")) {
    ProcessBuilder pb = new ProcessBuilder("ls", userInput);
    pb.start();
}
```

```python
# Vulnerable
os.system(f"ping {host}")

# Secure - Use subprocess with list
import subprocess
subprocess.run(["ping", "-c", "1", host], check=True)
```

#### LDAP Injection

```java
// Vulnerable
String filter = "(uid=" + username + ")";

// Secure - Escape special characters
String filter = "(uid=" + escapeLDAP(username) + ")";
```

### A04:2021 - Insecure Design

#### Security Design Principles
- Defense in depth
- Fail securely
- Least privilege
- Separation of duties
- Complete mediation
- Open design
- Psychological acceptability

#### Prevention
```java
// Implement rate limiting
@RateLimiter(name = "login", fallbackMethod = "loginFallback")
public ResponseEntity<AuthResponse> login(LoginRequest request) {
    // ...
}

// Resource limits
@Bean
public HttpFirewall httpFirewall() {
    StrictHttpFirewall firewall = new StrictHttpFirewall();
    firewall.setAllowedHttpMethods(Arrays.asList("GET", "POST", "PUT", "DELETE"));
    return firewall;
}
```

### A05:2021 - Security Misconfiguration

#### Common Issues
- Default accounts and passwords
- Unnecessary features enabled
- Error messages revealing sensitive information
- Missing security headers
- Outdated software

#### Prevention
```java
// Disable detailed error messages in production
@ControllerAdvice
public class GlobalExceptionHandler {
    @ExceptionHandler(Exception.class)
    public ResponseEntity<ErrorResponse> handleException(Exception ex) {
        // Log the full error
        logger.error("Error occurred", ex);

        // Return generic message to user
        return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR)
            .body(new ErrorResponse("An error occurred"));
    }
}

// Add security headers
@Configuration
public class SecurityConfig {
    @Bean
    public SecurityFilterChain filterChain(HttpSecurity http) {
        return http
            .headers()
            .contentSecurityPolicy("default-src 'self'")
            .and()
            .xssProtection()
            .and()
            .frameOptions().deny()
            .and()
            .build();
    }
}
```

```python
# Flask security headers
from flask_talisman import Talisman

Talisman(app,
    force_https=True,
    strict_transport_security=True,
    content_security_policy={
        'default-src': "'self'"
    }
)

# Django security settings
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
```

### A06:2021 - Vulnerable and Outdated Components

#### Prevention
- Maintain inventory of components and versions
- Monitor for vulnerabilities (CVE, NVD)
- Only obtain components from official sources
- Remove unused dependencies
- Use automated tools (OWASP Dependency-Check, Snyk)

```xml
<!-- Maven dependency check -->
<plugin>
    <groupId>org.owasp</groupId>
    <artifactId>dependency-check-maven</artifactId>
    <version>8.0.0</version>
    <executions>
        <execution>
            <goals>
                <goal>check</goal>
            </goals>
        </execution>
    </executions>
</plugin>
```

```bash
# Python - Check for vulnerabilities
pip install safety
safety check

# Or use pip-audit
pip install pip-audit
pip-audit
```

### A07:2021 - Identification and Authentication Failures

#### Vulnerabilities
- Permits brute force attacks
- Permits default, weak, or well-known passwords
- Uses plain text or weakly hashed passwords
- Missing or ineffective multi-factor authentication
- Exposes session identifiers in URLs
- Doesn't rotate session IDs after login

#### Prevention
```java
// Implement account lockout
private static final int MAX_ATTEMPTS = 5;
private Map<String, Integer> loginAttempts = new ConcurrentHashMap<>();

public void login(String username, String password) {
    int attempts = loginAttempts.getOrDefault(username, 0);

    if (attempts >= MAX_ATTEMPTS) {
        throw new AccountLockedException("Account locked");
    }

    if (!authenticate(username, password)) {
        loginAttempts.put(username, attempts + 1);
        throw new BadCredentialsException("Invalid credentials");
    }

    loginAttempts.remove(username);
}

// Secure session management
http.sessionManagement()
    .sessionCreationPolicy(SessionCreationPolicy.IF_REQUIRED)
    .sessionFixation().newSession()
    .maximumSessions(1)
    .maxSessionsPreventsLogin(true);
```

```python
# Flask-Login with rate limiting
from flask_limiter import Limiter

limiter = Limiter(app, key_func=lambda: request.remote_addr)

@app.route('/login', methods=['POST'])
@limiter.limit("5 per minute")
def login():
    # ...

# Strong password validation
import re

def is_strong_password(password):
    if len(password) < 12:
        return False
    if not re.search(r'[A-Z]', password):
        return False
    if not re.search(r'[a-z]', password):
        return False
    if not re.search(r'[0-9]', password):
        return False
    if not re.search(r'[!@#$%^&*]', password):
        return False
    return True
```

### A08:2021 - Software and Data Integrity Failures

#### Prevention
- Verify software updates and patches are from trusted sources
- Use digital signatures
- Ensure CI/CD pipeline has proper access controls
- Review code and configuration changes

```java
// Verify digital signature
Signature signature = Signature.getInstance("SHA256withRSA");
signature.initVerify(publicKey);
signature.update(data);
boolean isValid = signature.verify(signatureBytes);
```

### A09:2021 - Security Logging and Monitoring Failures

#### What to Log
- Login attempts (success and failure)
- Access control failures
- Input validation failures
- Authentication token validation failures

#### What NOT to Log
- Session identifiers
- Passwords
- Credit card numbers
- Personal identifiable information (PII)

```java
// Secure logging
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

private static final Logger securityLogger = LoggerFactory.getLogger("SECURITY");

public void login(String username, String password) {
    try {
        authenticate(username, password);
        securityLogger.info("Login successful for user: {}", username);
    } catch (BadCredentialsException e) {
        securityLogger.warn("Login failed for user: {}", username);
        throw e;
    }
}

// Don't log sensitive data
logger.info("Processing payment"); // Good
logger.info("Processing payment for card: {}", cardNumber); // Bad!
```

```python
import logging

security_logger = logging.getLogger('security')

def login(username, password):
    try:
        authenticate(username, password)
        security_logger.info(f"Login successful: {username}")
    except AuthenticationError:
        security_logger.warning(f"Login failed: {username}")
        raise
```

### A10:2021 - Server-Side Request Forgery (SSRF)

#### Prevention
```java
// Whitelist allowed domains
private static final Set<String> ALLOWED_DOMAINS = Set.of(
    "api.example.com",
    "cdn.example.com"
);

public String fetchUrl(String url) {
    try {
        URL urlObj = new URL(url);
        String host = urlObj.getHost();

        if (!ALLOWED_DOMAINS.contains(host)) {
            throw new SecurityException("Domain not allowed");
        }

        // Additional checks
        if (isPrivateIP(urlObj.getHost())) {
            throw new SecurityException("Private IP not allowed");
        }

        return httpClient.get(url);
    } catch (MalformedURLException e) {
        throw new IllegalArgumentException("Invalid URL");
    }
}

private boolean isPrivateIP(String host) {
    // Check for localhost, 127.0.0.1, 192.168.x.x, 10.x.x.x, etc.
    return host.equals("localhost") ||
           host.startsWith("127.") ||
           host.startsWith("192.168.") ||
           host.startsWith("10.");
}
```

## Additional Security Best Practices

### Cross-Site Scripting (XSS) Prevention

```java
// Use context-aware escaping
import org.owasp.encoder.Encode;

String safe = Encode.forHtml(userInput);
String safeJs = Encode.forJavaScript(userInput);

// Content Security Policy
response.setHeader("Content-Security-Policy",
    "default-src 'self'; script-src 'self' 'unsafe-inline'");
```

```python
# Flask - automatic escaping in templates
from markupsafe import escape

@app.route('/hello/<name>')
def hello(name):
    return f"Hello, {escape(name)}!"

# Django - templates auto-escape by default
# {{ user_input }}  # Automatically escaped
```

### Cross-Site Request Forgery (CSRF) Prevention

```java
// Spring Security - CSRF enabled by default
http.csrf().csrfTokenRepository(CookieCsrfTokenRepository.withHttpOnlyFalse());
```

```python
# Flask-WTF
from flask_wtf.csrf import CSRFProtect

csrf = CSRFProtect(app)

# Django - CSRF middleware enabled by default
MIDDLEWARE = [
    'django.middleware.csrf.CsrfViewMiddleware',
]
```

### XML External Entity (XXE) Prevention

```java
// Disable external entities
DocumentBuilderFactory dbf = DocumentBuilderFactory.newInstance();
dbf.setFeature("http://apache.org/xml/features/disallow-doctype-decl", true);
dbf.setFeature("http://xml.org/sax/features/external-general-entities", false);
dbf.setFeature("http://xml.org/sax/features/external-parameter-entities", false);
```

```python
# Use defusedxml
from defusedxml import ElementTree

tree = ElementTree.parse('file.xml')
```
