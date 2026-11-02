---
title: "コードの無視"
description: "djLint にコードブロックをフォーマットさせない方法と、djLint のルールをインラインで無視する方法。"
sidebar:
  label: "コードの無視"
---

コードは `djlint` タグで囲むと無視できます：

通常の HTML の場合：

<!-- prettier-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

コメントとして書く場合：

<!-- prettier-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

長い形式のコメントとして書く場合：

<!-- prettier-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

golang 形式のコメントとして書く場合：

<!-- prettier-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

handlebars 形式のコメントとして書く場合：

<!-- prettier-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## ルールの無視

無視するブロックの開始タグにルール名を加えると、特定のリンタールールだけを無視することもできます。

<!-- prettier-ignore -->
```html
{# djlint:off H025,H026 #}
<p>
{# djlint:on #}

<!-- djlint:off H025-->
<p>
<!-- djlint:on -->

{% comment %} djlint:off H025 {% endcomment %}
<p>
{% comment %} djlint:on {% endcomment %}

{{!-- djlint:off H025 --}}
<p>
{{!-- djlint:on --}}

{{ /* djlint:off H025 */ }}
<p>
{{ /* djlint:on */ }}
```
