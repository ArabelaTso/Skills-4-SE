#!/usr/bin/env python3
"""
Generate static skills-data.json for GitHub Pages deployment.

This script scans the repository for all SKILL.md files and creates
a static JSON file containing all skills metadata.
"""

import os
import json
import yaml
from pathlib import Path
from datetime import datetime

# Paths
SCRIPT_DIR = Path(__file__).parent.resolve()
REPO_ROOT = SCRIPT_DIR.parent.resolve()
OUTPUT_FILE = SCRIPT_DIR / 'frontend' / 'skills-data.json'
TRANSLATIONS_FILE = SCRIPT_DIR / 'skills-translations-zh.json'

print(f"Script directory: {SCRIPT_DIR}")
print(f"Repository root: {REPO_ROOT}")
print(f"Output file: {OUTPUT_FILE}")
print(f"Translations file: {TRANSLATIONS_FILE}")

# Directories to exclude
EXCLUDED_DIRS = ['skill-manager', 'node_modules', 'skill-creator', '.git', 'awesome-claude-skills', '_report']

# Additional directories to include
ADDITIONAL_SKILL_DIRS = []

# Category mapping (from app.js)
CATEGORY_MAP = {
    'code-generation': ['function-class-generator', 'module-component-generator', 'template-code-generator',
                        'specification-driven-generation', 'test-driven-generation', 'incremental-python-programmer',
                        'incremental-java-programmer', 'frontend-design', 'pseudocode-extractor'],
    'testing': ['unit-test-generator', 'integration-test-generator', 'java-test-updater', 'flaky-test-detector',
                'test-oracle-generator', 'edge-case-generator', 'directed-test-input-generator',
                'fuzzing-input-generator', 'test-suite-prioritizer', 'coverage-enhancer',
                'test-case-documentation', 'python-test-updater', 'req-to-test',
                'test-app-automation', 'webapp-testing', 'webapp-testing-anthropics',
                'python-regression-test-generator', 'java-regression-test-generator',
                'mocking-test-generator', 'test-guided-bug-detector'],
    'documentation': ['api-documentation-generator', 'code-comment-generator', 'markdown-document-structurer',
                      'readme-generator', 'change-log-generator', 'code-change-summarizer', 'release-notes-writer',
                      'legacy-code-summarizer', 'python-repo-quickstart', 'error-explanation-generator',
                      'confluence-automation'],
    'quality': ['code-review-assistant', 'code-smell-detector', 'design-smell-detector', 'code-optimizer',
                'dead-code-eliminator', 'technical-debt-analyzer', 'code-pattern-extractor',
                'code-search-assistant', 'component-boundary-identifier',
                'sentry-automation', 'datadog-automation', 'bugsnag-automation', 'bugbug-automation',
                'bugherd-automation', 'pagerduty-automation',
                'static-bug-detector', 'semantic-bug-detector', 'static-vulnerability-detector',
                'vulnerability-pattern-matcher', 'exploitability-analyzer', 'vulnerability-root-cause-analyzer',
                'security-patch-advisor', 'code-summarizer'],
    'requirements': ['requirement-summarizer', 'requirement-coverage-checker', 'requirement-comparison-reporter',
                     'ambiguity-detector', 'scenario-generator', 'specification-generator', 'nl-to-constraints',
                     'jira-automation', 'linear-automation'],
    'devops': ['ci-pipeline-synthesizer', 'cd-pipeline-generator', 'containerization-assistant',
               'environment-setup-assistant', 'rollback-strategy-advisor',
               'circleci-automation', 'buildkite-automation', 'appveyor-automation', 'appcircle-automation',
               'docker-hub-automation', 'docker_hub-automation', 'vercel-automation',
               'digital-ocean-automation', 'cloudflare-automation', 'cloudflare-api-key-automation',
               'cloudflare-browser-rendering-automation', 'npm-automation',
               'github-automation', 'gitlab-automation', 'bitbucket-automation', 'sourcegraph-automation',
               'slack-automation', 'slackbot-automation', 'discord-automation', 'discordbot-automation',
               'slack-gif-creator', 'supabase-automation', 'hookdeck-automation'],
    'debugging': ['bug-localization', 'bug-to-patch-generator', 'runtime-error-explainer',
                  'regression-root-cause-analyzer', 'conflict-analyzer', 'counterexample-debugger',
                  'issue-report-generator'],
    'verification': ['acsl-annotation-assistant', 'assertion-synthesizer', 'invariant-inference',
                     'static-reasoning-verifier', 'symbolic-execution-assistant', 'counterexample-generator',
                     'counterexample-explainer', 'formal-spec-generator', 'program-to-model-extractor',
                     'imperative-to-coq-model-extractor', 'python-to-dafny-translator', 'python-to-lean4-translator',
                     'c-cpp-to-lean4-translator', 'cpp-to-dafny-translator', 'program-correctness-prover',
                     'proof-skeleton-generator', 'proof-failure-explainer', 'proof-refactoring-assistant',
                     'proof-trace-summarizer', 'proof-carrying-code-generator', 'verified-spec-code-mapper',
                     'verification-boundary-reporter', 'verified-pseudocode-extractor',
                     'lemma-discovery-assistant', 'tactic-suggestion-assistant', 'refinement-step-generator',
                     'abstract-domain-explorer', 'abstract-invariant-generator', 'abstract-state-analyzer',
                     'abstract-trace-summarizer', 'control-flow-abstraction-generator',
                     'library-for-proof-advisor', 'requirement-enhancer'],
    'maintenance': ['code-refactoring-assistant', 'deprecated-api-updater', 'code-translation'],
    'architecture': ['api-design-assistant', 'design-pattern-suggestor', 'interface-specification-generator',
                     'interface-contract-verifier'],
    'visualization': ['system-diagram-generator']
}

