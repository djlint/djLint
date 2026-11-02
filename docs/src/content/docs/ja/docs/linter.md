---
title: "リンターのルール"
description: "djLint の HTML テンプレートリンターのルールと、独自のルールを追加する方法。"
sidebar:
  label: "リンター"
---

djLint には、テンプレートのスタイルと妥当性をチェックするルールが多数含まれています。使用するテンプレート言語に合わせたプリセットのプロファイルを設定して、リンターを最大限に活用しましょう。

```bash
djlint /path/to/templates --lint

# カスタム拡張子を指定する場合
djlint /path/to/templates -e html.dj --profile=django

# ファイルを指定する場合
djlint /path/to/this.html.j2  --profile=jinja
```

:::tip
[すべてのオプションは設定ガイドで確認してください！](/ja/docs/configuration/)
:::

## ルールの有効化と無効化

ほとんどのルールはデフォルトで有効です。コマンドラインでは、`--ignore` フラグでルールを無効にできます。ルールを有効にするには `--include` フラグを使います。

例：

```bash
djlint . --lint --include=H006,H017 --ignore=H013,H015
```

これは[設定](/ja/docs/configuration)ファイルでも行えます。

## ルール

| コード | 意味                                                                                                  | デフォルト |
| ------ | ----------------------------------------------------------------------------------------------------- | ---------- |
| T001   | 変数は空白で囲む必要があります。例：`{{ this }}`                                                      | ✔️         |
| T002   | タグ内ではダブルクォートを使う必要があります。例：`{% extends "this.html" %}`                         | ✔️         |
| T003   | endblock には名前が必要です。例：`{% endblock body %}`。                                              | -          |
| D004   | （Django）静的ファイルの URL は `{% static path/to/file %}` のパターンに従う必要があります。          | ✔️         |
| J004   | （Jinja）静的ファイルの URL は `{{ url_for('static'..) }}` のパターンに従う必要があります。           | ✔️         |
| H005   | html タグには空でない `lang` 属性が必要です。                                                         | ✔️         |
| H006   | `img` タグには `height` 属性と `width` 属性が必要です。                                               | -          |
| H007   | html タグの前に `<!DOCTYPE ... >` が必要です。                                                        | ✔️         |
| H008   | 属性はダブルクォートで囲む必要があります。                                                            | ✔️         |
| H009   | タグ名は小文字にする必要があります。                                                                  | ✔️         |
| H010   | 属性名は小文字にする必要があります。                                                                  | ✔️         |
| H011   | 属性値は引用符で囲む必要があります。                                                                  | ✔️         |
| H012   | 属性の `=` の前後にスペースを入れてはいけません。                                                     | ✔️         |
| H013   | `img` タグには alt 属性が必要です。                                                                   | ✔️         |
| H014   | 設定で残す数よりも多くの空行があります。                                                              | ✔️         |
| H015   | `h` タグの後には改行を入れてください。                                                                | ✔️         |
| H016   | html に `title` タグがありません。                                                                    | ✔️         |
| H017   | 空要素のタグは自己終了にする必要があります（H018 と競合）。                                           | -          |
| D018   | （Django）内部リンクには `{% url ... %}` のパターンを使う必要があります。                             | ✔️         |
| H018   | 空要素のタグは本来自己終了なので、"/>" ではなく ">" で終わる必要があります（H017 と競合）。           | -          |
| J018   | （Jinja）内部リンクには `{{ url_for() ... }}` のパターンを使う必要があります。                        | ✔️         |
| H019   | `javascript:abc()` は `on_` イベントと実際の URL に置き換えてください。                               | ✔️         |
| H020   | 空のタグのペアが見つかりました。削除を検討してください。                                              | ✔️         |
| H021   | インラインスタイルは避けてください。                                                                  | ✔️         |
| H022   | 外部リンクには HTTPS を使ってください。                                                               | ✔️         |
| H023   | 実体参照を使わないでください。                                                                        | ✔️         |
| H024   | script と style では type を省略してください。                                                        | ✔️         |
| H025   | タグが孤立しているようです。                                                                          | ✔️         |
| H026   | 空の id と class は削除できます。                                                                     | ✔️         |
| T027   | テンプレート構文内に閉じられていない文字列が見つかりました。                                          | ✔️         |
| T028   | 属性値の中では空白制御タグの使用を検討してください。`{%- if/for -%}`                                  | -          |
| H029   | form の method の値には小文字の使用を検討してください。                                               | ✔️         |
| H030   | meta description の追加を検討してください。                                                           | ✔️         |
| T032   | テンプレートタグ内に余分な空白が見つかりました。                                                      | ✔️         |
| H033   | form の action に余分な空白が見つかりました。                                                         | ✔️         |
| T034   | {% ... }% ではなく {% ... %} を使うつもりでしたか？                                                   | ✔️         |
| H036   | 間隔を空けるために `br` タグを使わないでください。                                                    | ✔️         |
| H037   | 重複した属性が見つかりました。                                                                        | ✔️         |
| T038   | ブロックタグに対応する終了タグがありません。                                                          | ✔️         |
| T039   | 閉じられていないテンプレートタグが見つかりました。                                                    | ✔️         |
| T040   | extends タグまたは include タグのテンプレート名がないか、空です。                                     | ✔️         |
| H041   | タグが、開かれたテンプレートブロックとは別のブロックで閉じられています。                              | ✔️         |
| T041   | extends タグはテンプレートの最初のタグにする必要があります。                                          | ✔️         |
| H042   | label の for 属性に一致する id を持つ要素がこのファイルにありません。                                 | ✔️         |
| T042   | 別のテンプレートを継承するテンプレートでは、ブロック外のコンテンツはレンダリングされません。          | ✔️         |
| H043   | button タグには `type` 属性が必要です。                                                               | ✔️         |
| T043   | テンプレート内で同じブロック名が複数回使われています。                                                | ✔️         |
| H044   | thead で `th` セルと `td` セルを混在させてはいけません。                                              | ✔️         |
| T044   | 出力タグに文のキーワードが含まれています。ブロックタグを使ってください。                              | ✔️         |
| H045   | iframe タグには `title` 属性が必要です。                                                              | ✔️         |
| T045   | html コメント内のテンプレートタグも実行されます。無効にするにはテンプレートコメントを使ってください。 | ✔️         |
| H046   | tabindex を正の値にしてはいけません。                                                                 | ✔️         |
| H047   | フォーカス可能な要素に aria-hidden を設定してはいけません。                                           | ✔️         |
| H048   | 仕様で定義されていない aria 属性です。                                                                | ✔️         |
| H049   | viewport でページのズームを妨げてはいけません。                                                       | ✔️         |
| H050   | 廃止された要素なので、置き換える必要があります。                                                      | ✔️         |
| H051   | ARIA がマークアップ用に定義していないロールです。                                                     | ✔️         |
| H052   | meta refresh でタイマーによるページの再読み込みやリダイレクトを行ってはいけません。                   | ✔️         |
| H053   | ファイル内で同じ id が複数回使われています。                                                          | ✔️         |
| H054   | インタラクティブ要素を別のインタラクティブ要素の中に入れ子にしてはいけません。                        | ✔️         |
| H055   | lang 属性は en や pt-BR のような言語タグにする必要があります。                                        | ✔️         |
| H056   | src を空にしてはいけません。                                                                          | ✔️         |
| H057   | video にはキャプションのトラックが必要です。                                                          | ✔️         |

### コードのパターン

コードの最初の文字は次のパターンに従います：

- D：Django 専用
- H：html に適用
- J：Jinja 専用
- M：Handlebars 専用
- N：Nunjucks 専用
- T：テンプレート全般に適用

### ルールの詳細

<!-- oxfmt-ignore-start -->

#### T001

`Variables should be wrapped in a whitespace.`

`{{user.name}}` のように内側に余白がないテンプレート構文は、目で追いにくく、差分も読みにくくなります。また、コードベース全体でスペースの入れ方が揃っていないと、同じ式が複数の書き方で存在することになり、grep を使ったリファクタリング（変数やタグの検索）が当てにならなくなります。Django と Jinja のスタイルガイドはどちらも、`{{ var }}` や `{% tag %}` のようにスペースを 1 つずつ入れて書いています。

