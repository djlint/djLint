---
title: "Biçimlendirici Kullanımı"
description: "HTML şablonlarınızı djLint ile biçimlendirin. Hızlı ve doğru; çıktısı şablonlarınızı parlatır."
sidebar:
  label: "Biçimlendirici"
---

djLint'in biçimlendiricisi özensiz yazılmış HTML şablonlarını alır ve biçimlendirmelerini tutarlı ve kolay takip edilir hâle getirir!

Değişiklikleri uygulamadan önce çıktıyı `--check` ile gözden geçirin.

Biçimlendirmede nelerin değişebileceğini görmek için şunu çalıştırın:

```bash
djlint . --check
```

Kodu biçimlendirip dosyaları güncellemek için şunu çalıştırın:

```bash
djlint . --reformat --single-attribute-per-line

# betikleri ve stilleri de biçimlendirmeye ne dersiniz?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
[Tüm seçenekler için yapılandırma kılavuzuna göz atın!](/tr/docs/configuration/)
:::

:::note[Not]
Bir özniteliğin içine yazılmış JSON ve JavaScript, `--format-attribute-js-json` açık olmadıkça olduğu gibi bırakılır. Bir özniteliğin içindeki HTML'e ise hiçbir zaman dokunulmaz.
:::

:::note[Not]
djLint bir HTML ayrıştırıcısı ya da sözdizimi doğrulayıcısı değildir.
:::

## İşte bir örnek!

### Önce

Acilen ilgi bekleyen bir yığın HTML -

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

Şimdi biraz daha iyi görünüyor... artık okuyabiliyoruz :)

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
