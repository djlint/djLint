---
title: "Linter i formater szablonów Jinja"
description: "djLint lintuje i formatuje szablony Jinja. Ustaw profil jinja, aby reguły i formatowanie były do nich dopasowane."
sidebar:
  label: "Jinja"
---

djLint lintuje i formatuje szablony Jinja. Ustaw profil `jinja`, aby reguły i formatowanie były do nich dopasowane.

**[Czym jest Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja stosuje składnię Jinja2, a szablony Jinjava od HubSpot też są w stylu Jinja, więc dla obu używaj profilu `jinja`.

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile=jinja
```

## W pliku konfiguracyjnym

Skonfiguruj djLint w pliku `pyproject.toml`, `djlint.toml` / `.djlint.toml` lub `.djlintrc` swojego projektu.

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
