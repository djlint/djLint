---
title: Go Template Linter and Formatter
keywords: go templates, golang, djlint, go template linter, go template formatter, golang template linter, golang template formatter, format go templates, hugo template linter, helm template linter
description: djLint - это линтер шаблонов Go и форматер шаблонов Go! Используйте преимущества профиля предварительной сборки при линтинге и форматировании ваших шаблонов с помощью djLint.
tool: golang
---

# {{ title }}

{{ description }}

**[Что такое шаблоны Go?](https://pkg.go.dev/text/template)**

На шаблонах Go (`text/template`, `html/template`) также работают темы Hugo и чарты Helm, поэтому используйте для них этот же профиль.

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
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Ознакомьтесь с руководством по настройке, чтобы узнать обо всех возможностях!</a></div>
</div>
