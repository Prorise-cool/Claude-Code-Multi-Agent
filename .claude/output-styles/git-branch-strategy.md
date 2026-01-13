---
name: Git分支策略
description: GitHub Flow 和 Git Flow 分支管理规范
---

# Git 分支策略指南

本文档定义了两种主流的 Git 协作工作流：**GitHub Flow** 和 **Git Flow**。根据项目需求选择合适的策略。

---

## 🌊 GitHub Flow（简单分支策略）

**适用场景**: 持续部署、快速迭代、小型团队、Web 应用

### 核心原则
- **主分支**: `main` 或 `master` 始终可部署
- **功能分支**: 从 `main` 创建，完成后合并回 `main`
- **无长期分支**: 所有分支都是临时性的

### 分支结构
```
main (生产环境)
  ├── feature/user-login (功能分支)
  ├── feature/payment-integration (功能分支)
  └── hotfix/critical-bug (热修复分支)
```

### 工作流程

#### 1. 创建功能分支
```bash
# 从 main 创建功能分支
git checkout main
git pull origin main
git checkout -b feature/功能名称

# 分支命名规范:
# - feature/功能名称 (新功能)
# - fix/问题描述 (Bug 修复)
# - hotfix/紧急修复 (生产环境紧急修复)
# - docs/文档更新 (文档相关)
# - refactor/重构内容 (代码重构)
```

#### 2. 开发与提交
```bash
# 开发过程中频繁提交
git add .
git commit -m "feat(scope): 简短描述"

# Commitlint 规范:
# type(scope): subject
# - type: feat/fix/docs/style/refactor/test/chore
# - scope: 模块或文件范围（可选）
# - subject: 简短描述（50字符内）
```

#### 3. 推送与合并
```bash
# 推送分支
git push origin feature/功能名称

# 创建 Pull Request (PR)
# - 标题: feat(scope): 功能描述
# - 描述: 详细说明变更内容
# - 审查后合并到 main
```

#### 4. 合并后删除分支
```bash
# 合并后自动删除功能分支
git checkout main
git pull origin main
git branch -d feature/功能名称
```

### 分支命名规范

| 前缀 | 用途 | 示例 |
|------|------|------|
| `feature/` | 新功能开发 | `feature/user-authentication` |
| `fix/` | Bug 修复 | `fix/login-error-handling` |
| `hotfix/` | 生产环境紧急修复 | `hotfix/security-patch` |
| `docs/` | 文档更新 | `docs/api-documentation` |
| `refactor/` | 代码重构 | `refactor/database-layer` |
| `test/` | 测试相关 | `test/unit-tests` |
| `chore/` | 构建/工具相关 | `chore/update-dependencies` |

### 提交信息规范（Commitlint）

```bash
# 格式: type(scope): subject
# 
# type 类型:
# - feat: 新功能
# - fix: Bug 修复
# - docs: 文档变更
# - style: 代码格式（不影响功能）
# - refactor: 重构
# - test: 测试相关
# - chore: 构建/工具变更

# 示例:
git commit -m "feat(auth): 添加用户登录功能"
git commit -m "fix(api): 修复数据验证错误"
git commit -m "docs(readme): 更新安装说明"
git commit -m "refactor(db): 重构数据库连接层"
```

---

## 🌳 Git Flow（复杂分支策略）

**适用场景**: 版本发布、大型团队、需要维护多个版本、企业级应用

### 核心原则
- **主分支**: `main` 或 `master` 始终是生产环境代码
- **开发分支**: `develop` 是集成分支，包含最新开发代码
- **功能分支**: 从 `develop` 创建，完成后合并回 `develop`
- **发布分支**: 从 `develop` 创建，用于准备新版本发布
- **热修复分支**: 从 `main` 创建，用于生产环境紧急修复

### 分支结构
```
main (生产环境)
  ├── develop (开发集成分支)
  │   ├── feature/user-login (功能分支)
  │   ├── feature/payment-integration (功能分支)
  │   └── release/v1.2.0 (发布分支)
  └── hotfix/critical-security (热修复分支)
```

### 分支说明

#### 1. 主分支 (main/master)
- **用途**: 生产环境代码
- **保护**: 只能通过 `release` 或 `hotfix` 分支合并
- **标签**: 每次发布都打标签（如 `v1.0.0`）

#### 2. 开发分支 (develop)
- **用途**: 开发集成分支
- **来源**: 从 `main` 创建
- **合并**: 所有 `feature` 分支合并到这里

#### 3. 功能分支 (feature/*)
- **用途**: 新功能开发
- **来源**: 从 `develop` 创建
- **合并**: 完成后合并回 `develop`
- **删除**: 合并后删除

