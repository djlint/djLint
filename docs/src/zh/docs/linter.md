---
description: djLint HTML 模板的代码检查包括30余条规则！在这里可以查看它们的定义。使用自定义规则，可以轻松拓展它的功能！
title: 代码检查
keywords: 模板检查, 模板格式化, djLint, HTML, 模板语言, 格式化, 检查, 代码检查, 规则
---

# 代码检查

djLint 包含若干用于检查代码样式和验证模板语言的规则。添加你的配置文件，你可以充分利用该工具的功能。

```bash
djlint /path/to/templates --lint

# 使用自定义拓展
djlint /path/to/templates -e html.dj --profile=django

# 使用模板文件
djlint /path/to/this.html.j2  --profile=jinja
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block">详情请参考 <a href="{{ "lang_code_url" | i18n }}/docs/configuration/">配置</a> 章节</div>
</div>

## 启用或禁用某规则

大多数规则默认启用。规则可以在命令行中使用 `--ignore` 参数来禁用，也可以使用 `--include` 参数来启用。

示例:

```bash
djlint . --lint --include=H017,H035 --ignore=H013,H015
```

这样可以通过 [{{ "configuration" | i18n }}]({{ "lang_code_url" | i18n }}/docs/configuration) 文件来配置。

## 规则列表

| 编码 | 含义                                                                               | 默认行为 |
| ---- | ---------------------------------------------------------------------------------- | -------- |
| D004 | （Django） 静态 URL 应遵循 {% raw %}`{% static path/to/file %}`{% endraw %} 形式。 | ✔️       |
| D018 | （Django） 内部链接应使用 {% raw %}`{% url ... %}`{% endraw %} 形式。              | ✔️       |
| H005 | HTML 标签应包含 `lang` 属性。                                                      | ✔️       |
| H006 | `img` 标签应包含 `height` 和 `width` 属性。                                        | -        |
| H007 | `<!DOCTYPE ... >` 应在 HTML 标签之前。                                             | ✔️       |
| H008 | 属性应使用双引号。                                                                 | ✔️       |
| H009 | 标签名应小写。                                                                     | ✔️       |
| H010 | 属性名应小写。                                                                     | ✔️       |
| H011 | 属性值应加引号。                                                                   | ✔️       |
| H012 | 属性 `=` 周围不应有空格。                                                          | ✔️       |
| H013 | `img` 标签应有 `alt` 属性。                                                        | ✔️       |
| H014 | 存在超过两行的空行。                                                               | ✔️       |
| H015 | `h` 标签后换行。                                                                   | ✔️       |
| H016 | HTML 中可缺少 `title` 标签。                                                       | ✔️       |
| H017 | 空标签应为自闭合标签（与 H018 冲突）。                                             | -        |
| H018 | 空标签本质上是自闭合的，必须以“>”结尾，而非“/>”（与 H017 冲突）。                  | -        |
| H019 | 将 `javascript:abc()` 替换为 `on_` 事件和实际 URL。                                | ✔️       |
| H020 | 发现空标签对时考虑移除。                                                           | ✔️       |
| H021 | 应避免使用内联样式。                                                               | ✔️       |
| H022 | 外部链接应使用 HTTPS。                                                             | ✔️       |
| H023 | 不使用实体引用。                                                                   | ✔️       |
| H024 | 脚本和样式标签中可省略 `type` 属性。                                               | ✔️       |
| H025 | 标签可孤立存在。                                                                   | ✔️       |
| H026 | 空的 id 和 class 标签应被移除。                                                    | ✔️       |
| H029 | 建议使用小写表单方法值。                                                           | ✔️       |
| H030 | 建议添加 meta 描述。                                                               | ✔️       |
| H031 | 建议添加 meta 关键字。                                                             | -        |
| H033 | 表单 action 发现多余空格。                                                         | ✔️       |
| J004 | (Jinja) 静态 URL 应遵循 {% raw %}`{{ url_for('static'..) }}`{% endraw %} 形式。    | ✔️       |
| J018 | (Jinja) 内部链接应使用 {% raw %}`{% url ... %}`{% endraw %} 形式。                 | ✔️       |
| T001 | 变量外包含空格。示例：{% raw %}`{{ this }}`{% endraw %}                            | ✔️       |
| T002 | 标签中应使用双引号。示例：{% raw %}`{% extends "this.html" %}`{% endraw %}         | -        |
| T003 | `Endblock` 应包含名称。示例：{% raw %}`{% endblock body %}`{% endraw %}.           | -        |
| T027 | 模板语法中发现未闭合的字符串。.                                                    | ✔️       |
| T028 | 建议在属性值中使用无空格标签，例如：{% raw %}`{%- if/for -%}`{% endraw %}          | ✔️       |
| T032 | 模板标签中发现多余空格。                                                           | ✔️       |
| T034 | 使用 {% raw %}{% ... %} 代替 {% ... }%? {% endraw %}。                             | ✔️       |
| H035 | Meta 标签应自闭合。                                                                | -        |
| H036 | 避免使用 `<br>` 标签。                                                             | -        |
| H037 | 发现重复属性。                                                                     | ✔️       |
| T038 | 块标签没有匹配的结束标签。                                                         | ✔️       |
| T039 | 发现未闭合的模板标签。                                                             | ✔️       |
| T040 | extends 或 include 标签中缺少模板名或模板名为空。                                  | ✔️       |
| H041 | 标签在与打开它不同的模板块中关闭。                                                 | ✔️       |
| H042 | label 的 for 属性在此文件中没有匹配的元素 id。                                     | ✔️       |

### 编码规则

规则编码的第一个字母遵循如下规则。

::: content

- D: Django 专用
- H: HTML 适用
- J: Jinja 专用
- M: Handlebars 专用
- N: Nunjucks 专用
- T: 各模板语言通用
  :::

### 规则详情

<!-- prettier-ignore-start -->
<!-- the examples below are verified against djlint itself; prettier's html style would change what they demonstrate -->

{% raw %}

#### T001

`变量外包含空格。示例：{{ this }}`

像 `{{user.name}}` 这样内部不加空格的模板语法更难阅读和比对差异，而且整个代码库中空格风格不一致会让基于 grep 的重构（搜索某个变量或标签）变得不可靠，因为同一个表达式存在多种写法。Django 和 Jinja 的风格指南都采用带单个空格的 `{{ var }}` 和 `{% tag %}` 写法。

不适用于 handlebars 和 golang 配置文件。

错误示例：

```html
{{user.name}}
```

正确示例：

```html
{{ user.name }}
```

#### T002

`标签中应使用双引号。示例：{% extends "this.html" %}`

默认禁用；使用 `--include=T002` 启用。

在模板标签（`{% extends %}`、`{% include %}`、`{% with %}`、`{% trans %}`、`{% now %}`）中混用单引号和双引号，会让同一个模板名出现两种写法，导致搜索和批量重命名漏掉一半。统一使用双引号还能让标签参数与文件中其余 HTML 属性的引号风格保持一致。

HTML 属性值内部的单引号（例如 `<span title="{% trans 'x' %}">`）不会被标记，因为属性本身的双引号迫使那里只能使用单引号。

错误示例：

```html
{% extends 'base.html' %}
```

正确示例：

```html
{% extends "base.html" %}
```

#### T003

`Endblock 应包含名称。示例：{% endblock body %}.`

当 `{% block %}` 跨越多行或存在嵌套时，不带名称的 `{% endblock %}` 无法说明它闭合的是哪个块，编辑时很容易结束错误的块，子模板随之覆盖错误的内容。为 endblock 命名可以标明配对关系，让 djLint 和 Django（endblock 名称不匹配时会抛出 TemplateSyntaxError）都能发现闭合位置错误的块。配对错误（未闭合的块、孤立的 endblock 以及名称不匹配）属于正确性检查，由 T038 负责。

默认禁用；使用 `--include=T003` 启用。

当块在同一行内开始并结束时不要求命名，例如 `{% block title %}``{% endblock %}`。

错误示例：

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

正确示例：

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`（Django） 静态 URL 应遵循 {% static path/to/file %} 形式。`

硬编码 /static/ 路径会绕过 Django 的 `{% static %}` 标签，一旦 STATIC_URL 发生变化（例如把静态资源迁移到 CDN 或部署在子路径下），模板就会失效，也永远无法获取 ManifestStaticFilesStorage 生成的带哈希的文件名，从而在生产环境中导致 404 或加载到过期的缓存资源。

错误示例：

```html
<link rel="stylesheet" href="/static/css/style.css">
```

正确示例：

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) 静态 URL 应遵循 {{ url_for('static'..) }} 形式。`

