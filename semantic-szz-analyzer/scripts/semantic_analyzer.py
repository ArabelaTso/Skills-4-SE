#!/usr/bin/env python3
"""
Semantic Analyzer - Core module for computing semantic similarity between code versions.
Uses AST, control-flow, and data-flow analysis to distinguish semantic changes from refactorings.
"""

import ast
import subprocess
from pathlib import Path
from typing import Dict, List, Set, Tuple, Optional
import difflib


class SemanticAnalyzer:
    """Analyzes semantic differences between code versions."""

    # Similarity thresholds
    CFG_THRESHOLD = 0.7   # Control-flow similarity
    DFG_THRESHOLD = 0.6   # Data-flow similarity
    AST_THRESHOLD = 0.8   # AST structural similarity

    def __init__(self, threshold: float = 0.7):
        self.threshold = threshold

    def get_file_content(self, repo_path: Path, file_path: str, commit: str) -> Optional[str]:
        """Get file content at a specific commit."""
        cmd = ['git', '-C', str(repo_path), 'show', f'{commit}:{file_path}']
        result = subprocess.run(cmd, capture_output=True, text=True)

        if result.returncode != 0:
            return None
        return result.stdout

    def parse_python_ast(self, code: str) -> Optional[ast.AST]:
        """Parse Python code into AST."""
        try:
            return ast.parse(code)
        except SyntaxError:
            return None

    def compute_ast_similarity(self, code1: str, code2: str) -> float:
        """Compute structural similarity between two code snippets using AST."""
        tree1 = self.parse_python_ast(code1)
        tree2 = self.parse_python_ast(code2)

        if tree1 is None or tree2 is None:
            # Fallback to text-based similarity
            return difflib.SequenceMatcher(None, code1, code2).ratio()

        # Extract AST node types and structure
        nodes1 = self._extract_ast_structure(tree1)
        nodes2 = self._extract_ast_structure(tree2)

        # Compute similarity based on node sequences
        return difflib.SequenceMatcher(None, nodes1, nodes2).ratio()

    def _extract_ast_structure(self, tree: ast.AST) -> List[str]:
        """Extract AST node type sequence."""
        nodes = []
        for node in ast.walk(tree):
            nodes.append(type(node).__name__)
        return nodes

    def compute_cfg_similarity(self, code1: str, code2: str) -> float:
        """Compute control-flow graph similarity."""
        cfg1 = self._extract_control_flow(code1)
        cfg2 = self._extract_control_flow(code2)

        if not cfg1 or not cfg2:
            return 0.0

        # Compare control flow patterns
        common = len(cfg1.intersection(cfg2))
        total = len(cfg1.union(cfg2))

        return common / total if total > 0 else 0.0

    def _extract_control_flow(self, code: str) -> Set[str]:
        """Extract control flow patterns from code."""
        tree = self.parse_python_ast(code)
        if tree is None:
            return set()

        patterns = set()
        for node in ast.walk(tree):
            if isinstance(node, (ast.If, ast.While, ast.For)):
                patterns.add(f"{type(node).__name__}")
            elif isinstance(node, ast.FunctionDef):
                patterns.add(f"Function:{node.name}")
            elif isinstance(node, ast.Return):
                patterns.add("Return")

        return patterns

    def compute_dfg_similarity(self, code1: str, code2: str) -> float:
        """Compute data-flow graph similarity based on variable usage."""
        vars1 = self._extract_variable_usage(code1)
        vars2 = self._extract_variable_usage(code2)

        if not vars1 or not vars2:
            return 0.0

        # Compare variable usage patterns
        common = len(vars1.intersection(vars2))
        total = len(vars1.union(vars2))

        return common / total if total > 0 else 0.0

    def _extract_variable_usage(self, code: str) -> Set[str]:
        """Extract variable names and usage patterns."""
        tree = self.parse_python_ast(code)
        if tree is None:
            return set()

        variables = set()
        for node in ast.walk(tree):
            if isinstance(node, ast.Name):
                variables.add(node.id)
            elif isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name):
                        variables.add(f"assign:{target.id}")

        return variables

    def is_refactoring(self, code1: str, code2: str) -> bool:
        """Determine if changes are likely refactoring rather than semantic changes."""
        # High AST similarity suggests structural preservation
        ast_sim = self.compute_ast_similarity(code1, code2)

        # High CFG similarity suggests control flow preservation
        cfg_sim = self.compute_cfg_similarity(code1, code2)

        # Check if it's just formatting/whitespace changes
        normalized1 = self._normalize_code(code1)
        normalized2 = self._normalize_code(code2)

        if normalized1 == normalized2:
            return True

        # If both AST and CFG are highly similar, likely refactoring
        if ast_sim > self.AST_THRESHOLD and cfg_sim > self.CFG_THRESHOLD:
            return True

        return False

    def _normalize_code(self, code: str) -> str:
        """Normalize code by removing whitespace and comments."""
        lines = []
        for line in code.split('\n'):
            # Remove comments
            if '#' in line:
                line = line[:line.index('#')]
            # Remove leading/trailing whitespace
            line = line.strip()
            if line:
                lines.append(line)
        return '\n'.join(lines)

    def classify_change_type(self, code1: str, code2: str) -> str:
        """Classify the type of semantic change."""
        cfg_sim = self.compute_cfg_similarity(code1, code2)
        dfg_sim = self.compute_dfg_similarity(code1, code2)

        if cfg_sim < 0.5:
            return "logic_modification"
        elif dfg_sim < 0.5:
            return "data_flow_change"
        elif self.is_refactoring(code1, code2):
            return "refactoring"
        else:
            return "minor_semantic_change"

    def analyze_commit_pair(self, repo_path: Path, file_path: str,
                           candidate_commit: str, fix_commit: str) -> Dict:
        """Analyze a candidate commit against the fix commit."""
        # Get file content at both commits
        content_candidate = self.get_file_content(repo_path, file_path, candidate_commit)
        content_fix = self.get_file_content(repo_path, file_path, fix_commit)

        if content_candidate is None or content_fix is None:
            return {
                'is_bug_introducing': False,
                'confidence': 0.0,
                'semantic_change_type': 'unknown',
                'explanation': 'Could not retrieve file content'
            }

        # Compute similarity scores
        ast_sim = self.compute_ast_similarity(content_candidate, content_fix)
        cfg_sim = self.compute_cfg_similarity(content_candidate, content_fix)
        dfg_sim = self.compute_dfg_similarity(content_candidate, content_fix)

        # Check if it's a refactoring
        if self.is_refactoring(content_candidate, content_fix):
            return {
                'is_bug_introducing': False,
                'confidence': 0.0,
                'semantic_change_type': 'refactoring',
                'explanation': 'Changes appear to be refactoring without semantic impact',
                'similarity_scores': {
                    'ast': ast_sim,
                    'cfg': cfg_sim,
                    'dfg': dfg_sim
                }
            }

        # Classify change type
        change_type = self.classify_change_type(content_candidate, content_fix)

        # Compute confidence based on semantic change magnitude
        # Lower similarity = higher confidence it's bug-introducing
        semantic_change = 1.0 - ((ast_sim + cfg_sim + dfg_sim) / 3.0)
        confidence = semantic_change

        is_bug_introducing = confidence >= (1.0 - self.threshold)

        explanation = self._generate_explanation(change_type, confidence, ast_sim, cfg_sim, dfg_sim)

        return {
            'is_bug_introducing': is_bug_introducing,
            'confidence': confidence,
            'semantic_change_type': change_type,
            'explanation': explanation,
            'similarity_scores': {
                'ast': ast_sim,
                'cfg': cfg_sim,
                'dfg': dfg_sim
            }
        }

    def _generate_explanation(self, change_type: str, confidence: float,
                             ast_sim: float, cfg_sim: float, dfg_sim: float) -> str:
        """Generate human-readable explanation."""
        explanations = {
            'logic_modification': f'Significant control-flow changes detected (CFG similarity: {cfg_sim:.2f}). '
                                 f'This indicates modifications to conditional logic or program structure.',
            'data_flow_change': f'Data-flow patterns changed (DFG similarity: {dfg_sim:.2f}). '
                               f'This suggests modifications to variable usage or data dependencies.',
            'minor_semantic_change': f'Minor semantic changes detected. AST similarity: {ast_sim:.2f}, '
                                    f'CFG similarity: {cfg_sim:.2f}.',
            'refactoring': 'Code restructuring without significant semantic changes.',
            'unknown': 'Unable to classify change type.'
        }

        base_explanation = explanations.get(change_type, explanations['unknown'])
        return f"{base_explanation} Confidence: {confidence:.2f}"
