---
title: "Angular テンプレートのリンター"
description: "djLint で Angular テンプレートをリントできます。ルールがテンプレートに合うよう、angular プロファイルを設定してください。"
sidebar:
  label: "Angular"
---

djLint で Angular テンプレートをリントできます。ルールがテンプレートに合うよう、`angular` プロファイルを設定してください。

**[Angular とは？](https://angular.io/guide/template-syntax)**

## コマンドラインを使う

```bash
djlint /path/to/templates --profile=angular
```

## または、設定ファイルを使う

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

```toml title="pyproject.toml"
[tool.djlint]
profile = "angular"
```

```toml title="djlint.toml / .djlint.toml"
profile = "angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::
