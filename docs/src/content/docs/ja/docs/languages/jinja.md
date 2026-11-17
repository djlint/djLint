---
title: "Jinja テンプレートのリンターとフォーマッター"
description: "djLint で Jinja テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、jinja プロファイルを設定してください。"
sidebar:
  label: "Jinja"
---

djLint で Jinja テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、`jinja` プロファイルを設定してください。

**[Jinja とは？](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja は Jinja2 の構文に従い、HubSpot の Jinjava のテンプレートも Jinja 形式なので、どちらにも `jinja` プロファイルを使ってください。J004 と J018 は Flask の `url_for` を勧めるルールなので、Flask を使わないプロジェクトでは無視してください。

## コマンドラインを使う

```bash
djlint /path/to/templates --profile=jinja
```

## 設定ファイルで

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

```toml title="pyproject.toml"
[tool.djlint]
profile = "jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile = "jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```