handlebars と golang のプロファイルには適用されません。

悪い例：

```html
{{user.name}}
```

良い例：

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

テンプレートタグ（`{% extends %}`、`{% include %}`、`{% with %}`、`{% trans %}`、`{% now %}`）でシングルクォートとダブルクォートが混在すると、同じテンプレート名が 2 通りの書き方で現れるため、検索や一括での名前変更で半分を見落とします。ダブルクォートに統一すれば、タグの引数をファイル内のほかの部分にある HTML 属性の引用符と揃えられます。

HTML 属性値の中のシングルクォート（例：`<span title="{% trans 'x' %}">`）は報告されません。そこでは属性のダブルクォートのせいで、シングルクォートを使うしかないためです。

`quote_style = "single"` を指定すると、このルールは代わりにシングルクォートを求め、フォーマッターもシングルクォートで書きます。

`--reformat` がこれらの引用符を書き換えます。

悪い例：

```html
{% extends 'base.html' %}
```

良い例：

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

`{% block %}` が多くの行にわたる場合やブロックが入れ子になっている場合、名前のない `{% endblock %}` からはどのブロックを閉じているのかがわからないため、編集中に別のブロックを閉じてしまいやすく、その結果、子テンプレートが誤った内容を上書きします。endblock に名前を付けると対応関係が明示され、間違った場所で閉じられたブロックを djLint と Django（endblock の名前が一致しないと TemplateSyntaxError を送出します）の両方が検出できます。対応関係のエラー（閉じられていないブロック、対応する開始タグのない endblock、名前の不一致）は正しさのチェックであり、T038 が扱います。

デフォルトでは無効です。`--include=T003` で有効にします。`--name-endblocks` が名前を書き込みます。

`{% block title %}``{% endblock %}` のように、ブロックが同じ行で開いて閉じる場合、名前は必要ありません。フォーマッターはほかのタグを含むブロックの中身をそれぞれ独立した行に移すため、1 行で書いたブロックでもフォーマット後に名前が必要になることがあります。`--name-endblocks` を指定すると、フォーマッターがその名前も書き込みます。

悪い例：

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

良い例：

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Static urls should follow {% static path/to/file %} pattern.`

/static/ のパスをハードコードすると Django の `{% static %}` タグを経由しないため、STATIC_URL が変わったとき（アセットを CDN に移す場合やサブパスにデプロイする場合など）にテンプレートが壊れ、ManifestStaticFilesStorage が生成するハッシュ付きのファイル名も使われないので、本番環境で 404 や古いキャッシュのアセットの原因になります。このルールは文字どおりの `/static/` という接頭辞を探すため、静的ファイルを別のパスで配信しているプロジェクトは対象外です。

悪い例：

```html
<link rel="stylesheet" href="/static/css/style.css">
```

良い例：

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

/static/ のパスをハードコードすると Flask/Jinja の url_for('static', ...) を経由しないため、アプリが URL の接頭辞の下にマウントされたときや、静的ファイルのフォルダーやホストが変わったときにアセットが 404 になり、フレームワークが付けるキャッシュ回避用のクエリ文字列も失われます。このルールは文字どおりの `/static/` という接頭辞を探すため、静的ファイルを別のパスで配信しているプロジェクトは対象外です。

悪い例：

```html
<link rel="stylesheet" href="/static/css/style.css">
```

良い例：

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have a non-empty lang attribute.`

`<html>` に lang 属性がないと、スクリーンリーダーは発音の規則を推測するしかなく、ページを誤った言語で読み上げることがあります。また、ブラウザーは翻訳、ハイフネーション、ロケールに応じた引用符を正しく提供できません。ページの言語の宣言は、WCAG 2.1 の達成基準 3.1.1（レベル A）です。

`lang=""` と値のない `lang` はどちらも言語が不明であることを表すため、属性がない場合と同じように報告されます。

悪い例：

```html
<!DOCTYPE html>
<html>
</html>
```

良い例：

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`Img tag should have height and width attributes.`

デフォルトでは無効です。`--include=H006` で有効にします。

`<img>` に width と height がないと、ブラウザーは画像のダウンロード前に表示領域を確保できないため、画像が読み込まれるにつれて周囲のコンテンツがずれます。このレイアウトのずれは Cumulative Layout Shift（Core Web Vitals の指標の 1 つ）を悪化させ、ページが落ち着くまでのあいだにユーザーが誤ってクリックする原因にもなります。

悪い例：

```html
<img src="cat.png" alt="Cat">
```

良い例：

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

`<html>` タグの前に `<!DOCTYPE>` がないと、ブラウザーは古いボックスモデルやレイアウトの挙動を再現する後方互換モード（quirks モード）でページを描画するため、CSS の表示がブラウザーごとに異なります。doctype の前にあるテンプレートタグやコメントは問題ありません。doctype が前になければならないのは `<html>` タグだけです。

悪い例：

```html
<html lang="en">
</html>
```

良い例：

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Attributes should be double quoted.`

引用符のスタイルが混在していると、属性値が目で追いにくく grep でも探しにくくなります。また、シングルクォートで囲んだ値は、内容にアポストロフィが含まれた途端に壊れます。ダブルクォートは HTML の仕様、フォーマッター、ほとんどのスタイルガイドで使われている慣習なので、ダブルクォートに統一すれば、テンプレートをより広いエコシステムと揃えられます。

悪い例：

```html
<div class='content'></div>
```

良い例：

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

HTML パーサーは大文字のタグ名を受け付けますが、XHTML や XML のシリアライズでは大文字と小文字が区別されるため拒否されます。また、大文字と小文字が混在するとテキスト検索や差分のレビューが当てにならなくなります（`<h1>` を grep しても `<H1>` は見つかりません）。タグ名を小文字にすれば、テンプレートの移植性と一貫性を保てます。

フォーマッターに大文字・小文字をそのままにするよう指示する `--ignore-case` を指定した場合は報告されません。

悪い例：

```html
<H1>Welcome</H1>
```

良い例：

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

大文字の属性名は XHTML/XML のシリアライズでは無効であり、テンプレート全体のテキスト検索も妨げます（src= を grep しても SRC= は見つかりません）。いずれにせよ DOM は HTML の属性名を小文字に正規化するため、大文字で書いても一貫性が損なわれるだけで利点はありません。報告されるのは、フォーマッターが小文字にする名前（`class`、`id`、`src`、`width`、`height`、`alt`、`style`、`lang`、`title`、`media`、`srcset`）だけです。`--reformat` がこれらを修正します。また、`:itemID` のようなフレームワークのバインディングや、`data-ID` のようなより長い名前は、大文字・小文字がそのまま保たれます。

フォーマッターに大文字・小文字をそのままにするよう指示する `--ignore-case` を指定した場合は報告されません。

悪い例：

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

良い例：

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

引用符で囲まれていない属性値は最初の空白で終わるため、class=btn primary のような値では、スペース以降がすべて黙って失われます（ブラウザーは "primary" を独立したブール属性として扱います）。テンプレート変数から来る値は特に壊れやすく、レンダリングされたスペース、"="、">" のどれか 1 つでタグが壊れます。引用符で囲めば、値の境界が明確になり安全です。

悪い例：

```html
<div class=test></div>
```

良い例：

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

"=" の前後にスペースがあると、タグは 3 つの別々のトークンのように読め、1 回の編集でばらばらになりかねません。途中で行が折り返されたり切り詰められたりすると、値のないブール属性と余計なテキストが残ります。name="value" を続けて書くことは、単純なテキストツール（grep、検索と置換）が前提としていることでもあるため、スペースの入れ方が混在していると、属性を確実に見つけたりリファクタリングしたりするのが難しくなります。`--reformat` がスペースを取り除きます。

悪い例：

```html
<div class = "test"></div>
```

良い例：

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

alt 属性がないと、スクリーンリーダーは画像のファイル名を読み上げるか、何も読み上げないため、WCAG 1.1.1（非テキストコンテンツ）を満たしません。alt テキストは、画像の読み込みに失敗したときにユーザーに表示されるものでもあります。装飾目的の画像には、支援技術が読み飛ばせるように明示的に空の alt="" を付けてください。これもこのルールを満たします。

値のない `alt` は、装飾画像の場合の `alt=""` と同じなので、受け入れられます。

悪い例：

```html
<img src="cat.jpg" height="200" width="300">
```

良い例：

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

連続した空行は、レンダリングされたページには何の影響もありません（HTML は空白をまとめます）が、テンプレートを肥大化させ、隣接する行が変わったときに差分を読みにくくします。djLint のフォーマッターはデフォルトで空行を完全に削除する（残すのは最大 `max_blank_lines` 行までで、そのデフォルトは 0）ため、連続した空行が残っていれば、フォーマットされていないコードであることを示します。

悪い例：

```html
<div>one</div>


