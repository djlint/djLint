---
title: "API Python"
description: "Formatez et lintez des templates depuis votre propre code Python avec l'API de djLint."
---

`djlint.api` formate et linte du texte depuis un programme Python, avec les mêmes résultats que la ligne de commande. Il s'adresse aux éditeurs, aux outils de build et à tout ce qui garde un template en mémoire. Tout le reste du paquet peut changer d'une version à l'autre : utilisez donc ce module plutôt que `djlint.settings` ou `djlint.lint`.

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, **options)` lit la configuration qui s'applique aux fichiers d'un dossier. Il la cherche en remontant depuis ce dossier, comme la ligne de commande le fait depuis le répertoire courant, et ne change pas de répertoire courant.

Les options portent les noms des options de la ligne de commande, avec des tirets bas, et fonctionnent comme là-bas : une valeur définie l'emporte sur le fichier de configuration, tandis que `False`, une chaîne vide et, pour la plupart des options, `0` comptent comme non renseignés. Les chemins sont passés en `pathlib.Path`.

La lecture de la configuration prend un certain temps : conservez donc le résultat tant que les fichiers dont il provient ne changent pas. Il peut servir pour un nombre quelconque de textes.

Avec `python_rules=False`, les règles personnalisées dotées d'un `python_module` ne sont pas chargées, ce qui empêche le code d'un projet auquel vous ne faites pas confiance de s'exécuter. Leurs noms figurent dans `config.skipped_rules`.

## format_text

`format_text(config, text)` renvoie le texte formaté. Un texte dont la première ligne se termine par CRLF est renvoyé en CRLF, et tout autre en LF. Avec `require_pragma`, un texte sans le pragma est renvoyé inchangé.

## lint_text

`lint_text(config, text, filename="-")` renvoie une liste de `Finding`, dans l'ordre du document. `filename` est ce à quoi `per-file-ignores` est comparé. Avec `require_pragma`, un texte sans le pragma n'a aucun signalement.

`Finding` est un tuple nommé avec les champs suivants :

- `code` : le code de la règle, par exemple `H013`.
- `message` : ce que dit la règle.
- `match` : le début du texte trouvé, jusqu'à 20 caractères.
- `line`, `column` : l'endroit où commence le signalement. Les lignes sont comptées à partir de 1, et les colonnes à partir de 0.
- `end_line`, `end_column` : juste après l'endroit où il se termine, ce qui peut se trouver sur une ligne suivante.

Les colonnes comptent des caractères, pas des octets ni des unités de code UTF-16.

## is_excluded

`is_excluded(config, path)` indique si `exclude`, `extend_exclude` ou le gitignore excluent un fichier, comme le fait la ligne de commande. `format_text` et `lint_text` ne le vérifient pas d'eux-mêmes.

## Modules de règles

Le `python_module` d'une règle personnalisée est importé une fois par processus, depuis la racine du projet de la configuration. Un programme qui reste en cours d'exécution et travaille avec plusieurs projets doit retirer de `sys.modules` tout ce qui a été importé depuis le projet, ainsi que la racine du projet, qui reste à la fin de `sys.path`, pour lire les modules d'un autre projet.
