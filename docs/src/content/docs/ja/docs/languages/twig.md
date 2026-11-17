---
title: "Twig テンプレートのリンターとフォーマッター"
description: "djLint で Twig テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、nunjucks プロファイルを設定してください。"
sidebar:
  label: "Twig"
---

djLint で Twig テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、`nunjucks` プロファイルを設定してください。

**[Twig とは？](https://twig.symfony.com/)**

Pebble（Java）のテンプレートは Twig と互換性があるので、同じプロファイルを使ってください。

## コマンドラインを使う

```bash
djlint /path/to/templates --profile=nunjucks
```

## または、設定ファイルを使う

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

```toml title="pyproject.toml"
[tool.djlint]
profile = "nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile = "nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::
