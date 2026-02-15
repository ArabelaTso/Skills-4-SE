from flask import Flask, jsonify, request
from flask_cors import CORS
import os
import shutil
import yaml
from pathlib import Path

app = Flask(__name__)
CORS(app)

# Paths
REPO_ROOT = Path(__file__).parent.parent.parent
SKILLS_DIR = REPO_ROOT
CLAUDE_SKILLS_DIR = Path.home() / '.claude' / 'skills'

def get_skill_metadata(skill_path):
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
                return {
                    'name': frontmatter.get('name', skill_path.name),
                    'description': frontmatter.get('description', '')[:200] + '...' if len(frontmatter.get('description', '')) > 200 else frontmatter.get('description', '')
                }
    except Exception as e:
        print(f"Error reading {skill_path.name}: {e}")

    return None

def is_skill_installed(skill_name):
    """Check if skill is already installed"""
    return (CLAUDE_SKILLS_DIR / skill_name).exists()

@app.route('/api/skills', methods=['GET'])
def get_skills():
    """Get list of all available skills"""
    skills = []

    # Directories to exclude from skill list
    excluded_dirs = ['skill-manager', 'node_modules', 'skill-creator']

    # Scan repository for skill directories
    for item in SKILLS_DIR.iterdir():
        if item.is_dir() and not item.name.startswith('.') and not item.name in excluded_dirs:
            # Check if it's a skill directory (has SKILL.md)
            if (item / 'SKILL.md').exists():
                metadata = get_skill_metadata(item)
                if metadata:
                    skills.append({
                        'name': item.name,
                        'description': metadata['description'],
                        'installed': is_skill_installed(item.name),
                        'path': str(item)
                    })

    return jsonify({
        'skills': sorted(skills, key=lambda x: x['name']),
        'total': len(skills)
    })

@app.route('/api/install', methods=['POST'])
def install_skills():
    """Install selected skills to Claude skills directory"""
    data = request.json
    skill_names = data.get('skills', [])

    if not skill_names:
        return jsonify({'error': 'No skills specified'}), 400

    # Ensure Claude skills directory exists
    CLAUDE_SKILLS_DIR.mkdir(parents=True, exist_ok=True)

    installed = []
    failed = []

    for skill_name in skill_names:
        source = SKILLS_DIR / skill_name
        destination = CLAUDE_SKILLS_DIR / skill_name

        if not source.exists():
            failed.append({'skill': skill_name, 'reason': 'Skill not found'})
            continue

        try:
            # Remove existing installation if present
            if destination.exists():
                shutil.rmtree(destination)

            # Copy skill directory
            shutil.copytree(source, destination)
            installed.append(skill_name)

        except Exception as e:
            failed.append({'skill': skill_name, 'reason': str(e)})

    return jsonify({
        'installed': len(installed),
        'failed': len(failed),
        'details': {
            'installed': installed,
            'failed': failed
        }
    })

@app.route('/api/uninstall', methods=['POST'])
def uninstall_skills():
    """Uninstall selected skills from Claude skills directory"""
    data = request.json
    skill_names = data.get('skills', [])

    if not skill_names:
        return jsonify({'error': 'No skills specified'}), 400

    uninstalled = []
    failed = []

    for skill_name in skill_names:
        destination = CLAUDE_SKILLS_DIR / skill_name

        if not destination.exists():
            failed.append({'skill': skill_name, 'reason': 'Skill not installed'})
            continue

        try:
            shutil.rmtree(destination)
            uninstalled.append(skill_name)
        except Exception as e:
            failed.append({'skill': skill_name, 'reason': str(e)})

    return jsonify({
        'uninstalled': len(uninstalled),
        'failed': len(failed),
        'details': {
            'uninstalled': uninstalled,
            'failed': failed
        }
    })

@app.route('/api/status', methods=['GET'])
def get_status():
    """Get installation status"""
    return jsonify({
        'claude_skills_dir': str(CLAUDE_SKILLS_DIR),
        'exists': CLAUDE_SKILLS_DIR.exists(),
        'writable': os.access(CLAUDE_SKILLS_DIR.parent, os.W_OK)
    })

if __name__ == '__main__':
    print(f"Repository root: {REPO_ROOT}")
    print(f"Claude skills directory: {CLAUDE_SKILLS_DIR}")
    print(f"Starting server on http://localhost:8080")
    app.run(debug=True, port=8080)
