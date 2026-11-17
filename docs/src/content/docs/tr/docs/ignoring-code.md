---
title: "Kodu yok sayma"
description: "djLint'in bir kod bloğunu biçimlendirmesi nasıl engellenir, linter kuralları satır içinde nasıl yok sayılır."
---

`djlint:off` ve `djlint:on` yorumları arasındaki koda biçimlendirici de linter da dokunmaz. Yorumlar HTML yorumu olabilir:

<!-- oxfmt-ignore -->
```html
<!-- djlint:off -->
   <bad html to ignore>
<!-- djlint:on -->
```

Ya da Django ve Jinja yorumları:

<!-- oxfmt-ignore -->
```html
{# djlint:off #}
   <bad html to ignore>
{# djlint:on #}
```

Ya da `{% comment %}` blokları:

<!-- oxfmt-ignore -->
```html
{% comment %} djlint:off {% endcomment %}
   <bad html to ignore>
{% comment %} djlint:on {% endcomment %}
```

Ya da Go şablonu yorumları:

<!-- oxfmt-ignore -->
```html
{{ /* djlint:off */ }}
   <bad html to ignore>
{{ /* djlint:on */ }}
```

Ya da Handlebars yorumları:

<!-- oxfmt-ignore -->
```html
{{!-- djlint:off --}}
   <bad html to ignore>
{{!-- djlint:on --}}
```

## Kuralları yok sayma

Belirli linter kuralları da kural adı, yok sayılan bloğun açılış etiketine eklenerek yok sayılabilir.

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

{{ /* djlint:off H025 */ }}
<p>
{{ /* djlint:on */ }}
```
