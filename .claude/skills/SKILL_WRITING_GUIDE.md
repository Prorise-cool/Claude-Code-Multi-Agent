# Claude Code Skills 撰写规范指南

> 本文档基于 Claude Code Skills 官方规范、社区最佳实践和本项目中的实际案例整理而成。

## 📋 目录

1. [Skills 概述](#skills-概述)
2. [SKILL.md 文件结构](#skillmd-文件结构)
3. [YAML Frontmatter 规范](#yaml-frontmatter-规范)
4. [内容编写规范](#内容编写规范)
5. [资源组织规范](#资源组织规范)
6. [最佳实践](#最佳实践)
7. [质量检查清单](#质量检查清单)

---

## Skills 概述

### 什么是 Skills？

Skills 是模块化、自包含的包，通过提供专业知识、工作流和工具来扩展 Claude 的能力。它们将 Claude 从通用助手转变为具备特定领域程序性知识的专业助手。

### Skills 提供什么？

1. **专业工作流** - 特定领域的多步骤程序
2. **工具集成** - 处理特定文件格式或 API 的指令
3. **领域专业知识** - 公司特定知识、模式、业务逻辑
4. **打包资源** - 用于复杂和重复任务的脚本、参考资料和资源

### Skills 的加载机制

Skills 使用三级加载系统来高效管理上下文：

1. **元数据 (name + description)** - 始终在上下文中（~100 词）
2. **SKILL.md 正文** - 当技能触发时加载（< 5000 词，建议 < 500 行）
3. **打包资源** - 由 Claude 按需加载（无限制*）

*无限制是因为脚本可以在不读入上下文窗口的情况下执行。

---

## SKILL.md 文件结构

### 基本结构

每个 Skill 必须包含一个 `SKILL.md` 文件，结构如下：

```
skill-name/
├── SKILL.md (必需)
│   ├── YAML frontmatter metadata (必需)
│   │   ├── name: (必需)
│   │   └── description: (必需)
│   └── Markdown instructions (必需)
└── 打包资源 (可选)
    ├── scripts/          - 可执行代码 (Python/Bash/etc.)
    ├── references/       - 按需加载到上下文的文档
    └── assets/           - 输出中使用的文件 (模板、图标、字体等)
```

### 完整示例

```markdown
---
name: your-skill-name
description: 清晰描述技能功能以及 Claude 应何时使用它。使用第三人称，包含关键词。
license: Complete terms in LICENSE.txt  # 可选
---

# Skill 标题

技能的主要说明和用途。

## 何时使用此技能

明确说明在什么情况下应该触发此技能。

## 功能特性

### 功能 1
详细说明...

### 功能 2
详细说明...

## 使用步骤

1. 步骤 1
2. 步骤 2
3. 步骤 3

## 参考资源

- [详细文档](./references/detailed-doc.md)
- [API 文档](./references/api-docs.md)
```

---

## YAML Frontmatter 规范

### 必需字段

#### `name` (必需)
- **格式**: 小写字母、数字和连字符
- **长度**: 最多 64 个字符
- **要求**: 唯一标识符，使用 kebab-case
- **示例**: `artifacts-builder`, `architecture-specialist`

```yaml
name: your-skill-name
```

#### `description` (必需)
- **长度**: 最多 1024 个字符
- **要求**: 
  - 使用第三人称描述（例如："This skill should be used when..." 而不是 "Use this skill when..."）
  - 具体说明技能功能和触发条件
  - 包含关键词以提高可发现性
- **示例**:

```yaml
description: 一套用于使用现代前端 Web 技术（React、Tailwind CSS、shadcn/ui）创建复杂的多组件 claude.ai HTML 工件的工具集。适用于需要状态管理、路由或 shadcn/ui 组件的复杂工件，不适用于简单的单文件 HTML/JSX 工件。
```

### 可选字段

#### `license`
- **格式**: 字符串
- **说明**: 许可证信息，通常指向 LICENSE.txt 文件
- **示例**: `license: Complete terms in LICENSE.txt`

---

## 内容编写规范

### 写作风格

1. **使用命令式/不定式形式**
   - ✅ 正确: "To accomplish X, do Y"
   - ❌ 错误: "You should do X" 或 "If you need to do X"

2. **使用第三人称描述触发条件**
   - ✅ 正确: "This skill should be used when..."
   - ❌ 错误: "Use this skill when..."

3. **客观、指令性语言**
   - 保持一致性，便于 AI 理解
   - 避免主观判断和模糊表述

### 内容组织原则

#### 渐进式披露 (Progressive Disclosure)

**核心原则**: 将信息分层，按需加载。

1. **SKILL.md 正文** - 保持精简（< 500 行）
   - 包含核心工作流程
   - 包含关键步骤和指令
   - 引用详细资源而非重复内容

2. **references/** - 详细文档
   - 数据库模式
   - API 文档
   - 详细工作流指南
   - 公司政策文档

3. **scripts/** - 可执行代码
   - 重复使用的代码
   - 需要确定性可靠性的任务

4. **assets/** - 输出资源
   - 模板文件
   - 图像、图标
   - 字体文件
   - 示例文档

#### 避免重复

- 信息应该只存在于一个地方
- SKILL.md 中只保留核心程序指令和工作流指导
- 详细参考材料、模式和示例应移至 references 文件
- 这使 SKILL.md 保持精简，同时使信息可发现而不占用上下文窗口

### 内容长度建议

- **SKILL.md 正文**: < 500 行（< 5000 词）
- **references/**: 无限制，但建议单个文件 < 10k 词
- **scripts/**: 无限制（可执行而不读入上下文）

---

## 资源组织规范

### scripts/ 目录

**用途**: 可执行代码（Python/Bash/etc.）用于需要确定性可靠性或重复编写的任务。

**何时包含**:
- 相同代码被重复编写时
- 需要确定性可靠性时

**示例**:
- `scripts/rotate_pdf.py` - PDF 旋转任务
- `scripts/init-artifact.sh` - 项目初始化脚本

**好处**:
- Token 高效
- 确定性
- 可以在不加载到上下文的情况下执行

**注意事项**:
- 脚本可能仍需要被 Claude 读取以进行补丁或环境特定调整
- 在说明中列出所需的包
- 验证包的可用性
- 提供清晰的文档

### references/ 目录

**用途**: 文档和参考资料，按需加载到上下文以指导 Claude 的流程和思考。

**何时包含**:
- Claude 在工作时应参考的文档

**示例**:
- `references/finance.md` - 财务模式
- `references/api_docs.md` - API 规范
- `references/schema.md` - 数据库模式
- `references/policies.md` - 公司政策

**使用场景**:
- 数据库模式
- API 文档
- 领域知识
- 公司政策
- 详细工作流指南

**好处**:
- 保持 SKILL.md 精简
- 仅在 Claude 确定需要时加载

**最佳实践**:
- 如果文件很大（> 10k 词），在 SKILL.md 中包含 grep 搜索模式
- 避免重复：信息应存在于 SKILL.md 或 references 文件中，而不是两者都有

### assets/ 目录

**用途**: 不打算加载到上下文中的文件，而是在 Claude 产生的输出中使用。

**何时包含**:
- 技能需要用于最终输出的文件

**示例**:
- `assets/logo.png` - 品牌资源
- `assets/slides.pptx` - PowerPoint 模板
- `assets/frontend-template/` - HTML/React 样板代码
- `assets/font.ttf` - 字体文件

**使用场景**:
- 模板
- 图像、图标
- 样板代码
- 字体
- 被复制或修改的示例文档

**好处**:
- 将输出资源与文档分离
- 使 Claude 能够使用文件而不将其加载到上下文

---

## 最佳实践

### 1. 元数据质量

- **描述具体且包含关键术语**: description 字段决定 Claude 何时使用技能
- **使用第三人称**: "This skill should be used when..." 而不是 "Use this skill when..."
- **包含触发关键词**: 帮助 Claude 识别何时应该使用此技能

### 2. 内容质量

- **正文控制在 500 行以内**: 其他详细信息放在单独文件中
- **术语一致**: 在整个技能中使用一致的术语
- **示例具体**: 提供真实、可操作的示例
- **适当使用渐进式披露**: 工作流程有清晰的步骤

### 3. 脚本质量

- **解决问题而非推卸给 Claude**: 脚本应该完成工作，而不是让 Claude 猜测
- **错误处理明确且有帮助**: 提供清晰的错误消息和处理机制
- **列出所需包**: 在说明中明确列出并验证可用性
- **清晰的文档**: 脚本应该有清晰的文档说明其用途和使用方法

### 4. 工作流设计

- **清晰的步骤**: 工作流程应该有明确的步骤
- **质量关键任务的反馈循环**: 包含验证/验证步骤
- **关键操作的验证步骤**: 确保质量

### 5. 测试和迭代

- **至少创建三个评估**: 使用 Haiku、Sonnet 和 Opus 进行测试
- **使用真实使用场景进行测试**: 不要只测试理论场景
- **纳入团队反馈**: 如果适用，收集团队反馈

---

## 质量检查清单

在分享技能前，验证以下方面：

### 元数据和结构
- [ ] YAML frontmatter 格式正确
- [ ] `name` 字段存在且符合命名规范（小写、连字符）
- [ ] `description` 字段存在且具体（最多 1024 字符）
- [ ] `description` 使用第三人称
- [ ] `description` 包含关键术语
- [ ] 目录结构正确（SKILL.md 必需，其他可选）

### 内容质量
- [ ] SKILL.md 正文在 500 行以内
- [ ] 其他详细信息在单独文件中（references/）
- [ ] 术语一致
- [ ] 示例具体且可操作
- [ ] 适当使用渐进式披露
- [ ] 工作流程有清晰的步骤

### 脚本（如果适用）
- [ ] 脚本解决问题而非推卸给 Claude
- [ ] 错误处理明确且有帮助
- [ ] 所需的包在说明中列出并验证可用
- [ ] 脚本有清晰的文档

### 工作流
- [ ] 关键操作有验证/验证步骤
- [ ] 质量关键任务有反馈循环
- [ ] 工作流程清晰且易于遵循

### 测试
- [ ] 至少创建了三个评估（Haiku、Sonnet、Opus）
- [ ] 使用真实使用场景进行测试
- [ ] 纳入了团队反馈（如果适用）

---

## 创建流程

### Step 1: 理解技能（具体示例）

明确理解技能将如何使用的具体示例。这可以来自：
- 直接的用户示例
- 生成的示例（通过用户反馈验证）

**关键问题**:
- "这个技能应该支持什么功能？"
- "你能给出一些这个技能将如何使用的例子吗？"
- "用户说什么应该触发这个技能？"

### Step 2: 规划可重用技能内容

分析每个示例：
1. 考虑如何从头开始执行示例
2. 识别在执行这些工作流时会有帮助的脚本、参考资料和资源

### Step 3: 初始化技能

使用 `init_skill.py` 脚本创建新技能：

```bash
scripts/init_skill.py <skill-name> --path <output-directory>
```

脚本将：
- 在指定路径创建技能目录
- 生成带有适当 frontmatter 和 TODO 占位符的 SKILL.md 模板
- 创建示例资源目录：`scripts/`、`references/`、`assets/`
- 在每个目录中添加可以自定义或删除的示例文件

### Step 4: 编辑技能

#### 从可重用技能内容开始

实现上面识别的可重用资源：`scripts/`、`references/`、`assets/` 文件。

#### 更新 SKILL.md

回答以下问题：
1. 技能的目的是什么？（几句话）
2. 何时应该使用技能？
3. 在实践中，Claude 应该如何使用技能？应该引用所有上面开发的可重用技能内容，以便 Claude 知道如何使用它们。

### Step 5: 打包技能

使用 `package_skill.py` 脚本打包技能：

```bash
scripts/package_skill.py <path/to/skill-folder>
```

脚本将：
1. **验证** 技能自动检查：
   - YAML frontmatter 格式和必需字段
   - 技能命名约定和目录结构
   - 描述完整性和质量
   - 文件组织和资源引用

2. **打包** 技能（如果验证通过），创建以技能命名的 zip 文件（例如 `my-skill.zip`），包括所有文件并保持适当的目录结构以便分发。

### Step 6: 迭代

在使用技能后，用户可能会请求改进。迭代工作流：
1. 在真实任务上使用技能
2. 注意困难或低效
3. 识别 SKILL.md 或打包资源应如何更新
4. 实施更改并再次测试

---

## 项目中的示例

### 示例 1: artifacts-builder

**特点**:
- 清晰的 YAML frontmatter
- 结构化的步骤说明
- 引用外部资源（shadcn/ui）
- 包含脚本说明

**参考**: `.claude/skills/artifacts-builder/SKILL.md`

### 示例 2: architecture-specialist

**特点**:
- 简洁的描述
- 使用 references/ 目录存储详细文档
- 渐进式披露设计

**参考**: `.claude/skills/architecture-specialist/SKILL.md`

---

## 常见错误

### ❌ 错误示例

```yaml
---
name: My Skill  # 错误：包含空格和大写
description: A skill  # 错误：太模糊，没有触发条件
---
```

```markdown
# My Skill

You should use this skill when...  # 错误：使用第二人称
```

### ✅ 正确示例

```yaml
---
name: my-skill
description: 此技能应在需要处理 PDF 文档旋转、合并或拆分任务时使用。适用于需要批量处理多个 PDF 文件的场景。
---
```

```markdown
# My Skill

此技能应在需要处理 PDF 文档时使用。

## 何时使用此技能

当用户需要旋转、合并或拆分 PDF 文档时，应使用此技能。
```

---

## 参考资源

- [Claude Skills 官方文档](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [Skill Creator 指南](.claude/skills/skill-creator/SKILL.md)
- [模板技能](.claude/skills/template-skill/SKILL.md)

---

## 总结

创建有效的 Skills 的关键是：

1. **清晰的元数据**: 具体、关键词丰富的描述
2. **精简的正文**: < 500 行，核心工作流程
3. **渐进式披露**: 详细信息在 references/ 中
4. **可重用资源**: scripts/ 和 assets/ 用于重复任务
5. **持续迭代**: 基于真实使用场景改进

记住：Skills 是为另一个 Claude 实例使用的。专注于包含对 Claude 有益且不明显的程序性知识、领域特定细节或可重用资源。

