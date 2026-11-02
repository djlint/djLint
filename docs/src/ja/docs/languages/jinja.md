---
title: Jinja テンプレートのリンターとフォーマッター
keywords: jinja, djlint, jinja テンプレート リンター, jinja テンプレート フォーマッター, jinja テンプレートのフォーマット, minijinja, jinjava, minijinja テンプレート リンター, jinjava テンプレート リンター
description: djLint で Jinja テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、jinja プロファイルを設定してください。
tool: jinja
---

# {{ title }}

{{ description }}

**[Jinja とは？](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja のテンプレートは Jinja2 と完全に互換性があるので、同じ `jinja` プロファイルを使ってください。

HubSpot の Jinjava のテンプレートも jinja 形式なので、これらにもこのプロファイルを使ってください。

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
