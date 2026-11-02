---
title: "Линтер и форматер шаблонов Askama"
description: "djLint — линтер и форматер шаблонов Askama! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint."
sidebar:
  label: "Askama"
---

djLint — линтер и форматер шаблонов Askama! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint.

**[Что такое Askama?](https://askama.readthedocs.io/)**

#### Через командную строку

```bash
djlint /path/to/templates --profile=askama
```

#### Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile = "askama"
```

```toml title="djlint.toml / .djlint.toml"
profile = "askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::
