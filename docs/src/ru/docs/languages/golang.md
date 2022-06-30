---
title: GoLang Template Linter and Formatter
keywords: GoLang, djlint, GoLang template linter, GoLang template formatter, format GoLang templates
description: djLint - это линтер шаблонов GoLang и форматер шаблонов GoLang! Используйте преимущества профиля предварительной сборки при линтинге и форматировании ваших шаблонов с помощью djLint.
tool: golang
---

# {{ title }}

{{ description }}

**[Что такое GoLang?](https://pkg.go.dev/text/template)**

#### Использование командной строки

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Или используйте файл конфигурации

Настройте djLint в вашем проекте `pyproject.toml`.

```toml
[tool.djlint]
profile="{{ tool }}"
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/ru/docs/configuration/">Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!</a></div>
</div>
