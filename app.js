// Data source - static JSON file for GitHub Pages
const SKILLS_DATA_URL = 'skills-data.json?v=' + Date.now();

// State
let allSkills = [];
let allSkillPacks = [];
let allSkillsData = {}; // Store full data including category translations
let selectedSkills = new Set();
let selectedCategories = new Set(['all']); // Changed to Set for multi-select
let currentLang = 'en'; // Default language
let currentView = 'category'; // 'category', 'stage', or 'packs'

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
        viewByCategory: '📂 By Category',
        viewByStage: '🔄 By Stage',
        viewByPacks: '📦 Skill Packs',
        filterAll: 'All',
        filterInstalled: '✓ Installed',
        filterCodeGen: 'Code Generation',
        filterTesting: 'Testing',
        filterDocs: 'Documentation',
        filterQuality: 'Code Quality & Analysis',
        filterArchitecture: 'Architecture & Design',
        filterReqs: 'Requirements & Specifications',
        filterDevOps: 'DevOps & Deployment',
        filterVersionControl: 'Version Control & Collaboration',
        filterProjectMgmt: 'Project Management & Issue Tracking',
        filterTeamComm: 'Team Communication',
        filterMonitoring: 'Monitoring & Error Tracking',
        filterDatabase: 'Database & Backend Services',
        filterDevTools: 'Development Tools & Builders',
        filterIntegration: 'Integration & Webhooks',
        filterDebug: 'Debugging & Error Handling',
        filterVerify: 'Formal Methods & Verification',
        filterMaint: 'Maintenance & Refactoring',
        filterVisualization: 'Visualization',
        filterOther: 'Other',
        stageRequirements: '📕 Requirements',
        stageDesign: '💡 Software Design',
        stageImplementation: '⌨️ Implementation',
        stageTesting: '👩🏽‍💻 Testing',
        stageVerification: '✅ Verification',
        stageDeployment: '💻 Deployment',
        stageMaintenance: '🔧 Maintenance',
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
        viewByCategory: '📂 按类别',
        viewByStage: '🔄 按阶段',
        viewByPacks: '📦 技能包',
        filterAll: '全部',
        filterInstalled: '✓ 已安装',
        filterCodeGen: '代码生成',
        filterTesting: '测试',
        filterDocs: '文档',
        filterQuality: '代码质量与分析',
        filterArchitecture: '架构与设计',
        filterReqs: '需求与规范',
        filterDevOps: 'DevOps 与部署',
        filterVersionControl: '版本控制与协作',
        filterProjectMgmt: '项目管理与问题跟踪',
        filterTeamComm: '团队沟通',
        filterMonitoring: '监控与错误跟踪',
        filterDatabase: '数据库与后端服务',
        filterDevTools: '开发工具与构建器',
        filterIntegration: '集成与 Webhooks',
        filterDebug: '调试与错误处理',
        filterVerify: '形式化方法与验证',
        filterMaint: '维护与重构',
        filterVisualization: '可视化',
        filterOther: '其他',
        stageRequirements: '📕 需求分析',
        stageDesign: '💡 软件设计',
        stageImplementation: '⌨️ 实现',
        stageTesting: '👩🏽‍💻 测试',
        stageVerification: '✅ 验证',
        stageDeployment: '💻 部署',
        stageMaintenance: '🔧 维护',
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
};

// Initialize
document.addEventListener('DOMContentLoaded', () => {
    // Load saved language preference
    currentLang = localStorage.getItem('skillsManagerLang') || 'en';
    updateLanguage();

    loadSkills();
    setupEventListeners();
    setupTabListeners();
});

