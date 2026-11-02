---
title: "Linter et formateur de templates Mustache"
description: "djLint linte et formate les templates Mustache. Utilisez le profil handlebars pour adapter les règles et le formatage à ces templates."
sidebar:
  label: "Mustache"
---

djLint linte et formate les templates Mustache. Utilisez le profil `handlebars` pour adapter les règles et le formatage à ces templates.

**[Qu'est-ce que Mustache ?](https://mustache.github.io/mustache.5.html)**

## En ligne de commande

```bash
djlint /path/to/templates --profile=handlebars
```

## Ou avec un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile = "handlebars"
```

```toml title="djlint.toml / .djlint.toml"
profile = "handlebars"
```

```json title=".djlintrc"
{ "profile": "handlebars" }
```

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::
