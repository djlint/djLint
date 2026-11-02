---
description: 开始使用 djLint 进行 HTML 模板代码检查与格式化。充分利用简单易用的命令行界面和丰富的格式化选项。
title: 快速入门
keywords: 模板代码检查工具, 模板格式化工具, djLint, HTML, 模板, 格式化工具, 代码检查工具, 用法
---

# 快速入门

## 安装

djLint 使用 [Python](https://python.org) 编写，发布在 [PyPI](https://pypi.org/project/djlint/) 上。使用 [uv](https://docs.astral.sh/uv/) 时，可以将其添加为项目的开发依赖：

```bash
uv add --dev djlint
```

或者将其安装为独立工具：

```bash
uv tool install djlint
```

或者使用 pip：

```bash
pip install djlint
```

或者使用 [pipx](https://pipx.pypa.io/)：

```bash
pipx install djlint
```

或者在 macOS 或 Linux 上使用社区维护的 [Homebrew formula](https://formulae.brew.sh/formula/djlint)：

```bash
brew install djlint
```

_或者使用 npm。**警告**：npm 包只是一个包装器，它的安装脚本会用系统路径中碰巧存在的那个 `python3` 运行 `pip install --upgrade djlint`。npm 不会管理或卸载实际安装的包，因此请尽量直接使用 pip。_

```bash
npm i djlint
```

要在每次提交时运行 djLint，请参阅 [pre-commit]({{ "lang_code_url" | i18n }}/docs/integrations/#pre-commit)。

## 命令行用法

djLint 是一个命令行应用程序。高级配置请参阅[配置]({{ "lang_code_url" | i18n }}/docs/configuration/)页面。

{% include 'src/_includes/cli.md' %}

{% admonition
   "note",
   "注意",
   "如果找不到 `djlint` 命令，请确认 Python 已[添加到 PATH 中](https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/)。"
%}

## 使用路径还是标准输入

djLint 既可以处理路径，也可以处理标准输入（stdin）。

指定路径运行：

```bash
djlint /path/to/templates --lint
```

或者指定某个文件：

```bash
djlint /path/to/this.mustache --lint
```

或者使用标准输入：

```bash
echo "<div></div>" | djlint -
```

标准输入也可以用来重新格式化代码。输出中只有格式化后的代码，不含任何消息。

```bash
echo "<div></div>" | djlint - --reformat
```

输出：

```html
<div></div>
```

从标准输入读取时，djLint 没有真实路径可用于匹配 `per-file-ignores` 或显示在消息中，因此默认使用 `-`。可以传入 `--stdin-filename` 告诉 djLint 管道内容的真实路径，例如编辑器集成在保存时把文件内容通过管道传入的情况。

```bash
echo "<div></div>" | djlint - --stdin-filename templates/index.html
```

## 退出码

| 代码 | 含义                                                                                                         |
| ---- | ------------------------------------------------------------------------------------------------------------ |
| `0`  | djLint 被要求检查的内容全部没有问题，或者找到的每个文件都被你的配置跳过了。                                  |
| `1`  | djLint 发现了代码检查错误，或者有需要重新格式化的文件。使用 `--warn` 时，这些会作为警告报告，并以 `0` 退出。 |
| `2`  | djLint 没有检查你要求它检查的内容：路径没有匹配到任何文件、命令行或配置无效，或者 djLint 运行失败。          |

只有代码 `1` 表示 djLint 检查了你的模板，并且对发现的内容不满意。代码 `2` 始终表示这次运行本身没有完成任务，因此流水线可以区别对待这两种情况，而不必去猜。

代码 `2` 能捕获根本什么都没检查的运行：路径写错了、`--extension` 不再匹配，或者模板已经移走了。没有它，这样的运行会悄无声息地通过，而实际上一个模板都没看过。

djLint *确实*找到、但随后因 `exclude`、`extend_exclude`、`use_gitignore` 或 `require_pragma` 而有意跳过的文件，不算错误。这样的运行以 `0` 退出，因为配置完全按照指示执行了。也正因如此，`exclude` 才能在 pre-commit 下正常工作：无论你是否希望 djLint 检查，pre-commit 都会传入所有已暂存文件的名称。

如果某个路径确实没有模板，而这在你的流水线中是正常情况，可以用 `allow_empty_input` 关闭代码 `2`：

```bash
djlint /path/to/templates --lint --allow-empty-input
```
