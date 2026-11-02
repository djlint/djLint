---
title: Линтер и форматер шаблонов Django
keywords: django, djlint, линтер шаблонов django, форматер шаблонов django, форматирование шаблонов django
description: djLint проверяет и форматирует шаблоны Django. Задайте профиль django, чтобы правила и форматирование подходили для них.
tool: django
---

# {{ title }}

{{ description }}

**[Что такое Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

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
