---
title: Angular Template Linter
keywords: angular, djlint, angular template linter, lint angular templates
description: djLint - это ангулярный линтер шаблонов! Используйте преимущества профиля предварительной сборки при линтинге и форматировании ваших шаблонов с помощью djLint.
tool: angular
---

# {{ title }}

{{ description }}

**[Что такое Angular?](https://angular.io/guide/template-syntax)**

#### Использование командной строки

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Или используйте файл конфигурации

Настройте djLint в вашем проекте `pyproject.toml`.

```toml
[tool.djlint]
profile="{{ tool }}"
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-arrow-circle-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/ru/docs/configuration/">Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!</a></div>
</div>
