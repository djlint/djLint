---
title: "Linter a formátovač šablon Jinja"
description: "djLint lintuje a formátuje šablony Jinja. Nastavte profil jinja, aby jim pravidla i formátování odpovídaly."
sidebar:
  label: "Jinja"
---

djLint lintuje a formátuje šablony Jinja. Nastavte profil `jinja`, aby jim pravidla i formátování odpovídaly.

**[Co je Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja má syntaxi Jinja2 a šablony Jinjava od HubSpotu jsou také ve stylu Jinja, takže pro obě použijte profil `jinja`. J004 a J018 navrhují `url_for` z Flasku, proto je v projektu bez Flasku ignorujte.

## Z příkazového řádku

```bash
djlint /path/to/templates --profile=jinja
```

## V konfiguračním souboru

Nastavte djLint v souboru `pyproject.toml`, `djlint.toml` / `.djlint.toml` nebo `.djlintrc` svého projektu.

```toml title="pyproject.toml"
[tool.djlint]
profile = "jinja"
```

```toml title="djlint.toml / .djlint.toml"
profile = "jinja"
```

```json title=".djlintrc"
{ "profile": "jinja" }
```
