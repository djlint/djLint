---
title: "整合"
description: "在編輯器中使用 djLint，並透過 pre-commit 執行它。"
---

無論你使用哪種編輯器，都請將 djLint 安裝在編輯器找得到的地方，最好是專案的虛擬環境中，然後從該環境啟動編輯器，或讓編輯器指向該環境中的 `djlint`。這樣編輯器執行的就是專案鎖定的版本，結果會與你的 pre-commit hook 或 CI 相同。

如果專案用 [npm](/zh-tw/docs/getting-started/#安裝) 安裝 djLint，它的命令是專案中的 `node_modules/.bin/djlint`，在 Windows 上則是 `node_modules\.bin\djlint.cmd`。下面的編輯器中執行 `djlint` 的地方，請填入這個路徑。VS Code 和 Zed 的擴充功能會自己找到它。

## Visual Studio Code

從 Visual Studio Marketplace 安裝 [djLint 擴充功能](https://marketplace.visualstudio.com/items?itemName=monosans.djlint)。Cursor、Windsurf、VSCodium 等以 VS Code 為基礎的編輯器則從 [Open VSX 安裝同一個擴充功能](https://open-vsx.org/extension/monosans/djlint)。它會在你的環境中尋找 djLint，找不到時改用內建的版本，並在你的 djLint 支援時使用語言伺服器。

它的 [README](https://github.com/djlint/djlint-vscode#readme) 說明了它的設定，以及它會執行哪一個 djLint。

## Zed

[djLint 擴充功能](https://github.com/djlint/djlint-zed)會在 HTML 以及 Django、Jinja、Twig 等範本擴充功能的語言中執行[語言伺服器](#語言伺服器)。它還沒有列入 Zed 的擴充功能登錄庫，因此請以開發用擴充功能的方式安裝：

1. 透過 [rustup](https://rustup.rs) 安裝 Rust，Zed 會用它建置擴充功能，並自動加入 `wasm32-wasip2` 目標。如果 Rust 是用 Homebrew 或 Nix 等其他方式安裝，請自行加入這個目標。
1. 複製擴充功能：

   ```bash
   git clone https://github.com/djlint/djlint-zed
   ```

1. 在 Zed 中開啟命令面板（macOS 為 `cmd-shift-p`，其他系統為 `ctrl-shift-p`），執行 **zed: install dev extension**，並選擇複製下來的 `djlint-zed` 資料夾。

若要更新，請在該資料夾中執行 `git pull`，再執行 **zed: rebuild dev extension**。

需要 PATH 中或專案裡用 npm 安裝的 djLint 1.49 或更新版本，或是有 [uv](https://docs.astral.sh/uv/)，它不必安裝就能執行 djLint。它的 [README](https://github.com/djlint/djlint-zed#readme) 說明了如何將它設為某個語言的格式化工具，以及它的設定。

## Neovim

Neovim 不會替部分範本副檔名設定檔案類型。無論你使用下面哪種方式，都請先註冊它們：

```lua
vim.filetype.add({
  extension = {
    gohtml = "gotmpl", gotmpl = "gotmpl", handlebars = "handlebars",
    j2 = "jinja", jinja2 = "jinja", mako = "mako", njk = "nunjucks",
  },
})
```

### 內建 LSP 用戶端（建議使用）

Neovim 0.11 或更新版本不需要任何外掛，就能直接與 djLint 的[語言伺服器](#語言伺服器)溝通。這樣可以在輸入時取得檢查結果，並以底線標示範圍，還能用 `vim.lsp.buf.format()` 進行格式化：

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

若要在儲存時格式化，請在同一份設定中加入：

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

請參閱[設定](#設定)。

### conform.nvim 和 nvim-lint

[conform.nvim](https://github.com/stevearc/conform.nvim) 負責格式化，[nvim-lint](https://github.com/mfussenegger/nvim-lint) 負責 lint，兩者都是以指令的方式執行 djLint。檢查結果不會以底線標示範圍，而且只有在你要求 nvim-lint 進行 lint 時才會出現。profile 和命令列一樣，來自專案的[設定](/zh-tw/docs/configuration/#profile)。此範例需要 djLint 1.49 或更新版本。

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

- [GitHub 儲存庫](https://github.com/nvimtools/none-ls.nvim)
- [Lint](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint)
- [格式化](https://github.com/nvimtools/none-ls.nvim/blob/main/doc/BUILTINS.md#djlint-1)

### coc.nvim

- [npm 套件](https://www.npmjs.com/package/coc-htmldjango)

## JetBrains IDE

在 PyCharm 和其他以 IntelliJ 為基礎的 IDE 中，請使用免費的 [LSP4IJ](https://plugins.jetbrains.com/plugin/23257-lsp4ij) 外掛：

1. 從 Marketplace 安裝 LSP4IJ。
1. 開啟 LSP Consoles 工具視窗，新增一個語言伺服器。
1. 在 **Server** 分頁中，將名稱設為 `djLint`，指令設為 `djlint --lsp`；如果它不在 PATH 上，請使用專案虛擬環境中 `djlint` 的完整路徑。
1. 在 **Mappings** 分頁中，新增你的範本的檔案名稱模式。如果專案的設定沒有指定 [profile](/zh-tw/docs/configuration/#profile)，就由每個模式的語言 ID 選用 profile：

   | 模式                                  | 語言 ID                          |
   | ------------------------------------- | -------------------------------- |
   | `*.html`, `*.htm`                     | `html`，Django 中為 `htmldjango` |
   | `*.jinja`, `*.jinja2`, `*.j2`         | `jinja`                          |
   | `*.njk`, `*.twig`                     | `nunjucks`                       |
   | `*.hbs`, `*.handlebars`, `*.mustache` | `handlebars`                     |
   | `*.liquid`                            | `liquid`                         |
   | `*.gotmpl`, `*.gohtml`                | `gotmpl`                         |
   | `*.tera`                              | `tera`                           |
   | `*.mako`                              | `mako`                           |

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

使用 Package Control 安裝 SublimeLinter 和 [SublimeLinter-contrib-djlint](https://packagecontrol.io/packages/SublimeLinter-contrib-djlint)。djLint 必須位於 Sublime Text 所看到的 PATH 上。

## Helix

Helix 可以透過 `languages.toml` 執行[語言伺服器](#語言伺服器)。`language-servers` 清單會取代 Helix 為該語言設定的清單，所以請在 `djlint` 之後保留 Helix 自己的伺服器：

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

Helix 本身不會把任何檔案當作 `htmldjango` 開啟。在 Django 專案中，請在專案的 `.helix/languages.toml` 裡為這一項加上 `file-types = ["html"]`。

## Emacs

Emacs 29 及更新版本內建的 Eglot：

```elisp
(with-eval-after-load 'eglot
  (dolist (mode '(html-mode mhtml-mode web-mode jinja2-mode twig-mode
                  handlebars-mode mustache-mode))
    (add-to-list 'eglot-server-programs `(,mode . ("djlint" "--lsp")))))
```

接著在範本中執行 `M-x eglot`。`eglot-format-buffer` 會將它格式化。`html-mode`、`mhtml-mode` 和 `web-mode` 不會指出範本語言，因此在這些模式中，profile 來自專案的[設定](/zh-tw/docs/configuration/#profile)。

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

`--sarif` 會將 SARIF 2.1.0 文件寫到 stdout，且只輸出這份文件，因此可以如上所示重新導向。每條已啟用的規則都會附上其說明文件的連結，每個檢查結果都帶有行號與欄號；搭配 `--check` 時，需要重新格式化的檔案會以 `formatting` 規則回報。

## pre-commit

djLint 可以作為 [pre-commit](https://pre-commit.com) hook 使用，同時擔任 linter 和格式化工具。

下表中的每個 profile 都有一個用於 lint 的 hook（列於表中），以及一個用於格式化、名稱中多了 `reformat` 的 hook：例如 `djlint-django` 對應 `djlint-reformat-django`。這些 hook 會設定 `--profile`，以及 pre-commit 要傳入的檔案。`angular` 沒有專屬的 hook：請為 `djlint` 或 `djlint-reformat` 設定 `args: [--profile=angular]`。

| Hook                | Profile    | 檔案                                 |
| ------------------- | ---------- | ------------------------------------ |
| `djlint`            | 無         | `.html`, `.htm`, `.xhtml`            |
| `djlint-django`     | django     | `.html`, `.htm`, `.xhtml`            |
| `djlint-jinja`      | jinja      | `.j2`, `.jinja`, `.jinja2`           |
| `djlint-nunjucks`   | nunjucks   | `.njk`                               |
| `djlint-handlebars` | handlebars | `.hbs`, `.handlebars`, `.mustache`   |
| `djlint-liquid`     | liquid     | `.html`, `.htm`, `.xhtml`, `.liquid` |
| `djlint-golang`     | golang     | `.gotmpl`                            |
| `djlint-tera`       | tera       | `.html`, `.htm`, `.xhtml`            |
| `djlint-askama`     | askama     | `.html`, `.htm`, `.xhtml`            |
| `djlint-mako`       | mako       | `.html`, `.htm`, `.xhtml`            |

若範本使用其他副檔名，請在設定中覆寫 `files`；如果 hook 有設定 `types_or`，也要一併覆寫，因為 pre-commit 需要兩者都符合。請參閱 [pre-commit 說明文件](https://pre-commit.com/#pre-commit-configyaml---hooks)。

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

[MegaLinter](https://megalinter.io) 內建了 djLint。執行 `npx mega-linter-runner --install` 即可設定，選項請參閱[它的 djLint 頁面](https://megalinter.io/latest/descriptors/html_djlint/)。
