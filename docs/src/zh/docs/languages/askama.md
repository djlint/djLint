---
title: Askama 模板代码检查与格式化工具
keywords: askama, rust, djlint, askama 模板代码检查工具, askama 模板格式化工具, 格式化 askama 模板
description: djLint 可以检查和格式化 Askama 模板。设置 askama 预设，让规则和格式化方式适合这类模板。
tool: askama
---

# {{ title }}

{{ description }}

**[什么是 Askama？](https://askama.readthedocs.io/)**

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
