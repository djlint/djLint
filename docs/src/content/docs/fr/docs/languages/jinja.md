---
title: "Linter et formateur de templates Jinja"
description: "djLint linte et formate les templates Jinja. Utilisez le profil jinja pour adapter les règles et le formatage à ces templates."
sidebar:
  label: "Jinja"
---

djLint linte et formate les templates Jinja. Utilisez le profil `jinja` pour adapter les règles et le formatage à ces templates.

**[Qu'est-ce que Jinja ?](https://jinja.palletsprojects.com/en/stable/templates/)**

Les templates MiniJinja sont entièrement compatibles avec Jinja2 : utilisez ce même profil `jinja`.

Les templates Jinjava de HubSpot suivent eux aussi le style jinja : utilisez également ce profil pour eux.

## En ligne de commande

```bash
djlint /path/to/templates --profile=jinja
```

## Ou avec un fichier de configuration

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

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::
