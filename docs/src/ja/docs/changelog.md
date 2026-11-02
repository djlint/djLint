---
description: djLint の変更履歴。最近のリリースでの更新内容と、次のアップグレードで期待できる機能を確認できます。
title: 変更履歴
keywords: テンプレート リンター, テンプレート フォーマッター, djLint, HTML, テンプレート, フォーマッター, リンター, 変更履歴
---

{% raw %}

# 変更履歴

変更履歴は現在、[リリース](https://github.com/djlint/djLint/releases)に含まれています。

## 1.0.2

::: content

- バグ修正 [#240](https://github.com/djlint/djLint/issues/240)
  :::

## 1.0.1

::: content

- バグ修正 [#236](https://github.com/djlint/djLint/issues/236)
  :::

## 1.0.0

::: content

- バグ修正 [#224](https://github.com/djlint/djLint/issues/224)
  :::

## 0.7.6

::: content

- バグ修正 [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/189)
- エラーを警告として返す `--warn` フラグを追加
  :::

## 0.7.5

::: content

- バグ修正 [#187](https://github.com/djlint/djLint/issues/187)
- テンプレートファイル内の `yaml` フロントマターのサポートを改善
- [#123](https://github.com/djlint/djLint/issues/123) に対応してルール T032 を追加
- [#124](https://github.com/djlint/djLint/issues/124) に対応してルール H033 を追加
- [#178](https://github.com/djlint/djLint/issues/178) に対応して、リンターのプロファイルを除外方式から包含方式に変更
- [#188](https://github.com/djlint/djLint/issues/188) に対応して、代替の設定ファイル `.djlintrc` を追加
  :::

## 0.7.4

::: content

- バグ修正 [#177](https://github.com/djlint/djLint/issues/177)
  :::

## 0.7.3

::: content

- バグ修正 [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- `pyproject.toml` から Py3.6 を削除
  :::

## 0.7.2

::: content

- バグ修正 [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
  :::

## 0.7.1

::: content

- バグ修正 [#166](https://github.com/djlint/djLint/issues/166)
  :::

## 0.7.0

::: content

- カスタム HTML タグの設定を追加
- バグ修正
  :::

## 0.6.9

::: content

- HTML と Angular のプロファイルを追加
- ルール #H023 で一部の実体参照を許可
- バグ修正
  :::

## 0.6.8

::: content

- バグ修正
- ドキュメントを更新
  :::

## 0.6.7

::: content

- 属性内のテンプレートタグをフォーマットするための、オプトインの設定オプション `format_attribute_template_tags` を追加
- リンターのメッセージの変数の順序をカスタマイズする設定オプション `linter_output_format` を追加
- meta タグをチェックするルール H030 と H031 を追加
  :::

## 0.6.6

::: content

- バグ修正
  :::

## 0.6.5

::: content

- 出力パスをプロジェクトルートからの相対パスに変更
- バグ修正
  :::

## 0.6.4

::: content

- バグ修正
  :::

## 0.6.3

::: content

- django の `blocktrans` タグをサポート
- バグ修正
  :::

## 0.6.2

::: content

- バグ修正
  :::

## 0.6.1

::: content

- バグ修正
- ルール T028 をより厳格にし、メッセージをわかりやすく変更
  :::

## 0.6.0

::: content

- テンプレート構文内の閉じられていないものをチェックするルール T027 を追加
- 属性内で空白制御タグが欠けていないかをチェックするルール T028 を追加
- form の method が小文字かどうかをチェックするルール H029 を追加
- "trimmed" を持たない django の blocktranslate タグをフォーマッターの対象外に変更
- バグ修正
  :::

## 0.5.9a

::: content

- python 3.10 でのテストをサポート
- pre-commit フックを追加
  :::

## 0.5.9

::: content

- 除外対象を拡張するオプション `--use-gitignore` を追加
- デフォルトの除外の照合方法を変更
- windows での除外パスを修正
- 属性内の `{%...%}` タグのフォーマットを修正
- 属性内の for ループと入れ子の条件のフォーマットを修正
  :::

## 0.5.8

::: content

- require_pragma オプションを追加
- input の `data-src` と `action` を検出するように DJ018 を更新
- インラインで無視する構文を修正
- デフォルトの使い方のプレースホルダーとして `--lint` オプションを追加
- バグ修正
  :::

## 0.5.7

::: content

- バグ修正
  :::

## 0.5.6

::: content

- 空の id と class を見つけるルール H026 を追加
- バグ修正
  :::

## 0.5.5

::: content

- 設定を統合し、コードを軽量化
- バグ修正
  :::

## 0.5.4

::: content

- 空のタグのペアを見つけるルール H020 を追加
- インラインスタイルを見つけるルール H021 を追加
- http のリンクを見つけるルール H022 を追加
- 実体参照を見つけるルール H023 を追加
- script と style の type を見つけるルール H024 を追加
- 孤立したタグをチェックするルール H025 を追加。https://stackoverflow.com/a/1736801/10265880 に感謝します
- 属性のフォーマットを改善
- 位置にかかわらず改行を追加するように `blank_line_after_tag` オプションを更新
- django の `trans` タグのフォーマットを修正
- インラインスタイルのフォーマットを追加
- 属性内のテンプレートの条件のフォーマットを追加
- リンターのルールで、URL が書かれうる場所として srcset を追加
- フォーマットを高速化
- [jayvdb](https://github.com/jayvdb) に特別な感謝を
  :::

## 0.5.3

::: content

- 入力に標準入力を使う場合、`--reformat/check` オプションの標準出力に新しい html だけを出力するように変更
  :::

## 0.5.2

::: content

- `alt` の要件を H006 から H013 に分離
- 省略可能なカスタムルールファイルを追加
- プロファイルの選択肢に `golang` を追加
- インラインコメントを含む無視ブロックのフォーマットを修正
- `--indent` と `-e` オプションにデフォルトのテキストを追加
- # を受け付けるように URL のルールを更新
- Windows OS でのファイルのエンコーディングを修正
- 1 行のテンプレートタグの正規表現を修正
- 先頭にスペースがあるタグでの `blank_line_after_tag` を修正
  :::

## 0.5.1

::: content

- ルール H019 を追加
- DJ018 と H012 のバグを修正
  :::

## 0.5.0

::: content

- リンターのルールにおける正規表現の照合のバグをいくつか修正
- 無視ブロック内でリンターがエラーを返さないように変更
- `{% djlint:off %}...{% djlint:on %}` タグでコードブロックをリンター/フォーマッターの対象外にするオプションを追加
  :::

## 0.4.9

::: content

- バグ [#35](https://github.com/djlint/djLint/issues/35) を修正
  :::

## 0.4.8

::: content

- バグ [#34](https://github.com/djlint/djLint/issues/34) を修正
  :::

## 0.4.7

::: content

- `source` タグを 1 行のタグに移動
  :::

## 0.4.6

::: content

- バグ [#31](https://github.com/djlint/djLint/issues/31) を修正
  :::

## 0.4.5

::: content

- ドキュメントにベストプラクティスを追加
- リンター/フォーマッターのデフォルトのルールを設定する `--profile` オプションを追加
- jinja の URL パターン用のリンタールールを追加
  :::

## 0.4.4

::: content

- インデントの設定を文字列から整数に変更。`--indent 3`
  :::

## 0.4.3

::: content

- インデントの幅を指定する CLI オプションを追加。`--indent=" "`
  :::

## 0.4.2

::: content

- `blank_line_after_tag` オプションによる、タグの後の追加の空白をサポート
  :::

## 0.4.1

::: content

- 複数のファイルやフォルダーの一括処理をサポート
  :::

## 0.4.0

::: content

- django の `{# ... #}` タグのフォーマットを修正
- figcaption、details、summary タグのインデントをサポート
- `pyproject.toml` での除外パスのリストの上書きと拡張をサポート
  :::

## 0.3.9

::: content

- 属性の処理を更新
  :::

## 0.3.8

::: content

- 標準入力をサポート
  :::

## 0.3.7

::: content

- `small`、`dt`、`dd` タグのフォーマットを修正
  :::

## 0.3.6

::: content

- Nunjucks の `{%-` で始まるブロックのフォーマットをサポート
  :::

## 0.3.5

::: content

- より多くの Django ブロックをサポート
- カスタムブロックをサポート
- `pyproject.toml` での設定をサポート
  :::

## 0.3.4

::: content

- Nunjucks の空白制御タグ `-%}` のフォーマットを修正
  :::

## 0.3.3

::: content

- 短い `div` タグを 1 行にできるように変更
  :::

## 0.3.2

::: content

- Django のコメントのフォーマットを修正
- textarea をフォーマットの対象外に変更
  :::

## 0.3.1

::: content

- 属性のフォーマットの正規表現を更新
- リントのルール W010 を更新
  :::

## 0.3.0

::: content

- フォーマットによる変更があった場合に終了コードを 1 にするように変更
- Jinja の `asset` タグをサポート
  :::

## 0.2.9

::: content

- W018 の正規表現を更新
- 重複したリントのメッセージを削除
- Handlebars 向けに E001 を更新
  :::

## 0.2.8

::: content

- 古いバージョンの Click でのプログレスバーのエラーを修正
  :::

{% endraw %}
