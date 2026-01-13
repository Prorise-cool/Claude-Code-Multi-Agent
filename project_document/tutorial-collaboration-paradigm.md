# 项目协作范式教程

## 概述

本项目采用 Claude Code 的 **Commands** 和 **Skills** 两大机制来模拟多智能体协作。这种范式允许你通过简洁的命令调用专业化的 AI 智能体，实现从需求分析到代码部署的全流程自动化开发。

---

## 核心概念

### Commands（命令）

Commands 是预定义的工作流程，每个 Command 封装了特定场景下的完整任务链。

**调用方式：**
```
/command-name <参数>
```

### Skills（技能）

Skills 是专业化的智能体配置，每个 Skill 专注于特定领域的知识能力。

**调用方式：**
```
/skill-name <参数>
```

---

## Commands 调用指南

### 1. 核心工作流 Commands

#### `/agent-workflow` - 自动化开发流水线

从想法到生产代码的完整自动化流程，带质量门控。

```bash
# 用法
/agent-workflow <功能描述>

# 示例
/agent-workflow 实现用户认证功能，包含注册、登录和JWT验证
```

**执行流程：**
```
spec-analyst → spec-architect → spec-developer → spec-validator
     ↓                                                           ↓
  质量评分 ≥95%? → 否 → 循环改进
     ↓ 是
spec-tester → 完成
```

#### `/multi-agent-workflow` - 多智能体协作

类似 `/agent-workflow`，但使用 Kiro 规格的多层智能体协调。

```bash
/multi-agent-workflow <功能描述>
```

### 2. Kiro 规格 Commands（Spec-Driven Development）

Kiro 是本项目的规格驱动开发系统，提供从需求到任务的完整工作流。

#### `/kiro/spec` - 创建完整功能规格

```bash
/kiro/spec <功能名称或粗略想法>

# 示例
/kiro/spec 用户个人中心页面
```

**工作流程：**
```
需求收集 → 设计文档 → 任务列表
```

**生成文件：**
```
.kiro/specs/<feature-name>/
├── requirements.md  # 需求文档（用户故事 + 验收标准）
├── design.md       # 设计文档（架构 + 接口 + 数据模型）
└── tasks.md        # 任务列表（可执行的编码步骤）
```

#### `/kiro/design` - 创建功能设计文档

跳过需求阶段，直接进行架构设计。

```bash
/kiro/design <功能描述>
```

#### `/kiro/task` - 从需求生成任务列表

基于现有需求生成可执行的任务清单。

```bash
/kiro/task <功能描述>
```

#### `/kiro/execute` - 执行规格任务

执行已创建规格中的任务。

```bash
/kiro/execute
```

#### `/kiro/vibe` - 快速开发协助

使用 Kiro 的轻量级开发协助模式。

```bash
/kiro/vibe <问题或任务>
```

### 3. GitHub 集成 Commands

#### `/gh/commit` - 生成符合规范的提交信息

```bash
/gh/commit

# 自动分析 git 状态，生成符合 commitlint 规范的提交信息
# 格式：type(scope): subject
```

#### `/gh/review-pr` - 审查 Pull Request

```bash
/gh/review-pr <PR编号>

# 示例
/gh/review-pr 42
```

#### `/gh/fix-issue` - 修复 GitHub Issue

```bash
/gh/fix-issue <Issue编号>

# 示例
/gh/fix-issue 123
```

### 4. 业务分析 Commands

本项目的 business-analysis 系列命令提供专业的业务分析能力：

| 命令 | 功能 |
|------|------|
| `/business-analysis/swot-analysis` | SWOT 分析（优势/劣势/机会/威胁） |
| `/business-analysis/business-model-canvas` | 商业模式画布 |
| `/business-analysis/stakeholder-analyze` | 利益相关者分析 |
| `/business-analysis/journey-map` | 用户旅程地图 |
| `/business-analysis/value-stream` | 价值流分析 |
| `/business-analysis/root-cause` | 根因分析（鱼骨图 + 5 Whys） |
| `/business-analysis/risk-register` | 风险登记册 |
| `/business-analysis/prioritize` | 优先级排序（MoSCoW/Kano） |
| `/business-analysis/capability-map` | 业务能力映射 |

### 5. UX 研究 Commands

