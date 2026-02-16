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
EXCLUDED_DIRS = ['skill-manager', 'node_modules', 'skill-creator', '.git', 'awesome-claude-skills']

# Additional directories to include (from awesome-claude-skills-SE-skills)
ADDITIONAL_SKILL_DIRS = ['awesome-claude-skills-SE-skills']

# Category mapping (from app.js)
CATEGORY_MAP = {
    'code-generation': ['function-class-generator', 'module-component-generator', 'template-code-generator',
                        'specification-driven-generation', 'test-driven-generation', 'incremental-python-programmer',
                        'incremental-java-programmer'],
    'testing': ['unit-test-generator', 'integration-test-generator', 'java-test-updater', 'flaky-test-detector',
                'test-oracle-generator', 'edge-case-generator', 'directed-test-input-generator',
                'fuzzing-input-generator', 'test-suite-prioritizer', 'coverage-enhancer',
                'test-case-documentation', 'python-test-updater', 'req-to-test',
                'test-app-automation', 'webapp-testing'],
    'documentation': ['api-documentation-generator', 'code-comment-generator', 'markdown-document-structurer',
                      'readme-generator', 'change-log-generator', 'code-change-summarizer', 'release-notes-writer',
                      'legacy-code-summarizer', 'python-repo-quickstart', 'error-explanation-generator',
                      'confluence-automation'],
    'quality': ['code-review-assistant', 'code-smell-detector', 'design-smell-detector', 'code-optimizer',
                'dead-code-eliminator', 'technical-debt-analyzer', 'code-pattern-extractor',
                'code-search-assistant', 'component-boundary-identifier',
                'sentry-automation', 'datadog-automation', 'bugsnag-automation', 'bugbug-automation',
                'bugherd-automation', 'pagerduty-automation'],
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
                  'regression-root-cause-analyzer', 'conflict-analyzer'],
    'verification': ['acsl-annotation-assistant', 'assertion-synthesizer', 'invariant-inference',
                     'static-reasoning-verifier', 'symbolic-execution-assistant', 'counterexample-generator',
                     'counterexample-explainer'],
    'maintenance': ['code-refactoring-assistant', 'deprecated-api-updater', 'code-translation'],
    'development-tools': ['artifacts-builder', 'mcp-builder', 'codeinterpreter-automation', 'codereadr-automation']
}

def get_skill_category(skill_name):
    """Get category for a skill"""
    for category, skills in CATEGORY_MAP.items():
        if skill_name in skills:
            return category
    return 'other'

def load_translations():
    """Load Chinese translations"""
    try:
        with open(TRANSLATIONS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Warning: Could not load translations: {e}")
        return {'skills': {}, 'category_names': {}}

def extract_metadata(skill_path, translations):
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

                # Get description and truncate if needed
                description = frontmatter.get('description', '')
                if len(description) > 200:
                    description = description[:200] + '...'

                skill_name = skill_path.name
                skill_translations = translations['skills'].get(skill_name, {})

                return {
                    'name': skill_name,
                    'displayName': frontmatter.get('name', skill_name),
                    'description': description,
                    'category': get_skill_category(skill_name),
                    'installed': False,
                    'displayName_zh': skill_translations.get('name', frontmatter.get('name', skill_name)),
                    'description_zh': skill_translations.get('description', description)
                }
    except Exception as e:
        print(f"Error reading {skill_path.name}: {e}")

    return None

def scan_skills(translations):
    """Scan repository for all skills"""
    skills = []

    # Scan main repository skills
    for item in REPO_ROOT.iterdir():
        if item.is_dir() and not item.name.startswith('.') and item.name not in EXCLUDED_DIRS:
            # Check if it's a skill directory (has SKILL.md)
            if (item / 'SKILL.md').exists():
                metadata = extract_metadata(item, translations)
                if metadata:
                    skills.append(metadata)

    # Scan additional skill directories (awesome-claude-skills-SE-skills)
    for additional_dir_name in ADDITIONAL_SKILL_DIRS:
        additional_dir = REPO_ROOT / additional_dir_name
        if additional_dir.exists() and additional_dir.is_dir():
            print(f"Scanning additional directory: {additional_dir_name}")
            for item in additional_dir.iterdir():
                if item.is_dir() and not item.name.startswith('.'):
                    # Check if it's a skill directory (has SKILL.md)
                    if (item / 'SKILL.md').exists():
                        metadata = extract_metadata(item, translations)
                        if metadata:
                            skills.append(metadata)

    # Sort by name
    skills.sort(key=lambda x: x['name'])

    return skills

def main():
    print("Loading translations...")
    translations = load_translations()

    print("Scanning repository for skills...")
    skills = scan_skills(translations)
    print(f"Found {len(skills)} skills")

    # Create output data
    output_data = {
        'skills': skills,
        'total': len(skills),
        'category_names_zh': translations.get('category_names', {}),
        'generated_at': datetime.now().strftime('%Y-%m-%d')
    }

    # Write to file
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_FILE, 'w', encoding='utf-8') as f:
        json.dump(output_data, f, indent=2, ensure_ascii=False)

    print(f"Generated {OUTPUT_FILE}")
    print(f"Total skills: {len(skills)}")

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
