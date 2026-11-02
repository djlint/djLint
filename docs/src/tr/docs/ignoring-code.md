---
description: djLint'in bir kod bloğunu biçimlendirmesini engelleme. djLint kurallarını satır içinde yok sayma.
title: Kodu Yok Sayma
keywords: şablon linter'ı, şablon biçimlendiricisi, djLint, HTML, şablonlar, biçimlendirici, linter, biçimlendirici kullanımı, kodu yok sayma, kuralları yok sayma
date: Last Modified
---

# Kodu Yok Sayma

Kod, `djlint` etiketleri arasına alınarak yok sayılabilir:

{% raw %}

Düz HTML için -

<!-- oxfmt-ignore -->

```html
<!-- djlint:off -->
<bad html to ignore> <!-- djlint:on --></bad>
```

ya da bir yorum olarak -

<!-- oxfmt-ignore -->

```html
{# djlint:off #} <bad html to ignore> {# djlint:on #}</bad>
```

ya da uzun bir yorum olarak -

<!-- oxfmt-ignore -->

```html
{% comment %} djlint:off {% endcomment %}
<bad html to ignore> {% comment %} djlint:on {% endcomment %}</bad>
```

ya da golang tarzı bir yorum olarak -

<!-- oxfmt-ignore -->

```html
{{ /* djlint:off */ }} <bad html to ignore> {{ /* djlint:on */ }}</bad>
```

ya da handlebars tarzı bir yorum olarak -

<!-- oxfmt-ignore -->

```html
{{!-- djlint:off --}} <bad html to ignore> {{!-- djlint:on --}}</bad>
```

{% endraw %}

## Kuralları yok sayma

Belirli linter kuralları da kural adı, yok sayılan bloğun açılış etiketine eklenerek yok sayılabilir.

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
