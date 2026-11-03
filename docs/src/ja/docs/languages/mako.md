---
title: Mako テンプレートのリンターとフォーマッター
keywords: mako, python, pyramid, open edx, djlint, mako テンプレート リンター, mako テンプレート フォーマッター, mako テンプレートのフォーマット
description: djLint で Mako テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、mako プロファイルを設定してください。
tool: mako
---

# {{ title }}

{{ description }}

**[Mako とは？](https://www.makotemplates.org/)**

mako プロファイルでは、`% if x:` のような制御行と `##` コメントは常にそれぞれ独立した行に置かれ、属性が制御行に左右されるタグは書かれたまま残ります。Python ブロックと `<%doc>`、`<%text>` の中身は変更されず、`--format-js` や `--format-css` を使っても Mako の構文を含む script や style はそのまま残ります。制御行の中身はまだインデントされません。

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
