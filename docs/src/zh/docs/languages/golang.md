---
title: GoLang 模板检查与格式化
keywords: GoLang, djlint, GoLang 模板检查, GoLang 模板格式化
description: djLint是一个 GoLang 模板的代码检查与格式化工具！使用与构建的配置文件，充分利用djLint来检查并格式化你的模板。
tool: golang
---

# {{ title }}

{{ description }}

**[GoLang简介](https://pkg.go.dev/text/template)**

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
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block">详情请参考 <a href="/zh/docs/configuration/">配置</a> 章节</div>
</div>
