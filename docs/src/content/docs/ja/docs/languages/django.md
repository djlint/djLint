---
title: "Django テンプレートのリンターとフォーマッター"
description: "djLint は django テンプレートのリンターであり、django テンプレートのフォーマッターでもあります！djLint でテンプレートをリント・フォーマットするときは、用意済みのプロファイルを活用してください。"
sidebar:
  label: "Django"
---

djLint は django テンプレートのリンターであり、django テンプレートのフォーマッターでもあります！djLint でテンプレートをリント・フォーマットするときは、用意済みのプロファイルを活用してください。

**[Django とは？](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### コマンドラインを使う

```bash
djlint /path/to/templates --profile=django
```

#### または、設定ファイルを使う

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

```toml title="pyproject.toml"
[tool.djlint]
profile="django"
```

```toml title="djlint.toml / .djlint.toml"
profile="django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::
