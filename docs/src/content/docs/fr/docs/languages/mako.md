---
title: "Linter et formateur de templates Mako"
description: "djLint linte et formate les templates Mako. Utilisez le profil mako pour adapter les règles et le formatage à ces templates."
sidebar:
  label: "Mako"
---

djLint linte et formate les templates Mako. Utilisez le profil `mako` pour adapter les règles et le formatage à ces templates.

**[Qu'est-ce que Mako ?](https://www.makotemplates.org/)**

Avec le profil mako, une ligne de contrôle comme `% if x:` et un commentaire `##` gardent toujours une ligne à eux, et une balise dont les attributs dépendent de lignes de contrôle les garde tels qu'ils sont écrits. Les blocs Python et le contenu de `<%doc>` et `<%text>` ne sont pas modifiés, pas plus qu'un script ou un style qui contient de la syntaxe Mako avec `--format-js` ou `--format-css`. Les lignes entre `% if` et `% endif`, et entre une balise `<%block>` ou `<%def>` et sa balise fermante quand chacune est sur sa propre ligne, sont indentées comme n'importe quel autre bloc. Le code d'une expression `${}` reste tel qu'il est écrit.

## En ligne de commande

```bash
djlint /path/to/templates --profile=mako
```

## Ou avec un fichier de configuration

Configurez djLint dans le fichier `pyproject.toml`, `djlint.toml` / `.djlint.toml` ou `.djlintrc` de votre projet.

```toml title="pyproject.toml"
[tool.djlint]
profile = "mako"
```

```toml title="djlint.toml / .djlint.toml"
profile = "mako"
```

```json title=".djlintrc"
{ "profile": "mako" }
```

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::
