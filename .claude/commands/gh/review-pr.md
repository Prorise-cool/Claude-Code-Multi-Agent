---
description: 审查 GitHub pull request，提供详细的代码分析
argument-hint: [pr-number]
allowed-tools: Write, Read, LS, Glob, Grep, Bash(gh:*), Bash(git:*)
---



# Review PR (审查 PR)

你是一位专家级的代码审查员。请按照以下步骤审查 GitHub PR `$ARGUMENTS`：

1. 如果参数中未提供 PR 编号，请使用 Bash(`gh pr list`) 显示未关闭的 PR。
2. 如果提供了 PR 编号，请使用 Bash(`gh pr view $ARGUMENTS`) 获取 PR 详情。
3. 使用 Bash(`gh pr diff $ARGUMENTS`) 获取代码差异 (diff)。
4. 分析更改并提供详尽的代码审查，内容应包括：
* PR 功能概览
* 代码质量和风格分析
* 具体的改进建议
* 任何潜在的问题或风险


5. 仅提供包含建议和必要更改的代码审查评论：
* **不要** 评论 PR 的作用或总结 PR 内容
* **仅** 关注建议、代码更改以及潜在的问题和风险
* **使用** Bash(`gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments`) 发布你的审查评论



保持审查简洁但透彻。重点关注：

* 代码正确性
* 是否遵循项目规范
* 性能影响
* 测试覆盖率
* 安全考量

请使用清晰的章节和要点列表来格式化你的审查内容。

## gh 命令参考

```sh
# 列出 PR
gh pr list

# 查看 PR 描述
gh pr view 78

# 查看 PR 代码更改
gh pr diff 78

# 审查评论应发布到更改的文件中
gh api repos/OWNER/REPO/pulls/PR_NUMBER/comments \
    --method POST \
    --field body="[你的评论内容]" \
    --field commit_id="[commitID]" \
    --field path="path/to/file" \
    --field line=lineNumber \
    --field side="RIGHT"

# 获取 commitID 的示例命令
gh api repos/OWNER/REPO/pulls/PR_NUMBER --jq '.head.sha'

```