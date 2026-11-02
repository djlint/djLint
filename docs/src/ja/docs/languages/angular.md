---
title: Angular テンプレートのリンター
keywords: angular, djlint, angular テンプレート リンター, angular テンプレートのリント
description: djLint で Angular テンプレートをリントできます。ルールがテンプレートに合うよう、angular プロファイルを設定してください。
tool: angular
---

# {{ title }}

{{ description }}

**[Angular とは？](https://angular.io/guide/template-syntax)**

## コマンドラインを使う

```bash
djlint /path/to/templates --profile={{ tool }}
```

## または、設定ファイルを使う

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">すべてのオプションは設定ガイドで確認してください！</a></div>
</div>
