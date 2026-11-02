---
title: Линтер и форматер шаблонов Go
keywords: шаблоны go, golang, djlint, линтер шаблонов go, форматер шаблонов go, линтер шаблонов golang, форматер шаблонов golang, форматирование шаблонов go, линтер шаблонов hugo, линтер шаблонов helm
description: djLint проверяет и форматирует шаблоны Go. Задайте профиль golang, чтобы правила и форматирование подходили для них.
tool: golang
---

# {{ title }}

{{ description }}

**[Что такое шаблоны Go?](https://pkg.go.dev/text/template)**

На шаблонах Go (`text/template`, `html/template`) построены также темы Hugo и чарты Helm, поэтому используйте для них этот же профиль.

## Через командную строку

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Или через файл конфигурации

Настройте djLint в файле `pyproject.toml`, `djlint.toml` / `.djlint.toml` или `.djlintrc` вашего проекта.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Обо всех параметрах читайте в руководстве по конфигурации!</a></div>
</div>
