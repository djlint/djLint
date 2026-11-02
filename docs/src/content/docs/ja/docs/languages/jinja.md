---
title: "Jinja テンプレートのリンターとフォーマッター"
description: "djLint で Jinja テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、jinja プロファイルを設定してください。"
sidebar:
  label: "Jinja"
---

djLint で Jinja テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、`jinja` プロファイルを設定してください。

**[Jinja とは？](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja のテンプレートは Jinja2 と完全に互換性があるので、同じ `jinja` プロファイルを使ってください。

HubSpot の Jinjava のテンプレートも jinja 形式なので、これらにもこのプロファイルを使ってください。

## コマンドラインを使う

```bash
djlint /path/to/templates --profile=jinja
```

## または、設定ファイルを使う

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

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::
