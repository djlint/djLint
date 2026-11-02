---
title: Линтер шаблонов Angular
keywords: angular, djlint, линтер шаблонов angular, проверка шаблонов angular
description: djLint проверяет шаблоны Angular. Задайте профиль angular, чтобы правила подходили для них.
tool: angular
---

# {{ title }}

{{ description }}

**[Что такое Angular?](https://angular.io/guide/template-syntax)**

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
