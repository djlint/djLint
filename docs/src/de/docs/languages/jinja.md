---
title: Linter und Formatter für Jinja-Templates
keywords: jinja, djlint, Linter für Jinja-Templates, Formatter für Jinja-Templates, Jinja-Templates formatieren, minijinja, jinjava, Linter für MiniJinja-Templates, Linter für Jinjava-Templates
description: djLint ist ein Linter und ein Formatter für Jinja-Templates! Nutzen Sie das vorgefertigte Profil, wenn Sie Ihre Templates mit djLint linten und formatieren.
tool: jinja
---

# {{ title }}

{{ description }}

**[Was ist Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja-Templates sind vollständig Jinja2-kompatibel. Verwenden Sie daher ebenfalls das Profil `jinja`.

Auch die Jinjava-Templates von HubSpot folgen dem Jinja-Stil. Verwenden Sie dieses Profil also auch für sie.

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
