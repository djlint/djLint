---
title: Linter und Formatter für Askama-Templates
keywords: askama, rust, djlint, Linter für Askama-Templates, Formatter für Askama-Templates, Askama-Templates formatieren
description: djLint ist ein Linter und ein Formatter für Askama-Templates! Nutzen Sie das vorgefertigte Profil, wenn Sie Ihre Templates mit djLint linten und formatieren.
tool: askama
---

# {{ title }}

{{ description }}

**[Was ist Askama?](https://askama.readthedocs.io/)**

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
