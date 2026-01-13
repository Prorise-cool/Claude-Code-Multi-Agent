"""
文档管理模块
负责维护 /project_document 目录下的文档
"""
import json
import subprocess
from pathlib import Path
from datetime import datetime
from typing import Dict, Optional, List
from .logger import logger


class DocumentManager:
    """文档管理器"""
    
    def __init__(self, project_root: Path):
        self.project_root = project_root
        self.doc_dir = project_root / "project_document"
        self.doc_dir.mkdir(exist_ok=True)
        
        # 文档路径
        self.development_doc = self.doc_dir / "DEVELOPMENT.md"
        self.knowledge_doc = self.doc_dir / "KNOWLEDGE.md"
        self.changelog_doc = self.doc_dir / "CHANGELOG.md"
        
        # 去重记录（使用操作哈希）
        self.operation_hashes = set()
        self._load_operation_hashes()
    
    def _load_operation_hashes(self):
        """加载已记录的操作哈希（用于去重）"""
        hash_file = self.doc_dir / ".operation_hashes.json"
        if hash_file.exists():
            try:
                self.operation_hashes = set(json.loads(hash_file.read_text(encoding='utf-8')))
            except Exception:
                self.operation_hashes = set()
    
    def _save_operation_hash(self, op_hash: str):
        """保存操作哈希"""
        self.operation_hashes.add(op_hash)
        hash_file = self.doc_dir / ".operation_hashes.json"
        hash_file.write_text(json.dumps(list(self.operation_hashes), ensure_ascii=False), encoding='utf-8')
    
    def _hash_operation(self, tool_name: str, tool_input: Dict) -> str:
        """生成操作哈希（用于去重）"""
        key = f"{tool_name}:{json.dumps(tool_input, sort_keys=True)}"
        return str(hash(key))
    
    def initialize_documents(self):
        """初始化文档（如果不存在）"""
        if not self.development_doc.exists():
            self._create_development_template()
        if not self.knowledge_doc.exists():
            self._create_knowledge_template()
        if not self.changelog_doc.exists():
            self._create_changelog_template()
    
    def _create_development_template(self):
        """创建 DEVELOPMENT.md 模板（bullet-points 格式）"""
        template = """# 开发工作文档

> **格式要求**: 严格遵循 `.claude/output-styles/bullet-points.md` 格式规范

## 当前任务
- [ ] 待完成任务列表

## 任务详情
- 任务1
  - 状态: 进行中
  - 文件: 待定
  - 描述: 待定

## 最近完成
- 暂无

## 遇到的问题
- 暂无

## 技术决策
- 暂无

---
*本文档由 Claude Code 自动维护，请勿手动编辑格式*
"""
        self.development_doc.write_text(template, encoding='utf-8')
        logger.info(f"已创建开发文档: {self.development_doc}")
    
    def _create_knowledge_template(self):
        """创建 KNOWLEDGE.md 模板（markdown-focused 格式）"""
        template = """# 项目知识库

> **格式要求**: 严格遵循 `.claude/output-styles/markdown-focused.md` 格式规范

## 代码模式

### 认证模式
- 待补充

## 常见问题

### Q: 待补充
A: 待补充

## 技术决策记录

### 决策1
- **背景**: 待补充
- **决策**: 待补充
- **原因**: 待补充

## 学习资源
- 待补充

---
*本文档由 Claude Code 自动维护，请勿手动编辑格式*
"""
        self.knowledge_doc.write_text(template, encoding='utf-8')
        logger.info(f"已创建知识库文档: {self.knowledge_doc}")
    
    def _create_changelog_template(self):
        """创建 CHANGELOG.md 模板（bullet-points 格式）"""
        today = datetime.now().strftime("%Y-%m-%d")
        template = f"""# 变更日志

> **格式要求**: 严格遵循 `.claude/output-styles/bullet-points.md` 格式规范  
> **提交规范**: 遵循 commitlint 规范（type(scope): subject）

## [{today}]
### 新增
- 暂无

### 修改
- 暂无

### 修复
- 暂无

### 重构
- 暂无

---
*本文档由 Claude Code 自动维护，请勿手动编辑格式*
"""
        self.changelog_doc.write_text(template, encoding='utf-8')
        logger.info(f"已创建变更日志: {self.changelog_doc}")
    
    def should_update_documents(self, tool_name: str, tool_input: Dict, tool_result: str) -> bool:
        """判断是否应该更新文档（重要操作才更新）"""
        # 只处理写操作
        write_tools = ['Write', 'Edit', 'MultiEdit']
        if tool_name not in write_tools:
            return False
        
        # 检查去重
        op_hash = self._hash_operation(tool_name, tool_input)
        if op_hash in self.operation_hashes:
            logger.debug(f"操作已记录，跳过: {tool_name}")
            return False
        
        # 检查文件路径（排除临时文件和文档本身）
        file_path = tool_input.get('file_path', '')
        if not file_path:
            return False
        
        # 排除文档目录和临时文件
        excluded_patterns = [
            'project_document',
            '.claude',
            'node_modules',
            '.git',
            '__pycache__',
            '.pyc',
            '.tmp',
        ]
        if any(pattern in file_path for pattern in excluded_patterns):
            return False
        
        return True
    
    def update_documents(self, tool_name: str, tool_input: Dict, tool_result: str) -> Dict[str, str]:
        """更新文档（返回更新内容用于提示词）"""
        if not self.should_update_documents(tool_name, tool_input, tool_result):
            return {}
        
        op_hash = self._hash_operation(tool_name, tool_input)
        file_path = tool_input.get('file_path', 'unknown')
        content_preview = str(tool_input.get('content', ''))[:100]
        
        # 生成更新提示词
        updates = {
            'development': self._generate_development_update(tool_name, file_path, content_preview),
            'knowledge': self._generate_knowledge_update(tool_name, file_path, content_preview),
            'changelog': self._generate_changelog_update(tool_name, file_path),
        }
        
        # 保存操作哈希
        self._save_operation_hash(op_hash)
        
        return updates
    
    def _generate_development_update(self, tool_name: str, file_path: str, content_preview: str) -> str:
        """生成 DEVELOPMENT.md 更新提示词（bullet-points 格式）"""
        return f"""请更新 `/project_document/DEVELOPMENT.md` 文件，在"最近完成"部分添加以下内容（严格遵循 bullet-points 格式）：

- {tool_name} 操作
  - 文件: `{file_path}`
  - 操作类型: {tool_name}
  - 内容预览: {content_preview}...
  - 时间: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}

**格式要求**:
- 必须遵循 `.claude/output-styles/bullet-points.md` 格式
- 使用短横线 (-) 表示无序列表
- 保持层次结构清晰（2 空格缩进）
- 每个项目符号简洁（最多 1-2 行）"""
    
    def _generate_knowledge_update(self, tool_name: str, file_path: str, content_preview: str) -> str:
        """生成 KNOWLEDGE.md 更新提示词（markdown-focused 格式）"""
        return f"""请更新 `/project_document/KNOWLEDGE.md` 文件，根据以下信息添加相关内容（严格遵循 markdown-focused 格式）：

**操作信息**:
- 工具: {tool_name}
- 文件: `{file_path}`
- 内容预览: {content_preview}...

**更新要求**:
1. 如果是新的代码模式，添加到"代码模式"部分
2. 如果是技术决策，添加到"技术决策记录"部分
3. 如果是常见问题，添加到"常见问题"部分

**格式要求**:
- 必须遵循 `.claude/output-styles/markdown-focused.md` 格式
- 使用 **粗体** 强调关键概念
- 使用 `行内代码` 表示文件名、函数名
- 使用标题 (##、###) 创建层次结构
- 使用表格、列表等结构化元素"""
    
    def _generate_changelog_update(self, tool_name: str, file_path: str) -> str:
        """生成 CHANGELOG.md 更新提示词（bullet-points 格式）"""
        today = datetime.now().strftime("%Y-%m-%d")
        return f"""请更新 `/project_document/CHANGELOG.md` 文件，在今天的日期部分添加以下内容（严格遵循 bullet-points 格式和 commitlint 规范）：

**操作信息**:
- 工具: {tool_name}
- 文件: `{file_path}`
- 日期: {today}

**更新要求**:
1. 如果是新文件，添加到"新增"部分
2. 如果是修改文件，添加到"修改"部分
3. 如果是修复问题，添加到"修复"部分
4. 如果是重构，添加到"重构"部分

**格式要求**:
- 必须遵循 `.claude/output-styles/bullet-points.md` 格式
- 提交信息遵循 commitlint 规范: `type(scope): subject`
  - type: feat/fix/docs/style/refactor/test/chore
  - scope: 文件或模块名
  - subject: 简短描述
- 使用短横线 (-) 表示无序列表
- 保持简洁（最多 1-2 行）"""
    
    def check_git_repo(self) -> bool:
        """检查是否存在 Git 仓库"""
        git_dir = self.project_root / ".git"
        return git_dir.exists()
    
    def get_git_workflow(self) -> Optional[str]:
        """获取 Git 工作流配置（github-flow 或 git-flow）"""
        config_file = self.doc_dir / ".git_workflow.json"
        if config_file.exists():
            try:
                config = json.loads(config_file.read_text(encoding='utf-8'))
                return config.get('workflow', 'github-flow')
            except Exception:
                pass
        return None
    
    def save_git_workflow(self, workflow: str):
        """保存 Git 工作流配置"""
        config_file = self.doc_dir / ".git_workflow.json"
        config = {'workflow': workflow}
        config_file.write_text(json.dumps(config, ensure_ascii=False), encoding='utf-8')
        logger.info(f"已保存 Git 工作流配置: {workflow}")
    
    def commit_changes(self, tool_name: str, file_path: str, workflow: str = 'github-flow') -> bool:
        """提交更改（遵循 commitlint 规范）"""
        if not self.check_git_repo():
            return False
        
        try:
            # 生成 commitlint 格式的提交信息
            commit_type = self._get_commit_type(tool_name, file_path)
            scope = self._get_scope(file_path)
            subject = self._get_subject(tool_name, file_path)
            
            commit_message = f"{commit_type}({scope}): {subject}"
            
            # 添加所有更改
            subprocess.run(
                ["git", "add", "-A"],
                cwd=self.project_root,
                capture_output=True,
                check=True
            )
            
            # 提交
            result = subprocess.run(
                ["git", "commit", "-m", commit_message],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                logger.info(f"Git 提交成功: {commit_message}")
                return True
            elif "nothing to commit" in result.stdout.lower():
                logger.debug("没有需要提交的更改")
                return True
            else:
                logger.warning(f"Git 提交失败: {result.stderr}")
                return False
        except Exception as e:
            logger.error(f"Git 提交异常: {e}")
            return False
    
    def _get_commit_type(self, tool_name: str, file_path: str) -> str:
        """根据操作类型获取 commitlint type"""
        if tool_name == 'Write':
            return 'feat'  # 新功能/文件
        elif tool_name == 'Edit':
            return 'fix'  # 修复
        elif tool_name == 'MultiEdit':
            return 'refactor'  # 重构
        else:
            return 'chore'  # 其他
    
    def _get_scope(self, file_path: str) -> str:
        """从文件路径提取 scope"""
        path = Path(file_path)
        # 返回文件名或目录名
        if path.suffix:
            return path.stem  # 文件名（不含扩展名）
        else:
            return path.name  # 目录名
    
    def _get_subject(self, tool_name: str, file_path: str) -> str:
        """生成简短的主题描述"""
        path = Path(file_path)
        action = "创建" if tool_name == 'Write' else "更新"
        return f"{action} {path.name}"

