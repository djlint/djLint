---
title: Линтер и форматер шаблонов Jinja
keywords: jinja, djlint, линтер шаблонов jinja, форматер шаблонов jinja, форматирование шаблонов jinja, minijinja, jinjava, линтер шаблонов minijinja, линтер шаблонов jinjava
description: djLint проверяет и форматирует шаблоны Jinja. Задайте профиль jinja, чтобы правила и форматирование подходили для них.
tool: jinja
---

# {{ title }}

{{ description }}

**[Что такое Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Шаблоны MiniJinja полностью совместимы с Jinja2, поэтому используйте тот же профиль `jinja`.

Шаблоны Jinjava от HubSpot тоже написаны в стиле jinja, поэтому используйте этот профиль и для них.

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
