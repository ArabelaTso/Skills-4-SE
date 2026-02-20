# Common Reachability Patterns

## Direct Import and Usage

### Pattern: Direct Function Call
```python
from vulnerable_lib import vulnerable_function

def my_code():
    result = vulnerable_function(user_input)  # REACHABLE
```
**Reachability**: Likely reachable
**Evidence**: Direct import and invocation in code path

### Pattern: Imported but Unused
```python
from vulnerable_lib import vulnerable_function  # Imported but never called

def my_code():
    safe_function()
```
**Reachability**: Likely unreachable
**Evidence**: Import exists but no call sites found

### Pattern: Transitive Dependency
```python
from safe_wrapper import wrapper_function

# safe_wrapper internally uses vulnerable_lib
def my_code():
    wrapper_function()  # May be reachable through wrapper
```
**Reachability**: Possibly reachable
**Evidence**: Depends on wrapper implementation

## Indirect Invocation Patterns

### Pattern: Reflection/Dynamic Loading
```python
import importlib

module_name = get_module_from_config()  # Could be vulnerable_lib
module = importlib.import_module(module_name)
module.function()  # POSSIBLY REACHABLE
```
**Reachability**: Possibly reachable
**Evidence**: Dynamic loading makes static analysis uncertain

### Pattern: Callback Registration
```python
from vulnerable_lib import VulnerableClass

def my_callback():
    pass

obj = VulnerableClass()
obj.register_callback(my_callback)  # Vulnerable code may execute
```
**Reachability**: Likely reachable
**Evidence**: Instantiation and method invocation of vulnerable class

### Pattern: Dependency Injection
```python
class MyService:
    def __init__(self, dependency):
        self.dep = dependency

    def process(self):
        self.dep.vulnerable_method()  # Reachability depends on injection
```
**Reachability**: Possibly reachable
**Evidence**: Depends on runtime dependency injection configuration

## Configuration-Gated Patterns

### Pattern: Feature Flag
```python
from vulnerable_lib import vulnerable_feature

if config.get('enable_vulnerable_feature'):
    vulnerable_feature()  # Reachable only if flag enabled
```
**Reachability**: Possibly reachable
**Evidence**: Gated by configuration; check if flag is enabled in production

### Pattern: Environment-Specific Code
```python
if os.environ.get('ENV') == 'development':
    from vulnerable_lib import debug_function
    debug_function()  # Only in dev environment
```
**Reachability**: Possibly reachable (or unreachable in production)
**Evidence**: Environment-dependent; check deployment configuration

### Pattern: Build Profile
```java
// Maven profile: dev-only
if (BuildConfig.DEBUG) {
    VulnerableLib.debugMethod();  // Only in debug builds
}
```
**Reachability**: Possibly reachable
**Evidence**: Build-time conditional; check production build profile

## Framework-Specific Patterns

### Pattern: Servlet/Controller Endpoint
```java
@RestController
public class MyController {
    @Autowired
    private VulnerableService service;  // Vulnerable dependency injected

    @GetMapping("/api/endpoint")
    public Response handle() {
        return service.process();  // REACHABLE via HTTP endpoint
    }
}
```
**Reachability**: Likely reachable
**Evidence**: Exposed via HTTP endpoint, vulnerable service invoked

### Pattern: Event Listener
```javascript
const vulnerableLib = require('vulnerable-lib');

eventEmitter.on('user-action', (data) => {
    vulnerableLib.process(data);  // REACHABLE when event fires
});
```
**Reachability**: Likely reachable
**Evidence**: Event-driven invocation, depends on event frequency

### Pattern: Middleware Chain
```javascript
const vulnerableMiddleware = require('vulnerable-middleware');

app.use(vulnerableMiddleware());  // Executes on every request
```
**Reachability**: Likely reachable
**Evidence**: Middleware executes on all matching requests

## Data Flow Patterns

### Pattern: User Input Reaches Vulnerable Code
```python
from vulnerable_lib import parse_input

@app.route('/process')
def process():
    user_data = request.get_json()
    result = parse_input(user_data)  # User input flows to vulnerable function
```
**Reachability**: Likely reachable (and exploitable)
**Evidence**: User-controlled data reaches vulnerable function

### Pattern: Sanitized Input
```python
from vulnerable_lib import parse_input

def process(user_input):
    sanitized = sanitize(user_input)
    result = parse_input(sanitized)  # Input sanitized before vulnerable code
```
**Reachability**: Likely reachable (but may not be exploitable)
**Evidence**: Vulnerable code is reached, but exploitation depends on sanitization effectiveness

### Pattern: Internal Data Only
```python
from vulnerable_lib import process_data

def internal_job():
    trusted_data = database.get_internal_config()
    process_data(trusted_data)  # Only internal data, no user input
```
**Reachability**: Likely reachable (but lower risk)
**Evidence**: Vulnerable code reached with trusted data only

## Dead Code Patterns

### Pattern: Commented Out
```python
# from vulnerable_lib import vulnerable_function
# vulnerable_function()  # Code commented out
```
**Reachability**: Likely unreachable
**Evidence**: Code is commented out

### Pattern: Unreachable Branch
```python
from vulnerable_lib import vulnerable_function

if False:  # Always false
    vulnerable_function()
```
**Reachability**: Likely unreachable
**Evidence**: Unreachable code branch

### Pattern: Deprecated Code Path
```python
from vulnerable_lib import old_function

def legacy_handler():
    old_function()  # Function exists but no callers found
```
**Reachability**: Likely unreachable
**Evidence**: No call sites found in codebase

## Test-Only Usage

### Pattern: Test Code
```python
# In test_module.py
from vulnerable_lib import vulnerable_function

def test_something():
    result = vulnerable_function(test_data)  # Only used in tests
```
**Reachability**: Likely unreachable (in production)
**Evidence**: Only referenced in test files

### Pattern: Development Tool
```python
# In dev_tools/debug.py
from vulnerable_lib import debug_helper

if __name__ == '__main__':
    debug_helper()  # Development script, not deployed
```
**Reachability**: Likely unreachable (in production)
**Evidence**: Development-only script

## Language-Specific Patterns

### Python: `__init__.py` Imports
```python
# In __init__.py
from .vulnerable_module import *  # Imports everything

# May expose vulnerable functions even if not directly used
```
**Reachability**: Possibly reachable
**Evidence**: Wildcard import may expose vulnerable symbols

### Java: Classpath Scanning
```java
@ComponentScan(basePackages = "com.example")
public class Application {
    // Spring may instantiate vulnerable beans automatically
}
```
**Reachability**: Possibly reachable
**Evidence**: Framework may auto-instantiate vulnerable components

### JavaScript: Dynamic Require
```javascript
const moduleName = getUserInput();
const module = require(moduleName);  // Could load vulnerable module
```
**Reachability**: Possibly reachable
**Evidence**: Dynamic module loading based on runtime data

### Go: Blank Import
```go
import _ "vulnerable/package"  // Side-effect import

// Package init() may execute vulnerable code
```
**Reachability**: Possibly reachable
**Evidence**: Package initialization may execute vulnerable code
