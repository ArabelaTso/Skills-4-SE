# Language-Specific Analysis Guide

## Python

### Dependency Files
- `requirements.txt` - pip dependencies
- `Pipfile` / `Pipfile.lock` - pipenv
- `pyproject.toml` - poetry, modern Python projects
- `setup.py` / `setup.cfg` - package configuration

### Import Analysis
```python
# Direct imports
import vulnerable_lib
from vulnerable_lib import function
from vulnerable_lib.module import Class

# Aliased imports
import vulnerable_lib as vlib

# Wildcard imports (check all symbols)
from vulnerable_lib import *
```

### Call Chain Analysis
- Search for function/class names in codebase
- Check for `getattr()`, `__import__()`, `importlib.import_module()`
- Look for dynamic attribute access: `obj.__dict__[name]()`

### Configuration Patterns
- Environment variables: `os.environ.get()`, `os.getenv()`
- Config files: `configparser`, `yaml.safe_load()`, `json.load()`
- Django settings: `settings.py`, `INSTALLED_APPS`
- Flask config: `app.config.from_object()`

### Framework-Specific
- **Django**: Check `INSTALLED_APPS`, middleware, URL patterns
- **Flask**: Check blueprints, `@app.route`, extensions
- **FastAPI**: Check routers, dependencies, middleware

## JavaScript/TypeScript

### Dependency Files
- `package.json` - npm/yarn dependencies
- `package-lock.json` / `yarn.lock` - locked versions
- `pnpm-lock.yaml` - pnpm

### Import Analysis
```javascript
// CommonJS
const lib = require('vulnerable-lib');
const { func } = require('vulnerable-lib');

// ES6 modules
import lib from 'vulnerable-lib';
import { func } from 'vulnerable-lib';
import * as lib from 'vulnerable-lib';

// Dynamic imports
const lib = await import('vulnerable-lib');
require(dynamicName);
```

### Call Chain Analysis
- Search for function/class usage
- Check for `eval()`, `Function()` constructor
- Look for dynamic property access: `obj[prop]()`
- Check for `Reflect.apply()`, `Reflect.construct()`

### Configuration Patterns
- Environment variables: `process.env.VAR`
- Config files: `.env`, `config.js`, `config.json`
- Build-time: `webpack.DefinePlugin`, `vite.define`

### Framework-Specific
- **Express**: Check middleware, routes, `app.use()`
- **React**: Check component imports, hooks, context providers
- **Next.js**: Check API routes, middleware, `getServerSideProps`
- **Vue**: Check plugins, mixins, components

## Java

### Dependency Files
- `pom.xml` - Maven
- `build.gradle` / `build.gradle.kts` - Gradle
- `ivy.xml` - Ivy

### Import Analysis
```java
// Direct imports
import com.vulnerable.lib.VulnerableClass;
import com.vulnerable.lib.*;

// Static imports
import static com.vulnerable.lib.VulnerableClass.method;
```

### Call Chain Analysis
- Search for class/method usage
- Check for reflection: `Class.forName()`, `Method.invoke()`
- Look for dynamic proxies: `Proxy.newProxyInstance()`
- Check for service loaders: `ServiceLoader.load()`

### Configuration Patterns
- System properties: `System.getProperty()`
- Environment variables: `System.getenv()`
- Spring: `@Value`, `application.properties`, `application.yml`
- Config files: `config.properties`, XML configs

### Framework-Specific
- **Spring**: Check `@Autowired`, `@Component`, `@Bean`, component scanning
- **Spring Boot**: Check auto-configuration, starters
- **Jakarta EE**: Check `@Inject`, CDI beans, servlets
- **Android**: Check manifest, build variants, ProGuard rules

## Go

### Dependency Files
- `go.mod` - module dependencies
- `go.sum` - checksums
- `vendor/` - vendored dependencies

### Import Analysis
```go
// Direct imports
import "vulnerable/package"
import vp "vulnerable/package"

// Blank imports (side effects)
import _ "vulnerable/package"

// Dot imports (not recommended)
import . "vulnerable/package"
```

### Call Chain Analysis
- Search for package usage
- Check for `reflect` package usage
- Look for `plugin.Open()` for dynamic loading
- Check for `go:linkname` directives

### Configuration Patterns
- Environment variables: `os.Getenv()`
- Config files: `viper`, `yaml`, `json` packages
- Build tags: `// +build tag`
- Build constraints: `//go:build`

