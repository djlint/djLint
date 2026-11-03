---
title: "Python API"
description: "djLint の API を使って、自分の Python コードからテンプレートをフォーマット・リントします。"
---

`djlint.api` は、Python プログラムからテキストをフォーマット・リントし、コマンドラインと同じ結果を返します。エディターやビルドツールなど、テンプレートをメモリー上に保持するものに向けたモジュールです。パッケージ内のほかの部分はどのリリースでも変わる可能性があるため、`djlint.settings` や `djlint.lint` ではなく、このモジュールを使ってください。

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, **options)` は、フォルダー内のファイルに適用される設定を読み込みます。コマンドラインがカレントディレクトリから探すのと同じように、そのフォルダーから上に向かって設定を探します。カレントディレクトリは変更しません。

オプションにはコマンドラインオプションの名前をアンダースコア区切りで指定し、コマンドラインと同じように動作します。指定した値は設定ファイルよりも優先され、`False`、空文字列、そしてほとんどのオプションでは `0` も、指定なしとして扱われます。パスは `pathlib.Path` で指定します。

設定の読み込みには時間がかかるため、読み込み元のファイルが変わらないあいだは結果を保持しておいてください。結果はいくつのテキストにも使えます。

`python_rules=False` を指定すると、`python_module` を持つカスタムルールは読み込まれないため、信頼できないプロジェクトのコードが実行されるのを防げます。読み込まれなかったルールの名前は `config.skipped_rules` に入ります。

## format_text

`format_text(config, text)` はフォーマット済みのテキストを返します。最初の行が CRLF で終わるテキストは CRLF で、それ以外は LF で返されます。`require_pragma` が有効な場合、プラグマのないテキストは変更されずに返されます。

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

カスタムルールの `python_module` は、設定のプロジェクトルートから、プロセスごとに 1 回だけインポートされます。実行し続けて複数のプロジェクトを扱うプログラムが別のプロジェクトのモジュールを読み込むには、プロジェクトからインポートしたものをすべて `sys.modules` から削除し、`sys.path` の末尾に残っているプロジェクトルートも削除する必要があります。
