# Metamorphic Test Generator Skill

## 概述

这个技能使用元变测试（Metamorphic Testing）方法自动生成测试用例。它接受一个程序、原始测试用例集和一组元变属性作为输入，通过应用转换自动生成新的测试用例，执行测试，验证输出是否满足相应的属性，并报告任何违规或异常。

## 功能特性

- **自动测试生成**：基于元变属性自动生成新测试用例
- **多属性支持**：支持6种内置元变属性（排列、加法、乘法、逆运算、单调性、等价性）
- **多语言支持**：支持Python、JavaScript、Java等多种编程语言
- **执行与验证**：自动执行生成的测试并验证元变关系
- **详细报告**：生成包含属性覆盖率、违规和异常的详细报告
- **扩展测试套件**：输出包含原始和生成测试的完整测试套件

## 安装

将 `metamorphic-test-generator.skill` 文件复制到 Claude 的技能目录。

## 使用方法

### 基本用法

```bash
python scripts/generate.py program.py --tests tests/ --properties permutation,addition
```

### 使用属性配置文件

```bash
python scripts/generate.py program.py --tests tests.json --properties properties.json
```

### 生成完整报告

```bash
python scripts/generate.py program.py \
  --tests tests/ \
  --properties permutation,addition,inverse \
  --output report.json \
  --suite-output expanded-suite.json
```

## 内置元变属性

1. **permutation**（排列）：重新排序输入不应影响输出
2. **addition**（加法）：添加元素应增加或保持结果
3. **multiplication**（乘法）：缩放输入应按比例缩放输出
4. **inverse**（逆运算）：应用逆操作应返回原始状态
5. **monotonicity**（单调性）：增加输入不应减少输出
6. **equivalence**（等价性）：不同表示应产生相同结果

## 输出

技能生成以下输出：

1. **测试报告**（JSON格式）：
   - 原始测试数量
   - 生成的测试数量
   - 应用的属性
   - 发现的违规
   - 属性覆盖率
   - 异常信息

2. **扩展测试套件**（可选）：
   - 原始测试用例
   - 生成的测试用例及其元变关系

## 示例

技能包含一个完整的示例：

```bash
cd metamorphic-test-generator
python scripts/generate.py assets/example-program.py \
  --tests assets/test-cases-template.json \
  --properties permutation,addition \
  --output report.json
```

## 文件结构

```
metamorphic-test-generator/
├── SKILL.md                          # 技能说明文档
├── scripts/
│   └── generate.py                   # 主测试生成脚本
├── references/
│   └── properties.md                 # 元变属性参考文档
└── assets/
    ├── example-program.py            # 示例程序
    ├── test-cases-template.json      # 测试用例模板
    └── properties-template.json      # 属性配置模板
```

## 技术细节

- 支持JSON格式的输入/输出
- 自动检测程序语言（.py, .js, .java等）
- 10秒执行超时保护
- 详细的错误和异常报告
- 可扩展的属性系统

## 适用场景

- 缺乏测试预言（oracle）的程序测试
- 数学或算法属性验证
- 扩展现有测试套件
- 通过输入输出关系检测细微错误
- 回归测试和持续集成

## 参考资料

详细的属性说明和使用指南请参阅 `references/properties.md`。

## 版本

v1.0.0 - 初始版本
