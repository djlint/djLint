---
title: "Liquid テンプレートのリンターとフォーマッター"
description: "djLint で Liquid テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、liquid プロファイルを設定してください。"
sidebar:
  label: "Liquid"
---

djLint で Liquid テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、`liquid` プロファイルを設定してください。

**[Liquid とは？](https://shopify.github.io/liquid/)**

Shopify テーマ、Jekyll、LiquidJS（Eleventy）、Fluid（Orchard Core）と、すべての Liquid の方言に 1 つのプロファイルで対応します。

## コマンドラインを使う

```bash
djlint /path/to/templates --profile=liquid
```

## または、設定ファイルを使う

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

```toml title="pyproject.toml"
[tool.djlint]
profile = "liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile = "liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::
