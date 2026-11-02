---
title: Liquid テンプレートのリンターとフォーマッター
keywords: liquid, shopify, jekyll, eleventy, djlint, liquid テンプレート リンター, liquid テンプレート フォーマッター, liquid テンプレートのフォーマット, shopify, jekyll, eleventy, liquidjs, fluid, shopify テーマ リンター, jekyll リンター
description: djLint で Liquid テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、liquid プロファイルを設定してください。
tool: liquid
---

# {{ title }}

{{ description }}

**[Liquid とは？](https://shopify.github.io/liquid/)**

Shopify テーマ、Jekyll、LiquidJS（Eleventy）、Fluid（Orchard Core）と、すべての Liquid の方言に 1 つのプロファイルで対応します。

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
