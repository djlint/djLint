---
title: Twig Template Linter and Formatter
keywords: twig, djlint, twig template linter, twig template formatter, format twig templates
description: djLint - это линтер шаблонов twig и форматировщик шаблонов twig! Используйте преимущества профиля предварительной сборки при линтинге и форматировании ваших шаблонов с помощью djLint.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Что такое Twig?](https://twig.symfony.com/)**

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
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/ru/docs/configuration/">Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!</a></div>
</div>
