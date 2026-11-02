---
title: Mustache 模板代码检查与格式化工具
keywords: mustache, djlint, mustache 模板代码检查工具, mustache 模板格式化工具, 格式化 mustache 模板
description: djLint 是一款 Mustache 模板代码检查工具，也是一款 Mustache 模板格式化工具！使用 djLint 检查和格式化模板时，可以直接使用内置的预设。
tool: handlebars
---

# {{ title }}

{{ description }}

**[什么是 Mustache？](https://mustache.github.io/mustache.5.html)**

#### 使用命令行

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### 或者，使用配置文件

在项目的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">查看配置指南，了解所有选项！</a></div>
</div>
