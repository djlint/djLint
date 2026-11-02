---
title: Go 模板代码检查与格式化工具
keywords: go 模板, golang, djlint, go 模板代码检查工具, go 模板格式化工具, golang 模板代码检查工具, golang 模板格式化工具, 格式化 go 模板, hugo 模板代码检查工具, helm 模板代码检查工具
description: djLint 是一款 Go 模板代码检查工具，也是一款 Go 模板格式化工具！使用 djLint 检查和格式化模板时，可以直接使用内置的预设。
tool: golang
---

# {{ title }}

{{ description }}

**[什么是 Go 模板？](https://pkg.go.dev/text/template)**

Hugo 主题和 Helm chart 同样基于 Go 模板（`text/template`、`html/template`），因此也请为它们使用这个预设。

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