硬编码 /static/ 路径会绕过 Flask/Jinja 的 url_for('static', ...)，当应用挂载在某个 URL 前缀下、或静态目录/主机发生变化时，资源就会 404，框架附加的缓存清除（cache-busting）查询串也会丢失。

错误示例：

```html
<link rel="stylesheet" href="/static/css/style.css">
```

正确示例：

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`HTML 标签应包含 lang 属性。`

如果 `<html>` 上没有 lang 属性，屏幕阅读器只能猜测发音规则，可能用错误的语言朗读页面，浏览器也无法正确提供翻译、断字或符合区域习惯的引号。声明页面语言是 WCAG 2.1 成功标准 3.1.1（A 级）的要求。

错误示例：

```html
<!DOCTYPE html>
<html>
</html>
```

正确示例：

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`img 标签应包含 height 和 width 属性。`

默认禁用；使用 `--include=H006` 启用。

当 `<img>` 没有 width 和 height 时，浏览器无法在图片下载前预留空间，图片加载过程中周围内容会随之跳动。这种布局偏移会恶化 Cumulative Layout Shift（Core Web Vitals 指标之一），还可能让用户在页面稳定前误点。

错误示例：

```html
<img src="cat.png" alt="Cat">
```

正确示例：

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > 应在 HTML 标签之前。`

如果 `<html>` 标签之前没有 `<!DOCTYPE>`，浏览器会以怪异模式（quirks mode）渲染页面，模拟遗留的盒模型和布局行为，导致 CSS 在不同浏览器中渲染不一致。位于 doctype 之前的模板标签和注释没有问题；只要求 `<html>` 标签本身位于其后。

错误示例：

```html
<html lang="en">
</html>
```

正确示例：

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`属性应使用双引号。`

混用引号风格让属性值更难阅读和检索，而且内容一旦含有撇号，单引号包裹的值就会出错。双引号是 HTML 规范、格式化工具和多数风格指南采用的惯例，统一使用双引号能让模板与更广泛的生态保持一致。

错误示例：

```html
<div class='content'></div>
```

正确示例：

```html
<div class="content"></div>
```

#### H009

`标签名应小写。`

HTML 解析器接受大写标签名，但 XHTML 和 XML 序列化是大小写敏感的，会拒绝它们；大小写混用还会让文本搜索和 diff 评审变得不可靠（grep `<h1>` 会漏掉 `<H1>`）。小写标签名让模板保持可移植且风格一致。

错误示例：

```html
<H1>Welcome</H1>
```

正确示例：

```html
<h1>Welcome</h1>
```

#### H010

`属性名应小写。`

大写属性名在 XHTML/XML 序列化中是非法的，还会让跨模板的文本搜索失效（grep src= 会漏掉 SRC=）。DOM 本来就会把 HTML 属性名规范化为小写，因此大写写法只带来不一致，没有任何好处。

错误示例：

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

正确示例：

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`属性值应加引号。`

不加引号的属性值到第一个空白字符就结束了，因此像 class=btn primary 这样的值会悄悄丢掉空格之后的所有内容（浏览器把 "primary" 当作一个独立的布尔属性）。来自模板变量的值尤其脆弱：渲染出的任何空格、"=" 或 ">" 都会破坏标签。加引号让值的边界明确而安全。

错误示例：

```html
<div class=test></div>
```

正确示例：

```html
<div class="test"></div>
```

#### H012

`属性 = 周围不应有空格。`

在 "=" 周围加空格后，标签会被读成三个独立的部分，而且离出错只有一步之遥：中间的一次换行或截断就会留下一个孤立的布尔属性加上零散文本。让 name="value" 保持连续也是简单文本工具（grep、查找替换）的默认假设，混杂的空格会让属性难以可靠地查找和重构。

错误示例：

```html
<div class = "test"></div>
```

正确示例：

```html
<div class="test"></div>
```

#### H013

`img 标签应有 alt 属性。`

没有 alt 属性时，屏幕阅读器会读出图片的文件名，或者什么都不读，违反 WCAG 1.1.1（非文本内容）。alt 文本也是图片加载失败时用户看到的内容。装饰性图片应显式写上空的 alt=""，让辅助技术知道跳过它们，这样写同样满足此规则。

错误示例：

```html
<img src="cat.jpg" height="200" width="300">
```

正确示例：

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`存在超过两行的空行。`

连续的空行对渲染后的页面没有任何影响（HTML 会折叠空白），却让模板变得臃肿，并在相邻行改动时产生嘈杂的 diff。djLint 的格式化工具默认会将其完全移除（最多保留 `max_blank_lines` 个空行，默认为 0），因此残留的连续空行说明代码未经格式化。

错误示例：

```html
<div>one</div>


