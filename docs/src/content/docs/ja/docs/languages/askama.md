---
title: "Askama テンプレートのリンターとフォーマッター"
description: "djLint で Askama テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、askama プロファイルを設定してください。"
sidebar:
  label: "Askama"
---

djLint で Askama テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、`askama` プロファイルを設定してください。

**[Askama とは？](https://askama.readthedocs.io/)**

## コマンドラインを使う

```bash
djlint /path/to/templates --profile=askama
```

## または、設定ファイルを使う

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

```toml title="pyproject.toml"
[tool.djlint]
profile = "askama"
```

```toml title="djlint.toml / .djlint.toml"
profile = "askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::
