---
description: HTML şablonlarını djLint ile biçimlendirirken en iyi uygulamalar.
title: En İyi Uygulamalar
keywords: şablon linter'ı, şablon biçimlendiricisi, djLint, HTML, şablonlar, biçimlendirici, linter, en iyi uygulamalar
---

# En İyi Uygulamalar

## Koşullu özniteliklerin çevresindeki boşluklar

Bazen bir etikete sınıf eklemek için koşullar kullanılır. djLint, koşul ifadelerinin içindeki boşlukları kaldırır.

Önerilen kalıp:

{% raw %}

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

{% endraw %}

Önerilmeyen kalıp:

{% raw %}

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

{% endraw %}

## `format_attribute_template_tags` ve boşluksuz koşullu öznitelikler

`format_attribute_template_tags` seçeneği etkinse koşullu öznitelikler, etiketin içindeki boşlukları kaldırmak için boşluksuz etiketler kullanmalıdır; örneğin nunjucks ve jinja'da {% raw %}`{% if a -%}`{% endraw %}.

djLint uzun öznitelikleri birden çok satıra böler ve özniteliklerin içinde korunan boşluklar kodunuzu bozabilir.

Önerilen kalıp:

{% raw %}

```html
<input value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}" />
                        ^                       ^      ^        ^
```

{% endraw %}

İşaretlenen her konum boşluksuz bir etikettir.

Önerilmeyen kalıp:

{% raw %}

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

{% endraw %}

Biçimlendirmeden sonra şöyle görünebilir:

{% raw %}

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```

{% endraw %}
