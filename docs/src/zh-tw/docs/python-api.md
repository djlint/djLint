---
description: 透過 djLint API，在你自己的 Python 程式碼中格式化與 lint 範本。
title: Python API
keywords: 範本 linter, 範本格式化工具, djLint, HTML, 範本, 格式化工具, linter, python, api
---

# Python API

`djlint.api` 可以在 Python 程式中格式化與 lint 文字，結果與命令列相同。它是為編輯器、建置工具，以及其他在記憶體中持有範本的程式所設計。套件中的其他部分在任何版本都可能變動，因此請使用這個模組，而不要使用 `djlint.settings` 或 `djlint.lint`。

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', filename="templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", /, *, python_rules=True, **options)` 會讀取適用於某個資料夾內檔案的設定。它會從該資料夾往上層尋找設定，就像命令列從目前目錄往上找一樣，而且不會變更目前目錄。

選項使用命令列選項的名稱（以底線連接），作用方式也與命令列相同：有設定的值會優先於設定檔，而 `False`、空字串，以及大多數選項的 `0`，都視為未指定。路徑以 `pathlib.Path` 指定。

讀取設定需要一些時間，因此只要讀取來源的檔案沒有變動，就請保留這個結果。它可以用於任意數量的文字。

使用 `python_rules=False` 時，不會載入帶有 `python_module` 的自訂規則，可避免執行你不信任的專案的程式碼。這些規則的名稱會列在 `config.skipped_rules` 中。

## format_text

`format_text(config, text, /)` 會傳回格式化後的文字。第一行以 CRLF 結尾的文字，傳回時會使用 CRLF；其他文字則使用 LF。使用 `require_pragma` 時，沒有 pragma 的文字會原樣傳回。

## lint_text

`lint_text(config, text, /, *, filename="-")` 會依文件順序傳回 `Finding` 的清單。`per-file-ignores` 會以 `filename` 進行比對。使用 `require_pragma` 時，沒有 pragma 的文字不會有任何檢查結果。

`Finding` 是具有下列欄位的具名元組：

::: content

- `code`：規則的代碼，例如 `H013`。
- `message`：規則的訊息內容。
- `match`：找到的文字的開頭部分，最多 20 個字元。
- `line`、`column`：檢查結果的起始位置。行號從 1 開始計算，欄號從 0 開始。
- `end_line`、`end_column`：結束位置的下一個位置，可能位於後面的某一行。
:::

欄號以字元計算，而不是位元組或 UTF-16 程式碼單元。

## is_excluded

`is_excluded(config, path, /)` 會判斷 `exclude`、`extend_exclude` 或 gitignore 是否排除了某個檔案，與命令列的行為相同。`format_text` 和 `lint_text` 本身不會檢查這一點。

## 規則模組

自訂規則的 `python_module` 在每個處理程序中只會匯入一次，從設定的專案根目錄匯入。一個持續執行並處理多個專案的程式，若要讀取另一個專案的規則模組，必須從 `sys.modules` 移除所有從該專案匯入的內容，並移除專案根目錄（它會一直留在 `sys.path` 的末端）。
