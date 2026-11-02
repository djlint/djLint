---
title: "Линтер и форматер шаблонов Nunjucks"
description: "djLint — линтер и форматер шаблонов Nunjucks! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint."
sidebar:
  label: "Nunjucks"
---

djLint — линтер и форматер шаблонов Nunjucks! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint.

**[Что такое Nunjucks?](https://mozilla.github.io/nunjucks/)**

Шаблоны Pebble (Java) совместимы с Twig, поэтому используйте для них этот же профиль.

#### Через командную строку

```bash
djlint /path/to/templates --profile=nunjucks
```

#### Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile="nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile="nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::
