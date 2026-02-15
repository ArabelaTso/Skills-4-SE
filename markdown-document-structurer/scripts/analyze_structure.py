#!/usr/bin/env python3
"""
Analyze markdown document structure and identify issues.

Usage:
    python analyze_structure.py <markdown_file>
"""

import re
import sys
from pathlib import Path
from typing import List, Dict, Tuple


class MarkdownAnalyzer:
    def __init__(self, file_path: str):
        self.file_path = Path(file_path)
        self.content = self.file_path.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')

    def extract_headings(self) -> List[Tuple[int, str, int]]:
        """Extract all headings with their levels and line numbers."""
        headings = []
        for i, line in enumerate(self.lines, 1):
            match = re.match(r'^(#{1,6})\s+(.+)$', line)
            if match:
                level = len(match.group(1))
                text = match.group(2).strip()
                headings.append((level, text, i))
        return headings

    def check_heading_hierarchy(self) -> List[str]:
        """Check for heading hierarchy issues."""
        issues = []
        headings = self.extract_headings()

        if not headings:
            return ["No headings found in document"]

        # Check for multiple h1s
        h1_count = sum(1 for level, _, _ in headings if level == 1)
        if h1_count > 1:
            issues.append(f"Multiple h1 headings found ({h1_count}). Should have only one.")
        elif h1_count == 0:
            issues.append("No h1 heading found. Document should start with h1.")

        # Check for skipped levels
        prev_level = 0
        for level, text, line_num in headings:
            if prev_level > 0 and level > prev_level + 1:
                issues.append(
                    f"Line {line_num}: Skipped heading level (h{prev_level} → h{level}). "
                    f"Should be h{prev_level + 1}."
                )
            prev_level = level

        return issues

    def check_toc(self) -> Dict[str, any]:
        """Check for table of contents."""
        toc_pattern = re.compile(r'##\s+Table of Contents', re.IGNORECASE)
        has_toc = any(toc_pattern.search(line) for line in self.lines)

        headings = self.extract_headings()
        section_count = sum(1 for level, _, _ in headings if level == 2)

        return {
            'has_toc': has_toc,
            'needs_toc': section_count >= 3,
            'section_count': section_count
        }

    def check_code_blocks(self) -> List[str]:
        """Check code block formatting."""
        issues = []
        in_code_block = False
        code_block_start = 0

        for i, line in enumerate(self.lines, 1):
            if line.strip().startswith('```'):
                if not in_code_block:
                    in_code_block = True
                    code_block_start = i
                    # Check if language is specified
                    if line.strip() == '```':
                        issues.append(
                            f"Line {i}: Code block without language specification. "
                            "Add language for syntax highlighting."
                        )
                else:
                    in_code_block = False

        if in_code_block:
            issues.append(f"Line {code_block_start}: Unclosed code block")

        return issues

    def check_list_formatting(self) -> List[str]:
        """Check list formatting consistency."""
        issues = []
        list_markers = set()

        for i, line in enumerate(self.lines, 1):
            # Check unordered list markers
            match = re.match(r'^(\s*)([-*+])\s', line)
            if match:
                marker = match.group(2)
                list_markers.add(marker)

        if len(list_markers) > 1:
            issues.append(
                f"Inconsistent list markers found: {', '.join(sorted(list_markers))}. "
                "Use '-' consistently for unordered lists."
            )

        return issues

    def check_emphasis(self) -> List[str]:
        """Check emphasis formatting consistency."""
        issues = []

        # Count different emphasis styles
        bold_asterisk = len(re.findall(r'\*\*[^*]+\*\*', self.content))
        bold_underscore = len(re.findall(r'__[^_]+__', self.content))
        italic_asterisk = len(re.findall(r'(?<!\*)\*(?!\*)([^*]+)\*(?!\*)', self.content))
        italic_underscore = len(re.findall(r'(?<!_)_(?!_)([^_]+)_(?!_)', self.content))

        if bold_asterisk > 0 and bold_underscore > 0:
            issues.append(
                f"Mixed bold styles: ** ({bold_asterisk}) and __ ({bold_underscore}). "
                "Use ** consistently."
            )

        if italic_asterisk > 0 and italic_underscore > 0:
            issues.append(
                f"Mixed italic styles: * ({italic_asterisk}) and _ ({italic_underscore}). "
                "Use * consistently."
            )

        return issues

    def detect_duplicate_sections(self) -> List[str]:
        """Detect potential duplicate sections."""
        issues = []
        headings = self.extract_headings()
        heading_texts = {}

        for level, text, line_num in headings:
            text_lower = text.lower()
            if text_lower in heading_texts:
                issues.append(
                    f"Duplicate section heading '{text}' at lines "
                    f"{heading_texts[text_lower]} and {line_num}"
                )
            else:
                heading_texts[text_lower] = line_num

        return issues

    def analyze(self) -> Dict:
        """Perform full analysis."""
        toc_info = self.check_toc()

        return {
            'heading_issues': self.check_heading_hierarchy(),
            'toc_status': toc_info,
            'code_block_issues': self.check_code_blocks(),
            'list_issues': self.check_list_formatting(),
            'emphasis_issues': self.check_emphasis(),
            'duplicate_sections': self.detect_duplicate_sections()
        }

    def generate_report(self) -> str:
        """Generate analysis report."""
        analysis = self.analyze()

        report = []
        report.append("=" * 60)
        report.append("MARKDOWN STRUCTURE ANALYSIS")
        report.append("=" * 60)
        report.append(f"\nFile: {self.file_path}")

        # Heading issues
        if analysis['heading_issues']:
            report.append("\n📋 Heading Hierarchy Issues:")
            for issue in analysis['heading_issues']:
                report.append(f"  ⚠️  {issue}")
        else:
            report.append("\n✅ Heading hierarchy is correct")

        # TOC status
        toc = analysis['toc_status']
        report.append(f"\n📑 Table of Contents:")
        report.append(f"  Has TOC: {'Yes' if toc['has_toc'] else 'No'}")
        report.append(f"  Sections: {toc['section_count']}")
        if toc['needs_toc'] and not toc['has_toc']:
            report.append(f"  ⚠️  Document has {toc['section_count']} sections. Consider adding TOC.")

        # Code block issues
        if analysis['code_block_issues']:
            report.append("\n💻 Code Block Issues:")
            for issue in analysis['code_block_issues']:
                report.append(f"  ⚠️  {issue}")
        else:
            report.append("\n✅ Code blocks are properly formatted")

        # List issues
        if analysis['list_issues']:
            report.append("\n📝 List Formatting Issues:")
            for issue in analysis['list_issues']:
                report.append(f"  ⚠️  {issue}")
        else:
            report.append("\n✅ List formatting is consistent")

        # Emphasis issues
        if analysis['emphasis_issues']:
            report.append("\n✨ Emphasis Formatting Issues:")
            for issue in analysis['emphasis_issues']:
                report.append(f"  ⚠️  {issue}")
        else:
            report.append("\n✅ Emphasis formatting is consistent")

        # Duplicate sections
        if analysis['duplicate_sections']:
            report.append("\n🔄 Duplicate Sections:")
            for issue in analysis['duplicate_sections']:
                report.append(f"  ⚠️  {issue}")
        else:
            report.append("\n✅ No duplicate sections found")

        return "\n".join(report)


def main():
    if len(sys.argv) != 2:
        print("Usage: python analyze_structure.py <markdown_file>")
        sys.exit(1)

    file_path = sys.argv[1]

    if not Path(file_path).exists():
        print(f"Error: File '{file_path}' not found")
        sys.exit(1)

    analyzer = MarkdownAnalyzer(file_path)
    print(analyzer.generate_report())


if __name__ == '__main__':
    main()
