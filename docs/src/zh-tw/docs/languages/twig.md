---
title: Twig 範本 Linter 與格式化工具
keywords: twig, djlint, twig 範本 linter, twig 範本格式化工具, 格式化 twig 範本, pebble, pebble 範本 linter
description: djLint 是 twig 範本 linter，也是 twig 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。
tool: nunjucks
---

# {{ title }}

{{ description }}

**[什麼是 Twig？](https://twig.symfony.com/)**

Pebble（Java）範本與 Twig 相容，因此它們也請使用同一個 profile。

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
