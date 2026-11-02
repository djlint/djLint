---
title: Jinja 範本 Linter 與格式化工具
keywords: jinja, djlint, jinja 範本 linter, jinja 範本格式化工具, 格式化 jinja 範本, minijinja, jinjava, minijinja 範本 linter, jinjava 範本 linter
description: djLint 可以 lint 並格式化 Jinja 範本。設定 jinja profile，讓規則與格式化方式符合這類範本。
tool: jinja
---

# {{ title }}

{{ description }}

**[什麼是 Jinja？](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja 範本與 Jinja2 完全相容，因此請使用同一個 `jinja` profile。

HubSpot 的 Jinjava 範本也是 jinja 風格，因此它們也請使用這個 profile。

## 使用命令列

```bash
djlint /path/to/templates --profile={{ tool }}
```

## 或者，使用設定檔

在專案的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 檔案中設定 djLint。

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">查看設定指南，了解所有選項！</a></div>
</div>
