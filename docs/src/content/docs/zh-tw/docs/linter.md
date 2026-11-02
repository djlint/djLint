---
title: "Linter 規則"
description: "djLint HTML 範本 linter 的規則，以及如何新增自己的規則。"
sidebar:
  label: "Linter"
---

djLint 內含許多規則，用來檢查範本的風格與正確性。將 linter 設定為使用你所選範本語言的預設 profile，就能充分發揮它的功用。

```bash
djlint /path/to/templates --lint

# 使用自訂副檔名
djlint /path/to/templates -e html.dj --profile=django

# 或指定檔案
djlint /path/to/this.html.j2  --profile=jinja
```

:::tip
[查看設定指南，了解所有選項！](/zh-tw/docs/configuration/)
:::

## 啟用或停用規則

大多數規則預設為啟用。在命令列中，可以用 `--ignore` 旗標停用規則，用 `--include` 旗標啟用規則。

例如：

```bash
djlint . --lint --include=H006,H017 --ignore=H013,H015
```

這也可以透過[設定](/zh-tw/docs/configuration)檔完成。

## 規則

| 代碼 | 意義                                                                        | 預設 |
| ---- | --------------------------------------------------------------------------- | ---- |
| T001 | 變數應以空白包圍。例如：`{{ this }}`                                        | ✔️   |
| T002 | 標籤中應使用雙引號。例如 `{% extends "this.html" %}`                        | ✔️   |
| T003 | Endblock 應寫上名稱。例如：`{% endblock body %}`。                          | -    |
| D004 | （Django）靜態 URL 應遵循 `{% static path/to/file %}` 的寫法。              | ✔️   |
| J004 | （Jinja）靜態 URL 應遵循 `{{ url_for('static'..) }}` 的寫法。               | ✔️   |
| H005 | Html 標籤應具有非空的 `lang` 屬性。                                         | ✔️   |
| H006 | `img` 標籤應具有 `height` 和 `width` 屬性。                                 | -    |
| H007 | html 標籤之前應有 `<!DOCTYPE ... >`。                                       | ✔️   |
| H008 | 屬性應使用雙引號。                                                          | ✔️   |
| H009 | 標籤名稱應為小寫。                                                          | ✔️   |
| H010 | 屬性名稱應為小寫。                                                          | ✔️   |
| H011 | 屬性值應加上引號。                                                          | ✔️   |
| H012 | 屬性的 `=` 前後不應有空格。                                                 | ✔️   |
| H013 | `img` 標籤應具有 alt 屬性。                                                 | ✔️   |
| H014 | 空白行多於設定所保留的數量。                                                | ✔️   |
| H015 | `h` 標籤之後應換行。                                                        | ✔️   |
| H016 | html 中缺少 `title` 標籤。                                                  | ✔️   |
| H017 | 空元素標籤應自閉合（與 H018 衝突）。                                        | -    |
| D018 | （Django）內部連結應使用 `{% url ... %}` 的寫法。                           | ✔️   |
| H018 | 空元素標籤本身就是自閉合的，必須以「>」結尾，而不是「/>」（與 H017 衝突）。 | -    |
| J018 | （Jinja）內部連結應使用 `{{ url_for() ... }}` 的寫法。                      | ✔️   |
| H019 | 將 `javascript:abc()` 換成 `on_` 事件與真正的 URL。                         | ✔️   |
| H020 | 發現空的標籤對。請考慮移除。                                                | ✔️   |
| H021 | 應避免使用行內樣式。                                                        | ✔️   |
| H022 | 外部連結請使用 HTTPS。                                                      | ✔️   |
| H023 | 不要使用字元實體參照。                                                      | ✔️   |
| H024 | 省略 script 和 style 的 type。                                              | ✔️   |
| H025 | 標籤似乎是孤立的。                                                          | ✔️   |
| H026 | 空的 id 和 class 屬性可以移除。                                             | ✔️   |
| T027 | 範本語法中發現未閉合的字串。                                                | ✔️   |
| T028 | 請考慮在屬性值中使用去除空白的標籤。`{%- if/for -%}`                        | -    |
| H029 | 請考慮使用小寫的表單 method 值。                                            | ✔️   |
| H030 | 請考慮加上 meta description。                                               | ✔️   |
| T032 | 範本標籤中發現多餘的空白。                                                  | ✔️   |
| H033 | 表單 action 中發現多餘的空白。                                              | ✔️   |
| T034 | 你是不是想寫 {% ... %}，而不是 {% ... }%？                                  | ✔️   |
| H036 | 不要用 `br` 標籤製造間距。                                                  | ✔️   |
| H037 | 發現重複的屬性。                                                            | ✔️   |
| T038 | 區塊標籤沒有對應的結束標籤。                                                | ✔️   |
| T039 | 發現未閉合的範本標籤。                                                      | ✔️   |
| T040 | extends 或 include 標籤中缺少範本名稱，或範本名稱為空。                     | ✔️   |
| H041 | 標籤在與開啟時不同的範本區塊中關閉。                                        | ✔️   |
| T041 | Extends 標籤應為範本中的第一個標籤。                                        | ✔️   |
| H042 | Label 的 for 屬性在此檔案中沒有對應的元素 id。                              | ✔️   |
| T042 | 在繼承其他範本的範本中，區塊以外的內容不會被渲染。                          | ✔️   |
| H043 | Button 標籤應具有 `type` 屬性。                                             | ✔️   |
| T043 | 區塊名稱在範本中被使用了不只一次。                                          | ✔️   |
| H044 | Thead 不應混用 `th` 和 `td` 儲存格。                                        | ✔️   |
| T044 | 輸出標籤中含有陳述式關鍵字；請改用區塊標籤。                                | ✔️   |
| H045 | Iframe 標籤應具有 `title` 屬性。                                            | ✔️   |
| T045 | HTML 註解中的範本標籤仍會執行；請改用範本註解來停用它。                     | ✔️   |
| H046 | Tabindex 不應為正數。                                                       | ✔️   |
| H047 | 不應在可取得焦點的元素上設定 aria-hidden。                                  | ✔️   |
| H048 | 規格中沒有定義這個 aria 屬性。                                              | ✔️   |
| H049 | Viewport 不應阻止頁面縮放。                                                 | ✔️   |
| H050 | 元素已過時，應予以替換。                                                    | ✔️   |
| H051 | 這個 role 不是 ARIA 為標記定義的角色。                                      | ✔️   |
| H052 | Meta refresh 不應以計時方式重新載入或重新導向頁面。                         | ✔️   |
| H053 | Id 在檔案中被使用了不只一次。                                               | ✔️   |
| H054 | 互動元素不應巢狀放在另一個互動元素內。                                      | ✔️   |
| H055 | Lang 屬性應為語言標記，例如 en 或 pt-BR。                                   | ✔️   |
| H056 | Src 不應為空。                                                              | ✔️   |
| H057 | Video 應具有字幕軌。                                                        | ✔️   |

### 代碼規則

代碼的第一個字母遵循以下規則：

- D：專門適用於 Django
- H：適用於 html
- J：專門適用於 Jinja
- M：專門適用於 Handlebars
- N：專門適用於 Nunjucks
- T：普遍適用於範本

### 規則詳細說明

<!-- oxfmt-ignore-start -->

#### T001

`Variables should be wrapped in a whitespace.`

像 `{{user.name}}` 這樣內側沒有留白的範本語法比較難瀏覽與比對差異，而且整個程式碼庫中不一致的空格，會讓以 grep 為基礎的重構（搜尋某個變數或標籤）變得不可靠，因為同一個運算式會有多種寫法。Django 和 Jinja 的風格指南都將 `{{ var }}` 和 `{% tag %}` 寫成內側各留一個空格。

不適用於 handlebars 和 golang profile。

不要這樣寫：

```html
{{user.name}}
```

應該這樣寫：

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

