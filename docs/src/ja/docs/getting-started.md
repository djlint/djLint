---
description: HTML テンプレートのリントとフォーマットのための djLint 入門。使いやすい CLI と豊富なフォーマッターのオプションを活用しましょう。
title: はじめに
keywords: テンプレート リンター, テンプレート フォーマッター, djLint, HTML, テンプレート, フォーマッター, リンター, 使い方
---

# はじめに

## インストール

djLint は [Python](https://python.org) で作られており、[PyPI](https://pypi.org/project/djlint/) で公開されています。[uv](https://docs.astral.sh/uv/) を使う場合は、開発用の依存関係としてプロジェクトに追加します：

```bash
uv add --dev djlint
```

または、単独のツールとしてインストールします：

```bash
uv tool install djlint
```

または、pip でインストールします：

```bash
pip install djlint
```

または、[pipx](https://pipx.pypa.io/) でインストールします：

```bash
pipx install djlint
```

または、macOS や Linux では、コミュニティが管理している [Homebrew formula](https://formulae.brew.sh/formula/djlint) でインストールします：

```bash
brew install djlint
```

_または、npm でインストールします。**警告**：npm パッケージはラッパーにすぎず、そのインストールスクリプトはシステムのパス上にある `python3` で `pip install --upgrade djlint` を実行します。npm は実際のパッケージを管理もアンインストールもしないため、できるだけ pip を直接使ってください。_

```bash
npm i djlint
```

コミットのたびに djLint を実行するには、[pre-commit]({{ "lang_code_url" | i18n }}/docs/integrations/#pre-commit) を参照してください。

## CLI の使い方

djLint はコマンドラインアプリケーションです。高度な設定については[設定]({{ "lang_code_url" | i18n }}/docs/configuration/)のページを参照してください。

{% include 'src/_includes/cli.md' %}

{% admonition
   "note",
   "メモ",
   "`djlint` コマンドが見つからない場合は、Python が[パスに含まれている](https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/)ことを確認してください。"
%}

## パスと標準入力の使い分け

djLint はパスと標準入力のどちらでも動作します。

パスを指定して実行する場合：

```bash
djlint /path/to/templates --lint
```

特定のファイルを指定する場合：

```bash
djlint /path/to/this.mustache --lint
```

標準入力を使う場合：

```bash
echo "<div></div>" | djlint -
```

標準入力はコードの再フォーマットにも使えます。出力はフォーマット済みのコードだけで、メッセージは含まれません。

```bash
echo "<div></div>" | djlint - --reformat
```

出力：

```html
<div></div>
```

標準入力から読み込む場合、djLint には `per-file-ignores` との照合やメッセージの表示に使う実際のパスがないため、デフォルトで `-` を使います。エディターとの連携機能が保存時にファイルの内容をパイプで渡す場合などは、`--stdin-filename` を指定して、パイプで渡した内容の実際のパスを djLint に伝えてください。

```bash
echo "<div></div>" | djlint - --stdin-filename templates/index.html
```

## 終了コード

| コード | 意味                                                                                                                                                    |
| ------ | ------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0`    | djLint がチェックを求められたものすべてに問題がないか、見つかったファイルがすべて設定によってスキップされました。                                       |
| `1`    | djLint がリントエラー、または再フォーマットが必要なファイルを見つけました。`--warn` を指定すると、これらを警告として報告し、代わりに `0` で終了します。 |
| `2`    | djLint は求められたチェックを行いませんでした。パスに一致するファイルがなかったか、コマンドラインや設定が無効だったか、djLint が失敗しました。          |

djLint がテンプレートを調べて問題を見つけたことを意味するのは、コード `1` だけです。コード `2` は常に、実行そのものが役目を果たさなかったことを意味するため、パイプラインは推測に頼らずにこの 2 つを区別して扱えます。

まったく何もチェックしなかった実行を捕まえるのがコード `2` です。パスの誤り、もう一致しなくなった `--extension`、移動したテンプレートなどがこれにあたります。コード `2` がなければ、このような実行はテンプレートを 1 つも見ないまま黙って成功してしまいます。

djLint が _実際に_ 見つけたうえで、`exclude`、`extend_exclude`、`use_gitignore`、`require_pragma` によって意図的にスキップしたファイルはエラーではありません。この場合の実行は `0` で終了します。設定が指示どおりに動作したからです。これは、djLint に見てほしいかどうかに関係なくステージされたファイルの名前を渡す pre-commit で、`exclude` が機能する理由でもあります。

テンプレートがないパスがパイプラインにとって正常な場合は、`allow_empty_input` でコード `2` を無効にしてください：

```bash
djlint /path/to/templates --lint --allow-empty-input
```
