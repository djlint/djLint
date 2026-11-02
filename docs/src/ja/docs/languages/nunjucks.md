---
title: Nunjucks テンプレートのリンターとフォーマッター
keywords: nunjucks, djlint, nunjucks テンプレート リンター, nunjucks テンプレート フォーマッター, nunjucks テンプレートのフォーマット, pebble, pebble テンプレート リンター
description: djLint で Nunjucks テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、nunjucks プロファイルを設定してください。
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Nunjucks とは？](https://mozilla.github.io/nunjucks/)**

Pebble（Java）のテンプレートは Twig と互換性があるので、同じプロファイルを使ってください。

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
