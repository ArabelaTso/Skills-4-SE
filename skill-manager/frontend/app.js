// Data source - static JSON file for GitHub Pages
const SKILLS_DATA_URL = 'skills-data.json';

// State
let allSkills = [];
let allSkillsData = {}; // Store full data including category translations
let selectedSkills = new Set();
let currentCategory = 'all';
let currentLang = 'en'; // Default language

// i18n translations
const translations = {
    en: {
        subtitle: 'Manage and install Claude Code skills for software engineering',
        infoBanner: 'ℹ️ Running in static mode. Click install buttons to get installation commands.',
        installAll: '📦 Install All Skills',
        installSelected: '✅ Install Selected Skills',
        refresh: '🔄 Refresh',
        help: '📖 How to Use',
        searchPlaceholder: '🔍 Search skills by name or description...',
        filterAll: 'All',
        filterInstalled: '✓ Installed',
        filterCodeGen: 'Code Generation',
        filterTesting: 'Testing',
        filterDocs: 'Documentation',
        filterQuality: 'Code Quality',
        filterReqs: 'Requirements',
        filterDevOps: 'DevOps',
        filterDebug: 'Debugging',
        filterVerify: 'Verification',
        filterMaint: 'Maintenance',
        totalSkills: 'skills available',
        selected: 'selected',
        loading: 'Loading skills...',
        failedLoad: '❌ Failed to load skills',
        errorLoading: 'Error loading skills-data.json',
        installCommand: 'Installation Command',
        copyCommand: 'Copy Command',
        copied: 'Copied!',
        close: 'Close'
    },
    zh: {
        subtitle: '管理和安装面向软件工程的 Claude Code 技能',
        infoBanner: 'ℹ️ 静态模式运行中。点击安装按钮获取安装命令。',
        installAll: '📦 安装所有技能',
        installSelected: '✅ 安装选中的技能',
        refresh: '🔄 刷新',
        help: '📖 使用说明',
        searchPlaceholder: '🔍 按名称或描述搜索技能...',
        filterAll: '全部',
        filterInstalled: '✓ 已安装',
        filterCodeGen: '代码生成',
        filterTesting: '测试',
        filterDocs: '文档',
        filterQuality: '代码质量',
        filterReqs: '需求',
        filterDevOps: 'DevOps',
        filterDebug: '调试',
        filterVerify: '验证',
        filterMaint: '维护',
        totalSkills: '个可用技能',
        selected: '个已选中',
        loading: '加载技能中...',
        failedLoad: '❌ 加载技能失败',
        errorLoading: '加载 skills-data.json 出错',
        installCommand: '安装命令',
        copyCommand: '复制命令',
        copied: '已复制！',
        close: '关闭'
    }
};

// Category mapping
const categoryMap = {
    'code-generation': ['function-class-generator', 'module-component-generator', 'template-code-generator',
                        'specification-driven-generation', 'test-driven-generation', 'incremental-python-programmer',
                        'incremental-java-programmer'],
    'testing': ['unit-test-generator', 'integration-test-generator', 'java-test-updater', 'flaky-test-detector',
                'test-oracle-generator', 'edge-case-generator', 'directed-test-input-generator',
                'fuzzing-input-generator', 'test-suite-prioritizer', 'coverage-enhancer',
                'test-case-documentation', 'python-test-updater', 'req-to-test'],
    'documentation': ['api-documentation-generator', 'code-comment-generator', 'markdown-document-structurer',
                      'readme-generator', 'change-log-generator', 'code-change-summarizer', 'release-notes-writer',
                      'legacy-code-summarizer', 'python-repo-quickstart', 'error-explanation-generator'],
    'quality': ['code-review-assistant', 'code-smell-detector', 'design-smell-detector', 'code-optimizer',
                'dead-code-eliminator', 'technical-debt-analyzer', 'code-pattern-extractor',
                'code-search-assistant', 'component-boundary-identifier'],
    'requirements': ['requirement-summarizer', 'requirement-coverage-checker', 'requirement-comparison-reporter',
                     'ambiguity-detector', 'scenario-generator', 'specification-generator', 'nl-to-constraints'],
    'devops': ['ci-pipeline-synthesizer', 'cd-pipeline-generator', 'containerization-assistant',
               'environment-setup-assistant', 'rollback-strategy-advisor'],
    'debugging': ['bug-localization', 'bug-to-patch-generator', 'runtime-error-explainer',
                  'regression-root-cause-analyzer', 'conflict-analyzer'],
    'verification': ['acsl-annotation-assistant', 'assertion-synthesizer', 'invariant-inference',
                     'static-reasoning-verifier', 'symbolic-execution-assistant', 'counterexample-generator',
                     'counterexample-explainer'],
    'maintenance': ['code-refactoring-assistant', 'deprecated-api-updater', 'code-translation']
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load saved language preference
    currentLang = localStorage.getItem('skillsManagerLang') || 'en';
    updateLanguage();

    loadSkills();
    setupEventListeners();
});

