---
title: "Линтер и форматер шаблонов Tera"
description: "djLint — линтер и форматер шаблонов Tera! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint."
sidebar:
  label: "Tera"
---

djLint — линтер и форматер шаблонов Tera! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint.

**[Что такое Tera?](https://keats.github.io/tera/)**

#### Через командную строку

```bash
djlint /path/to/templates --profile=tera
```

#### Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile = "tera"
```

```toml title="djlint.toml / .djlint.toml"
profile = "tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::
