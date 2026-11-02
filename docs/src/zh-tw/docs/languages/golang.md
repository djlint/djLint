---
title: Go 範本 Linter 與格式化工具
keywords: go 範本, golang, djlint, go 範本 linter, go 範本格式化工具, golang 範本 linter, golang 範本格式化工具, 格式化 go 範本, hugo 範本 linter, helm 範本 linter
description: djLint 是 Go 範本 linter，也是 Go 範本格式化工具！使用 djLint lint 與格式化範本時，善用預先建置好的 profile。
tool: golang
---

# {{ title }}

{{ description }}

**[什麼是 Go 範本？](https://pkg.go.dev/text/template)**

Hugo 佈景主題和 Helm chart 也是以 Go 範本（`text/template`、`html/template`）為基礎，因此它們也請使用同一個 profile。

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
