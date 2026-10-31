---
description: Formatez et analysez des modèles depuis votre code Python avec l'API de djLint.
title: API Python
keywords: linter de modèles, formateur de modèles, djLint, HTML, modèles, formateur, linter, python, api
---

# API Python

`djlint.api` formate et analyse du texte depuis un programme Python, avec les mêmes résultats que la ligne de commande. Il s'adresse aux éditeurs, aux outils de build et à tout ce qui garde un modèle en mémoire. Tout le reste du paquet peut changer à chaque version : utilisez ce module plutôt que `djlint.settings` ou `djlint.lint`.

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, **options)` lit la configuration qui s'applique aux fichiers d'un dossier. La recherche remonte depuis ce dossier, comme la ligne de commande depuis le répertoire courant, et le répertoire courant ne change pas.

Les options portent le nom de celles de la ligne de commande, avec des tirets bas, et fonctionnent de la même façon : une valeur définie l'emporte sur le fichier de configuration, tandis que `False`, `0` ou une chaîne vide comptent comme non définis. Les chemins sont donnés en `pathlib.Path`.

La lecture de la configuration prend du temps : gardez le résultat tant que les fichiers lus ne changent pas. Il sert pour autant de textes que nécessaire.

Avec `python_rules=False`, les règles personnalisées avec un `python_module` ne sont pas chargées, ce qui empêche le code d'un projet auquel vous ne faites pas confiance de s'exécuter. Leurs noms sont dans `config.skipped_rules`.

## format_text

`format_text(config, text)` renvoie le texte formaté. Un texte dont la première ligne se termine par CRLF revient en CRLF, tout autre en LF. Avec `require_pragma`, un texte sans le pragma revient inchangé.

## lint_text

`lint_text(config, text, filename="-")` renvoie une liste de `Finding`, dans l'ordre du document. `filename` est ce à quoi `per-file-ignores` est comparé. Avec `require_pragma`, un texte sans le pragma n'a aucun résultat.

`Finding` est un tuple nommé avec ces champs :

::: content

- `code` : Le code de la règle, comme `H013`.
- `message` : Le message de la règle.
- `match` : Le début du texte trouvé, jusqu'à 20 caractères.
- `line`, `column` : Le début du résultat. Les lignes comptent à partir de 1, les colonnes à partir de 0.
- `end_line`, `end_column` : La position juste après sa fin, qui peut être sur une ligne suivante.
  :::

Les colonnes comptent des caractères, pas des octets ni des unités UTF-16.

## Modules de règles

Le `python_module` d'une règle personnalisée est importé une fois par processus, depuis la racine du projet de la configuration. Un programme qui reste lancé et travaille sur plusieurs projets doit retirer ce module et ses paquets parents de `sys.modules` pour le relire. La racine du projet reste à la fin de `sys.path`.
