---
title: "En İyi Uygulamalar"
description: "HTML şablonlarını djLint ile biçimlendirirken en iyi uygulamalar."
sidebar:
  label: "En iyi uygulamalar"
---

## Koşullu özniteliklerin çevresindeki boşluklar

Bazen bir etikete sınıf eklemek için koşullar kullanılır. djLint, koşul ifadelerinin içindeki boşlukları kaldırır.

Önerilen kalıp:

```html
<div class="class1 {% if condition -%}class2{%- endif %}">content</div>
                  ^ space here
```

Önerilmeyen kalıp:

```html
<div class="class1{% if condition -%} class2{%- endif %}">content</div>
                                     ^ space here
```

## `format_attribute_template_tags` ve boşluksuz koşullu öznitelikler

`format_attribute_template_tags` seçeneği etkinse koşullu öznitelikler, etiketin içindeki boşlukları kaldırmak için boşluksuz etiketler kullanmalıdır; örneğin nunjucks ve jinja'da `{% if a -%}`.

djLint uzun öznitelikleri birden çok satıra böler ve özniteliklerin içinde korunan boşluklar kodunuzu bozabilir.

Önerilen kalıp:

```html
<input
  value="{% if database -%}{{ database.name }}{%- else -%}blah{%- endif %}"
/>
                        ^                       ^      ^        ^
```

İşaretlenen her konum boşluksuz bir etikettir.

Önerilmeyen kalıp:

```html
<input value="{% if database %}{{ database.name }}{% else %}blah{% endif %}" />
```

Biçimlendirmeden sonra şöyle görünebilir:

```html
<input
  value="{% if database %}
                  {{ database.name }}
              {% else %}
                  blah
              {% endif %}"
/>
```
