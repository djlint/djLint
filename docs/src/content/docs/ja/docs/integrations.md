---
title: "連携"
description: "エディターで djLint を使い、pre-commit で実行します。"
---

どのエディターを使う場合も、djLint はエディターが見つけられる場所、できればプロジェクトの仮想環境にインストールし、その環境からエディターを起動するか、その環境の `djlint` をエディターに指定してください。そうすれば、エディターはプロジェクトで固定したバージョンを実行し、pre-commit フックや CI と同じ結果が得られます。

プロジェクトで djLint を [npm](/ja/docs/getting-started/#インストール) でインストールしている場合、コマンドはプロジェクト内の `node_modules/.bin/djlint`（Windows では `node_modules\.bin\djlint.cmd`）です。以下のエディターで `djlint` を実行する箇所には、このパスを指定してください。VS Code と Zed の拡張機能は自動で見つけます。

## Visual Studio Code

Visual Studio Marketplace から [djLint 拡張機能](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)をインストールしてください。Cursor、Windsurf、VSCodium など VS Code ベースのエディターでは、[同じ拡張機能を Open VSX から](https://open-vsx.org/extension/monosans/djlint)インストールします。この拡張機能は環境内の djLint を見つけ、見つからなければ同梱の djLint を使い、djLint が言語サーバーに対応していればそれを使います。

[README](https://github.com/djlint/djlint-vscode#readme) では、設定と、どの djLint を実行するかを説明しています。

## Zed

[djLint 拡張機能](https://github.com/djlint/djlint-zed)は、HTML と、Django、Jinja、Twig などのテンプレート拡張機能の言語で[言語サーバー](#言語サーバー)を実行します。まだ Zed の拡張機能レジストリには登録されていないため、開発用拡張機能としてインストールします：

1. [rustup](https://rustup.rs) で Rust をインストールします。Zed はこれで拡張機能をビルドし、`wasm32-wasip2` ターゲットも自動で追加します。Homebrew や Nix など別の方法で入れた Rust では、このターゲットを自分で追加してください。
1. 拡張機能をクローンします：

   ```bash
   git clone https://github.com/djlint/djlint-zed
   ```

1. Zed でコマンドパレットを開き（macOS では `cmd-shift-p`、それ以外では `ctrl-shift-p`）、**zed: install dev extension** を実行して、クローンした `djlint-zed` フォルダーを選びます。

更新するには、そのフォルダーで `git pull` を実行してから **zed: rebuild dev extension** を実行します。

PATH 上またはプロジェクトに npm でインストールした djLint 1.49 以降か、djLint をインストールせずに実行できる [uv](https://docs.astral.sh/uv/) が必要です。言語のフォーマッターに指定する方法と設定については、[README](https://github.com/djlint/djlint-zed#readme) で説明しています。

## Neovim

Neovim はテンプレートの拡張子の一部にファイルタイプを割り当てません。下のどの方法を使う場合も、先に登録してください：

```lua
vim.filetype.add({
  extension = {
    gohtml = "gotmpl", gotmpl = "gotmpl", handlebars = "handlebars",
    j2 = "jinja", jinja2 = "jinja", mako = "mako", njk = "nunjucks",
  },
})
```

### 組み込みの LSP クライアント（推奨）

Neovim 0.11 以降は、プラグインなしで djLint の[言語サーバー](#言語サーバー)と直接やり取りできます。入力中に検出結果が範囲の下線付きで表示され、`vim.lsp.buf.format()` でフォーマットできます。

v2.12.0 より新しい [nvim-lspconfig](https://github.com/neovim/nvim-lspconfig) には設定が含まれているので、導入済みなら 1 行で足ります：

```lua
vim.lsp.enable("djlint")
```

プロジェクトに npm で djLint をインストールしている場合は、この行の前に `vim.lsp.config("djlint", { cmd = { "node_modules/.bin/djlint", "--lsp" } })` を書いてください。

nvim-lspconfig を使わない場合や古い版の場合は、設定を自分で定義します：

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

保存時にフォーマットするには、同じ設定に次を追加します：

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

[設定](#設定)を参照してください。

### conform.nvim と nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) はフォーマットを、[nvim-lint](https://github.com/mfussenegger/nvim-lint) はリントを、djLint をコマンドとして実行して行います。検出結果には範囲の下線が付かず、nvim-lint にリントを指示したときにだけ表示されます。プロファイルは、コマンドラインと同じくプロジェクトの[設定](/ja/docs/configuration/#profile)から決まります。この例には djLint 1.49 以降が必要です。

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

- [GitHub リポジトリ](https://github.com/nvimtools/none-ls.nvim)
- [リント](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [フォーマット](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### coc.nvim

- [npm パッケージ](https://www.npmjs.com/package/coc-htmldjango)

## JetBrains の IDE

PyCharm やその他の IntelliJ ベースの IDE では、無料の [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) プラグインを使います：

1. Marketplace から LSP4IJ をインストールします。
1. LSP Consoles ツールウィンドウを開き、新しい言語サーバーを追加します。
1. **Server** タブで、名前を `djLint`、コマンドを `djlint --lsp` に設定します。`djlint` が PATH 上にない場合は、プロジェクトの仮想環境にある `djlint` のフルパスを指定します。
1. **Mappings** タブで、テンプレートのファイル名パターンを追加します。プロジェクトの設定に[プロファイル](/ja/docs/configuration/#profile)がない場合は、パターンごとの言語 ID でプロファイルが選ばれます：

   | パターン                              | 言語 ID                          |
   | ------------------------------------- | -------------------------------- |
   | `*.html`, `*.htm`                     | `html`、Django では `htmldjango` |
   | `*.jinja`, `*.jinja2`, `*.j2`         | `jinja`                          |
   | `*.njk`, `*.twig`                     | `nunjucks`                       |
   | `*.hbs`, `*.handlebars`, `*.mustache` | `handlebars`                     |
   | `*.liquid`                            | `liquid`                         |
   | `*.gotmpl`, `*.gohtml`                | `gotmpl`                         |
   | `*.tera`                              | `tera`                           |
   | `*.mako`                              | `mako`                           |

1. **Configuration** タブでは、[設定](#設定)を `djlint` キーの下に JSON で指定できます。

検出結果がエディターに表示され、マッピングしたファイルでは **Reformat Code** がこのサーバーを使えるようになります。

## Sublime Text

### LSP（推奨）

[LSP](https://packagecontrol.io/packages/LSP) パッケージは[言語サーバー](#言語サーバー)を実行し、入力中の検出結果の表示とフォーマットを提供します。

**Preferences: LSP Server Configurations** を実行し、次を追加します：

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

Package Control で SublimeLinter と [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) をインストールします。djLint は Sublime Text から見える PATH 上に必要です。

## Helix

Helix は `languages.toml` から[言語サーバー](#言語サーバー)を実行できます。`language-servers` のリストは Helix がその言語に持つリストを置き換えるので、`djlint` の後に Helix 自身のサーバーを残してください：

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

Helix は自分ではどのファイルも `htmldjango` として開きません。Django プロジェクトでは、プロジェクトの `.helix/languages.toml` でこのエントリに `file-types = ["html"]` を追加してください。

## Emacs

Emacs 29 以降に付属している Eglot を使います：

```elisp
(with-eval-after-load 'eglot
  (dolist (mode '(html-mode mhtml-mode web-mode jinja2-mode twig-mode
                  handlebars-mode mustache-mode))
    (add-to-list 'eglot-server-programs `(,mode . ("djlint" "--lsp")))))
```

あとはテンプレートで `M-x eglot` を実行します。`eglot-format-buffer` でフォーマットできます。`html-mode`、`mhtml-mode`、`web-mode` はテンプレート言語を示さないため、これらではプロファイルはプロジェクトの[設定](/ja/docs/configuration/#profile)から決まります。

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

`--sarif` は SARIF 2.1.0 ドキュメントだけを標準出力に書き出すため、上のようにリダイレクトできます。有効なルールはすべてドキュメントへのリンク付きで一覧され、各検出結果には行と列が含まれます。また `--check` と組み合わせると、再フォーマットされるファイルが `formatting` ルールとして報告されます。

## pre-commit

djLint は [pre-commit](https://pre-commit.com) フックとして、リンターとしてもフォーマッターとしても使えます。

下の表のプロファイルには、それぞれ表に載っているリント用のフックと、フォーマット用のフックがあります。フォーマット用のフックは名前に `reformat` が入り、`djlint-django` なら `djlint-reformat-django` です。どちらも `--profile` と、pre-commit が渡すファイルを設定します。`angular` には専用のフックがないため、`djlint` か `djlint-reformat` に `args: [--profile=angular]` を指定してください。

| フック              | プロファイル | ファイル                             |
| ------------------- | ------------ | ------------------------------------ |
| `djlint`            | なし         | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django       | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja        | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks     | `.njk`                               |
| `djlint-handlebars` | handlebars   | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid       | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang       | `.gotmpl`                            |
| `djlint-tera`       | tera         | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama       | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako         | `.html`, `.htm`, `.xhtml`            |

ほかの拡張子のテンプレートでは、設定で `files` を上書きし、フックが `types_or` を設定している場合はそれも上書きします。pre-commit では両方に一致する必要があるためです。詳しくは [pre-commit のドキュメント](https://pre-commit.com/#pre-commit-configyaml---hooks)を参照してください。

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

[MegaLinter](https://megalinter.io) には djLint が含まれています。`npx mega-linter-runner --install` を実行するとセットアップでき、オプションは [MegaLinter の djLint のページ](https://megalinter.io/latest/descriptors/html_djlint/)にあります。
