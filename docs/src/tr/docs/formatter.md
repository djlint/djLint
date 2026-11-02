---
description: djLint'in HTML şablonlarını nasıl biçimlendirdiği ve değişiklikleri uygulamadan önce nasıl gözden geçireceğiniz.
title: Biçimlendirici Kullanımı
keywords: şablon linter'ı, şablon biçimlendiricisi, djLint, HTML, şablonlar, biçimlendirici, linter, biçimlendirici kullanımı
---

# Biçimlendirici Kullanımı

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

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Tüm seçenekler için yapılandırma kılavuzuna göz atın!</a></div>
</div>

{% admonition
   "note",
   "Not",
   "Bir özniteliğin içine yazılmış JSON ve JavaScript, `--format-attribute-js-json` açık olmadıkça olduğu gibi bırakılır. Bir özniteliğin içindeki HTML'e ise hiçbir zaman dokunulmaz."
%}

{% admonition
   "note",
   "Not",
   "djLint bir HTML ayrıştırıcısı ya da sözdizimi doğrulayıcısı değildir."
%}

## İşte bir örnek!

### Önce

Acilen ilgi bekleyen bir yığın HTML -

{% raw %}

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

{% endraw %}

### Sonra

Şimdi biraz daha iyi görünüyor... artık okuyabiliyoruz :)

{% raw %}

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

{% endraw %}

### `single_attribute_per_line` ile sonra

Prettier tarzı öznitelikleri mi tercih ediyorsunuz? `single_attribute_per_line` seçeneğini etkinleştirin:

{% raw %}

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

{% endraw %}
