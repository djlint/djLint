---
description: Lancez djLint comme serveur de langage, pour voir les erreurs pendant la saisie et formater dans tout éditeur compatible LSP.
title: Serveur de langage
keywords: linter de modèles, formateur de modèles, djLint, HTML, modèles, formateur, linter, serveur de langage, lsp, neovim, zed, helix
---

# Serveur de langage

`djlint --lsp` lance djLint comme serveur de langage sur stdio. Il reste actif : l'éditeur reçoit les erreurs pendant la saisie et formate un document sans démarrer un processus à chaque fois.

Il signale les erreurs et formate des documents entiers. Il ne demande aucun paquet supplémentaire.

Quel que soit l'éditeur, installez djLint là où il peut le trouver, idéalement dans l'environnement virtuel du projet, et lancez l'éditeur depuis celui-ci ou indiquez-lui le `djlint` de cet environnement. L'éditeur utilise alors la version fixée par le projet, avec les mêmes résultats que votre hook pre-commit ou votre CI.

## Visual Studio Code

Installez l'[extension djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint), ou [sa version sur Open VSX](https://open-vsx.org/extension/monosans/djlint) pour VSCodium. Elle trouve djLint dans votre environnement, utilise celui qu'elle embarque sinon, et passe par le serveur de langage quand votre djLint le propose.

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

Pour formater à l'enregistrement, ajoutez à la même configuration :

```lua
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = { "*.html", "*.jinja", "*.jinja2", "*.j2" },
  callback = function(args)
    vim.lsp.buf.format({ bufnr = args.buf, name = "djlint" })
  end,
})
```

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
```

## IDE JetBrains

Dans PyCharm et les autres IDE basés sur IntelliJ, utilisez le plugin gratuit [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) :

1. Installez LSP4IJ depuis le Marketplace.
1. Ouvrez la fenêtre LSP Consoles et ajoutez un nouveau serveur de langage.
1. Dans l'onglet **Server**, indiquez le nom `djLint` et la commande `djlint --lsp`, avec le chemin complet du `djlint` de l'environnement virtuel du projet s'il n'est pas dans le PATH.
1. Dans l'onglet **Mappings**, ajoutez un motif de nom de fichier pour vos modèles, comme `*.html`. Pour un projet Django, donnez l'identifiant de langage `htmldjango`, afin de choisir le bon [profil](/fr/docs/configuration/#profile).
1. Dans l'onglet **Configuration**, vous pouvez donner les [réglages](#reglages) en JSON, sous une clé `djlint`.

Les erreurs apparaissent dans l'éditeur, et **Reformat Code** peut utiliser le serveur pour ces fichiers.

## Sublime Text

Avec le paquet [LSP](https://packagecontrol.io/packages/LSP), lancez **Preferences: LSP Server Configurations** et ajoutez :

```json
{
  "djlint": {
    "enabled": true,
    "command": ["djlint", "--lsp"],
    "selector": "text.html"
  }
}
```

## Emacs

Eglot, fourni avec Emacs 29 et plus récent :

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Lancez ensuite `M-x eglot` dans un modèle. `eglot-format-buffer` le formate.

## Réglages

Le serveur lit la [configuration](/fr/docs/configuration/) du projet comme la ligne de commande, depuis le dossier de chaque fichier vers le haut. Les réglages de l'éditeur ont la priorité mais, comme en ligne de commande, ils peuvent seulement activer une option ou donner une valeur : `false` ne désactive pas ce que le projet active. Ils portent les noms des [options de la ligne de commande](/fr/docs/configuration/), avec des tirets bas ou en camelCase, et des listes peuvent remplacer les valeurs séparées par des virgules :

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