// Setup event listeners
function setupEventListeners() {
    const installAllBtn = document.getElementById('installAll');
    const installSelectedBtn = document.getElementById('installSelected');
    const searchInput = document.getElementById('searchInput');
    const helpBtn = document.getElementById('helpBtn');
    const langToggleMain = document.getElementById('langToggleMain');
    const langToggle = document.getElementById('langToggle');
    const viewByCategoryBtn = document.getElementById('viewByCategory');
    const viewByStageBtn = document.getElementById('viewByStage');
    const viewByPacksBtn = document.getElementById('viewByPacks');

    if (installAllBtn) installAllBtn.addEventListener('click', installAllSkills);
    if (installSelectedBtn) installSelectedBtn.addEventListener('click', installSelectedSkills);
    if (searchInput) searchInput.addEventListener('input', handleSearch);
    if (helpBtn) helpBtn.addEventListener('click', openHelpModal);
    if (langToggleMain) langToggleMain.addEventListener('click', toggleLanguage);
    if (langToggle) langToggle.addEventListener('click', toggleHelpLanguage);
    if (viewByCategoryBtn) viewByCategoryBtn.addEventListener('click', () => switchView('category'));
    if (viewByStageBtn) viewByStageBtn.addEventListener('click', () => switchView('stage'));
    if (viewByPacksBtn) viewByPacksBtn.addEventListener('click', () => switchView('packs'));

    // Help modal
    const modal = document.getElementById('helpModal');
    const closeBtn = document.querySelector('.close');

    if (closeBtn) closeBtn.addEventListener('click', closeHelpModal);

    window.addEventListener('click', (e) => {
        if (e.target === modal) {
            closeHelpModal();
        }
    });

    // Filter tabs - support multi-select
    document.querySelectorAll('.tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const category = tab.dataset.category;

            // Handle "All" button
            if (category === 'all') {
                selectedCategories.clear();
                selectedCategories.add('all');
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
            }
            // Handle "Installed" button (exclusive with other categories)
            else if (category === 'installed') {
                selectedCategories.clear();
                selectedCategories.add('installed');
                document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
                tab.classList.add('active');
            }
            // Handle regular category buttons (multi-select)
            else {
                // Remove "all" and "installed" if selecting specific categories
                selectedCategories.delete('all');
                selectedCategories.delete('installed');
                document.querySelector('.tab[data-category="all"]').classList.remove('active');
                document.querySelector('.tab[data-category="installed"]').classList.remove('active');

                // Toggle current category
                if (selectedCategories.has(category)) {
                    selectedCategories.delete(category);
                    tab.classList.remove('active');
                } else {
                    selectedCategories.add(category);
                    tab.classList.add('active');
                }

                // If no categories selected, default to "all"
                if (selectedCategories.size === 0) {
                    selectedCategories.add('all');
                    document.querySelector('.tab[data-category="all"]').classList.add('active');
                }
            }

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
        allSkillPacks = data.skill_packs || [];
        console.log('Total skills loaded:', allSkills.length);
        console.log('Total skill packs loaded:', allSkillPacks.length);
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

// Global variable to store current search terms for highlighting
let currentSearchTerms = [];

// Render skills
function renderSkills() {
    const container = document.getElementById('skillsList');

    // If in packs view, render skill packs instead
    if (currentView === 'packs') {
        renderSkillPacks();
        return;
    }

    const searchInput = document.getElementById('searchInput').value.toLowerCase().trim();
    console.log('Rendering skills with search term:', searchInput);

    // Split search input into multiple terms by space
    const searchTerms = searchInput ? searchInput.split(/\s+/).filter(term => term.length > 0) : [];
    currentSearchTerms = searchTerms; // Store for highlighting

    let filteredSkills = allSkills.filter(skill => {
        // Handle "installed" filter
        if (selectedCategories.has('installed')) {
            return skill.installed;
        }

        // Handle "all" filter
        if (selectedCategories.has('all')) {
            return true;
        }

        // Handle multi-category/stage filter
        if (currentView === 'category') {
            const skillCategory = getSkillCategory(skill.name);
            return selectedCategories.has(skillCategory);
        } else {
            // Stage view
            const skillStage = skill.stage ? getStageId(skill.stage) : null;
            return skillStage && selectedCategories.has(skillStage);
        }
    });

    // If there are search terms, filter and rank the skills
    if (searchTerms.length > 0) {
        const rankedSkills = [];

        filteredSkills.forEach(skill => {
            const name = String(skill.name || '').toLowerCase();
            const displayName = String(skill.displayName || '').toLowerCase();
            const displayNameZh = String(skill.displayName_zh || '').toLowerCase();
            const description = String(skill.description || '').toLowerCase();
            const descriptionZh = String(skill.description_zh || '').toLowerCase();

            let nameMatches = 0;
            let descriptionMatches = 0;

            // Check each search term
            searchTerms.forEach(term => {
                // Escape special regex characters
                const escapedTerm = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

                // Check name matches (English and Chinese)
                if (name.includes(term) || displayName.includes(term) || displayNameZh.includes(term)) {
                    nameMatches++;
                }

                // Count occurrences in description (English and Chinese)
                try {
                    const descMatches = (description.match(new RegExp(escapedTerm, 'g')) || []).length;
                    const descZhMatches = (descriptionZh.match(new RegExp(escapedTerm, 'g')) || []).length;
                    descriptionMatches += descMatches + descZhMatches;
                } catch (e) {
                    console.error('Regex error for term:', term, e);
                }
            });

            // Only include skills that match at least one term
            if (nameMatches > 0 || descriptionMatches > 0) {
                rankedSkills.push({
                    skill: skill,
                    nameMatches: nameMatches,
                    descriptionMatches: descriptionMatches
                });
            }
        });

        // Sort: name matches first (by count), then description matches (by frequency)
        rankedSkills.sort((a, b) => {
            // First priority: skills with name matches come before those without
            if (a.nameMatches > 0 && b.nameMatches === 0) return -1;
            if (a.nameMatches === 0 && b.nameMatches > 0) return 1;

            // If both have name matches, sort by number of name matches
            if (a.nameMatches > 0 && b.nameMatches > 0) {
                if (a.nameMatches !== b.nameMatches) {
                    return b.nameMatches - a.nameMatches;
                }
            }

            // If both have only description matches (or same name matches), sort by description frequency
            return b.descriptionMatches - a.descriptionMatches;
        });

        filteredSkills = rankedSkills.map(item => item.skill);
    }

    console.log('Filtered skills count:', filteredSkills.length);

    if (filteredSkills.length === 0) {
        const noResultsText = currentLang === 'zh' ? '未找到技能' : 'No skills found';
        container.innerHTML = `<div class="loading">${noResultsText}</div>`;
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

// Highlight matching text
function highlightText(text, searchTerms) {
    if (!text || searchTerms.length === 0) {
        return text;
    }

    let highlightedText = String(text);

    // Sort terms by length (longest first) to avoid partial replacements
    const sortedTerms = [...searchTerms].sort((a, b) => b.length - a.length);

    sortedTerms.forEach(term => {
        // Escape special regex characters
        const escapedTerm = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

        try {
            // Case-insensitive replacement with highlight span
            const regex = new RegExp(`(${escapedTerm})`, 'gi');
            highlightedText = highlightedText.replace(regex, '<mark class="highlight">$1</mark>');
        } catch (e) {
            console.error('Highlight error for term:', term, e);
        }
    });

    return highlightedText;
}

// Create skill card HTML
function createSkillCard(skill) {
    const isSelected = selectedSkills.has(skill.name);
    const t = translations[currentLang];

    // Get category or stage based on current view
    let labelText, labelClass;
    if (currentView === 'category') {
        const category = getSkillCategory(skill.name);
        labelClass = `cat-${category}`;
        // Get localized category name
        labelText = currentLang === 'zh' && allSkillsData.category_names_zh && allSkillsData.category_names_zh[category]
            ? allSkillsData.category_names_zh[category]
            : category.split('-').map(w => w.charAt(0).toUpperCase() + w.slice(1)).join(' ');
    } else {
        // Stage view
        const stageName = skill.stage || 'No Stage';
        const stageId = skill.stage ? getStageId(skill.stage) : 'none';
        labelClass = `stage-${stageId}`;

        // Convert stage ID to display name with emoji
        if (skill.stage) {
            const stageDisplayMap = {
                'requirements': currentLang === 'zh' ? '📕 需求分析' : '📕 Requirements',
                'design': currentLang === 'zh' ? '💡 软件设计' : '💡 Software Design',
                'implementation': currentLang === 'zh' ? '⌨️ 实现' : '⌨️ Implementation',
                'testing': currentLang === 'zh' ? '👩🏽‍💻 测试' : '👩🏽‍💻 Testing',
                'verification': currentLang === 'zh' ? '✅ 验证' : '✅ Verification',
                'deployment': currentLang === 'zh' ? '💻 部署' : '💻 Deployment',
                'maintenance': currentLang === 'zh' ? '🔧 维护' : '🔧 Maintenance'
            };
            labelText = stageDisplayMap[stageId] || skill.stage;
        } else {
            labelText = currentLang === 'zh' ? '未分类' : 'No Stage';
        }
    }

    // Get localized skill name and description
    let skillName = currentLang === 'zh' && skill.displayName_zh
        ? skill.displayName_zh
        : formatSkillName(skill.name);

    let skillDescription = currentLang === 'zh' && skill.description_zh
        ? skill.description_zh
        : skill.description;

    // Truncate description for card display (keep full description for tooltip)
    const maxDescriptionLength = 150;
    if (skillDescription.length > maxDescriptionLength) {
        skillDescription = skillDescription.substring(0, maxDescriptionLength) + '...';
    }

    // Apply highlighting if there are search terms
    if (currentSearchTerms.length > 0) {
        skillName = highlightText(skillName, currentSearchTerms);
        skillDescription = highlightText(skillDescription, currentSearchTerms);
    }

    const statusText = skill.installed
        ? (currentLang === 'zh' ? '✓ 已安装' : '✓ Installed')
        : (currentLang === 'zh' ? '○ 可用' : '○ Available');

    // Get full description for tooltip (without truncation)
    const fullDescription = currentLang === 'zh' && skill.description_zh
        ? skill.description_zh
        : skill.description;

    // Escape HTML for tooltip to prevent XSS
    const escapeHtml = (text) => {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    };

    // Generate GitHub URL for the skill
    const githubBaseUrl = 'https://github.com/ArabelaTso/LLM4SE-Skills/tree/main';
    const skillGithubUrl = `${githubBaseUrl}/${skill.path}`;

    return `
        <div class="skill-card ${isSelected ? 'selected' : ''} ${skill.installed ? 'installed' : ''}"
             data-skill="${skill.name}">
            <div class="skill-header">
                <div class="skill-name">${skillName}</div>
                <input type="checkbox" class="skill-checkbox"
                       ${isSelected ? 'checked' : ''}
                       ${skill.installed ? 'disabled' : ''}>
            </div>
            <div class="skill-category ${labelClass}">${labelText}</div>
            <div class="skill-description">
                ${skillDescription}
                <a href="${skillGithubUrl}" target="_blank" class="see-more-link" onclick="event.stopPropagation()">
                    ${currentLang === 'zh' ? '查看详情' : 'See more'}
                </a>
            </div>
            <span class="skill-status ${skill.installed ? 'status-installed' : 'status-available'}">
                ${statusText}
            </span>
            <div class="tooltip">${escapeHtml(fullDescription)}</div>
        </div>
    `;
}

// Get skill category
function getSkillCategory(skillName) {
    // Find skill in allSkills array and return its category
    const skill = allSkills.find(s => s.name === skillName);
    return skill ? skill.category : 'other';
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
    console.log('Search triggered');
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
    // Get skill objects to access their paths
    const skills = allSkills.filter(s => skillNames.includes(s.name));
    const skillList = skills.map(s => `  - ${s.name}`).join('\n');
    const commands = skills.map(s => {
        const sourcePath = s.path || s.name;
        return `cp -r ${sourcePath} ~/.claude/skills/`;
    }).join('\n');

    const message = `To install these skills, clone the repository and run:\n\n` +
                   `git clone https://github.com/ArabelaTso/Skills-4-SE.git\n` +
                   `cd Skills-4-SE\n` +
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

// Switch between category, stage, and packs view
function switchView(view) {
    currentView = view;

    // Update button states
    const categoryBtn = document.getElementById('viewByCategory');
    const stageBtn = document.getElementById('viewByStage');
    const packsBtn = document.getElementById('viewByPacks');

    // Remove active from all buttons
    categoryBtn.classList.remove('active');
    stageBtn.classList.remove('active');
    packsBtn.classList.remove('active');

    // Hide all tab containers
    document.getElementById('categoryTabs').style.display = 'none';
    document.getElementById('stageTabs').style.display = 'none';

    if (view === 'category') {
        categoryBtn.classList.add('active');
        document.getElementById('categoryTabs').style.display = 'flex';
    } else if (view === 'stage') {
        stageBtn.classList.add('active');
        document.getElementById('stageTabs').style.display = 'flex';
    } else if (view === 'packs') {
        packsBtn.classList.add('active');
        // No tabs for packs view
    }

    // Reset selection to 'all'
    selectedCategories.clear();
    selectedCategories.add('all');

    // Update active tab
    document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
    if (view === 'category') {
        const activeTab = document.querySelector('#categoryTabs .tab[data-category="all"]');
        if (activeTab) activeTab.classList.add('active');
    } else if (view === 'stage') {
        const activeTab = document.querySelector('#stageTabs .tab[data-stage="all"]');
        if (activeTab) activeTab.classList.add('active');
    }

    // Re-setup tab listeners
    setupTabListeners();
    
    // Re-render skills
    renderSkills();
}

// Setup tab listeners for both category and stage tabs
function setupTabListeners() {
    // Category tabs
    document.querySelectorAll('#categoryTabs .tab').forEach(tab => {
        tab.replaceWith(tab.cloneNode(true)); // Remove old listeners
    });
    
    document.querySelectorAll('#categoryTabs .tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const category = tab.dataset.category;
            handleTabClick(category, tab, 'category');
        });
    });
    
    // Stage tabs
    document.querySelectorAll('#stageTabs .tab').forEach(tab => {
        tab.replaceWith(tab.cloneNode(true)); // Remove old listeners
    });
    
    document.querySelectorAll('#stageTabs .tab').forEach(tab => {
        tab.addEventListener('click', () => {
            const stage = tab.dataset.stage;
            handleTabClick(stage, tab, 'stage');
        });
    });
}

// Handle tab click for both category and stage
function handleTabClick(value, tab, type) {
    const containerSelector = type === 'category' ? '#categoryTabs' : '#stageTabs';
    
    // Handle "All" button
    if (value === 'all') {
        selectedCategories.clear();
        selectedCategories.add('all');
        document.querySelectorAll(`${containerSelector} .tab`).forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
    }
    // Handle "Installed" button
    else if (value === 'installed') {
        selectedCategories.clear();
        selectedCategories.add('installed');
        document.querySelectorAll(`${containerSelector} .tab`).forEach(t => t.classList.remove('active'));
        tab.classList.add('active');
    }
    // Handle other categories/stages - support multi-select
    else {
        // Remove "all" and "installed" if present
        selectedCategories.delete('all');
        selectedCategories.delete('installed');
        document.querySelector(`${containerSelector} .tab[data-${type}="all"]`)?.classList.remove('active');
        document.querySelector(`${containerSelector} .tab[data-${type}="installed"]`)?.classList.remove('active');
        
        // Toggle current category/stage
        if (selectedCategories.has(value)) {
            selectedCategories.delete(value);
            tab.classList.remove('active');
        } else {
            selectedCategories.add(value);
            tab.classList.add('active');
        }
        
        // If no categories selected, default to "all"
        if (selectedCategories.size === 0) {
            selectedCategories.add('all');
            document.querySelector(`${containerSelector} .tab[data-${type}="all"]`)?.classList.add('active');
        }
    }
    
    renderSkills();
}

// Get skill stage ID from stage name
function getStageId(stageName) {
    // If stageName is already a simple ID (from JSON data), return it directly
    if (stageName && !stageName.includes(' ')) {
        return stageName;
    }

    // Otherwise, map emoji-prefixed names to IDs
    const stageMap = {
        '📕 Requirements': 'requirements',
        '💡 Software Design': 'design',
        '⌨️ Implementation': 'implementation',
        '👩🏽‍💻 Testing': 'testing',
        '✅ Verification': 'verification',
        '💻 Deployment': 'deployment',
        '🔧 Maintenance': 'maintenance'
    };
    return stageMap[stageName] || null;
}

// Render skill packs
function renderSkillPacks() {
    const container = document.getElementById('skillsList');
    const searchInput = document.getElementById('searchInput').value.toLowerCase().trim();

    // Split search input into multiple terms
    const searchTerms = searchInput ? searchInput.split(/\s+/).filter(term => term.length > 0) : [];
    currentSearchTerms = searchTerms;

    let filteredPacks = allSkillPacks;

    // Apply search filter
    if (searchTerms.length > 0) {
        const rankedPacks = [];

        filteredPacks.forEach(pack => {
            const name = String(pack.name || '').toLowerCase();
            const nameZh = String(pack.name_zh || '').toLowerCase();
            const description = String(pack.description || '').toLowerCase();
            const descriptionZh = String(pack.description_zh || '').toLowerCase();

            let nameMatches = 0;
            let descriptionMatches = 0;

            searchTerms.forEach(term => {
                const escapedTerm = term.replace(/[.*+?^${}()|[\]\\]/g, '\\$&');

                if (name.includes(term) || nameZh.includes(term)) {
                    nameMatches++;
                }

                try {
                    const descMatches = (description.match(new RegExp(escapedTerm, 'g')) || []).length;
                    const descZhMatches = (descriptionZh.match(new RegExp(escapedTerm, 'g')) || []).length;
                    descriptionMatches += descMatches + descZhMatches;
                } catch (e) {
                    console.error('Regex error for term:', term, e);
                }
            });

            if (nameMatches > 0 || descriptionMatches > 0) {
                rankedPacks.push({
                    pack: pack,
                    nameMatches: nameMatches,
                    descriptionMatches: descriptionMatches
                });
            }
        });

        rankedPacks.sort((a, b) => {
            if (a.nameMatches > 0 && b.nameMatches === 0) return -1;
            if (a.nameMatches === 0 && b.nameMatches > 0) return 1;
            if (a.nameMatches > 0 && b.nameMatches > 0) {
                if (a.nameMatches !== b.nameMatches) {
                    return b.nameMatches - a.nameMatches;
                }
            }
            return b.descriptionMatches - a.descriptionMatches;
        });

        filteredPacks = rankedPacks.map(item => item.pack);
    }

    if (filteredPacks.length === 0) {
        const noResultsText = currentLang === 'zh' ? '未找到技能包' : 'No skill packs found';
        container.innerHTML = `<div class="loading">${noResultsText}</div>`;
        return;
    }

    container.innerHTML = filteredPacks.map(pack => createSkillPackCard(pack)).join('');

    // Add click handlers for install buttons
    document.querySelectorAll('.pack-install-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const packId = btn.dataset.packId;
            installSkillPack(packId);
        });
    });

    // Add click handlers for expand/collapse
    document.querySelectorAll('.pack-expand-btn').forEach(btn => {
        btn.addEventListener('click', (e) => {
            e.stopPropagation();
            const packCard = btn.closest('.skill-pack-card');
            const skillsList = packCard.querySelector('.pack-skills-list');
            const isExpanded = packCard.classList.contains('expanded');

            if (isExpanded) {
                packCard.classList.remove('expanded');
                skillsList.style.maxHeight = '0';
                btn.textContent = currentLang === 'zh' ? '▼ 展开查看技能' : '▼ Expand to view skills';
            } else {
                packCard.classList.add('expanded');
                skillsList.style.maxHeight = skillsList.scrollHeight + 'px';
                btn.textContent = currentLang === 'zh' ? '▲ 收起' : '▲ Collapse';
            }
        });
    });
}

