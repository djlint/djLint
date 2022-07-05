---
description: Format your HTML Templates with djLint. Fast, accurate, output will make your templates shine.
title: Formatter Usage
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, formatter usage
---

# Formatter Usage

djLint's formatter will take sloppy html templates and make the formatting consistent and easy to follow!

Formatting is a beta tool. `--check` the output before applying changes.

To review what may change in formatting run:

```bash
djlint . --check
```

To format the code and update files run:

```bash
djlint . --reformat
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/docs/configuration/">Check out the configuration guide for all the options!</a></div>
</div>

{% admonition
   "note",
   "Note",
   "Reformatting does not work with long json/html embedded into attribute data."
%}

{% admonition
   "note",
   "Note",
   "djLint is not an html parser or syntax validator."
%}

## Here's an example!

### Before

Here's a blob of HTML that's in desperate need of attention -
{% raw %}

```
{% load admin_list %}{% load i18n %}<p class="paginator">{% if pagination_required %}{% for i in page_range %}{% paginator_number cl i %}{% endfor %}{% endif %}{{ cl.result_count }}{% if cl.result_count == 1 %}{{ cl.opts.verbose_name }}   {% else %}{{ cl.opts.verbose_name_plural }}       {% endif %}{% if show_all_url %} <a href="{{ show_all_url }}" class="showall">{% translate 'Show all' %}          </a>  {% endif %}{% if cl.formset and cl.result_count %}<input type="submit" name="_save" class="default" value="{% translate 'Save' %}">{% endif %}      </p>
```

{% endraw %}

### After

It looks a bit better now... we can read it :)

{% raw %}

```html
{% load admin_list %} {% load i18n %}
<p class="paginator">
  {% if pagination_required %} {% for i in page_range %} {% paginator_number cl
  i %} {% endfor %} {% endif %} {{ cl.result_count }} {% if cl.result_count == 1
  %} {{ cl.opts.verbose_name }} {% else %} {{ cl.opts.verbose_name_plural }} {%
  endif %} {% if show_all_url %}
  <a href="{{ show_all_url }}" class="showall"> {% translate 'Show all' %} </a>
  {% endif %} {% if cl.formset and cl.result_count %}
  <input
    type="submit"
    name="_save"
    class="default"
    value="{% translate 'Save' %}"
  />
  {% endif %}
</p>
```

{% endraw %}
