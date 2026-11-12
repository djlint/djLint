---
title: "Linter und Formatter für Django-Templates"
description: "djLint lintet und formatiert Django-Templates. Setzen Sie das Profil django, damit Regeln und Formatierung zu ihnen passen."
sidebar:
  label: "Django"
---

djLint lintet und formatiert Django-Templates. Setzen Sie das Profil `django`, damit Regeln und Formatierung zu ihnen passen.

**[Was ist Django?](https://django.readthedocs.io/en/stable/ref/templates/language.html)**

## Über die Befehlszeile

```bash
djlint /path/to/templates --profile=django
```

## Oder über eine Konfigurationsdatei

Konfigurieren Sie djLint in der Datei `pyproject.toml`, `djlint.toml` / `.djlint.toml` oder `.djlintrc` Ihres Projekts.

```toml title="pyproject.toml"
[tool.djlint]
profile = "django"
```

```toml title="djlint.toml / .djlint.toml"
profile = "django"
```

```json title=".djlintrc"
{ "profile": "django" }
```

:::tip
[Alle Optionen finden Sie in der Anleitung zur Konfiguration!](/de/docs/configuration/)
:::
