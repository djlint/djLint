---
title: "Линтер шаблонов Angular"
description: "djLint — линтер шаблонов Angular! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint."
sidebar:
  label: "Angular"
---

djLint — линтер шаблонов Angular! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint.

**[Что такое Angular?](https://angular.io/guide/template-syntax)**

#### Через командную строку

```bash
djlint /path/to/templates --profile=angular
```

#### Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile = "angular"
```

```toml title="djlint.toml / .djlint.toml"
profile = "angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::
