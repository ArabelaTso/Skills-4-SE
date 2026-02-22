# 面向软件工程的实用技能集 (Skills-4-SE)


[![Welcome Contribution](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](https://github.com/ArabelaTso/Skills-4-SE/blob/main/CONTRIBUTING.md)
[![中文](https://img.shields.io/badge/lang-中文-red)](https://github.com/ArabelaTso/Skills-4-SE/blob/main/README-zh.md)
[![English](https://img.shields.io/badge/lang-English-blue)](https://github.com/ArabelaTso/Skills-4-SE/blob/main/README.md)

> *注：本文档由Claude翻译而成。*

---
本仓库是**一个全面的、可重用的、面向任务的技能集合**，旨在支持**整个开发生命周期的软件工程活动**，包括：

> 需求理解、系统设计、实现、测试、验证、部署和维护。

**本仓库提供**:
- 🌐 [**技能速览页**](https://ArabelaTso.github.io/Skills-4-SE/) 
- 📦 8大 [**核心技能包**](#-技能包)
- 🚀 180+ [**代码专项技能**](#目录)


## 🌐 Skills Manager 网页界面

**[🚀 访问 Skills Manager](https://ArabelaTso.github.io/Skills-4-SE/)**

> 你也可以本地部署. 👉 [指南](https://github.com/ArabelaTso/Skills-4-SE/blob/main/skill-manager/README.md)


<p align="center">
  <img src="https://github.com/ArabelaTso/Skills-4-SE/raw/main/images/skill-manager-image.png" alt="Skills Manager 界面" width="100%">
</p>

通过我们的交互式网页界面浏览、搜索和安装技能。Skills Manager 提供：
- 📦 一键安装所有个技能
- ✅ 选择性安装特定技能
- 🔍 按类别搜索和筛选
- 📖 中英文双语帮助文档
- 🎨 现代化响应式界面

<p align="center">
  <img src="https://github.com/ArabelaTso/Skills-4-SE/raw/main/images/zh-image.png" alt="Skills Manager Interface" width="100%">
</p>

## 📦 技能包

为常见软件工程工作流组织的相关技能集合。您可以安装精心策划的技能包，将相关功能捆绑在一起，而不是单独安装技能。

<p align="center">
  <img src="https://github.com/ArabelaTso/Skills-4-SE/raw/main/images/skill-pack-image.png" alt="Skills Manager Interface" width="100%">
</p>

### 🚀 可用技能包（共 8 个）

- **🐛 [错误修复套件](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/bug-fixing-suite/)** - 12 个技能，用于错误检测、定位和自动修复
- **✨ [代码质量工具包](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/code-quality-toolkit/)** - 13 个技能，用于代码质量、重构和技术债务管理
- **🧪 [测试自动化套件](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/test-automation-suite/)** - 18 个技能，用于全面的测试生成和优化
- **📋 [需求工程套件](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/requirements-engineering-suite/)** - 12 个技能，用于需求分析、形式化和可追溯性
- **🔄 [代码理解与操作套件](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/code-understanding-and-manipulation-suite/)** - 19 个技能，用于代码理解、分析、搜索、翻译和操作
- **🚀 [DevOps 自动化工具包](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/devops-automation-toolkit/)** - 10 个技能，用于 CI/CD 流水线、容器化和部署
- **🔍 [形式化验证工具包](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/formal-verification-toolkit/)** - 17 个技能，用于软件系统的形式化验证
- **🔒 [安全扫描套件](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/security-scanner-suite/)** - 13 个技能，用于全面的安全分析

### 快速安装

```bash
# 安装单个技能包
cd skill-packs/formal-verification-toolkit
./install.sh

# 安装多个技能包
cd skill-packs
./install-packs.sh formal-verification-toolkit security-scanner-suite

# 安装所有技能包
cd skill-packs
./install-all-packs.sh
```

👉 [了解更多关于技能包的信息](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skill-packs/README.md)

---


## ✨ 为什么是技能（而不仅仅是提示词）？

现代 LLM 功能强大，但**原始提示词很脆弱**：
- 难以复现
- 难以评估
- 难以集成到真实工作流中

我们将**技能视为一级artifact**，为**未来的元编程**做准备。

本仓库中的技能不仅仅是提示词：
- 它编码了**过程性知识**
- 它指定了**预期的输入/输出**
- 它记录了**失败模式**
- 它可以被**评估、组合和重用**

> 🤗 将本仓库视为 LLM 驱动系统的*软件工程能力标准库*。

## 目录

- [**按类别分类的技能**](#按类别分类的技能)
  - ⌨️ [代码生成](#代码生成)
  - 👩🏽‍💻 [测试](#测试)
  - ⚖️ [代码质量与分析](#代码质量与分析)
  - 📕 [文档](#文档)
  - 💡 [架构与设计](#架构与设计)
  - 📗 [需求与规范](#需求与规范)
  - 💻 [DevOps 与部署](#devops-与部署)
  - 🔀 [版本控制与协作](#版本控制与协作)
  - 📋 [项目管理与问题跟踪](#项目管理与问题跟踪)
  - 💬 [团队沟通](#团队沟通)
  - 📊 [监控与错误跟踪](#监控与错误跟踪)
  - 🗄️ [数据库与后端服务](#数据库与后端服务)
  - 🛠️ [开发工具与构建器](#开发工具与构建器)
  - 🔗 [集成与 Webhooks](#集成与-webhooks)
  - 🔨 [调试与错误处理](#调试与错误处理)
  - ✅ [形式化方法与验证](#形式化方法与验证)
  - 🔧 [维护与重构](#维护与重构)
  - 👀 [可视化](#可视化)
- [**按阶段分类的技能**](#-按阶段分类的技能)
  - 📕 [需求分析](#-需求)
  - 💡[软件设计](#-软件设计)
  - ⌨️ [实现](#️-实现)
  - 👩🏽‍💻 [测试](#-测试-1)
  - ✅ [验证](#-验证)
  - 💻 [部署](#-部署)
  - 🔧 [维护](#-维护-1)
- 📖 [使用方法](#使用方法)
- 🫶 [贡献](#贡献)
- 🎯 [愿景](#-愿景)
- 🙏 [参考](#参考)


## 按类别分类的技能

### 代码生成

**[函数/类生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/function-class-generator/)**
- 从规范生成函数和类
- 支持多种编程语言
- 包含类型提示、文档和错误处理

**[模块/组件生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/module-component-generator/)**
- 从接口契约构建完整模块
- 生成分层架构（模型、仓储、服务）
- 支持 Python 和 Java 的设计模式

**[模板代码生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/template-code-generator/)**
- 从模板创建样板代码
- 支持常见模式和框架
- 可定制的模板适用于不同用例

**[规范驱动生成](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/specification-driven-generation/)**
- 从形式化规范生成代码
- 确保规范合规性
- 验证生成的代码是否符合需求

**[测试驱动生成](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-driven-generation/)**
- 从测试用例生成实现
- 遵循 TDD 原则
- 确保测试覆盖率

**[增量式 Python 编程器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/incremental-python-programmer/)**
- 根据自然语言描述在 Python 仓库中实现新功能
- 生成全面的单元测试和集成测试
- 确保所有测试通过并遵循现有代码模式

**[增量式 Java 编程器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/incremental-java-programmer/)**
- 根据自然语言描述在 Java 仓库中实现新功能
- 支持 Maven 和 Gradle 构建系统
- 生成 JUnit 测试并确保所有测试成功通过

**[伪代码提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/pseudocode-extractor/)**
- 从源代码中提取与编程语言无关的伪代码
- 保留控制流和逻辑结构
- 过滤实现细节以提高清晰度

**[模块级代码翻译器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/module-level-code-translator/)**
- 在模块级别在编程语言之间翻译源代码
- 保留行为并适应目标语言习惯
- 为翻译的代码生成验证测试

**[伪代码到 Java 代码](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/pseudocode-to-java-code/)**
- 将伪代码描述转换为完整的、可执行的 Java 程序
- 保留原始逻辑和控制流
- 应用适当的 Java 习惯用法和最佳实践

**[伪代码到 Python 代码](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/pseudocode-to-python-code/)**
- 将伪代码和算法描述转换为可执行的 Python 代码
- 提供适当的结构、文档和测试
- 在遵循 Python 约定的同时保持算法逻辑

### 测试

### 测试

**[单元测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/unit-test-generator/)**
- 为函数和类生成单元测试
- 支持多种测试框架
- 包含边界情况和断言

**[集成测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/integration-test-generator/)**
- 为系统组件创建集成测试
- 测试组件交互
- 包含设置和清理逻辑

**[Java 测试更新器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/java-test-updater/)**
- 在重构后更新 Java 测试以适配新代码版本
- 处理签名变更、重构和行为修改
- 更新方法调用、断言、模拟对象并确保测试通过

**[不稳定测试检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/flaky-test-detector/)**
- 识别非确定性测试
- 分析测试执行模式
- 建议常见不稳定模式的修复方法

**[测试预言生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-oracle-generator/)**
- 为测试用例生成预期输出
- 创建断言和验证逻辑
- 支持基于属性的测试

**[边界情况生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/edge-case-generator/)**
- 识别并生成边界情况测试
- 覆盖边界条件
- 包含极端情况和错误场景

**[定向测试输入生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/directed-test-input-generator/)**
- 生成针对性的测试输入
- 专注于特定代码路径
- 使用符号执行技术

**[模糊测试输入生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/fuzzing-input-generator/)**
- 创建随机化测试输入
- 发现意外行为
- 支持基于变异的模糊测试

**[测试套件优先级排序器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-suite-prioritizer/)**
- 优先排序测试执行顺序
- 优化早期故障检测
- 考虑测试依赖关系和覆盖率

**[覆盖率增强器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/coverage-enhancer/)**
- 识别未覆盖的代码路径
- 生成测试以提高覆盖率
- 报告覆盖率指标

**[测试用例文档](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-case-documentation/)**
- 记录测试用例及其目的
- 解释测试场景和预期结果
- 维护测试文档

**[Python 测试更新器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-test-updater/)**
- 更新 Python 测试以适配新代码版本
- 修复由于签名和行为变更导致的测试失败
- 分析代码差异并相应更新断言

**[Bug 重现测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-reproduction-test-generator/)**
- 根据问题报告自动生成重现 bug 的测试
- 分析 bug 症状、堆栈跟踪和触发条件
- 创建最小化、聚焦的测试来可靠地触发 bug
- 支持 Python、Java 和 JavaScript 测试框架

**[区间引导回归测试更新器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interval-guided-regression-test-update/)**
- 基于区间分析更新回归测试

**[需求到测试转换器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/req-to-test/)**
- 将需求转换为测试用例
- 确保需求覆盖
- 将测试追溯到需求

**[测试用例简化器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-case-reducer/)**
- 使用增量调试将测试用例简化为最小形式

**[Java 回归测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/java-regression-test-generator/)**
- 自动为 Java 代码库生成回归测试
- 分析新旧代码版本之间的变更
- 确保测试覆盖重构或修改的功能

**[Python 回归测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-regression-test-generator/)**
- 自动为 Python 代码库生成回归测试
- 分析代码版本之间的变更并迁移现有测试
- 为新功能生成测试

**[模拟测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/mocking-test-generator/)**
- 为 Python 和 Java 生成带有适当模拟的单元测试
- 支持 Python 的 unittest.mock/pytest 和 Java 的 Mockito/JUnit
- 处理外部依赖和复杂交互

**[测试引导的 Bug 检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-guided-bug-detector/)**
- 分析失败的测试以检测代码中的功能性 bug
- 检查执行行为、断言和堆栈跟踪
- 识别导致测试失败的可疑代码区域

**[行为变异分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/behavioral-mutation-analyzer/)**
- 系统地分析变异测试中存活的变异体
- 识别测试套件弱点并生成改进建议
- 分类变异体存活的原因并建议测试增强

**[变形属性提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/metamorphic-property-extractor/)**
- 从程序中自动识别变形属性
- 无需显式测试预言即可实现变形测试
- 发现用于测试生成的输入输出关系

**[变形测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/metamorphic-test-generator/)**
- 使用变形测试原则生成测试用例
- 基于变形属性应用转换
- 通过输入输出关系扩展测试套件并检测 bug

**[反例到测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-to-test-generator/)**
- 将形式化验证反例转换为可执行测试用例
- 将模型检查器输出转换为单元测试或集成测试
- 连接形式化验证和测试工作流

**[变异测试套件优化器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/mutation-test-suite-optimizer/)**
- 使用变异测试分析优化测试套件
- 选择最大化变异杀死率的最小测试子集
- 减少执行时间并消除冗余

**[测试去重器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-deduplicator/)**
- 分析测试套件以识别冗余或重复的测试
- 检查代码覆盖率、语义相似性和执行行为
- 对等效测试进行分组并解释去重原理

**[Java API 一致性验证器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/java-api-consistency-validator/)**
- 验证两个版本的 Java 库之间的 API 一致性
- 比较签名、行为和异常
- 识别破坏性变更和不兼容的修改

**[Python API 一致性验证器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-api-consistency-validator/)**
- 验证两个版本的 Python 库之间的 API 一致性
- 比较签名、行为和异常
- 识别破坏性变更并提供迁移指导



### 代码质量与分析

**[代码审查助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-review-assistant/)**
- 执行自动化代码审查
- 识别问题并提出改进建议
- 检查编码标准合规性

**[代码异味检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-smell-detector/)**
- 检测代码异味和反模式
- 建议重构机会
- 按严重程度分类异味

**[设计异味检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/design-smell-detector/)**
- 识别架构和设计问题
- 检测设计原则违规
- 建议设计改进

**[代码优化器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-optimizer/)**
- 优化代码性能
- 识别瓶颈
- 建议算法改进

**[死代码消除器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/dead-code-eliminator/)**
- 识别未使用的代码
- 安全删除死代码
- 报告消除机会

**[技术债务分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/technical-debt-analyzer/)**
- 识别技术债务
- 量化债务影响
- 优先处理债务减少

**[代码模式提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-pattern-extractor/)**
- 分析代码库以识别可重用的代码模式和重复代码
- 生成包含重构建议的模式目录
- 为高价值模式创建可重用的模板代码

**[代码搜索助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-search-assistant/)**
- 在仓库中搜索与给定代码片段相关的代码
- 根据调用链、文本和功能相似性对结果进行排名
- 输出带有匹配代码片段的排名文件列表

**[组件边界识别器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/component-boundary-identifier/)**
- 识别模块/组件边界
- 检测边界违规
- 分析架构分离

**[代码总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-summarizer/)**
- 在多个尺度上生成源代码的简洁摘要
- 从函数到整个代码库解释代码功能
- 帮助快速理解复杂的代码结构

**[静态 Bug 检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/static-bug-detector/)**
- 静态分析源代码以检测潜在的功能性 bug
- 识别空指针解引用、错误条件、不可达代码
- 检测逻辑错误、资源泄漏和不一致的状态更新

**[静态漏洞检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/static-vulnerability-detector/)**
- 静态分析代码以检测安全漏洞
- 识别缓冲区溢出、注入风险、不安全的反序列化
- 检测不当的身份验证和不安全的加密使用

**[漏洞模式匹配器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/vulnerability-pattern-matcher/)**
- 通过匹配已知模式检测安全漏洞
- 识别不安全的编码习惯和 CVE 风格的模式
- 解释模式为何有风险以及利用条件

**[漏洞根因分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/vulnerability-root-cause-analyzer/)**
- 分析易受攻击的代码以识别潜在的根本原因
- 识别违反的假设、错误的不变量、缺失的验证
- 检测不安全的组件交互

**[可利用性分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/exploitability-analyzer/)**
- 评估检测到的漏洞的实际可利用性
- 检查控制流、输入源和清理逻辑
- 确定漏洞是否可实际利用

**[安全补丁顾问](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/security-patch-advisor/)**
- 为安全漏洞提出安全的修复策略
- 解决缓冲区溢出、注入风险、不安全的反序列化
- 提供不当身份验证和不安全加密使用的修复方案

**[CVE 可达性分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cve-reachability-analyzer/)**
- 分析依赖项中的 CVE 漏洞是否可从应用程序代码到达
- 执行静态和动态可达性分析
- 基于实际可利用性优先处理 CVE 修复

**[CVE 监控列表行动建议生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cve-watchlist-action-recommendation-generator/)**
- 为依赖项监控列表中的 CVE 生成可操作的建议
- 基于严重性、可利用性和影响优先处理 CVE
- 建议修补、缓解或监控策略

**[时间感知依赖 CVE 扫描器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/time-aware-dependency-cve-scanner/)**
- 扫描具有时间上下文感知的依赖项 CVE
- 跟踪 CVE 披露时间线和补丁可用性
- 提供时间敏感的漏洞管理建议

**[语义 Bug 检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/semantic-bug-detector/)**
- 通过分析代码行为与意图来检测语义级 bug
- 从名称、注释和文档推断预期目的
- 识别实现与预期行为之间的不匹配

**[行为保持检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/behavior-preservation-checker/)**
- 验证迁移或重构的代码库是否保留原始行为
- 比较运行时行为、测试结果和执行跟踪
- 识别代码版本之间的行为差异

**[语义等价验证器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/semantic-equivalence-verifier/)**
- 分析两个代码制品之间的语义等价性
- 比较控制流、数据流和可观察行为
- 为函数、类或模块提供严格的等价性分析

**[多版本行为比较器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/multi-version-behavior-comparator/)**
- 比较程序多个版本之间的行为
- 识别功能变更、回归和行为差异
- 指导安全升级和验证过程

**[回归一致性检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/regression-consistency-checker/)**
- 检查新版本是否保留旧版本测试观察到的行为
- 验证跨版本的行为一致性
- 识别意外的行为变更

**[区间差异分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interval-difference-analyzer/)**
- 分析版本之间程序区间（变量值范围）的差异
- 检测行为变更并识别潜在 bug
- 基于区间分析指导测试工作

**[区间分析性能分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interval-profiling-performance-analyzer/)**
- 分析程序以识别性能瓶颈
- 生成带有可视化的优化建议
- 使用区间分析获得性能洞察

### 文档

**[API 文档生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/api-documentation-generator/)**
- 生成 API 文档
- 创建参考文档
- 包含使用示例

**[代码注释生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-comment-generator/)**
- 生成内联代码注释
- 解释复杂逻辑
- 遵循文档标准

**[Markdown 文档结构化工具](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/markdown-document-structurer/)**
- 将 Markdown 文档重组为结构良好的格式
- 修复标题层次结构并生成目录
- 标准化格式并提高可读性

**[README 生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/readme-generator/)**
- 生成全面、用户友好的 README.md 文件
- 包含项目介绍、先决条件和设置说明
- 提供可执行的使用示例和仓库结构概览

**[变更日志生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/change-log-generator/)**
- 从提交创建变更日志
- 按类型分类变更
- 遵循语义化版本控制

**[代码变更总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-change-summarizer/)**
- 从代码变更生成结构化的拉取请求描述
- 记录带有迁移指南的破坏性变更
- 添加测试说明和上下文增强

**[发布说明编写器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/release-notes-writer/)**
- 编写发布说明
- 突出新功能和修复
- 面向最终用户

**[遗留代码总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/legacy-code-summarizer/)**
- 总结遗留代码库
- 解释代码功能
- 帮助理解旧代码

**[Python 仓库快速入门](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-repo-quickstart/)**
- 快速分析 Python 仓库
- 识别项目类型、入口点和依赖项
- 生成设置和执行说明

**[错误解释生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/error-explanation-generator/)**
- 解释错误消息
- 提供上下文和解决方案
- 帮助调试

### 架构与设计

**[API 设计助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/api-design-assistant/)**
- 协助 API 设计
- 建议 RESTful 模式
- 验证 API 一致性

**[设计模式建议器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/design-pattern-suggestor/)**
- 建议适当的设计模式
- 解释模式适用性
- 提供实现指导

**[配置生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/configuration-generator/)**
- 生成配置文件
- 支持多种格式（YAML、JSON、XML）
- 验证配置模式

**[依赖解析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/dependency-resolver/)**
- 解决依赖冲突
- 建议兼容版本
- 分析依赖树

### 需求与规范

**[需求总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-summarizer/)**
- 总结需求文档
- 提取关键需求
- 按优先级组织

**[需求覆盖检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-coverage-checker/)**
- 检查需求覆盖
- 识别实现中的差距
- 将需求追溯到代码

**[需求比较报告器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-comparison-reporter/)**
- 比较新旧需求文档
- 将需求变更映射到代码组件
- 生成详细的 Markdown 格式修改计划

**[歧义检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/ambiguity-detector/)**
- 检测模糊的需求
- 突出不清晰的规范
- 建议澄清

**[场景生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/scenario-generator/)**
- 生成使用场景
- 创建用户故事
- 开发测试场景

**[规范生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/specification-generator/)**
- 生成形式化规范
- 将自然语言转换为规范
- 验证规范完整性

**[自然语言到约束转换器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/nl-to-constraints/)**
- 将自然语言需求转换为形式化约束
- 支持约束语言
- 验证约束一致性

### DevOps 与部署

**[CI 流水线合成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/ci-pipeline-synthesizer/)**
- 生成用于自动化构建和测试的 CI 流水线配置
- 支持 GitHub Actions，包含依赖缓存和矩阵测试
- 包含 Node.js、Python、Go 和 Rust 项目的模板

**[CD 流水线生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cd-pipeline-generator/)**
- 创建用于自动化部署的 CD 流水线配置
- 支持 AWS、GCP 和 Azure 云平台
- 包含环境分离、审批门和回滚功能

**[容器化助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/containerization-assistant/)**
- 创建 Dockerfile 和容器配置
- 优化容器镜像
- 支持多阶段构建

**[环境设置助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/environment-setup-assistant/)**
- 生成环境设置脚本
- 管理依赖和配置
- 支持多个平台

**[回滚策略顾问](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rollback-strategy-advisor/)**
- 建议回滚策略
- 规划部署回退
- 最小化停机时间




**[Docker Hub Automation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/docker_hub-automation/)**
- 通过 Rube MCP (Composio) 自动化 Docker Hub 任务
- 管理仓库、镜像、标签和容器注册表
- 支持 Docker Hub 操作



**[代码插桩生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-instrumentation-generator/)**
- 自动插桩源代码以收集运行时信息
- 在添加插桩的同时保留程序语义
- 支持各种用于调试和分析的插桩策略

**[安全敏感路径插桩器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/security-sensitive-path-instrumenter/)**
- 向安全关键代码路径添加结构化日志插桩
- 监控身份验证、授权、输入验证和会话管理
- 实现安全相关事件的运行时监控

**[污点插桩助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/taint-instrumentation-assistant/)**
- 插桩代码以跟踪不受信任和敏感数据流
- 通过污点分析检测安全漏洞
- 识别潜在的注入点和数据泄漏

**[关键区间安全检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/critical-interval-security-checker/)**
- 分析代码以识别安全关键时间区间
- 检测可能危及安全的时序漏洞
- 识别竞态条件和检查时间使用时间问题



### 调试与错误处理

**[Bug 定位器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-localization/)**
- 在代码中定位 bug
- 分析堆栈跟踪和日志
- 建议可能的 bug 位置

**[Bug 到补丁生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-to-patch-generator/)**
- 为识别的 bug 生成补丁
- 创建最小修复
- 包含修复的测试用例

**[运行时错误解释器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/runtime-error-explainer/)**
- 解释运行时错误
- 提供调试指导
- 建议修复方法

**[回归根因分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/regression-root-cause-analyzer/)**
- 分析回归失败
- 识别根本原因
- 建议修复方法

**[冲突分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/conflict-analyzer/)**
- 分析合并冲突
- 建议冲突解决方案
- 解释冲突的变更

**[问题报告生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/issue-report-generator/)**
- 从失败的测试自动生成清晰、可操作的问题报告
- 分析测试失败以理解预期与实际行为
- 识别受影响的代码组件并建议修复

**[Bug 历史总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-history-summarizer/)**
- 跟踪并总结 bug 在代码版本中的完整生命周期
- 提供 bug 演变的历史背景
- 帮助理解 bug 模式和解决策略

**[Bisect 感知插桩](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bisect-aware-instrumentation/)**
- 插桩代码以支持高效的 git bisect 操作
- 产生确定性的通过/失败信号和简洁的运行时摘要
- 为 bisect 工作流创建健壮的测试脚本

**[重现跟踪插桩器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/reproduction-trace-instrumenter/)**
- 插桩源代码以捕获详细的执行跟踪用于 bug 重现
- 记录函数调用、变量值、控制流和程序状态
- 生成用于确定性 bug 重现的重放脚本

**[状态快照插桩器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/state-snapshot-instrumenter/)**
- 插桩程序以在运行时捕获关键程序状态的快照
- 包括变量值、内存状态、调用栈和执行上下文
- 以结构化 JSON 格式保存快照以供分析

**[跟踪收集助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/trace-collection-assistant/)**
- 收集、规范化和结构化来自插桩程序的执行跟踪
- 处理 strace、ltrace 和自定义跟踪格式
- 使跟踪适合调试、重现或性能分析

**[SZZ Bug 识别器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/szz-bug-identifier/)**
- 执行 SZZ 算法分析以识别引入 bug 的提交
- 通过版本历史追溯修改的行
- 将 bug 修复链接到其原始变更

**[语义 SZZ 分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/semantic-szz-analyzer/)**
- 通过语义分析扩展传统 SZZ 算法
- 区分实际引入 bug 的变更和重构
- 提供更准确的 bug 起源识别

### 形式化方法与验证

**[ACSL 注解助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/acsl-annotation-assistant/)**
- 协助 ACSL 注解
- 生成函数契约
- 验证注解正确性

**[断言合成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/assertion-synthesizer/)**
- 合成程序断言
- 生成不变量和前置/后置条件
- 验证断言正确性

**[不变量推断器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/invariant-inference/)**
- 推断循环和程序不变量
- 使用静态和动态分析
- 验证推断的不变量

**[静态推理验证器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/static-reasoning-verifier/)**
- 使用静态分析验证代码
- 检查正确性属性
- 报告验证结果

**[符号执行助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/symbolic-execution-assistant/)**
- 协助符号执行
- 生成路径约束
- 探索执行路径

**[反例生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-generator/)**
- 为失败的证明生成反例
- 从反例创建测试用例
- 帮助理解验证失败

**[反例解释器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-explainer/)**
- 解释反例
- 提供调试见解
- 建议修复方法

**[反例调试器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-debugger/)**
- 使用 Nitpick 或 QuickChick 的反例调试证明失败
- 识别规范错误和缺失的前置条件
- 帮助解决证明策略问题

**[抽象域探索器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-domain-explorer/)**
- 使用不同的抽象域应用抽象解释
- 支持区间、八边形、多面体、符号和同余域
- 推断不变量、值范围和关系

**[抽象不变量生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-invariant-generator/)**
- 使用抽象解释自动推断循环不变量
- 生成函数前置条件和后置条件
- 支持形式化验证工作流

**[抽象状态分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-state-analyzer/)**
- 执行抽象解释以推断程序状态
- 在不执行的情况下分析变量范围和数据属性
- 报告潜在的运行时错误

**[抽象跟踪总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-trace-summarizer/)**
- 使用抽象解释生成总结的执行跟踪
- 突出关键控制流路径和变量关系
- 生成高级程序行为表示

**[控制流抽象生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/control-flow-abstraction-generator/)**
- 生成抽象控制流图（CFG）表示
- 显示用于静态分析的循环、分支和函数调用
- 支持验证和程序理解

**[形式化规范生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/formal-spec-generator/)**
- 在 Isabelle/HOL 或 Coq 中生成形式化规范
- 将非形式化需求转换为形式化定义和谓词
- 从自然语言创建不变量、前置/后置条件

**[C/C++ 到 Lean4 翻译器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/c-cpp-to-lean4-translator/)**
- 将 C 或 C++ 程序翻译为等效的 Lean4 代码
- 保留程序语义并确保类型安全
- 生成类型良好、可执行和可验证的代码

**[C++ 到 Dafny 翻译器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cpp-to-dafny-translator/)**
- 将 C/C++ 程序翻译为等效的 Dafny 代码
- 保留语义并确保验证
- 支持形式化验证工作流

**[Python 到 Dafny 翻译器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-to-dafny-translator/)**
- 将 Python 程序翻译为等效的 Dafny 代码
- 保留程序语义并确保可验证性
- 生成类型良好、可执行的 Dafny 代码

**[Python 到 Lean4 翻译器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-to-lean4-translator/)**
- 将 Python 程序翻译为等效的 Lean4 代码
- 保留语义并确保类型安全
- 支持 Lean4 中的形式化验证

**[命令式到 Coq 模型提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/imperative-to-coq-model-extractor/)**
- 从命令式代码中提取抽象数学模型
- 支持 C、C++、Python、Java 用于 Coq 形式化推理
- 创建适合验证的 Coq 规范

**[程序到模型提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/program-to-model-extractor/)**
- 从函数式代码中提取抽象数学模型
- 支持 Haskell、OCaml、F# 到 Isabelle/HOL 的转换
- 实现对函数式程序的形式化推理

**[程序正确性证明器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/program-correctness-prover/)**
- 为程序正确性生成 Isabelle 或 Coq 证明
- 从规范建立部分或完全正确性
- 使用 Hoare 逻辑和最弱前置条件演算

**[证明携带代码生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-carrying-code-generator/)**
- 生成带有形式化正确性证明的可执行代码
- 在 Isabelle/HOL 或 Coq 中认证安全性和正确性属性
- 支持经过验证的软件和安全关键系统

**[证明骨架生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-skeleton-generator/)**
- 生成带有策略和战术的结构化证明骨架
- 为 Isabelle/HOL 或 Coq 中的定理创建中间引理
- 为复杂定理提供证明大纲

**[证明跟踪总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-trace-summarizer/)**
- 总结长的 Isabelle 或 Coq 证明脚本
- 提取高级逻辑步骤和推理流程
- 记录证明策略以便理解

**[证明失败解释器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-failure-explainer/)**
- 分析并解释为什么 Isabelle 或 Coq 证明失败
- 识别类型不匹配、缺失假设、错误目标
- 检测统一失败和不适用的策略

**[证明重构助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-refactoring-assistant/)**
- 重构 Isabelle 或 Coq 证明以提高可读性
- 在不改变语义的情况下增强模块化和可维护性
- 消除重复模式并改进证明结构

**[引理发现助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/lemma-discovery-assistant/)**
- 分析失败或卡住的证明以提出辅助引理
- 帮助在 Isabelle/HOL 或 Coq 中完成证明
- 解决无法证明的子目标和卡住的证明状态

**[库顾问](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/library-for-proof-advisor/)**
- 推荐相关的 Isabelle/HOL 或 Coq 标准库资源
- 根据证明目标建议理论、引理和策略
- 帮助找到现有的库支持以进行证明

**[策略建议助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tactic-suggestion-assistant/)**
- 分析 Isabelle 或 Coq 中的证明状态
- 建议可应用的策略以取得进展
- 帮助在交互式证明中选择下一步

**[细化步骤生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/refinement-step-generator/)**
- 从规范到实现生成系统的细化步骤
- 在 Isabelle/HOL 或 Coq 中使用正确性义务
- 通过细化支持形式化验证

**[验证边界报告器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/verification-boundary-reporter/)**
- 分析形式化验证制品（Isabelle、Coq、Dafny）
- 识别已验证、假设和未验证组件之间的边界
- 生成关于验证覆盖范围的结构化报告

**[已验证伪代码提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/verified-pseudocode-extractor/)**
- 从已验证的程序中提取与语言无关的伪代码
- 保留已验证的控制流和数据依赖
- 维护来自 Isabelle/HOL 或 Coq 代码的算法逻辑

**[已验证规范代码映射器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/verified-spec-code-mapper/)**
- 在形式化规范和已验证代码之间建立可追溯性
- 将前置条件、后置条件、不变量映射到代码组件
- 生成带有正确性证明的结构化 Markdown 映射

**[需求增强器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-enhancer/)**
- 迭代地将用户需求增强为清晰的规范
- 分析和澄清不完整或模糊的需求
- 生成可操作、完整的规范

**[接口契约验证器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interface-contract-verifier/)**
- 验证形式化契约（前置条件、后置条件、不变量）是否被保留
- 在更新到新程序版本时验证契约合规性
- 确保接口规范保持一致

**[代码补全语义约束](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-completion-semantic-constraints/)**
- 在满足语义约束的同时补全部分代码片段
- 生成带有验证测试的可编译代码
- 解释如何满足每个约束

**[模型引导代码修复](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/model-guided-code-repair/)**
- 使用反例自动修复时序属性的代码违规
- 推理模型级原因并提出最小化修复
- 通过重新验证或测试生成验证修复

**[TLA+ 引导代码修复](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tlaplus-guided-code-repair/)**
- 基于 TLA+ 规范违规修复代码
- 使用 TLA+ 模型检查结果指导修复策略
- 确保修复后的代码满足时序属性

**[程序到 TLA+ 规范生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/program-to-tlaplus-spec-generator/)**
- 从程序代码自动生成 TLA+ 规范
- 识别状态变量、动作和不变量
- 创建用于验证的形式化模型

**[TLA+ 规范生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tlaplus-spec-generator/)**
- 从需求或设计生成 TLA+ 规范
- 创建具有正确语法的形式化规范
- 支持并发和分布式系统建模

**[需求到 TLA+ 属性生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-to-tlaplus-property-generator/)**
- 将自然语言需求转换为 TLA+ 时序属性
- 形式化安全性和活性属性
- 从非形式化描述生成可验证的规范

**[规范到时序逻辑生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/specification-to-temporal-logic-generator/)**
- 将规范翻译为时序逻辑公式（LTL、CTL）
- 支持多种时序逻辑表示法
- 实现系统属性的形式化验证

**[TLA+ 模型简化](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tlaplus-model-reduction/)**
- 在保留属性的同时降低 TLA+ 模型复杂度
- 应用抽象和对称性简化技术
- 提高模型检查性能

**[SMV 模型提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/smv-model-extractor/)**
- 从程序代码或规范中提取 SMV 模型
- 生成适合符号模型检查的模型
- 支持 NuSMV 和 nuXmv 验证工具

**[RTL 规范一致性检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rtl-specification-consistency-checker/)**
- 检查 RTL 和规范之间的行为一致性
- 识别满足、违规、欠规范和不可检查的需求
- 提供带有执行跟踪的详细违规报告

**[RTL 等价检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rtl-equivalence-checker/)**
- 验证两个 RTL 实现之间的等价性
- 检测硬件设计中的功能差异
- 支持形式化等价检查工作流

**[RTL 属性推断](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rtl-property-inference/)**
- 从 RTL 代码自动推断时序属性
- 发现不变量和协议属性
- 为硬件验证生成断言

### 维护与重构

**[代码重构助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-refactoring-assistant/)**
- 建议重构机会
- 应用重构模式
- 确保行为保持

**[废弃 API 更新器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/deprecated-api-updater/)**
- 更新废弃的 API 使用
- 建议现代替代方案
- 自动化 API 迁移

**[代码翻译器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-translation/)**
- 在语言之间翻译代码
- 保持功能
- 适应目标语言习惯用法

**[框架迁移助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/framework-migration-assistant/)**
- 自动在框架之间迁移 Python Web 应用程序
- 在保留功能的同时转换代码、配置和测试
- 处理路由迁移和请求/响应模式

**[Spring MVC 到 Boot 迁移器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/spring-mvc-to-boot-migrator/)**
- 自动将 Spring MVC 应用程序迁移到 Spring Boot
- 转换构建配置、注解和 XML 配置
- 在现代化架构的同时保留现有功能

**[测试引导的迁移助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-guided-migration-assistant/)**
- 自动将代码库更新到新的语言或框架版本
- 确保在迁移期间所有测试继续通过
- 提供安全的、测试驱动的迁移路径

**[测试引导的精简](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-guided-debloating/)**
- 在保留测试执行的行为的同时从仓库中删除不必要的代码
- 安全地识别和消除死代码
- 准确维护测试套件覆盖的功能

**[智能变异算子生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/smart-mutation-operator-generator/)**
- 生成针对特定代码库定制的自定义变异算子
- 最大化变异测试的有效性
- 创建特定领域的变异以更好地评估测试

**[代码修复生成组合](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-repair-generation-combo/)**
- 自动修复有缺陷的代码并生成全面的测试
- 支持 Python、Java 和 C++ 程序
- 诊断 bug、生成修复并创建测试以防止回归

### 可视化

**[系统图生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/system-diagram-generator/)**
- 创建系统架构图
- 支持 Mermaid、PlantUML、Graphviz
- 生成数据流和部署图


## 🔁 按阶段分类的技能

> 软件开发生命周期（SDLC）中的阶段

### 📕 **需求分析**
- **需求分析**
    - [歧义检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/ambiguity-detector) – 自动检测需求中的模糊或含糊陈述
    - [需求总结器（长）](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-summarizer) – 从需求文档中提取核心功能、约束和优先级，输出 markdown 文件
    - [需求总结器（短）](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-summary) – 生成简洁、结构化的需求摘要，便于团队快速理解
    - [需求冲突分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/conflict-analyzer) – 检测需求之间的冲突或矛盾

- **可追溯性与覆盖**
    - [需求到测试转换器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/req-to-test) – 从需求自动生成测试用例
    - [需求到约束转换器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/nl-to-constraints) -- 将自然语言需求转换为形式化规范和约束（结构化、可测试的规范，带有明确的约束）
    - [可追溯性矩阵生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/traceability-matrix-generator) – 构建连接需求 → 设计 → 实现 → 测试的可追溯性矩阵
    - [需求覆盖检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-coverage-checker) – 检查现有设计/代码是否覆盖所有需求
    - [需求比较报告器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-comparison-reporter) – 比较需求版本，将变更映射到代码组件，并生成修改计划

- **文档与沟通**
    - [需求文档格式化器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/markdown-document-structurer) – 生成清晰、标准化的需求文档

- **场景与用户故事生成**
    - [场景生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/scenario-generator) – 基于需求生成使用场景和用户故事
    - [需求增强器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-enhancer) – 通过分析和澄清迭代地将用户需求增强为清晰、完整、可操作的规范



### 💡 **软件设计**
- **架构与高层设计**
    - [系统图生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/system-diagram-generator) – 创建系统结构的可视化表示
    - [设计模式建议器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/design-pattern-suggestor) – 为给定需求推荐合适的设计模式

- **接口与 API 设计**
    - [API 设计助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/api-design-assistant) – 建议 API 端点、参数和返回类型

- **设计质量与分析**
    - [设计异味检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/design-smell-detector) – 识别潜在问题，如高耦合或低内聚
    - [组件边界识别器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/component-boundary-identifier) – 识别模块/组件边界并检测边界违规
    - [配置生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/configuration-generator) – 为应用程序、服务或基础设施生成配置文件
    - [依赖解析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/dependency-resolver) – 识别和管理软件依赖

### ⌨️ **代码实现**
- **规范到代码**
    - [函数/类生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/function-class-generator) – 从形式化规范或设计描述生成函数或类
    - [模块/组件生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/module-component-generator) – 基于接口契约构建更大的组件或模块
    - [模板/骨架代码生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/template-code-generator) – 自动生成样板代码或项目模板/骨架
    - [增量式 Python 编程器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/incremental-python-programmer) – 根据自然语言描述在 Python 仓库中实现新功能，并自动生成测试
    - [增量式 Java 编程器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/incremental-java-programmer) – 根据自然语言描述在 Java 仓库（Maven/Gradle）中实现新功能，并生成 JUnit 测试

- **重构与优化**
    - [重构助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-refactoring-assistant) – 建议持续的代码改进以增强可维护性
    - [代码优化器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-optimizer) – 改进代码性能、内存使用或效率
    - [死代码消除器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/dead-code-eliminator) – 识别并删除未使用或冗余的代码
    - [代码审查助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-review-assistant) - 识别 bug、安全问题、性能问题、代码质量问题和最佳实践违规
    - [不良代码异味检测](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-smell-detector) - 识别并报告可能表明设计不良或可维护性问题的代码异味
    - [技术债务分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/technical-debt-analyzer) – 识别技术债务并量化债务影响
    - [代码模式提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-pattern-extractor) – 分析代码库以识别可重用的代码模式和重复代码
    - [代码搜索助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-search-assistant) – 使用相似性分析在仓库中搜索与给定代码片段相关的代码
    - [组件边界识别器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/component-boundary-identifier) – 识别模块/组件边界并分析架构分离
    - [代码总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-summarizer) – 在多个尺度上生成源代码的简洁摘要以解释和理解代码功能
    - [伪代码提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/pseudocode-extractor) – 从源代码中提取与编程语言无关的伪代码，保留控制流和逻辑结构
    - [模块级代码翻译器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/module-level-code-translator) – 在模块级别在编程语言之间翻译源代码，同时保留行为
    - [伪代码到 Java 代码](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/pseudocode-to-java-code) – 将伪代码描述转换为完整的、可执行的 Java 程序
    - [伪代码到 Python 代码](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/pseudocode-to-python-code) – 将伪代码和算法描述转换为可执行的 Python 代码
    - [代码插桩生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-instrumentation-generator) – 自动插桩源代码以在保留语义的同时收集运行时信息
    - [代码补全语义约束](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-completion-semantic-constraints) – 在满足指定语义约束的同时补全部分代码片段

- **TDD 与 SDD**
    - [测试驱动代码生成器（TDD）](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-driven-generation) – 生成通过给定单元测试集的实现（主要支持 Python 和 Java；处理简单的单元测试（隔离的函数/方法））
    - [规范驱动代码生成器（SDD）](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/specification-driven-generation) - 根据规范生成实现
    
- **多语言与翻译**
    - [代码翻译器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-translation) – 在编程语言之间转换代码，同时保持功能


### 👩🏽‍💻 **测试**
- **测试生成**
    - [单元测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/unit-test-generator) – 自动为函数或模块生成单元测试
    - [集成测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/integration-test-generator) – 为多个交互组件生成测试
    - [定向测试输入生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/directed-test-input-generator) – 使用程序上下文和测试目标指导 LLM 驱动的测试输入生成，以达到难以触及的行为
    - [模糊测试输入生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/fuzzing-input-generator) -- 生成随机化输入以检测意外故障
    - [Bug 重现测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-reproduction-test-generator) – 根据问题报告和堆栈跟踪自动生成重现 bug 的测试
    - [Java 回归测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/java-regression-test-generator) – 通过分析新旧代码版本之间的变更自动为 Java 代码库生成回归测试
    - [Python 回归测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-regression-test-generator) – 通过分析代码版本之间的变更自动为 Python 代码库生成回归测试并迁移现有测试
    - [模拟测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/mocking-test-generator) – 为具有外部依赖的 Python (unittest.mock/pytest) 或 Java (Mockito/JUnit) 代码生成带有适当模拟的单元测试
    - [变形测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/metamorphic-test-generator) – 使用变形测试原则通过基于变形属性应用转换来生成测试用例
    - [反例到测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-to-test-generator) – 将形式化验证反例转换为可执行测试用例以连接验证和测试工作流


- **断言与预言合成**
    - [覆盖率增强器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/coverage-enhancer) – 建议额外的单元测试以提高测试覆盖率
    - [断言合成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/assertion-synthesizer) – 为自动化测试用例生成断言（*场景*：为未测试的代码添加测试，增强现有测试，捕获实际行为。*复杂性*：简单和复杂断言。*编程语言*：多语言。）
    - [测试预言生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-oracle-generator) – 创建自动化预言以验证正确行为

- **测试覆盖分析与增强**
    - [场景生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/scenario-generator) – 基于需求生成测试场景或用户故事
    - [边界情况生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/edge-case-generator) – 从需求中自动识别潜在的边界和异常情况，并创建针对边界条件或不常见场景的测试
    - [测试套件优先级排序器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-suite-prioritizer) – 根据影响建议首先运行哪些测试
    - [变形属性提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/metamorphic-property-extractor) – 从程序中自动识别变形属性以实现无需显式测试预言的变形测试

- **测试质量与优化**
    - [行为变异分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/behavioral-mutation-analyzer) – 系统地分析变异测试中存活的变异体以识别测试套件弱点
    - [变异测试套件优化器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/mutation-test-suite-optimizer) – 使用变异测试优化测试套件以选择最大化变异杀死率的最小子集
    - [测试去重器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-deduplicator) – 通过检查覆盖率和语义相似性分析测试套件以识别冗余或重复的测试
    - [Java API 一致性验证器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/java-api-consistency-validator) – 验证两个版本的 Java 库之间的 API 一致性
    - [Python API 一致性验证器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-api-consistency-validator) – 验证两个版本的 Python 库之间的 API 一致性

- **故障分析**
    - [回归根因分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/regression-root-cause-analyzer) – 定位失败回归测试的根本原因
    - [错误解释生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/error-explanation-generator) – 解释测试失败的原因并提供可操作的指导
    - [运行时错误解释生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/runtime-error-explainer) – 解释运行时错误和编译失败，提供可操作的调试指导
    - [测试引导的 Bug 检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-guided-bug-detector) – 通过检查执行行为、断言和堆栈跟踪分析失败的测试以检测代码中的功能性 bug

- **测试文档与报告**
    - [测试用例文档](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-case-documentation) – 总结测试用例的文档

- **测试维护**
    - [Python 测试更新器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-test-updater) – 更新 Python 测试以适配新代码版本，修复失败的测试并更新断言
    - [Java 测试更新器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/java-test-updater) – 在代码重构后更新 Java 测试，处理签名变更、模拟对象和断言
    - [不稳定测试检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/flaky-test-detector) – 识别非确定性测试并建议常见不稳定模式的修复方法
    - [区间引导回归测试更新器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interval-guided-regression-test-update) – 基于区间分析更新回归测试
    - [测试用例简化器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-case-reducer) – 使用增量调试将测试用例简化为最小形式



### ✅ **验证**
- **规范与注解**
    - [接口规范生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interface-specification-generator) – 生成形式化或结构化的接口规范
    - [ACSL 注解助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/acsl-annotation-assistant) – 为 C/C++ 程序创建 ACSL 或其他形式化注解
    - [不变量推断器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/invariant-inference) – 自动推断循环或函数不变量
    - [规范生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/specification-generator) – 从代码或需求生成形式化规范（前置/后置条件、不变量）
    - [形式化规范生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/formal-spec-generator) – 从非形式化需求在 Isabelle/HOL 或 Coq 中生成形式化规范（定义、谓词、不变量、前置/后置条件）
    - [抽象不变量生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-invariant-generator) – 使用抽象解释自动推断循环不变量、函数前置条件和后置条件以进行形式化验证

- **抽象解释与分析**
    - [抽象域探索器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-domain-explorer) – 使用不同的抽象域（区间、八边形、多面体、符号、同余）应用抽象解释来分析程序变量
    - [抽象状态分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-state-analyzer) – 执行抽象解释以在不执行程序的情况下推断可能的程序状态、变量范围和数据属性
    - [抽象跟踪总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/abstract-trace-summarizer) – 执行抽象解释以生成总结的执行跟踪和高级程序行为表示
    - [控制流抽象生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/control-flow-abstraction-generator) – 生成显示循环、分支和函数调用的抽象控制流图（CFG）表示以进行静态分析

- **用于验证的代码翻译**
    - [C/C++ 到 Lean4 翻译器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/c-cpp-to-lean4-translator) – 将 C 或 C++ 程序翻译为等效的 Lean4 代码，保留程序语义并确保类型安全
    - [C++ 到 Dafny 翻译器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cpp-to-dafny-translator) – 将 C/C++ 程序翻译为等效的 Dafny 代码，同时保留语义并确保验证
    - [Python 到 Dafny 翻译器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-to-dafny-translator) – 将 Python 程序翻译为等效的 Dafny 代码，保留程序语义并确保可验证性
    - [Python 到 Lean4 翻译器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-to-lean4-translator) – 将 Python 程序翻译为等效的 Lean4 代码，同时保留语义并确保类型安全
    - [命令式到 Coq 模型提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/imperative-to-coq-model-extractor) – 从命令式代码（C、C++、Python、Java）中提取适合在 Coq 中进行形式化推理的抽象数学模型
    - [程序到模型提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/program-to-model-extractor) – 从函数式代码（Haskell、OCaml、F#）中提取抽象数学模型以在 Isabelle/HOL 中进行形式化推理

- **形式化验证**
    - [静态推理验证器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/static-reasoning-verifier) – 根据规范静态检查代码正确性
    - [符号执行助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/symbolic-execution-assistant) – 执行符号执行以检测潜在错误
    - [程序正确性证明器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/program-correctness-prover) – 从代码和形式化规范生成 Isabelle 或 Coq 证明，建立命令式程序的部分或完全正确性
    - [证明携带代码生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-carrying-code-generator) – 在 Isabelle/HOL 或 Coq 中生成可执行代码以及认证安全性和正确性属性的形式化证明

- **证明开发与辅助**
    - [证明骨架生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-skeleton-generator) – 为 Isabelle/HOL 或 Coq 中的定理生成带有策略、战术和中间引理的结构化证明骨架
    - [证明跟踪总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-trace-summarizer) – 将长的 Isabelle 或 Coq 证明脚本总结为高级逻辑步骤和推理流程
    - [证明重构助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-refactoring-assistant) – 重构和改进 Isabelle 或 Coq 证明以增强可读性、模块化和可维护性，而不改变语义
    - [引理发现助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/lemma-discovery-assistant) – 分析失败或卡住的证明并提出辅助引理以帮助在 Isabelle/HOL 或 Coq 中完成证明
    - [库顾问](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/library-for-proof-advisor) – 根据证明目标推荐相关的 Isabelle/HOL 或 Coq 标准库理论、引理和策略
    - [策略建议助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tactic-suggestion-assistant) – 分析 Isabelle 或 Coq 中的证明状态并建议可应用的策略以取得进展
    - [细化步骤生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/refinement-step-generator) – 在 Isabelle/HOL 或 Coq 中从高级规范到具体实现生成系统的细化步骤

- **反例分析**
    - [反例生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-generator) – 在验证失败时生成反例
    - [反例解释器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-explainer) – 解释为什么反例违反规范
    - [反例调试器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-debugger) – 使用 Nitpick (Isabelle) 或 QuickChick (Coq) 的反例调试证明失败，以识别规范错误和缺失的前置条件
    - [证明失败解释器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/proof-failure-explainer) – 分析并解释为什么 Isabelle 或 Coq 证明失败，识别根本原因，如类型不匹配、缺失假设和错误目标

- **验证报告与可追溯性**
    - [验证边界报告器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/verification-boundary-reporter) – 分析形式化验证制品（Isabelle、Coq、Dafny）并生成结构化报告，识别已验证、假设和未验证组件之间的边界
    - [已验证伪代码提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/verified-pseudocode-extractor) – 从形式化验证的程序（Isabelle/HOL、Coq）中提取与语言无关的伪代码，同时保留已验证的控制流和数据依赖
    - [已验证规范代码映射器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/verified-spec-code-mapper) – 在形式化规范（前置条件、后置条件、不变量）和已验证代码组件及其正确性证明之间建立明确的可追溯性
    - [接口契约验证器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interface-contract-verifier) – 验证在更新到新程序版本时形式化契约是否被保留
    - [行为保持检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/behavior-preservation-checker) – 验证迁移或重构的代码库是否保留原始行为
    - [语义等价验证器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/semantic-equivalence-verifier) – 分析两个代码制品之间的语义等价性
    - [回归一致性检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/regression-consistency-checker) – 检查新版本是否保留旧版本测试观察到的行为

- **TLA+ 规范与验证**
    - [程序到 TLA+ 规范生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/program-to-tlaplus-spec-generator) – 通过识别状态变量、动作和不变量从程序代码自动生成 TLA+ 规范
    - [TLA+ 规范生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tlaplus-spec-generator) – 从需求或设计生成 TLA+ 规范，用于并发和分布式系统建模
    - [需求到 TLA+ 属性生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/requirement-to-tlaplus-property-generator) – 将自然语言需求转换为 TLA+ 时序属性和形式化规范
    - [规范到时序逻辑生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/specification-to-temporal-logic-generator) – 将规范翻译为时序逻辑公式（LTL、CTL）以进行形式化验证
    - [TLA+ 模型简化](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tlaplus-model-reduction) – 使用抽象和对称性简化在保留属性的同时降低 TLA+ 模型复杂度
    - [TLA+ 引导代码修复](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/tlaplus-guided-code-repair) – 基于 TLA+ 规范违规使用模型检查结果修复代码
    - [模型引导代码修复](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/model-guided-code-repair) – 使用反例和模型级推理自动修复时序属性的代码违规

- **硬件验证**
    - [RTL 规范一致性检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rtl-specification-consistency-checker) – 检查 RTL 和规范之间的行为一致性，提供详细的违规报告
    - [RTL 等价检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rtl-equivalence-checker) – 验证两个 RTL 实现之间的等价性并检测功能差异
    - [RTL 属性推断](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rtl-property-inference) – 从 RTL 代码自动推断时序属性和不变量

- **模型检查与提取**
    - [SMV 模型提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/smv-model-extractor) – 从程序代码或规范中提取 SMV 模型以进行符号模型检查
    - [反例到测试生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/counterexample-to-test-generator) – 将形式化验证反例转换为可执行测试用例


### 💻 **部署**
- **部署准备**
    - [环境设置助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/environment-setup-assistant) – 为目标环境生成设置脚本或说明
    - [配置生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/configuration-generator) – 为应用程序、服务或基础设施生成配置文件
    - [依赖解析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/dependency-resolver) – 在部署前识别和管理软件依赖
    - [容器化助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/containerization-assistant) – 生成 Dockerfile 或容器化脚本
    - [配置一致性检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/config-consistency-checker) – 检测跨环境的配置不一致
    - [安全敏感路径插桩器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/security-sensitive-path-instrumenter) – 向安全关键代码路径添加结构化日志插桩以进行运行时监控
    - [污点插桩助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/taint-instrumentation-assistant) – 插桩代码以跟踪不受信任和敏感数据流以检测安全漏洞
    - [关键区间安全检查器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/critical-interval-security-checker) – 分析代码以识别安全关键时间区间和时序漏洞

- **持续集成与交付（CI/CD）**
    - [CI 流水线合成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/ci-pipeline-synthesizer) – 创建用于自动化构建和测试的 CI 流水线
    - [CD 流水线生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cd-pipeline-generator) – 生成用于自动化部署到预发布或生产环境的脚本
    - [构建/CI 迁移助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/build-ci-migration-assistant) – 迁移构建系统和 CI/CD 配置

- **云与基础设施部署**
    - [Docker Hub Automation](https://github.com/ArabelaTso/Skills-4-SE/tree/main/docker_hub-automation) – 通过 Rube MCP (Composio) 自动化 Docker Hub 任务，用于仓库、镜像、标签和容器注册表管理

- **部署验证与测试**
    - [回滚策略顾问](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/rollback-strategy-advisor) – 为失败的部署建议回滚策略

- **文档与报告**
    - [发布说明编写器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/release-notes-writer) – 自动生成面向用户的发布说明

- **监控与错误跟踪**

- **集成与 Webhooks**


### 🔧 **软件维护**
- **Bug 与问题处理**
    - [Bug 定位器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-localization) – 识别代码或模块中 bug 的位置
    - [回归根因分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/regression-root-cause-analyzer) – 查找失败回归测试的根本原因
    - [运行时错误解释生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/runtime-error-explainer) – 解释运行时错误和编译失败，提供可操作的调试指导
    - [Bug 到补丁生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-to-patch-generator) – 从 bug 报告或失败的测试用例生成代码修复
    - [Git Bisect 助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/git-bisect-assistant) – 自动化 git bisect 以找到第一个错误提交
    - [问题报告生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/issue-report-generator) – 从失败的测试和仓库分析自动生成清晰、可操作的问题报告
    - [Bug 历史总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bug-history-summarizer) – 跟踪并总结 bug 在代码版本中的完整生命周期
    - [Bisect 感知插桩](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/bisect-aware-instrumentation) – 插桩代码以支持高效的 git bisect 操作
    - [重现跟踪插桩器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/reproduction-trace-instrumenter) – 插桩源代码以捕获详细的执行跟踪用于 bug 重现
    - [状态快照插桩器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/state-snapshot-instrumenter) – 插桩程序以在运行时捕获关键程序状态的快照
    - [跟踪收集助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/trace-collection-assistant) – 收集、规范化和结构化来自插桩程序的执行跟踪
    - [SZZ Bug 识别器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/szz-bug-identifier) – 执行 SZZ 算法分析以识别引入 bug 的提交
    - [语义 SZZ 分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/semantic-szz-analyzer) – 通过语义分析扩展传统 SZZ 算法以更准确地识别 bug 起源
    - [代码修复生成组合](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-repair-generation-combo) – 自动修复有缺陷的代码并生成全面的测试以验证正确性

- **安全与漏洞管理**
    - [静态 Bug 检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/static-bug-detector) – 静态分析源代码以检测潜在的功能性 bug，包括空指针解引用、错误条件和逻辑错误
    - [静态漏洞检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/static-vulnerability-detector) – 静态分析代码以检测安全漏洞，包括缓冲区溢出、注入风险和不安全的反序列化
    - [漏洞模式匹配器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/vulnerability-pattern-matcher) – 通过将代码与已知漏洞模式和不安全编码习惯进行匹配来检测安全漏洞
    - [漏洞根因分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/vulnerability-root-cause-analyzer) – 分析易受攻击的代码以识别潜在的根本原因，如违反的假设和缺失的验证检查
    - [可利用性分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/exploitability-analyzer) – 通过检查控制流、输入源和清理逻辑来评估检测到的漏洞的实际可利用性
    - [安全补丁顾问](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/security-patch-advisor) – 为检测到的安全漏洞提出安全的修复策略
    - [语义 Bug 检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/semantic-bug-detector) – 通过分析代码行为是否与从名称、注释和文档推断的预期目的匹配来检测语义级 bug
    - [CVE 可达性分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cve-reachability-analyzer) – 分析依赖项中的 CVE 漏洞是否可从应用程序代码到达
    - [CVE 监控列表行动建议生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/cve-watchlist-action-recommendation-generator) – 为依赖项监控列表中的 CVE 生成可操作的建议
    - [时间感知依赖 CVE 扫描器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/time-aware-dependency-cve-scanner) – 扫描具有时间上下文感知的依赖项 CVE 并提供时间敏感的建议

- **遗留代码与技术债务管理**
    - [遗留代码总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/legacy-code-summarizer) – 生成关于遗留代码库的摘要和见解
    - [技术债务分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/technical-debt-analyzer) – 检测维护成本高或设计不良的区域
    - [废弃 API 更新器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/deprecated-api-updater) – 识别并替换废弃的 API

- **性能与可靠性监控**
    - [不稳定测试检测器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/flaky-test-detector) – 识别不稳定或不可靠的测试用例

- **版本控制与合并冲突**
    - [冲突分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/conflict-analyzer) – 分析合并冲突并建议冲突解决方案

- **文档与知识转移**
    - [api-documentation-generator](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/api-documentation-generator) - 为给定仓库总结 API 文档
    - [README 生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/readme-generator) – 生成全面、用户友好的 README.md 文件，包含设置说明和使用示例
    - [Python 仓库快速入门](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/python-repo-quickstart) - 快速分析 Python 仓库以了解结构、依赖项和设置要求
    - [Markdown 文档结构化工具](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/markdown-document-structurer) - 将 Markdown 文档重组为结构良好、一致的格式，提高可读性
    - [代码注释生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-comment-generator) – 生成有意义的注释以提高维护可读性
    - [变更日志生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/change-log-generator) – 从提交或补丁自动生成变更日志
    - [代码变更总结器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-change-summarizer) – 从代码变更生成结构化的 PR 描述，包含测试说明和上下文

- **持续改进**
    - [重构助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-refactoring-assistant) – 建议持续的代码改进以增强可维护性
    - [代码模式提取器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-pattern-extractor) – 识别可重用的代码模式以供未来开发
    - [代码搜索助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/code-search-assistant) – 使用多维相似性分析在仓库中搜索相关代码
    - [组件边界识别器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/component-boundary-identifier) – 识别模块/组件边界并检测边界违规
    - [框架迁移助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/framework-migration-assistant) – 自动在框架之间迁移 Python Web 应用程序
    - [Spring MVC 到 Boot 迁移器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/spring-mvc-to-boot-migrator) – 自动将 Spring MVC 应用程序迁移到 Spring Boot
    - [测试引导的迁移助手](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-guided-migration-assistant) – 在确保测试通过的同时自动将代码库更新到新的语言或框架版本
    - [测试引导的精简](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/test-guided-debloating) – 在保留测试执行的行为的同时删除不必要的代码
    - [智能变异算子生成器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/smart-mutation-operator-generator) – 生成针对特定代码库定制的自定义变异算子
    - [多版本行为比较器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/multi-version-behavior-comparator) – 比较程序多个版本之间的行为
    - [区间差异分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interval-difference-analyzer) – 分析版本之间的程序区间差异以检测行为变更
    - [区间分析性能分析器](https://github.com/ArabelaTso/Skills-4-SE/tree/main/skills/interval-profiling-performance-analyzer) – 分析程序以识别性能瓶颈

    


## 使用方法

每个技能都打包为一个包含 `SKILL.md` 文件和其他必要脚本/参考资料的技能文件夹，可以加载到 Claude Code 或其他兼容的 LLM 系统中。

### 设置技能

```bash
# 将技能文件夹复制到您的技能目录
cp -r skill-folder ~/.claude/skills
```

如果 `~/.claude/skills` 不存在，您可能还需要创建一个目录：

```bash
mkdir ~/.claude/skills
```

更多关于 [**Claude 如何存储技能和其他配置**](https://milvus.io/blog/why-claude-code-feels-so-stable-a-developers-deep-dive-into-its-local-storage-design.md#Claude-Code-Local-Storage-Layout) 的详细信息


### 使用技能

详见[网页](https://ArabelaTso.github.io/Skills-4-SE/) "使用说明"

## ⚡ 风险披露
为了防止技能在本地运行时可能存在的潜在**安全风险**（例如访问 SSH 密钥、API 密钥、向外部服务器发送数据、执行任意系统命令或修改全局依赖项），本项目中的所有技能均已通过 [Skill-Security-Scanner](https://github.com/huifer/skill-security-scan) 进行了**安全扫描**。以下是扫描报告摘要，完整报告可在此处查看：[此处](https://github.com/ArabelaTso/Skills-4-SE/tree/main/_report/)

📊 Risk Level 统计报告

  风险分布（共扫描 174 个技能）：

  - 🔴 CRITICAL: 16 个 Skill (9.2%)
    > 尝试访问 `\tmp` 或其他系统目录，安装软件包等
    - framework-migration-assistant
    - vulnerability-pattern-matcher
    - code-smell-detector
    - req-to-test
    - traceability-matrix-generator
    - python-test-updater
    - requirement-enhancer
    - security-sensitive-path-instrumenter
    - critical-interval-security-checker
    - static-vulnerability-detector
    - environment-setup-assistant
    - scenario-generator
    - security-patch-advisor
    - api-documentation-generator
    - test-case-documentation
    - symbolic-execution-assistant
  - 🟠 HIGH: 5 个 Skill (2.9%)
    > 使用 `os.system`、`subprocess`、`eval`、`exec`
    - containerization-assistant
    - bisect-aware-instrumentation
    - code-change-summarizer
    - configuration-generator
    - code-comment-generator
  - 🟡 MEDIUM: 9 个 Skill (5.2%)
    > 请求网络
  - 🟢 LOW: 21 个 Skill (12.1%)
  - ✅ SAFE: 123 个 Skill (70.7%)


⚠️ 注意：误报高，注意甄别。例如，Skill描述中出现“password”等单词，则被判定为风险级别高。自行决定是否使用。

详情见[日志](https://github.com/ArabelaTso/Skills-4-SE/tree/main/_report/security_scan_raw.log).


## 🤝 贡献

我们欢迎来自以下方面的贡献：
- **研究人员**（新技能、评估方法）
- **实践者**（真实世界用例、流水线）

您可以：
- **提交新技能** 
- **改进已有技能** （以现有技能作为baseline，改进流程、触发条件、运行脚本或示例代码）
- **建议新技能包** （将现有工具打包组合，以服务于新任务场景）


在提交拉取请求之前，请阅读[贡献指南](https://github.com/ArabelaTso/Skills-4-SE/blob/main/CONTRIBUTING.md)。

**快速贡献步骤**：
- 确保您的技能基于真实用例
- 检查现有技能中是否有重复
- 遵循技能结构模板
- 跨平台测试您的技能
- 提交带有清晰文档的拉取请求

## 🎯 愿景

我们的长期愿景是构建：
> **一个用于 LLM 驱动的软件工程系统的共享、开放的技能层** 

✅ 与提示词集合或临时演示不同，本仓库中的每个技能都是：
- **任务导向的**（解决具体的软件工程问题）
- **可重用的**（明确指定输入和输出）
- **可组合的**（可以链接成更大的工作流或管道）
- **工具和制品感知的**（操作真实的代码、测试、规范、配置、日志）

🧰 本仓库旨在作为以下系统的**共享技能层**：
- AI的助手（例如 Claude Skills、智能体）
- 工具增强的软件工程工作流
- 研究原型和实证研究
- 工业自动化和开发者生产力工具

🎉 如果您正在构建或研究用于软件工程的AI Agent，这个仓库适合您。




## 参考

特别感谢以下链接，它们对构建和增强本仓库中的技能做出了贡献：

- [awesome-claude-skills](https://github.com/ComposioHQ/awesome-claude-skills/)
- [anthropics-skills](https://github.com/anthropics/skills/)
- [openclaw-skills](https://github.com/openclaw/skills/)