<p>two</p>
```

良い例：

```html
<div>one</div>

<p>two</p>
```

#### H015

`Follow h tags with a line break.`

見出しは文書のアウトラインを形作るブロックレベルの目印です。閉じ h タグと同じ行に次の要素を詰め込むと、ソース上でその構造が見えなくなり、どちらかの要素を編集しただけで差分では両方が変更されたように表示されます。各見出しの後に改行を入れれば、テンプレートの見た目の構造をレンダリング後のアウトラインと揃えられます。

悪い例：

```html
<h1>Heading</h1><p>Intro text.</p>
```

良い例：

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Missing title tag in html.`

HTML の仕様では、すべての文書に title 要素が必要です。title がないと、ブラウザーのタブ、ブックマーク、履歴にはページ名ではなく生の URL が表示され、検索エンジンはページの主要なラベルを失い、スクリーンリーダーのユーザーは読み込み時に最初に読み上げられる情報を失うため、WCAG 2.4.2（ページタイトル、レベル A）を満たしません。

完全な `<html>`...`</html>` 文書を含むファイルでのみ検出されるため、パーシャルや、ベーステンプレートを継承する子テンプレートが報告されることはありません。クライアント側でタイトルを設定する SPA のシェルにも、静的な `<title>` は必要です。最初の描画時、クローラー、JavaScript が失敗したときに表示されるのはこのタイトルだからです。

悪い例：

```html
<html lang="en">
<body>Content</body>
</html>
```

良い例：

```html
<html lang="en">
<head>
<title>My page</title>
</head>
<body>Content</body>
</html>
```

#### H017

`Void tags should be self closing.`

XML/XHTML としても解析できなければならないテンプレート（または XML ベースのツールに渡すテンプレート）では、閉じスラッシュなしで書かれた空要素は拒否されます。また、コードベース全体で `<br>` と `<br />` が混在すると、差分が不揃いになります。このルールは XHTML スタイルの慣習を強制し、すべての空要素を同じ方法で閉じるようにします。

デフォルトでは無効です。`--include=H017` で有効にします。H018 とは両立しないため、2 つの慣習のどちらか一方だけを有効にしてください。`--close-void-tags` が html の空要素にスラッシュを追加します。svg の `<path>` は書かれたままになるので、手作業で閉じてください。

悪い例：

```html
<br>
<meta charset="utf-8">
```

