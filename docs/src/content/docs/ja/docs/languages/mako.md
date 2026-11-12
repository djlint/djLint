---
title: "Mako テンプレートのリンターとフォーマッター"
description: "djLint で Mako テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、mako プロファイルを設定してください。"
sidebar:
  label: "Mako"
---

djLint で Mako テンプレートをリント・フォーマットできます。ルールとフォーマットがテンプレートに合うよう、`mako` プロファイルを設定してください。

**[Mako とは？](https://www.makotemplates.org/)**

mako プロファイルでは、`% if x:` のような制御行と `##` コメントは常にそれぞれ独立した行に置かれ、属性が制御行に左右されるタグは書かれたまま残ります。Python ブロックと `<%doc>`、`<%text>` の中身は変更されず、`--format-js` や `--format-css` を使っても Mako の構文を含む script や style はそのまま残ります。`% if` と `% endif` の間の行、およびそれぞれが独立した行にある `<%block>` や `<%def>` タグとその閉じタグの間の行は、ほかのブロックと同じようにインデントされます。`${}` 式のコードは書かれたまま残ります。

## コマンドラインを使う

```bash
djlint /path/to/templates --profile=mako
```

## または、設定ファイルを使う

プロジェクトの `pyproject.toml`、`djlint.toml` / `.djlint.toml`、または `.djlintrc` ファイルで djLint を設定します。

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::
