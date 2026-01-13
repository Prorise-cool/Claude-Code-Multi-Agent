# MCP 配置说明（Windows 示例）

本项目使用 Claude Code 的 **Model Context Protocol（MCP）** 扩展能力，通过 `.mcp.json` 统一配置多个外部服务（代码索引、搜索、数据库、浏览器控制等）。本节以当前的 **Windows** 配置为例进行说明，并指出需要你手动填写的 **凭证类字段** 与 **本地路径**，以便安全地在自己电脑上启用这些能力。

## 1. `.mcp.json` 放在哪儿？

- **文件位置**：项目根目录下的 `.mcp.json`（已随仓库提供）
- **作用**：当你在该项目目录中启动 Claude Code 时，会自动加载这里声明的 `mcpServers`，为本项目启用相应的工具
- **可移植性**：当前示例以 **Windows + PowerShell / cmd** 为主（大量使用 `cmd` 和 Windows 盘符路径），如需在 macOS / Linux 上使用，可以参考本文件末尾的适配建议进行修改

---

## 2. 当前内置的 MCP 服务概览

下面对 `.mcp.json` 中的每个 `mcpServers` 项做一个简要说明，并标出是否需要你手动配置 **token / key / 密码 / 路径**。

- **Context7**
  - **用途**：代码/库相关文档与示例搜索（依赖 Context7 MCP）
  - **配置片段**：`"command": "cmd", "args": ["/c", "npx", "-y", "@upstash/context7-mcp@latest"]`
  - **手动配置**：通常需要在本地环境变量或 Context7 配置中设置 API Key（不放在仓库里）

- **AceMCP (代码索引)**
  - **用途**：为本地项目建立代码索引，支持更快的代码搜索与跳转
  - **配置片段**：`"command": "npx", "args": ["-y", "acemcp-node"]`
  - **手动配置**：无必填密钥，一般只需要保证 `node` / `npx` 可用

- **Exa AI (搜索)**
  - **用途**：通过 Exa AI 进行联网搜索
  - **配置片段**：HTTP 类型 MCP：`"type": "http", "url": "https://mcp.exa.ai/mcp"`
  - **手动配置**：如果需要私有 key，建议通过 Claude / Exa 官方文档配置到环境变量或单独的本地设置文件，而不是 `.mcp.json` 中

- **mcp-feedback-enhanced**
  - **用途**：图形化/网页方式的交互反馈面板
  - **重要参数**：
    - `MCP_WEB_HOST`, `MCP_WEB_PORT`：Web UI 监听地址和端口
    - `MCP_DESKTOP_MODE`: `"true"` 表示桌面模式
  - **手动配置**：如端口被占用，可自行修改 `MCP_WEB_PORT`

- **Sequential Thinking**
  - **用途**：链式思维 / 多步推理工具
  - **配置片段**：`"args": ["/c", "npx", "@modelcontextprotocol/server-sequential-thinking"]`
  - **手动配置**：无敏感字段

- **Shrimp Task Manager**
  - **用途**：任务拆分 / 进度管理 MCP
  - **配置片段**：`"args": ["/c", "npx", "mcp-shrimp-task-manager"]`
  - **手动配置**：无敏感字段

- **everything-search**
  - **用途**：基于 Everything 的本地文件极速搜索
  - **关键配置**：
    - `EVERYTHING_SDK_PATH`: `E:\\everythingsdk\\dll\\Everything64.dll`
  - **手动配置（重要）**：
    - 需要你在本机安装 Everything SDK，并把 `Everything64.dll` 的实际路径填入
    - 路径必须存在，否则 MCP 无法启动
    - **理由**：避免 MCP 拥有你电脑所有盘符的默认访问，需要你显式告知允许访问的 SDK 路径（安全 + 可移植）

- **github**
  - **用途**：通过 GitHub MCP 读写 Issue / PR / 仓库信息等
  - **敏感字段（必须手动填）**：
    - `env.GITHUB_PERSONAL_ACCESS_TOKEN: ""`
  - **填写方式建议**：
    - 在本地创建 GitHub PAT（仅赋予必要权限，如 `repo` 范围）
    - 将 token 填入本机 `.mcp.json` 或更安全地放入用户级配置文件（如 `~/.claude/settings.local.json`），仓库中的默认值应保持为空字符串

- **filesystem**
  - **用途**：向 Claude 暴露本机部分目录，使其可以读写这些路径下的文件
  - **关键配置**：
    - `args` 中传入了多个允许访问的根目录：
      - `D:\\`
      - `C:\\Users\\Prorise\\Desktop`
      - `E:\\`
  - **手动配置（强烈推荐）**：
    - 根据你自己的电脑情况修改这几个路径：
      - 只暴露 **工作目录** 或某几个专门的数据盘（例如：`D:\\Projects`、`C:\\Users\\<你的用户名>\\Desktop\\SomeFolder`）
      - **不要** 无脑暴露整个系统盘或含有隐私/生产数据的目录
    - **配置理由**：
      - `filesystem` MCP 决定了 Claude 在本机可以“看见”和“操作”哪些文件，是最敏感的权限之一
      - 明确限制为少数目录可以大大减少误操作和隐私泄露的风险