// Setup event listeners
function setupEventListeners() {
    const installAllBtn = document.getElementById('installAll');
    const installSelectedBtn = document.getElementById('installSelected');
    const refreshBtn = document.getElementById('refresh');
    const searchInput = document.getElementById('searchInput');
    const helpBtn = document.getElementById('helpBtn');
    const langToggleMain = document.getElementById('langToggleMain');
    const langToggle = document.getElementById('langToggle');

    if (installAllBtn) installAllBtn.addEventListener('click', installAllSkills);
    if (installSelectedBtn) installSelectedBtn.addEventListener('click', installSelectedSkills);
    if (refreshBtn) refreshBtn.addEventListener('click', loadSkills);
    if (searchInput) searchInput.addEventListener('input', handleSearch);
    if (helpBtn) helpBtn.addEventListener('click', openHelpModal);
    if (langToggleMain) langToggleMain.addEventListener('click', toggleLanguage);
    if (langToggle) langToggle.addEventListener('click', toggleHelpLanguage);

    // Help modal
    const modal = document.getElementById('helpModal');
    const closeBtn = document.querySelector('.close');

    if (closeBtn) closeBtn.addEventListener('click', closeHelpModal);

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeHelpModal();
        }
    });

    // Filter tabs
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
            tab.classList.add('active');
            currentCategory = tab.dataset.category;
            renderSkills();
        });
    });
}

// Language toggle
function toggleLanguage() {
    currentLang = currentLang === 'en' ? 'zh' : 'en';
    localStorage.setItem('skillsManagerLang', currentLang);
    updateLanguage();
}

// Toggle help modal language
function toggleHelpLanguage() {
    currentLang = currentLang === 'en' ? 'zh' : 'en';
    localStorage.setItem('skillsManagerLang', currentLang);

    const zhContent = document.getElementById('helpContentZh');
    const enContent = document.getElementById('helpContentEn');
    const langToggle = document.getElementById('langToggle');
    const helpTitle = document.getElementById('helpTitle');

    if (currentLang === 'zh') {
        zhContent.style.display = 'block';
        enContent.style.display = 'none';
        langToggle.textContent = 'EN';
        helpTitle.textContent = '📖 如何使用 Skills';
    } else {
        zhContent.style.display = 'none';
        enContent.style.display = 'block';
        langToggle.textContent = '中文';
        helpTitle.textContent = '📖 How to Use Skills';
    }

    // Also update main UI
    updateLanguage();
}

// Update UI language
function updateLanguage() {
    const t = translations[currentLang];

    // Update all elements with data-i18n attribute
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (t[key]) {
            el.textContent = t[key];
        }
    });

    // Update placeholder
    const searchInput = document.getElementById('searchInput');
    if (searchInput && t.searchPlaceholder) {
        searchInput.placeholder = t.searchPlaceholder;
    }

    // Update language toggle button
    const langToggleMain = document.getElementById('langToggleMain');
    if (langToggleMain) {
        langToggleMain.textContent = currentLang === 'en' ? '中文' : 'EN';
    }

    // Re-render skills with new language
    if (allSkills.length > 0) {
        renderSkills();
        updateStats();
    }
}

