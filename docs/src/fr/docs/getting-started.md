---
description: Démarrage avec djLint pour le linting et le formatage de modèles HTML. Profitez de l'interface client facile et des nombreuses options de formatage.
title: Commencer
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, usage
---

# {{ "getting_started" | i18n }}

## Installation de [Pypi](https://pypi.org/project/djlint/)

djLint est construit avec [Python 3.7+](https://python.org), il peut être installé en exécutant simplement:

```bash
pip install djlint
```

## Utilisation de l'interface CLI

djLint est une application en ligne de commande. Voir `configuration` pour une configuration avancée.

```bash
Usage: djlint [OPTIONS] SRC ...

  djLint · lint and reformat HTML templates.

Options:
  --version             Show the version and exit.
  -e, --extension TEXT  File extension to check [default: html]
  -i, --ignore TEXT     Codes to ignore. ex: "H014,H017"
  --reformat            Reformat the file(s).
  --check               Check formatting on the file(s).
  --indent INTEGER      Indent spacing. [default: 4]
  --quiet               Do not print diff when reformatting.
  --profile TEXT        Enable defaults by template language. ops: django,
                        jinja, nunjucks, handlebars, golang, angular,
                        html [default: html]
  --require-pragma      Only format or lint files that starts with a comment
                        with the text 'djlint:on'
  --lint                Lint for common issues. [default option]
  --use-gitignore       Use .gitignore file to extend excludes.
  -h, --help            Show this message and exit.
```

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
