---
title: "Linter et formateur de templates Twig"
description: "djLint est un linter de templates twig et un formateur de templates twig ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint."
sidebar:
  label: "Twig"
---

djLint est un linter de templates twig et un formateur de templates twig ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint.

**[Qu'est-ce que Twig ?](https://twig.symfony.com/)**

Les templates Pebble (Java) sont compatibles avec Twig : utilisez ce même profil pour eux.

#### En ligne de commande

```bash
djlint /path/to/templates --profile=nunjucks
```

#### Ou avec un fichier de configuration

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

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::