良い例：

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Internal links should use the {% url ... %} pattern.`

ハードコードされた内部 URL は、urls.py でルートのパスが変わると黙って古くなり、URLconf のテストでは検出できないリンク切れや無効なフォームの action を生みます。`{% url %}` はルート名からパスを解決するため、パスを変更するとすべてのリンクが一度に更新されます。

悪い例：

```html
<a href="/accounts/login">Login</a>
```

良い例：

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

HTML Living Standard では、空要素の末尾のスラッシュには意味がありません（パーサーは無視します）。そのため `<br />` と書くと、HTML にはない XML 風の自己終了の動作をほのめかすことになり、読み手が空要素ではないタグにまでスラッシュを付けてしまうおそれがあります。そこでは余計な / は黙って捨てられ、閉じられていないタグのバグを覆い隠します。このルールは、空要素を単純な > で終えることを強制します。

デフォルトでは無効です。`--include=H018` で有効にします。H017 とは両立しないため、2 つの慣習のどちらか一方だけを有効にしてください。SVG は XML であり、スラッシュが必要なので、SVG の `<path />` は対象外です。`--close-void-tags` を指定した場合は報告されません。その場合、このルールが報告するスラッシュをフォーマッターが書き込むためです。

悪い例：

```html
<br />
<meta charset="utf-8" />
```

良い例：

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

ハードコードされた内部 URL は、ルートのパスが変わったときやアプリが接頭辞の下にマウントされたときに黙って壊れ、リンク切れや 404 に送信するフォームの action が残ります。url_for() はエンドポイント名から URL を組み立てるため、ルートの変更は自動的にすべてのテンプレートに反映されます。

悪い例：

```html
<a href="/accounts/login">Login</a>
```

良い例：

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

javascript: の URL は、中クリックや新しいタブで開く操作を壊し、JavaScript が無効なときや読み込みに失敗したときには何もせず、厳格な Content Security Policy でブロックされ、典型的な XSS インジェクションの入口にもなります。代わりに href には実際の URL を使い、動作はイベントハンドラーで付けてください。厳格な CSP の下ではインラインの on* ハンドラーもブロックされます。例の onclick はテンプレート内でできる最小限の修正であり、スクリプトファイルから addEventListener でリスナーを付けるほうが望ましい方法です。

悪い例：

```html
<a href="javascript:openPopup()">Open popup</a>
```

良い例：

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

空のタグのペアは何もコンテンツを表示しませんが、それでも DOM ノードを作るため、スタイルシートのマージン、ボーダー、flex/grid の gap が適用されて、原因を追いにくい謎の余白が生じます。たいていは以前の編集で残ったマークアップです。通常のマークアップで正当に空になるタグ（td、th、li、dt、dd、slot）は対象外です。属性を持つタグ（`<div id="app">``</div>` のような JS のマウントポイントや、`<i class="fa fa-user">``</i>` のようなアイコンフォントの要素）も報告されません。該当するのは属性がまったくない空のペアだけです。

悪い例：

```html
<p>Saved.</p>
<span> </span>
```

良い例：

```html
<p>Saved.</p>
```

#### H021

`Inline styles should be avoided.`

インラインスタイルはどのスタイルシートのセレクターよりも詳細度が高いため、後から上書きするには !important が必要になります。また、style-src に 'unsafe-inline' を含まない Content Security Policy ではブロックされ、見た目の指定がテンプレート中に散らばるため、テーマやデザインを変更するにはスタイルシート 1 つではなくマークアップを編集する必要があります。宣言は CSS クラスに移してください。ただし HTML メールのテンプレートは正当な例外で、多くのメールクライアントが `<style>` ブロックを取り除くため、インラインスタイルが標準的な手法です。メールテンプレートのディレクトリを除外するか、それらに対してこのルールを無効にしてください。

悪い例：

```html
<div style="color: red;">Wrong username or password.</div>
```

良い例：

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

HTTPS で配信されるページにある単なる http:// のサブリソースは混在コンテンツです。ブラウザーはスクリプト、スタイルシート、iframe を完全にブロックし、画像は自動的にアップグレードするか警告を出します。http:// のページへの `<a>` リンクは混在コンテンツではありませんが、それでも訪問者を、傍受や改ざんの危険がある暗号化されていない接続に送ることになります。本当に TLS を持たない内部ホストへの参照も報告されます。ルールを無効にするのではなく、その箇所を `{# djlint:off H022 #}` ブロックで抑制してください。

悪い例：

```html
<a href="http://example.com">Example</a>
```

良い例：

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

HTML5 の文書は UTF-8 なので、文字そのものはどこでも使え、レビュー担当者が実際に読むのもその文字です。実体参照のタイプミス（例：`&mdsah;`）はブラウザーに検出されず、壊れたテキストとしてそのまま表示されます。djLint は、構文上の意味を持つ実体参照（`&lt;`、`&gt;`、`&amp;`、`&quot;`、`&apos;`、そしてそのまま書くとテンプレートの区切り文字を完成させてしまう、波かっこの `&lbrace;` と `&rbrace;`、および `&percnt;`、`&num;`、`&dollar;`）と、目に見えないため文字そのものではレビューできない文字を表す実体参照を許可します。後者には、スペース（`&nbsp;`、`&thinsp;`、`&hairsp;`）、結合子と制御マーク（`&zwnj;`、`&zwj;`、`&lrm;`、`&rlm;`）、`&shy;` があり、名前付き、10 進数、16 進数のどの形式でも同じです。

`--reformat` が実体参照を文字に書き換えます。テンプレートタグの中に書かれた実体参照は、ページではなくタグの一部なので、ルールもフォーマッターも触れません。`--no-entity-formatting` は書き換えを無効にしますが、ルールは有効のままなので、実体参照は引き続き報告されます。実体参照を残すには、`H023` を `ignore` に追加してください。

悪い例：

```html
<p>Dates 1900 &mdash; 2000</p>
```

良い例：

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript と text/css は `<script>` と `<style>` の HTML5 でのデフォルトなので、この属性はブラウザーが無視する無駄なものです。WHATWG の仕様も、省略するよう明記しています。省略しておけば、モジュールスクリプト（type="module" が実際に意味を持つ場所）にコピーされたときに要素を壊してしまう、古い MIME 文字列が残ることもありません。

悪い例：

```html
<script type="text/javascript" src="app.js">
```

良い例：

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

対応する開始タグや終了タグのないタグがあると、ブラウザーはエラー回復処理で要素の終わりを推測するしかなくなり、後続のマークアップが誤った要素に取り込まれます。その結果、レイアウト、CSS セレクター、JavaScript の DOM クエリが、ブラウザーごとに異なる形で黙って壊れます。H025 は、`<p>` の中で開かれた `<ol>` や `<ul>` も報告します。HTML パーサーはリストの前で段落を閉じるため、マークアップは書かれたとおりには入れ子になりません。

悪い例：

```html
<div>
  <p>Hello</p>
```

良い例：

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Empty id and class tags can be removed.`

空の属性に一致する class セレクターや id セレクターはなく、空の id は無効な HTML です（id の値は空文字列であってはなりません）。ただし、`div[class]` のような属性の存在セレクターには一致するため、そのように書かれたスタイルシートには、属性を削除したことが影響します。空の属性はたいてい、変数を埋め込むつもりだったテンプレートのバグを示しているので、削除するか値を埋めれば、そのバグが見過ごされることはなくなります。

悪い例：

```html
<div id="" class="">content</div>
```

良い例：

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

`{% ... %}` や `{{ ... }}` の中で開いたまま閉じられていない引用符があると、テンプレートエンジンはタグを誤って解析します。Django と Jinja は、レンダリング時に TemplateSyntaxError を送出するか、タグの残りの引数を文字列の内容として黙って飲み込むため、ページは 500 エラーになるか、引数が欠けた状態でレンダリングされます。

悪い例：

```html
{% trans "Welcome %}
```

良い例：

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

デフォルトでは無効です。`--include=T028` で有効にします。

空白制御タグが取り除く空白は、レンダリングされる空白です。そのため、このルールは失っても困る空白がない属性にだけ適用してください。`alt="{%- if brand -%}Acme{%- endif -%} logo"` は `Acmelogo` とレンダリングされ、svg の `d="M12 {%- if big -%}20{%- endif -%} 4Z"` は別のパスになります。このルールがオプトインなのはこのためです。

属性値の中のテンプレートタグは、その前後の空白や改行をレンダリング後の属性にそのまま出力します。そのため、通常の `{% if %}`/`{% for %}` タグで組み立てた href や src には余計なスペースが入り、壊れた URL になることがあります。Jinja/Nunjucks の空白制御タグ（`{%- ... -%}`）はその前後の空白を取り除くため、属性は 1 つのきれいな値としてレンダリングされます。class 属性は対象外です。クラス名のあいだの余分な空白は無害だからです。

django プロファイルには適用されません。Django のテンプレートタグは `{%- -%}` による空白制御に対応していません。

悪い例：

```html
<a href="{% if x %}/home{% endif %}"></a>
```

良い例：

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

HTML の仕様では、フォームの method のキーワードは小文字（get、post）で定義されています。ブラウザーが大文字の表記を受け付けるのは、大文字・小文字を区別しない代替の照合によるものにすぎません。正規の小文字の形に揃えておけば、テンプレートに一貫性が生まれて grep もしやすくなり、厳格なバリデーターや XHTML ベースのツールチェーンから警告されることもなくなります。

悪い例：

```html
<form method="POST"></form>
```

良い例：

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

検索エンジンは、検索結果でページタイトルの下に表示するスニペットとして meta description を使います。これがないと、ページ内の任意のテキストからスニペットが作られるため、クリック率が下がり、ページが共有されたときのリンクのプレビューも見劣りします。

完全な `<html>`...`</html>` 文書を含むファイルでのみ検出されます。スニペットの話は、公開されて検索エンジンにインデックスされるページに当てはまります。認証が必要なアプリやイントラネットのアプリでは、このルールは無効にされることがよくあります。

悪い例：

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

良い例：

```html
<html lang="en">
  <head>
    <title>Home</title>
    <meta name="description" content="A short summary of this page.">
  </head>
  <body>Welcome</body>
</html>
```

#### T032

`Extra whitespace found in template tags.`

テンプレートタグの引数のあいだに連続したスペースやタブがあっても目に見えないノイズになるだけです。差分の中で実際の違いを覆い隠し、引数の欠落を見つけにくくし、djLint のフォーマッターが出力するスペース 1 つのスタイルからずれるため、不要な再フォーマットの変更を生みます。引用符で囲まれた文字列の中の空白は保持され、報告されません。

悪い例：

```html
{% static  'css/style.css' %}
```

良い例：

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

フォームの action の値の先頭や末尾にある空白は、レンダリングされる URL の一部になります。ブラウザーは解析時にこれを取り除きますが、ブラウザー以外のクライアントや、値をそのまま使うテストではそうとは限りません。また、`{% url %}` タグの前後にある余計なスペースは、ほぼ確実にタイプミスであり、サーバー側のルートの照合に失敗する送信先 URL を生成します。

悪い例：

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

良い例：

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Did you intend to use {% ... %} instead of {% ... }%?`

}% はほぼ確実に %} のタイプミスです。テンプレートエンジンは }% をタグの区切り文字として認識しないため、タグはまったく解析されません。生の {% ... }% のテキストがレンダリング後の HTML に漏れ出すか、閉じられていないタグに達したところでエンジンが構文エラーを送出します。

悪い例：

```html
{% include "footer.html" }%
```

良い例：

```html
{% include "footer.html" %}
```

#### H036

`Do not use br tags for spacing.`

html の仕様では、`<br>` を使えるのは、住所や詩のように、改行がコンテンツそのものの一部である場合だけです。そのような使い方はそのままにされます。報告されるのは、仕様が認めていない見た目のための使い方です。つまり、縦方向の余白となる 2 つ以上の連続した改行と、ブロック要素の内側の端にあり、要素自身のマージンと同じ効果しかない改行です。どちらも狭い幅でのテキストの再配置を崩し、スクリーンリーダーは何も読み上げるもののない場所で強制改行を読み上げます。

悪い例：

```html
<p>Shipping is free.<br><br>Delivery takes 3 days.</p>
```

良い例：

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

重複した属性は無効な HTML であり、ブラウザーは最初のものだけを残して残りを黙って捨てるため、2 つ目の class や style の値は決して反映されず、実際のバグを覆い隠します。このチェックはテンプレートを考慮しており、互いに排他的な分岐（`{% if %}`/`{% else %}`）で繰り返される属性は報告されません。レンダリングされるのは 1 つだけだからです。

悪い例：

```html
<div class="card" id="profile" class="active">...</div>
```

良い例：

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

