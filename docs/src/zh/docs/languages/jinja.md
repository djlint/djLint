---
title: Jinja 模板检查与格式化
keywords: jinja, djlint, jinja 模板检查, jinja 模板格式化, minijinja, jinjava, minijinja template linter, jinjava template linter
description: djLint是一个 jinja 模板的代码检查与格式化工具！使用与构建的配置文件，充分利用djLint来检查并格式化你的模板。
tool: jinja
---

# {{ title }}

{{ description }}

**[Jinja简介](https://jinja2docs.readthedocs.io/en/stable/)**

MiniJinja 模板与 Jinja2 完全兼容 — 请使用同一个 `jinja` 配置。

HubSpot 的 Jinjava 模板也是 jinja 风格 — 也请使用此配置。

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
