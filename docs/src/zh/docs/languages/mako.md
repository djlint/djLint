---
title: Mako 模板代码检查与格式化工具
keywords: mako, python, pyramid, open edx, djlint, mako 模板代码检查工具, mako 模板格式化工具, 格式化 mako 模板
description: djLint 可以检查和格式化 Mako 模板。设置 mako 预设，让规则和格式化方式适合这类模板。
tool: mako
---

# {{ title }}

{{ description }}

**[什么是 Mako？](https://www.makotemplates.org/)**

使用 mako 预设时，`% if x:` 这样的控制行和 `##` 注释始终独占一行；属性由控制行决定的标签会保持原样。Python 块以及 `<%doc>` 和 `<%text>` 的内容不会被改动；在 `--format-js` 或 `--format-css` 下，含有 Mako 语法的 script 或 style 也保持原样。控制行目前还不会缩进其中的内容。

## 使用命令行

```bash
djlint /path/to/templates --profile={{ tool }}
```

## 或者，使用配置文件

在项目的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">查看配置指南，了解所有选项！</a></div>
</div>
