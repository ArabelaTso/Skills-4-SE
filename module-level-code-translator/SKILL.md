---
name: module-level-code-translator
description: Translate source code between programming languages at function, class, and module levels while preserving behavior and generating verification tests. Use when translating code from one language to another (e.g., "translate this Python module to JavaScript", "convert this Java class to C#", "port this code to Go and generate tests"), migrating codebases between languages, or creating equivalent implementations across different technology stacks. Handles idiom adaptation, standard library mappings, and test generation.
---

# Module-Level Code Translator

Translate source code between programming languages while preserving behavior, adapting idioms, and generating verification tests.

## Translation Workflow

Follow this sequential process for code translation:

### 1. Analyze Source Code

Before translating, thoroughly understand the source code:

- **Identify scope**: Determine if translating functions, classes, or entire modules
- **Map dependencies**: List all imports, external libraries, and dependencies
- **Understand behavior**: Identify core logic, algorithms, and expected behavior
- **Note language-specific features**: Identify features that require special handling (decorators, generators, async/await, etc.)
- **Extract test cases**: If existing tests are available, analyze them to understand expected behavior

### 2. Plan Translation Strategy

Create a translation plan before writing code:

- **Map standard libraries**: Identify equivalent libraries in target language (see references/stdlib_mappings.md)
- **Adapt idioms**: Plan how to translate language-specific patterns (see references/language_mappings.md)
- **Handle type systems**: Plan type annotations/declarations if moving between typed/untyped languages
- **Identify testing framework**: Choose appropriate testing framework for target language (see references/testing_frameworks.md)
- **List transformations**: Document major transformations needed (e.g., class → struct, decorator → annotation)

### 3. Translate Code

Implement the translation following target language conventions:

**Core principles:**
- Preserve original behavior exactly
- Follow target language idioms and conventions
- Maintain code structure when possible (functions → functions, classes → classes)
- Adapt patterns that don't translate directly (e.g., Python decorators → Java annotations)
- Add appropriate error handling for target language
- Include necessary imports and dependencies

**Common transformations:**

**Python → JavaScript:**
- Classes: Keep class structure, adapt `__init__` to `constructor`
- List comprehensions: Convert to `.map()`, `.filter()`, `.reduce()`
- Decorators: Convert to higher-order functions or use libraries
- Type hints: Convert to TypeScript or JSDoc comments

**Python → Java:**
- Functions: Convert to static methods or instance methods in classes
- Dynamic typing: Add explicit type declarations
- Duck typing: Use interfaces or abstract classes
- List/dict operations: Use Collections framework

**Python → Go:**
- Classes: Convert to structs with methods
- Exceptions: Convert to error return values
- Dynamic features: Use interfaces for polymorphism
- List comprehensions: Use explicit loops

**Java → C#:**
- Naming: Convert PascalCase for methods
- Properties: Use C# property syntax instead of getters/setters
- Collections: Map to .NET collections
- Annotations: Convert to C# attributes

### 4. Generate Tests

Create comprehensive tests to verify translation correctness:

**Test generation approach:**
1. Use appropriate test template from `assets/` directory
2. Port existing tests if available in source code
3. Create new tests covering:
   - Basic functionality for each function/method
   - Edge cases (empty inputs, null values, boundary conditions)
   - Error handling and exceptions
   - Integration between components

**Test equivalence:**
- Ensure tests verify the same behavior as original code
- Use equivalent assertions (see references/testing_frameworks.md)
- Maintain test structure and organization
- Add setup/teardown as needed for target framework

### 5. Create Translation Summary

Document the translation with a summary including:

**Mappings:**
- List of source → target function/class/module mappings
- Standard library equivalences used
- External dependencies and their target equivalents

**Transformations:**
- Major structural changes (e.g., decorator → annotation)
- Idiom adaptations (e.g., list comprehension → map/filter)
- Type system changes (dynamic → static typing)

**Verification notes:**
- Test coverage summary
- Known limitations or differences
- Manual verification steps if needed

## Output Format

Provide the translation in this structure:

```
## Translated Code

[Target language code with appropriate file structure]

## Tests

[Test code using target language testing framework]

## Translation Summary

### Mappings
- SourceClass → TargetClass
- source_function() → targetFunction()
- source_module → target.package

### Standard Library Equivalences
- source.lib.function → target.lib.function

### Transformations
- [Description of major transformations]

### Verification
- [Test coverage and verification notes]
```

## Language-Specific Considerations

### Python → JavaScript/TypeScript
- Convert snake_case to camelCase
- Handle async/await (similar syntax)
- Map list/dict operations to array/object methods
- Consider using TypeScript for type safety

### Python → Java
- Add explicit type declarations throughout
- Convert modules to packages with proper structure
- Use appropriate Java collections (ArrayList, HashMap, etc.)
- Handle checked exceptions

### Python → Go
- Convert classes to structs with receiver methods
- Replace exceptions with error return values
- Use goroutines for concurrency (if applicable)
- Follow Go naming conventions (exported vs unexported)

### Java → C#
- Convert naming conventions (PascalCase methods)
- Use C# properties instead of getters/setters
- Map Java collections to .NET equivalents
- Convert annotations to attributes

### JavaScript → Python
- Convert camelCase to snake_case
- Handle promises/async with Python async/await
- Map array methods to list comprehensions or loops
- Add type hints if using modern Python

## Resources

### references/
- **language_mappings.md**: Common idiom mappings between languages
- **stdlib_mappings.md**: Standard library equivalences across languages
- **testing_frameworks.md**: Testing framework mappings and patterns

### assets/
Test templates for common target languages:
- **test_template_python.py**: pytest template
- **test_template_javascript.js**: Jest template
- **test_template_java.java**: JUnit 5 template
- **test_template_go.go**: Go testing template

Use these templates as starting points for generated tests.

## Best Practices

1. **Preserve behavior first**: Correctness is more important than idiomatic code
2. **Follow target conventions**: Use target language's naming, structure, and patterns
3. **Test thoroughly**: Generate comprehensive tests to verify equivalence
4. **Document differences**: Note any behavioral differences or limitations
5. **Handle edge cases**: Ensure edge cases are properly translated
6. **Consider performance**: Be aware of performance implications of translations
7. **Use appropriate types**: Leverage target language's type system effectively
8. **Maintain readability**: Keep code readable and maintainable in target language
