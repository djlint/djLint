---
title: "Linter et formateur de templates Go"
description: "djLint est un linter de templates Go et un formateur de templates Go ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint."
sidebar:
  label: "Templates Go"
---

djLint est un linter de templates Go et un formateur de templates Go ! Profitez du profil prédéfini pour linter et formater vos templates avec djLint.

**[Que sont les templates Go ?](https://pkg.go.dev/text/template)**

Les templates Go (`text/template`, `html/template`) servent aussi aux thèmes Hugo et aux charts Helm : utilisez ce même profil pour eux.

#### En ligne de commande

```bash
djlint /path/to/templates --profile=golang
```

#### Ou avec un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile = "golang"
```

```toml title="djlint.toml / .djlint.toml"
profile = "golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::
