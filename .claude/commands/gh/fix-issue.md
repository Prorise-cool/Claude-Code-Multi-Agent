---
description: 修复 GitHub issue
argument-hint: [issue-number]
allowed-tools: Write, Read, LS, Glob, Grep, Bash(gh:*), Bash(git:*)
---


请按照以下步骤分析并修复 GitHub issue `$ARGUMENTS`：

# PLAN (计划)

1. 使用 `gh issue view` 获取 issue 的详细信息。
2. 理解 issue 中描述的问题。
3. 如有必要，提出澄清性问题。
4. 理解该 issue 的相关背景 (Prior art)：
* 搜索便笺 (scratchpads) 以查找与该 issue 相关的过往思路。
* 搜索 PR (Pull Requests) 以查看是否能找到关于此 issue 的历史记录。
* 在代码库中搜索相关文件。


5. 深入思考如何将该 issue 分解为一系列小的、可管理的任务。
6. 在一个新的便笺 (scratchpad) 中记录你的计划：
* 文件名中需包含 issue 名称。
* 便笺中需包含指向该 issue 的链接。



# CREATE (开发)

* 为该 issue 创建一个新的分支。
* 根据你的计划，以小的、可管理的步骤解决该 issue。
* 每完成一个步骤后提交 (Commit) 你的更改。

# TEST (测试)

* 如果你更改了 UI 并且工具列表中包含 puppeteer，请通过 MCP 使用 puppeteer 来测试更改。
* 编写单元测试以描述代码的预期行为。
* 运行完整的测试套件，确保没有破坏任何现有功能。
* 如果测试失败，请修复它们。
* 在进入下一步之前，确保所有测试均通过。

# OPEN PULL REQUEST (提交 PR)

* 提交 PR (Pull Request) 并请求审查。

请记住，所有 GitHub 相关的任务都要使用 GitHub CLI (`gh`)。