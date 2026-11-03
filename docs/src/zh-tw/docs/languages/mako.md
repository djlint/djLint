---
title: Mako 範本 Linter 與格式化工具
keywords: mako, python, pyramid, open edx, djlint, mako 範本 linter, mako 範本格式化工具, 格式化 mako 範本
description: djLint 可以 lint 並格式化 Mako 範本。設定 mako profile，讓規則與格式化方式符合這類範本。
tool: mako
---

# {{ title }}

{{ description }}

**[什麼是 Mako？](https://www.makotemplates.org/)**

使用 mako profile 時，`% if x:` 這類控制行和 `##` 註解一定會單獨佔一行；屬性取決於控制行的標籤會保持原樣。Python 區塊以及 `<%doc>` 和 `<%text>` 的內容不會被更動；在 `--format-js` 或 `--format-css` 下，含有 Mako 語法的 script 或 style 也會保持原樣。控制行目前還不會縮排其中的內容。

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