`{% if %}`、`{% for %}`、`{% macro %}` などのブロックタグに対応する終了タグがないと、Django と Jinja では TemplateSyntaxError という致命的なエラーになり、リクエスト時にページのレンダリングに失敗します。このルールは、それをデプロイ前に検出します。また、対応する開始タグのない終了タグや、誤って交差したブロック（例：`{% if %}``{% for %}``{% endif %}`）も報告します。

`{% block %}`/`{% endblock %}` の対応と endblock の名前の不一致はこのルールがチェックします。T003（デフォルトでは無効）は、さらに複数行にわたるすべての `{% endblock %}` に名前を求めます。custom_blocks で登録したカスタムブロックタグもチェックされ、その自己終了の / %} 形式も対象になります。

悪い例：

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

良い例：

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Unclosed template tag found.`

`{{` や `{%` で開いたテンプレートタグが、対応する `}}` や `%}` で閉じられていないと、タグとして解析されません。Django/Jinja は TemplateSyntaxError を送出するか、生の波かっこをページにレンダリングし、次の区切り文字までのすべてが黙って飲み込まれることもあります。このようなタイプミス（波かっこが 1 つ足りない、区切り文字が一致しない）は、テンプレートが部分的にはレンダリングされることもあるため、レビューで見落としがちです。

悪い例：

```html
<p>{{ user.name }</p>
```

良い例：

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

`{% extends %}` や `{% include %}` タグのテンプレート名がない、空、または空白だけの場合、読み込むものがありません。Django は、名前がまったくない場合は TemplateSyntaxError を、空の場合はレンダリング時に TemplateDoesNotExist を送出します。そのため、テンプレートファイル自体は構文的にもっともらしく見えても、本番環境ではページが 500 エラーになります。

悪い例：

```html
{% extends "" %}
```

良い例：

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

HTML タグをある `{% block %}` で開き、別のブロックで閉じると、それらのブロックの一方だけを上書きする子テンプレートは要素の半分だけを継承するため、レンダリングされたページのマークアップの対応が崩れます。するとブラウザーが予測できない形で要素を自動的に閉じたり入れ子を組み直したりして、実際に編集したテンプレートから遠く離れた場所でレイアウトや CSS セレクターが壊れます。各要素を同じブロック内で開いて閉じるようにすれば、どのブロックも独立して安全に上書きできます。

悪い例：

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

良い例：

```html
{% block content %}
<div class="wrapper">
</div>
{% endblock content %}
{% block footer %}
{% endblock footer %}
```

#### T041

`Extends tag should be the first tag in the template.`

Django は、`{% extends %}` の前に別のタグがあるテンプレートのコンパイルを拒否します。また、その前に書かれたテキストはレンダリングされるため、親テンプレートが出力するすべてのものより前にページに漏れ出します。Jinja もそのテキストをレンダリングし、nunjucks はそれを捨てます。つまり、どのエンジンでも、テンプレートは見た目どおりには動作しません。

`{# #}` コメントは何もレンダリングしないので数に入りません。`{% comment %}`、<code>{&#37; raw %}</code>、`{% verbatim %}` ブロック（名前付きかどうかを問わない）の中のもの、3 通りのどの書き方による `{# djlint:off #}` 領域、yaml のフロントマターも同様です。html コメントは数に入ります。エンジンはそれを親テンプレートの doctype より前にページに書き出すため、まさにこのルールが対象とする漏れになります。`{% blocktrans %}` ブロック、`{% filter %}` ブロック、`<?php ?>` ブロックも、いずれもレンダリングされるので数に入ります。チェックされるのは最初の `{% extends %}` だけです。2 つ目の `{% extends %}` はそれ自体が別のエラーです。jinja と nunjucks のプロファイルでは、その前にある分岐タグは数に入りません。jinja は親テンプレートを選ぶ方法として `{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}` をドキュメントに記載しているためです。django はテンプレートの残りを `{% extends %}` に読み込んだうえで `{% endif %}` を拒否するため、django プロファイルでは分岐タグも数に入ります。

handlebars、golang、liquid、angular のプロファイルには適用されません。

悪い例：

```html
{% load static %}
{% extends "base.html" %}
```

良い例：

```html
{% extends "base.html" %}
{% load static %}
```

#### H042

`Label for attribute has no matching element id in this file.`

このチェックは、確実に解析できるファイルに対してだけ実行されます。このファイル内には現れない id をレンダリングする可能性のあるもの（フォームウィジェットのような `{{ ... }}` の出力、`{% include %}` や `{% extends %}`、認識できないテンプレートタグ）がファイルに含まれていれば、そのファイルではルールは何も報告しません。実行された場合、報告されるのは実際に壊れている関連付けです。

悪い例：

```html
<label for="email">Email</label>
<input id="username">
```

良い例：

```html
<label for="email">Email</label>
<input id="email">
```

#### T042

`Content outside a block is not rendered in a template that extends another.`

テンプレートが別のテンプレートを継承すると、何を出力するかは親が決め、子は親のブロックを埋めるだけになります。`{% extends %}` の後、どの `{% block %}` の外に書かれたテキストや html も、レンダリング時に黙って捨てられるため、ソース上では問題なさそうに見える段落がページに表示されることはありません。

その位置にあるテンプレートタグは実行されるため、`{% load %}`、`{% set %}`、ブロックを囲む `{% if %}` はそのままにされます。`{# #}` と `{% comment %}` のコメント、html コメント、<code>{&#37; raw %}</code> と `{% verbatim %}` のブロック、そして `{% macro %}`、ブロック形式の `{% set %}`、`{% partialdef %}`、`{% addtoblock %}` の本体も同様です。これらの本体は出力されるのではなく取り込まれるからです。`{% blocktrans %}` は `{% block %}` ではないため、`{% blocktrans %}` のテキストは報告されます。対象となるのは extends タグより後のコンテンツだけで、連続したコンテンツはそれぞれ、その先頭で 1 回だけ報告されます。

エンジンは html より先にテンプレートタグを読むため、html コメントや `<pre>` の中に書かれた `{% extends %}` もやはり実行され、ファイルは子テンプレートになります。本当に隠せるのは `{# #}`、`{% comment %}`、<code>{&#37; raw %}</code>、`{% verbatim %}` だけです。html コメントの中のテキストはどちらにしても読み手に届かないので報告されませんが、そこに書かれたタグは読み込まれます。

handlebars、golang、liquid、angular のプロファイルには適用されません。

悪い例：

```html
{% extends "base.html" %}
<p>This paragraph is never shown.</p>
{% block content %}
<h1>Welcome</h1>
{% endblock %}
```

良い例：

```html
{% extends "base.html" %}
{% block content %}
<h1>Welcome</h1>
<p>This paragraph is shown.</p>
{% endblock %}
```

#### H043

`Button tag should have a type attribute.`

`type` のない `<button>` はデフォルトで `submit` になるため、スクリプトを実行するために書いたボタンが、それを囲むフォームまで送信してしまい、ページが再読み込みされます。type を明示すれば、これを防げます。

悪い例：

```html
<form>
  <button onclick="preview()">Preview</button>
</form>
```

良い例：

```html
<form>
  <button type="button" onclick="preview()">Preview</button>
</form>
```

#### T043

`Block name is used more than once in the template.`

Django、Jinja、Nunjucks はいずれも、2 つのブロックに同じ名前が付いたテンプレートの解析を拒否するため、ページはまったく読み込まれません。エンジンは 2 つのブロックが `{% if %}` の別々の分岐にあるかどうかを考慮しないため、ブロックが並んでいても一方が他方の中に入れ子になっていても、ブロック名はテンプレート全体で一意でなければなりません。

数に入るのは `{% block %}` だけです。`{% blocktrans %}` はブロックではなく、`{% endblock name %}` は閉じるブロックの名前を示しているだけです。エンジンは `Content` と `content` を 2 つのブロックとして扱うため、名前は書かれたとおりに比較されます。

スキップされるのは、エンジン自体がまったく解析しないものだけです。つまり、テンプレートコメント、`{% comment %}` ブロック、<code>{&#37; raw %}</code> や `{% verbatim %}` の本体、`djlint:off` 領域です。html コメント、`<script>`、`<style>`、`<pre>`、`<textarea>` の本体、`{% filter %}` の本体の中に書かれたブロックは数に入ります。エンジンはそれらをすべて読み込み、重複した名前があればやはりエラーを送出するからです。

`{% embed %}` は独自のスコープを開きます。その中のブロックはこのテンプレートではなく埋め込まれたテンプレートを埋めるため、同じパーシャルを 2 回 embed すれば、それぞれに `{% block body %}` を書けます。1 つの embed の中で名前が繰り返されている場合は報告されます。

handlebars、golang、liquid、angular のプロファイルには適用されません。

悪い例：

```html
{% block content %}{% endblock %}
{% block content %}{% endblock %}
```

良い例：

```html
{% block content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

#### H044

`Thead should not mix th and td cells.`

行はそれぞれ単独で判定されるため、html の仕様が `thead` 内で見出しの行の横に置いている、`td` による説明の行は混在とはみなされません。行の先頭にある空の `td` は、最初の列を縦に見出しが並ぶ表の角のセルであり、W3C のアクセシビリティのチュートリアルが求めているマークアップなので、スキップされます。

`th` と `td` はスクリーンリーダーに対して異なる意味を持ち、通常は CSS も異なるため、見出しの行に 1 つだけ紛れ込んだセルはデータとして読み上げられ、隣の列とは違うスタイルになります。この混在は html として正当なので、気付きにくくなります。

悪い例：

```html
<thead>
  <tr>
    <th>Name</th>
    <td>Size</td>
  </tr>
</thead>
```

良い例：

```html
<thead>
  <tr>
    <th>Name</th>
    <th>Size</th>
  </tr>
</thead>
```

#### T044

`Output tag holds a statement keyword; use a block tag.`

golang、handlebars、angular のプロファイルには適用されません。

出力タグは値を出力するものであり、`if`、`for`、`url`、`include` などは、ブロックタグに書くべき文です。Django、Jinja、Nunjucks はいずれも `{{ if x }}` を構文エラーとして拒否します。また、`{{ endif }}` のように終了のキーワードだけを書くと、何もレンダリングしない変数として読まれ、閉じるはずだったブロックは開いたままになります。そのため、ページは読み込みに失敗するか、条件で隠すはずだったものを表示してしまいます。

キーワード単体は普通の変数名なので、`{{ url }}`、`{{ url|default:"/" }}`、`{{ set.name }}` は報告されません。報告されるのは、引数が付いたキーワードと、`{{ endif }}` や `{{ else }}` のような単独の終了または分岐のキーワードだけです。`if` や `for` のような制御キーワードは式の先頭に来ることができないため、その後に続くものは演算子も含めてすべて引数とみなされ、`{{ if -1 > count }}` は報告されます。それ以外の名前は変数や関数としても使われるため、引数とみなされるのは引用符で囲んだ文字列か単語だけです。そのため、たまたまそれらの名前で始まる式はそのままにされます。`{{ url ~ "/x" }}`、`{{ url if url else "#" }}`、`{{ url ? url : '#' }}`、`{{ block ('title') }}`、`{{ block .super }}`、`{{ filter [0] }}` はいずれも報告されません。

<code>{&#37; raw %}</code> や `{% verbatim %}` ブロックの本体は、テンプレート構文ではなくテキストなのでスキップされます。名前付きの形式 `{% verbatim vueapp %}...{% endverbatim vueapp %}` も含まれるため、このように保護された Vue や Handlebars の `{{ }}` は報告されません。`{% trans "Write {{ if x }} instead" %}` のように、ブロックタグの引用符で囲んだ引数の中に書かれた `{{ }}` も、エンジンが出力するテキストなので、そのままにされます。

悪い例：

```html
{{ if user.is_active }}
```

良い例：

```html
{% if user.is_active %}
```

#### H045

`Iframe tag should have a title attribute.`

スクリーンリーダーは、iframe をそのアクセシブルな名前で読み上げます。名前がないと、フレームの URL を読み上げるか何も読み上げないため、中に入る前に埋め込まれたページが何なのかを知る方法がありません。WCAG ではこれを 4.1.2 名前（name）・役割（role）及び値（value）で扱っており、axe と html-validate はどちらもこのチェックをデフォルトで備えています。

名前は `title`、`aria-label`、`aria-labelledby` のいずれかから得られ、3 つのうちどれか 1 つがあればルールを満たします。テンプレートタグで書かれた名前も数に入るため、ページごとにタイトルを付けたフレームは報告されません。

悪い例：

```html
<iframe src="/report/"></iframe>
```

良い例：

```html
<iframe src="/report/" title="Quarterly report"></iframe>
```

#### T045

`Template tag inside an html comment still runs; use a template comment to disable it.`

html コメントがマークアップを隠すのはブラウザーからであって、テンプレートエンジンからではありません。`<!-- {% include "debug.html" %} -->` は Django、Jinja、Nunjucks、Handlebars、Go のいずれでもファイルをレンダリングし、`<!-- {% if debug %}...{% endif %} -->` も評価されます。そのため、このようにコメントアウトしたタグは実行され続け、その出力はコメントの中に入るか、`-->` を含んでいればコメントの外に飛び出します。タグの実行を止められるのはテンプレートコメント（Django と Jinja の `{# #}`、Handlebars の `{{! }}`、Go の `{{/* */}}`）だけです。

報告されるのは文のタグだけです。つまり、それを持つプロファイルでの `{% %}`、handlebars のセクション、終了タグ、パーシャル、そして `{{if}}` や `{{end}}` のような Go のキーワードです。`<!-- built {{ version }} -->` のようにコメントに値を出力するのは意図的な使い方なので、そのままにされます。テンプレートコメント、`{% comment %}` ブロック、raw ブロックの中のタグや、Internet Explorer 向けの条件付きコメント `<!--[if IE]> ... <![endif]-->`（その本体は指定したブラウザー向けのマークアップ）も同様です。

Go のキーワード単体は、ほかのすべてのエンジンでは普通の変数名なので、`<!-- period {{ start }} to {{ end }} -->` や `<!-- Template: {{ template }} -->` は Django、Jinja、Nunjucks、Handlebars、Liquid では値であり、文として読まれるのは `--profile golang` の場合だけです。`{{ if .X }}` や `{{ template "footer" . }}` のように Go のオペランドを伴うものは、ほかのどのエンジンも出力しない文なので、どのプロファイルでも報告されます。同様に、`{%` もエンジンがそれを持つ場合にだけ読まれるため、`--profile handlebars` と `--profile golang` ではテキストとして扱われます。また、`<!-- battery at 50{% charge -->` のように閉じかっこが続かない開始は、見たとおりの文章です。条件付きコメントとみなされるのは、そのように書かれたもの、つまり `<!--[if` で始まり、大文字・小文字を問わず `<![endif]-->` で閉じられているものです。閉じられていないものは、ブラウザーがそう読むとおり普通のコメントであり、その中のタグは報告されます。

悪い例：

```html
<!-- {% include "banner.html" %} -->
```

良い例：

```html
{# {% include "banner.html" %} #}
```

#### H046

`Tabindex should not be positive.`

正の `tabindex` は、要素をタブ順序の先頭に引き出し、tabindex を持たないすべての要素より前に置きます。1 つあるだけでキーボードユーザーにとってページ全体の順序が入れ替わり、以後はコントロールを追加するすべてのテンプレートで、その順序を手作業で維持しなければならなくなります。WCAG ではこれを 2.4.3 フォーカス順序で扱っています。

`0` は要素を文書上の位置どおりにタブ順序に入れ、`-1` はスクリプトからはフォーカスできるようにしたまま要素をタブ順序から外します。どちらも報告されません。テンプレートタグで書かれた値も、ここでは数値がわからないため報告されません。

悪い例：

```html
<input tabindex="1">
```

良い例：

```html
<input tabindex="0">
```

#### H047

`Aria-hidden should not be set on a focusable element.`

`aria-hidden="true"` は要素をアクセシビリティツリーから外しますが、タブ順序には残すため、キーボードユーザーはその要素にたどり着いても何も読み上げられません。装飾的なアイコンを隠すのはこの属性の通常の使い方なので報告されません。報告されるのは、それ自体がフォーカスを受け取る要素だけです。

フォーカス可能とみなされるのは、`button`、`select`、`textarea`、`iframe`、`summary`、`href` を持つ `a` や `area`、hidden ではない `input`、`controls` を持つ `audio` や `video`、そして `contenteditable` または `0` 以上の `tabindex` を持つ任意の要素です。`disabled` のコントロールや `tabindex="-1"` を持つコントロールはすでにタブ順序から外れているので、そのままにされます。

悪い例：

```html
<button aria-hidden="true">Close</button>
```

良い例：

```html
<button type="button" aria-label="Close"><span aria-hidden="true">x</span></button>
```

#### H048

`Aria attribute is not one the specification defines.`

綴りを間違えた aria 属性はまったく何もしません。ブラウザーは警告せず、スクリーンリーダーも報告せず、マークアップはアクセシブルにしたように見えたままです。そのため、`aria-lable` が何年もテンプレートに残り、名前を付けるはずだったコントロールが名前のないままになることがあります。

ルールが知っている名前は、ARIA が定義しているものです。フレームワークが書くバインディングは単純な aria の名前ではないため、`:aria-label`、`v-bind:aria-label`、`[attr.aria-label]` はそのままにされます。

悪い例：

```html
<button type="button" aria-lable="Close">x</button>
```

良い例：

```html
<button type="button" aria-label="Close">x</button>
```

#### H049

`Viewport should not stop the page being zoomed.`

`user-scalable=no` や 2 未満の `maximum-scale` は、スマートフォンでのページの拡大を妨げます。多くの人にとって、拡大はページを読むための唯一の方法です。WCAG は 1.4.4 テキストのサイズ変更で 200% を求めています。ブラウザーはこの制限を無視することが増えていますが、それでもこのタグは、制限が守られる環境ではズームを無効にします。

name と content は、どちらの順序で書かれていても見つけられます。

悪い例：

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

良い例：

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### H050

`Element is obsolete and should be replaced.`

`<center>`、`<font>`、`<big>`、`<strike>`、`<tt>` は、見た目の指定を CSS が担うようになったときに廃止されました。`<marquee>`、`<blink>`、`<nobr>`、`<spacer>` は、そもそも標準だったことがありません。現在の html はどれも定義していないため、ブラウザーがそれらをどうレイアウトするかは何も保証されず、スタイルシートからもクラスのようには対象にできません。

ルールが知っている要素は、`acronym`、`applet`、`basefont`、`bgsound`、`big`、`blink`、`center`、`dir`、`font`、`frame`、`frameset`、`isindex`、`keygen`、`marquee`、`menuitem`、`nobr`、`noembed`、`noframes`、`plaintext`、`spacer`、`strike`、`tt`、`xmp` です。報告されるのは開始タグだけなので、各要素は 1 回だけ示されます。また、`<font-picker>` のように、名前がこれらで始まるだけのカスタム要素はそのままにされます。

悪い例：

```html
<center><font color="red">Warning</font></center>
```

良い例：

```html
<p class="warning">Warning</p>
```

#### H051

`Role is not one ARIA defines for markup.`

どの仕様にも名前のないロールは完全に無視され、要素は元々の意味のままになります。そのため、`role="buton"` を指定しても `<div>` は `<div>` のままで、スクリーンリーダーにとっては何でもないのに、マークアップは役割を与えられたように見えます。何も警告されないからこそ、このタイプミスは見つける価値があります。

ルールが知っている名前は、ARIA が作成者向けに定義しているロールに、DPUB-ARIA（`doc-chapter` など）と GRAPHICS-ARIA（`graphics-symbol` など）が追加するものを加えたものです。`landmark` や `sectionhead` のような ARIA の抽象ロールは報告されます。仕様では、これらはオントロジーを構築するために存在し、マークアップに書いてはならないとされています。

`role` にはフォールバックのリストとして複数の名前を書くことができ、それぞれがチェックされます。テンプレート構文を含む値は内容がわからないため、そのままにされます。`:role` や `[attr.role]` のような、フレームワークが書くバインディングも同様です。

悪い例：

```html
<div role="buton">Save</div>
```

良い例：

```html
<button type="button">Save</button>
```

#### H052

`Meta refresh should not reload or redirect the page on a timer.`

時間指定のリフレッシュは、読んでいる人の目の前からページを移動させてしまいます。読むのが遅い人、スクリーンリーダーを使っている人、あるいは単に中断された人は、警告もなく止める方法もないまま読んでいた場所を失います。これは WCAG 2.2.1 タイミング調整可能を満たしません。また、同じページを再読み込みするリフレッシュは、入力された内容をすべて捨ててしまいます。

遅延が 0 の場合はタイマーではなく即時のリダイレクトであり、サーバーでのリダイレクトが使えない場合には WCAG でも認められているため、報告されません。2 つの属性は、どちらの順序で書かれていても見つけられます。

悪い例：

```html
<meta http-equiv="refresh" content="30">
```

良い例：

```html
<meta http-equiv="refresh" content="0; url=/next-page">
```

#### H053

`Id is used more than once in the file.`

id は 1 つの要素に付ける名前です。同じ id を持つ 2 つ目の要素があると、`getElementById`、`<label for>`、フラグメントリンク、`aria-labelledby` が壊れます。ブラウザーは最初のものを使って残りを黙って無視するため、ラベル、リンク、スクリプトが何の警告もなく誤った要素を指してしまいます。

1 つの `{% if %}...{% else %}...{% endif %}` の互いに排他的な分岐にある 2 つの id は、両方がレンダリングされることはないので報告されません。`{% for %}` ループや `{% block %}` は分岐ではありません。その中にある id と、その外にある同じ id はどちらもレンダリングされるため、後のほうが報告されます。テンプレートタグで書かれた値は内容がわからないためそのままにされ、空の値も同様です。id はブラウザーと同じように厳密に比較されるため、`save` と `Save` は 2 つの別の id です。

分岐は、ファイルが書かれている言語に従って、区切り文字とタグ名のあいだにその言語が許すどのような空白があっても読み取られます。対象は、`{% elif %}` と `{% else %}`、liquid の `{% elsif %}` と `{% when %}`、go の `{{ else }}`、mako の `% else:` 行文、そして handlebars の `{{else}}`、その連鎖形の `{{else if x}}`、カスタムヘルパーを含むあらゆる `{{#helper}}` ブロックの inverse セクションです。`<template>` の内容は `getElementById` が決して届かない独立した文書フラグメントなので、その中の id は同じ `<template>` 内の id とだけ比較されます。2 つのテンプレートがそれぞれ同じ id の行を持つことはできますが、1 つのテンプレートの中に 2 つあれば報告されます。コメント、<code>{&#37; raw %}</code> や `{% verbatim %}` の本体、`djlint:off` 領域の中の id は、まったく読み取られません。

悪い例：

```html
<button type="submit" id="submit">Save</button>
<button type="submit" id="submit">Save and continue</button>
```

良い例：

```html
<button type="submit" id="submit">Save</button>
<button type="button" id="cancel">Cancel</button>
```

#### H054

`Interactive element should not be nested inside another.`

html では、`<a>` と `<button>` の中にインタラクティブコンテンツを入れることは禁止されています。リンクの中のボタンやボタンの中のリンクは無効なマークアップで、ブラウザーはそれぞれ独自の方法で修復し、スクリーンリーダーやキーボードのユーザーには 2 つのように振る舞う 1 つのコントロールが渡されます。axe も同じものを "nested-interactive" として報告します。

監視対象となるコンテナーは `href` を持つ `<a>` と `<button>` で、その中で報告されるコントロールは、`href` を持つリンク、`button`、`input`、`select`、`textarea` です。`href` を持たない `<a>` はインタラクティブではないので、どちらの側にあってもそのままにされます。hidden の input や、type をテンプレートタグで書いている input も同様です。`<template>` の内容は書かれた場所でレンダリングされないため、その中のコントロールは周囲のリンクの中に入れ子になっているとはみなされません。ただし、テンプレートの中で書かれた入れ子は報告されます。

属性として読まれるのは、タグが属性を書く位置だけです。`{% if not href %}` の `href` は変数名であり、`{# href="{{ url }}" #}` の中のものはコメントアウトされており、`data-attr=href` の中のものは別の属性に属しています。一方、`{% if %}` が自身のタグのあいだで書く `href` は、ほかと同じ属性です。開いたままのリンクやボタンは、ブラウザーと同じように周囲の要素とともに終わるため、1 つのタイプミスでファイルの残りすべてが報告されることはありません。トップレベルで開いたままのものは、終わらせる周囲の要素がないためファイルの最後まで続き、そこで H025 も孤立したタグとして報告します。

悪い例：

```html
<a href="/cart"><button>Add</button></a>
```

良い例：

```html
<a href="/cart" class="button">Add</a>
```

#### H055

`Lang attribute should be a language tag such as en or pt-BR.`

H005 は `<html>` に `lang` を求めますが、`lang="english"` や `lang="en_US"` のような値は、ブラウザーが知っている言語を何も示していないにもかかわらず H005 を満たしてしまいます。するとスクリーンリーダーはデフォルトの音声に戻り、翻訳やハイフネーションは誤った規則を選ぶか、何も選びません。値は BCP 47 のタグでなければなりません。つまり、2 文字または 3 文字の英字の後に、ハイフンに続く 1 〜 8 文字の英数字のサブタグが任意の数だけ続く形で、`en`、`pt-BR`、`zh-Hant-TW` などがその例です。

H005 に合わせて、チェックされるのは `<html>` タグだけです。空の値はそのルールに任せますが、空白だけの値は H005 が値として読むため、ここで報告されます。`lang="{{ LANGUAGE_CODE }}"` のようにテンプレートタグで書かれた値や、`lang="<?= $lang ?>"` のように php の短縮 echo で書かれた値は内容がわからないためそのままにされますが、`lang="$LANG"` のように `$` や `{` で始まるだけの値は書かれたとおりに読まれます。`xml:lang` や `data-lang` は `lang` としては読まれません。また、`{% if a > b %}` のように、属性より前のテンプレートタグの中に書かれた `>` があっても、属性は隠れません。

悪い例：

```html
<html lang="english">
```

良い例：

```html
<html lang="en">
```

#### H056

`Src should not be empty.`

html の仕様では空の `src` は無効とされており、ブラウザーはそれを文書自身の URL に対して解決すると警告しています。そのため、`<img src="">` はページを画像としてもう一度取得し、`<script src=""></script>` はスクリプトとして取得します。これはたいてい、スクリプトで埋めるつもりだったプレースホルダーです。修正方法は、実際の値ができるまで属性を削除するか、値を data 属性に保持することです。`<img src>` のように値なしで書かれた `src` も空であり、報告されます。

チェックされるのは `img`、`script`、`iframe`、`embed`、`source`、`track`、`audio`、`video` だけです。`src` が指すものを取得するのはこれらの要素だからです。報告されるのはブラウザーが空と読む値だけなので、`<img src=/static/logo.png>` のような引用符のない値はそのままにされます。空白だけの値やテンプレートタグで書かれた値も同様です。また、`srcset` と `data-src` は別の属性であり、このルールの判定対象ではありません。

悪い例：

```html
<img src="" alt="Logo">
```

良い例：

```html
<img src="{% static 'logo.png' %}" alt="Logo">
```

#### H057

`Video should have a captions track.`

音声付きの動画では、話の内容は音声にしか含まれていないため、キャプションがなければ、ろう者や難聴の視聴者には何も伝わりません。これは WCAG 1.2.2 キャプション（収録済）が求めていることです。`<video>` の中に `kind` が `captions` または `subtitles` の `<track>` があればルールを満たします。`kind` がまったくない `<track>` も、`subtitles` がデフォルトなので同様です。

`muted` の動画にはキャプションを付ける音声がないので報告されません。開始タグや本体にテンプレートタグを含む動画も報告されません。トラックや `muted` 属性が、djLint からは見えない場所でテンプレートによって書かれている可能性があるためです。ここでいうテンプレートタグとは、テンプレート言語が開く `{{`、`{%`、`{#`、`${` のことです。そのため、`onclick="$(this).play()"` のような jQuery のハンドラー、Alpine の `$refs`、CSS の波かっこ、フォールバックのテキストに書かれた価格は見たとおりの普通のテキストであり、動画は引き続き読み取られます。

`muted` は属性でなければならないため、`<video class=muted>` は muted という名前のクラスであり、報告されます。また、コメントアウトされた `<track>` や属性値の中に書かれた `<track>` は、トラックではなくテキストです。値の中の `</video>` は何も終わらせず、要素は本当の終了タグで閉じられた位置で判定されるため、開いたままの `<video>` は `H025` に任されます。

悪い例：

```html
<video controls src="talk.mp4"></video>
```

良い例：

```html
<video controls src="talk.mp4">
  <track kind="captions" src="talk.vtt" srclang="en">
</video>
```

<!-- oxfmt-ignore-end -->

### ルールの追加

新しいルールのプルリクエストを歓迎します！

よいルールは次の要素で構成されます：

- 名前
- コード
- メッセージ：エラーが見つかったときに表示するメッセージ。
- フラグ：正規表現のフラグ（例：re.I|re.M）。デフォルトは re.DOTALL です。
- パターン：エラーを見つける正規表現。
- 除外：ルールを適用しないプロファイルのリスト（省略可）。

ルールを検証するテストも含めてください。

## カスタムルール

`pyproject.toml` と同じ場所に `.djlint_rules.yaml` を作成すると、プロジェクト専用のカスタムルールを追加できます。このファイルにルールを追加すると、djLint がそれを読み込みます。別の場所にあるルールファイルは、CLI の `--rules` オプションで指定できます。

### パターンルール

正規表現のパターンのいずれかに一致したときに失敗するルールを追加できます：

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Python モジュールルール

カスタムの Python 関数をインポートして実行するルールを追加できます：

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

指定した `python_module` には、チェック対象の各ファイルに対して実行される `run()` 関数が含まれていなければなりません。この関数は次の引数を受け取る必要があります：

- `rule`：`.djlint_rules.yaml` 内のルールを表す dict。通常、この変数はルール名とメッセージを取得するのに使います。
- `config`：djLint の設定オブジェクト。
- `html`：ファイルの html の内容全体。
- `filepath`：現在チェックしているファイルのパス。
- `line_ends`：各行の `start` と `end` の文字位置のリスト。`djlint.lint.get_line()` と組み合わせて、文字位置から行番号を取得できます。例を参照してください。
- `*args, **kwargs`：将来ほかの引数を追加する可能性があるため、djLint のアップグレード時に失敗するリスクを減らせるように、この 2 つの引数を含めてください。

モジュールはプロジェクトのルートに置けます。関数が位置ではない `line` や `end` を返した場合、djLint はルール名を示すエラーで停止します。

関数は、エラーごとに 1 つ、次のキーを持つ dict のリストを返す必要があります：

- `code`：エラーを報告するルールのコード名（通常は `rule['name']`）
- `line`：行番号とその行内の文字番号を ':' で区切った文字列。
  たとえば `"2:3"` は、エラーが 2 行目の 3 文字目で見つかったことを意味します
- `end`：省略可。エラーの終了位置で、最後の文字の直後を `line` と同じ形式で書きます。省略すると、エラーは `match` の終わりで終わります。
- `match`：エラーを含む部分の内容
- `message`：エラーを知らせるために表示されるメッセージ（通常は `rule['message']`）

```python
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from djlint.helpers import inside_ignored_linter_block, inside_ignored_rule
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Any

    from djlint.settings import Config
    from djlint.types import LintError


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> list[LintError]:
    """Rule that fails if the html file contains 'bad'.

    This is just an example, in reality it's much simpler to do that with a
    "pattern rule".
    """
    return [
        {
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "end": get_line(match.end(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        }
        for match in re.finditer(r"bad", html)
        if not inside_ignored_rule(config, html, match, rule["name"])
        and not inside_ignored_linter_block(config, html, match)
    ]
```