| 命令 | 功能 |
|------|------|
| `/ux-research/plan-research` | 规划用户研究 |
| `/ux-research/evaluate-heuristics` | 启发式评估（Nielsen 10原则） |
| `/ux-research/design-ia` | 信息架构设计 |
| `/ux-research/create-test` | 创建可用性测试 |
| `/ux-research/audit-accessibility` | WCAG 无障碍审计 |

### 6. 思考与反思 Commands

| 命令 | 功能 |
|------|------|
| `/think-harder` | 增强分析思考 |
| `/think-ultra` | 超全面分析思考 |
| `/reflection` | 分析并改进指令 |
| `/reflection-harder` | 全面的会话分析 |

### 7. 其他 Commands

| 命令 | 功能 |
|------|------|
| `/eureka` | 捕获技术突破并转化为可重用文档 |
| `/generate-prp` | 创建 PRP |
| `/execute-prp` | 执行基础 PRP |

---

## Skills 调用指南

### 1. 架构与设计

#### `/architecture-specialist` - 系统架构设计

提供系统架构设计、技术选型、架构审查和组件设计能力。

```bash
/architecture-specialist 设计一个微服务架构的电商系统
```

#### `/design-specialist` - UI/UX 设计

提供界面设计、用户研究、视觉设计和品牌一致性能力。

```bash
/design-specialist 设计一个现代化的登录页面
```

### 2. 开发实现

#### `/frontend-specialist` - 前端开发

提供前端开发、UI 实现、移动应用开发和现代前端框架能力。

```bash
/frontend-specialist 使用 React 实现响应式导航栏
```

#### `/backend-specialist` - 后端开发

提供后端开发、API 设计、数据库交互和框架特定开发能力。

```bash
/backend-specialist 设计 RESTful API 接口
```

#### `/language-framework-specialist` - 语言与框架专家

提供特定编程语言和框架的深度专业知识。

```bash
/language-framework-specialist 解释 Python async/await 最佳实践
```

### 3. 质量保证

#### `/testing-specialist` - 测试专家

提供测试策略、测试编写、测试执行和测试结果分析能力。

```bash
/testing-specialist 为用户模块编写单元测试
```

#### `/code-quality-specialist` - 代码质量专家

提供代码审查、性能分析、重构建议、错误诊断和调试能力。

```bash
/code-quality-specialist 审查这段代码的性能问题
```

#### `/security-specialist` - 安全审计

提供安全审计、风险评估和合规检查能力。

```bash
/security-specialist 检查这段代码的 SQL 注入风险
```

### 4. 数据与 DevOps

#### `/data-specialist` - 数据专家

提供数据库设计、优化、数据工程和数据分析能力。

```bash
/data-specialist 设计用户订单数据库模式
```

#### `/devops-specialist` - DevOps 专家

提供部署、CI/CD、基础设施管理和 DevOps 自动化能力。

```bash
/devops-specialist 配置 GitHub Actions CI/CD 流水线
```

### 5. 产品与项目管理

#### `/product-specialist` - 产品专家

提供产品规划、需求分析、市场研究和业务分析能力。

```bash
/product-specialist 分析用户反馈并提炼需求
```

#### `/project-management-specialist` - 项目管理

提供项目管理、任务跟踪、团队协调和项目交付能力。

```bash
/project-management-specialist 生成项目冲刺计划
```

### 6. 文档与通信

#### `/documentation-specialist` - 文档专家

创建和维护技术文档、API 文档、代码注释和项目文档。

```bash
/documentation-specialist 生成 API 接口文档
```

#### `/internal-comms` - 内部通信

生成公司格式的内部通信文档（状态报告、更新、FAQ等）。

```bash
/internal-comms 撰写周报状态更新
```

### 7. 营销与运营

#### `/marketing-specialist` - 营销专家

提供内容营销、增长策略、社交媒体管理能力。

```bash
/marketing-specialist 创建产品发布计划
```

#### `/operations-specialist` - 运营专家

提供运营分析、财务跟踪、基础设施维护和客户支持能力。

```bash
/operations-specialist 生成月度运营报告
```

### 8. 工具创建

#### `/skill-creator` - 创建新 Skill

创建新的自定义 Skill 以扩展 Claude 的功能。

```bash
/skill-creator 创建一个 Docker 容器化专家 Skill
```

