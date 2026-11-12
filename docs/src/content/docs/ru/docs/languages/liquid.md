---
title: "Линтер и форматер шаблонов Liquid"
description: "djLint проверяет и форматирует шаблоны Liquid. Задайте профиль liquid, чтобы правила и форматирование подходили для них."
sidebar:
  label: "Liquid"
---

djLint проверяет и форматирует шаблоны Liquid. Задайте профиль `liquid`, чтобы правила и форматирование подходили для них.

**[Что такое Liquid?](https://shopify.github.io/liquid/)**

Один профиль охватывает все диалекты Liquid: темы Shopify, Jekyll, LiquidJS (Eleventy) и Fluid (Orchard Core).

## Через командную строку

```bash
djlint /path/to/templates --profile=liquid
```

## Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile = "liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile = "liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::