### Framework-Specific
- **HTTP servers**: Check handlers, middleware
- **gRPC**: Check service implementations
- **Gin/Echo**: Check route handlers, middleware

## Ruby

### Dependency Files
- `Gemfile` - bundler dependencies
- `Gemfile.lock` - locked versions
- `.gemspec` - gem specification

### Import Analysis
```ruby
# Require statements
require 'vulnerable_lib'
require_relative 'vulnerable_lib'

# Autoload
autoload :VulnerableClass, 'vulnerable_lib'
```

### Call Chain Analysis
- Search for class/module usage
- Check for `send()`, `public_send()`, `method()`, `eval()`
- Look for `const_get()`, `const_missing()`
- Check for `method_missing()` hooks

### Configuration Patterns
- Environment variables: `ENV['VAR']`
- Config files: `config/*.rb`, YAML configs
- Rails: `config/application.rb`, `config/environments/`

### Framework-Specific
- **Rails**: Check `Gemfile`, initializers, middleware, routes
- **Sinatra**: Check routes, middleware
- **Rake**: Check task definitions

## C#/.NET

### Dependency Files
- `*.csproj` - project file with PackageReference
- `packages.config` - NuGet (legacy)
- `*.sln` - solution file

### Import Analysis
```csharp
// Using directives
using VulnerableLib;
using VulnerableLib.Namespace;
using static VulnerableLib.Class;
```

### Call Chain Analysis
- Search for type/method usage
- Check for reflection: `Type.GetType()`, `Assembly.Load()`
- Look for `Activator.CreateInstance()`
- Check for MEF: `[Import]`, `[Export]`

### Configuration Patterns
- App settings: `appsettings.json`, `web.config`
- Environment variables: `Environment.GetEnvironmentVariable()`
- Configuration API: `IConfiguration`

### Framework-Specific
- **ASP.NET Core**: Check `Startup.cs`, middleware, controllers, DI
- **ASP.NET MVC**: Check controllers, filters, bundles
- **WPF/WinForms**: Check XAML, event handlers

## PHP

### Dependency Files
- `composer.json` - Composer dependencies
- `composer.lock` - locked versions

### Import Analysis
```php
// Require/include
require 'vulnerable_lib.php';
require_once 'vulnerable_lib.php';
include 'vulnerable_lib.php';

// Autoloading
use VulnerableLib\VulnerableClass;
use function VulnerableLib\vulnerable_function;
```

### Call Chain Analysis
- Search for class/function usage
- Check for `call_user_func()`, `call_user_func_array()`
- Look for `eval()`, `create_function()`
- Check for variable functions: `$func()`

### Configuration Patterns
- Environment variables: `$_ENV`, `getenv()`
- Config files: `.env`, `config.php`
- Framework configs: Laravel `.env`, Symfony `config/`

### Framework-Specific
- **Laravel**: Check service providers, facades, middleware
- **Symfony**: Check bundles, services, event listeners
- **WordPress**: Check plugins, themes, hooks

## Rust

### Dependency Files
- `Cargo.toml` - dependencies
- `Cargo.lock` - locked versions

### Import Analysis
```rust
// Use statements
use vulnerable_crate::VulnerableType;
use vulnerable_crate::*;

// Extern crate (older style)
extern crate vulnerable_crate;
```

### Call Chain Analysis
- Search for type/function usage
- Check for dynamic loading: `libloading` crate
- Look for unsafe code blocks
- Check for procedural macros

### Configuration Patterns
- Environment variables: `env!()`, `option_env!()`
- Feature flags: `[features]` in `Cargo.toml`
- Conditional compilation: `#[cfg()]`

### Framework-Specific
- **Web frameworks**: Check Actix/Rocket/Axum handlers, middleware
- **Async runtime**: Check tokio/async-std usage

## Analysis Priorities by Language

### High Priority (Easy to Analyze)
1. **Python**: Clear import statements, straightforward call chains
2. **Go**: Explicit imports, limited reflection
3. **Rust**: Strong type system, explicit dependencies

### Medium Priority (Moderate Complexity)
1. **Java**: Reflection and DI complicate analysis
2. **C#**: Similar to Java, but with LINQ and dynamic
3. **TypeScript**: Type information helps, but still dynamic

### Lower Priority (Complex Analysis)
1. **JavaScript**: Highly dynamic, eval, dynamic requires
2. **Ruby**: Metaprogramming, method_missing, eval
3. **PHP**: Variable functions, dynamic includes