# Stage mapping based on README.md "Skills by Stages" section
STAGE_MAP = {
    'requirements': [
        # Requirement Analysis
        'ambiguity-detector', 'requirement-summarizer', 'requirement-summary', 'conflict-analyzer',
        # Traceability & Coverage
        'req-to-test', 'nl-to-constraints', 'traceability-matrix-generator', 'requirement-coverage-checker',
        'requirement-comparison-reporter',
        # Documentation & Communication
        'markdown-document-structurer',
        # Scenario & User Story Generation
        'scenario-generator', 'requirement-enhancer'
    ],
    'design': [
        # Architecture & High-Level Design
        'system-diagram-generator', 'design-pattern-suggestor',
        # Interface & API Design
        'api-design-assistant',
        # Design Quality & Analysis
        'design-smell-detector', 'component-boundary-identifier', 'configuration-generator', 'dependency-resolver'
    ],
    'implementation': [
        # Spec-to-Code
        'function-class-generator', 'module-component-generator', 'template-code-generator',
        'incremental-python-programmer', 'incremental-java-programmer',
        # Refactoring & Optimization
        'code-refactoring-assistant', 'code-optimizer', 'dead-code-eliminator', 'code-review-assistant',
        'code-smell-detector', 'technical-debt-analyzer', 'code-pattern-extractor', 'code-search-assistant',
        'code-summarizer', 'pseudocode-extractor', 'module-level-code-translator', 'pseudocode-to-java-code',
        'pseudocode-to-python-code', 'code-instrumentation-generator', 'code-completion-semantic-constraints',
        # TDD & SDD
        'test-driven-generation', 'specification-driven-generation',
        # Multi-Language & Translation
        'code-translation'
    ],
    'testing': [
        # Test Generation
        'unit-test-generator', 'integration-test-generator', 'directed-test-input-generator',
        'fuzzing-input-generator', 'bug-reproduction-test-generator', 'java-regression-test-generator',
        'python-regression-test-generator', 'mocking-test-generator', 'metamorphic-test-generator',
        'counterexample-to-test-generator',
        # Assertion & Oracle Synthesis
        'coverage-enhancer', 'assertion-synthesizer', 'test-oracle-generator',
        # Test Coverage Analysis and Enhancement
        'edge-case-generator', 'test-suite-prioritizer', 'metamorphic-property-extractor',
        # Test Quality & Optimization
        'behavioral-mutation-analyzer', 'mutation-test-suite-optimizer', 'test-deduplicator',
        'java-api-consistency-validator', 'python-api-consistency-validator',
        # Failure Analysis
        'regression-root-cause-analyzer', 'error-explanation-generator', 'runtime-error-explainer',
        'failure-oriented-instrumentation', 'replay-oriented-instrumentation', 'test-guided-bug-detector',
        # Test Documentation & Reporting
        'test-case-documentation',
        # Test Maintenance
        'python-test-updater', 'java-test-updater', 'flaky-test-detector',
        'interval-guided-regression-test-update', 'test-case-reducer',
        # Testing Automation & Tools
        'webapp-testing-anthropics', 'test-app-automation', 'webapp-testing'
    ],
    'verification': [
        # Specification & Annotation
        'interface-specification-generator', 'acsl-annotation-assistant', 'invariant-inference',
        'specification-generator', 'formal-spec-generator', 'abstract-invariant-generator',
        # Abstract Interpretation & Analysis
        'abstract-domain-explorer', 'abstract-state-analyzer', 'abstract-trace-summarizer',
        'control-flow-abstraction-generator',
        # Code Translation for Verification
        'c-cpp-to-lean4-translator', 'cpp-to-dafny-translator', 'python-to-dafny-translator',
        'python-to-lean4-translator', 'imperative-to-coq-model-extractor', 'program-to-model-extractor',
        # Formal Verification
        'static-reasoning-verifier', 'symbolic-execution-assistant', 'program-correctness-prover',
        'proof-carrying-code-generator',
        # Proof Development & Assistance
        'proof-skeleton-generator', 'proof-trace-summarizer', 'proof-refactoring-assistant',
        'lemma-discovery-assistant', 'library-for-proof-advisor', 'tactic-suggestion-assistant',
        'refinement-step-generator',
        # Counterexample Analysis
        'counterexample-generator', 'counterexample-explainer', 'counterexample-debugger',
        'proof-failure-explainer',
        # Verification Reporting & Traceability
        'verification-boundary-reporter', 'verified-pseudocode-extractor', 'verified-spec-code-mapper',
        'interface-contract-verifier', 'behavior-preservation-checker', 'semantic-equivalence-verifier',
        'regression-consistency-checker',
        # TLA+ Specification & Verification
        'program-to-tlaplus-spec-generator', 'tlaplus-spec-generator', 'requirement-to-tlaplus-property-generator',
        'specification-to-temporal-logic-generator', 'tlaplus-model-reduction', 'tlaplus-guided-code-repair',
        'model-guided-code-repair',
        # Hardware Verification
        'rtl-specification-consistency-checker', 'rtl-equivalence-checker', 'rtl-property-inference',
        # Model Checking & Extraction
        'smv-model-extractor'
    ],
    'deployment': [
        # Deployment Preparation
        'environment-setup-assistant', 'containerization-assistant', 'config-consistency-checker',
        'security-sensitive-path-instrumenter', 'taint-instrumentation-assistant', 'critical-interval-security-checker',
        # Continuous Integration & Delivery (CI/CD)
        'ci-pipeline-synthesizer', 'cd-pipeline-generator', 'build-ci-migration-assistant',
        # Cloud & Infrastructure Deployment
        'cloudflare-api-key-automation', 'cloudflare-browser-rendering-automation', 'docker_hub-automation',
        'docker-hub-automation', 'slack-gif-creator', 'codereadr-automation',
        'circleci-automation', 'buildkite-automation', 'appveyor-automation', 'appcircle-automation',
        'vercel-automation', 'digital-ocean-automation', 'cloudflare-automation', 'npm-automation',
        'github-automation', 'gitlab-automation', 'bitbucket-automation', 'sourcegraph-automation',
        'slack-automation', 'slackbot-automation', 'discord-automation', 'discordbot-automation',
        'supabase-automation', 'hookdeck-automation',
        # Deployment Verification & Testing
        'rollback-strategy-advisor',
        # Documentation & Reporting
        'release-notes-writer'
    ],
    'maintenance': [
        # Bug & Issue Handling
        'bug-localization', 'bug-to-patch-generator', 'git-bisect-assistant', 'issue-report-generator',
        'bug-history-summarizer', 'bisect-aware-instrumentation', 'reproduction-trace-instrumenter',
        'state-snapshot-instrumenter', 'trace-collection-assistant', 'szz-bug-identifier',
        'semantic-szz-analyzer', 'code-repair-generation-combo',
        # Security & Vulnerability Management
        'static-bug-detector', 'static-vulnerability-detector', 'vulnerability-pattern-matcher',
        'vulnerability-root-cause-analyzer', 'exploitability-analyzer', 'security-patch-advisor',
        'semantic-bug-detector', 'cve-reachability-analyzer', 'cve-watchlist-action-recommendation-generator',
        'time-aware-dependency-cve-scanner',
        # Legacy & Technical Debt Management
        'legacy-code-summarizer', 'deprecated-api-updater',
        # Version Control & Merge Conflicts
        'conflict-analyzer',
        # Documentation & Knowledge Transfer
        'api-documentation-generator', 'readme-generator', 'python-repo-quickstart',
        'code-comment-generator', 'change-log-generator', 'code-change-summarizer',
        # Continuous Improvement
        'framework-migration-assistant', 'spring-mvc-to-boot-migrator', 'test-guided-migration-assistant',
        'test-guided-debloating', 'smart-mutation-operator-generator', 'multi-version-behavior-comparator',
        'interval-difference-analyzer', 'interval-profiling-performance-analyzer',
        # Monitoring & Error Tracking
        'sentry-automation', 'datadog-automation', 'bugsnag-automation', 'bugbug-automation',
        'bugherd-automation', 'pagerduty-automation',
        # Project Management & Issue Tracking
        'jira-automation', 'linear-automation', 'confluence-automation',
        # Development Tools & Builders
        'artifacts-builder', 'mcp-builder', 'codeinterpreter-automation', 'web-artifacts-builder'
    ]
}