<p>two</p>
```

正确示例：

```html
<div>one</div>

<p>two</p>
```

#### H015

`h 标签后换行。`

标题是定义文档大纲的块级地标；把下一个元素挤在闭合的 h 标签同一行会在源码中掩盖这种结构，还会让对其中任一元素的编辑在 diff 中表现为对两者的改动。每个标题后换行能让模板的视觉结构与渲染后的大纲保持一致。

错误示例：

```html
<h1>Heading</h1><p>Intro text.</p>
```

正确示例：

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`HTML 中可缺少 title 标签。`

HTML 规范要求每个文档都有 title 元素。缺少它时，浏览器标签页、书签和历史记录只能显示原始 URL 而非页面名称，搜索引擎失去页面的主要标签，屏幕阅读器用户也失去页面加载时最先播报的内容，违反 WCAG 2.4.2（页面标题，A 级）。

只对包含完整 `<html>`...`</html>` 文档的文件生效，因此局部模板和继承基础模板的子模板永远不会被标记。即使 SPA 外壳会在客户端设置标题，也仍然需要一个静态的 `<title>`：它是首次绘制时、爬虫眼中以及 JavaScript 失败时显示的内容。

错误示例：

```html
<html lang="en">
<body>Content</body>
</html>
```

正确示例：

```html
<html lang="en">
<head>
<title>My page</title>
</head>
<body>Content</body>
</html>
```

#### H017

`空标签应为自闭合标签（与 H018 冲突）。`

必须同时能按 XML/XHTML 解析（或供 XML 类工具消费）的模板会拒绝不带闭合斜杠的空元素，而在代码库中混用 `<br>` 和 `<br />` 会产生不一致的 diff。该规则强制采用 XHTML 风格的约定，让所有空元素以同一种方式闭合。

默认禁用；使用 `--include=H017` 启用。与 H018 互斥，两种约定只能启用其一。

错误示例：

```html
<br>
<meta charset="utf-8">
```

正确示例：

```html
<br />
<meta charset="utf-8" />
```

#### D018

`（Django） 内部链接应使用 {% url ... %} 形式。`

硬编码的内部 URL 会在 urls.py 中某个路由的路径变更时悄然失效，产生失效链接和提交到不存在地址的表单 action，而针对 URLconf 的任何测试都发现不了这一点。`{% url %}` 通过路由名称解析路径，因此重命名路径时所有链接会一并更新。

错误示例：

```html
<a href="/accounts/login">Login</a>
```

正确示例：

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`空标签本质上是自闭合的，必须以“>”结尾，而非“/>”（与 H017 冲突）。`

在 HTML 现行标准中，空元素末尾的斜杠没有任何含义（解析器会忽略它），因此写 `<br />` 暗示了 HTML 并不具备的 XML 式自闭合行为，还可能误导读者给非空元素也加上斜杠，而那里多余的 / 会被悄悄丢弃，掩盖未闭合标签的 bug。该规则强制空元素以纯 > 结尾。

默认禁用；使用 `--include=H018` 启用。与 H017 互斥，两种约定只能启用其一。SVG 的 `<path />` 不受约束，因为 SVG 是 XML，必须带斜杠。

错误示例：

```html
<br />
<meta charset="utf-8" />
```

正确示例：

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) 内部链接应使用 {% url ... %} 形式。`

