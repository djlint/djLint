---
title: Go 模板检查与格式化
keywords: Go 模板, golang, djlint, Go 模板检查, Go 模板格式化, go template linter, golang template formatter, hugo, helm
description: djLint是一个 Go 模板的代码检查与格式化工具！使用与构建的配置文件，充分利用djLint来检查并格式化你的模板。
tool: golang
---

# {{ title }}

{{ description }}

**[Go 模板简介](https://pkg.go.dev/text/template)**

Hugo 主题和 Helm chart 使用的正是 Go 模板（`text/template`、`html/template`），请为它们使用同一个配置。

#### 使用命令行

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### 使用配置文件

在你项目中的 `pyproject.toml` 配置 djLint。

```toml
[tool.djlint]
profile="{{ tool }}"
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block">详情请参考 <a href="{{ "lang_code_url" | i18n }}/docs/configuration/">配置</a> 章节</div>
</div>
