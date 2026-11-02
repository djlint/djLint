---
title: Linter und Formatter für Mustache-Templates
keywords: mustache, djlint, Linter für Mustache-Templates, Formatter für Mustache-Templates, Mustache-Templates formatieren
description: djLint ist ein Linter und ein Formatter für Mustache-Templates! Nutzen Sie das vorgefertigte Profil, wenn Sie Ihre Templates mit djLint linten und formatieren.
tool: handlebars
---

# {{ title }}

{{ description }}

**[Was ist Mustache?](https://mustache.github.io/mustache.5.html)**

#### Über die Befehlszeile

```bash
djlint /path/to/templates --profile={{ tool }}
```

#### Oder über eine Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

{% include 'src/_includes/profile_config.md' %}

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Alle Optionen finden Sie in der Anleitung zur Konfiguration!</a></div>
</div>
