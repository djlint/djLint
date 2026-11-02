---
title: Liquid 範本 Linter 與格式化工具
keywords: liquid, shopify, jekyll, eleventy, djlint, liquid 範本 linter, liquid 範本格式化工具, 格式化 liquid 範本, shopify, jekyll, eleventy, liquidjs, fluid, shopify 佈景主題 linter, jekyll linter
description: djLint 是 Liquid 範本 linter，也是 Liquid 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。
tool: liquid
---

# {{ title }}

{{ description }}

**[什麼是 Liquid？](https://shopify.github.io/liquid/)**

一個 profile 就涵蓋所有 Liquid 方言：Shopify 佈景主題、Jekyll、LiquidJS（Eleventy）和 Fluid（Orchard Core）。

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