硬编码的内部 URL 会在路由路径变更或应用挂载在前缀下时悄然失效，留下死链接和提交到 404 的表单 action。url_for() 根据端点名称构建 URL，因此路由变更会自动同步到所有模板。

错误示例：

```html
<a href="/accounts/login">Login</a>
```

正确示例：

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`将 javascript:abc() 替换为 on_ 事件和实际 URL。`

javascript: URL 会破坏鼠标中键点击和在新标签页打开，在 JavaScript 被禁用或加载失败时毫无作用，会被严格的内容安全策略（CSP）拦截，还是经典的 XSS 注入入口。href 应使用真实 URL，并改用事件处理器来附加行为。在严格 CSP 下，内联的 on* 处理器同样会被拦截：示例中的 onclick 只是模板内的最小修复；更好的做法是在脚本文件中用 addEventListener 绑定监听器。

错误示例：

```html
<a href="javascript:openPopup()">Open popup</a>
```

正确示例：

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`发现空标签对时考虑移除。`

空标签对不渲染任何内容，却仍会创建一个 DOM 节点，可能从样式表继承外边距、边框或 flex/grid 间距，产生难以追查的幽灵间距；它通常是先前编辑留下的残余标记。正常标记中合理为空的标签（td、th、li、dt、dd、slot）不受约束。带有任何属性的标签（例如 JS 挂载点 `<div id="app">``</div>`、图标字体元素 `<i class="fa fa-user">``</i>`）也不会被标记；只有完全不带属性的空标签对才会命中。

