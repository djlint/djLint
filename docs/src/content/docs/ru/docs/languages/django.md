---
title: "Линтер и форматер шаблонов Django"
description: "djLint — линтер и форматер шаблонов Django! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint."
sidebar:
  label: "Django"
---

djLint — линтер и форматер шаблонов Django! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint.

**[Что такое Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

#### Через командную строку

```bash
djlint /path/to/templates --profile=django
```

#### Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile="django"
```

```toml title="djlint.toml / .djlint.toml"
profile="django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::
