---
title: Linter und Formatter für Tera-Templates
keywords: tera, rust, zola, djlint, Linter für Tera-Templates, Formatter für Tera-Templates, Tera-Templates formatieren
description: djLint lintet und formatiert Tera-Templates. Setzen Sie das Profil tera, damit Regeln und Formatierung zu ihnen passen.
tool: tera
---

# {{ title }}

{{ description }}

**[Was ist Tera?](https://keats.github.io/tera/)**

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
