---
title: Go テンプレートのリンターとフォーマッター
keywords: go テンプレート, golang, djlint, go テンプレート リンター, go テンプレート フォーマッター, golang テンプレート リンター, golang テンプレート フォーマッター, go テンプレートのフォーマット, hugo テンプレート リンター, helm テンプレート リンター
description: djLint で Go テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、golang プロファイルを設定してください。
tool: golang
---

# {{ title }}

{{ description }}

**[Go テンプレートとは？](https://pkg.go.dev/text/template)**

Go テンプレート（`text/template`、`html/template`）は Hugo のテーマや Helm チャートでも使われているので、それらにも同じプロファイルを使ってください。

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
