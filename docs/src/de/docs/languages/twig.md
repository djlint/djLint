---
title: Linter und Formatter für Twig-Templates
keywords: twig, djlint, Linter für Twig-Templates, Formatter für Twig-Templates, Twig-Templates formatieren, pebble, Linter für Pebble-Templates
description: djLint lintet und formatiert Twig-Templates. Setzen Sie das Profil nunjucks, damit Regeln und Formatierung zu ihnen passen.
tool: nunjucks
---

# {{ title }}

{{ description }}

**[Was ist Twig?](https://twig.symfony.com/)**

Pebble-Templates (Java) sind Twig-kompatibel. Verwenden Sie für sie daher dasselbe Profil.

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
