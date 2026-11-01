---
description: Intégrez djLint avec votre éditeur préféré. Formatez automatiquement vos modèles avec Pre-Commit. Lint avec SublimeText.
title: Intégrations
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, intégrations
---

# {{ "integrations" | i18n }}

Il existe plusieurs intégrations d'éditeurs construites pour djLint.

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

::: content

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
  :::

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

## Linter SublimeText

djLint peut être utilisé comme un plugin SublimeText Linter. Il peut être installé via [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint).

::: content

1. `cmd + shift + p`
2. Installer SublimeLinter
3. Installer SublimeLinter-contrib-djlint
   :::

Assurez-vous que djLint est installé dans votre python global, ou sur votre `PATH`.

## Visual Studio Code

::: content

- [GitHub dépôt](https://github.com/djlint/djlint-vscode)
- [Page sur VS Marketplace](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)
- [Page sur Open VSX](https://open-vsx.org/extension/monosans/djlint)
  :::

## neovim

djLint peut être utilisé comme linter et formateur dans neovim.

Neovim 0.11 ou plus récent peut parler directement au [serveur de langage](/fr/docs/language-server/) de djLint, sans plugin. Vous obtenez les erreurs pendant la saisie, avec leur étendue soulignée, et le formatage avec `vim.lsp.buf.format()` :

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

Voir [Serveur de langage](/fr/docs/language-server/#reglages) pour les réglages. Les plugins ci-dessous lancent djLint comme une commande.

Avec le plugin `none-ls`.

::: content

- [GitHub dépôt](https://github.com/nvimtools/none-ls.nvim)
- [Linting](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [Formatage](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)
  :::

Avec `coc.nvim`.

::: content

- [npm package](https://www.npmjs.com/package/coc-htmldjango)
  :::

Avec `efm-langserver`.

::: content

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

:::

## Zed

Installez l'[extension djLint](https://github.com/djlint/zed-djlint), qui lance le [serveur de langage](/fr/docs/language-server/).

## Helix

Helix lance le [serveur de langage](/fr/docs/language-server/) depuis `languages.toml` :

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["vscode-html-language-server", "djlint"]
```

## MegaLinter

djLint est intégré nativement parmi les plus de 100 linters de [MegaLinter](https://megalinter.io).

Pour l'installer, lancez `npx mega-linter-runner --install` et suivez les instructions.

::: content

- [GitHub dépôt](https://github.com/oxsecurity/megalinter)
- [djlint dans la documentation de MegaLinter](https://megalinter.io/latest/descriptors/html_djlint/)
  :::
