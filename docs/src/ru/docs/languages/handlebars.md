---
title: Handlebars Template Linter and Formatter
keywords: handlebars, djlint, handlebars template linter, handlebars template formatter, format handlebars templates
description: djLint - это линтер шаблонов handlebars и форматер шаблонов handlebars! Используйте преимущества готового профиля при линтинге и форматировании ваших шаблонов с помощью djLint.
tool: handlebars
---

# {{ title }}

{{ description }}

**[Что такое Handlebars?](https://handlebarsjs.com/)**

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
