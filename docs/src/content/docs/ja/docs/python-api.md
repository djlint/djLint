---
title: "Python API"
description: "djLint の API を使って、自分の Python コードからテンプレートをフォーマット・リントします。"
---

`djlint.api` は、Python プログラムからテキストをフォーマット・リントし、コマンドラインと同じ結果を返します。エディターやビルドツールなど、テンプレートをメモリー上に保持するものに向けたモジュールです。パッケージ内のほかの部分はどのリリースでも変わる可能性があるため、`djlint.settings` や `djlint.lint` ではなく、このモジュールを使ってください。[カスタムルールの例](/ja/docs/linter/#python-モジュールルール)がインポートしているヘルパー、`djlint.lint.get_line`、`djlint.helpers.inside_ignored_rule`、`djlint.helpers.inside_ignored_linter_block` も引き続き使えます。

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, on_warning=None, **options)` は、フォルダー内のファイルに適用される設定を読み込みます。コマンドラインが最初に渡されたパスから[探す](/ja/docs/configuration/)のと同じように、そのフォルダーから上に向かって設定を探します。カレントディレクトリは変更しません。

オプションにはコマンドラインオプションの名前をアンダースコア区切りで指定し、コマンドラインと同じように動作します。指定した値は設定ファイルよりも優先され、`False`、空文字列、そしてほとんどのオプションでは `0` も、指定なしとして扱われます。パスは `pathlib.Path` で指定します。

設定の読み込みには時間がかかるため、読み込み元のファイルが変わらないあいだは結果を保持しておいてください。結果はいくつのテキストにも使えます。

`python_rules=False` を指定すると、`python_module` を持つカスタムルールは読み込まれないため、信頼できないプロジェクトのコードが実行されるのを防げます。読み込まれなかったルールの名前は `config.skipped_rules` に入ります。

`on_warning` にメッセージを受け取る関数を渡すと、名前のつづり間違いや、どのルールにもないルールコードなど、設定についての警告をすべて受け取れます。指定しない場合、各警告はプロセスごとに 1 回、標準エラー出力に書き出されます。読み込めない設定ファイルや無効な値は `click.UsageError` を発生させます。

## format_text

`format_text(config, text)` はフォーマット済みのテキストを返します。最初の行が CRLF で終わるテキストは CRLF で、それ以外は LF で返されます。`require_pragma` が有効な場合、プラグマのないテキストは変更されずに返されます。`load_config` のオプションでも設定ファイルでも `indent` や `max_line_length` が設定されていない場合は、`load_config` に渡したフォルダーにある、設定された拡張子のファイルに適用される `.editorconfig` のセクションから取ります。コマンドラインでは、ファイルごとにそのパスで決まります。

## lint_text

`lint_text(config, text, filename="-")` は、`Finding` のリストをドキュメント内の順序で返します。`filename` は `per-file-ignores` との照合に使われます。`require_pragma` が有効な場合、プラグマのないテキストには検出結果がありません。

`Finding` は次のフィールドを持つ名前付きタプルです：

- `code`：ルールのコード（`H013` など）。
- `message`：ルールのメッセージ。
- `match`：見つかったテキストの先頭部分（最大 20 文字）。
- `line`、`column`：検出結果の開始位置。行は 1 から、列は 0 から数えます。
- `end_line`、`end_column`：終了位置の直後。後続の行になることもあります。

列は、バイト単位や UTF-16 コードユニット単位ではなく、文字単位で数えます。

## is_excluded

`is_excluded(config, path)` は、コマンドラインと同じように、`exclude`、`extend_exclude`、または gitignore によってファイルが除外されるかどうかを返します。`format_text` と `lint_text` は、これを自分ではチェックしません。

## ルールモジュール

カスタムルールの `python_module` は、設定のプロジェクトルートから、プロセスごとに 1 回だけインポートされます。実行し続けるプログラムが別のプロジェクトのルールを読み込むには、最初のプロジェクトからインポートしたものをすべて `sys.modules` から削除し、そのプロジェクトのルートを `sys.path` の末尾から削除する必要があります。
