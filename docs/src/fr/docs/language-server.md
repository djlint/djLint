---
description: Lancez djLint comme serveur de langage, pour voir les erreurs pendant la saisie et formater dans tout éditeur compatible LSP.
title: Serveur de langage
keywords: linter de modèles, formateur de modèles, djLint, HTML, modèles, formateur, linter, serveur de langage, lsp, neovim, zed, helix
---

# Serveur de langage

`djlint --lsp` lance djLint comme serveur de langage sur stdio. Il reste actif : l'éditeur reçoit les erreurs pendant la saisie et formate un document sans démarrer un processus à chaque fois.

Il signale les erreurs et formate des documents entiers. Il ne demande aucun paquet supplémentaire.

## Neovim

Avec Neovim 0.11 ou plus récent :

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Pour formater, appelez `vim.lsp.buf.format()`.

## Zed

Installez l'[extension djLint](https://github.com/djlint/zed-djlint).

## Helix

Dans `languages.toml` :

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["vscode-html-language-server", "djlint"]
formatter = { command = "djlint", args = ["--reformat", "--quiet", "-"] }
```

## Réglages

Le serveur lit la [configuration](/fr/docs/configuration/) du projet comme la ligne de commande, depuis le dossier de chaque fichier vers le haut. Les réglages de l'éditeur ont la priorité. Ils portent les noms des [options de la ligne de commande](/fr/docs/configuration/), avec des tirets bas ou en camelCase, et des listes peuvent remplacer les valeurs séparées par des virgules :

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

Le serveur demande la section `djlint` avec `workspace/configuration`. Un éditeur qui ne sait pas répondre peut envoyer les mêmes clés dans `initializationOptions`.

Deux réglages n'ont pas d'option de ligne de commande :

- `use_editor_indentation` : formater avec la taille de tabulation de l'éditeur, au lieu de `indent`.
- `python_rules` : la valeur `false` ignore les règles personnalisées avec un `python_module`, ce qui évite d'exécuter le code du projet.

Sans `profile` défini à l'un de ces endroits, la langue du document en choisit un : `htmldjango` utilise le profil `django`, par exemple.

## Fonctionnement

- Les erreurs arrivent après une courte pause dans la saisie. Un éditeur avec les diagnostics en pull les demande, les autres les reçoivent.
- `exclude`, `extend_exclude` et `use_gitignore` s'appliquent aux documents ouverts. Un document exclu n'a pas d'erreurs et n'est pas formaté.
- Il recharge la configuration quand `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc` ou `.gitignore` changent, si l'éditeur sait surveiller les fichiers.