在範本標籤（`{% extends %}`、`{% include %}`、`{% with %}`、`{% trans %}`、`{% now %}`）中混用單引號和雙引號，會讓同一個範本名稱出現兩種寫法，導致搜尋和大量重新命名時漏掉一半的出現位置。統一使用雙引號，可讓標籤引數與檔案其餘部分的 HTML 屬性引號保持一致。

HTML 屬性值中的單引號（例如 `<span title="{% trans 'x' %}">`）不會被標記，因為屬性的雙引號迫使那裡只能使用單引號。

使用 `quote_style = "single"` 時，這條規則會改為要求單引號，而格式化工具也會寫成單引號。

`--reformat` 會替你改寫這些引號。

不要這樣寫：

```html
{% extends 'base.html' %}
```

應該這樣寫：

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

當 `{% block %}` 跨越許多行或區塊彼此巢狀時，單獨的 `{% endblock %}` 無法看出它關閉的是哪個區塊，因此編輯時很容易結束錯誤的區塊；子範本接著就會覆寫錯誤的內容。為 endblock 寫上名稱可以記錄配對關係，讓 djLint 和 Django（在 endblock 名稱不符時會引發 TemplateSyntaxError）都能抓出在錯誤位置關閉的區塊。配對錯誤（未閉合的區塊、孤立的 endblock 以及名稱不符）屬於正確性檢查，由 T038 處理。

預設為停用；可用 `--include=T003` 啟用。`--name-endblocks` 會替你寫上名稱。

區塊在同一行開啟並關閉時不需要名稱，例如 `{% block title %}``{% endblock %}`。格式化工具會將含有其他標籤的區塊內容移到各自獨立的行，因此寫在一行上的區塊在格式化之後可能需要名稱；使用 `--name-endblocks` 時，格式化工具也會寫上該名稱。

不要這樣寫：

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

應該這樣寫：

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Static urls should follow {% static path/to/file %} pattern.`

寫死 /static/ 路徑會繞過 Django 的 `{% static %}` 標籤，因此當 STATIC_URL 變更時（例如將靜態資源移到 CDN 或部署在子路徑下），範本就會失效，也永遠不會使用 ManifestStaticFilesStorage 產生的雜湊檔名，導致正式環境出現 404 或過時的快取資源。這條規則尋找的是字面上的 `/static/` 前置詞，因此從其他路徑提供靜態檔案的專案不在檢查範圍內。

不要這樣寫：

```html
<link rel="stylesheet" href="/static/css/style.css">
```

應該這樣寫：

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

寫死 /static/ 路徑會繞過 Flask/Jinja 的 url_for('static', ...)，因此當應用程式掛載在 URL 前置詞下，或靜態資料夾/主機變更時，靜態資源就會出現 404，框架加上的快取破壞（cache-busting）查詢字串也會遺失。這條規則尋找的是字面上的 `/static/` 前置詞，因此從其他路徑提供靜態檔案的專案不在檢查範圍內。

不要這樣寫：

```html
<link rel="stylesheet" href="/static/css/style.css">
```

應該這樣寫：

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have a non-empty lang attribute.`

`<html>` 上沒有 lang 屬性時，螢幕閱讀器只能猜測發音規則，可能會用錯誤的語言朗讀頁面，而瀏覽器也無法正確提供翻譯、斷字或依地區設定顯示的引號。宣告頁面語言是 WCAG 2.1 成功準則 3.1.1（A 級）。

`lang=""` 和沒有值的 `lang` 都表示語言不明，因此會與缺少屬性一樣被回報。

不要這樣寫：

```html
<!DOCTYPE html>
<html>
</html>
```

應該這樣寫：

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`Img tag should have height and width attributes.`

預設為停用；可用 `--include=H006` 啟用。

`<img>` 沒有寬度和高度時，瀏覽器無法在圖片下載前預留空間，因此周圍的內容會隨著圖片載入而跳動。這種版面位移會使累計版面配置位移（Cumulative Layout Shift，一項 Core Web Vitals 指標）變差，也可能讓使用者在頁面穩定前誤點。

不要這樣寫：

```html
<img src="cat.png" alt="Cat">
```

應該這樣寫：

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

`<html>` 標籤之前沒有 `<!DOCTYPE>` 時，瀏覽器會以相容模式（quirks mode）渲染頁面，模擬舊式的盒模型與版面配置行為，導致 CSS 在各瀏覽器間的渲染結果不一致。doctype 之前出現範本標籤和註解沒有問題；只有 `<html>` 標籤本身必須在它之後。

不要這樣寫：

```html
<html lang="en">
</html>
```

應該這樣寫：

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Attributes should be double quoted.`

混用引號風格會讓屬性值更難瀏覽和 grep，而以單引號包住的值只要內容含有撇號就會出錯。雙引號是 HTML 規格、格式化工具和大多數風格指南採用的慣例，因此統一使用雙引號能讓範本與更廣泛的生態系保持一致。

不要這樣寫：

```html
<div class='content'></div>
```

應該這樣寫：

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

HTML 剖析器接受大寫的標籤名稱，但 XHTML 和 XML 序列化區分大小寫，會拒絕大寫名稱，而且大小寫混用會讓文字搜尋和 diff 審查變得不可靠（grep `<h1>` 會漏掉 `<H1>`）。使用小寫標籤名稱能讓範本保持可攜性與一致性。

使用 `--ignore-case` 時不會回報，因為這個選項會讓格式化工具不更動大小寫。

不要這樣寫：

```html
<H1>Welcome</H1>
```

應該這樣寫：

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

大寫的屬性名稱在 XHTML/XML 序列化中是無效的，也會讓跨範本的文字搜尋失效（grep src= 會漏掉 SRC=）。DOM 本來就會將 HTML 屬性名稱正規化為小寫，因此大寫寫法只會增加不一致，沒有任何好處。只有格式化工具會轉成小寫的名稱才會回報：`class`、`id`、`src`、`width`、`height`、`alt`、`style`、`lang`、`title`、`media` 和 `srcset`。`--reformat` 會替你修正它們，而像 `:itemID` 這樣的框架繫結，或像 `data-ID` 這樣較長的名稱，則會保留原本的大小寫。

使用 `--ignore-case` 時不會回報，因為這個選項會讓格式化工具不更動大小寫。

不要這樣寫：

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

應該這樣寫：

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

沒有加引號的屬性值會在第一個空白處結束，因此像 class=btn primary 這樣的值，會默默丟掉空格之後的所有內容（瀏覽器會把「primary」當成另一個布林屬性）。來自範本變數的值尤其脆弱：只要渲染出空格、「=」或「>」，就會破壞標籤。加上引號可以讓值的邊界明確且安全。

不要這樣寫：

```html
<div class=test></div>
```

應該這樣寫：

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

HTML 允許「=」前後有空白，因此這是一條風格規則。寫成不含空格的 name="value" 是常見的風格，也是簡單的文字工具（例如 grep 或搜尋與取代）所預設的寫法，因此空格不一致會讓屬性更難尋找與重構。`--reformat` 會替你刪除這些空格。

不要這樣寫：

```html
<div class = "test"></div>
```

應該這樣寫：

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

沒有 alt 屬性時，螢幕閱讀器會朗讀圖片的檔名，或什麼都不讀，不符合 WCAG 1.1.1（非文字內容）。圖片載入失敗時，使用者看到的也是 alt 文字。裝飾性圖片應明確寫上空的 alt=""，讓輔助技術知道要略過它們；這樣也符合這條規則。

沒有值的 `alt` 等同於 `alt=""`，也就是裝飾性圖片的情況，因此會被接受。

不要這樣寫：

```html
<img src="cat.jpg" height="200" width="300">
```

應該這樣寫：

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

連續的空白行對渲染後的頁面沒有任何影響（HTML 會合併空白），卻會讓範本變得臃腫，並在相鄰行變更時產生雜亂的 diff。djLint 的格式化工具預設會將它們完全移除（最多保留 `max_blank_lines` 個空白行，預設值為 0），因此殘留的連續空白行表示程式碼尚未格式化。

不要這樣寫：

```html
<div>one</div>


