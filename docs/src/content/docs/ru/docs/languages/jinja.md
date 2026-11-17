---
title: "Линтер и форматер шаблонов Jinja"
description: "djLint проверяет и форматирует шаблоны Jinja. Задайте профиль jinja, чтобы правила и форматирование подходили для них."
sidebar:
  label: "Jinja"
---

djLint проверяет и форматирует шаблоны Jinja. Задайте профиль `jinja`, чтобы правила и форматирование подходили для них.

**[Что такое Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja следует синтаксису Jinja2, а шаблоны Jinjava от HubSpot тоже написаны в стиле Jinja, поэтому для обоих используйте профиль `jinja`. J004 и J018 предлагают `url_for` из Flask, поэтому в проекте без Flask отключите их.

## Через командную строку

```bash
djlint /path/to/templates --profile=jinja
```

## В файле конфигурации

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
