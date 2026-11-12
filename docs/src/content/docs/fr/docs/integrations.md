---
title: "Intégrations"
description: "Utilisez djLint dans votre éditeur et exécutez-le avec pre-commit."
sidebar:
  label: "Intégrations"
---

Plusieurs intégrations d'éditeurs ont été conçues pour djLint.

Quel que soit votre éditeur, installez djLint là où l'éditeur peut le trouver, idéalement dans l'environnement virtuel du projet, puis lancez l'éditeur depuis cet environnement ou indiquez-lui le `djlint` de cet environnement. Ainsi, l'éditeur exécute la version fixée par votre projet, avec les mêmes résultats que votre hook pre-commit ou votre CI.

## Visual Studio Code

Installez l'[extension djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint), ou [celle publiée sur Open VSX](https://open-vsx.org/extension/monosans/djlint) pour VSCodium. Elle trouve djLint dans votre environnement, se rabat sur une version embarquée, et utilise le serveur de langage quand votre djLint en dispose.

Son code est sur [GitHub](https://github.com/djlint/djlint-vscode).

## Zed

Installez l'[extension djLint](https://github.com/djlint/djlint-zed), qui lance le [serveur de langage](#serveur-de-langage). Les erreurs s'affichent dans le HTML et dans les langages des extensions de modèles dès l'installation. Il faut djLint 1.49 ou plus récent. L'extension lance le `djlint` du PATH, ou djLint via uv s'il n'y en a pas ; pour en utiliser un autre, définissez `lsp.djlint.binary.path`.

Pour formater avec djLint, faites-en le formateur d'un langage :

```json
{ "languages": { "HTML": { "formatter": { "language_server": { "name": "djlint" } } } } }
```

Les [réglages](#options) se placent dans `lsp.djlint.settings`.

## Neovim

djLint peut servir de linter et de formateur dans Neovim.

### Client LSP intégré (recommandé)

Neovim 0.11 ou plus récent peut dialoguer directement avec le [serveur de langage](#serveur-de-langage) de djLint, sans plugin. Vous obtenez ainsi les signalements pendant la frappe, avec les plages concernées soulignées, et `vim.lsp.buf.format()` pour le formatage :

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Pour formater à l'enregistrement, ajoutez ceci à la même configuration :

```lua
vim.api.nvim_create_autocmd("BufWritePre", {
  pattern = {
    "*.html", "*.jinja", "*.jinja2", "*.j2",
    "*.hbs", "*.handlebars", "*.liquid", "*.gotmpl",
  },
  callback = function(args)
    vim.lsp.buf.format({ bufnr = args.buf, name = "djlint" })
  end,
})
```

Voir [Options](#options).

### conform.nvim et nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formate et [nvim-lint](https://github.com/mfussenegger/nvim-lint) linte, en exécutant djLint comme une commande. Les signalements n'ont pas de plage soulignée, et n'arrivent que lorsque vous demandez à nvim-lint de linter.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

- [Dépôt GitHub](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formatage](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### efm-langserver

- [Dépôt GitHub](https://github.com/mattn/efm-langserver)

1. Installez efm-langserver et djLint avec Mason via `:MasonInstall efm djlint`
1. Ajoutez `htmldjango` à `filetypes`.
1. Créez la configuration de formatage :

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. Associez le langage au formateur avec `htmldjango = { djlint }`.

Exemple de configuration :

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}

require("lspconfig").efm.setup({
    filetypes = { "htmldjango" },
    init_options = { documentFormatting = true },
    settings = {
        rootMarkers = { ".git/" },
        languages = {
            htmldjango = { djlint },
        },
    },
})
```

### coc.nvim

- [Paquet npm](https://www.npmjs.com/package/coc-htmldjango)

## IDE JetBrains

Dans PyCharm et les autres IDE basés sur IntelliJ, utilisez le plugin gratuit [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) :

1. Installez LSP4IJ depuis le Marketplace.
1. Ouvrez la fenêtre d'outils LSP Consoles et ajoutez un nouveau serveur de langage.
1. Dans l'onglet **Server**, définissez le nom `djLint` et la commande `djlint --lsp`, avec le chemin complet du `djlint` de l'environnement virtuel du projet s'il n'est pas dans le PATH.
1. Dans l'onglet **Mappings**, ajoutez un motif de nom de fichier pour vos templates, par exemple `*.html`. Si la configuration du projet n'a pas de [profil](/fr/docs/configuration/#profile), définissez l'identifiant de langage `htmldjango` pour un projet Django, afin que le bon profil soit choisi.
1. Dans l'onglet **Configuration**, vous pouvez définir des [options](#options) en JSON, sous une clé `djlint`.

Les signalements apparaissent dans l'éditeur, et **Reformat Code** peut utiliser le serveur pour les fichiers associés.

## Sublime Text

### LSP (recommandé)

Le paquet [LSP](https://packagecontrol.io/packages/LSP) exécute le [serveur de langage](#serveur-de-langage), qui fournit les signalements pendant la frappe ainsi que le formatage.

Exécutez **Preferences: LSP Server Configurations** et ajoutez :

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

djLint peut servir de plugin de linter pour Sublime Text. Il s'installe via [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

1. `cmd + shift + p`
2. Installez SublimeLinter
3. Installez SublimeLinter-contrib-djlint

Vérifiez que djLint est installé dans votre Python global, ou dans votre `PATH`.

## Helix

Helix peut exécuter le [serveur de langage](#serveur-de-langage) depuis `languages.toml` :

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Eglot, fourni avec Emacs 29 et plus récent :

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Exécutez ensuite `M-x eglot` dans un template. `eglot-format-buffer` le formate.

## Serveur de langage

`djlint --lsp` exécute djLint en tant que serveur de langage sur stdio. Il reste actif : un éditeur obtient donc les signalements pendant la frappe et formate un document sans lancer de processus à chaque fois.

Il remonte les signalements et formate des documents entiers. Il ne nécessite aucun paquet supplémentaire. Tout autre éditeur compatible LSP peut l'exécuter avec la même commande.

### Options

Le serveur lit la [configuration](/fr/docs/configuration/) du projet comme le fait la ligne de commande, en remontant depuis le dossier de chaque fichier. Les réglages de l'éditeur l'emportent sur elle, mais comme en ligne de commande, ils peuvent seulement activer une option ou définir une valeur : `false` ne désactive pas ce que le projet active. Ils portent les noms des [options de la ligne de commande](/fr/docs/configuration/), avec des tirets bas ou en camelCase, et des listes peuvent remplacer les valeurs séparées par des virgules :

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

Le serveur demande la section `djlint` avec `workspace/configuration`. Un éditeur qui ne sait pas y répondre peut envoyer les mêmes clés dans `initializationOptions`.

Deux réglages n'ont pas d'option en ligne de commande :

- `use_editor_indentation` : formater avec la taille de tabulation de l'éditeur, au lieu de `indent`.
- `python_rules` : réglez-le sur `false` pour ignorer les règles personnalisées dotées d'un `python_module`, ce qui empêche le code du projet de s'exécuter.

djLint prend le `profile` dans la première de ces sources qui en définit un :

1. Les réglages de l'éditeur.
1. La configuration du projet.
1. Le langage du document : `htmldjango` utilise le profil `django`, par exemple.

Si aucune n'en définit, il s'exécute sans profil, comme en ligne de commande. Un `profile` dans la configuration du projet est le choix le plus simple : il fonctionne dans tous les éditeurs, sans identifiant de langage à configurer.

### Ce qu'il fait

- Les signalements arrivent après une courte pause dans la frappe. Un éditeur qui prend en charge les diagnostics en mode pull les demande, et tout autre les reçoit en mode push.
- `exclude`, `extend_exclude` et `use_gitignore` s'appliquent aux documents ouverts. Un document exclu n'a aucun signalement et n'est pas formaté.
- Il recharge la configuration quand `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` ou `.gitignore` changent, si l'éditeur sait surveiller les fichiers, et sinon quand un document est ouvert ou enregistré. Les fichiers désignés par `configuration` ou `rules` sont relus quand un document est ouvert ou enregistré. Une modification du code du `python_module` d'une règle personnalisée nécessite un redémarrage.
- Une règle lente retarde ce qui vient après elle, car le serveur ne fait qu'une chose à la fois.

## GitHub Actions

Dans un workflow GitHub Actions, djLint remonte chaque signalement sous forme d'annotation, qui apparaît donc directement dans le diff d'une pull request. Aucune configuration n'est nécessaire : djLint détecte le workflow et change de format de sortie automatiquement.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

Utilisez `--no-github-output` pour obtenir à la place la sortie console classique, ou `--github-output` pour forcer les annotations en dehors d'Actions.

Les annotations sont liées à une seule pull request. Pour conserver les signalements dans l'onglet Security du dépôt, avec leur historique d'une exécution à l'autre, écrivez-les au format SARIF et envoyez le fichier :

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

L'étape d'envoi nécessite la permission `security-events: write` sur le job ou le workflow.

`--sarif` écrit un document SARIF 2.1.0 sur stdout et rien d'autre, ce qui permet de le rediriger comme ci-dessus. Chaque règle activée y figure avec un lien vers sa documentation, chaque signalement indique sa ligne et sa colonne, et avec `--check`, un fichier qui serait reformaté est signalé sous une règle `formatting`. Azure DevOps, GitLab et la plupart des éditeurs lisent ce même format.

## Pre-Commit

djLint peut servir de hook [pre-commit](https://pre-commit.com), à la fois comme linter et comme formateur.

Le dépôt fournit plusieurs hooks préconfigurés pour certains profils de djLint (ils se contentent de prérégler l'argument `--profile` et d'indiquer à pre-commit quelles extensions de fichiers rechercher) :

- `djlint` pour le linting et `djlint-reformat` pour le formatage
  Recherche les fichiers correspondant à `*.html` sans définir `--profile`.
- `djlint-django` et `djlint-reformat-django`
  Recherche les fichiers correspondant à `*.html` et définit `--profile=django`.
- `djlint-jinja` et `djlint-reformat-jinja`
  Recherche les fichiers correspondant à `*.j2`,`*.jinja` ou `*.jinja2` et définit `--profile=jinja`.
- `djlint-nunjucks` et `djlint-reformat-nunjucks`
  Recherche les fichiers correspondant à `*.njk` et définit `--profile=nunjucks`.
- `djlint-handlebars` et `djlint-reformat-handlebars`
  Recherche les fichiers correspondant à `*.hbs` et définit `--profile=handlebars`.
- `djlint-liquid` et `djlint-reformat-liquid`
  Recherche les fichiers correspondant à `*.html` et définit `--profile=liquid`.
- `djlint-golang` et `djlint-reformat-golang`
  Recherche les fichiers correspondant à `*.gotmpl` et définit `--profile=golang`.
- `djlint-tera` et `djlint-reformat-tera`
  Recherche les fichiers correspondant à `*.html` et définit `--profile=tera`.
- `djlint-askama` et `djlint-reformat-askama`
  Recherche les fichiers correspondant à `*.html` et définit `--profile=askama`.
- `djlint-mako` et `djlint-reformat-mako`
  Recherche les fichiers correspondant à `*.html` et définit `--profile=mako`.

Notez que ces hooks prédéfinis sont parfois trop restrictifs quant aux fichiers qu'ils acceptent (vos templates utilisent peut-être une autre extension) : pre-commit vous permet donc explicitement de remplacer chacune de ces options prédéfinies. Consultez la [documentation de pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks) pour les autres options de configuration.

### Exemple Django par défaut

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### Handlebars avec l'extension .html au lieu de .hbs

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-handlebars
        files: "\\.html"
        types_or: ["html"]
      - id: djlint-handlebars
        files: "\\.html"
        types_or: ["html"]
```

Vous pouvez utiliser les paramètres `files` ou `exclude` pour limiter chaque hook à son propre répertoire, ce qui permet de gérer plusieurs langages de templates dans un même dépôt.

## MegaLinter

djlint est intégré nativement parmi les plus de 100 linters de [MegaLinter](https://megalinter.io)

Pour l'installer, exécutez simplement `npx mega-linter-runner --install` et suivez les instructions

- [Dépôt GitHub](https://github.com/oxsecurity/megalinter)
- [djlint dans la documentation de MegaLinter](https://megalinter.io/latest/descriptors/html_djlint/)