#### 4. 发布分支 (release/*)
- **用途**: 准备新版本发布
- **来源**: 从 `develop` 创建（功能完成后）
- **操作**: 
  - 修复 Bug
  - 更新版本号
  - 更新文档
- **合并**: 
  - 合并到 `main`（打标签）
  - 合并回 `develop`

#### 5. 热修复分支 (hotfix/*)
- **用途**: 生产环境紧急修复
- **来源**: 从 `main` 创建
- **合并**: 
  - 合并到 `main`（打标签）
  - 合并回 `develop`

### 工作流程

#### 功能开发流程
```bash
# 1. 从 develop 创建功能分支
git checkout develop
git pull origin develop
git checkout -b feature/user-login

# 2. 开发与提交
git add .
git commit -m "feat(auth): 添加用户登录功能"

# 3. 推送分支
git push origin feature/user-login

# 4. 创建 Pull Request 合并到 develop
# 审查后合并

# 5. 删除功能分支
git checkout develop
git pull origin develop
git branch -d feature/user-login
```

#### 发布流程
```bash
# 1. 从 develop 创建发布分支
git checkout develop
git pull origin develop
git checkout -b release/v1.2.0

# 2. 准备发布
# - 修复 Bug
# - 更新版本号
# - 更新 CHANGELOG.md
git commit -m "chore(release): 准备 v1.2.0 发布"

# 3. 合并到 main 并打标签
git checkout main
git merge release/v1.2.0
git tag -a v1.2.0 -m "Release version 1.2.0"
git push origin main --tags

# 4. 合并回 develop
git checkout develop
git merge release/v1.2.0
git push origin develop

# 5. 删除发布分支
git branch -d release/v1.2.0
```

#### 热修复流程
```bash
# 1. 从 main 创建热修复分支
git checkout main
git pull origin main
git checkout -b hotfix/critical-security

# 2. 修复问题
git add .
git commit -m "fix(security): 修复安全漏洞"

# 3. 合并到 main 并打标签
git checkout main
git merge hotfix/critical-security
git tag -a v1.1.1 -m "Hotfix: 安全漏洞修复"
git push origin main --tags

# 4. 合并回 develop
git checkout develop
git merge hotfix/critical-security
git push origin develop

# 5. 删除热修复分支
git branch -d hotfix/critical-security
```

### 分支命名规范

| 前缀 | 用途 | 来源分支 | 合并到 | 示例 |
|------|------|----------|--------|------|
| `feature/` | 新功能 | `develop` | `develop` | `feature/user-authentication` |
| `release/` | 版本发布 | `develop` | `main` + `develop` | `release/v1.2.0` |
| `hotfix/` | 紧急修复 | `main` | `main` + `develop` | `hotfix/critical-bug` |
| `fix/` | Bug 修复 | `develop` | `develop` | `fix/login-error` |

---

## 📋 选择指南

### 选择 GitHub Flow 如果：
- ✅ 持续部署（CD）环境
- ✅ 快速迭代需求
- ✅ 小型团队（< 10 人）
- ✅ Web 应用或 SaaS 产品
- ✅ 不需要维护多个版本

### 选择 Git Flow 如果：
- ✅ 需要版本发布管理
- ✅ 需要维护多个版本（如 v1.x, v2.x）
- ✅ 大型团队（> 10 人）
- ✅ 企业级应用
- ✅ 需要严格的发布流程

---

## 🔧 Claude Code 集成

### 自动分支管理

当使用 Git 时，Claude Code 应该：

1. **根据工作流自动创建分支**
   - GitHub Flow: `feature/功能名称`
   - Git Flow: `feature/功能名称`（从 develop）

2. **遵循提交规范**
   - 使用 commitlint 格式: `type(scope): subject`
   - 每次写工具后立即提交
   - 大任务完成后提交

3. **自动合并策略**
   - GitHub Flow: 功能完成后合并到 main
   - Git Flow: 功能完成后合并到 develop

4. **分支清理**
   - 合并后自动删除功能分支

### 配置示例

```json
{
  "git_workflow": "github-flow",
  "branch_prefix": "feature/",
  "commit_format": "commitlint",
  "auto_merge": true,
  "auto_cleanup": true
}
```

---

## ⚠️ 注意事项

1. **分支保护**: 主分支（main/master）应该设置保护规则
2. **代码审查**: 所有合并都应该通过 Pull Request 审查
3. **提交频率**: 频繁提交，每次提交应该是原子性的
4. **提交信息**: 遵循 commitlint 规范，清晰描述变更
5. **分支命名**: 使用小写字母和连字符，避免特殊字符

---

## 📚 参考资源

- [GitHub Flow](https://guides.github.com/introduction/flow/)
- [Git Flow](https://nvie.com/posts/a-successful-git-branching-model/)
- [Conventional Commits](https://www.conventionalcommits.org/)
- [Commitlint](https://commitlint.js.org/)

