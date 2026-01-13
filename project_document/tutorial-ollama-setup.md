# Ollama 配置教程

## 概述

Ollama 是本项目中用于本地代码总结的核心模型服务。通过配置 Ollama，可以在本地运行轻量级语言模型，为 Claude Code 提供快速的代码理解、文档生成和上下文总结能力。

## 推荐模型：gemma3:1b

**为什么选择 gemma3:1b？**

- **轻量级**：仅需约 1GB 内存占用
- **响应迅速**：本地推理，无需网络请求
- **性价比高**：在资源受限环境下表现优异
- **开源免费**：Google Gemma 系列模型

## 安装步骤

### 1. 安装 Ollama

#### Windows

```powershell
# 使用 PowerShell
winget install Ollama.Ollama

# 或访问官网下载安装包
# https://ollama.com/download
```

#### macOS

```bash
brew install ollama
```

#### Linux

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

### 2. 启动 Ollama 服务

安装完成后，Ollama 服务会自动启动。你可以通过以下命令验证：

```bash
# 检查服务状态
ollama --version

# 预期输出：
# ollama version is 0.1.x
```

### 3. 下载推荐模型

```bash
# 下载 gemma3:1b 模型（推荐）
ollama pull gemma3:1b

# 验证模型安装
ollama list

# 预期输出应包含：
# NAME                ID              SIZE    MODIFIED
# gemma3:1b           xxx...xxx       1.0GB   2024-xx-xx
```

### 4. 测试模型

```bash
# 交互式测试
ollama run gemma3:1b

# 输入测试问题：
# > 请用一句话解释什么是递归？
#
# 预期会收到模型的回复
```

## 项目配置

### 1. 创建环境变量文件

在项目根目录下创建 `.env` 文件：

```bash
# 复制示例配置文件
cp .env.example .env
```

### 2. 配置 Ollama 模型

编辑 `.env` 文件，设置以下变量：

```env
# ===== Ollama 模型配置 =====
# 指定使用的模型名称
OLLAMA_MODEL=gemma3:1b

# 可选：设置 Ollama API 端点（默认为 http://localhost:11434）
# OLLAMA_API_BASE=http://localhost:11434

# 可选：设置超时时间（秒）
# OLLAMA_TIMEOUT=30
```

### 3. 验证配置

```bash
# 确保 Ollama 服务正在运行
# Windows: 在服务管理器中查看 Ollama 服务状态
# macOS/Linux: pgrep ollama

# 测试 API 连接
curl http://localhost:11434/api/tags

# 预期返回已安装的模型列表
```

## 项目中使用

Ollama 配置完成后，项目中的以下功能会自动使用本地模型：

| 功能 | 描述 |
|------|------|
| **代码总结** | 自动生成代码片段的简洁摘要 |
| **文档生成** | 基于代码结构生成技术文档 |
| **上下文压缩** | 压缩长对话历史以节省 Token |
| **问题分析** | 快速理解代码问题并提供建议 |

## 可选：其他模型

如果你需要更强的能力，可以考虑以下替代模型：

```bash
# 2B 参数版本（更强，但需要更多资源）
ollama pull gemma3:2b

# 4B 参数版本（更强，适合开发环境）
ollama pull gemma3:4b

# 修改 .env 文件中的 OLLAMA_MODEL 变量即可切换
```

**模型对比：**

| 模型 | 内存占用 | 推荐场景 |
|------|----------|----------|
| gemma3:1b | ~1GB | 资源受限环境、快速响应 |
| gemma3:2b | ~2GB | 日常开发、平衡性能 |
| gemma3:4b | ~4GB | 复杂任务、高质量输出 |

## 常见问题

### Q1: Ollama 服务无法启动？

```bash
# Windows: 以管理员身份运行 PowerShell，重启服务
Restart-Service Ollama

# macOS/Linux
ollama serve
```

### Q2: 模型下载失败？

```bash
# 使用镜像加速（如适用）
# 或手动下载后放置到 Ollama 模型目录
# Windows: C:\Users\<用户名>\.ollama\models
# macOS/Linux: ~/.ollama/models
```

### Q3: 如何查看 Ollama 日志？

```bash
# Windows: 事件查看器 -> 应用程序和服务日志 -> Ollama
# macOS: Console.app -> 搜索 "ollama"
# Linux: journalctl -u ollama -f
```

## 下一步

配置完成后，你可以：

1. 阅读 [项目协作范式教程](./tutorial-collaboration-paradigm.md) 了解如何使用 Commands 和 Skills
2. 查看 [项目 README](../README.md) 了解项目概述
3. 开始使用 Claude Code 进行开发