<p>two</p>
```

應該這樣寫：

```html
<div>one</div>

<p>two</p>
```

#### H015

`Follow h tags with a line break.`

標題是定義文件大綱的區塊層級地標；把下一個元素擠到 h 結束標籤的同一行，會在原始碼中隱藏這個結構，而且編輯其中任何一個元素，在 diff 中都會顯示為兩者都有變更。在每個標題後換行，能讓範本的視覺結構與渲染後的大綱保持一致。

不要這樣寫：

```html
<h1>Heading</h1><p>Intro text.</p>
```

應該這樣寫：

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Missing title tag in html.`

HTML 規格要求每份文件都要有 title 元素。如果沒有，瀏覽器分頁、書籤和瀏覽記錄就會顯示原始的 URL 而不是頁面名稱，搜尋引擎會失去頁面的主要標示，而螢幕閱讀器使用者也會失去頁面載入時第一個朗讀的內容，不符合 WCAG 2.4.2（頁面標題，A 級）。

只會在包含完整 `<html>`...`</html>` 文件的檔案上觸發，因此部分範本（partial）和繼承基底範本的子範本永遠不會被標記。在用戶端設定標題的 SPA 外殼仍然需要靜態的 `<title>`：首次繪製時、爬蟲看到的，以及 JavaScript 執行失敗時顯示的，都是它。

不要這樣寫：

```html
<html lang="en">
<body>Content</body>
</html>
```

應該這樣寫：

```html
<html lang="en">
<head>
<title>My page</title>
</head>
<body>Content</body>
</html>
```

#### H017

`Void tags should be self closing.`

必須同時能以 XML/XHTML 剖析（或提供給以 XML 為基礎的工具）的範本，會拒絕沒有結尾斜線的空元素，而在程式碼庫中混用 `<br>` 和 `<br />` 會產生不一致的 diff。這條規則強制採用 XHTML 風格的慣例，讓每個空元素都以相同方式關閉。

預設為停用；可用 `--include=H017` 啟用。與 H018 互斥；兩種慣例只能擇一啟用。`--close-void-tags` 會替你為 html 空元素標籤加上斜線。svg 的 `<path>` 會保持原樣，因此請手動關閉它。

不要這樣寫：

```html
<br>
<meta charset="utf-8">
```

