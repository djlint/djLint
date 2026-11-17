---
title: "コードの無視"
description: "djLint にコードブロックをフォーマットさせない方法と、リンターのルールをインラインで無視する方法。"
---

`djlint:off` と `djlint:on` のコメントで囲んだコードは、フォーマッターもリンターもそのままにします。コメントは HTML のものでも構いません：

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

Django や Jinja のコメントでも：

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

`{% comment %}` ブロックでも：

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

Go テンプレートのコメントでも：

<!-- oxfmt-ignore -->
```html
{{/* djlint:off */}}
   <bad html to ignore>
{{/* djlint:on */}}
```

Handlebars のコメントでも：

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## ルールの無視

無視するブロックの開始タグにルール名を加えると、特定のリンタールールだけを無視することもできます。

<!-- oxfmt-ignore -->
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

{{/* djlint:off H025 */}}
<p>
{{/* djlint:on */}}
```
