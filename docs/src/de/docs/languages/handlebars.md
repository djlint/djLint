---
title: Linter und Formatter für Handlebars-Templates
keywords: handlebars, djlint, Linter für Handlebars-Templates, Formatter für Handlebars-Templates, Handlebars-Templates formatieren
description: djLint lintet und formatiert Handlebars-Templates. Setzen Sie das Profil handlebars, damit Regeln und Formatierung zu ihnen passen.
tool: handlebars
---

# {{ title }}

{{ description }}

**[Was ist Handlebars?](https://handlebarsjs.com/)**

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
