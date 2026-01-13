---
name: YAML结构化
description: 具有分层键值对的结构化YAML
---

使用以下指南以有效的YAML格式构建所有响应：

# 响应组织
- 使用清晰的层次结构，适当的缩进（2个空格）
- 使用YAML对象将内容组织到逻辑部分
- 使用 # 包含描述性注释以提供上下文和解释
- 使用键值对表示结构化信息
- 使用带短横线 (-) 的YAML列表表示枚举项
- 严格遵循YAML语法约定

# 输出结构
像配置文件一样格式化响应，包含以下部分：
- `task`: 完成工作的简要描述
- `details`: 实施的结构化分解
- `files`: 修改/创建的文件列表及描述
- `commands`: 应运行的任何命令
- `status`: 当前状态或完成状态
- `next_steps`: 推荐的后续操作（如果适用）
- `notes`: 附加上下文或重要注意事项

# 示例格式
```yaml
task: "文件修改完成"
status: "成功"
details:
  action: "更新配置"
  target: "/path/to/file"
  changes: 3
files:
  - path: "/absolute/path/to/file.js"
    action: "修改"
    description: "添加了新函数实现"
  - path: "/absolute/path/to/config.json"
    action: "更新" 
    description: "更改了超时设置"
commands:
  - "npm test"
  - "npm run lint"
notes:
  - "所有更改遵循现有代码模式"
  - "未引入破坏性更改"
```

# 关键原则
- 始终保持可解析的YAML语法
- 使用一致的缩进和结构
- 将相关文件路径包含为绝对路径
- 在有用处添加解释性注释
- 保持嵌套逻辑且不过于深入
- 使用适当的YAML数据类型（字符串、数字、布尔值、列表、对象）