// Create skill pack card HTML
function createSkillPackCard(pack) {
    const packName = currentLang === 'zh' && pack.name_zh ? pack.name_zh : pack.name;
    const packDescription = currentLang === 'zh' && pack.description_zh ? pack.description_zh : pack.description;
    const packDifficulty = currentLang === 'zh' && pack.difficulty_zh ? pack.difficulty_zh : pack.difficulty;

    // Apply highlighting if there are search terms
    let highlightedName = packName;
    let highlightedDescription = packDescription;
    if (currentSearchTerms.length > 0) {
        highlightedName = highlightText(packName, currentSearchTerms);
        highlightedDescription = highlightText(packDescription, currentSearchTerms);
    }

    const githubBaseUrl = 'https://github.com/ArabelaTso/LLM4SE-Skills/tree/main';
    const packGithubUrl = `${githubBaseUrl}/${pack.path}`;

    const installText = currentLang === 'zh' ? '安装' : 'Install';
    const skillsText = currentLang === 'zh' ? '个技能' : 'skills';
    const difficultyText = currentLang === 'zh' ? '难度' : 'Difficulty';
    const expandText = currentLang === 'zh' ? '▼ 展开查看技能' : '▼ Expand to view skills';

    // Generate skills list HTML
    let skillsListHTML = '';
    if (pack.skills && pack.skills.length > 0) {
        const skillsItems = pack.skills.map(skillName => {
            // Find the skill in allSkills to get display name and path
            const skill = allSkills.find(s => s.name === skillName);
            const displayName = skill
                ? (currentLang === 'zh' && skill.displayName_zh ? skill.displayName_zh : skill.displayName || formatSkillName(skillName))
                : formatSkillName(skillName);

            // Generate GitHub URL for the skill
            const githubBaseUrl = 'https://github.com/ArabelaTso/LLM4SE-Skills/tree/main';
            const skillPath = skill ? skill.path : `skills/${skillName}`;
            const skillGithubUrl = `${githubBaseUrl}/${skillPath}`;

            return `<li class="pack-skill-item"><a href="${skillGithubUrl}" target="_blank" onclick="event.stopPropagation()">${displayName}</a></li>`;
        }).join('');

        skillsListHTML = `
            <div class="pack-skills-list">
                <ul class="pack-skills-ul">
                    ${skillsItems}
                </ul>
            </div>
        `;
    }

    return `
        <div class="skill-pack-card" data-pack-id="${pack.id}">
            <div class="pack-header">
                <div class="pack-icon">${pack.icon}</div>
                <div class="pack-info">
                    <div class="pack-name">${highlightedName}</div>
                    <div class="pack-meta">
                        <span class="pack-skills-count">${pack.skills_count} ${skillsText}</span>
                        <span class="pack-difficulty">${difficultyText}: ${packDifficulty}</span>
                    </div>
                </div>
            </div>
            <div class="pack-description">
                ${highlightedDescription}
                <a href="${packGithubUrl}" target="_blank" class="see-more-link" onclick="event.stopPropagation()">
                    ${currentLang === 'zh' ? '查看详情' : 'See more'}
                </a>
            </div>
            <button class="pack-expand-btn" data-pack-id="${pack.id}">
                ${expandText}
            </button>
            ${skillsListHTML}
            <button class="pack-install-btn" data-pack-id="${pack.id}">
                ${installText}
            </button>
        </div>
    `;
}

