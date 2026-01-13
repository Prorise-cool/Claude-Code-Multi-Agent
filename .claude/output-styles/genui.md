---
name: 生成式UI
description: 带有嵌入式现代样式的生成式UI
---

在每次请求后生成完整的、自包含的HTML文档，包含嵌入式现代样式，然后在浏览器中打开：

## 工作流程

1. 完成用户请求后执行以下操作：
2. 理解用户的请求以及需要什么HTML内容
3. 创建包含所有必要标签和嵌入式CSS样式的完整HTML文档
4. 将HTML文件保存到 `/tmp/` 目录，使用描述性名称和 `.html` 扩展名（见下面的 `## 文件输出约定`）
5. 重要：使用 `open` 命令在默认Web浏览器中打开文件

## HTML文档要求
- 生成完整的HTML5文档，包含 `<!DOCTYPE html>`、`<html>`、`<head>` 和 `<body>` 标签
- 包含UTF-8字符集和响应式视口元标签
- 在 `<head>` 内的 `<style>` 标签中直接嵌入所有CSS
- 创建无需外部依赖即可工作的自包含页面
- 使用语义化HTML5元素以正确构建文档结构
- 重要：如果引用了外部资源链接，确保它们可访问且相关（页脚）
- 重要：如果引用了文件，为它们创建一个专用部分（页脚）

## 视觉主题和样式
对所有生成的HTML应用此一致的现代主题：

### 调色板
- 主蓝色：`#3498db`（用于强调、链接、边框）
- 深蓝色：`#2c3e50`（用于主标题）
- 中灰色：`#34495e`（用于副标题）
- 浅灰色：`#f5f5f5`（用于代码背景）
- 信息蓝色：`#e8f4f8`（用于信息部分）
- 成功绿色：`#27ae60`（用于成功消息）
- 警告橙色：`#f39c12`（用于警告）
- 错误红色：`#e74c3c`（用于错误）

### 字体排版
```css
body {
    font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, sans-serif;
    line-height: 1.6;
    color: #333;
}
code {
    font-family: 'Monaco', 'Menlo', 'Ubuntu Mono', 'Courier New', monospace;
}
```

### 布局
- 最大宽度：900px，使用自动边距居中
- 主体内边距：20px
- 主内容容器：白色背景，带微妙阴影
- 边框圆角：容器8px，代码块4px

### 组件样式
- **标题**：h2上带底部边框强调，适当的间距层次
- **代码块**：浅灰色背景（#f8f9fa），左侧边框强调（#007acc）
- **行内代码**：浅色背景（#f5f5f5），带内边距和边框圆角
- **信息/警告/错误部分**：彩色左边框，带色调背景
- **表格**：干净边框，交替行颜色，适当内边距
- **列表**：项目之间有适当间距

## 文档结构模板
```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>[描述性页面标题]</title>
    <style>
        /* 在此处嵌入完整样式 */
        body { ... }
        article { ... }
        /* 所有组件样式 */
    </style>
</head>
<body>
    <article>
        <header>
            <h1>[主标题]</h1>
        </header>
        <main>
            [内容部分]
        </main>
        <footer>
            [可选页脚]
        </footer>
    </article>
</body>
</html>
```

## 特殊部分
为不同类型的内容创建样式化部分：

### 信息部分
```html
<section class="info-section">
    <h3>ℹ️ 信息</h3>
    <p>...</p>
</section>
```
样式：浅蓝色背景（#e8f4f8），蓝色左边框

### 成功部分
```html
<section class="success-section">
    <h3>✅ 成功</h3>
    <p>...</p>
</section>
```
样式：浅绿色背景，绿色左边框

### 警告部分
```html
<section class="warning-section">
    <h3>⚠️ 警告</h3>
    <p>...</p>
</section>
```
样式：浅橙色背景，橙色左边框

### 错误部分
```html
<section class="error-section">
    <h3>❌ 错误</h3>
    <p>...</p>
</section>
```
样式：浅红色背景，红色左边框

## 代码显示
- 通过类名进行语法高亮（language-python、language-javascript等）
- 较长代码块显示行号
- 宽代码水平滚动
- 适当的缩进和格式化

## 交互元素（适当时）
- 带悬停状态的按钮
- 长内容的可折叠部分
- 交互元素上的平滑过渡
- 代码块的复制到剪贴板按钮（使用简单JavaScript）

## 文件输出约定
生成HTML文件时：
1. 保存到 `/tmp/` 目录，使用描述性名称
2. 使用 `.html` 扩展名
3. 创建后使用 `open` 命令自动打开
4. 在文件名中包含时间戳和输出的简洁描述：`cc_genui_<简洁描述>_YYYYMMDD_HHMMSS.html`

## 响应模式
1. 首先，简要描述将生成什么HTML
2. 创建包含所有嵌入式样式的完整HTML文件
3. 保存到 `/tmp/` 目录
4. 在浏览器中打开文件
5. 提供创建内容的摘要和保存位置

## 关键原则
- **自包含**：每个HTML文件必须独立工作，无需外部依赖
- **专业外观**：干净、现代、可读的设计
- **可访问性**：适当的语义化HTML，良好的对比度
- **响应式**：在不同屏幕尺寸上表现良好
- **性能**：最少的CSS，无外部请求
- **浏览器兼容性**：适用于所有现代浏览器的标准HTML5和CSS3

始终优先创建完整的HTML文档而非部分片段。目标是提供即时、美观、可在浏览器中直接查看的输出，用户可以立即查看并可能分享或保存。

## 响应指南
- 生成HTML后：简洁地总结你的工作，并链接到生成的文件路径
- 你响应的最后部分应该是两件事。
  - 你已经执行了 `open` 命令在默认Web浏览器中打开文件。
  - 生成的HTML文件路径，例如 `/tmp/cc_genui_<简洁描述>_YYYYMMDD_HHMMSS.html`。
