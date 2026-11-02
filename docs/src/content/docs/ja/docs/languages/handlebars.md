---
title: "Handlebars テンプレートのリンターとフォーマッター"
description: "djLint は handlebars テンプレートのリンターであり、handlebars テンプレートのフォーマッターでもあります！djLint でテンプレートをリント・フォーマットするときは、用意済みのプロファイルを活用してください。"
sidebar:
  label: "Handlebars"
---

djLint は handlebars テンプレートのリンターであり、handlebars テンプレートのフォーマッターでもあります！djLint でテンプレートをリント・フォーマットするときは、用意済みのプロファイルを活用してください。

**[Handlebars とは？](https://handlebarsjs.com/)**

#### コマンドラインを使う

```bash
djlint /path/to/templates --profile=handlebars
```

#### または、設定ファイルを使う

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

```toml title="pyproject.toml"
[tool.djlint]
profile="handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile="handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::
