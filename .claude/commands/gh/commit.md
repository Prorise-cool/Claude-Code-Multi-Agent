---
allowed-tools: Bash, Read, Write, Edit, Grep, Glob
description: 使用模板、验证和最佳实践生成符合规范的 git 提交信息
---

# Git 提交助手

一份全面的指南，帮助您使用 Conventional Commits 格式编写有效的 git 提交，包含模板、自动化工具和最佳实践。

## 目录

- [简介](#简介)
- [Conventional Commits 格式](#conventional-commits-格式)
- [提交信息模板](#提交信息模板)
- [自动化提交生成](#自动化提交生成)
- [Git Hooks 集成](#git-hooks-集成)
- [提交信息校验](#提交信息校验)
- [交互式提交工具](#交互式提交工具)
- [最佳实践](#最佳实践)

## 简介

精心编写的提交信息对于维护干净、易懂的 git 历史至关重要。它们帮助团队有效协作，使代码审查更容易，并简化调试和项目维护。

### 为什么良好的提交很重要

```javascript
const commitBenefits = {
  collaboration: [
    '清晰的变更沟通',
    '更容易的代码审查',
    '更好地理解项目历史'
  ],
  maintenance: [
    '快速识别破坏性变更',
    '更容易找到引入错误的时间',
    '简化变更日志生成',
    '更好的 git bisect 结果'
  ],
  automation: [
    '自动语义版本控制',
    '自动生成变更日志',
    '自动生成发布说明',
    'CI/CD 触发规则'
  ]
};
```

## Conventional Commits 格式

Conventional Commits 规范提供了一种结构化的提交信息格式。

### 格式结构

```
<type>(<scope>): <subject>

<body>

<footer>
```

### 提交类型

```javascript
const commitTypes = {
  feat: {
    description: '新功能',
    example: 'feat(auth): 添加 OAuth2 登录支持',
    semver: 'MINOR',
    emoji: '✨'
  },
  fix: {
    description: '修复 bug',
    example: 'fix(api): 解决用户服务中的空指针异常',
    semver: 'PATCH',
    emoji: '🐛'
  },
  docs: {
    description: '文档变更',
    example: 'docs(readme): 更新安装说明',
    semver: 'PATCH',
    emoji: '📝'
  },
  style: {
    description: '代码样式变更（格式、缺少分号等）',
    example: 'style(components): 应用 prettier 格式化',
    semver: 'PATCH',
    emoji: '💄'
  },
  refactor: {
    description: '不改变功能的代码重构',
    example: 'refactor(auth): 简化令牌验证逻辑',
    semver: 'PATCH',
    emoji: '♻️'
  },
  perf: {
    description: '性能提升',
    example: 'perf(database): 在用户邮箱列上添加索引',
    semver: 'PATCH',
    emoji: '⚡'
  },
  test: {
    description: '添加或更新测试',
    example: 'test(auth): 为登录流程添加单元测试',
    semver: 'PATCH',
    emoji: '✅'
  },
  build: {
    description: '构建系统或依赖变更',
    example: 'build(deps): 升级 react 到版本 18',
    semver: 'PATCH',
    emoji: '📦'
  },
  ci: {
    description: 'CI/CD 配置变更',
    example: 'ci(github): 添加自动发布工作流',
    semver: 'PATCH',
    emoji: '👷'
  },
  chore: {
    description: '其他不修改 src 或测试文件的变更',
    example: 'chore(gitignore): 将 .env 添加到忽略文件',
    semver: 'PATCH',
    emoji: '🔧'
  },
  revert: {
    description: '回退之前的提交',
    example: 'revert: 回退 "feat(auth): 添加 OAuth2 登录"',
    semver: 'PATCH',
    emoji: '⏪'
  }
};
```

### 破坏性变更

```javascript
// 破坏性变更示例
const breakingChangeExamples = [
  {
    format: 'feat!: 移除过时的 API 端点',
    description: '感叹号表示破坏性变更',
    semver: 'MAJOR'
  },
  {
    format: `feat(api): 重新设计身份验证流程

BREAKING CHANGE: 身份验证端点已从 /auth 移动到 /v2/auth。
所有客户端必须更新其配置以使用新端点。`,
    description: 'BREAKING CHANGE 页脚提供详细信息',
    semver: 'MAJOR'
  },
  {
    format: `refactor(database)!: 将主键类型更改为 UUID

BREAKING CHANGE: 需要数据库迁移。所有整数 ID 转换为 UUID。
请参阅迁移指南 docs/migrations/uuid-migration.md`,
    description: '带有迁移说明的破坏性变更',
    semver: 'MAJOR'
  }
];
```

### 完整示例

```javascript
// 良好的提交示例
const goodCommits = [
  {
    message: `feat(auth): 添加双因素身份验证支持

实现基于 TOTP 的 2FA，使用 speakeasy 库。
用户可以在其个人资料设置中启用 2FA。

Closes #123`,
    explanation: '清晰的主题，详细的主体，引用了问题'
  },
  {
    message: `fix(api): 防止订单处理中的竞争条件

在订单状态更新周围添加互斥锁，以防止
并发修改导致的无效状态。

当多个工作线程同时处理同一订单时，会发生竞争条件，
导致重复收费。

Fixes #456`,
    explanation: '解释了问题和解决方案'
  },
  {
    message: `perf(queries): 使用数据库索引优化用户搜索

在 (email, created_at) 列上添加复合索引。
将平均查询时间从 1.2s 降低到 45ms。

基准测试：
- 之前：平均 1200ms，p95 2500ms
- 之后：平均 45ms，p95 120ms`,
    explanation: '包含性能指标'
  },
  {
    message: `docs(api): 添加 OpenAPI 规范

从路由定义生成 OpenAPI 3.0 规范。
文档现在可在 /api/docs 获取。

该规范包括：
- 所有端点及其请求/响应模式
- 身份验证要求
- 限速信息
- 示例请求和响应`,
    explanation: '列出了添加的内容'
  }
];

// 不良的提交示例（应避免）
const badCommits = [
  {
    message: '修复 bug',
    problem: '过于模糊 - 哪个 bug？修复了什么？'
  },
  {
    message: '更新内容',
    problem: '不具体 - 更新了什么，为什么？'
  },
  {
    message: 'WIP',
    problem: '进行中的工作 - 不应出现在主历史中'
  },
  {
    message: '修复登录问题，还更新了主页设计并重构了数据库查询',
    problem: '一次提交中包含太多不相关的变更'
  },
  {
    message: 'feat: 添加新功能',
    problem: '主题过于通用 - 什么功能？'
  }
];
```

## 提交信息模板

### 基本模板

```bash
# .gitmessage 模板
# 将其放在 ~/.gitmessage 并使用以下命令配置：
# git config --global commit.template ~/.gitmessage

# <type>(<scope>): <subject>
# |<---- 使用最多 50 个字符 ---->|

# 解释为什么要进行此更改
# |<---- 尝试将每行限制为最多 72 个字符 ---->|

# 提供任何相关票据、文章或其他资源的链接
# 示例：Fixes #23

# --- 提交结束 ---
# 类型可以是：
#   feat     (新功能)
#   fix      (修复 bug)
#   docs     (文档变更)
#   style    (格式、缺少分号等)
#   refactor (代码重构)
#   perf     (性能提升)
#   test     (添加测试)
#   build    (构建系统变更)
#   ci       (CI/CD 变更)
#   chore    (其他变更)
# --------------------
# 请记住：
#   - 在主题行中使用祈使语气
#   - 不要在主题行末尾加句号
#   - 用空行将主题与主体分开
#   - 使用主体解释什么和为什么，而不是如何
#   - 可以使用多行 "-" 或 "*" 在主体中列出要点
```

### 交互式模板生成器

```javascript
#!/usr/bin/env node
// commit-helper.js

const readline = require('readline');
const { execSync } = require('child_process');

const rl = readline.createInterface({
  input: process.stdin,
  output: process.stdout
});

const commitTypes = [
  { value: 'feat', name: 'feat:     新功能' },
  { value: 'fix', name: 'fix:      修复 bug' },
  { value: 'docs', name: 'docs:     文档变更' },
  { value: 'style', name: 'style:    代码样式变更' },
  { value: 'refactor', name: 'refactor: 代码重构' },
  { value: 'perf', name: 'perf:     性能提升' },
  { value: 'test', name: 'test:     添加或更新测试' },
  { value: 'build', name: 'build:    构建系统变更' },
  { value: 'ci', name: 'ci:       CI/CD 变更' },
  { value: 'chore', name: 'chore:    其他变更' }
];

function question(prompt) {
  return new Promise((resolve) => {
    rl.question(prompt, resolve);
  });
}

function showTypes() {
  console.log('\n可用的提交类型：\n');
  commitTypes.forEach((type, index) => {
    console.log(`${index + 1}. ${type.name}`);
  });
  console.log();
}

async function getGitDiff() {
  try {
    const diff = execSync('git diff --cached --stat', { encoding: 'utf8' });
    return diff;
  } catch (error) {
    return null;
  }
}

async function generateCommit() {
  console.log('=== Git 提交助手 ===\n');

  // 显示已暂存的更改
  const diff = await getGitDiff();
  if (diff) {
    console.log('已暂存的更改：');
    console.log(diff);
  }

  // 选择类型
  showTypes();
  const typeIndex = await question('选择提交类型 (1-10): ');
  const type = commitTypes[parseInt(typeIndex) - 1]?.value;

  if (!type) {
    console.log('无效的类型选择');
    rl.close();
    return;
  }

  // 获取范围
  const scope = await question('输入范围（可选，按回车跳过）：');

  // 获取主题
  const subject = await question('输入提交主题（必填）：');

  if (!subject) {
    console.log('主题是必填项');
    rl.close();
    return;
  }

  // 获取主体
  console.log('\n输入提交主体（可选，按回车两次结束）：');
  let body = '';
  let line = '';
  let emptyLineCount = 0;

  while (emptyLineCount < 2) {
    line = await question('');
    if (line === '') {
      emptyLineCount++;
    } else {
      emptyLineCount = 0;
      body += line + '\n';
    }
  }

  // 检查是否为破坏性变更
  const isBreaking = await question('这是一个破坏性变更吗？ (y/N): ');
  const breaking = isBreaking.toLowerCase() === 'y';

  // 如果适用，获取破坏性变更描述
  let breakingDesc = '';
  if (breaking) {
    breakingDesc = await question('描述破坏性变更：');
  }

  // 获取问题引用
  const issueRef = await question('输入问题引用（例如，#123）或按回车跳过：');

  // 构建提交信息
  let commitMessage = '';

  // 主题行
  const scopeStr = scope ? `(${scope})` : '';
  const breakingIndicator = breaking ? '!' : '';
  commitMessage += `${type}${scopeStr}${breakingIndicator}: ${subject}\n`;

  // 主体
  if (body.trim()) {
    commitMessage += `\n${body.trim()}\n`;
  }

  // 页脚
  let footer = '';
  if (breaking && breakingDesc) {
    footer += `BREAKING CHANGE: ${breakingDesc}\n`;
  }
  if (issueRef) {
    footer += `Closes ${issueRef}\n`;
  }

  if (footer) {
    commitMessage += `\n${footer}`;
  }

  // 预览
  console.log('\n=== 提交信息预览 ===\n');
  console.log(commitMessage);
  console.log('==============================\n');

  const confirm = await question('创建此提交吗？ (Y/n): ');

  if (confirm.toLowerCase() !== 'n') {
    try {
      // 将信息写入临时文件
      const fs = require('fs');
      const tempFile = '/tmp/commit-msg.txt';
      fs.writeFileSync(tempFile, commitMessage);

      // 执行 git 提交
      execSync(`git commit -F ${tempFile}`, { stdio: 'inherit' });

      console.log('\n✅ 提交成功创建！');
    } catch (error) {
      console.error('\n❌ 创建提交时出错：', error.message);
    }
  } else {
    console.log('\n提交已取消。');
  }

  rl.close();
}

generateCommit();
```

## 自动化提交生成

### 从 Git Diff 生成提交信息

```javascript
// generate-commit.js
const { execSync } = require('child_process');
const fs = require('fs');

class CommitGenerator {
  constructor() {
    this.changes = {
      added: [],
      modified: [],
      deleted: []
    };
  }

  analyzeChanges() {
    try {
      // 获取已暂存的文件
      const status = execSync('git diff --cached --name-status', {
        encoding: 'utf8'
      });

      const lines = status.trim().split('\n');

      lines.forEach(line => {
        const [status, file] = line.split('\t');

        switch (status) {
          case 'A':
            this.changes.added.push(file);
            break;
          case 'M':
            this.changes.modified.push(file);
            break;
          case 'D':
            this.changes.deleted.push(file);
            break;
        }
      });

      return this.changes;
    } catch (error) {
      console.error('分析更改时出错：', error.message);
      return null;
    }
  }

  inferCommitType() {
    const { added, modified, deleted } = this.changes;

    // 检查新功能
    if (added.some(f => f.includes('feature') || f.includes('component'))) {
      return 'feat';
    }

    // 检查测试
    if (added.some(f => f.includes('test')) || modified.some(f => f.includes('test'))) {
      if (this.changes.added.length + this.changes.modified.length === 1) {
        return 'test';
      }
    }

    // 检查文档
    if (added.concat(modified).every(f =>
      f.includes('.md') || f.includes('docs/') || f.includes('README')
    )) {
      return 'docs';
    }

    // 检查配置变更
    if (added.concat(modified).every(f =>
      f.includes('config') || f.includes('.json') || f.includes('.yml') ||
      f.includes('.yaml') || f.includes('package.json')
    )) {
      return 'chore';
    }

    // 检查 CI 变更
    if (added.concat(modified).some(f =>
      f.includes('.github') || f.includes('.gitlab') || f.includes('ci/')
    )) {
      return 'ci';
    }

    // 默认对于修改使用 fix
    if (modified.length > 0 && added.length === 0) {
      return 'fix';
    }

    // 默认对于添加使用 feat
    if (added.length > 0) {
      return 'feat';
    }

    return 'chore';
  }

  inferScope() {
    const allFiles = [
      ...this.changes.added,
      ...this.changes.modified,
      ...this.changes.deleted
    ];

    // 提取公共目录
    if (allFiles.length === 0) return '';

    const paths = allFiles.map(f => f.split('/'));

    // 查找公共前缀
    let commonPath = paths[0];

    for (let i = 1; i < paths.length; i++) {
      const path = paths[i];
      const newCommon = [];

      for (let j = 0; j < Math.min(commonPath.length, path.length); j++) {
        if (commonPath[j] === path[j]) {
          newCommon.push(commonPath[j]);
        } else {
          break;
        }
      }

      commonPath = newCommon;
    }

    // 使用公共路径中的最后一个目录作为范围
    if (commonPath.length > 0) {
      return commonPath[commonPath.length - 1];
    }

    return '';
  }

  generateSubject() {
    const { added, modified, deleted } = this.changes;

    if (added.length === 1 && modified.length === 0 && deleted.length === 0) {
      const file = added[0].split('/').pop();
      return `添加 ${file}`;
    }

    if (modified.length === 1 && added.length === 0 && deleted.length === 0) {
      const file = modified[0].split('/').pop();
      return `更新 ${file}`;
    }

    if (deleted.length === 1 && added.length === 0 && modified.length === 0) {
      const file = deleted[0].split('/').pop();
      return `移除 ${file}`;
    }

    // 多个文件
    const total = added.length + modified.length + deleted.length;

    if (added.length > 0) {
      return `添加 ${added.length} 个新文件${added.length > 1 ? 's' : ''}`;
    }

    if (modified.length > 0) {
      return `更新 ${modified.length} 个文件${modified.length > 1 ? 's' : ''}`;
    }

    return `修改 ${total} 个文件${total > 1 ? 's' : ''}`;
  }

  generateCommitMessage() {
    this.analyzeChanges();

    const type = this.inferCommitType();
    const scope = this.inferScope();
    const subject = this.generateSubject();

    const scopeStr = scope ? `(${scope})` : '';
    const message = `${type}${scopeStr}: ${subject}`;

    return message;
  }

  generateDetailedBody() {
    const { added, modified, deleted } = this.changes;
    const lines = [];

    if (added.length > 0) {
      lines.push('添加：');
      added.forEach(file => lines.push(`- ${file}`));
      lines.push('');
    }

    if (modified.length > 0) {
      lines.push('修改：');
      modified.forEach(file => lines.push(`- ${file}`));
      lines.push('');
    }

    if (deleted.length > 0) {
      lines.push('删除：');
      deleted.forEach(file => lines.push(`- ${file}`));
    }

    return lines.join('\n');
  }
}

// 使用示例
const generator = new CommitGenerator();
const message = generator.generateCommitMessage();
console.log('建议的提交信息：');
console.log(message);
console.log('\n详细更改：');
console.log(generator.generateDetailedBody());
```

## Git Hooks 集成

### 提交信息钩子 (commit-msg)

```bash
#!/bin/sh
# .git/hooks/commit-msg

# Conventional Commits 验证钩子

commit_msg_file=$1
commit_msg=$(cat "$commit_msg_file")

# Conventional Commits 的正则表达式
conventional_commit_regex='^(feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert)(\([a-z0-9\-]+\))?!?: .{1,50}'

# 检查提交信息是否符合 Conventional Commits 格式
if ! echo "$commit_msg" | grep -iqE "$conventional_commit_regex"; then
    echo "❌ 提交信息格式无效"
    echo ""
    echo "提交信息必须遵循 Conventional Commits 格式："
    echo "  <type>(<scope>): <subject>"
    echo ""
    echo "示例：feat(auth): 添加登录功能"
    echo ""
    echo "有效类型：feat, fix, docs, style, refactor, perf, test, build, ci, chore, revert"
    echo ""
    exit 1
fi

# 检查主题长度（应 <= 50 个字符）
subject_line=$(echo "$commit_msg" | head -n1)
subject_length=${#subject_line}

if [ $subject_length -gt 72 ]; then
    echo "⚠️  警告：提交主题行过长 ($subject_length 字符，应 <= 72)"
    echo ""
    echo "当前主题：$subject_line"
    echo ""
fi

# 检查是否使用祈使语气
if echo "$subject_line" | grep -qE "(ed|ing)$"; then
    echo "⚠️  警告：在主题行中使用祈使语气"
    echo "   不好：'Added feature' 或 'Adding feature'"
    echo "   好：'Add feature'"
    echo ""
fi

echo "✅ 提交信息格式有效"
exit 0
```

### 准备提交信息钩子

```bash
#!/bin/sh
# .git/hooks/prepare-commit-msg

commit_msg_file=$1
commit_source=$2

# 仅对常规提交运行（不对合并、压缩等）
if [ -z "$commit_source" ]; then
    # 获取当前分支名称
    branch=$(git symbolic-ref --short HEAD 2>/dev/null)

    # 从分支名称中提取问题编号（例如，feature/ABC-123-description）
    issue=$(echo "$branch" | grep -oE '[A-Z]+-[0-9]+' | head -n1)

    if [ -n "$issue" ]; then
        # 检查提交信息中是否已包含问题编号
        if ! grep -q "$issue" "$commit_msg_file"; then
            # 将问题引用添加到提交信息中
            echo "" >> "$commit_msg_file"
            echo "Refs: $issue" >> "$commit_msg_file"
        fi
    fi
fi
```

## 提交信息校验

### Commitlint 配置

```javascript
// commitlint.config.js
module.exports = {
  extends: ['@commitlint/config-conventional'],

  rules: {
    // 类型枚举
    'type-enum': [
      2,
      'always',
      [
        'feat',
        'fix',
        'docs',
        'style',
        'refactor',
        'perf',
        'test',
        'build',
        'ci',
        'chore',
        'revert'
      ]
    ],

    // 类型大小写
    'type-case': [2, 'always', 'lower-case'],

    // 类型不能为空
    'type-empty': [2, 'never'],

    // 范围大小写
    'scope-case': [2, 'always', 'lower-case'],

    // 主题大小写
    'subject-case': [2, 'always', 'lower-case'],

    // 主题不能为空
    'subject-empty': [2, 'never'],

    // 主题末尾不加句号
    'subject-full-stop': [2, 'never', '.'],

    // 主题最大长度
    'subject-max-length': [2, 'always', 50],

    // 主体前必须空行
    'body-leading-blank': [2, 'always'],

    // 主体最大行长度
    'body-max-line-length': [2, 'always', 72],

    // 页脚前必须空行
    'footer-leading-blank': [2, 'always'],

    // 自定义规则
    'header-max-length': [2, 'always', 72]
  },

  // 自定义插件
  plugins: [
    {
      rules: {
        'ticket-reference': (parsed) => {
          const { body, footer } = parsed;
          const text = (body || '') + (footer || '');

          // 检查是否有票据引用（例如，#123, JIRA-123）
          const hasTicket = /(?:#\d+|[A-Z]+-\d+)/.test(text);

          return [
            hasTicket,
            '提交必须引用一个票据（例如，#123 或 JIRA-123）'
          ];
        }
      }
    }
  ]
};
```

### Husky 集成

```json
{
  "name": "my-project",
  "version": "1.0.0",
  "scripts": {
    "prepare": "husky install"
  },
  "devDependencies": {
    "@commitlint/cli": "^17.0.0",
    "@commitlint/config-conventional": "^17.0.0",
    "husky": "^8.0.0"
  },
  "commitlint": {
    "extends": [
      "@commitlint/config-conventional"
    ]
  }
}
```

```bash
# 安装 husky 和 commitlint
npm install --save-dev @commitlint/cli @commitlint/config-conventional husky

# 初始化 husky
npx husky install

# 添加 commit-msg 钩子
npx husky add .husky/commit-msg 'npx --no -- commitlint --edit $1'
```

## 交互式提交工具

### Commitizen 设置

```bash
# 安装 commitizen
npm install --save-dev commitizen cz-conventional-changelog

# 初始化
npx commitizen init cz-conventional-changelog --save-dev --save-exact
```

```json
{
  "scripts": {
    "commit": "cz"
  },
  "config": {
    "commitizen": {
      "path": "./node_modules/cz-conventional-changelog"
    }
  }
}
```

### 自定义 Commitizen 适配器

```javascript
// .cz-config.js
module.exports = {
  types: [
    { value: 'feat', name: 'feat:     新功能' },
    { value: 'fix', name: 'fix:      修复 bug' },
    { value: 'docs', name: 'docs:     仅文档变更' },
    { value: 'style', name: 'style:    代码样式变更' },
    { value: 'refactor', name: 'refactor: 不修复 bug 也不添加功能的代码变更' },
    { value: 'perf', name: 'perf:     性能提升' },
    { value: 'test', name: 'test:     添加或更新测试' },
    { value: 'build', name: 'build:    构建系统或外部依赖' },
    { value: 'ci', name: 'ci:       CI 配置文件和脚本' },
    { value: 'chore', name: 'chore:    其他不修改 src 或测试文件的变更' },
    { value: 'revert', name: 'revert:   回退到某个提交' }
  ],

  scopes: [
    { name: 'api' },
    { name: 'auth' },
    { name: 'database' },
    { name: 'ui' },
    { name: 'components' },
    { name: 'services' },
    { name: 'utils' },
    { name: 'config' },
    { name: 'deps' }
  ],

  allowCustomScopes: true,
  allowBreakingChanges: ['feat', 'fix'],
  skipQuestions: [],

  subjectLimit: 50,
  breaklineChar: '|',

  footerPrefix: 'ISSUES CLOSED:',

  messages: {
    type: '选择您正在提交的更改类型：',
    scope: '此更改的范围是什么（例如组件或文件名）：',
    customScope: '指定此更改的范围：',
    subject: '写下此更改的简短描述：\n',
    body: '提供此更改的更长描述（可选）。使用 "|" 换行：\n',
    breaking: '列出任何破坏性变更（可选）：\n',
    footer: '列出此更改关闭的任何问题（可选）。例如：#31, #34:\n',
    confirmCommit: '您确定要继续提交上述内容吗？'
  }
};
```

## 最佳实践

```javascript
const commitBestPractices = {
  content: [
    '编写清晰、简洁的提交信息',
    '使用祈使语气（"Add feature" 而不是 "Added feature"）',
    '主题行以小写字母开头',
    '主题行末尾不要加句号',
    '将主题行限制在 50 个字符内',
    '用空行将主题与主体分开',
    '主体行限制在 72 个字符内',
    '解释什么和为什么，而不是如何',
    '引用问题和拉取请求'
  ],

  structure: [
    '进行原子提交（每次提交一个逻辑变更）',
    '提交完整、可工作的代码',
    '不要提交注释掉的代码',
    '不要提交调试语句',
    '在提交前审查更改（git diff --staged）',
    '在需要时使用交互式暂存（git add -p）'
  ],

  workflow: [
    '经常提交，使用有意义的消息',
    '不要将进行中的工作提交到主分支',
    '使用功能分支进行新开发',
    '在合并到主分支之前压缩提交',
    '在提交时编写提交信息，而不是稍后',
    '使用 git 提交钩子来强制执行标准'
  ],

  team: [
    '始终遵循团队约定',
    '就提交信息格式达成一致',
    '使用提交模板',
    '配置校验工具',
    '在代码审查期间审查提交历史',
    '在 CONTRIBUTING.md 中记录提交约定'
  ]
};

// 示例工作流程
const exampleWorkflow = `
# 1. 暂存特定更改
git add src/auth/login.js

# 2. 审查已暂存的更改
git diff --staged

# 3. 使用规范消息提交
git commit -m "feat(auth): 实现 OAuth2 登录流程

使用 passport.js 库添加 OAuth2 身份验证。
支持 Google 和 GitHub 提供者。

Closes #42"

# 4. 或使用交互式工具
npm run commit

# 5. 验证提交信息
git log -1 --pretty=format:"%s%n%n%b"
`;
```

本指南提供了实现有效 git 提交实践的所有必要信息，采用 Conventional Commits 格式、自动化工具和团队工作流程。