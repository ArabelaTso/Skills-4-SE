#!/usr/bin/env python3
"""
Language-specific parsers for C/C++, Java, and Python.
"""

import ast
import re


class LanguageParser:
    """Multi-language parser for extracting AST from source code."""

    def parse_file(self, file_path, language):
        """
        Parse source file and return AST.

        Args:
            file_path: Path to source file
            language: Language identifier ('c', 'cpp', 'java', 'python')

        Returns:
            AST representation (format depends on language)
        """
        with open(file_path, 'r', encoding='utf-8') as f:
            source_code = f.read()

        if language == 'python':
            return self._parse_python(source_code)
        elif language in ['c', 'cpp']:
            return self._parse_c_cpp(source_code)
        elif language == 'java':
            return self._parse_java(source_code)
        else:
            raise ValueError(f"Unsupported language: {language}")

    def _parse_python(self, source_code):
        """Parse Python code using built-in ast module."""
        try:
            tree = ast.parse(source_code)
            return self._convert_python_ast(tree)
        except SyntaxError as e:
            print(f"[!] Python syntax error: {e}")
            return None

    def _convert_python_ast(self, tree):
        """Convert Python AST to simplified representation."""
        result = {
            'type': 'module',
            'functions': [],
            'classes': []
        }

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                func_info = {
                    'name': node.name,
                    'args': [arg.arg for arg in node.args.args],
                    'body': self._extract_python_body(node.body),
                    'lineno': node.lineno
                }
                result['functions'].append(func_info)
            elif isinstance(node, ast.ClassDef):
                class_info = {
                    'name': node.name,
                    'methods': []
                }
                result['classes'].append(class_info)

        return result

    def _extract_python_body(self, body):
        """Extract control flow from Python function body."""
        statements = []
        for stmt in body:
            stmt_info = self._analyze_python_statement(stmt)
            if stmt_info:
                statements.append(stmt_info)
        return statements

    def _analyze_python_statement(self, stmt):
        """Analyze a single Python statement."""
        if isinstance(stmt, ast.If):
            return {
                'type': 'if',
                'condition': ast.unparse(stmt.test),
                'then_body': self._extract_python_body(stmt.body),
                'else_body': self._extract_python_body(stmt.orelse) if stmt.orelse else []
            }
        elif isinstance(stmt, ast.While):
            return {
                'type': 'while',
                'condition': ast.unparse(stmt.test),
                'body': self._extract_python_body(stmt.body)
            }
        elif isinstance(stmt, ast.For):
            return {
                'type': 'for',
                'target': ast.unparse(stmt.target),
                'iter': ast.unparse(stmt.iter),
                'body': self._extract_python_body(stmt.body)
            }
        elif isinstance(stmt, ast.Return):
            return {
                'type': 'return',
                'value': ast.unparse(stmt.value) if stmt.value else None
            }
        elif isinstance(stmt, ast.Assign):
            return {
                'type': 'assign',
                'targets': [ast.unparse(t) for t in stmt.targets],
                'value': ast.unparse(stmt.value)
            }
        else:
            return {
                'type': 'other',
                'code': ast.unparse(stmt)
            }

    def _parse_c_cpp(self, source_code):
        """
        Parse C/C++ code.

        Note: This is a simplified parser. For production use, consider:
        - pycparser for C
        - libclang Python bindings for C/C++
        """
        # Simplified regex-based parsing for demonstration
        result = {
            'type': 'c_module',
            'functions': []
        }

        # Extract function definitions (simplified)
        func_pattern = r'(\w+)\s+(\w+)\s*\([^)]*\)\s*\{'
        matches = re.finditer(func_pattern, source_code)

        for match in matches:
            return_type = match.group(1)
            func_name = match.group(2)

            # Find function body (simplified - doesn't handle nested braces properly)
            start = match.end()
            brace_count = 1
            end = start

            for i in range(start, len(source_code)):
                if source_code[i] == '{':
                    brace_count += 1
                elif source_code[i] == '}':
                    brace_count -= 1
                    if brace_count == 0:
                        end = i
                        break

            body = source_code[start:end]

            func_info = {
                'name': func_name,
                'return_type': return_type,
                'body': self._extract_c_control_flow(body)
            }
            result['functions'].append(func_info)

        return result

    def _extract_c_control_flow(self, body):
        """Extract control flow structures from C/C++ code."""
        statements = []

        # Detect if statements
        if_pattern = r'if\s*\([^)]+\)'
        for match in re.finditer(if_pattern, body):
            statements.append({
                'type': 'if',
                'condition': match.group(0),
                'position': match.start()
            })

        # Detect while loops
        while_pattern = r'while\s*\([^)]+\)'
        for match in re.finditer(while_pattern, body):
            statements.append({
                'type': 'while',
                'condition': match.group(0),
                'position': match.start()
            })

        # Detect for loops
        for_pattern = r'for\s*\([^)]+\)'
        for match in re.finditer(for_pattern, body):
            statements.append({
                'type': 'for',
                'condition': match.group(0),
                'position': match.start()
            })

        return sorted(statements, key=lambda x: x['position'])

    def _parse_java(self, source_code):
        """
        Parse Java code.

        Note: This is a simplified parser. For production use, consider:
        - javalang library
        - ANTLR with Java grammar
        """
        result = {
            'type': 'java_module',
            'classes': []
        }

        # Extract class definitions (simplified)
        class_pattern = r'class\s+(\w+)'
        class_matches = re.finditer(class_pattern, source_code)

        for class_match in class_matches:
            class_name = class_match.group(1)

            # Extract methods (simplified)
            method_pattern = r'(public|private|protected)?\s*(\w+)\s+(\w+)\s*\([^)]*\)\s*\{'
            method_matches = re.finditer(method_pattern, source_code)

            methods = []
            for method_match in method_matches:
                visibility = method_match.group(1) or 'default'
                return_type = method_match.group(2)
                method_name = method_match.group(3)

                methods.append({
                    'name': method_name,
                    'visibility': visibility,
                    'return_type': return_type
                })

            result['classes'].append({
                'name': class_name,
                'methods': methods
            })

        return result
