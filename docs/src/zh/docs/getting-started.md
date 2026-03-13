---
description: 开始使用 djLint 进行 HTML 模板代码检查与格式化。借助其简便的命令行界面（CLI）以及丰富的格式化选项，让你的工作更加高效。
title: 入门指南
keywords: 模板检查, 模板格式化, djLint, HTML, 模板语言, 格式化, 检查, 使用
---

# 入门指南

## 从 [Pypi](https://pypi.org/project/djlint/) 安装

djLint 是基于 [Python](https://python.org) 的, 因此它可以被简单的安装：

```bash
pip install djlint
```

_或者使用 npm 的实验性 install 命令（注意：这要求你的系统路径中已包含 Python 和 pip）。_

```bash
npm i djlint
```

## 命令行使用方法

djLint 是一个命令行程序。详情请参考 `配置` 章节。

{% include 'src/\_includes/cli.md' %}

{% admonition
   "note",
   "注意",
   "如果提示 `djlint` 不是内部或外部的命令，请确保 Python 在你的[环境变量](https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/)中。"
%}

## 使用路径或标准输入（stdin）

djLint 可以通过路径或标准输入（stdin）运行。

通过路径运行 -

```bash
djlint /path/to/templates --lint
```

或者针对指定文件 -

```bash
djlint /path/to/this.mustache --lint
```

或者使用标准输入（stdin） -

```bash
echo "<div></div>" | djlint -
```

标准输入（stdin）也可用于重新格式化代码。输出将仅包含格式化后的代码，而不包含任何消息。

```bash
echo "<div></div>" | djlint - --reformat
```

输出结果 -

```html
<div></div>
```
