---
title: "Linter et formateur de templates Nunjucks"
description: "djLint linte et formate les templates Nunjucks. Utilisez le profil nunjucks pour adapter les règles et le formatage à ces templates."
sidebar:
  label: "Nunjucks"
---

djLint linte et formate les templates Nunjucks. Utilisez le profil `nunjucks` pour adapter les règles et le formatage à ces templates.

**[Qu'est-ce que Nunjucks ?](https://mozilla.github.io/nunjucks/)**

## En ligne de commande

```bash
djlint /path/to/templates --profile=nunjucks
```

## Dans un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile = "nunjucks"
```

```toml title="djlint.toml / .djlint.toml"
profile = "nunjucks"
```

```json title=".djlintrc"
{ "profile": "nunjucks" }
```
