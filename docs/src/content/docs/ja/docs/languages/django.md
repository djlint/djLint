---
title: "Django テンプレートのリンターとフォーマッター"
description: "djLint で Django テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、django プロファイルを設定してください。"
sidebar:
  label: "Django"
---

djLint で Django テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、`django` プロファイルを設定してください。

**[Django とは？](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

## コマンドラインを使う

```bash
djlint /path/to/templates --profile=django
```

## または、設定ファイルを使う

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

```toml title="pyproject.toml"
[tool.djlint]
profile = "django"
```

```toml title="djlint.toml / .djlint.toml"
profile = "django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::