- **magic**
  - **用途**：调用 `@21st-dev/magic` 提供的能力（例如 UI 相关工具等）
  - **敏感字段（必须手动填）**：
    - `env.API_KEY: ""`
  - **说明**：从对应服务获取 API Key 后，本地填写；仓库默认留空

- **playwright**
  - **用途**：通过 Playwright MCP 驱动浏览器（端到端测试、页面自动化等）
  - **关键点**：
    - `type: "stdio"`，通过标准输入输出通信
  - **手动配置**：
    - 保证本机已安装需要的浏览器驱动，可以按官方文档执行 `npx playwright install`

- **memory**
  - **用途**：简单的本地记忆存储 MCP
  - **关键配置**：
    - `MEMORY_FILE_PATH: "C:\\Users\\Prorise\\memory\\memory.json"`
  - **手动配置**：
    - 建议修改为自己机器上存在且可写的路径，例如：
      - `C:\\Users\\<你的用户名>\\AppData\\Local\\ClaudeMemory\\memory.json`
    - 确保父目录存在；否则先创建对应目录
  - **配置理由**：
    - 避免把记忆文件写到不存在或无权限的路径导致报错
    - 也可以选择将记忆文件放在加密磁盘或专门的数据目录中

- **docker**
  - **用途**：通过 MCP 操作本地 Docker（查看容器、镜像等）
  - **前提**：本机需要安装并运行 Docker
  - **手动配置**：一般无需额外 env，按需修改

- **mysql**
  - **用途**：连接本地或远程 MySQL 数据库
  - **敏感配置（默认是 demo / 请自行替换）**：
    - `MYSQL_HOST: "localhost"`
    - `MYSQL_PORT: "3306"`
    - `MYSQL_USER: "root"`
    - `MYSQL_PASS: "root"`
    - `MYSQL_DB: "security"`
  - **强烈建议**：
    - 不要在真实生产中使用 `root / root` 这样的弱密码
    - 如果连接线上数据库，优先通过本机环境变量或用户级配置设置这些字段，不要提交到仓库

- **magic-ui**
  - **用途**：`magicui-mcp` 相关工具（UI 辅助）
  - **手动配置**：一般无需额外 env

- **time-mcp**
  - **用途**：时间/日期相关的简单工具
  - **手动配置**：无

- **redis-mcp**
  - **用途**：连接 Redis 实例
  - **当前配置**（示例）：
    - host: `localhost`
    - port: `6379`
    - `--password`: `""`（为空）
    - `--db`: `"0"`
    - `--username`: `"root"`
  - **注意事项**：
    - 如果你的 Redis 有密码，务必在本地填入真实密码，不要提交到仓库
    - 线上 Redis 建议使用更安全的账号体系

- **chrome-devtools**
  - **用途**：通过 Chrome DevTools MCP 控制/调试浏览器
  - **前提**：本机需要安装 Chrome 或兼容浏览器

---

## 3. 需要你本地手动填写 / 修改的字段汇总

在把项目跑起来前，建议你遍历以下几类字段并在本机做适配：

- **Token / API Key / 密码（不要提交到仓库）**
  - `github.env.GITHUB_PERSONAL_ACCESS_TOKEN`
  - `magic.env.API_KEY`
  - `mysql.env.MYSQL_PASS`（尤其是连接真实数据库时）
  - `redis-mcp` 的 `--password`（如你的 Redis 启用了密码）
  
- **本地路径 / 盘符相关（根据你的电脑修改）**
  - `filesystem` 暴露的目录列表（只保留你希望 Claude 访问的盘符/文件夹）
  - `everything-search.env.EVERYTHING_SDK_PATH`（指向你安装的 `Everything64.dll`）
  - `memory.env.MEMORY_FILE_PATH`（指向一个你本机存在且可写的路径）

---

## 4. 非 Windows 平台适配提示（简要）

如果你在 **macOS / Linux** 上使用本仓库，`.mcp.json` 需要做一些基本的替换：

- **命令前缀**
  - 将 `"command": "cmd", "args": ["/c", "npx", ...]` 换成：
    - `"command": "npx", "args": ["-y", "<server-name>", ...]`
  - 或者在 shell 中直接通过 `npx` 启动，无需 `cmd /c`

- **路径分隔符与盘符**
  - 把诸如 `D:\\`, `E:\\` 替换为对应系统的路径，例如：
    - `/Users/<you>/Projects`
    - `/home/<you>/data`

总体原则是：**MCP 只知道你在 `.mcp.json` 中显式暴露的路径和凭证**，你可以根据自己机器的情况做最小化授权，以满足开发需要同时保证安全可控。  


