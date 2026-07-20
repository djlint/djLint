---
title: Liquid Template Linter and Formatter
keywords: liquid, shopify, jekyll, eleventy, djlint, liquid template linter, liquid template formatter, format liquid templates, shopify, jekyll, eleventy, liquidjs, fluid, shopify theme linter, jekyll linter
description: djLint - это линтер шаблонов Liquid и форматер шаблонов Liquid! Используйте преимущества профиля предварительной сборки при линтинге и форматировании ваших шаблонов с помощью djLint.
tool: liquid
---

# {{ title }}

{{ description }}

**[Что такое Liquid?](https://shopify.github.io/liquid/)**

Один профиль покрывает все диалекты Liquid: темы Shopify, Jekyll, LiquidJS (Eleventy) и Fluid (Orchard Core).

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
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!</a></div>
</div>
