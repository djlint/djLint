---
title: Mustache 範本 Linter 與格式化工具
keywords: mustache, djlint, mustache 範本 linter, mustache 範本格式化工具, 格式化 mustache 範本
description: djLint 是 mustache 範本 linter，也是 mustache 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。
tool: handlebars
---

# {{ title }}

{{ description }}

**[什麼是 Mustache？](https://mustache.github.io/mustache.5.html)**

#### 使用命令列

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### 或者，使用設定檔

在專案的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 檔案中設定 djLint。

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">查看設定指南，了解所有選項！</a></div>
</div>
