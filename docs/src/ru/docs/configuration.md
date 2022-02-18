---
description: Конфигурация djLint для линтинга и форматирования HTML-шаблонов. Воспользуйтесь многочисленными возможностями форматирования.
title: Конфигурация
keywords: облицовка шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, использование, configuration
---

# {{ "configuration" | i18n }}

Конфигурация выполняется через файл `pyproject.toml` вашего проекта. Арги командной строки всегда будут переопределять любые настройки в `pyproject.toml`.

```ini
[tool.djlint]
<config options>
```

## ignore

Игнорируйте коды линтера.

Использование:

```ini
ignore="H014,H015"
```

## extension

Используется для поиска файлов только с определенным расширением.

Использование:

```ini
extension="html.dj"
```

## custom_blocks

Используется для отступов в пользовательских блоках кода. Например, {% raw %}`{% toc %}...{% endtoc %}`{% endraw %}

Использование:

```ini
custom_blocks="toc,example"
```

## custom_html

Используется для отступа пользовательских HTML-тегов. Например, `<mjml>` или `<simple-greeting>` или `<mj-\w+>`.

Использование:

```ini
custom_html="mjml,simple-greeting,mj-\\w+"
```

## indent

Используется для изменения отступа кода. По умолчанию - 4 (четыре пробела).

Использование:

```ini
indent=3
```

## exclude

Переопределите пути исключения по умолчанию.

Использование:

```ini
exclude=".venv,venv,.tox,.eggs,..."
```

## extend_exclude

Добавьте дополнительные пути к исключаемым по умолчанию.

Использование:

```ini
extend_exclude=".custom"
```

## blank_line_after_tag

Добавьте дополнительную пустую строку после групп тегов {% raw %}`{% <tag> ... %}`{% endraw %}.

Использование:

```ini
blank_line_after_tag="load,extends,include"
```

## profile

Установите профиль для языка шаблона. Профиль будет включать правила линтера, применимые к языку шаблонов, а также может изменять переформатирование. Например, в `handlebars` нет пробелов внутри тегов {% raw %}`{{#if}}`{% endraw %}.
Параметры:

:::content

- html (по умолчанию)
- django
- jinja
- nunjucks (для nunjucks и twig)
- handlebars (для handlebars и mustache)
- golang
- angular
  :::

Использование:

```ini
profile="django"
```

## require_pragma

Форматировать или линтовать только те файлы, которые начинаются с комментария, содержащего только текст 'djlint:on'. Комментарий может быть HTML-комментарием или комментарием на языке шаблонов, определенном настройкой профиля. Если профиль не указан, принимается комментарий на любом из языков шаблонов.

Использование:

```ini
require_pragma=true
```

{% raw %}

```html
<!-- djlint:on -->
или {# djlint:on #} или {% comment %} djlint:on {% endcomment %} или {{ /*
djlint:on */ }} или {{!-- djlint:on --}}
```

{% endraw %}

## max_line_length

Форматировщик попытается разместить некоторые html и шаблонные теги на одной строке вместо того, чтобы обернуть их, если длина строки не превышает этого значения.

Использование:

```ini
max_line_length=120
```

## max_attribute_length

Форматировщик попытается обернуть атрибуты тега, если длина атрибута превышает это значение.

Использование:

```ini
max_attribute_length=10
```

## use_gitignore

Добавьте исключения .gitignore к исключениям по умолчанию.

Использование:

```ini
use_gitignore=True
```

## format_attribute_template_tags

Форматировщик будет пытаться форматировать синтаксис шаблона внутри атрибутов тега. По умолчанию отключен.

Использование:

```ini
format_attribute_template_tags=true
```

Например, если эта опция включена, то допустимым будет следующий html:

```html
<input
  class="{% if this %}
                  then something neat
              {% else %}
                  that is long stuff asdf and more even
              {% endif %}"
/>
```

## linter_output_format

Настройка порядка вывода сообщения. По умолчанию="{code} {line} {message} {match}". Если `{filename}` не включено в сообщение, то вывод будет сгруппирован по файлам и к каждой группе будет автоматически добавлен заголовок.

Использование:

```ini
# необязательные переменные:
#   {filename}
#   {line}
#   {code}
#   {message}
#   {match}

linter_output_format="{filename}:{line}: {code} {message} {match}"
```
