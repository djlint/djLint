---
title: "整合"
description: "在編輯器中使用 djLint，並透過 pre-commit 執行它。"
sidebar:
  label: "整合"
---

djLint 有好幾種編輯器整合。

無論你使用哪種編輯器，都請將 djLint 安裝在編輯器找得到的地方，最好是專案的虛擬環境中，然後從該環境啟動編輯器，或讓編輯器指向該環境中的 `djlint`。這樣編輯器執行的就是專案鎖定的版本，結果會與你的 pre-commit hook 或 CI 相同。

## Visual Studio Code

安裝 [djLint 擴充功能](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)，若使用 VSCodium 則安裝 [Open VSX 上的版本](https://open-vsx.org/extension/monosans/djlint)。它會在你的環境中尋找 djLint，找不到時改用內建的版本，並在你的 djLint 支援時使用語言伺服器。

它的程式碼位於 [GitHub](https://github.com/djlint/djlint-vscode)。

## Neovim

djLint 可以在 Neovim 中作為 linter 和格式化工具使用。

### 內建 LSP 用戶端（建議使用）

Neovim 0.11 或更新版本不需要任何外掛，就能直接與 djLint 的[語言伺服器](#語言伺服器)溝通。這樣可以在輸入時取得檢查結果，並以底線標示範圍，還能用 `vim.lsp.buf.format()` 進行格式化：

```lua
vim.lsp.config("djlint", {
  cmd = { "djlint", "--lsp" },
  filetypes = { "html", "htmldjango", "jinja", "jinja.html", "handlebars", "liquid", "gotmpl" },
  root_markers = { "pyproject.toml", "djlint.toml", ".djlint.toml", ".djlintrc", ".git" },
})
vim.lsp.enable("djlint")
```

若要在儲存時格式化，請在同一份設定中加入：

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

請參閱[設定](#設定)。

### conform.nvim 和 nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) 負責格式化，[nvim-lint](https://github.com/mfussenegger/nvim-lint) 負責 lint，兩者都是以指令的方式執行 djLint。檢查結果不會以底線標示範圍，而且只有在你要求 nvim-lint 進行 lint 時才會出現。

```lua
require("conform").setup({ formatters_by_ft = { htmldjango = { "djlint" } } })
require("lint").linters_by_ft = { htmldjango = { "djlint" } }
```

### none-ls

- [GitHub 儲存庫](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [格式化](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### efm-langserver

- [GitHub 儲存庫](https://github.com/mattn/efm-langserver)

1. 透過 Mason 執行 `:MasonInstall efm djlint`，安裝 efm-langserver 和 djLint
1. 將 `htmldjango` 加入 `filetypes`。
1. 建立格式化設定：

```lua
local djlint = {
    formatCommand = "djlint --reformat --quiet --warn -",
    formatStdin = true,
}
```

1. 以 `htmldjango = { djlint }` 將語言與格式化工具連結起來。

設定範例：

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

- [npm 套件](https://www.npmjs.com/package/coc-htmldjango)

## JetBrains IDE

在 PyCharm 和其他以 IntelliJ 為基礎的 IDE 中，請使用免費的 [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) 外掛：

1. 從 Marketplace 安裝 LSP4IJ。
1. 開啟 LSP Consoles 工具視窗，新增一個語言伺服器。
1. 在 **Server** 分頁中，將名稱設為 `djLint`，指令設為 `djlint --lsp`；如果它不在 PATH 上，請使用專案虛擬環境中 `djlint` 的完整路徑。
1. 在 **Mappings** 分頁中，為你的範本新增檔案名稱模式，例如 `*.html`。如果專案的設定沒有指定 [profile](/zh-tw/docs/configuration/#profile)，請為 Django 專案將語言 ID 設為 `htmldjango`，以便選用正確的 profile。
1. 在 **Configuration** 分頁中，你可以在 `djlint` 鍵底下以 JSON 指定[設定](#設定)。

檢查結果會顯示在編輯器中，而 **Reformat Code** 可以對對應的檔案使用這個伺服器。

## Sublime Text

### LSP（建議使用）

[LSP](https://packagecontrol.io/packages/LSP) 套件會執行[語言伺服器](#語言伺服器)，提供輸入時的檢查結果與格式化功能。

執行 **Preferences: LSP Server Configurations** 並加入：

```json
{ "djlint": { "enabled": true, "command": ["djlint", "--lsp"], "selector": "text.html" } }
```

### SublimeLinter

djLint 可以作為 SublimeText 的 Linter 外掛使用。可以透過 [package-control](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint) 安裝。

1. `cmd + shift + p`
2. 安裝 SublimeLinter
3. 安裝 SublimeLinter-contrib-djlint

請確認 djLint 已安裝在全域的 Python 中，或位於你的 `PATH` 上。

## Helix

Helix 可以透過 `languages.toml` 執行[語言伺服器](#語言伺服器)：

```toml
[language-server.djlint]
command = "djlint"
args = ["--lsp"]

[[language]]
name = "html"
language-servers = ["djlint", "vscode-html-language-server"]
```

## Emacs

Emacs 29 及更新版本內建的 Eglot：

```elisp
(with-eval-after-load 'eglot
  (add-to-list 'eglot-server-programs
               '((html-mode web-mode) . ("djlint" "--lsp"))))
```

接著在範本中執行 `M-x eglot`。`eglot-format-buffer` 會將它格式化。

## 語言伺服器

`djlint --lsp` 會以語言伺服器的形式透過 stdio 執行 djLint。它會持續執行，因此編輯器能在你輸入時取得檢查結果，並在格式化文件時不必每次都啟動新的處理程序。

它會回報檢查結果，並格式化整份文件。它不需要額外的套件。任何支援 LSP 的其他編輯器，都能以相同的指令執行它。

### 設定

伺服器讀取專案[設定](/zh-tw/docs/configuration/)的方式與命令列相同，會從每個檔案所在的資料夾往上層尋找。編輯器的設定優先於專案設定，但就像在命令列上一樣，它們只能開啟選項或設定值：`false` 不會關閉專案已開啟的選項。設定使用[命令列選項](/zh-tw/docs/configuration/)的名稱，可以用底線連接或寫成 camelCase，而以逗號分隔的值可以改用清單表示：

```lua
vim.lsp.config("djlint", {
  settings = { djlint = { profile = "django", ignore = { "H013", "H016" } } },
})
```

伺服器會透過 `workspace/configuration` 要求 `djlint` 區段。無法回應這項要求的編輯器，可以改在 `initializationOptions` 中傳送相同的鍵。

有兩個設定沒有對應的命令列選項：

- `use_editor_indentation`：使用編輯器的 Tab 大小進行格式化，而不使用 `indent`。
- `python_rules`：設為 `false` 可略過帶有 `python_module` 的自訂規則，避免執行專案的程式碼。

djLint 會從下列來源中，取第一個有指定 `profile` 的來源：

1. 編輯器的設定。
1. 專案的設定。
1. 文件的語言：例如 `htmldjango` 會使用 `django` profile。

如果都沒有指定，它就會像在命令列上一樣，不使用任何 profile 執行。在專案的設定中指定 `profile` 是最簡單的做法：它在每個編輯器中都有效，而且不需要設定語言 ID。

### 運作方式

- 檢查結果會在你停止輸入片刻後出現。支援 pull diagnostics 的編輯器會主動要求結果，其他編輯器則會收到伺服器推送的結果。
- `exclude`、`extend_exclude` 和 `use_gitignore` 會套用到已開啟的文件。被排除的文件不會有檢查結果，也不會被格式化。
- 當 `pyproject.toml`、`djlint.toml`、`.djlint.toml`、`.djlintrc`、`.djlint_rules.yaml`、`.editorconfig` 或 `.gitignore` 變更時，如果編輯器能監看檔案，它就會重新載入設定；否則會在開啟或儲存文件時重新載入。由 `configuration` 或 `rules` 指定的檔案，會在開啟或儲存文件時重新讀取。自訂規則的 `python_module` 程式碼有變更時，需要重新啟動。
- 執行緩慢的規則會拖慢之後的所有處理，因為伺服器一次只做一件事。

## GitHub Actions

在 GitHub Actions 工作流程中，djLint 會將每個檢查結果回報為註記（annotation），讓它直接顯示在 pull request 的 diff 中。不需要任何設定：djLint 會偵測到工作流程並自動切換輸出方式。

```yaml
- run: pip install djlint
- run: djlint . --lint --profile django
```

使用 `--no-github-output` 可改為取得一般的主控台輸出，或使用 `--github-output` 在 Actions 以外的環境強制輸出註記。

註記只屬於單一個 pull request。若要將檢查結果保留在儲存庫的 Security 分頁中，並保有跨多次執行的歷史記錄，請將結果寫成 SARIF 並上傳該檔案：

```yaml
- run: djlint . --lint --sarif > djlint.sarif
  continue-on-error: true
- uses: github/codeql-action/upload-sarif@v4
  with:
    sarif_file: djlint.sarif
```

上傳步驟需要在 job 或工作流程上設定 `security-events: write` 權限。

`--sarif` 會將 SARIF 2.1.0 文件寫到 stdout，且只輸出這份文件，因此可以如上所示重新導向。每條已啟用的規則都會附上其說明文件的連結，每個檢查結果都帶有行號與欄號；搭配 `--check` 時，需要重新格式化的檔案會以 `formatting` 規則回報。Azure DevOps、GitLab 和大多數編輯器都能讀取相同的格式。

## Pre-Commit

djLint 可以作為 [pre-commit](https://pre-commit.com) hook 使用，同時擔任 linter 和格式化工具。

這個儲存庫為特定的 djLint profile 提供了多個預先設定好的 hook（它只是預先設定 `--profile` 引數，並告訴 pre-commit 要尋找哪些副檔名）：

- `djlint` 用於 lint，`djlint-reformat` 用於格式化
  這會尋找符合 `*.html` 的檔案，且不設定 `--profile`。
- `djlint-django` 和 `djlint-reformat-django`
  這會尋找符合 `*.html` 的檔案，並設定 `--profile=django`。
- `djlint-jinja` 和 `djlint-reformat-jinja`
  這會尋找符合 `*.j2`、`*.jinja` 或 `*.jinja2` 的檔案，並設定 `--profile=jinja`。
- `djlint-nunjucks` 和 `djlint-reformat-nunjucks`
  這會尋找符合 `*.njk` 的檔案，並設定 `--profile=nunjucks`。
- `djlint-handlebars` 和 `djlint-reformat-handlebars`
  這會尋找符合 `*.hbs` 的檔案，並設定 `--profile=handlebars`。
- `djlint-liquid` 和 `djlint-reformat-liquid`
  這會尋找符合 `*.html` 的檔案，並設定 `--profile=liquid`。
- `djlint-golang` 和 `djlint-reformat-golang`
  這會尋找符合 `*.gotmpl` 的檔案，並設定 `--profile=golang`。
- `djlint-tera` 和 `djlint-reformat-tera`
  這會尋找符合 `*.html` 的檔案，並設定 `--profile=tera`。
- `djlint-askama` 和 `djlint-reformat-askama`
  這會尋找符合 `*.html` 的檔案，並設定 `--profile=askama`。
- `djlint-mako` 和 `djlint-reformat-mako`
  這會尋找符合 `*.html` 的檔案，並設定 `--profile=mako`。

請注意，這些預先定義的 hook 對接受的輸入有時過於保守（你的範本可能使用不同的副檔名），因此 pre-commit 明確允許你覆寫任何預先定義的選項。其他設定方式請參閱 [pre-commit 說明文件](https://pre-commit.com/#pre-commit-configyaml---hooks)。

### 預設的 Django 範例

```yaml
repos:
  - repo: https://github.com/djlint/djLint
    rev: v{{ djlint_version }}
    hooks:
      - id: djlint-reformat-django
      - id: djlint-django
```

### 使用 .html 副檔名而非 .hbs 的 Handlebars

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

你可以使用 `files` 或 `exclude` 參數，將每個 hook 限制在各自的目錄中，讓同一個儲存庫能支援多種範本語言。

## MegaLinter

djlint 原生內建於 [MegaLinter](https://megalinter.io) 的 100 多個 linter 之中

若要安裝，只要執行 `npx mega-linter-runner --install` 並依照指示操作即可

- [GitHub 儲存庫](https://github.com/oxsecurity/megalinter)
- [MegaLinter 說明文件中的 djlint](https://megalinter.io/latest/descriptors/html_djlint/)
