---
description: djLint をお気に入りのエディターと連携させましょう。pre-commit でテンプレートを自動フォーマットし、SublimeText でリントします。
title: 連携
keywords: テンプレート リンター, テンプレート フォーマッター, djLint, HTML, テンプレート, フォーマッター, リンター, 連携, 言語サーバー, lsp, neovim, helix
---

# 連携

djLint 向けに作られたエディター連携がいくつかあります。

どのエディターを使う場合も、djLint はエディターが見つけられる場所、できればプロジェクトの仮想環境にインストールし、その環境からエディターを起動するか、その環境の `djlint` をエディターに指定してください。そうすれば、エディターはプロジェクトで固定したバージョンを実行し、pre-commit フックや CI と同じ結果が得られます。

## Visual Studio Code

[djLint 拡張機能](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)をインストールしてください。VSCodium では [Open VSX 版](https://open-vsx.org/extension/monosans/djlint)を使います。この拡張機能は環境内の djLint を見つけ、見つからなければ同梱の djLint を使い、djLint が言語サーバーに対応していればそれを使います。

ソースコードは [GitHub](https://github.com/djlint/djlint-vscode) にあります。

## Neovim

djLint は Neovim でリンターとフォーマッターとして使えます。

### 組み込みの LSP クライアント（推奨）

Neovim 0.11 以降は、プラグインなしで djLint の[言語サーバー](#言語サーバー)と直接やり取りできます。入力中に検出結果が範囲の下線付きで表示され、`vim.lsp.buf.format()` でフォーマットできます：

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

保存時にフォーマットするには、同じ設定に次を追加します：

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

[設定](#設定)を参照してください。

### conform.nvim と nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) はフォーマットを、[nvim-lint](https://github.com/mfussenegger/nvim-lint) はリントを、djLint をコマンドとして実行して行います。検出結果には範囲の下線が付かず、nvim-lint にリントを指示したときにだけ表示されます。

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

::: content

- [GitHub リポジトリ](https://github.com/nvimtools/none-ls.nvim)
- [リント](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [フォーマット](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)
  :::

### efm-langserver

::: content

- [GitHub リポジトリ](https://github.com/mattn/efm-langserver)

1. Mason で `:MasonInstall efm djlint` を実行して、efm-langserver と djLint をインストールします。
1. `filetypes` に `htmldjango` を追加します。
1. フォーマットの設定を作成します：

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. `htmldjango = { djlint }` で言語とフォーマッターを結び付けます。

設定例：

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

### coc.nvim

::: content

- [npm パッケージ](https://www.npmjs.com/package/coc-htmldjango)
  :::

## JetBrains の IDE

PyCharm やその他の IntelliJ ベースの IDE では、無料の [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) プラグインを使います：

1. Marketplace から LSP4IJ をインストールします。
1. LSP Consoles ツールウィンドウを開き、新しい言語サーバーを追加します。
1. **Server** タブで、名前を `djLint`、コマンドを `djlint --lsp` に設定します。`djlint` が PATH 上にない場合は、プロジェクトの仮想環境にある `djlint` のフルパスを指定します。
1. **Mappings** タブで、`*.html` などテンプレートのファイル名パターンを追加します。プロジェクトの設定に[プロファイル](/ja/docs/configuration/#profile)がない場合、Django プロジェクトでは正しいプロファイルが選ばれるように、言語 ID を `htmldjango` に設定します。
1. **Configuration** タブでは、[設定](#設定)を `djlint` キーの下に JSON で指定できます。

検出結果がエディターに表示され、マッピングしたファイルでは **Reformat Code** がこのサーバーを使えるようになります。

## Sublime Text

### LSP（推奨）

[LSP](https://packagecontrol.io/packages/LSP) パッケージは[言語サーバー](#言語サーバー)を実行し、入力中の検出結果の表示とフォーマットを提供します。

**Preferences: LSP Server Configurations** を実行し、次を追加します：

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

djLint は SublimeText のリンタープラグインとして使えます。[package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) からインストールできます。

::: content

1. `cmd + shift + p`
2. SublimeLinter をインストール
3. SublimeLinter-contrib-djlint をインストール
   :::

djLint がグローバルの Python か、`PATH` 上にインストールされていることを確認してください。

## Helix

Helix は `languages.toml` から[言語サーバー](#言語サーバー)を実行できます：

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Emacs 29 以降に付属している Eglot を使います：

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

あとはテンプレートで `M-x eglot` を実行します。`eglot-format-buffer` でフォーマットできます。

## 言語サーバー

`djlint --lsp` は、djLint を stdio 経由の言語サーバーとして実行します。起動したまま動き続けるため、エディターは入力中に検出結果を受け取り、毎回プロセスを起動することなくドキュメントをフォーマットできます。

検出結果を報告し、ドキュメント全体をフォーマットします。追加のパッケージは必要ありません。LSP に対応したほかのエディターでも、同じコマンドで実行できます。

### 設定

サーバーは、コマンドラインと同じように、各ファイルのフォルダーから上に向かってプロジェクトの[設定](/ja/docs/configuration/)を読み込みます。エディターの設定はそれよりも優先されますが、コマンドラインと同様に、オプションを有効にするか値を設定することしかできません。`false` を指定しても、プロジェクトで有効にしたものは無効になりません。設定名には[コマンドラインオプション](/ja/docs/configuration/)の名前をアンダースコア区切りかキャメルケースで使い、カンマ区切りの値にはリストを使えます：

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

サーバーは `workspace/configuration` で `djlint` セクションを要求します。これに応答できないエディターは、同じキーを `initializationOptions` で送れます。

次の 2 つの設定には、対応するコマンドラインオプションがありません：

- `use_editor_indentation`：`indent` の代わりにエディターのタブサイズでフォーマットします。
- `python_rules`：`false` にすると `python_module` を持つカスタムルールをスキップし、プロジェクトのコードが実行されるのを防ぎます。

djLint は、次のうち `profile` を持つ最初のものから `profile` を取得します：

1. エディターの設定。
1. プロジェクトの設定。
1. ドキュメントの言語。たとえば `htmldjango` では `django` プロファイルが使われます。

どれにもない場合は、コマンドラインと同じようにプロファイルなしで実行されます。プロジェクトの設定に `profile` を書くのがもっとも簡単です。どのエディターでも機能し、言語 ID を設定する必要もありません。

### 動作

- 検出結果は、入力が少し止まったあとに届きます。プル型の診断に対応したエディターは自分から要求し、それ以外のエディターにはサーバーからプッシュされます。
- `exclude`、`extend_exclude`、`use_gitignore` は開いているドキュメントにも適用されます。除外されたドキュメントには検出結果がなく、フォーマットもされません。
- エディターがファイルを監視できる場合は、`pyproject.toml`、`djlint.toml`、`.djlint.toml`、`.djlintrc`、`.djlint_rules.yaml`、`.editorconfig`、`.gitignore` が変更されたときに設定を再読み込みします。監視できない場合は、ドキュメントを開いたときや保存したときに再読み込みします。`configuration` や `rules` で指定したファイルは、ドキュメントを開いたときや保存したときに読み込み直されます。カスタムルールの `python_module` のコードを変更した場合は、再起動が必要です。
- サーバーは一度に 1 つの処理しか行わないため、遅いルールがあるとその後の処理が待たされます。

## GitHub Actions

GitHub Actions のワークフローでは、djLint は各検出結果をアノテーションとして報告するため、プルリクエストの差分上にインラインで表示されます。設定は必要ありません。djLint はワークフローを検出して、自動的に出力を切り替えます。

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

通常のコンソール出力にするには `--no-github-output` を、Actions の外でもアノテーションを強制するには `--github-output` を使います。

アノテーションは 1 つのプルリクエストにしか属しません。実行をまたいだ履歴とともに検出結果をリポジトリの Security タブに残すには、SARIF として書き出してファイルをアップロードします：

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

アップロードのステップには、ジョブかワークフローに `security-events: write` 権限が必要です。

`--sarif` は SARIF 2.1.0 ドキュメントだけを標準出力に書き出すため、上のようにリダイレクトできます。有効なルールはすべてドキュメントへのリンク付きで一覧され、各検出結果には行と列が含まれます。また `--check` と組み合わせると、再フォーマットされるファイルが `formatting` ルールとして報告されます。Azure DevOps、GitLab、そしてほとんどのエディターが同じ形式を読み込めます。

## Pre-Commit

djLint は [pre-commit](https://pre-commit.com) フックとして、リンターとしてもフォーマッターとしても使えます。

リポジトリには、djLint の各プロファイル向けに設定済みのフックが複数用意されています（`--profile` 引数を事前に設定し、対象とするファイル拡張子を pre-commit に伝えるだけのものです）：

::: content

- リント用の `djlint` とフォーマット用の `djlint-reformat`
  `--profile` を設定せずに、`*.html` に一致するファイルを対象とします。
- `djlint-django` と `djlint-reformat-django`
  `*.html` に一致するファイルを対象とし、`--profile=django` を設定します。
- `djlint-jinja` と `djlint-reformat-jinja`
  `*.j2`、`*.jinja`、`*.jinja2` に一致するファイルを対象とし、`--profile=jinja` を設定します。
- `djlint-nunjucks` と `djlint-reformat-nunjucks`
  `*.njk` に一致するファイルを対象とし、`--profile=nunjucks` を設定します。
- `djlint-handlebars` と `djlint-reformat-handlebars`
  `*.hbs` に一致するファイルを対象とし、`--profile=handlebars` を設定します。
- `djlint-liquid` と `djlint-reformat-liquid`
  `*.html` に一致するファイルを対象とし、`--profile=liquid` を設定します。
- `djlint-golang` と `djlint-reformat-golang`
  `*.gotmpl` に一致するファイルを対象とし、`--profile=golang` を設定します。
- `djlint-tera` と `djlint-reformat-tera`
  `*.html` に一致するファイルを対象とし、`--profile=tera` を設定します。
- `djlint-askama` と `djlint-reformat-askama`
  `*.html` に一致するファイルを対象とし、`--profile=askama` を設定します。
  :::

これらの定義済みフックは、受け付ける入力の点で保守的すぎることがあります（テンプレートで別の拡張子を使っている場合など）。そのため pre-commit では、定義済みのオプションをどれでも明示的に上書きできます。その他の設定については [pre-commit のドキュメント](https://pre-commit.com/#pre-commit-configyaml---hooks)を参照してください。

### デフォルトの Django の例

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### .hbs ではなく .html 拡張子を使う Handlebars

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

`files` や `exclude` パラメーターを使うと各フックの対象をそれぞれのディレクトリに限定できるため、同じリポジトリで複数のテンプレート言語をサポートできます。

## MegaLinter

djlint は [MegaLinter](https://megalinter.io) の 100 以上のリンターにネイティブに組み込まれています。

インストールするには、`npx mega-linter-runner --install` を実行して指示に従うだけです。

::: content

- [GitHub リポジトリ](https://github.com/oxsecurity/megalinter)
- [MegaLinter ドキュメントの djlint](https://megalinter.io/latest/descriptors/html_djlint/)
  :::
