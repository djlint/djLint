---
title: "Linter de templates Angular"
description: "djLint linte les templates Angular. Utilisez le profil angular pour adapter les règles à ces templates."
sidebar:
  label: "Angular"
---

djLint linte les templates Angular. Utilisez le profil `angular` pour adapter les règles à ces templates.

**[Qu'est-ce qu'Angular ?](https://angular.io/guide/template-syntax)**

## En ligne de commande

```bash
djlint /path/to/templates --profile=angular
```

## Ou avec un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile = "angular"
```

```toml title="djlint.toml / .djlint.toml"
profile = "angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::
