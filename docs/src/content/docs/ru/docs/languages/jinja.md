---
title: "Линтер и форматер шаблонов Jinja"
description: "djLint проверяет и форматирует шаблоны Jinja. Задайте профиль jinja, чтобы правила и форматирование подходили для них."
sidebar:
  label: "Jinja"
---

djLint проверяет и форматирует шаблоны Jinja. Задайте профиль `jinja`, чтобы правила и форматирование подходили для них.

**[Что такое Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Шаблоны MiniJinja полностью совместимы с Jinja2, поэтому используйте тот же профиль `jinja`.

Шаблоны Jinjava от HubSpot тоже написаны в стиле jinja, поэтому используйте этот профиль и для них.

## Через командную строку

```bash
djlint /path/to/templates --profile=jinja
```

## Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile = "jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile = "jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::
