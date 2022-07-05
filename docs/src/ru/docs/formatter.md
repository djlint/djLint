---
description: Форматируйте свои HTML-шаблоны с помощью djLint. Быстрый и точный вывод сделает ваши шаблоны блестящими.
title: Использование форматера
keywords: облицовка шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, использование, Использование форматера
---

# Использование форматера

Форматировщик djLint возьмет неряшливые html-шаблоны и сделает форматирование последовательным и легким!

Форматировщик - это бета-версия инструмента. Прежде чем вносить изменения, проверьте результат.

Чтобы просмотреть, что может измениться в форматировании, выполните следующие действия:

```bash
djlint . --check
```

Для форматирования кода и обновления файлов выполните:

```bash
djlint . --reformat
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/ru/docs/configuration/">Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!</a></div>
</div>

{% admonition
   "note",
   "Note",
   "Переформатирование не работает с длинными json/html, встроенными в данные атрибутов."
%}

{% admonition
   "note",
   "Note",
   "djLint не является парсером html или синтаксическим валидатором."
%}

## Вот пример!

### До

Вот кусок HTML, который отчаянно нуждается во внимании -
{% raw %}

```
{% load admin_list %}{% load i18n %}<p class="paginator">{% if pagination_required %}{% for i in page_range %}{% paginator_number cl i %}{% endfor %}{% endif %}{{ cl.result_count }}{% if cl.result_count == 1 %}{{ cl.opts.verbose_name }}   {% else %}{{ cl.opts.verbose_name_plural }}       {% endif %}{% if show_all_url %} <a href="{{ show_all_url }}" class="showall">{% translate 'Show all' %}          </a>  {% endif %}{% if cl.formset and cl.result_count %}<input type="submit" name="_save" class="default" value="{% translate 'Save' %}">{% endif %}      </p>
```

{% endraw %}

### После

Теперь он выглядит немного лучше... мы можем его прочитать :)

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
