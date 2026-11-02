---
title: "Linter et formateur de templates Liquid"
description: "djLint est un linter de templates Liquid et un formateur de templates Liquid ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint."
sidebar:
  label: "Liquid"
---

djLint est un linter de templates Liquid et un formateur de templates Liquid ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint.

**[Qu'est-ce que Liquid ?](https://shopify.github.io/liquid/)**

Un seul profil couvre tous les dialectes de Liquid : thèmes Shopify, Jekyll, LiquidJS (Eleventy) et Fluid (Orchard Core).

#### En ligne de commande

```bash
djlint /path/to/templates --profile=liquid
```

#### Ou avec un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile = "liquid"
```

```toml title="djlint.toml / .djlint.toml"
profile = "liquid"
```

```json title=".djlintrc"
{ "profile": "liquid" }
```

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::
