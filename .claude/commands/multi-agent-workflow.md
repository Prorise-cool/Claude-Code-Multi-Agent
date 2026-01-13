---
description: "基于 Kiro 规格的多层智能代理协调工作流"
allowed-tools: ["Task", "Read", "Write", "Edit", "MultiEdit", "Grep", "Glob", "TodoWrite"]
---

# Multi-Agent Workflow - 多层智能代理协调系统

基于Kiro规格文件实现的多层代理协调工作流，自动选择和调度专业代理团队。

## 用法

```bash
/multi-agent-workflow <功能名称>
```

## 上下文

- 功能特性名称: $ARGUMENTS
- 自动读取 `.kiro/specs/{feature}/` 下的三个文件
- 智能代理选择和多层任务分发
- 统一TODO.md管理和Hook驱动执行

## 你的角色

您是多层代理协调系统的总指挥官，负责：

1. 读取和分析Kiro规格文件
2. 智能选择和组建专业代理团队
3. 协调三层代理执行架构
4. 管理统一的TODO任务列表
5. 监督整个项目执行进度

## 三层代理架构

### 第一层：总协调器 (Orchestrator)

```
spec-orchestrator - 总指挥官，负责整体策略制定和代理团队组建
```

### 第二层：领域专家主管 (Domain Specialists)

基于分析结果动态选择需要的专家主管：

```
spec-analyst     → 需求分析领域主管
spec-architect   → 系统架构领域主管  
spec-planner     → 实施规划领域主管
spec-developer   → 开发实施领域主管
spec-reviewer    → 代码审查领域主管
spec-validator   → 质量验证领域主管
spec-tester      → 测试专家领域主管
spec-task-reviewer → 任务监督领域主管
```

### 第三层：专业执行代理 (Professional Agents)

从100个专业代理中智能选择，包括：

```
engineering/    → 前端、后端、移动端开发专家
databases/      → 数据工程、数据库管理专家
design/         → UI/UX设计、品牌设计专家
testing/        → 自动化测试、性能测试专家
deployment/     → 部署、运维、安全专家
marketing/      → 增长、内容、社交媒体专家
```

## 工作流程步骤

### 🔍 Step 1: 读取Kiro规格文件

首先读取指定特性的Kiro规格文件：

```
.kiro/specs/{$ARGUMENTS}/requirements.md  - 需求规格
.kiro/specs/{$ARGUMENTS}/design.md        - 设计文档  
.kiro/specs/{$ARGUMENTS}/tasks.md         - 任务列表
```

### 🧠 Step 2: 总协调器分析

使用 **spec-orchestrator** 子代理分析：

- 项目复杂度和技术栈需求
- 需要的专业领域和技能组合
- 预估工作量和时间安排
- 推荐的代理团队组合

### 🎯 Step 3: 智能代理选择

基于分析结果从agent-capability-map.json中选择：

- **核心领域专家**：必须参与的specialist
- **专业执行代理**：具体执行任务的专家
- **支持代理**：辅助和检查的专家

### 📋 Step 4: 创建统一TODO

创建/更新 `TODO.md` 包含：

- 项目总体进度概览
- 各代理分配的具体任务
- 任务依赖关系和执行顺序
- 实时状态追踪

### 🚀 Step 5: 启动多层执行

按层级启动代理执行：

1. **spec-orchestrator** 制定总体执行策略
2. **选定的specialist主管** 细化各领域任务
3. **专业执行代理** 并行执行具体任务
4. **spec-task-reviewer** 持续监督和触发

### 🔄 Step 6: Hook驱动自动化

通过Claude Code Hooks实现：

- 任务完成自动标记TODO
- 触发下一个任务执行
- 实时进度更新和通知
- 异常处理和错误恢复

## 预期输出结构

```
project/
├── TODO.md                 # 统一任务管理
├── .kiro/specs/{feature}/  # Kiro规格文件
├── .claude/
│   ├── agent-assignments.json  # 代理分配记录
│   └── execution-log.json      # 执行日志
├── src/                    # 源代码
├── tests/                  # 测试文件
└── docs/                   # 文档文件
```

## 核心优势

- **智能代理选择**：基于需求自动匹配最合适的专家团队
- **分层协调管理**：三层架构确保高效协作和质量控制
- **统一任务管理**：TODO.md集中管理所有任务状态
- **Hook驱动自动化**：任务完成自动触发后续流程
- **实时进度追踪**：可视化项目进度和代理状态

---

## 执行流程

**功能特性**: $ARGUMENTS

开始多层智能代理协调工作流...

### 🔍 阶段1: 读取Kiro规格文件

正在读取 `.kiro/specs/{$ARGUMENTS}/` 下的规格文件：

- requirements.md - 需求规格和验收标准
- design.md - 系统架构和技术设计
- tasks.md - 实施任务和优先级

### 🧠 阶段2: 总协调器分析

使用 **spec-orchestrator** 子代理进行深度分析：

- 分析项目技术复杂度和团队需求
- 识别关键技术栈和专业领域
- 评估工作量和资源分配
- 制定代理团队组建策略

### 🎯 阶段3: 智能代理选择

基于分析结果智能选择代理团队：

- 从9个specialist中选择必要的领域主管
- 从100个专业代理中匹配执行专家
- 建立代理协作关系和沟通机制

### 📋 阶段4: 创建统一TODO管理

生成统一的TODO.md任务管理文件：

- 项目总体进度和里程碑
- 各代理的具体任务分配
- 任务依赖关系和执行时序
- Hook触发点和自动化流程

### 🚀 阶段5: 启动多层执行链

按照三层架构启动代理执行：

1. spec-orchestrator 总体协调
2. 选定specialist 领域深化
3. 专业代理 并行执行
4. spec-task-reviewer 持续监督

### 🔄 阶段6: Hook驱动自动化

激活Claude Code Hooks实现：

- PostToolUse: 任务完成自动更新TODO
- Subagent Stop: 触发下一任务执行
- Notification: 进度通知和异常提醒

**现在开始执行多层代理协调工作流！**
