---
title: "Линтер и форматер шаблонов Askama"
description: "djLint проверяет и форматирует шаблоны Askama. Задайте профиль askama, чтобы правила и форматирование подходили для них."
sidebar:
  label: "Askama"
---

djLint проверяет и форматирует шаблоны Askama. Задайте профиль `askama`, чтобы правила и форматирование подходили для них.

**[Что такое Askama?](https://askama.readthedocs.io/)**

## Через командную строку

```bash
djlint /path/to/templates --profile=askama
```

## Или через файл конфигурации

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
