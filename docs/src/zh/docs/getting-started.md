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

或者使用 [uv](https://docs.astral.sh/uv/) 将其作为独立工具安装：

```bash
uv tool install djlint
```

或者使用 [pipx](https://pipx.pypa.io/) 安装：

```bash
pipx install djlint
```

或者在 macOS 或 Linux 上使用社区维护的 [Homebrew formula](https://formulae.brew.sh/formula/djlint) 安装：

```bash
brew install djlint
```

_或者使用 npm 安装 - **注意**：npm 包只是一个包装器，其安装脚本会用系统路径中的 `python3` 执行 `pip install --upgrade djlint`。npm 无法管理或卸载实际安装的包 - 建议尽量直接使用 pip。_

```bash
npm i djlint
```

## 命令行使用方法

djLint 是一个命令行程序。详情请参考 `配置` 章节。

{% include 'src/_includes/cli.md' %}

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
