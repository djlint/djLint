---
title: "Tera テンプレートのリンターとフォーマッター"
description: "djLint で Tera テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、tera プロファイルを設定してください。"
sidebar:
  label: "Tera"
---

djLint で Tera テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、`tera` プロファイルを設定してください。

**[Tera とは？](https://keats.github.io/tera/)**

## コマンドラインを使う

```bash
djlint /path/to/templates --profile=tera
```

## または、設定ファイルを使う

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

```toml title="pyproject.toml"
[tool.djlint]
profile = "tera"
```

```toml title="djlint.toml / .djlint.toml"
profile = "tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::