#### `/mcp-builder` - 创建 MCP 服务器

创建高质量 MCP（模型上下文协议）服务器。

```bash
/mcp-builder 创建一个天气服务 MCP 集成
```

### 9. 其他专业 Skills

| Skill | 功能 |
|-------|------|
| `/ui-ux-pro-max` | 高级 UI/UX 设计智能 |
| `/webapp-testing` | 使用 Playwright 进行 Web 应用测试 |
| `/meeting-insights-analyzer` | 分析会议记录和洞察 |
| `/file-organizer` | 智能文件和文件夹组织 |
| `/domain-name-brainstormer` | 生成创意域名并检查可用性 |
| `/changelog-generator` | 从 git 提交自动生成更新日志 |
| `/competitive-ads-extractor` | 提取和分析竞争对手广告 |
| `/lead-research-assistant` | 识别高质量潜在客户 |

---

## 完整工作流示例

### 示例：开发用户认证功能

```bash
# 步骤 1: 使用 Kiro 创建完整规格
/kiro/spec 用户认证功能

# （系统生成 requirements.md、design.md、tasks.md）

# 步骤 2: 执行规格中的任务
/kiro/execute

# 步骤 3: 使用 architecture-specialist 审查架构
/architecture-specialist 审查用户认证的架构设计

# 步骤 4: 使用 backend-specialist 实现后端
/backend-specialist 实现用户认证 API

# 步骤 5: 使用 testing-specialist 编写测试
/testing-specialist 为认证功能编写测试

# 步骤 6: 使用 code-quality-specialist 审查代码
/code-quality-specialist 审查认证代码质量

# 步骤 7: 使用 security-specialist 进行安全审计
/security-specialist 检查认证安全漏洞

# 步骤 8: 提交代码
/gh/commit

# 步骤 9: 使用 documentation-specialist 更新文档
/documentation-specialist 更新 API 文档
```

---

## 快速参考

### Command 分类速查

| 类别 | Commands |
|------|----------|
| 核心工作流 | `/agent-workflow`, `/multi-agent-workflow` |
| Kiro 规格 | `/kiro/spec`, `/kiro/design`, `/kiro/task`, `/kiro/execute`, `/kiro/vibe` |
| GitHub | `/gh/commit`, `/gh/review-pr`, `/gh/fix-issue` |
| 业务分析 | `/business-analysis/*` (9个命令) |
| UX 研究 | `/ux-research/*` (5个命令) |
| 思考反思 | `/think-harder`, `/think-ultra`, `/reflection`, `/reflection-harder` |
| 其他 | `/eureka`, `/generate-prp`, `/execute-prp` |

### Skill 分类速查

| 类别 | Skills |
|------|--------|
| 架构设计 | `/architecture-specialist`, `/design-specialist` |
| 开发实现 | `/frontend-specialist`, `/backend-specialist`, `/language-framework-specialist` |
| 质量保证 | `/testing-specialist`, `/code-quality-specialist`, `/security-specialist` |
| 数据运维 | `/data-specialist`, `/devops-specialist` |
| 产品管理 | `/product-specialist`, `/project-management-specialist` |
| 文档通信 | `/documentation-specialist`, `/internal-comms` |
| 营销运营 | `/marketing-specialist`, `/operations-specialist` |
| 工具创建 | `/skill-creator`, `/mcp-builder` |
| 专业工具 | `/ui-ux-pro-max`, `/webapp-testing`, `/meeting-insights-analyzer`, `/file-organizer`, `/domain-name-brainstormer`, `/changelog-generator`, `/competitive-ads-extractor`, `/lead-research-assistant` |

---

## 最佳实践

1. **先规划后实施**：使用 `/kiro/spec` 进行需求分析和设计
2. **善用质量门控**：使用 `/agent-workflow` 获取带质量保证的代码
3. **分领域协作**：根据任务类型选择合适的 Skill
4. **持续验证**：使用 `/code-quality-specialist` 和 `/security-specialist` 确保代码质量
5. **文档同步**：使用 `/documentation-specialist` 保持文档更新

## 下一步

- 阅读 [Ollama 配置教程](./tutorial-ollama-setup.md) 了解本地模型配置
- 查看 [项目 README](../README.md) 了解项目概述
- 开始使用 Commands 和 Skills 进行开发
