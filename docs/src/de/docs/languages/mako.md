---
title: Linter und Formatter für Mako-Templates
keywords: mako, python, pyramid, open edx, djlint, Linter für Mako-Templates, Formatter für Mako-Templates, Mako-Templates formatieren
description: djLint lintet und formatiert Mako-Templates. Setzen Sie das Profil mako, damit Regeln und Formatierung zu ihnen passen.
tool: mako
---

# {{ title }}

{{ description }}

**[Was ist Mako?](https://www.makotemplates.org/)**

Mit dem Profil mako steht eine Steuerzeile wie `% if x:` und ein `##`-Kommentar immer in einer eigenen Zeile, und ein Tag, dessen Attribute von Steuerzeilen abhängen, behält sie so, wie sie geschrieben sind. Python-Blöcke und der Inhalt von `<%doc>` und `<%text>` bleiben unverändert, ebenso ein script oder style mit Mako-Syntax bei `--format-js` oder `--format-css`. Steuerzeilen rücken ihren Inhalt noch nicht ein.

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
