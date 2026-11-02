---
title: Nunjucks 範本 Linter 與格式化工具
keywords: nunjucks, djlint, nunjucks 範本 linter, nunjucks 範本格式化工具, 格式化 nunjucks 範本, pebble, pebble 範本 linter
description: djLint 可以 lint 並格式化 Nunjucks 範本。設定 nunjucks profile，讓規則與格式化方式符合這類範本。
tool: nunjucks
---

# {{ title }}

{{ description }}

**[什麼是 Nunjucks？](https://mozilla.github.io/nunjucks/)**

Pebble（Java）範本與 Twig 相容，因此它們也請使用同一個 profile。

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
