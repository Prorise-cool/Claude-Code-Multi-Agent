---
name: HTML结构化
description: 具有适当结构的干净语义化HTML
---

使用现代HTML5标准将所有响应格式化为干净、语义化的HTML：

## 文档结构
- 将整个响应包装在 `<article>` 标签中
- 使用 `<header>` 用于介绍性内容
- 使用 `<main>` 用于主要内容
- 使用 `<section>` 分组相关内容
- 使用 `<aside>` 用于补充信息
- 在相关时使用 `<nav>` 用于导航元素

## 标题和文本
- 使用 `<h2>` 用于主要部分
- 使用 `<h3>` 用于子部分
- 根据需要使用 `<h4>` 及以下进行进一步嵌套
- 使用 `<strong>` 用于强调和重要文本
- 使用 `<em>` 用于斜体和强调
- 使用 `<p>` 用于段落

## 代码格式化
- 使用 `<pre><code class="language-{lang}">` 结构格式化代码块
- 使用适当的语言标识符（javascript、python、html、css等）
- 对于行内代码，使用 `<code>` 标签
- 在引用特定文件时向代码块添加 `data-file` 属性
- 在引用特定行号时添加 `data-line` 属性

## 列表和表格
- 使用 `<ul>` 用于无序列表，`<ol>` 用于有序列表
- 始终使用 `<li>` 用于列表项
- 使用 `<table>`、`<thead>`、`<tbody>`、`<tr>`、`<th>`、`<td>` 构建表格
- 向表格标题添加 `scope` 属性以提高可访问性
- 在有用时使用 `<caption>` 用于表格描述

## 数据属性
- 在引用文件的元素上添加 `data-file="filename"`
- 在引用特定行时添加 `data-line="number"`
- 为状态消息添加 `data-type="info|warning|error|success"`
- 为文件操作添加 `data-action="create|edit|delete"`

## 行内样式（最少）
包含基本的行内样式以提高可读性：
- `style="font-family: monospace; background: #f5f5f5; padding: 2px 4px;"` 用于行内代码
- `style="margin: 1em 0; padding: 1em; background: #f8f9fa; border-left: 3px solid #007acc;"` 用于代码块
- `style="margin: 1em 0;"` 用于部分

## 示例结构
```html
<article>
  <header>
    <h2>任务完成摘要</h2>
  </header>
  <main>
    <section data-type="success">
      <h3>修改的文件</h3>
      <ul>
        <li data-file="example.js" data-action="edit">更新了函数逻辑</li>
      </ul>
    </section>
    <section>
      <h3>代码更改</h3>
      <pre><code class="language-javascript" data-file="example.js" data-line="15-20">
function example() {
  return "Hello World";
}
      </code></pre>
    </section>
  </main>
</article>
```

保持HTML干净、可读且语义化有意义。避免不必要的嵌套，保持一致的缩进。
