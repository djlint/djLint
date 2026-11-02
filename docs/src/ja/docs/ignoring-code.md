---
description: djLint にコードブロックをフォーマットさせない方法と、djLint のルールをインラインで無視する方法。
title: コードの無視
keywords: テンプレート リンター, テンプレート フォーマッター, djLint, HTML, テンプレート, フォーマッター, リンター, フォーマッターの使い方, コードの無視, ルールの無視
date: Last Modified
---

# コードの無視

コードは `djlint` タグで囲むと無視できます：

{% raw %}

通常の HTML の場合：

<!-- oxfmt-ignore -->

```html
<!-- djlint:off -->
<bad html to ignore> <!-- djlint:on --></bad>
```

コメントとして書く場合：

<!-- oxfmt-ignore -->

```html
{# djlint:off #} <bad html to ignore> {# djlint:on #}</bad>
```

長い形式のコメントとして書く場合：

<!-- oxfmt-ignore -->

```html
{% comment %} djlint:off {% endcomment %}
<bad html to ignore> {% comment %} djlint:on {% endcomment %}</bad>
```

golang 形式のコメントとして書く場合：

<!-- oxfmt-ignore -->

```html
{{ /* djlint:off */ }} <bad html to ignore> {{ /* djlint:on */ }}</bad>
```

handlebars 形式のコメントとして書く場合：

<!-- oxfmt-ignore -->

```html
{{!-- djlint:off --}} <bad html to ignore> {{!-- djlint:on --}}</bad>
```

{% endraw %}

## ルールの無視

無視するブロックの開始タグにルール名を加えると、特定のリンタールールだけを無視することもできます。

{% raw %}

<!-- oxfmt-ignore -->

```html
{# djlint:off H025,H026 #}
<p>
  {# djlint:on #}

  <!-- djlint:off H025-->
</p>

<p>
  <!-- djlint:on -->

  {% comment %} djlint:off H025 {% endcomment %}
</p>

<p>{% comment %} djlint:on {% endcomment %} {{!-- djlint:off H025 --}}</p>

<p>{{!-- djlint:on --}} {{ /* djlint:off H025 */ }}</p>

<p>{{ /* djlint:on */ }}</p>
```

{% endraw %}
