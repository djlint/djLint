---
title: Линтер и форматер шаблонов Mako
keywords: mako, python, pyramid, open edx, djlint, линтер шаблонов mako, форматер шаблонов mako, форматирование шаблонов mako
description: djLint проверяет и форматирует шаблоны Mako. Задайте профиль mako, чтобы правила и форматирование подходили для них.
tool: mako
---

# {{ title }}

{{ description }}

**[Что такое Mako?](https://www.makotemplates.org/)**

С профилем mako управляющая строка вроде `% if x:` и комментарий `##` всегда остаются на отдельной строке, а тег, атрибуты которого зависят от управляющих строк, сохраняет их как написано. Блоки Python и содержимое `<%doc>` и `<%text>` не меняются, как и script или style с синтаксисом Mako при `--format-js` или `--format-css`. Содержимое управляющих блоков пока не получает отступа.

## Через командную строку

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Обо всех параметрах читайте в руководстве по конфигурации!</a></div>
</div>
