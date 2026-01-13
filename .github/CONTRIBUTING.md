# 为 Claude Code Multi-Agent 做贡献

首先，感谢您考虑为 Claude Code Multi-Agent 做贡献！正是像您这样的人使这个项目成为一个如此出色的工具。

## 目录

- [行为准则](#行为准则)
- [开始使用](#开始使用)
- [我如何贡献？](#我如何贡献)
- [开发环境设置](#开发环境设置)
- [拉取请求流程](#拉取请求流程)
- [风格指南](#风格指南)
- [创建技能](#创建技能)
- [创建命令](#创建命令)

## 行为准则

本项目以及参与其中的每个人都受我们的[行为准则](CODE_OF_CONDUCT.md)约束。通过参与，您应该遵守此准则。

## 开始使用

1. Fork 仓库
2. 在本地克隆您的 fork
3. 设置开发环境（参见[开发环境设置](#开发环境设置)）
4. 为您的更改创建一个分支
5. 进行您的更改
6. 测试您的更改
7. 提交拉取请求

## 我如何贡献？

### 报告 Bug

在创建 bug 报告之前，请检查现有问题以避免重复。创建 bug 报告时，请使用我们的[bug 报告模板](.github/ISSUE_TEMPLATE/bug_report.yml)尽可能多地包含详细信息。

### 建议功能

欢迎功能建议！请使用我们的[功能请求模板](.github/ISSUE_TEMPLATE/feature_request.yml)提交您的想法。

### 创建新技能

技能是本项目的核心。如果您在特定领域有专业知识，请考虑创建新技能！有关指南，请参见[创建技能](#创建技能)。

### 创建新命令

命令定义了用户可以触发的工作流。有关指南，请参见[创建命令](#创建命令)。

### 改进文档

欢迎文档改进。这包括：
- 修复拼写错误
- 澄清现有文档
- 添加示例
- 翻译文档

### 代码贡献

我们欢迎以下方面的代码贡献：
- Bug 修复
- 新功能
- 性能改进
- 测试覆盖率改进

## 开发环境设置

### 先决条件

- Python 3.8+
- [uv](https://github.com/astral-sh/uv) - Python 包管理器
- [Ollama](https://ollama.com/) - 本地 LLM 运行时
- Git

### 设置步骤

```bash
# 1. 克隆您的 fork
git clone https://github.com/YOUR_USERNAME/Claude-Code-Multi-Agent.git
cd Claude-Code-Multi-Agent

# 2. 安装依赖
uv sync

# 3. 复制环境文件
cp .env.example .env

# 4. 配置环境
# 使用您的设置编辑 .env

# 5. 拉取 Ollama 模型
ollama pull gemma3:1b

# 6. 验证设置
uv run python -c "print('设置完成！')"
```

### 运行测试

```bash
# 运行所有测试
uv run pytest

# 运行特定测试文件
uv run pytest tests/test_hooks.py

# 运行覆盖率测试
uv run pytest --cov=.claude/hooks
```

## 拉取请求流程

1. **创建分支**
   ```bash
   git checkout -b feature/your-feature-name
   # 或
   git checkout -b fix/your-bug-fix
   ```

2. **进行更改**
   - 遵循[风格指南](#风格指南)
   - 为新功能编写测试
   - 根据需要更新文档

3. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

   遵循[约定式提交](https://www.conventionalcommits.org/)：
   - `feat:` - 新功能
   - `fix:` - Bug 修复
   - `docs:` - 文档更改
   - `style:` - 代码风格更改（格式化等）
   - `refactor:` - 代码重构
   - `test:` - 添加或更新测试
   - `chore:` - 维护任务

4. **推送到您的 Fork**
   ```bash
   git push origin feature/your-feature-name
   ```

5. **创建拉取请求**
   - 使用 PR 模板
   - 链接相关问题
   - 请求维护者审查

6. **处理审查反馈**
   - 进行请求的更改
   - 推送额外的提交
   - 准备就绪时重新请求审查

## 风格指南

### Python 代码风格

- 遵循 PEP 8
- 尽可能使用类型提示
- 最大行长度：100 个字符
- 使用有意义的变量名
- 为公共函数添加文档字符串

```python
def process_hook_result(result: dict, context: HookContext) -> HookResponse:
    """
    处理来自 hook 执行的结果。

    Args:
        result: 来自 hook 执行的原始结果字典
        context: 当前的 hook 上下文

    Returns:
        HookResponse: 处理后的响应对象
    """
    # 实现
```

### Markdown 风格

- 使用 ATX 风格标题（`#`、`##` 等）
- 使用带语言标识符的代码块
- 尽可能保持行长度在 120 个字符以内
- 对重复的 URL 使用引用式链接

### 提交消息

- 使用现在时（"添加功能"而不是"已添加功能"）
- 使用祈使语气（"将光标移动到..."而不是"将光标移动到..."）
- 将第一行限制在 72 个字符以内
- 在正文中引用问题和 PR

## 创建技能

技能是提供领域专业知识的专业代理。要创建新技能：

### 1. 创建目录结构

```
.claude/skills/your-skill-name/
├── SKILL.md                    # 必需：技能定义
└── references/                 # 可选：参考文档
    ├── guide1.md
    └── guide2.md
```

### 2. 编写 SKILL.md

```markdown
---
name: your-skill-name
description: 此技能功能的简要描述
version: 1.0.0
author: 您的姓名
---

# 您的技能名称

技能的详细描述及其目的。

## 何时使用此技能

- 用例 1
- 用例 2
- 用例 3

## 能力

### 能力 1
此能力的描述。

📖 [参考文档](./references/guide1.md)

### 能力 2
此能力的描述。

📖 [参考文档](./references/guide2.md)
```

### 3. 添加参考文档

在 `references/` 文件夹中包含相关指南、最佳实践和示例。

### 4. 测试您的技能

- 使用各种提示进行测试
- 验证技能是否正确加载
- 检查引用是否可访问

## 创建命令

命令定义可重用的工作流。要创建新命令：

### 1. 创建命令文件

```
.claude/commands/your-command/
└── your-command.md
```

### 2. 编写命令定义

```markdown
---
name: your-command
description: 此命令的功能
---

# 您的命令

调用此命令时 Claude 应遵循的说明。

## 步骤

1. 第一步
2. 第二步
3. 第三步

## 输出

预期输出的描述。
```

### 3. 测试您的命令

- 测试命令工作流
- 验证所有步骤是否正确执行
- 检查输出格式

## 有问题？

如果您对贡献有疑问，请随时：
- 开启[讨论](https://github.com/Prorise-cool/Claude-Code-Multi-Agent/discussions)
- 在问题中提问
- 联系维护者

感谢您的贡献！
