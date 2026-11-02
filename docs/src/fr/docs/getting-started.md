---
description: Prise en main de djLint pour le linting et le formatage de templates HTML. Tirez parti de son interface en ligne de commande simple et des nombreuses options du formateur.
title: Prise en main
keywords: linter de templates, formateur de templates, djLint, HTML, templates, formateur, linter, utilisation
---

# Prise en main

## Installation

djLint est écrit en [Python](https://python.org) et publié sur [PyPI](https://pypi.org/project/djlint/). Avec [uv](https://docs.astral.sh/uv/), ajoutez-le à votre projet comme dépendance de développement :

```bash
uv add --dev djlint
```

Ou installez-le comme outil autonome :

```bash
uv tool install djlint
```

Ou avec pip :

```bash
pip install djlint
```

Ou avec [pipx](https://pipx.pypa.io/) :

```bash
pipx install djlint
```

Ou avec la [formule Homebrew](https://formulae.brew.sh/formula/djlint) maintenue par la communauté, sous macOS ou Linux :

```bash
brew install djlint
```

_Ou avec npm – **attention** : le paquet npm n'est qu'une surcouche, son script d'installation exécute `pip install --upgrade djlint` avec le `python3` présent dans le PATH de votre système. npm ne gère pas le vrai paquet et ne le désinstalle pas – utilisez plutôt pip directement quand c'est possible._

```bash
npm i djlint
```

Pour exécuter djLint à chaque commit, consultez [pre-commit]({{ "lang_code_url" | i18n }}/docs/integrations/#pre-commit).

## Utilisation en ligne de commande

djLint est une application en ligne de commande. Consultez la page [configuration]({{ "lang_code_url" | i18n }}/docs/configuration/) pour une configuration avancée.

{% include 'src/_includes/cli.md' %}

{% admonition
   "note",
   "Remarque",
   "Si la commande `djlint` est introuvable, vérifiez que Python est bien [dans votre PATH](https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/)."
%}

## Chemin ou stdin

djLint accepte un chemin ou l'entrée standard (stdin).

Avec un chemin :

```bash
djlint /path/to/templates --lint
```

Ou un fichier précis :

```bash
djlint /path/to/this.mustache --lint
```

Ou avec stdin :

```bash
echo "<div></div>" | djlint -
```

L'entrée standard permet aussi de reformater du code. La sortie ne contient alors que le code formaté, sans aucun message.

```bash
echo "<div></div>" | djlint - --reformat
```

Sortie :

```html
<div></div>
```

Quand il lit l'entrée standard, djLint n'a pas de vrai chemin à comparer à `per-file-ignores` ni à afficher dans les messages : il utilise donc `-` par défaut. Passez `--stdin-filename` pour indiquer à djLint le vrai chemin du contenu reçu, par exemple quand une intégration d'éditeur lui transmet le contenu d'un fichier à l'enregistrement.

```bash
echo "<div></div>" | djlint - --stdin-filename templates/index.html
```

## Codes de sortie

| Code | Signification                                                                                                                                                                  |
| ---- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `0`  | Tout ce que djLint devait vérifier est propre, ou chaque fichier trouvé a été ignoré par votre configuration.                                                                  |
| `1`  | djLint a trouvé des erreurs de linting, ou des fichiers à reformater. Avec `--warn`, ils sont signalés comme des avertissements et le code de sortie est `0`.                  |
| `2`  | djLint n'a pas vérifié ce que vous lui avez demandé : les chemins ne correspondent à aucun fichier, la ligne de commande ou la configuration est invalide, ou djLint a échoué. |

Seul le code `1` signifie que djLint a examiné vos templates et n'a pas aimé ce qu'il y a trouvé. Le code `2` signifie toujours que l'exécution elle-même n'a pas abouti : un pipeline peut donc traiter les deux cas différemment au lieu de deviner.

C'est le code `2` qui repère une exécution qui n'a rien vérifié du tout : un chemin erroné, une `--extension` qui ne correspond plus, ou des templates qui ont été déplacés. Sans lui, une telle exécution passe en silence, sans avoir examiné aucun de vos templates.

Les fichiers que djLint a _bien_ trouvés puis volontairement ignorés, via `exclude`, `extend_exclude`, `use_gitignore` ou `require_pragma`, ne constituent pas une erreur. L'exécution se termine alors avec `0`, car la configuration a fait exactement ce qu'on lui demandait. C'est aussi ce qui permet à `exclude` de fonctionner avec pre-commit, qui transmet les noms de vos fichiers indexés, que vous vouliez ou non que djLint les examine.

Si, dans votre pipeline, il est normal qu'un chemin ne contienne légitimement aucun template, désactivez le code `2` avec `allow_empty_input` :

```bash
djlint /path/to/templates --lint --allow-empty-input
```
