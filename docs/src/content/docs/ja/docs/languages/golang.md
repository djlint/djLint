---
title: "Go テンプレートのリンターとフォーマッター"
description: "djLint で Go テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、golang プロファイルを設定してください。"
sidebar:
  label: "Go テンプレート"
---

djLint で Go テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、`golang` プロファイルを設定してください。

**[Go テンプレートとは？](https://pkg.go.dev/text/template)**

Go テンプレート（`text/template`、`html/template`）は Hugo のテーマや Helm チャートでも使われているので、それらにも同じプロファイルを使ってください。

## コマンドラインを使う

```bash
djlint /path/to/templates --profile=golang
```

## または、設定ファイルを使う

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

```toml title="pyproject.toml"
[tool.djlint]
profile = "golang"
```

```toml title="djlint.toml / .djlint.toml"
profile = "golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::
