---
title: "Intégrations"
description: "Utilisez djLint dans votre éditeur et exécutez-le avec pre-commit."
---

Quel que soit votre éditeur, installez djLint là où l'éditeur peut le trouver, idéalement dans l'environnement virtuel du projet, puis lancez l'éditeur depuis cet environnement ou indiquez-lui le `djlint` de cet environnement. Ainsi, l'éditeur exécute la version fixée par votre projet, avec les mêmes résultats que votre hook pre-commit ou votre CI.

Si le projet installe djLint avec [npm](/fr/docs/getting-started/#installation), sa commande est `node_modules/.bin/djlint` dans le projet, ou `node_modules/.bin/djlint.cmd` sous Windows. Là où un éditeur ci-dessous lance `djlint`, donnez-lui ce chemin. Le chemin est relatif, lancez donc l'éditeur à la racine du projet. Les extensions pour VS Code et Zed le trouvent d'elles-mêmes.

## Visual Studio Code

Installez l'[extension djLint](https://marketplace.visualstudio.com/items?itemName=monosans.djlint) depuis le Visual Studio Marketplace. Cursor, Windsurf, VSCodium et les autres éditeurs basés sur VS Code installent [la même extension depuis Open VSX](https://open-vsx.org/extension/monosans/djlint). Elle trouve djLint dans votre environnement, se rabat sur une version embarquée, et utilise le serveur de langage quand votre djLint en dispose.

Son [README](https://github.com/djlint/djlint-vscode#readme) décrit ses paramètres et le djLint qu'elle exécute.

## Zed

L'[extension djLint](https://github.com/djlint/djlint-zed) exécute le [serveur de langage](#serveur-de-langage) dans le HTML et dans les langages des extensions de templates, comme Django, Jinja et Twig. Elle n'est pas encore dans le registre d'extensions de Zed, installez-la donc comme extension de développement :

1. Installez Rust avec [rustup](https://rustup.rs) : Zed compile l'extension avec et ajoute lui-même la cible `wasm32-wasip2`. Avec un Rust installé autrement, par exemple via Homebrew ou Nix, ajoutez-la vous-même.
1. Clonez l'extension :

   ```bash
   git clone https://github.com/djlint/djlint-zed
   ```

1. Dans Zed, ouvrez la palette de commandes (`cmd-shift-p` sur macOS, `ctrl-shift-p` ailleurs), lancez **zed: install dev extension** et choisissez le dossier cloné `djlint-zed`.

Pour la mettre à jour, lancez `git pull` dans ce dossier, puis **zed: rebuild dev extension**.

Elle a besoin de djLint 1.49 ou plus récent dans le PATH ou installé dans le projet avec npm, ou de [uv](https://docs.astral.sh/uv/), qui lance djLint sans l'installer. Son [README](https://github.com/djlint/djlint-zed#readme) explique comment en faire le formateur d'un langage, et présente ses réglages.

## Neovim

Neovim ne donne aucun filetype à certaines extensions de templates. Quelle que soit l'option choisie ci-dessous, enregistrez-les d'abord :

```lua
vim.filetype.add({
  extension = {
    gohtml = "gotmpl", gotmpl = "gotmpl", handlebars = "handlebars",
    j2 = "jinja", jinja2 = "jinja", mako = "mako", njk = "nunjucks",
  },
})
```

### Client LSP intégré (recommandé)

Neovim 0.11 ou plus récent peut dialoguer directement avec le [serveur de langage](#serveur-de-langage) de djLint, sans plugin. Vous obtenez ainsi les signalements pendant la frappe, avec les plages concernées soulignées, et `vim.lsp.buf.format()` pour le formatage :

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = {
    "html", "htmldjango", "htmlangular", "jinja", "jinja.html", "nunjucks",
    "twig", "handlebars", "mustache", "liquid", "gotmpl", "tera", "mako",
  },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Pour formater à l'enregistrement, ajoutez ceci à la même configuration :

```lua
local group = vim.api.nvim_create_augroup("djlint_format", {})
vim.api.nvim_create_autocmd("LspAttach", {
  callback = function(args)
    if vim.lsp.get_client_by_id(args.data.client_id).name ~= "djlint" then
      return
    end
    vim.api.nvim_clear_autocmds({ group = group, buffer = args.buf })
    vim.api.nvim_create_autocmd("BufWritePre", {
      group = group,
      buffer = args.buf,
      callback = function()
        vim.lsp.buf.format({ bufnr = args.buf, name = "djlint" })
      end,
    })
  end,
})
```

Voir [Options](#options).

### conform.nvim et nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) formate et [nvim-lint](https://github.com/mfussenegger/nvim-lint) linte, en exécutant djLint comme une commande. Les signalements n'ont pas de plage soulignée, et n'arrivent que lorsque vous demandez à nvim-lint de linter. Le profil vient de la [configuration](/fr/docs/configuration/#profile) du projet, comme en ligne de commande. Cet exemple demande djLint 1.49 ou plus récent.

```lua
local formatters, linters = {}, {}
for _, filetype in ipairs({
  "html", "htmldjango", "htmlangular", "jinja", "jinja.html", "nunjucks",
  "twig", "handlebars", "mustache", "liquid", "gotmpl", "tera", "mako",
}) do
  formatters[filetype] = { "djlint" }
  linters[filetype] = { "djlint" }
end
require("conform").setup({
  formatters_by_ft = formatters,
  formatters = { djlint = { prepend_args = { "--stdin-filename", "$FILENAME" } } },
})
local lint = require("lint")
lint.linters_by_ft = linters
vim.list_extend(lint.linters.djlint.args, {
  "--stdin-filename",
  function()
    return vim.api.nvim_buf_get_name(0)
  end,
})
```

### none-ls

- [Dépôt GitHub](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formatage](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### coc.nvim

- [Paquet npm](https://www.npmjs.com/package/coc-htmldjango)

## IDE JetBrains

Dans PyCharm et les autres IDE basés sur IntelliJ, utilisez le plugin gratuit [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) :

1. Installez LSP4IJ depuis le Marketplace.
1. Ouvrez la fenêtre d'outils LSP Consoles et ajoutez un nouveau serveur de langage.
1. Dans l'onglet **Server**, définissez le nom `djLint` et la commande `djlint --lsp`, avec le chemin complet du `djlint` de l'environnement virtuel du projet s'il n'est pas dans le PATH.
1. Dans l'onglet **Mappings**, ajoutez les motifs de nom de fichier de vos templates. Si la configuration du projet n'a pas de [profil](/fr/docs/configuration/#profile), l'identifiant de langage de chaque motif le choisit :

   | Motifs                                | Identifiant de langage              |
   | ------------------------------------- | ----------------------------------- |
   | `*.html`, `*.htm`                     | `html`, ou `htmldjango` pour Django |
   | `*.jinja`, `*.jinja2`, `*.j2`         | `jinja`                             |
   | `*.njk`, `*.twig`                     | `nunjucks`                          |
   | `*.hbs`, `*.handlebars`, `*.mustache` | `handlebars`                        |
   | `*.liquid`                            | `liquid`                            |
   | `*.gotmpl`, `*.gohtml`                | `gotmpl`                            |
   | `*.tera`                              | `tera`                              |
   | `*.mako`                              | `mako`                              |

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

Installez SublimeLinter et [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) avec Package Control. djLint doit se trouver dans le PATH que voit Sublime Text.

## Helix

Helix peut exécuter le [serveur de langage](#serveur-de-langage) depuis `languages.toml`. Une liste `language-servers` remplace celle que Helix a pour ce langage, gardez donc ses propres serveurs après `djlint` :

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server", "superhtml"]

[[language]]
name = "htmldjango"
language-servers = ["djlint", "djlsp", "vscode-html-language-server", "superhtml"]

[[language]]
name = "gotmpl"
language-servers = ["djlint", "gopls"]

[[language]]
name = "jinja"
language-servers = ["djlint"]

[[language]]
name = "nunjucks"
language-servers = ["djlint"]

[[language]]
name = "twig"
language-servers = ["djlint"]

[[language]]
name = "tera"
language-servers = ["djlint"]
```

Helix n'ouvre de lui-même aucun fichier en `htmldjango`. Dans un projet Django, ajoutez `file-types = ["html"]` à cette entrée dans le `.helix/languages.toml` du projet.

## Emacs

Eglot, fourni avec Emacs 29 et plus récent :

```elisp
(with-eval-after-load 'eglot
  (dolist (mode '(html-mode mhtml-mode web-mode jinja2-mode twig-mode
                  handlebars-mode mustache-mode))
    (add-to-list 'eglot-server-programs `(,mode . ("djlint" "--lsp")))))
```

Exécutez ensuite `M-x eglot` dans un template. `eglot-format-buffer` le formate. `html-mode`, `mhtml-mode` et `web-mode` n'indiquent aucun langage de templates : le profil y vient donc de la [configuration](/fr/docs/configuration/#profile) du projet.

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

`--sarif` écrit un document SARIF 2.1.0 sur stdout et rien d'autre, ce qui permet de le rediriger comme ci-dessus. Chaque règle activée y figure avec un lien vers sa documentation, chaque signalement indique sa ligne et sa colonne, et avec `--check`, un fichier qui serait reformaté est signalé sous une règle `formatting`.

## pre-commit

djLint peut servir de hook [pre-commit](https://pre-commit.com), à la fois comme linter et comme formateur.

Ces profils ont chacun un hook qui linte, listé ici, et un qui formate, du même nom avec `reformat` : `djlint-reformat-django` pour `djlint-django`. Ils définissent `--profile` et les fichiers que pre-commit transmet. `angular` n'a pas de hooks à lui : ajoutez `args: [--profile=angular]` à `djlint` ou `djlint-reformat`.

| Hook                | Profil     | Fichiers                             |
| ------------------- | ---------- | ------------------------------------ |
| `djlint`            | aucun      | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django     | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja      | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks   | `.njk`                               |
| `djlint-handlebars` | handlebars | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid     | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang     | `.gotmpl`                            |
| `djlint-tera`       | tera       | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama     | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako       | `.html`, `.htm`, `.xhtml`            |

Pour des templates avec d'autres extensions, remplacez `files` dans votre configuration, et aussi `types_or` là où le hook le définit, car pre-commit exige que les deux correspondent. Voir la [documentation de pre-commit](https://pre-commit.com/#pre-commit-configyaml---hooks).

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

[MegaLinter](https://megalinter.io) inclut djLint. Lancez `npx mega-linter-runner --install` pour le mettre en place, et consultez [sa page sur djLint](https://megalinter.io/latest/descriptors/html_djlint/) pour les options.