错误示例：

```html
<p>Saved.</p>
<span> </span>
```

正确示例：

```html
<p>Saved.</p>
```

#### H021

`应避免使用内联样式。`

内联样式的优先级高于任何样式表选择器，之后想覆盖它就得用 !important；在 style-src 不含 'unsafe-inline' 的内容安全策略下它们会被拦截；它们还把表现层散落在各个模板中，换主题或改设计意味着修改标记而非一份样式表。应把声明移到 CSS 类里。一个合理的例外：HTML 邮件模板（许多邮件客户端会剥离 `<style>` 块，内联样式是那里的标准做法），请排除你的邮件模板目录，或为其禁用此规则。

错误示例：

```html
<div style="color: red;">Wrong username or password.</div>
```

正确示例：

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`外部链接应使用 HTTPS。`

在通过 HTTPS 提供的页面上，纯 http:// 子资源属于混合内容：浏览器会直接拦截脚本、样式表和 iframe，并对图片自动升级或发出警告。指向 http:// 页面的 `<a>` 链接虽不算混合内容，但仍会把访问者送上易被窃听和篡改的未加密连接。指向确实没有 TLS 的内部主机的引用也会被标记；请用 `{# djlint:off H022 #}` 块局部静默这些位置，而不是禁用整条规则。

错误示例：

```html
<a href="http://example.com">Example</a>
```

正确示例：

```html
<a href="https://example.com">Example</a>
```

#### H023

`不使用实体引用。`

HTML5 文档采用 UTF-8，因此字面字符在任何地方都可用，也是评审者真正读到的内容；实体引用中的笔误（例如 `&mdsah;`）浏览器不会报错，而是原样渲染成一段乱码。djLint 只允许具有语法意义或在屏幕上不可见的实体，例如 `&lt;`、`&gt;`、`&amp;`、`&quot;`、`&nbsp;` 和 `&shy;`。

错误示例：

```html
<p>Dates 1900 &mdash; 2000</p>
```

正确示例：

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`脚本和样式标签中可省略 type 属性。`

text/javascript 和 text/css 是 HTML5 中 `<script>` 和 `<style>` 的默认值，这个属性只是浏览器会忽略的累赘，WHATWG 规范明确建议省略它。去掉它还能避免过时的 MIME 字符串在被复制到模块脚本（type="module" 真正起作用的地方）时破坏该元素。

错误示例：

```html
<script type="text/javascript" src="app.js">
```

正确示例：

```html
<script src="app.js"></script>
```

#### H025

`标签可孤立存在。`

缺少对应开始或闭合标签的标签会迫使浏览器的容错机制去猜测元素在哪里结束，后续标记就会被吞进错误的元素。布局、CSS 选择器和 JavaScript DOM 查询随之悄悄出错，而且在不同浏览器中表现各异。H025 还会报告在 `<p>` 内打开的 `<ol>` 或 `<ul>`：HTML 解析器会在列表之前先闭合段落，标记永远不会按书写的方式嵌套。

错误示例：

```html
<div>
  <p>Hello</p>
```

正确示例：

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`空的 id 和 class 标签应被移除。`

空的 id 或 class 属性毫无作用（没有样式或脚本能定位它），而且空的 id 是非法 HTML（id 值不得为空字符串）。它通常预示着一个模板 bug：本该在此插入某个变量，因此移除或补全它可以避免这个 bug 一直藏在眼皮底下。

