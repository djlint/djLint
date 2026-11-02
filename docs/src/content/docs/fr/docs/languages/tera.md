---
title: "Linter et formateur de templates Tera"
description: "djLint linte et formate les templates Tera. Utilisez le profil tera pour adapter les règles et le formatage à ces templates."
sidebar:
  label: "Tera"
---

djLint linte et formate les templates Tera. Utilisez le profil `tera` pour adapter les règles et le formatage à ces templates.

**[Qu'est-ce que Tera ?](https://keats.github.io/tera/)**

## En ligne de commande

```bash
djlint /path/to/templates --profile=tera
```

## Ou avec un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile = "tera"
```

```toml title="djlint.toml / .djlint.toml"
profile = "tera"
```

```json title=".djlintrc"
{ "profile": "tera" }
```

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::