// Load skills from static JSON file
async function loadSkills() {
    try {
        console.log('Loading skills from:', SKILLS_DATA_URL);
        const response = await fetch(SKILLS_DATA_URL);
        console.log('Response status:', response.status);

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const data = await response.json();
        console.log('Loaded skills data:', data);

        if (!data.skills || !Array.isArray(data.skills)) {
            throw new Error('Invalid data format: skills array not found');
        }

        allSkillsData = data; // Store full data
        allSkills = data.skills;
        console.log('Total skills loaded:', allSkills.length);
        renderSkills();
        updateStats();
    } catch (error) {
        console.error('Error loading skills:', error);
        const errorMsg = error.message || 'Unknown error';
        showNotification(`Failed to load skills: ${errorMsg}`, 'error');
        document.getElementById('skillsList').innerHTML = `
            <div class="loading">
                ❌ Failed to load skills<br>
                <small>Error: ${errorMsg}</small><br>
                <small>Check browser console for details</small>
            </div>
        `;
    }
}

// Render skills
function renderSkills() {
    const container = document.getElementById('skillsList');
    const searchTerm = document.getElementById('searchInput').value.toLowerCase();

    let filteredSkills = allSkills.filter(skill => {
        const matchesSearch = skill.name.toLowerCase().includes(searchTerm) ||
                            skill.description.toLowerCase().includes(searchTerm);

        // Handle "installed" filter
        if (currentCategory === 'installed') {
            return matchesSearch && skill.installed;
        }

        const matchesCategory = currentCategory === 'all' || getSkillCategory(skill.name) === currentCategory;
        return matchesSearch && matchesCategory;
    });

    if (filteredSkills.length === 0) {
        container.innerHTML = '<div class="loading">No skills found</div>';
        return;
    }

    container.innerHTML = filteredSkills.map(skill => createSkillCard(skill)).join('');

    // Add click handlers
    document.querySelectorAll('.skill-card').forEach(card => {
        card.addEventListener('click', (e) => {
            if (e.target.type !== 'checkbox') {
                const checkbox = card.querySelector('.skill-checkbox');
                checkbox.checked = !checkbox.checked;
                handleSkillSelection(checkbox);
            }
        });

        const checkbox = card.querySelector('.skill-checkbox');
        checkbox.addEventListener('change', (e) => {
            e.stopPropagation();
            handleSkillSelection(checkbox);
        });
    });
}

// Create skill card HTML
function createSkillCard(skill) {
    const isSelected = selectedSkills.has(skill.name);
    const category = getSkillCategory(skill.name);
    const t = translations[currentLang];

    // Get localized category name
    const categoryLabel = currentLang === 'zh' && allSkillsData.category_names_zh && allSkillsData.category_names_zh[category]
        ? allSkillsData.category_names_zh[category]
        : category.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');

    // Get localized skill name and description
    const skillName = currentLang === 'zh' && skill.displayName_zh
        ? skill.displayName_zh
        : formatSkillName(skill.name);

    const skillDescription = currentLang === 'zh' && skill.description_zh
        ? skill.description_zh
        : skill.description;

    const statusText = skill.installed
        ? (currentLang === 'zh' ? '✓ 已安装' : '✓ Installed')
        : (currentLang === 'zh' ? '○ 可用' : '○ Available');

    return `
        <div class="skill-card ${isSelected ? 'selected' : ''} ${skill.installed ? 'installed' : ''}"
             data-skill="${skill.name}">
            <div class="skill-header">
                <div class="skill-name">${skillName}</div>
                <input type="checkbox" class="skill-checkbox"
                       ${isSelected ? 'checked' : ''}
                       ${skill.installed ? 'disabled' : ''}>
            </div>
            <div class="skill-category cat-${category}">${categoryLabel}</div>
            <div class="skill-description">${skillDescription}</div>
            <span class="skill-status ${skill.installed ? 'status-installed' : 'status-available'}">
                ${statusText}
            </span>
        </div>
    `;
}

// Get skill category
function getSkillCategory(skillName) {
    for (const [category, skills] of Object.entries(categoryMap)) {
        if (skills.includes(skillName)) {
            return category;
        }
    }
    return 'other';
}

// Format skill name
function formatSkillName(name) {
    return name.split('-')
        .map(word => word.charAt(0).toUpperCase() + word.slice(1))
        .join(' ');
}

// Handle skill selection
function handleSkillSelection(checkbox) {
    const card = checkbox.closest('.skill-card');
    const skillName = card.dataset.skill;

    if (checkbox.checked) {
        selectedSkills.add(skillName);
        card.classList.add('selected');
    } else {
        selectedSkills.delete(skillName);
        card.classList.remove('selected');
    }

    updateStats();
}