错误示例：

```html
<div id="" class="">content</div>
```

正确示例：

```html
<div>content</div>
```

#### T027

`模板语法中发现未闭合的字符串。.`

在 `{% ... %}` 或 `{{ ... }}` 中打开却未闭合的引号会让模板引擎错误解析该标签：Django 和 Jinja 要么在渲染时抛出 TemplateSyntaxError，要么悄悄把标签剩余的参数当作字符串内容吞掉，结果页面报 500，或在缺失参数的情况下渲染。

错误示例：

```html
{% trans "Welcome %}
```

正确示例：

```html
{% trans "Welcome" %}
```

#### T028

`建议在属性值中使用无空格标签，例如：{%- if/for -%}`

属性值内部的模板标签会把标签周围的空白和换行原样输出到渲染后的属性中，因此用普通的 `{% if %}`/`{% for %}` 标签拼出来的 href 或 src 可能包含多余空格，产生损坏的 URL。Jinja/Nunjucks 的空白控制标签（`{%- ... -%}`）会去掉这些周围空白，让属性渲染为一个干净的值。class 属性不受此规则约束，因为类名之间的多余空白无伤大雅。

不适用于 django 配置文件：Django 模板标签不支持 `{%- -%}` 空白控制。

错误示例：

```html
<a href="{% if x %}/home{% endif %}"></a>
```

正确示例：

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`建议使用小写表单方法值。`

HTML 规范将表单 method 的关键字定义为小写（get、post）；浏览器只是通过大小写不敏感的回退匹配才接受大写变体。保持规范的小写形式让模板一致、便于 grep，也避免严格的校验器和基于 XHTML 的工具链报错。

错误示例：

```html
<form method="POST"></form>
```

正确示例：

```html
<form method="post"></form>
```

#### H030

`建议添加 meta 描述。`

搜索引擎用 meta description 作为搜索结果中页面标题下方的摘要；没有它时，搜索引擎会从页面的任意文本合成摘要，这会拉低点击率，页面被分享时也会产生糟糕的链接预览。

只对包含完整 `<html>`...`</html>` 文档的文件生效。摘要这一理由只适用于公开可被索引的页面；对于需要登录或内网的应用，通常会禁用此规则。

错误示例：

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

正确示例：

```html
<html lang="en">
  <head>
    <title>Home</title>
    <meta name="description" content="A short summary of this page.">
  </head>
  <body>Welcome</body>
</html>
```

#### H031

`建议添加 meta 关键字。`

默认禁用；使用 `--include=H031` 启用。

关键字元数据仍被一些站内搜索工具、内网索引器和较老的爬虫使用，因此从不声明 `<meta name="keywords">` 的页面对这些系统可能是不可见的。不过主流公共搜索引擎会忽略它，所以不依赖此类工具的团队通常会禁用此规则。

只对包含完整 `<html>...</html>` 文档的文件生效。

错误示例：

```html
<!DOCTYPE html>
<html lang="en">
<head>
<title>Home</title>
<meta name="description" content="A short summary.">
</head>
</html>
```

正确示例：

```html
<!DOCTYPE html>
<html lang="en">
<head>
<title>Home</title>
<meta name="description" content="A short summary.">
<meta name="keywords" content="django, templates">
</head>
</html>
```

#### T032

`模板标签中发现多余空格。`

模板标签参数之间连续的空格或制表符是看不见的噪音：它们会在 diff 中掩盖真正的差异，让人难以发现缺失的参数，还会偏离 djLint 格式化工具输出的单空格风格，造成无谓的重复格式化。引号字符串内部的空白会被保留，不会被标记。

错误示例：

```html
{% static  'css/style.css' %}
```

正确示例：

```html
{% static 'css/style.css' %}
```

#### H033

`表单 action 发现多余空格。`

表单 action 值中开头或结尾的空白会成为渲染后 URL 的一部分。浏览器解析时会去掉它，但直接使用字面值的非浏览器客户端和测试未必会；而 `{% url %}` 标签旁的多余空格几乎总是笔误的信号，会渲染出一个在服务端路由匹配中失败的提交 URL。

错误示例：

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

