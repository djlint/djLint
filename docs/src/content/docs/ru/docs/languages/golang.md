---
title: "Линтер и форматер шаблонов Go"
description: "djLint — линтер и форматер шаблонов Go! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint."
sidebar:
  label: "Шаблоны Go"
---

djLint — линтер и форматер шаблонов Go! Используйте готовый профиль для проверки и форматирования ваших шаблонов с помощью djLint.

**[Что такое шаблоны Go?](https://pkg.go.dev/text/template)**

На шаблонах Go (`text/template`, `html/template`) построены также темы Hugo и чарты Helm, поэтому используйте для них этот же профиль.

#### Через командную строку

```bash
djlint /path/to/templates --profile=golang
```

#### Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

```toml title="pyproject.toml"
[tool.djlint]
profile="golang"
```

```toml title="djlint.toml / .djlint.toml"
profile="golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[Обо всех параметрах читайте в руководстве по конфигурации!](/ru/docs/configuration/)
:::
