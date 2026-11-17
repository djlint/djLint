---
title: "Biçimlendirici kullanımı"
description: "djLint'in HTML şablonlarını nasıl biçimlendirdiği ve değişiklikleri uygulamadan önce nasıl gözden geçireceğiniz."
sidebar:
  label: "Biçimlendirici"
---

djLint'in biçimlendiricisi HTML şablonlarının düzenini tutarlı hâle getirir. Önce neyi değiştireceğine bakın:

```bash
djlint . --check --format-css --format-js
```

Sonra dosyaları yerinde biçimlendirin, burada `<style>` ve `<script>` içerikleriyle birlikte:

```bash
djlint . --reformat --format-css --format-js
```

:::note[Not]
Bir özniteliğin içine yazılmış JSON ve JavaScript, `--format-attribute-js-json` açık olmadıkça olduğu gibi bırakılır. Bir özniteliğin içindeki HTML'e ise hiçbir zaman dokunulmaz.
:::

:::note[Not]
djLint bir HTML ayrıştırıcısı ya da sözdizimi doğrulayıcısı değildir.
:::

## Örnek

### Önce

<!-- oxfmt-ignore -->
```html
{% load admin_list %}
{% load i18n %}
<p class="paginator">
{% if pagination_required %}
{% for i in page_range %}
{% paginator_number cl i %}
{% endfor %}
{% endif %}
{{ cl.result_count }}
{% if cl.result_count == 1 %}
{{ cl.opts.verbose_name }}
{% else %}
{{ cl.opts.verbose_name_plural }}
{% endif %}
{% if show_all_url %}
<a href="{{ show_all_url }}" class="showall">{% translate 'Show all' %}</a>
{% endif %}
{% if cl.formset and cl.result_count %}
<input type="submit" name="_save" class="default" value="{% translate 'Save' %}">
{% endif %}
</p>
```

### Sonra

<!-- oxfmt-ignore -->
```html
{% load admin_list %}
{% load i18n %}
<p class="paginator">
    {% if pagination_required %}
        {% for i in page_range %}
            {% paginator_number cl i %}
        {% endfor %}
    {% endif %}
    {{ cl.result_count }}
    {% if cl.result_count == 1 %}
        {{ cl.opts.verbose_name }}
    {% else %}
        {{ cl.opts.verbose_name_plural }}
    {% endif %}
    {% if show_all_url %}
        <a href="{{ show_all_url }}" class="showall">{% translate "Show all" %}</a>
    {% endif %}
    {% if cl.formset and cl.result_count %}
        <input type="submit"
               name="_save"
               class="default"
               value="{% translate 'Save' %}">
    {% endif %}
</p>
```

### `single_attribute_per_line` ile sonra

Prettier tarzı öznitelikleri mi tercih ediyorsunuz? `single_attribute_per_line` seçeneğini etkinleştirin:

<!-- oxfmt-ignore -->
```html
{% load admin_list %}
{% load i18n %}
<p class="paginator">
    {% if pagination_required %}
        {% for i in page_range %}
            {% paginator_number cl i %}
        {% endfor %}
    {% endif %}
    {{ cl.result_count }}
    {% if cl.result_count == 1 %}
        {{ cl.opts.verbose_name }}
    {% else %}
        {{ cl.opts.verbose_name_plural }}
    {% endif %}
    {% if show_all_url %}
        <a href="{{ show_all_url }}" class="showall">{% translate "Show all" %}</a>
    {% endif %}
    {% if cl.formset and cl.result_count %}
        <input
            type="submit"
            name="_save"
            class="default"
            value="{% translate 'Save' %}"
        >
    {% endif %}
</p>
```
