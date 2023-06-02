---
description: Démarrage avec djLint pour le linting et le formatage de modèles HTML. Profitez de l'interface client facile et des nombreuses options de formatage.
title: Commencer
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, usage
---

# {{ "getting_started" | i18n }}

## Installation de [Pypi](https://pypi.org/project/djlint/)

djLint est construit avec [Python](https://python.org), il peut être installé en exécutant simplement:

```bash
pip install djlint
```

_Ou avec l'installation expérimentale npm - Note, ceci requiert que python et pip soient dans votre chemin système._

```bash
npm i djlint
```

## Utilisation de l'interface CLI

djLint est une application en ligne de commande. Voir `configuration` pour une configuration avancée.

{% include 'src/\_includes/cli.md' %}

{% admonition
   "note",
   "Note",
   "Si la commande `djlint` n'est pas trouvée, assurez-vous que Python est [dans votre path].(https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/)."
%}

## Utilisation de Path vs Stdin

djLint fonctionne avec un path ou stdin.

Courir avec un path -

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
