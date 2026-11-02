---
title: Линтер и форматер шаблонов Mustache
keywords: mustache, djlint, линтер шаблонов mustache, форматер шаблонов mustache, форматирование шаблонов mustache
description: djLint — линтер и форматер шаблонов Mustache! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint.
tool: handlebars
---

# {{ title }}

{{ description }}

**[Что такое Mustache?](https://mustache.github.io/mustache.5.html)**

#### Через командную строку

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Обо всех параметрах читайте в руководстве по конфигурации!</a></div>
</div>
