---
title: "Linter et formateur de templates Askama"
description: "djLint linte et formate les templates Askama. Utilisez le profil askama pour adapter les règles et le formatage à ces templates."
sidebar:
  label: "Askama"
---

djLint linte et formate les templates Askama. Utilisez le profil `askama` pour adapter les règles et le formatage à ces templates.

**[Qu'est-ce qu'Askama ?](https://askama.readthedocs.io/)**

## En ligne de commande

```bash
djlint /path/to/templates --profile=askama
```

## Ou avec un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile = "askama"
```

```toml title="djlint.toml / .djlint.toml"
profile = "askama"
```

```json title=".djlintrc"
{ "profile": "askama" }
```

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::