正确示例：

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`使用 {% ... %} 代替 {% ... }%? 。`

}% 几乎总是 %} 的笔误。模板引擎不会把 }% 识别为标签定界符，因此该标签根本不会被解析：原始的 {% ... }% 文本会泄漏到渲染后的 HTML 中，或者引擎在遇到这个未闭合的标签时抛出语法错误。

错误示例：

```html
{% include "footer.html" }%
```

正确示例：

```html
{% include "footer.html" %}
```

#### H035

`Meta 标签应自闭合。`

在纯 HTML5 中 `<meta>` 末尾的斜杠是可选的，但同时还要经过 XML/XHTML 工具（XML 校验器、邮件流水线、XSLT）处理的模板在空元素未自闭合时会解析失败。启用此规则让 `<meta>` 标签保持 XHTML 兼容的 `<meta ... />` 形式，同一份标记在两种解析器下都能存活。

默认禁用；使用 `--include=H035` 启用。它是 H017 的子集（H017 对包括 meta 在内的所有空标签强制尾部斜杠）；只有当你只想让 meta 采用 XHTML 形式时才单独启用 H035。与 H018 互斥；不要同时启用两者。

错误示例：

```html
<meta name="viewport" content="width=device-width">
```

正确示例：

```html
<meta name="viewport" content="width=device-width" />
```

#### H036

`避免使用 <br> 标签。`

`<br>` 把表现写进了标记：用它制造间距或伪造段落会破坏窄屏下的文本回流，也有损可访问性，因为屏幕阅读器会播报强制换行，而不是块与块之间的自然停顿。相互独立的内容应放进各自的块级元素，垂直间距应交给 CSS 外边距。注意，当换行本身就是内容的一部分时（邮政地址、诗歌、歌词），`<br>` 是合理的，而此规则无法区分这类用法与表现性用法：它会标记每一个 `<br>`。如果你的模板会渲染这类内容，请保持禁用。

默认禁用；使用 `--include=H036` 启用。

错误示例：

```html
<p>Shipping is free.<br>Delivery takes 3 days.</p>
```

正确示例：

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`发现重复属性。`

重复的属性是非法 HTML，浏览器只保留第一次出现的值并悄悄丢弃其余的，于是第二个 class 或 style 值永远不会生效，从而掩盖真正的 bug。该检查是模板感知的：在互斥分支（`{% if %}`/`{% else %}`）中重复出现的属性不会被标记，因为最终只会渲染其中一份。

错误示例：

```html
<div class="card" id="profile" class="active">...</div>
```

正确示例：

```html
<div class="card active" id="profile">...</div>
```

#### T038

`块标签没有匹配的结束标签。`

像 `{% if %}`、`{% for %}` 或 `{% macro %}` 这样的块标签如果缺少对应的结束标签，在 Django 和 Jinja 中会直接导致 TemplateSyntaxError：页面在请求时无法渲染，而该规则能在部署前发现这一问题。它还会标记没有对应开始标签的孤立结束标签，以及嵌套交错错误的块（例如 `{% if %}``{% for %}``{% endif %}`）。

`{% block %}`/`{% endblock %}` 的配对以及 endblock 名称不匹配由本规则检查；T003（默认禁用）额外要求每个多行 `{% endblock %}` 都带名称。通过 custom_blocks 注册的自定义块标签也会被检查，包括其自闭合的 / %} 形式。

错误示例：

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

正确示例：

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`发现未闭合的模板标签。`

以 `{{` 或 `{%` 开头、却没有用对应的 `}}` 或 `%}` 闭合的模板标签不会被当作标签解析：Django/Jinja 要么抛出 TemplateSyntaxError，要么把原始的大括号字符渲染进页面，而直到下一个定界符之前的内容都可能被悄悄吞掉。这类笔误（少写一个大括号、定界符不匹配）在代码评审中很容易被忽略，因为模板可能仍能部分渲染。

错误示例：

```html
<p>{{ user.name }</p>
```

正确示例：

```html
<p>{{ user.name }}</p>
```

#### T040

`extends 或 include 标签中缺少模板名或模板名为空。`

`{% extends %}` 或 `{% include %}` 标签的模板名缺失、为空或只含空白时，就没有任何可加载的内容：名称完全缺失时 Django 会抛出 TemplateSyntaxError，名称为空时会在渲染时抛出 TemplateDoesNotExist，因此即使模板文件本身看起来语法上说得过去，页面也会在生产环境中报 500。