應該這樣寫：

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Internal links should use the {% url ... %} pattern.`

當路由的路徑在 urls.py 中變更時，寫死的內部 URL 會默默過時，產生失效的連結和無效的表單 action，而且任何針對 URLconf 的測試都抓不到。`{% url %}` 會根據路由名稱解析路徑，因此重新命名路徑時，所有連結都會一次更新。

不要這樣寫：

```html
<a href="/accounts/login">Login</a>
```

應該這樣寫：

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

在 HTML Living Standard 中，空元素結尾的斜線沒有任何意義（剖析器會忽略它），因此寫成 `<br />` 暗示了 HTML 並不具備的 XML 式自閉合行為，可能誤導讀者在非空元素的標籤上也加上斜線，而那裡多出來的 / 會被默默丟棄，掩蓋未閉合標籤的錯誤。這條規則強制空元素以單純的 > 結尾。

預設為停用；可用 `--include=H018` 啟用。與 H017 互斥；兩種慣例只能擇一啟用。SVG 的 `<path />` 不受此限，因為 SVG 是 XML，需要斜線。使用 `--close-void-tags` 時不會回報，因為此時格式化工具寫出的正是這條規則所回報的斜線。

不要這樣寫：

```html
<br />
<meta charset="utf-8" />
```

應該這樣寫：

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

當路由的路徑變更，或應用程式掛載在前置詞下時，寫死的內部 URL 會默默失效，留下失效的連結和送往 404 的表單 action。url_for() 會根據端點名稱建立 URL，因此路由的變更會自動反映到每個範本。

不要這樣寫：

```html
<a href="/accounts/login">Login</a>
```

應該這樣寫：

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

javascript: URL 會讓中鍵點擊和「在新分頁中開啟」失效，在 JavaScript 被停用或載入失敗時沒有任何作用，會被嚴格的內容安全政策（Content Security Policy）封鎖，而且是典型的 XSS 注入點。請在 href 中使用真正的 URL，並改以事件處理常式附加行為。在嚴格的 CSP 下，行內的 on* 處理常式同樣會被封鎖：範例中的 onclick 只是範本內最小幅度的修正；建議從指令碼檔案以 addEventListener 附加監聽器。

不要這樣寫：

```html
<a href="javascript:openPopup()">Open popup</a>
```

應該這樣寫：

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

空的標籤對不會渲染任何內容，但仍會建立 DOM 節點，可能從樣式表套用到 margin、border 或 flex/grid 間距，產生難以追查的幽靈間距；它通常是先前編輯時留下的標記。在一般標記中本來就可以合法為空的標籤（td、th、li、dt、dd、slot）不受此限。帶有任何屬性的標籤（像 `<div id="app">``</div>` 這樣的 JS 掛載點，或像 `<i class="fa fa-user">``</i>` 這樣的圖示字型元素）也不會被標記；只有完全沒有屬性的空標籤對才會符合。

不要這樣寫：

```html
<p>Saved.</p>
<span> </span>
```

應該這樣寫：

```html
<p>Saved.</p>
```

#### H021

`Inline styles should be avoided.`

行內樣式的權重高於任何樣式表選擇器，因此之後要覆寫它們就必須使用 !important；在 style-src 中沒有 'unsafe-inline' 的內容安全政策會封鎖它們；而且它們會把呈現方式分散到各個範本中，因此更換主題或設計時，就得修改標記，而不是只改一份樣式表。請將宣告移到 CSS class 中。有一個合理的例外：HTML 電子郵件範本，因為許多電子郵件用戶端會移除 `<style>` 區塊，行內樣式是標準做法；請排除你的電子郵件範本目錄，或針對它們停用這條規則。

不要這樣寫：

```html
<div style="color: red;">Wrong username or password.</div>
```

應該這樣寫：

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

在透過 HTTPS 提供的頁面上，以 http:// 載入的子資源屬於混合內容：瀏覽器會直接封鎖指令碼、樣式表和 iframe，對圖片則會自動升級或發出警告。連往 http:// 頁面的 `<a>` 連結不算混合內容，但它仍會讓訪客透過未加密、容易被攔截和竄改的連線前往該頁面。指向確實沒有 TLS 的內部主機的參照也會被標記；請以 `{# djlint:off H022 #}` 區塊讓這些地方不被回報，而不是停用這條規則。

不要這樣寫：

```html
<a href="http://example.com">Example</a>
```

應該這樣寫：

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

HTML5 文件使用 UTF-8，因此直接寫出字元本身在任何地方都能運作，也是審查者實際讀到的內容；字元實體參照中的拼字錯誤（例如 `&mdsah;`）不會被瀏覽器發現，而會原封不動地顯示為錯誤的文字。djLint 允許帶有語法作用的實體（`&lt;`、`&gt;`、`&amp;`、`&quot;`、`&apos;`，以及大括號 `&lbrace;` 和 `&rbrace;`，連同 `&percnt;`、`&num;` 和 `&dollar;`，因為直接寫出來會湊成範本分隔符號），以及代表不可見字元、因而無法以字面形式審查的實體：空格類（`&nbsp;`、`&thinsp;`、`&hairsp;`）、連接符與方向標記（`&zwnj;`、`&zwj;`、`&lrm;`、`&rlm;`）以及 `&shy;`，不論是具名、十進位或十六進位形式皆然。

`--reformat` 會替你將實體改寫為字元。寫在範本標籤內的實體屬於標籤而不屬於頁面，因此規則和格式化工具都不會處理它。`--no-entity-formatting` 會關閉改寫功能，但規則仍然有效，因此實體仍會回報。若要保留實體，請將 `H023` 加入 `ignore`。

不要這樣寫：

```html
<p>Dates 1900 &mdash; 2000</p>
```

應該這樣寫：

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript 和 text/css 是 HTML5 中 `<script>` 和 `<style>` 的預設值，因此這個屬性只是瀏覽器會忽略的多餘負擔；WHATWG 規格明確表示應該省略它。省略它也能避免過時的 MIME 字串在被複製到模組指令碼（type="module" 在那裡確實有意義）上時破壞元素。

不要這樣寫：

```html
<script type="text/javascript" src="app.js">
```

應該這樣寫：

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

缺少對應開始或結束標籤的標籤，會迫使瀏覽器的錯誤復原機制猜測元素在哪裡結束，因此後續的標記會被吞進錯誤的元素中；接著版面配置、CSS 選擇器和 JavaScript DOM 查詢就會默默出錯，而且在各瀏覽器上的表現各不相同。H025 也會回報在 `<p>` 內開啟的 `<ol>` 或 `<ul>`：HTML 剖析器會在清單之前關閉段落，因此標記永遠不會照著寫法巢狀。

不要這樣寫：

```html
<div>
  <p>Hello</p>
```

應該這樣寫：

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Empty id and class tags can be removed.`

沒有任何 class 或 id 選擇器會符合空的屬性，而且空的 id 是無效的 HTML（id 值不得為空字串）。像 `div[class]` 這樣的屬性存在選擇器仍然會符合它，因此移除它，會影響以這種方式撰寫的樣式表。它通常代表範本有錯誤，原本應該要插入某個變數，因此移除或填入它，可以避免這個錯誤明明就在眼前卻沒被發現。

不要這樣寫：

```html
<div id="" class="">content</div>
```

應該這樣寫：

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

在 `{% ... %}` 或 `{{ ... }}` 內開啟卻從未關閉的引號，會讓範本引擎錯誤地剖析標籤：Django 和 Jinja 不是在渲染時引發 TemplateSyntaxError，就是默默地把標籤其餘的引數當成字串內容吞掉，導致頁面出現 500 錯誤，或在缺少引數的情況下渲染。

不要這樣寫：

```html
{% trans "Welcome %}
```

應該這樣寫：

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

預設為停用；可用 `--include=T028` 啟用。

去除空白的標籤所移除的空白，是會被渲染出來的空白，因此請只在屬性沒有空白可失去的地方使用。`alt="{%- if brand -%}Acme{%- endif -%} logo"` 會渲染成 `Acmelogo`，而 svg 的 `d="M12 {%- if big -%}20{%- endif -%} 4Z"` 則會變成另一條路徑。這就是這條規則需要選擇啟用的原因。

屬性值中的範本標籤會把周圍的空白和換行輸出到渲染後的屬性中，因此用一般的 `{% if %}`/`{% for %}` 標籤組成的 href 或 src 可能會含有多餘的空格，產生無效的 URL。Jinja/Nunjucks 的空白控制標籤（`{%- ... -%}`）會移除周圍的空白，讓屬性渲染成一個乾淨的值。class 屬性不受此限，因為 class 名稱之間多出的空白沒有害處。

不適用於 django profile：Django 範本標籤不支援 `{%- -%}` 空白控制。

不要這樣寫：

```html
<a href="{% if x %}/home{% endif %}"></a>
```

應該這樣寫：

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

HTML 規格將表單的 method 關鍵字定義為小寫（get、post）；瀏覽器只是透過不區分大小寫的備援比對來接受大寫寫法。保持標準的小寫形式可以讓範本一致、容易 grep，並避免嚴格的驗證器和以 XHTML 為基礎的工具鏈發出警告。

不要這樣寫：

```html
<form method="POST"></form>
```

應該這樣寫：

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

搜尋引擎會將 meta description 作為搜尋結果中頁面標題下方的摘要；如果沒有，搜尋引擎會從頁面上任意的文字拼湊出摘要，這會降低點閱率，並在分享頁面時產生不佳的連結預覽。

只會在包含完整 `<html>`...`</html>` 文件的檔案上觸發。上述關於摘要的理由只適用於公開索引的頁面；對於需要登入或內部網路的應用程式，這條規則通常會被停用。

不要這樣寫：

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

應該這樣寫：

```html
<html lang="en">
  <head>
    <title>Home</title>
    <meta name="description" content="A short summary of this page.">
  </head>
  <body>Welcome</body>
</html>
```

#### T032

`Extra whitespace found in template tags.`

範本標籤引數之間連續的空格或 Tab 是看不見的雜訊：它們會在 diff 中掩蓋真正的差異，可能讓人難以發現缺少的引數，而且會偏離 djLint 格式化工具產生的單一空格風格，造成不必要的重新格式化變動。加上引號的字串內的空白會被保留，不會被標記。

不要這樣寫：

```html
{% static  'css/style.css' %}
```

應該這樣寫：

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

表單 action 值開頭或結尾的空白會成為渲染後 URL 的一部分。瀏覽器在剖析時會將它移除，但非瀏覽器的用戶端和直接使用字面值的測試可能不會，而且在 `{% url %}` 標籤周圍，多出來的空格幾乎一定代表打錯字，會渲染出無法通過伺服器端路由比對的送出 URL。

不要這樣寫：

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

應該這樣寫：

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Did you intend to use {% ... %} instead of {% ... }%?`

}% 幾乎一定是 %} 的打字錯誤。範本引擎不會將 }% 視為標籤分隔符號，因此標籤永遠不會被剖析：原始的 {% ... }% 文字會洩漏到渲染後的 HTML 中，或是引擎在遇到未閉合的標籤時引發語法錯誤。

不要這樣寫：

```html
{% include "footer.html" }%
```

應該這樣寫：

```html
{% include "footer.html" %}
```

#### H036

`Do not use br tags for spacing.`

html 規格只允許 `<br>` 用於屬於內容本身的換行，例如郵寄地址或詩句，這種用法不會回報。回報的是規格所禁止的呈現用途：兩個以上連續的換行，也就是垂直間距；以及緊貼在區塊元素內側邊緣的換行，它渲染出的效果，元素本身的 margin 都做得到。這兩種用法都會在窄寬度下破壞文字的重排，而螢幕閱讀器會在沒有任何內容可朗讀的地方宣告一個強制換行。

不要這樣寫：

```html
<p>Shipping is free.<br><br>Delivery takes 3 days.</p>
```

應該這樣寫：

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

重複的屬性是無效的 HTML，瀏覽器只會保留第一個，並默默丟棄其餘的，因此第二個 class 或 style 值永遠不會生效，從而掩蓋真正的錯誤。這項檢查能理解範本語法：在互斥分支（`{% if %}`/`{% else %}`）中重複出現的屬性不會被標記，因為只有其中一份會被渲染。

不要這樣寫：

```html
<div class="card" id="profile" class="active">...</div>
```

應該這樣寫：

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

像 `{% if %}`、`{% for %}` 或 `{% macro %}` 這樣缺少對應結束標籤的區塊標籤，在 Django 和 Jinja 中是嚴重的 TemplateSyntaxError：頁面會在請求時無法渲染，而這條規則能在部署前抓出這個問題。它也會標記沒有開始標籤的孤立結束標籤，以及交錯不正確的區塊（例如 `{% if %}``{% for %}``{% endif %}`）。

`{% block %}`/`{% endblock %}` 的配對以及 endblock 名稱不符，都由這條規則檢查；T003（預設停用）則另外要求每個多行的 `{% endblock %}` 都要寫上名稱。透過 custom_blocks 註冊的自訂區塊標籤也會被檢查，包括它們以 / %} 結尾的自閉合形式。

