---
title: "Linter et formateur de templates Go"
description: "djLint linte et formate les templates Go. Utilisez le profil golang pour adapter les règles et le formatage à ces templates."
sidebar:
  label: "Templates Go"
---

djLint linte et formate les templates Go. Utilisez le profil `golang` pour adapter les règles et le formatage à ces templates.

**[Que sont les templates Go ?](https://pkg.go.dev/text/template)**

Les templates Go (`text/template`, `html/template`) servent aussi aux thèmes Hugo et aux charts Helm : utilisez ce même profil pour eux.

## En ligne de commande

```bash
djlint /path/to/templates --profile=golang
```

## Ou avec un fichier de configuration

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
