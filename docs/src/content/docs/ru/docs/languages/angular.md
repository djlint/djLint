---
title: "Линтер шаблонов Angular"
description: "djLint проверяет шаблоны Angular. Задайте профиль angular, чтобы правила подходили для них."
sidebar:
  label: "Angular"
---

djLint проверяет шаблоны Angular. Задайте профиль `angular`, чтобы правила подходили для них.

**[Что такое Angular?](https://angular.io/guide/template-syntax)**

## Через командную строку

```bash
djlint /path/to/templates --profile=angular
```

## Или через файл конфигурации

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
