---
description: Démarrage avec djLint pour le linting et le formatage de modèles HTML. Profitez de l'interface client facile et des nombreuses options de formatage.
title: Commencer
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, usage
---

# {{ "getting_started" | i18n }}

## Installation

djLint est construit avec [Python](https://python.org) et publié sur [PyPI](https://pypi.org/project/djlint/). Avec [uv](https://docs.astral.sh/uv/), ajoutez-le à votre projet comme dépendance de développement :

```bash
uv add --dev djlint
```

Ou installez-le en tant qu'outil autonome :

```bash
uv tool install djlint
```

Ou avec pip :

```bash
pip install djlint
```

Ou avec [pipx](https://pipx.pypa.io/):

```bash
pipx install djlint
```

Ou avec la formule [Homebrew](https://formulae.brew.sh/formula/djlint) maintenue par la communauté sur macOS ou Linux:

```bash
brew install djlint
```

_Ou avec npm - **attention** : le paquet npm n'est qu'une enveloppe, son script d'installation exécute `pip install --upgrade djlint` avec le `python3` de votre chemin système. npm ne gère ni ne désinstalle le paquet réel - préférez pip directement si possible._

```bash
npm i djlint
```

Pour lancer djLint à chaque commit, voir [pre-commit]({{ "lang_code_url" | i18n }}/docs/integrations/#pre-commit).

## Utilisation de l'interface CLI

djLint est une application en ligne de commande. Voir la page [configuration]({{ "lang_code_url" | i18n }}/docs/configuration/) pour une configuration avancée.

{% include 'src/_includes/cli.md' %}

{% admonition
   "note",
   "Note",
   "Si la commande `djlint` n'est pas trouvée, assurez-vous que Python est [dans votre path](https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/)."
%}

## Utilisation de Path vs Stdin

djLint fonctionne avec un path ou stdin.

Exécution avec un path -

```bash
djlint /path/to/templates --lint
```

Ou un fichier spécifique -

```bash
djlint /path/to/this.mustache --lint
```

Ou avec stdin -

```bash
echo "<div></div>" | djlint -
```

Stdin peut également être utilisé pour reformater le code. La sortie sera uniquement le code formaté sans messages.

```bash
echo "<div></div>" | djlint - --reformat
```

Sortie -

```html
<div></div>
```

Lors de la lecture depuis stdin, djLint n'a pas de vrai chemin à comparer avec `per-file-ignores` ni à afficher dans les messages, il utilise donc `-` par défaut. Passez `--stdin-filename` pour indiquer à djLint le vrai chemin du contenu reçu, par exemple quand une intégration d'éditeur lui envoie le contenu d'un fichier à l'enregistrement.

```bash
echo "<div></div>" | djlint - --stdin-filename templates/index.html
```

## Codes de sortie

| Code | Signification                                                                                                                                                              |
| ---- | -------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0`  | Tout ce que djLint devait vérifier est correct, ou chaque fichier trouvé a été ignoré par votre configuration.                                                             |
| `1`  | djLint a trouvé des erreurs de linting ou des fichiers à reformater. Avec `--warn`, elles sont signalées comme avertissements et le code de sortie est `0`.                |
| `2`  | djLint n'a pas vérifié ce que vous avez demandé : les chemins ne correspondent à aucun fichier, la ligne de commande ou la configuration est invalide, ou djLint a échoué. |

Seul le code `1` signifie que djLint a examiné vos modèles et y a trouvé des problèmes. Le code `2` signifie toujours que l'exécution elle-même n'a pas abouti : un pipeline peut donc traiter les deux cas différemment sans avoir à deviner.

Le code `2` détecte une exécution qui n'a rien vérifié du tout : un mauvais chemin, une `--extension` qui ne correspond plus, ou des modèles qui ont été déplacés. Sans lui, une telle exécution réussit en silence sans avoir examiné un seul de vos modèles.

Les fichiers que djLint _a_ trouvés puis ignorés volontairement, via `exclude`, `extend_exclude`, `use_gitignore` ou `require_pragma`, ne sont pas une erreur. L'exécution se termine avec le code `0`, car la configuration a fait exactement ce qu'on lui demandait. C'est aussi ce qui permet à `exclude` de fonctionner avec pre-commit, qui transmet les noms de vos fichiers indexés, que vous vouliez ou non que djLint les examine.

Si un chemin sans aucun modèle est normal dans votre pipeline, désactivez le code `2` avec `allow_empty_input` :

```bash
djlint /path/to/templates --lint --allow-empty-input
```
