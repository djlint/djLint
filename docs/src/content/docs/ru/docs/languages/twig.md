---
title: "Линтер и форматер шаблонов Twig"
description: "djLint проверяет и форматирует шаблоны Twig. Задайте профиль nunjucks, чтобы правила и форматирование подходили для них."
sidebar:
  label: "Twig"
---

djLint проверяет и форматирует шаблоны Twig. Задайте профиль `nunjucks`, чтобы правила и форматирование подходили для них.

**[Что такое Twig?](https://twig.symfony.com/)**

Шаблоны Pebble (Java) совместимы с Twig, поэтому используйте для них этот же профиль.

## Через командную строку

```bash
djlint /path/to/templates --profile=nunjucks
```

## Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile = "nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile = "nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::
