---
title: "Go Template Linter and Formatter"
description: "djLint est un linter de modèles Go et un formateur de modèles Go ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint."
sidebar:
  label: "Go templates"
---

djLint est un linter de modèles Go et un formateur de modèles Go ! Profitez du profil pré-construit lorsque vous lintez et formatez vos modèles avec djLint.

**[C'est quoi les modèles Go ?](https://pkg.go.dev/text/template)**

Les modèles Go (`text/template`, `html/template`) sont aussi utilisés par les thèmes Hugo et les charts Helm, utilisez donc ce même profil pour eux.

#### Utilisation de la ligne de commande

```bash
djlint /path/to/templates --profile=golang
```

#### Ou, utiliser un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile="golang"
```

```toml title="djlint.toml / .djlint.toml"
profile="golang"
```

```json title=".djlintrc"
{ "profile": "golang" }
```

:::tip
[Consultez le guide de configuration pour connaître toutes les options !](/fr/docs/configuration/)
:::
