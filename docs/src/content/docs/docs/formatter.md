---
title: "Formatter Usage"
description: "Format your HTML Templates with djLint. Fast, accurate, output will make your templates shine."
sidebar:
  label: "Formatter"
---

djLint's formatter will take sloppy html templates and make the formatting consistent and easy to follow!

Review the output with `--check` before applying changes.

To review what may change in formatting run:

```bash
djlint . --check
```

To format the code and update files run:

```bash
djlint . --reformat --single-attribute-per-line

# how about formatting scripts and styles?
djlint . --reformat --single-attribute-per-line --format-css --format-js
```

:::tip
[Check out the configuration guide for all the options!](/docs/configuration/)
:::

:::note[Note]
JSON and JavaScript written into an attribute are left as they are unless `--format-attribute-js-json` is on. HTML inside an attribute is always left alone.
:::

:::note[Note]
djLint is not an html parser or syntax validator.
:::

## Here's an example!

### Before

Here's a blob of HTML that's in desperate need of attention -

<!-- prettier-ignore -->
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

### After

It looks a bit better now... we can read it :)

<!-- prettier-ignore -->
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

### After with `single_attribute_per_line`

Prefer Prettier-style attributes? Enable the `single_attribute_per_line` option:

<!-- prettier-ignore -->
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