错误示例：

```html
{% extends "" %}
```

正确示例：

```html
{% extends "base.html" %}
```

#### H041

`标签在与打开它不同的模板块中关闭。`

当一个 HTML 标签在某个 `{% block %}` 中打开、却在另一个块中闭合时，只覆盖其中一个块的子模板会继承半个元素，导致渲染页面中的标记不平衡：浏览器随即以不可预测的方式自动闭合或重新嵌套元素，使布局和 CSS 选择器在远离实际编辑的模板处出问题。让每个元素在同一个块内打开并闭合，才能保证每个块都可以被安全地独立覆盖。

错误示例：

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

正确示例：

```html
{% block content %}
<div class="wrapper">
</div>
{% endblock content %}
{% block footer %}
{% endblock footer %}
```

#### H042

`label 的 for 属性在此文件中没有匹配的元素 id。`

默认禁用；使用 --include=H042 启用。

该检查只在可以可靠分析的文件上运行：如果文件中包含任何可能渲染出本文件看不到的 id 的内容（如表单控件等 `{{ ... }}` 输出、`{% include %}` 或 `{% extends %}`、或无法识别的模板标签），该规则对此文件保持沉默。凡是它运行到的地方，报告都是真实的关联断裂。

错误示例：

```html
<label for="email">Email</label>
<input id="username">
```

正确示例：

```html
<label for="email">Email</label>
<input id="email">
```

{% endraw %}

<!-- prettier-ignore-end -->

### 添加规则

欢迎前来 PR 新规则！

优雅的规则应该包含

::: content

- Name
- Code
- Message - 报错信息。
- Flags - 正则表达式。默认为 re.DOTALL。 例如：re.I|re.M
- Patterns - 正则表达式将匹配的问题。
- Exclude - 可选的配置文件列表，用于排除特定规则。
  :::

请包含一个测试样例以验证该规则。

## 自定义规则

你可以在 `pyproject.toml` 相同路径下创建一个 `.djlint_rules.yaml` 来添加自定义规则。
也可以使用 CLI 选项 `--rules` 指定其他位置的规则文件。
你可以将规则添加到这个文件中，djLint 将会识别并应用这些规则。

### 形式规则

您可以添加规则，当其中一个正则表达式模式匹配成功时，该规则将判定为失败：

```yaml
- rule:
    name: T001
    message: 发现 Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Python 模块规则

您可以导入并执行自定义的 Python 函数来添加规则：

```yaml
- rule:
    name: T001
    message: 发现 `bad` 单词
    python_module: your_package.your_module
```

指定的 `python_module` 必须包含一个 `run()` 函数。
该函数会在每个被检查的文件中执行。它必须接受以下参数：

::: content

- `rule`: 表示 `.djlint_rules.yaml` 中规则的字典。通常使用此变量来访问规则的名称和提示信息。
- `config`: DJLint 的配置对象。
- `html`: 文件的完整 HTML 内容。
- `filepath`: 当前正在检查的文件的路径。
- `line_ends`: 行 `start` 和 `end` 字符位置的列表，可以与 `djlint.lint.get_line()` 结合使用，以从字符位置获取行号。请参考示例。
- `*args, **kwargs`: 未来可能会添加其他参数，因此应包含这两个参数以减少升级 djLint 时的失败风险。
  :::

该函数将返回一个字典列表，每个字典对应一个错误，并包含以下键：

::: content

- `code`: 报告错误的规则的代码名称（通常为 `rule['name']`）。
- `line`: 行号和该行的字符号，以字符串形式表示，中间用冒号 : 分隔。例如 `"2:3"` 表示错误出现在第 2 行第 3 个字符处。
- `match`: 包含错误的内容部分。
- `message`: 用于提示错误的消息（通常为 `rule['message']`）。
  :::

```python
from typing import Any, Dict, List
from djlint.settings import Config
from djlint.lint import get_line
import re


def run(
    rule: Dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: List[Dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> List[Dict[str, str]]:
    """
    如果 HTML 文件中包含 'bad'，则规则判定为失败。这只是一个示例，
    实际上，使用 `形式规则` 来实现会更简单。
    """
    errors: List[Dict[str, str]] = []
    for match in re.finditer(r"bad", html):
        errors.append({
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        })
    return errors
```