def get_skill_category(skill_name):
    """Get category for a skill"""
    for category, skills in CATEGORY_MAP.items():
        if skill_name in skills:
            return category
    return 'other'

def get_skill_stage(skill_name):
    """Get stage for a skill based on STAGE_MAP"""
    for stage, skills in STAGE_MAP.items():
        if skill_name in skills:
            return stage
    # Default stage based on category if not in STAGE_MAP
    category = get_skill_category(skill_name)
    if category == 'requirements':
        return 'requirements'
    elif category == 'testing':
        return 'testing'
    elif category == 'verification':
        return 'verification'
    elif category == 'devops':
        return 'deployment'
    elif category in ['quality', 'documentation', 'debugging', 'maintenance']:
        return 'maintenance'
    elif category == 'code-generation':
        return 'implementation'
    return None

def load_translations():
    """Load Chinese translations"""
    try:
        with open(TRANSLATIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load translations: {e}")
        return {'skills': {}, 'category_names': {}}

def extract_metadata(skill_path, translations, source_prefix=None, source_dir=None):
    """Extract metadata from SKILL.md file"""
    skill_md = skill_path / 'SKILL.md'
    if not skill_md.exists():
        return None

    try:
        with open(skill_md, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML frontmatter
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = yaml.safe_load(parts[1])

                # Get description (no truncation for full display in tooltips)
                description = frontmatter.get('description', '')

                skill_name = skill_path.name
                # Determine the relative path for installation
                if source_dir:
                    skill_relative_path = f"{source_dir}/{skill_path.name}"
                else:
                    skill_relative_path = skill_path.name

                # Add source prefix if provided (for duplicate names)
                if source_prefix:
                    skill_name = f"{skill_path.name}-{source_prefix}"
                skill_translations = translations['skills'].get(skill_path.name, {})

                return {
                    'name': skill_name,
                    'displayName': frontmatter.get('name', skill_name),
                    'description': description,
                    'category': get_skill_category(skill_name),
                    'stage': get_skill_stage(skill_name),
                    'installed': False,
                    'path': skill_relative_path,
                    'displayName_zh': skill_translations.get('name', frontmatter.get('name', skill_name)),
                    'description_zh': skill_translations.get('description', description)
                }
    except Exception as e:
        print(f"Error reading {skill_path.name}: {e}")

    return None

def scan_skills(translations):
    """Scan repository for all skills"""
    skills = []

    # Scan skills directory
    skills_dir = REPO_ROOT / 'skills'
    if skills_dir.exists() and skills_dir.is_dir():
        for item in skills_dir.iterdir():
            if item.is_dir() and not item.name.startswith('.'):
                # Check if it's a skill directory (has SKILL.md)
                if (item / 'SKILL.md').exists():
                    metadata = extract_metadata(item, translations, source_prefix=None, source_dir='skills')
                    if metadata:
                        skills.append(metadata)

    # Scan additional skill directories
    # Track skill names to detect duplicates
    skill_names = {skill['name'] for skill in skills}

    for additional_dir_name in ADDITIONAL_SKILL_DIRS:
        additional_dir = REPO_ROOT / additional_dir_name
        if additional_dir.exists() and additional_dir.is_dir():
            print(f"Scanning additional directory: {additional_dir_name}")
            for item in additional_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Check if it's a skill directory (has SKILL.md)
                    if (item / 'SKILL.md').exists():
                        # Check for duplicate names and add suffix if needed
                        source_prefix = None

                        metadata = extract_metadata(item, translations, source_prefix, additional_dir_name)
                        if metadata:
                            skills.append(metadata)
                            skill_names.add(metadata['name'])

    # Sort by name
    skills.sort(key=lambda x: x['name'])

    return skills

def scan_skill_packs():
    """Scan skill-packs directory for skill packs"""
    packs = []
    packs_dir = REPO_ROOT / 'skill-packs'

    if not packs_dir.exists():
        return packs

    # Skill pack metadata mapping
    pack_metadata = {
        'bug-fixing-suite': {
            'name': 'Bug Fixing Suite',
            'name_zh': '错误修复套件',
            'description': 'Comprehensive toolkit for bug detection, localization, analysis, and automated repair',
            'description_zh': '用于错误检测、定位、分析和自动修复的综合工具包',
            'icon': '🐛',
            'difficulty': 'Intermediate',
            'difficulty_zh': '中级'
        },
        'code-quality-toolkit': {
            'name': 'Code Quality Toolkit',
            'name_zh': '代码质量工具包',
            'description': 'Code quality, refactoring, and technical debt management',
            'description_zh': '代码质量、重构和技术债务管理',
            'icon': '✨',
            'difficulty': 'Beginner',
            'difficulty_zh': '初级'
        },
        'test-automation-suite': {
            'name': 'Test Automation Suite',
            'name_zh': '测试自动化套件',
            'description': 'Comprehensive test generation and optimization',
            'description_zh': '全面的测试生成和优化',
            'icon': '🧪',
            'difficulty': 'Beginner',
            'difficulty_zh': '初级'
        },
        'requirements-engineering-suite': {
            'name': 'Requirements Engineering Suite',
            'name_zh': '需求工程套件',
            'description': 'Requirements analysis, formalization, and traceability',
            'description_zh': '需求分析、形式化和可追溯性',
            'icon': '📋',
            'difficulty': 'Intermediate',
            'difficulty_zh': '中级'
        },
        'code-understanding-and-manipulation-suite': {
            'name': 'Code Understanding and Manipulation Suite',
            'name_zh': '代码理解与操作套件',
            'description': 'Code understanding, analysis, search, translation, and manipulation',
            'description_zh': '代码理解、分析、搜索、翻译和操作',
            'icon': '🔄',
            'difficulty': 'Intermediate',
            'difficulty_zh': '中级'
        },
        'devops-automation-toolkit': {
            'name': 'DevOps Automation Toolkit',
            'name_zh': 'DevOps 自动化工具包',
            'description': 'CI/CD pipelines, containerization, and deployment',
            'description_zh': 'CI/CD 流水线、容器化和部署',
            'icon': '🚀',
            'difficulty': 'Intermediate',
            'difficulty_zh': '中级'
        },
        'formal-verification-toolkit': {
            'name': 'Formal Verification Toolkit',
            'name_zh': '形式化验证工具包',
            'description': 'Formal verification of software systems',
            'description_zh': '软件系统的形式化验证',
            'icon': '🔍',
            'difficulty': 'Advanced',
            'difficulty_zh': '高级'
        },
        'security-scanner-suite': {
            'name': 'Security Scanner Suite',
            'name_zh': '安全扫描套件',
            'description': 'Comprehensive security analysis',
            'description_zh': '全面的安全分析',
            'icon': '🔒',
            'difficulty': 'Intermediate',
            'difficulty_zh': '中级'
        }
    }

    for item in packs_dir.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name in pack_metadata:
            metadata = pack_metadata[item.name]

            # Read pack.json to get skills list
            pack_json_path = item / 'pack.json'
            skills_list = []
            if pack_json_path.exists():
                try:
                    with open(pack_json_path, 'r', encoding='utf-8') as f:
                        pack_data = json.load(f)
                        skills_list = pack_data.get('skills', [])
                except Exception as e:
                    print(f"Warning: Could not read pack.json for {item.name}: {e}")

            packs.append({
                'id': item.name,
                'name': metadata['name'],
                'name_zh': metadata['name_zh'],
                'description': metadata['description'],
                'description_zh': metadata['description_zh'],
                'icon': metadata['icon'],
                'skills_count': len(skills_list),
                'skills': skills_list,
                'difficulty': metadata['difficulty'],
                'difficulty_zh': metadata['difficulty_zh'],
                'path': f'skill-packs/{item.name}'
            })

    packs.sort(key=lambda x: x['name'])
    return packs

def main():
    print("Loading translations...")
    translations = load_translations()

    print("Scanning repository for skills...")
    skills = scan_skills(translations)
    print(f"Found {len(skills)} skills")

    print("Scanning skill packs...")
    skill_packs = scan_skill_packs()
    print(f"Found {len(skill_packs)} skill packs")

    # Create output data
    output_data = {
        'skills': skills,
        'skill_packs': skill_packs,
        'total': len(skills),
        'total_packs': len(skill_packs),
        'category_names_zh': translations.get('category_names', {}),
        'generated_at': datetime.now().strftime('%Y-%m-%d')
    }

    # Write to file
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Generated {OUTPUT_FILE}")
    print(f"Total skills: {len(skills)}")
    print(f"Total skill packs: {len(skill_packs)}")

    # Show category breakdown
    categories = {}
    for skill in skills:
        cat = skill['category']
        categories[cat] = categories.get(cat, 0) + 1

    print("\nSkills by category:")
    for cat, count in sorted(categories.items()):
        print(f"  {cat}: {count}")

if __name__ == '__main__':
    main()
