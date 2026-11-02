---
title: Линтер и форматер шаблонов Tera
keywords: tera, rust, zola, djlint, линтер шаблонов tera, форматер шаблонов tera, форматирование шаблонов tera
description: djLint — линтер и форматер шаблонов Tera! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint.
tool: tera
---

# {{ title }}

{{ description }}

**[Что такое Tera?](https://keats.github.io/tera/)**

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
