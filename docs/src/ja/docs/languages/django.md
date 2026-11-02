---
title: Django テンプレートのリンターとフォーマッター
keywords: django, djlint, django テンプレート リンター, django テンプレート フォーマッター, django テンプレートのフォーマット
description: djLint で Django テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、django プロファイルを設定してください。
tool: django
---

# {{ title }}

{{ description }}

**[Django とは？](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

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
