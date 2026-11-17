---
title: "Linter et formateur de templates Jinja"
description: "djLint linte et formate les templates Jinja. Utilisez le profil jinja pour adapter les règles et le formatage à ces templates."
sidebar:
  label: "Jinja"
---

djLint linte et formate les templates Jinja. Utilisez le profil `jinja` pour adapter les règles et le formatage à ces templates.

**[Qu'est-ce que Jinja ?](https://jinja.palletsprojects.com/en/stable/templates/)**

MiniJinja suit la syntaxe de Jinja2, et les templates Jinjava de HubSpot suivent eux aussi le style Jinja : utilisez le profil `jinja` pour les deux.

## En ligne de commande

```bash
djlint /path/to/templates --profile=jinja
```

## Dans un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

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
