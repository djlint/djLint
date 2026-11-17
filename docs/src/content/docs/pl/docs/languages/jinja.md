---
title: "Linter i formater szablonów Jinja"
description: "djLint lintuje i formatuje szablony Jinja. Ustaw profil jinja, aby reguły i formatowanie były do nich dopasowane."
sidebar:
  label: "Jinja"
---

djLint lintuje i formatuje szablony Jinja. Ustaw profil `jinja`, aby reguły i formatowanie były do nich dopasowane.

**[Czym jest Jinja?](https://jinja.palletsprojects.com/en/stable/templates/)**

Szablony MiniJinja są w pełni zgodne z Jinja2, więc używaj tego samego profilu `jinja`.

Szablony Jinjava od HubSpot również są w stylu jinja, więc używaj tego profilu także dla nich.

## Z wiersza poleceń

```bash
djlint /path/to/templates --profile=jinja
```

## Lub w pliku konfiguracyjnym

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

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::
