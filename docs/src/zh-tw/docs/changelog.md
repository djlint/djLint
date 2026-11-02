---
description: djLint 變更記錄。查看近期版本的更新內容，以及下次升級時可以期待哪些功能。
title: 變更記錄
keywords: 範本 linter, 範本格式化工具, djLint, HTML, 範本, 格式化工具, linter, 變更記錄
---

{% raw %}

# 變更記錄

變更記錄現在收錄在[版本發布](https://github.com/djlint/djLint/releases)中。

## 1.0.2

::: content

- 錯誤修正 [#240](https://github.com/djlint/djLint/issues/240)
  :::

## 1.0.1

::: content

- 錯誤修正 [#236](https://github.com/djlint/djLint/issues/236)
  :::

## 1.0.0

::: content

- 錯誤修正 [#224](https://github.com/djlint/djLint/issues/224)
  :::

## 0.7.6

::: content

- 錯誤修正 [#189](https://github.com/djlint/djLint/issues/189)、[#197](https://github.com/djlint/djLint/issues/189)
- 新增 `--warn` 旗標，將錯誤以警告的形式傳回。
  :::

## 0.7.5

::: content

- 錯誤修正 [#187](https://github.com/djlint/djLint/issues/187)
- 改善對範本檔案中 `yaml` front matter 的支援
- 為 [#123](https://github.com/djlint/djLint/issues/123) 新增規則 T032
- 為 [#124](https://github.com/djlint/djLint/issues/124) 新增規則 H033
- 為 [#178](https://github.com/djlint/djLint/issues/178) 將 linter profile 從排除式改為納入式
- 為 [#188](https://github.com/djlint/djLint/issues/188) 新增替代設定檔選項 `.djlintrc`
  :::

## 0.7.4

::: content

- 錯誤修正 [#177](https://github.com/djlint/djLint/issues/177)
  :::

## 0.7.3

::: content

- 錯誤修正 [#173](https://github.com/djlint/djLint/issues/173)、[#174](https://github.com/djlint/djLint/issues/174)
- 從 `pyproject.toml` 中移除 Py3.6。
  :::

## 0.7.2

::: content

- 錯誤修正 [#167](https://github.com/djlint/djLint/issues/167)、[#166](https://github.com/djlint/djLint/issues/166)、[#171](https://github.com/djlint/djLint/issues/171)、[#169](https://github.com/djlint/djLint/issues/169)
  :::

## 0.7.1

::: content

- 錯誤修正 [#166](https://github.com/djlint/djLint/issues/166)
  :::

## 0.7.0

::: content

- 新增自訂 HTML 標籤的設定
- 錯誤修正
  :::

## 0.6.9

::: content

- 新增 HTML 和 Angular profile
- 在規則 #H023 中允許部分字元實體
- 錯誤修正
  :::

## 0.6.8

::: content

- 錯誤修正
- 更新說明文件
  :::

## 0.6.7

::: content

- 新增設定選項 `format_attribute_template_tags`，可選擇啟用屬性內範本標籤的格式化
- 新增設定選項 `linter_output_format`，可自訂 linter 訊息中變數的順序
- 新增規則 H030 和 H031，用來檢查 meta 標籤
  :::

## 0.6.6

::: content

- 錯誤修正
  :::

## 0.6.5

::: content

- 將輸出路徑更新為相對於專案根目錄
- 錯誤修正
  :::

## 0.6.4

::: content

- 錯誤修正
  :::

## 0.6.3

::: content

- 新增對 django `blocktrans` 標籤的支援
- 錯誤修正
  :::

## 0.6.2

::: content

- 錯誤修正
  :::

## 0.6.1

::: content

- 錯誤修正
- 讓規則 T028 更嚴格，並提供更清楚的訊息
  :::

## 0.6.0

::: content

- 新增規則 T027，檢查範本語法中未閉合的字串
- 新增規則 T028，檢查屬性中缺少的去除空白標籤
- 新增規則 H029，檢查小寫的表單 method
- 格式化工具會略過沒有「trimmed」的 django blocktranslate 標籤
- 錯誤修正
  :::

## 0.5.9a

::: content

- 新增對 python 3.10 的測試支援
- 新增 pre-commit hook
  :::

## 0.5.9

::: content

- 新增選項 `--use-gitignore`，用來擴充排除項目
- 變更預設的排除比對方式
- 修正 windows 的排除路徑
- 修正屬性中 `{%...%}` 標籤的格式化
- 修正屬性中 for 迴圈與巢狀條件判斷的格式化
  :::

## 0.5.8

::: content

- 新增 require_pragma 選項
- 更新 DJ018，以抓出 input 上的 `data-src` 和 `action`
- 修正行內忽略語法
- 新增 `--lint` 選項，作為預設用法的佔位選項
- 錯誤修正
  :::

## 0.5.7

::: content

- 錯誤修正
  :::

## 0.5.6

::: content

- 新增規則 H026，找出空的 id 和 class 屬性
- 錯誤修正
  :::

## 0.5.5

::: content

- 整合設定並精簡程式碼
- 錯誤修正
  :::

## 0.5.4

::: content

- 新增規則 H020，找出空的標籤對
- 新增規則 H021，找出行內樣式
- 新增規則 H022，找出 http 連結
- 新增規則 H023，找出字元實體參照
- 新增規則 H024，找出 script 和 style 上的 type
- 新增規則 H025，檢查孤立的標籤。感謝 https://stackoverflow.com/a/1736801/10265880
- 改善屬性的格式化
- 更新 `blank_line_after_tag` 選項，不論位置為何都會加上換行
- 修正 django `trans` 標籤的格式化
- 新增行內樣式的格式化
- 新增屬性內範本條件判斷的格式化
- 在 linter 規則中，將 srcset 加入可能的 url 位置
- 加快格式化速度
- 特別感謝 [jayvdb](https://github.com/jayvdb)
  :::

## 0.5.3

::: content

- 變更 `--reformat/check` 選項的 stdout 輸出，在以 stdin 作為輸入時只印出新的 html
  :::

## 0.5.2

::: content

- 將 `alt` 的要求從 H006 拆分到 H013
- 新增選用的自訂規則檔案
- 新增 `golang` 作為 profile 選項
- 修正含有行內註解的忽略區塊的格式化
- 為 `--indent` 和 `-e` 選項新增預設文字
- 更新 url 規則以接受 #
- 修正 Windows 作業系統上的檔案編碼
- 修正單行範本標籤的 regex
- 修正 `blank_line_after_tag` 對開頭有空格之標籤的處理
  :::

## 0.5.1

::: content

- 新增規則 H019
- 修正 DJ018 和 H012 中的錯誤
  :::

## 0.5.0

::: content

- 修正 linter 規則中數個 regex 比對錯誤
- linter 不再於忽略區塊中傳回錯誤
- 新增以 `{% djlint:off %}...{% djlint:on %}` 標籤讓 linter/格式化工具忽略程式碼區塊的選項
  :::

## 0.4.9

::: content

- 修正錯誤 [#35](https://github.com/djlint/djLint/issues/35)
  :::

## 0.4.8

::: content

- 修正錯誤 [#34](https://github.com/djlint/djLint/issues/34)
  :::

## 0.4.7

::: content

- 將 `source` 標籤移至單行標籤
  :::

## 0.4.6

::: content

- 修正錯誤 [#31](https://github.com/djlint/djLint/issues/31)
  :::

## 0.4.5

::: content

- 在說明文件中加入最佳做法
- 新增 `--profile` 選項，用來設定預設的 linter/格式化工具規則
- 新增 jinja url 寫法的 linter 規則
  :::

## 0.4.4

::: content

- 將縮排設定從字串改為整數。`--indent 3`
  :::

## 0.4.3

::: content

- 新增縮排間距的 cli 選項。`--indent=" "`
  :::

## 0.4.2

::: content

- 透過 `blank_line_after_tag` 選項，新增在標籤之後加上額外空白的支援
  :::

## 0.4.1

::: content

- 新增一次處理多個檔案或資料夾的支援
  :::

## 0.4.0

::: content

- 修正 django `{# ... #}` 標籤的格式化
- 新增 figcaption、details 和 summary 標籤的縮排支援
- 新增在 `pyproject.toml` 中覆寫或擴充排除路徑清單的支援
  :::

## 0.3.9

::: content

- 更新屬性的處理方式
  :::

## 0.3.8

::: content

- 新增對 stdin 的支援
  :::

## 0.3.7

::: content

- 修正 `small`、`dt` 和 `dd` 標籤的格式化
  :::

## 0.3.6

::: content

- 新增格式化工具對 Nunjucks `{%-` 開頭區塊的支援
  :::

## 0.3.5

::: content

- 新增對更多 Django 區塊的支援
- 新增對自訂區塊的支援
- 新增對 `pyproject.toml` 中設定的支援
  :::

## 0.3.4

::: content

- 修正 Nunjucks 去除空白標籤 `-%}` 的格式
  :::

## 0.3.3

::: content

- 允許簡短的 `div` 標籤保持單行
  :::

## 0.3.2

::: content

- 修正 Django 註解的格式化
- 格式化時忽略 textarea
  :::

## 0.3.1

::: content

- 更新屬性格式化的 regex
- 更新 lint 規則 W010
  :::

## 0.3.0

::: content

- 如有任何格式變更，結束代碼改為 1
- 新增對 Jinja `asset` 標籤的支援
  :::

## 0.2.9

::: content

- 更新 W018 的 regex
- 移除重複的 lint 訊息
- 更新 Handlebars 的 E001
  :::

## 0.2.8

::: content

- 修正舊版 Click 的進度列錯誤
  :::

{% endraw %}
