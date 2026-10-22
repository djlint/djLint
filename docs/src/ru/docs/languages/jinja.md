---
title: Jinja Template Linter and Formatter
keywords: jinja, djlint, jinja template linter, jinja template formatter, format jinja templates, minijinja, jinjava, minijinja template linter, jinjava template linter
description: djLint - это линтер шаблонов jinja и форматер шаблонов jinja! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint.
tool: jinja
---

# {{ title }}

{{ description }}

**[Что такое Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Шаблоны MiniJinja полностью совместимы с Jinja2, поэтому используйте этот же профиль `jinja`.

Шаблоны Jinjava от HubSpot тоже в стиле jinja, поэтому используйте этот профиль и для них.

#### Использование командной строки

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Или используйте файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!</a></div>
</div>