// Handle search
function handleSearch() {
    renderSkills();
}

// Update stats
function updateStats() {
    const t = translations[currentLang];
    const installedCount = allSkills.filter(s => s.installed).length;
    const availableCount = allSkills.length - installedCount;

    const statsText = currentLang === 'en'
        ? `${allSkills.length} skills (${installedCount} installed, ${availableCount} available)`
        : `${allSkills.length} 个技能（${installedCount} 个已安装，${availableCount} 个可用）`;

    const selectedText = currentLang === 'en'
        ? `${selectedSkills.size} selected`
        : `${selectedSkills.size} 个已选中`;

    document.getElementById('totalSkills').textContent = statsText;
    document.getElementById('selectedCount').textContent = selectedText;
}

// Install all skills - GitHub Pages version (provides instructions)
async function installAllSkills() {
    const availableSkills = allSkills.filter(s => !s.installed).map(s => s.name);

    if (availableSkills.length === 0) {
        showNotification('All skills are already installed!', 'info');
        return;
    }

    showInstallInstructions(availableSkills);
}

// Install selected skills - GitHub Pages version (provides instructions)
async function installSelectedSkills() {
    if (selectedSkills.size === 0) {
        showNotification('Please select at least one skill to install', 'info');
        return;
    }

    showInstallInstructions(Array.from(selectedSkills));
}

// Show installation instructions for GitHub Pages
function showInstallInstructions(skillNames) {
    const skillList = skillNames.map(name => `  - ${name}`).join('\n');
    const commands = skillNames.map(name =>
        `cp -r ${name} ~/.claude/skills/`
    ).join('\n');

    const message = `To install these skills, clone the repository and run:\n\n` +
                   `git clone https://github.com/YOUR_USERNAME/LLM4SE-Skills.git\n` +
                   `cd LLM4SE-Skills\n` +
                   `mkdir -p ~/.claude/skills\n` +
                   commands;

    // Create a modal or alert with instructions
    if (confirm(`Selected ${skillNames.length} skill(s) for installation.\n\n` +
                `Since this is running on GitHub Pages, you'll need to manually install them.\n\n` +
                `Click OK to see installation instructions.`)) {
        alert(message);

        // Also copy to clipboard if available
        if (navigator.clipboard) {
            navigator.clipboard.writeText(message).then(() => {
                showNotification('Installation instructions copied to clipboard!', 'success');
            }).catch(() => {
                showNotification('Please copy the installation instructions manually', 'info');
            });
        }
    }
}

// Install skills - kept for compatibility but redirects to instructions
async function installSkills(skillNames) {
    showInstallInstructions(skillNames);
}

// Show notification
function showNotification(message, type = 'info') {
    const notification = document.getElementById('notification');
    notification.textContent = message;
    notification.className = `notification ${type} show`;

    setTimeout(() => {
        notification.classList.remove('show');
    }, 3000);
}

// Help modal functions
function openHelpModal() {
    const modal = document.getElementById('helpModal');
    const zhContent = document.getElementById('helpContentZh');
    const enContent = document.getElementById('helpContentEn');
    const helpTitle = document.getElementById('helpTitle');
    const langToggle = document.getElementById('langToggle');

    // Show content based on current language
    if (currentLang === 'zh') {
        zhContent.style.display = 'block';
        enContent.style.display = 'none';
        helpTitle.textContent = '📖 如何使用 Skills';
        if (langToggle) langToggle.textContent = 'EN';
    } else {
        zhContent.style.display = 'none';
        enContent.style.display = 'block';
        helpTitle.textContent = '📖 How to Use Skills';
        if (langToggle) langToggle.textContent = '中文';
    }

    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
}

function closeHelpModal() {
    const modal = document.getElementById('helpModal');
    modal.classList.remove('show');
    document.body.style.overflow = 'auto';
}
// Keyboard shortcut for help (? key)
document.addEventListener('keydown', (e) => {
    if (e.key === '?' && !e.ctrlKey && !e.metaKey && !e.altKey) {
        const modal = document.getElementById('helpModal');
        if (modal.classList.contains('show')) {
            closeHelpModal();
        } else {
            openHelpModal();
        }
    }
    // ESC to close modal
    if (e.key === 'Escape') {
        closeHelpModal();
    }
});
