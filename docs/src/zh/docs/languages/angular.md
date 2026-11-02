---
title: Angular 模板代码检查工具
keywords: angular, djlint, angular 模板代码检查工具, 检查 angular 模板
description: djLint 可以检查 Angular 模板。设置 angular 预设，让规则适合这类模板。
tool: angular
---

# {{ title }}

{{ description }}

**[什么是 Angular？](https://angular.io/guide/template-syntax)**

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
