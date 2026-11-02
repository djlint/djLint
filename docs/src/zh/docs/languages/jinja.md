---
title: Jinja 模板代码检查与格式化工具
keywords: jinja, djlint, jinja 模板代码检查工具, jinja 模板格式化工具, 格式化 jinja 模板, minijinja, jinjava, minijinja 模板代码检查工具, jinjava 模板代码检查工具
description: djLint 是一款 Jinja 模板代码检查工具，也是一款 Jinja 模板格式化工具！使用 djLint 检查和格式化模板时，可以直接使用内置的预设。
tool: jinja
---

# {{ title }}

{{ description }}

**[什么是 Jinja？](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja 模板与 Jinja2 完全兼容，因此同样使用这个 `jinja` 预设。

HubSpot 的 Jinjava 模板同样是 Jinja 风格，因此也请为它们使用这个预设。

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
