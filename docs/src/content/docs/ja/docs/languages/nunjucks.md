---
title: "Nunjucks テンプレートのリンターとフォーマッター"
description: "djLint で Nunjucks テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、nunjucks プロファイルを設定してください。"
sidebar:
  label: "Nunjucks"
---

djLint で Nunjucks テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、`nunjucks` プロファイルを設定してください。

**[Nunjucks とは？](https://mozilla.github.io/nunjucks/)**

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
