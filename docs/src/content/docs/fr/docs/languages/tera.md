---
title: "Linter et formateur de templates Tera"
description: "djLint est un linter de templates Tera et un formateur de templates Tera ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint."
sidebar:
  label: "Tera"
---

djLint est un linter de templates Tera et un formateur de templates Tera ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint.

**[Qu'est-ce que Tera ?](https://keats.github.io/tera/)**

#### En ligne de commande

```bash
djlint /path/to/templates --profile=tera
```

#### Ou avec un fichier de configuration

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
