---
title: "Intégrations"
description: "Intégrez djLint avec votre éditeur préféré. Formatez automatiquement vos modèles avec Pre-Commit. Lint avec SublimeText."
sidebar:
  label: "Intégrations"
---

Il existe plusieurs intégrations d'éditeurs construites pour djLint.

Quel que soit l'éditeur, installez djLint là où il peut le trouver, idéalement dans l'environnement virtuel du projet, et lancez l'éditeur depuis celui-ci ou indiquez-lui le `djlint` de cet environnement. L'éditeur utilise alors la version fixée par le projet, avec les mêmes résultats que votre hook pre-commit ou votre CI.

## Visual Studio Code

Installez l'[extension djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint), ou [sa version sur Open VSX](https://open-vsx.org/extension/monosans/djlint) pour VSCodium. Elle trouve djLint dans votre environnement, utilise celui qu'elle embarque sinon, et passe par le serveur de langage quand votre djLint le propose.

Son code se trouve sur [GitHub](https://github.com/djlint/djlint-vscode).

## Neovim

djLint peut être utilisé comme linter et formateur dans Neovim.

### Client LSP intégré (recommandé)

Neovim 0.11 ou plus récent peut parler directement au [serveur de langage](#serveur-de-langage) de djLint, sans plugin. Vous obtenez les erreurs pendant la saisie, avec leur étendue soulignée, et le formatage avec `vim.lsp.buf.format()` :

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Pour formater à l'enregistrement, ajoutez à la même configuration :

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

Voir les [réglages](#réglages).

### conform.nvim et nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formate et [nvim-lint](https://github.com/mfussenegger/nvim-lint) analyse, en lançant djLint comme une commande. Les erreurs n'ont pas d'étendue soulignée et n'arrivent que lorsque vous demandez à nvim-lint d'analyser.

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

- [GitHub dépôt](https://github.com/nvimtools/none-ls.nvim)
- [Linting](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formatage](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### efm-langserver

- [GitHub dépôt](https://github.com/mattn/efm-langserver)

1. Installez efm-langserver et djLint avec Mason via `:MasonInstall efm djlint`
1. Ajoutez `htmldjango` à `filetypes`.
1. Créez la configuration de formatage :

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. Associez le langage au formateur avec `htmldjango = { djlint }`.

Exemple de configuration :

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

- [npm package](https://www.npmjs.com/package/coc-htmldjango)

## IDE JetBrains

Dans PyCharm et les autres IDE basés sur IntelliJ, utilisez le plugin gratuit [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) :

1. Installez LSP4IJ depuis le Marketplace.
1. Ouvrez la fenêtre LSP Consoles et ajoutez un nouveau serveur de langage.
1. Dans l'onglet **Server**, indiquez le nom `djLint` et la commande `djlint --lsp`, avec le chemin complet du `djlint` de l'environnement virtuel du projet s'il n'est pas dans le PATH.
1. Dans l'onglet **Mappings**, ajoutez un motif de nom de fichier pour vos modèles, comme `*.html`. Si la configuration du projet n'a pas de [profil](/fr/docs/configuration/#profile), donnez l'identifiant de langage `htmldjango` pour un projet Django, afin de choisir le bon.
1. Dans l'onglet **Configuration**, vous pouvez donner les [réglages](#réglages) en JSON, sous une clé `djlint`.

Les erreurs apparaissent dans l'éditeur, et **Reformat Code** peut utiliser le serveur pour ces fichiers.

## Sublime Text

### LSP (recommandé)

Le paquet [LSP](https://packagecontrol.io/packages/LSP) lance le [serveur de langage](#serveur-de-langage), qui signale les erreurs pendant la saisie et formate.

Lancez **Preferences: LSP Server Configurations** et ajoutez :

```json
{
  "djlint": {
    "enabled": true,
    "command": ["djlint", "--lsp"],
    "selector": "text.html"
  }
}
```

### SublimeLinter

djLint peut être utilisé comme un plugin SublimeText Linter. Il peut être installé via [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

1. `cmd + shift + p`
2. Installer SublimeLinter
3. Installer SublimeLinter-contrib-djlint

Assurez-vous que djLint est installé dans votre python global, ou sur votre `PATH`.

## Helix

Helix lance le [serveur de langage](#serveur-de-langage) depuis `languages.toml` :

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Eglot, fourni avec Emacs 29 et plus récent :

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

Lancez ensuite `M-x eglot` dans un modèle. `eglot-format-buffer` le formate.

## Serveur de langage

`djlint --lsp` lance djLint comme serveur de langage sur stdio. Il reste actif : l'éditeur reçoit les erreurs pendant la saisie et formate un document sans démarrer un processus à chaque fois.

Il signale les erreurs et formate des documents entiers. Il ne demande aucun paquet supplémentaire. Tout autre éditeur compatible LSP peut le lancer avec la même commande.

### Réglages

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

djLint prend le `profile` de la première de ces sources qui en a un :

1. Les réglages de l'éditeur.
1. La configuration du projet.
1. La langue du document : `htmldjango` utilise le profil `django`, par exemple.

Sinon, il fonctionne sans profil, comme en ligne de commande. Le plus simple est de définir `profile` dans la configuration du projet : cela marche dans tous les éditeurs, sans identifiant de langage à configurer.

### Fonctionnement

- Les erreurs arrivent après une courte pause dans la saisie. Un éditeur avec les diagnostics en pull les demande, les autres les reçoivent.
- `exclude`, `extend_exclude` et `use_gitignore` s'appliquent aux documents ouverts. Un document exclu n'a pas d'erreurs et n'est pas formaté.
- Il recharge la configuration quand `pyproject.toml`, `djlint.toml`, `.djlint.toml`, `.djlintrc`, `.djlint_rules.yaml`, `.editorconfig` ou `.gitignore` changent, si l'éditeur sait surveiller les fichiers, et sinon à l'ouverture ou à l'enregistrement d'un document. Les fichiers indiqués par `configuration` ou `rules` sont relus à l'ouverture ou à l'enregistrement d'un document. Une modification du code du `python_module` d'une règle personnalisée demande un redémarrage.
- Une règle lente retarde ce qui la suit, car le serveur traite une chose à la fois.

## GitHub Actions

Dans un workflow GitHub Actions, djLint signale chaque résultat sous forme d'annotation, qui apparaît donc directement dans le diff d'une pull request. Aucune configuration n'est nécessaire : djLint détecte le workflow et adapte sa sortie automatiquement.

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

Utilisez `--no-github-output` pour obtenir la sortie console habituelle, ou `--github-output` pour forcer les annotations en dehors d'Actions.

Les annotations sont liées à une seule pull request. Pour conserver les résultats dans l'onglet Security du dépôt, avec leur historique d'une exécution à l'autre, écrivez-les au format SARIF et téléversez le fichier :

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

L'étape de téléversement nécessite la permission `security-events: write` sur le job ou le workflow.

`--sarif` écrit sur stdout un document SARIF 2.1.0 et rien d'autre, la sortie peut donc être redirigée comme ci-dessus. Chaque règle activée y figure avec un lien vers sa documentation, chaque résultat indique sa ligne et sa colonne, et avec `--check` un fichier qui serait reformaté est signalé sous une règle `formatting`. Azure DevOps, GitLab et la plupart des éditeurs lisent le même format.

## Pre-Commit

djLint peut être utilisé comme un hook [pre-commit](https://pre-commit.com) en tant que linter et formatter.

Le repo fournit de multiples hooks pré-configurés pour des profils djLint spécifiques (il suffit de prédéfinir l'argument `--profile` et d'indiquer à pre-commit les extensions de fichiers à rechercher) :

- `djlint` pour le linting et `djlint-reformat` pour le formatage
  Ceci recherchera les fichiers correspondant à `*.html` sans définir `--profile`.
- `djlint-django` et `djlint-reformat-django`
  Ceci recherchera les fichiers correspondant à `*.html` et définira `--profile=django`.
- `djlint-jinja` et `djlint-reformat-jinja`
  Ceci recherchera les fichiers correspondant à `*.j2`, `*.jinja` ou `*.jinja2` et définira `--profile=jinja`.
- `djlint-nunjucks` et `djlint-reformat-nunjucks`
  Ceci recherchera les fichiers correspondant à `*.njk` et définira `--profile=nunjucks`.
- `djlint-handlebars` et `djlint-reformat-handlebars`
  Ceci recherchera les fichiers correspondant à `*.hbs` et définira `--profile=handlebars`.
- `djlint-liquid` et `djlint-reformat-liquid`
  Ceci recherchera les fichiers correspondant à `*.html` et définira `--profile=liquid`.
- `djlint-golang` et `djlint-reformat-golang`
  Ceci recherchera les fichiers correspondant à `*.gotmpl` et définira `--profile=golang`.
- `djlint-tera` et `djlint-reformat-tera`
  Ceci recherchera les fichiers correspondant à `*.html` et définira `--profile=tera`.
- `djlint-askama` et `djlint-reformat-askama`
  Ceci recherchera les fichiers correspondant à `*.html` et définira `--profile=askama`.

Notez que ces hooks prédéfinis sont parfois trop conservateurs dans les entrées qu'ils acceptent (vos templates peuvent utiliser une extension différente) donc pre-commit vous permet explicitement de remplacer n'importe laquelle de ces options prédéfinies. Consultez la [docs pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks) pour une configuration supplémentaire.

### Exemple de Django par défaut

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

Vous pouvez utiliser les paramètres `files` ou `exclude` pour contraindre chaque hook à son propre répertoire, ce qui vous permet de supporter plusieurs langages de template dans le même repo.

## MegaLinter

djLint est intégré nativement parmi les plus de 100 linters de [MegaLinter](https://megalinter.io).

Pour l'installer, lancez `npx mega-linter-runner --install` et suivez les instructions.

- [GitHub dépôt](https://github.com/oxsecurity/megalinter)
- [djlint dans la documentation de MegaLinter](https://megalinter.io/latest/descriptors/html_djlint/)
