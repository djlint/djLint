---
title: Linter und Formatter für Go-Templates
keywords: go templates, golang, djlint, Linter für Go-Templates, Formatter für Go-Templates, Linter für Golang-Templates, Formatter für Golang-Templates, Go-Templates formatieren, Linter für Hugo-Templates, Linter für Helm-Templates
description: djLint lintet und formatiert Go-Templates. Setzen Sie das Profil golang, damit Regeln und Formatierung zu ihnen passen.
tool: golang
---

# {{ title }}

{{ description }}

**[Was sind Go-Templates?](https://pkg.go.dev/text/template)**

Auf Go-Templates (`text/template`, `html/template`) bauen auch Hugo-Themes und Helm-Charts auf. Verwenden Sie für diese daher dasselbe Profil.

## Über die Befehlszeile

```bash
djlint /path/to/templates --profile={{ tool }}
```

## Oder über eine Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Alle Optionen finden Sie in der Anleitung zur Konfiguration!</a></div>
</div>