不要這樣寫：

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

應該這樣寫：

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Unclosed template tag found.`

以 `{{` 或 `{%` 開啟、卻從未以對應的 `}}` 或 `%}` 關閉的範本標籤，不會被剖析為標籤：Django/Jinja 不是引發 TemplateSyntaxError，就是將原始的大括號字元渲染到頁面中，而且直到下一個分隔符號之前的所有內容都可能被默默吞掉。這類打字錯誤（少一個大括號、分隔符號不相符）在審查時很容易被忽略，因為範本可能仍會部分渲染。

不要這樣寫：

```html
<p>{{ user.name }</p>
```

應該這樣寫：

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

範本名稱缺少、為空或只有空白的 `{% extends %}` 或 `{% include %}` 標籤，沒有任何東西可以載入：名稱完全缺少時，Django 會引發 TemplateSyntaxError；名稱為空時，則會在渲染時引發 TemplateDoesNotExist，因此即使範本檔案本身的語法看起來合理，頁面在正式環境中仍會出現 500 錯誤。

不要這樣寫：

```html
{% extends "" %}
```

應該這樣寫：

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

當 HTML 標籤在某個 `{% block %}` 中開啟、卻在另一個區塊中關閉時，只覆寫其中一個區塊的子範本會繼承到半個元素，在渲染後的頁面中產生不平衡的標記；接著瀏覽器會以無法預測的方式自動關閉或重新巢狀元素，在遠離實際編輯的範本之處破壞版面配置和 CSS 選擇器。讓每個元素都在同一個區塊內開啟和關閉，就能讓每個區塊都可以安全地單獨覆寫。

不要這樣寫：

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

應該這樣寫：

```html
{% block content %}
<div class="wrapper">
</div>
{% endblock content %}
{% block footer %}
{% endblock footer %}
```

#### T041

`Extends tag should be the first tag in the template.`

Django 拒絕編譯在 `{% extends %}` 之前出現其他標籤的範本，而寫在它之前的文字會被渲染，因此會洩漏到頁面中，出現在父範本產生的所有內容之前。Jinja 也會渲染那段文字，而 nunjucks 則會將它丟棄，因此不論在哪個引擎中，範本的行為都與看起來的不同。

`{# #}` 註解不會渲染任何內容，因此不算在內；`{% comment %}`、<code>{&#37; raw %}</code> 或 `{% verbatim %}` 區塊（無論是否具名）內的任何內容、三種寫法中任一種的 `{# djlint:off #}` 區域，以及 yaml front matter 也都不算。html 註解則會算在內：引擎會將它寫入頁面，出現在父範本的 doctype 之前，這正是這條規則所針對的洩漏。`{% blocktrans %}` 區塊、`{% filter %}` 區塊和 `<?php ?>` 區塊也一樣會算在內，因為它們都會被渲染。只會檢查第一個 `{% extends %}`；第二個本身就是另一個錯誤。在 jinja 和 nunjucks profile 中，出現在它之前的分支標籤不算在內，因為 jinja 的說明文件將 `{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}` 記載為選擇父範本的方法；django 則會把範本的其餘部分讀入 `{% extends %}`，然後拒絕 `{% endif %}`，因此在該 profile 中，分支標籤會算在內。

不適用於 handlebars、golang、liquid 和 angular profile。

不要這樣寫：

```html
{% load static %}
{% extends "base.html" %}
```

應該這樣寫：

```html
{% extends "base.html" %}
{% load static %}
```

#### H042

`Label for attribute has no matching element id in this file.`

這項檢查只會在能夠可靠分析的檔案上執行：如果檔案中含有任何可能渲染出此檔案未顯示的 id 的內容（像表單小工具這樣的 `{{ ... }}` 輸出、`{% include %}` 或 `{% extends %}`，或無法辨識的範本標籤），這條規則就不會對該檔案回報任何結果。在它確實執行的地方，每一筆回報都是真正失效的關聯。

不要這樣寫：

```html
<label for="email">Email</label>
<input id="username">
```

應該這樣寫：

```html
<label for="email">Email</label>
<input id="email">
```

#### T042

`Content outside a block is not rendered in a template that extends another.`

範本一旦繼承了另一個範本，輸出的內容就由父範本決定，子範本只負責填入父範本的區塊。寫在 `{% extends %}` 之後、且位於所有 `{% block %}` 之外的文字或 html，會在渲染時被默默丟棄，因此在原始碼中看起來沒問題的段落，永遠不會出現在頁面上。

那裡的範本標籤仍會執行，因此 `{% load %}`、`{% set %}`，以及包住某個區塊的 `{% if %}` 都不會回報；`{# #}` 和 `{% comment %}` 註解、html 註解、<code>{&#37; raw %}</code> 和 `{% verbatim %}` 區塊，以及 `{% macro %}`、區塊形式的 `{% set %}`、`{% partialdef %}` 或 `{% addtoblock %}` 的主體（這些內容會被擷取而非輸出）也是如此。`{% blocktrans %}` 的文字會回報，因為 `{% blocktrans %}` 不是 `{% block %}`。只會考慮 extends 標籤之後的內容，而每一段連續的內容只會在其開頭回報一次。

引擎會先讀取範本標籤再處理 html，因此寫在 html 註解或 `<pre>` 內的 `{% extends %}` 仍會執行，檔案也仍會成為子範本；只有 `{# #}`、`{% comment %}`、<code>{&#37; raw %}</code> 和 `{% verbatim %}` 才能真正隱藏它。html 註解內的文字無論如何都不會被讀者看到，因此不會回報，但寫在那裡的標籤仍會被讀取。

不適用於 handlebars、golang、liquid 和 angular profile。

不要這樣寫：

```html
{% extends "base.html" %}
<p>This paragraph is never shown.</p>
{% block content %}
<h1>Welcome</h1>
{% endblock %}
```

應該這樣寫：

```html
{% extends "base.html" %}
{% block content %}
<h1>Welcome</h1>
<p>This paragraph is shown.</p>
{% endblock %}
```

#### H043

`Button tag should have a type attribute.`

沒有 `type` 的 `<button>` 預設為 `submit`，因此原本用來執行指令碼的按鈕，也會送出外圍的表單並重新載入頁面。明確寫出 type 就能避免這個問題。

不要這樣寫：

```html
<form>
  <button onclick="preview()">Preview</button>
</form>
```

應該這樣寫：

```html
<form>
  <button type="button" onclick="preview()">Preview</button>
</form>
```

#### T043

`Block name is used more than once in the template.`

Django、Jinja 和 Nunjucks 都拒絕剖析有兩個同名區塊的範本，因此頁面完全無法載入。引擎並不在乎這兩個區塊是否位於 `{% if %}` 的不同分支中，因此每個區塊名稱都必須在整個範本中唯一，不論區塊是並列的，還是一個巢狀在另一個之中。

只有 `{% block %}` 會被計算：`{% blocktrans %}` 不是區塊，而 `{% endblock name %}` 只是為它所關閉的區塊命名。名稱會依照寫法比較，因為引擎會將 `Content` 和 `content` 視為兩個區塊。

只有引擎本身從不剖析的內容才會被略過：範本註解、`{% comment %}` 區塊、<code>{&#37; raw %}</code> 或 `{% verbatim %}` 的主體，以及 `djlint:off` 區域。寫在 html 註解、`<script>`、`<style>`、`<pre>` 或 `<textarea>` 主體，或 `{% filter %}` 主體內的區塊仍會被計算，因為引擎會讀取這些內容，同樣會因重複的名稱而引發錯誤。

`{% embed %}` 會開啟自己的作用域：其中的區塊填入的是被嵌入的範本，而不是這個範本，因此同一個部分範本的兩次嵌入可以各自寫上 `{% block body %}`。在單一 embed 內重複的名稱仍會回報。

不適用於 handlebars、golang、liquid 和 angular profile。

不要這樣寫：

```html
{% block content %}{% endblock %}
{% block content %}{% endblock %}
```

應該這樣寫：

```html
{% block content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

#### H044

`Thead should not mix th and td cells.`

每一列都是單獨判斷的，因此 html 規格放在 `thead` 中、位於標題列旁邊的 `td` 說明列不算混用。位於列開頭的空 `td`，是第一欄為標題的表格的角落儲存格，這正是 W3C 無障礙教學所要求的標記，因此會被略過。

`th` 和 `td` 對螢幕閱讀器而言具有不同的意義，通常也有不同的 css，因此標題列中混入一個錯置的儲存格，會被當成資料讀出，樣式也會與旁邊的欄不同。這種混用是合法的 html，這正是它難以被發現的原因。

不要這樣寫：

```html
<thead>
  <tr>
    <th>Name</th>
    <td>Size</td>
  </tr>
</thead>
```

應該這樣寫：

```html
<thead>
  <tr>
    <th>Name</th>
    <th>Size</th>
  </tr>
</thead>
```

#### T044

`Output tag holds a statement keyword; use a block tag.`

不適用於 golang、handlebars 和 angular profile。

輸出標籤用來印出值，而 `if`、`for`、`url`、`include` 等都是屬於區塊標籤的陳述式。Django、Jinja 和 Nunjucks 都會以語法錯誤拒絕 `{{ if x }}`，而單獨的結束關鍵字（例如 `{{ endif }}`）會被當成一個不渲染任何內容的變數，它原本要關閉的區塊則保持開啟，因此頁面不是無法載入，就是顯示出條件原本應該隱藏的內容。

單獨的關鍵字是普通的變數名稱，因此 `{{ url }}`、`{{ url|default:"/" }}` 和 `{{ set.name }}` 不會回報。只有帶有引數的關鍵字才會回報，單獨出現的結束或分支關鍵字（例如 `{{ endif }}` 或 `{{ else }}`）也是。像 `if` 或 `for` 這樣的控制關鍵字不能作為運算式的開頭，因此跟在它後面的任何內容（包括運算子）都是引數，`{{ if -1 > count }}` 會回報。其餘的名稱同時也可以作為變數和函式，對它們而言，只有加上引號的字串或單字才算是引數，因此恰好以其中某個名稱開頭的運算式不予檢查：`{{ url ~ "/x" }}`、`{{ url if url else "#" }}`、`{{ url ? url : '#' }}`、`{{ block ('title') }}`、`{{ block .super }}` 和 `{{ filter [0] }}` 都不會回報。

<code>{&#37; raw %}</code> 或 `{% verbatim %}` 區塊的主體是文字而不是範本語法，因此會被略過，具名的形式 `{% verbatim vueapp %}...{% endverbatim vueapp %}` 也包括在內，所以以這種方式保護的 Vue 或 Handlebars `{{ }}` 不會回報。寫在區塊標籤引號引數內的 `{{ }}`，如 `{% trans "Write {{ if x }} instead" %}`，是引擎會印出的文字，同樣不予檢查。

不要這樣寫：

```html
{{ if user.is_active }}
```

應該這樣寫：

```html
{% if user.is_active %}
```

#### H045

`Iframe tag should have a title attribute.`

螢幕閱讀器會以 iframe 的無障礙名稱來宣告它。沒有名稱時，它會唸出框架的 url，或什麼都不唸，而且在進入之前無從得知嵌入的頁面是什麼。WCAG 將此歸在 4.1.2 名稱、角色、值之下，而 axe 和 html-validate 都預設內建這項檢查。

名稱可以來自 `title`、`aria-label` 或 `aria-labelledby`，三者任一都符合這條規則。由範本標籤寫入的名稱也算數，因此依頁面設定標題的框架不會回報。

不要這樣寫：

```html
<iframe src="/report/"></iframe>
```

應該這樣寫：

```html
<iframe src="/report/" title="Quarterly report"></iframe>
```

#### T045

`Template tag inside an html comment still runs; use a template comment to disable it.`

html 註解只會對瀏覽器隱藏標記，而不會對範本引擎隱藏。`<!-- {% include "debug.html" %} -->` 仍會渲染該檔案，而 `<!-- {% if debug %}...{% endif %} -->` 仍會進行求值，在 Django、Jinja、Nunjucks、Handlebars 和 Go 中都是如此，因此以這種方式註解掉的標籤會繼續執行，它寫出的內容會落在註解內，或者如果其中含有 `-->`，就會跳脫出註解。只有範本註解，也就是 Django 和 Jinja 中的 `{# #}`、Handlebars 中的 `{{! }}` 或 Go 中的 `{{/* */}}`，才能阻止標籤執行。

規則只回報陳述式標籤：在具備此語法的 profile 下的 `{% %}`，handlebars 的 section、close 或 partial，以及像 `{{if}}` 或 `{{end}}` 這樣的 Go 關鍵字。印到註解中的值，如 `<!-- built {{ version }} -->`，是刻意的用法，不予檢查；範本註解、`{% comment %}` 區塊或 raw 區塊內的標籤，以及 Internet Explorer 的條件式註解 `<!--[if IE]> ... <![endif]-->`（其主體是給它所指名瀏覽器的標記）也是如此。

單獨的 Go 關鍵字在其他所有引擎中都是普通的變數名稱，因此 `<!-- period {{ start }} to {{ end }} -->` 和 `<!-- Template: {{ template }} -->` 在 Django、Jinja、Nunjucks、Handlebars 和 Liquid 下都是值，只有在 `--profile golang` 下才會被當成陳述式。帶有 Go 運算元的關鍵字，如 `{{ if .X }}` 和 `{{ template "footer" . }}`，是其他引擎都不會印出的陳述式，在任何 profile 下都會回報。`{%` 同樣只會在具備此語法的引擎中被讀取，因此在 `--profile handlebars` 和 `--profile golang` 下它是文字；而後面沒有接上結束大括號的開頭，如 `<!-- battery at 50{% charge -->`，就是它看起來的那段普通文字。條件式註解是指以條件式註解形式寫成的註解：以 `<!--[if` 開頭，並以 `<![endif]-->`（不分大小寫）關閉；沒有關閉的條件式註解，就是瀏覽器所讀到的普通註解，其中的標籤會回報。

不要這樣寫：

```html
<!-- {% include "banner.html" %} -->
```

應該這樣寫：

```html
{# {% include "banner.html" %} #}
```

#### H046

`Tabindex should not be positive.`

正數的 `tabindex` 會把元素拉到 Tab 鍵順序的最前面，排在所有沒有設定 tabindex 的元素之前。只要有一個這樣的元素，就會為鍵盤使用者重新排列整個頁面，而之後每個新增控制項的範本，都必須手動維護這個順序。WCAG 將此歸在 2.4.3 焦點順序之下。

`0` 會讓元素依照它在文件中的位置加入 Tab 鍵順序，`-1` 則會將它移出順序，但仍可從指令碼取得焦點。這兩者都不會回報，由範本標籤寫入的值也不會回報，因為在這裡無法得知它的數字。

不要這樣寫：

```html
<input tabindex="1">
```

應該這樣寫：

```html
<input tabindex="0">
```

#### H047

`Aria-hidden should not be set on a focusable element.`

`aria-hidden="true"` 會將元素移出無障礙樹，但仍將它留在 Tab 鍵順序中，因此鍵盤使用者仍會移到它上面，卻聽不到任何宣告內容。隱藏裝飾性圖示是這個屬性的一般用法，不會回報；只有本身就能取得焦點的元素才會回報。

元素在下列情況下會被視為可取得焦點：它是 `button`、`select`、`textarea`、`iframe` 或 `summary`；帶有 `href` 的 `a` 或 `area`；非隱藏的 `input`；帶有 `controls` 的 `audio` 或 `video`；或任何帶有 `contenteditable` 或 `tabindex` 為 `0` 以上的元素。`disabled` 的控制項，或帶有 `tabindex="-1"` 的控制項，本來就不在 Tab 鍵順序中，因此不予檢查。

不要這樣寫：

```html
<button aria-hidden="true">Close</button>
```

應該這樣寫：

```html
<button type="button" aria-label="Close"><span aria-hidden="true">x</span></button>
```

#### H048

`Aria attribute is not one the specification defines.`

拼錯的 aria 屬性完全沒有作用。瀏覽器不會警告，螢幕閱讀器也不會回報，而標記看起來就像已經做好無障礙處理，因此 `aria-lable` 可能在範本中存在好幾年，而它原本要命名的控制項始終沒有名稱。

這條規則認得的名稱，就是 ARIA 所定義的名稱。由框架寫出的繫結不是單純的 aria 名稱，因此 `:aria-label`、`v-bind:aria-label` 和 `[attr.aria-label]` 不予檢查。

不要這樣寫：

```html
<button type="button" aria-lable="Close">x</button>
```

應該這樣寫：

```html
<button type="button" aria-label="Close">x</button>
```

#### H049

`Viewport should not stop the page being zoomed.`

`user-scalable=no`，以及小於 2 的 `maximum-scale`，會阻止頁面在手機上放大，而對許多人來說，這是閱讀頁面的唯一方法。WCAG 在 1.4.4 調整文字大小中要求支援 200%。瀏覽器越來越常忽略這項限制，但在仍遵守它的地方，這個標籤仍會關閉縮放功能。

不論 name 和 content 以何種順序撰寫，都能找到這兩者。

不要這樣寫：

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

應該這樣寫：

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### H050

`Element is obsolete and should be replaced.`

`<center>`、`<font>`、`<big>`、`<strike>` 和 `<tt>` 在 css 接手呈現工作後就被移除了，而 `<marquee>`、`<blink>`、`<nobr>` 和 `<spacer>` 則從來都不是標準。Html 已不再定義其中任何一個，因此無法保證瀏覽器會如何排版它們，而樣式表也無法像針對 class 那樣針對它們。

這條規則認得的元素有 `acronym`、`applet`、`basefont`、`bgsound`、`big`、`blink`、`center`、`dir`、`font`、`frame`、`frameset`、`isindex`、`keygen`、`marquee`、`menuitem`、`nobr`、`noembed`、`noframes`、`plaintext`、`spacer`、`strike`、`tt` 和 `xmp`。規則只回報開始標籤，因此每個元素只會指出一次，而名稱只是以其中某個名稱開頭的自訂元素，例如 `<font-picker>`，不予檢查。

不要這樣寫：

```html
<center><font color="red">Warning</font></center>
```

應該這樣寫：

```html
<p class="warning">Warning</p>
```

#### H051

`Role is not one ARIA defines for markup.`

沒有任何規格定義的 role 會被直接忽略，元素則保留原本的意義，因此 `role="buton"` 會讓 `<div>` 依然只是 `<div>`：對螢幕閱讀器毫無意義，而標記看起來卻像已經被賦予了用途。沒有任何東西會對此發出警告，這正是這種打字錯誤值得抓出來的原因。

這條規則認得的名稱，是 ARIA 為作者定義的角色，加上 DPUB-ARIA（`doc-chapter` 等）和 GRAPHICS-ARIA（`graphics-symbol` 等）所新增的角色。ARIA 的抽象角色，例如 `landmark` 和 `sectionhead`，會回報：規格表示它們的存在是為了建構其本體論，不得寫在標記中。

`role` 可以包含多個名稱作為備援清單，每一個都會被檢查。含有範本語法的值無法得知其內容，因此不予檢查；由框架寫出的繫結，如 `:role` 或 `[attr.role]`，也是如此。

不要這樣寫：

```html
<div role="buton">Save</div>
```

應該這樣寫：

```html
<button type="button">Save</button>
```

#### H052

`Meta refresh should not reload or redirect the page on a timer.`

計時重新整理會在讀者閱讀時把頁面抽走。閱讀速度較慢、使用螢幕閱讀器，或只是被打斷的人，會在沒有任何警告、也無法阻止的情況下失去閱讀位置，這不符合 WCAG 2.2.1 可調整時間；而重新載入同一頁面的重新整理，還會丟棄已經輸入的內容。

延遲為零是立即重新導向而不是計時器，在無法使用伺服器重新導向的情況下，WCAG 允許這種做法，因此不會回報。不論這兩個屬性以何種順序撰寫，都能找到它們。

不要這樣寫：

```html
<meta http-equiv="refresh" content="30">
```

應該這樣寫：

```html
<meta http-equiv="refresh" content="0; url=/next-page">
```

#### H053

`Id is used more than once in the file.`

一個 id 只命名一個元素。第二個帶有相同 id 的元素會破壞 `getElementById`、`<label for>`、片段連結和 `aria-labelledby`：瀏覽器會取第一個，並默默忽略其餘的，因此標籤、連結或指令碼會在沒有任何警告的情況下落在錯誤的元素上。

同一個 `{% if %}...{% else %}...{% endif %}` 中互斥分支內的兩個 id 永遠不會同時被渲染，因此不會回報。`{% for %}` 迴圈或 `{% block %}` 不是分支：位於其中的 id 和位於其外的相同 id 都會被渲染，後出現的那個會回報。由範本標籤寫入的值無法得知其內容，因此不予檢查；空值也是如此。id 會依照瀏覽器的做法精確比較，因此 `save` 和 `Save` 是兩個不同的 id。

分支會以檔案所使用的語言來讀取，分隔符號與標籤名稱之間也可以有該語言允許的任何空白：`{% elif %}` 和 `{% else %}`、liquid 的 `{% elsif %}` 和 `{% when %}`、go 的 `{{ else }}`、mako 的 `% else:` 行陳述式，以及 handlebars 的 `{{else}}`、其鏈式的 `{{else if x}}`，和任何 `{{#helper}}` 區塊（包括自訂 helper）的反向區段。`<template>` 的內容是一個獨立的文件片段，`getElementById` 永遠無法觸及，因此其中的 id 只會與同一個 `<template>` 內的 id 比較：兩個 template 可以各自含有相同 id 的一列，但同一個 template 內的兩個相同 id 仍會回報。註解、<code>{&#37; raw %}</code> 或 `{% verbatim %}` 主體，或 `djlint:off` 區域內的 id 完全不會被讀取。

不要這樣寫：

```html
<button type="submit" id="submit">Save</button>
<button type="submit" id="submit">Save and continue</button>
```

應該這樣寫：

```html
<button type="submit" id="submit">Save</button>
<button type="button" id="cancel">Cancel</button>
```

#### H054

`Interactive element should not be nested inside another.`

Html 禁止在 `<a>` 和 `<button>` 內放置互動內容。連結內的按鈕，或按鈕內的連結，是無效的標記，各家瀏覽器會以各自的方式修復，而螢幕閱讀器或鍵盤使用者拿到的，會是一個表現得像兩個控制項的控制項。axe 也會以「nested-interactive」回報相同的問題。

受監看的容器是帶有 `href` 的 `<a>` 和 `<button>`，而在其中會回報的控制項，是帶有 `href` 的連結、`button`、`input`、`select` 和 `textarea`。沒有 `href` 的 `<a>` 不是互動元素，不論在哪一邊都不予檢查；隱藏的 input，或 type 由範本標籤寫入的 input 也是如此。`<template>` 的內容不會在寫入的位置渲染，因此其中的控制項不算巢狀在外圍的連結內，不過寫在 template 內部的巢狀仍會回報。

只有在標籤寫出屬性的地方才會讀取屬性，其他地方都不會：`{% if not href %}` 中的 `href` 是變數名稱，`{# href="{{ url }}" #}` 中的那個已被註解掉，而 `data-attr=href` 中的那個屬於另一個屬性；但 `{% if %}` 在自己的標籤之間寫出的 `href`，就和其他屬性一樣。沒有關閉的連結或按鈕會隨著外圍的元素一起結束，就像在瀏覽器中一樣，因此一個打字錯誤不會導致檔案其餘部分都被回報；而在最上層沒有關閉的元素，外圍沒有任何元素可以結束它，因此確實會一直延續到檔案結尾，H025 也會在那裡回報這個孤立的標籤。

不要這樣寫：

```html
<a href="/cart"><button>Add</button></a>
```

應該這樣寫：

```html
<a href="/cart" class="button">Add</a>
```

#### H055

`Lang attribute should be a language tag such as en or pt-BR.`

H005 要求 `<html>` 上要有 `lang`，但像 `lang="english"` 或 `lang="en_US"` 這樣的值雖然滿足了它，卻沒有指名任何瀏覽器認得的語言。螢幕閱讀器會因此退回預設的語音，而翻譯和斷字會套用錯誤的規則，或完全沒有規則。這個值必須是 BCP 47 標記：兩到三個字母，接著是任意數量、各以連字號開頭、由一到八個字母或數字組成的子標記，如 `en`、`pt-BR` 或 `zh-Hant-TW`。

只會檢查 `<html>` 標籤，與 H005 一致。空值交由該規則處理，而只有空白的值則會在這裡被回報，因為 H005 將它視為有值。由範本標籤寫入的值，如 `lang="{{ LANGUAGE_CODE }}"`，或由 php 短 echo 寫入的值，如 `lang="<?= $lang ?>"`，無法得知其內容，因此不予檢查；但只是以 `$` 或 `{` 開頭的值，如 `lang="$LANG"`，則會依照寫法讀取。`xml:lang` 或 `data-lang` 不會被當作 `lang` 讀取，而寫在屬性之前的範本標籤內的 `>`，如 `{% if a > b %}`，也不會讓屬性被隱藏。

不要這樣寫：

```html
<html lang="english">
```

應該這樣寫：

```html
<html lang="en">
```

#### H056

`Src should not be empty.`

html 規格表示空的 `src` 是無效的，並警告瀏覽器會以文件本身的 url 來解析它，因此 `<img src="">` 會將頁面再次當成圖片抓取，而 `<script src=""></script>` 會將它當成指令碼抓取。它通常是原本要由指令碼填入的預留位置，修正方式是在有真正的值之前移除這個屬性，或將值放在 data 屬性中。完全沒有值的 `src`，如 `<img src>`，也是空的，同樣會回報。

只會檢查 `img`、`script`、`iframe`、`embed`、`source`、`track`、`audio` 和 `video`，因為這些是會抓取 `src` 所指名內容的元素。只有瀏覽器會讀成空值的值才會回報，因此像 `<img src=/static/logo.png>` 這樣沒有加引號的值不予檢查，只有空白的值和由範本標籤寫入的值也是如此；而 `srcset` 和 `data-src` 是不同的屬性，不在這條規則的判斷範圍內。

不要這樣寫：

```html
<img src="" alt="Logo">
```

應該這樣寫：

```html
<img src="{% static 'logo.png' %}" alt="Logo">
```

#### H057

`Video should have a captions track.`

有聲音的影片只在音訊中傳達語音，因此沒有字幕的話，聾人或聽障觀眾無法從中獲得任何內容，而 WCAG 1.2.2 字幕（預錄）要求提供字幕。`<video>` 內 `kind` 為 `captions` 或 `subtitles` 的 `<track>` 符合這條規則，完全沒有 `kind` 的 `<track>` 也符合，因為 `subtitles` 是預設值。

`muted` 的影片沒有需要加上字幕的音訊，不會回報。開始標籤或主體中含有範本標籤的影片也不會回報，因為字幕軌或 `muted` 屬性可能是由範本寫入，而 djLint 看不到。範本標籤是指範本語言所開啟的標籤，也就是 `{{`、`{%`、`{#` 或 `${`，因此像 `onclick="$(this).play()"` 這樣的 jQuery 處理常式、Alpine 的 `$refs`、css 的大括號，以及寫在備援文字中的價格，都是它們看起來的普通文字，影片仍會被讀取。

`muted` 必須是屬性，因此 `<video class=muted>` 是一個名為 muted 的 class，仍會回報；被註解掉或寫在屬性值內的 `<track>` 是文字，而不是字幕軌。值內的 `</video>` 不會結束任何東西，元素會在真正的結束標籤關閉它的地方被判斷，因此沒有關閉的 `<video>` 交由 `H025` 處理。

不要這樣寫：

```html
<video controls src="talk.mp4"></video>
```

應該這樣寫：

```html
<video controls src="talk.mp4">
  <track kind="captions" src="talk.vtt" srclang="en">
</video>
```

<!-- oxfmt-ignore-end -->

### 新增規則

我們歡迎提交新增規則的 pull request！

一條好的規則包含

- 名稱
- 代碼
- 訊息：發現錯誤時要顯示的訊息。
- 旗標：regex 旗標，例如 re.I|re.M。預設為 re.DOTALL。
- 模式：用來找出錯誤的正規表示式。
- 排除：此規則不適用的 profile 清單（選用）。

請附上驗證這條規則的測試。

## 自訂規則

你可以在 `pyproject.toml` 旁建立 `.djlint_rules.yaml`，為專案新增專屬的自訂規則。規則可以加到這個檔案中，djLint 就會讀取它們。位於其他位置的規則檔案，可以透過 `--rules` CLI 選項指定。

### 模式規則

你可以新增在任一 regex 模式比對成功時判定失敗的規則：

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Python 模組規則

你可以新增會匯入並執行自訂 Python 函式的規則：

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

指定的 `python_module` 必須包含一個 `run()` 函式，它會在每個受檢查的檔案上執行。它必須接受下列引數：

- `rule`：代表 `.djlint_rules.yaml` 中這條規則的 dict。你通常會用這個變數來取得規則名稱和訊息。
- `config`：DJLint 的設定物件。
- `html`：檔案的完整 html 內容。
- `filepath`：目前正在檢查的檔案路徑。
- `line_ends`：每一行 `start` 和 `end` 字元位置的清單，可搭配 `djlint.lint.get_line()` 從字元位置取得行號。請參閱範例。
- `*args, **kwargs`：我們未來可能會新增其他引數，因此你應該加上這兩個引數，以降低升級 djLint 時出錯的風險。

模組可以放在專案根目錄中。如果它傳回的 `line` 或 `end` 不是一個位置，djLint 就會停止並顯示指名該規則的錯誤。

它必須傳回一個 dict 清單，每個錯誤一個 dict，並包含下列鍵：

- `code`：回報錯誤的規則代碼名稱（通常是 `rule['name']`）
- `line`：行號以及該行中的字元位置，以 ':' 分隔，寫成字串。
  例如 `"2:3"` 表示錯誤是在第 2 行的第 3 個字元發現的
- `end`：選用。錯誤結束的位置，寫法與 `line` 相同，指向最後一個字元的下一個位置。若省略，錯誤會在 `match` 結束的位置結束。
- `match`：內容中含有錯誤的部分
- `message`：用來提示錯誤的訊息（通常是 `rule['message']`）

```python
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from djlint.helpers import inside_ignored_linter_block, inside_ignored_rule
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Any

    from djlint.settings import Config
    from djlint.types import LintError


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> list[LintError]:
    """當 html 檔案含有 'bad' 時判定失敗的規則。

    這只是一個範例，實際上同樣的事情用
    「模式規則」來做會簡單得多。
    """
    return [
        {
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "end": get_line(match.end(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        }
        for match in re.finditer(r"bad", html)
        if not inside_ignored_rule(config, html, match, rule["name"])
        and not inside_ignored_linter_block(config, html, match)
    ]
```
