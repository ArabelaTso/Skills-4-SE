# Common Migration Scenarios

This document outlines common migration scenarios and their specific challenges.

## Language Version Migrations

### Python 2 to Python 3

**Breaking changes**:
- Print statement → print() function
- Integer division: `/` → `//` for floor division
- Unicode strings: `u"string"` → default in Python 3
- `xrange()` → `range()`
- `.iteritems()` → `.items()`
- Exception syntax: `except Exception, e:` → `except Exception as e:`
- `raw_input()` → `input()`

**Migration tools**:
- `2to3` automated conversion tool
- `futurize` for gradual migration

### Python 3.6 → 3.12

**Breaking changes**:
- Removed `asyncio.coroutine` decorator
- Collections ABC moved from `collections` to `collections.abc`
- `distutils` removed (use `setuptools`)
- Type hint changes

### JavaScript ES5 → ES6+

**Breaking changes**:
- `var` → `let`/`const`
- Function expressions → arrow functions
- Callbacks → Promises/async-await
- `require()` → `import`/`export`

### Java 8 → Java 17

**Breaking changes**:
- Removed Java EE modules (JAXB, JAX-WS)
- Strong encapsulation of JDK internals
- Removed Nashorn JavaScript engine
- Security manager deprecation

## Framework Migrations

### React 16 → React 18

**Breaking changes**:
- Automatic batching changes
- `ReactDOM.render()` → `ReactDOM.createRoot()`
- Concurrent features
- Strict mode changes
- `useEffect` timing changes

**Migration strategy**:
1. Update to React 18
2. Replace render calls
3. Test for concurrent rendering issues
4. Adopt new features gradually

### Angular.js → Angular

**Breaking changes**:
- Complete rewrite (TypeScript-based)
- Component-based architecture
- Dependency injection changes
- Template syntax changes

**Migration strategy**:
1. Use `ngUpgrade` for hybrid approach
2. Migrate component by component
3. Update services and dependency injection
4. Rewrite templates

### Django 2.2 → Django 4.2

**Breaking changes**:
- `django.conf.urls.url()` → `django.urls.re_path()`
- `USE_L10N` setting removed
- `django.utils.translation.ugettext*` → `gettext*`
- `Signal.disconnect()` return value changed

### Express 4 → Express 5

**Breaking changes**:
- `app.del()` → `app.delete()`
- `req.param()` removed
- Path route matching changes
- Promise rejection handling

## Library/Dependency Updates

### jQuery 1.x → 3.x

**Breaking changes**:
- `.load()`, `.unload()`, `.error()` removed
- `.bind()`, `.unbind()` → `.on()`, `.off()`
- `.size()` → `.length`
- AJAX changes

### Lodash 3 → 4

**Breaking changes**:
- Method chaining changes
- `_.pluck()` → `_.map()`
- Removed `_.where()`, `_.findWhere()`
- Iteratee argument changes

### Moment.js → Day.js/date-fns

**Breaking changes**:
- Complete API change
- Immutability differences
- Plugin system changes
- Timezone handling

## Database Migrations

### MySQL 5.7 → 8.0

**Breaking changes**:
- Reserved keywords added
- Authentication plugin changes
- SQL mode defaults changed
- `GROUP BY` behavior

### PostgreSQL 9.6 → 15

**Breaking changes**:
- `WITH OIDS` removed
- `pg_stat_activity` column changes
- Function signature changes
- Permission changes

## Build Tool Migrations

### Webpack 4 → 5

**Breaking changes**:
- Node.js polyfills removed
- `file-loader`, `url-loader` → Asset Modules
- Cache configuration changes
- Module federation

### Gulp 3 → 4

**Breaking changes**:
- Task system rewrite
- Series/parallel execution
- `gulp.task()` signature changes

## Testing Framework Migrations

### Jest 26 → 29

**Breaking changes**:
- `done` callback changes
- Timer mock changes
- Snapshot format changes
- `testEnvironment` defaults

### Mocha 8 → 10

**Breaking changes**:
- Node.js version requirements
- `--no-warnings` flag changes
- Reporter API changes

## Migration Patterns

### Incremental Migration

1. Update dependencies one at a time
2. Run tests after each update
3. Fix breaking changes immediately
4. Commit working state

### Big Bang Migration

1. Update all dependencies at once
2. Identify all breaking changes
3. Fix systematically
4. Extensive testing

### Parallel Migration (Strangler Pattern)

1. Run old and new versions side by side
2. Gradually route traffic to new version
3. Deprecate old version when complete

## Common Migration Challenges

### Deprecated API Usage

**Detection**:
- Compiler/interpreter warnings
- Linter rules
- Deprecation notices in logs

**Resolution**:
- Find replacement API in migration guide
- Update all usages
- Test thoroughly

### Breaking Type Changes

**Detection**:
- Type checker errors
- Runtime type errors
- Test failures

**Resolution**:
- Update type annotations
- Add type conversions
- Update interfaces

### Changed Default Behavior

**Detection**:
- Tests pass but behavior differs
- Integration test failures
- User-reported issues

**Resolution**:
- Read migration guide carefully
- Explicitly set previous defaults
- Update code to new patterns

### Removed Features

**Detection**:
- Import errors
- Undefined function/method errors
- Module not found errors

**Resolution**:
- Find alternative in new version
- Implement workaround
- Use compatibility library

### Performance Regressions

**Detection**:
- Slower test execution
- Increased memory usage
- Timeout failures

**Resolution**:
- Profile performance
- Optimize hot paths
- Update configuration

## Migration Verification

### Test Coverage Requirements

- All existing tests must pass
- No new test failures
- Same test coverage percentage
- Integration tests pass

### Behavioral Verification

- Same inputs produce same outputs
- Error handling unchanged
- Edge cases handled identically
- Performance within acceptable range

### Compatibility Checks

- Dependencies compatible
- Build succeeds
- No deprecation warnings (or documented)
- Documentation updated