// Install skill pack
function installSkillPack(packId) {
    const pack = allSkillPacks.find(p => p.id === packId);
    if (!pack) {
        showNotification('Skill pack not found', 'error');
        return;
    }

    const packName = currentLang === 'zh' && pack.name_zh ? pack.name_zh : pack.name;
    const sourcePath = pack.path || `skill-packs/${packId}`;

    const message = currentLang === 'zh'
        ? `要安装 "${packName}" 技能包，请克隆仓库并运行：\n\n` +
          `git clone https://github.com/ArabelaTso/LLM4SE-Skills.git\n` +
          `cd LLM4SE-Skills\n` +
          `mkdir -p ~/.claude/skills\n` +
          `cp -r ${sourcePath}/* ~/.claude/skills/`
        : `To install "${packName}" skill pack, clone the repository and run:\n\n` +
          `git clone https://github.com/ArabelaTso/LLM4SE-Skills.git\n` +
          `cd LLM4SE-Skills\n` +
          `mkdir -p ~/.claude/skills\n` +
          `cp -r ${sourcePath}/* ~/.claude/skills/`;

    const confirmText = currentLang === 'zh'
        ? `选择安装 "${packName}" 技能包（包含 ${pack.skills_count} 个技能）。\n\n` +
          `由于这是在 GitHub Pages 上运行，您需要手动安装。\n\n` +
          `点击确定查看安装说明。`
        : `Selected "${packName}" skill pack (${pack.skills_count} skills) for installation.\n\n` +
          `Since this is running on GitHub Pages, you'll need to manually install them.\n\n` +
          `Click OK to see installation instructions.`;

    if (confirm(confirmText)) {
        alert(message);

        if (navigator.clipboard) {
            navigator.clipboard.writeText(message).then(() => {
                const successText = currentLang === 'zh'
                    ? '安装说明已复制到剪贴板！'
                    : 'Installation instructions copied to clipboard!';
                showNotification(successText, 'success');
            }).catch(() => {
                const infoText = currentLang === 'zh'
                    ? '请手动复制安装说明'
                    : 'Please copy the installation instructions manually';
                showNotification(infoText, 'info');
            });
        }
    }
}
