---
title: Линтер и форматер шаблонов Liquid
keywords: liquid, shopify, jekyll, eleventy, djlint, линтер шаблонов liquid, форматер шаблонов liquid, форматирование шаблонов liquid, shopify, jekyll, eleventy, liquidjs, fluid, линтер тем shopify, линтер jekyll
description: djLint проверяет и форматирует шаблоны Liquid. Задайте профиль liquid, чтобы правила и форматирование подходили для них.
tool: liquid
---

# {{ title }}

{{ description }}

**[Что такое Liquid?](https://shopify.github.io/liquid/)**

Один профиль охватывает все диалекты Liquid: темы Shopify, Jekyll, LiquidJS (Eleventy) и Fluid (Orchard Core).

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
