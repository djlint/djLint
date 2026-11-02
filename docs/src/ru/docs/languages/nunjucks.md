---
title: Линтер и форматер шаблонов Nunjucks
keywords: nunjucks, djlint, линтер шаблонов nunjucks, форматер шаблонов nunjucks, форматирование шаблонов nunjucks, pebble, линтер шаблонов pebble
description: djLint — линтер и форматер шаблонов Nunjucks! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Что такое Nunjucks?](https://mozilla.github.io/nunjucks/)**

Шаблоны Pebble (Java) совместимы с Twig, поэтому используйте для них этот же профиль.

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
