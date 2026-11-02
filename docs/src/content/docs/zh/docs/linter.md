---
title: "代码检查规则"
description: "djLint HTML 模板代码检查工具包含 30 多条规则！在这里查看它们的定义。还可以通过自定义规则轻松扩展！"
sidebar:
  label: "代码检查工具"
---

djLint 包含许多规则，用于检查模板的风格和有效性。为你所选的模板语言配置相应的预设，即可充分发挥代码检查工具的作用。

```bash
djlint /path/to/templates --lint

# 使用自定义扩展名
djlint /path/to/templates -e html.dj --profile=django

# 或者检查单个文件
djlint /path/to/this.html.j2  --profile=jinja
```

:::tip
[查看配置指南，了解所有选项！](/zh/docs/configuration/)
:::

## 启用或禁用规则

大多数规则默认启用。可以在命令行中使用 `--ignore` 参数禁用规则，使用 `--include` 参数启用规则。

例如：

```bash
djlint . --lint --include=H006,H017 --ignore=H013,H015
```

也可以通过[配置](/zh/docs/configuration)文件完成同样的设置。

## 规则

| 代码 | 含义                                                                      | 默认 |
| ---- | ------------------------------------------------------------------------- | ---- |
| T001 | 变量两侧应有空白。例如：`{{ this }}`                                      | ✔️   |
| T002 | 标签中应使用双引号。例如 `{% extends "this.html" %}`                      | ✔️   |
| T003 | endblock 应带有名称。例如：`{% endblock body %}`。                        | -    |
| D004 | （Django）静态文件 URL 应遵循 `{% static path/to/file %}` 模式。          | ✔️   |
| J004 | （Jinja）静态文件 URL 应遵循 `{{ url_for('static'..) }}` 模式。           | ✔️   |
| H005 | html 标签应带有非空的 `lang` 属性。                                       | ✔️   |
| H006 | `img` 标签应带有 `height` 和 `width` 属性。                               | -    |
| H007 | html 标签之前应有 `<!DOCTYPE ... >`。                                     | ✔️   |
| H008 | 属性应使用双引号。                                                        | ✔️   |
| H009 | 标签名应为小写。                                                          | ✔️   |
| H010 | 属性名应为小写。                                                          | ✔️   |
| H011 | 属性值应加引号。                                                          | ✔️   |
| H012 | 属性的 `=` 两侧不应有空格。                                               | ✔️   |
| H013 | `img` 标签应带有 alt 属性。                                               | ✔️   |
| H014 | 空行数量超过了配置允许保留的数量。                                        | ✔️   |
| H015 | `h` 标签之后应换行。                                                      | ✔️   |
| H016 | html 中缺少 `title` 标签。                                                | ✔️   |
| H017 | 空元素标签应自闭合（与 H018 冲突）。                                      | -    |
| D018 | （Django）内部链接应使用 `{% url ... %}` 模式。                           | ✔️   |
| H018 | 空元素标签本身就是自闭合的，必须以 ">" 而不是 "/>" 结尾（与 H017 冲突）。 | -    |
| J018 | （Jinja）内部链接应使用 `{{ url_for() ... }}` 模式。                      | ✔️   |
| H019 | 将 `javascript:abc()` 替换为 `on_` 事件和真实的 URL。                     | ✔️   |
| H020 | 发现空的标签对。考虑将其删除。                                            | ✔️   |
| H021 | 应避免使用内联样式。                                                      | ✔️   |
| H022 | 外部链接应使用 HTTPS。                                                    | ✔️   |
| H023 | 不要使用实体引用。                                                        | ✔️   |
| H024 | 省略 script 和 style 上的 type。                                          | ✔️   |
| H025 | 标签似乎是孤立的。                                                        | ✔️   |
| H026 | 空的 id 和 class 可以删除。                                               | ✔️   |
| T027 | 在模板语法中发现未闭合的字符串。                                          | ✔️   |
| T028 | 考虑在属性值中使用无空白标签。`{%- if/for -%}`                            | -    |
| H029 | 考虑使用小写的表单 method 值。                                            | ✔️   |
| H030 | 考虑添加 meta description。                                               | ✔️   |
| T032 | 在模板标签中发现多余的空白。                                              | ✔️   |
| H033 | 在表单 action 中发现多余的空白。                                          | ✔️   |
| T034 | 你是想用 {% ... %} 而不是 {% ... }% 吗？                                  | ✔️   |
| H036 | 不要用 `br` 标签制造间距。                                                | ✔️   |
| H037 | 发现重复的属性。                                                          | ✔️   |
| T038 | 块标签没有匹配的结束标签。                                                | ✔️   |
| T039 | 发现未闭合的模板标签。                                                    | ✔️   |
| T040 | extends 或 include 标签中缺少模板名称或模板名称为空。                     | ✔️   |
| H041 | 标签的闭合位置与开启位置不在同一个模板块中。                              | ✔️   |
| T041 | extends 标签应是模板中的第一个标签。                                      | ✔️   |
| H042 | 在此文件中，label 的 for 属性没有对应 id 的元素。                         | ✔️   |
| T042 | 在继承其他模板的模板中，块之外的内容不会被渲染。                          | ✔️   |
| H043 | button 标签应带有 `type` 属性。                                           | ✔️   |
| T043 | 模板中同一个块名称被使用了不止一次。                                      | ✔️   |
| H044 | thead 中不应混用 `th` 和 `td` 单元格。                                    | ✔️   |
| T044 | 输出标签中包含语句关键字；请使用块标签。                                  | ✔️   |
| H045 | iframe 标签应带有 `title` 属性。                                          | ✔️   |
| T045 | html 注释中的模板标签仍会执行；请使用模板注释来禁用它。                   | ✔️   |
| H046 | tabindex 不应为正数。                                                     | ✔️   |
| H047 | 不应在可获得焦点的元素上设置 aria-hidden。                                | ✔️   |
| H048 | aria 属性不是规范中定义的属性。                                           | ✔️   |
| H049 | viewport 不应阻止页面缩放。                                               | ✔️   |
| H050 | 元素已过时，应予以替换。                                                  | ✔️   |
| H051 | role 不是 ARIA 为标记定义的角色。                                         | ✔️   |
| H052 | meta refresh 不应定时重新加载或重定向页面。                               | ✔️   |
| H053 | 文件中同一个 id 被使用了不止一次。                                        | ✔️   |
| H054 | 交互元素不应嵌套在另一个交互元素中。                                      | ✔️   |
| H055 | lang 属性应为语言标签，例如 en 或 pt-BR。                                 | ✔️   |
| H056 | src 不应为空。                                                            | ✔️   |
| H057 | video 应带有字幕轨道。                                                    | ✔️   |

### 代码规律

代码的首字母遵循以下规律：

- D：专用于 Django
- H：适用于 html
- J：专用于 Jinja
- M：专用于 Handlebars
- N：专用于 Nunjucks
- T：通用于各种模板

### 规则详情

<!-- oxfmt-ignore-start -->

#### T001

`Variables should be wrapped in a whitespace.`

`{{user.name}}` 这种内侧没有空白的模板语法更难浏览和比较差异；而且如果整个代码库的空格风格不一致，同一个表达式就会有多种写法，基于 grep 的重构（搜索某个变量或标签）也就变得不可靠。Django 和 Jinja 的风格指南都把它们写成 `{{ var }}` 和 `{% tag %}`，两侧各留一个空格。

不适用于 handlebars 和 golang 预设。

错误示例：

```html
{{user.name}}
```

正确示例：

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

如果在模板标签（`{% extends %}`、`{% include %}`、`{% with %}`、`{% trans %}`、`{% now %}`）中混用单引号和双引号，同一个模板名称就会出现两种写法，搜索和批量重命名都会漏掉一半。统一使用双引号，可以让标签参数与文件其余部分的 HTML 属性引号风格保持一致。

HTML 属性值中的单引号（例如 `<span title="{% trans 'x' %}">`）不会被报告，因为属性外层的双引号使那里只能使用单引号。

设置 `quote_style = "single"` 时，此规则会改为要求使用单引号，格式化工具也会写成单引号。

`--reformat` 会自动改写这些引号，因此任何检查结果都无需手动修复。

错误示例：

```html
{% extends 'base.html' %}
```

正确示例：

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

当一个 `{% block %}` 跨越很多行或者块相互嵌套时，单独的 `{% endblock %}` 看不出它关闭的是哪个块，编辑时很容易结束错块，导致子模板覆盖了错误的内容。为 endblock 写上名称，既能标明配对关系，也能让 djLint 和 Django（endblock 名称不匹配时会抛出 TemplateSyntaxError）发现关闭位置错误的块。配对错误（未闭合的块、孤立的 endblock 和名称不匹配）属于正确性检查，由 T038 负责。

默认关闭；使用 `--include=T003` 启用。`--name-endblocks` 会自动写入名称，因此任何检查结果都无需手动修复。

当块在同一行内开启和关闭时，不要求写名称，例如 `{% block title %}``{% endblock %}`。格式化工具会把包含其他标签的块的内容移到各自单独的行上，因此写在一行内的块在格式化后可能就需要名称了；使用 `--name-endblocks` 时，格式化工具也会写入该名称。

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

`(Django) Static urls should follow {% static path/to/file %} pattern.`

硬编码 /static/ 路径会绕过 Django 的 `{% static %}` 标签，因此当 STATIC_URL 改变时（例如把静态资源迁移到 CDN 或部署到子路径下）模板就会失效，而且永远用不上 ManifestStaticFilesStorage 生成的带哈希的文件名，导致生产环境中出现 404 或使用过期的缓存资源。此规则查找的是字面上的 `/static/` 前缀，因此从其他路径提供静态文件的项目不在检查范围内。

错误示例：

```html
<link rel="stylesheet" href="/static/css/style.css">
```

正确示例：

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

硬编码 /static/ 路径会绕过 Flask/Jinja 的 url_for('static', ...)，因此当应用挂载在某个 URL 前缀下，或者静态文件夹/主机发生变化时，静态资源就会返回 404，框架添加的缓存破坏（cache-busting）查询字符串也会丢失。此规则查找的是字面上的 `/static/` 前缀，因此从其他路径提供静态文件的项目不在检查范围内。

错误示例：

```html
<link rel="stylesheet" href="/static/css/style.css">
```

正确示例：

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have a non-empty lang attribute.`

如果 `<html>` 上没有 lang 属性，屏幕阅读器只能猜测发音规则，可能会用错误的语言朗读页面，浏览器也无法正确提供翻译、断字或符合区域习惯的引号。声明页面语言是 WCAG 2.1 成功标准 3.1.1（A 级）的要求。

`lang=""` 和没有值的 `lang` 都表示语言未知，因此它们与缺少该属性同样会被报告。

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

`Img tag should have height and width attributes.`

默认关闭；使用 `--include=H006` 启用。

如果 `<img>` 没有宽度和高度，浏览器就无法在图片下载之前预留空间，图片加载时周围的内容就会跳动。这种布局偏移会恶化累积布局偏移（Cumulative Layout Shift，Core Web Vitals 指标之一），还可能让用户在页面稳定下来之前点错位置。

错误示例：

```html
<img src="cat.png" alt="Cat">
```

正确示例：

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

如果 `<html>` 标签之前没有 `<!DOCTYPE>`，浏览器会以怪异模式（quirks mode）渲染页面，模拟旧式的盒模型和布局行为，导致 CSS 在不同浏览器中的渲染结果不一致。doctype 之前可以有模板标签和注释；只要求 `<html>` 标签本身之前必须有 doctype。

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

`Attributes should be double quoted.`

混用引号风格会让属性值更难浏览和 grep，而单引号括起的值一旦内容中包含撇号就会出错。双引号是 HTML 规范、格式化工具和大多数风格指南采用的惯例，统一使用双引号可以让模板与更广泛的生态保持一致。

错误示例：

```html
<div class='content'></div>
```

正确示例：

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

HTML 解析器接受大写的标签名，但 XHTML 和 XML 序列化区分大小写，会拒绝它们；而且大小写混用会让文本搜索和差异审查变得不可靠（grep `<h1>` 会漏掉 `<H1>`）。使用小写标签名可以让模板保持可移植和一致。

使用 `--ignore-case` 时不会报告，该选项让格式化工具不改动大小写。

错误示例：

```html
<H1>Welcome</H1>
```

正确示例：

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

大写的属性名在 XHTML/XML 序列化中无效，还会妨碍在模板中进行文本搜索（grep src= 会漏掉 SRC=）。DOM 本来就会把 HTML 属性名规范化为小写，因此大写写法只会带来不一致，没有任何好处。只有格式化工具会转为小写的属性名才会被报告：`class`、`id`、`src`、`width`、`height`、`alt`、`style`、`lang`、`title`、`media` 和 `srcset`。`--reformat` 会自动修复它们，而 `:itemID` 这样的框架绑定或 `data-ID` 这样更长的名称会保留原有的大小写。

使用 `--ignore-case` 时不会报告，该选项让格式化工具不改动大小写。

错误示例：

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

正确示例：

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

不加引号的属性值在第一个空白处结束，因此像 class=btn primary 这样的值会悄无声息地丢掉空格之后的所有内容（浏览器会把 "primary" 当作一个单独的布尔属性）。来自模板变量的值尤其脆弱：渲染出来的任何空格、"=" 或 ">" 都会破坏标签。加上引号可以明确并安全地界定值的边界。

错误示例：

```html
<div class=test></div>
```

正确示例：

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

如果 "=" 两侧有空格，标签读起来就像三个独立的词元，而且只差一次编辑就会散架：在中间换行或截断，就会留下一个光秃秃的布尔属性和一段多余的文本。保持 name="value" 连在一起，也是简单的文本工具（grep、搜索替换）所默认的写法，因此空格风格不一致会让属性难以可靠地查找和重构。`--reformat` 会自动删除这些空格。

错误示例：

```html
<div class = "test"></div>
```

正确示例：

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

如果没有 alt 属性，屏幕阅读器会读出图片的文件名，或者什么都不读，这不符合 WCAG 1.1.1（非文本内容）。图片加载失败时，用户看到的也是 alt 文本。装饰性图片应显式写上空的 alt=""，让辅助技术知道可以跳过它们；这样也满足此规则。

没有值的 `alt` 等同于 `alt=""`，即装饰性图片的情况，因此会被接受。

错误示例：

```html
<img src="cat.jpg" height="200" width="300">
```

正确示例：

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

连续的空行对渲染出的页面没有任何影响（HTML 会合并空白），却会让模板变得臃肿，并在相邻行发生变化时产生杂乱的差异。djLint 的格式化工具默认会把它们全部删除（最多保留 `max_blank_lines` 个空行，默认为 0），因此残留的连续空行说明代码还没有格式化。

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

`Follow h tags with a line break.`

标题是定义文档大纲的块级标志；把下一个元素挤在 h 结束标签的同一行，会在源码中掩盖这种结构，并且修改其中任何一个元素，在差异中都会显示为两者都有改动。在每个标题之后换行，可以让模板的视觉结构与渲染出的大纲保持一致。

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

`Missing title tag in html.`

HTML 规范要求每个文档都有 title 元素。如果没有，浏览器标签页、书签和历史记录中显示的就是原始 URL 而不是页面名称，搜索引擎会失去页面的主要标签，屏幕阅读器用户也会失去页面加载时首先播报的内容，这不符合 WCAG 2.4.2（页面标题，A 级）。

只在包含完整 `<html>`...`</html>` 文档的文件上触发，因此局部模板和继承基础模板的子模板永远不会被报告。在客户端设置标题的 SPA 外壳仍然需要一个静态的 `<title>`：首次绘制时、爬虫抓取时以及 JavaScript 运行失败时，显示的都是它。

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

`Void tags should be self closing.`

同时需要作为 XML/XHTML 解析（或输入给基于 XML 的工具）的模板，会拒绝没有闭合斜杠的空元素；而在代码库中混用 `<br>` 和 `<br />` 也会产生不一致的差异。此规则强制使用 XHTML 风格的惯例，让每个空元素都以相同的方式闭合。

默认关闭；使用 `--include=H017` 启用。与 H018 互斥；两种惯例只能启用其一。`--close-void-tags` 会自动为 html 空元素标签添加斜杠。svg 的 `<path>` 会保持原样，因此请手动闭合它。

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

`(Django) Internal links should use the {% url ... %} pattern.`

当 urls.py 中某个路由的路径改变时，硬编码的内部 URL 会悄无声息地失效，产生失效链接和无效的表单 action，而针对 URLconf 的任何测试都发现不了。`{% url %}` 根据路由名称解析路径，因此重命名路径时，所有链接都会同时更新。

错误示例：

```html
<a href="/accounts/login">Login</a>
```

正确示例：

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

在 HTML Living Standard 中，空元素末尾的斜杠没有任何意义（解析器会忽略它），因此写成 `<br />` 暗示了 HTML 并不具备的 XML 式自闭合行为，可能误导读者给非空元素也加上斜杠，而那里多余的 / 会被悄悄丢弃，从而掩盖标签未闭合的错误。此规则强制空元素以普通的 > 结尾。

默认关闭；使用 `--include=H018` 启用。与 H017 互斥；两种惯例只能启用其一。SVG 的 `<path />` 不受此规则约束，因为 SVG 是 XML，要求有斜杠。使用 `--close-void-tags` 时不会报告，因为此时格式化工具写入的正是此规则所报告的斜杠。

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

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

当路由的路径改变或应用挂载在某个前缀下时，硬编码的内部 URL 会悄无声息地失效，留下失效链接，表单 action 也会提交到 404 页面。url_for() 根据端点名称构建 URL，因此路由的变化会自动传递到每个模板。

错误示例：

```html
<a href="/accounts/login">Login</a>
```

正确示例：

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

javascript: URL 会破坏鼠标中键点击和“在新标签页中打开”，在 JavaScript 被禁用或加载失败时毫无作用，会被严格的内容安全策略（CSP）拦截，而且是典型的 XSS 注入点。请为 href 使用真实的 URL，并改用事件处理程序来附加行为。在严格的 CSP 下，内联的 on* 处理程序同样会被拦截：示例中的 onclick 只是模板内最小限度的修复；更好的做法是在脚本文件中使用 addEventListener 附加监听器。

错误示例：

```html
<a href="javascript:openPopup()">Open popup</a>
```

正确示例：

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

空的标签对不渲染任何内容，但仍会创建一个 DOM 节点，这个节点可能会从样式表中继承外边距、边框或 flex/grid 间隙，产生难以追查的幽灵间距；它通常是之前编辑时遗留下来的标记。在正常标记中本来就可以为空的标签（td、th、li、dt、dd、slot）不受此规则约束。带有任何属性的标签（例如 `<div id="app">``</div>` 这样的 JS 挂载点，`<i class="fa fa-user">``</i>` 这样的图标字体元素）也不会被报告；只有完全不带属性的空标签对才会匹配。

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

`Inline styles should be avoided.`

内联样式的优先级高于任何样式表选择器，因此之后要覆盖它们就得用 !important；在 style-src 中不含 'unsafe-inline' 的内容安全策略下，它们会被拦截；它们还会把表现层的代码分散到各个模板中，因此更换主题或修改设计时，就得去改标记，而不是只改一个样式表。请把声明移到 CSS 类中。有一个合理的例外：HTML 邮件模板，许多邮件客户端会剥离 `<style>` 块，内联样式是那里的标准做法；请排除你的邮件模板目录，或者为它们禁用此规则。

错误示例：

```html
<div style="color: red;">Wrong username or password.</div>
```

正确示例：

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

在通过 HTTPS 提供的页面上，普通的 http:// 子资源属于混合内容：浏览器会直接拦截脚本、样式表和 iframe，对图片则会自动升级或发出警告。指向 http:// 页面的 `<a>` 链接不算混合内容，但它仍会让访问者通过未加密的连接访问，容易遭到拦截和篡改。对确实没有 TLS 的内部主机的引用也会被报告；请用 `{# djlint:off H022 #}` 块让这些地方静默，而不要禁用此规则。

错误示例：

```html
<a href="http://example.com">Example</a>
```

正确示例：

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

HTML5 文档使用 UTF-8 编码，因此字面字符在任何地方都能正常使用，而且审查者实际读到的也是它；实体引用中的拼写错误（例如 `&mdsah;`）浏览器不会发现，而是原样渲染成错误的文本。djLint 允许承载语法的实体（`&lt;`、`&gt;`、`&amp;`、`&quot;`、`&apos;`，以及花括号 `&lbrace;` 和 `&rbrace;`，还有 `&percnt;`、`&num;` 和 `&dollar;`，这些字符直接写出来会凑成模板定界符），也允许表示不可见字符、因而无法以字面形式审查的实体：空格（`&nbsp;`、`&thinsp;`、`&hairsp;`）、连接符和方向标记（`&zwnj;`、`&zwj;`、`&lrm;`、`&rlm;`）以及 `&shy;`，无论是命名形式、十进制形式还是十六进制形式。

`--reformat` 会自动把实体改写为对应的字符，因此任何检查结果都无需手动修复。写在模板标签内的实体属于标签而不属于页面，因此此规则和格式化工具都不会处理它。`--no-entity-formatting` 会关闭这种改写，但不会关闭此规则，因此实体仍会被报告。要保留实体，请把 `H023` 添加到 `ignore` 中。

错误示例：

```html
<p>Dates 1900 &mdash; 2000</p>
```

正确示例：

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript 和 text/css 分别是 `<script>` 和 `<style>` 在 HTML5 中的默认值，因此这个属性是浏览器会忽略的冗余内容；WHATWG 规范明确要求省略它。去掉它还可以避免过时的 MIME 字符串被复制到模块脚本上（那里的 type="module" 真正起作用）而导致元素失效。

错误示例：

```html
<script type="text/javascript" src="app.js">
```

正确示例：

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

缺少对应开始标签或结束标签的标签，会迫使浏览器的错误恢复机制去猜测元素在哪里结束，于是后面的标记会被吞进错误的元素中；布局、CSS 选择器和 JavaScript DOM 查询随之悄无声息地出错，并且在不同浏览器中表现各异。H025 还会报告在 `<p>` 中开启的 `<ol>` 或 `<ul>`：HTML 解析器会在列表之前关闭段落，因此标记永远不会按照书写的方式嵌套。

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

`Empty id and class tags can be removed.`

任何 class 或 id 选择器都不会匹配空属性，而空的 id 是无效的 HTML（id 值不能是空字符串）。不过像 `div[class]` 这样的属性存在选择器仍会匹配它，因此对于以这种方式编写的样式表，删除这样的属性会产生可见的影响。它通常意味着模板中存在本该插入变量的错误，删除它或者填上值，可以避免这个错误藏在显眼处而无人察觉。

错误示例：

```html
<div id="" class="">content</div>
```

正确示例：

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

在 `{% ... %}` 或 `{{ ... }}` 中开启了却从未关闭的引号，会让模板引擎错误地解析该标签：Django 和 Jinja 要么在渲染时抛出 TemplateSyntaxError，要么悄悄把标签的其余参数当成字符串内容吞掉，结果页面返回 500，或者渲染时缺少参数。

错误示例：

```html
{% trans "Welcome %}
```

正确示例：

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

默认关闭；使用 `--include=T028` 启用。

无空白标签去除的空白是会被渲染出来的空白，因此只应在属性中没有可丢失的空白时使用。`alt="{%- if brand -%}Acme{%- endif -%} logo"` 会渲染为 `Acmelogo`，而 svg 的 `d="M12 {%- if big -%}20{%- endif -%} 4Z"` 会变成另一条路径。这就是此规则需要手动启用的原因。

属性值中的模板标签会把它们周围的空白和换行输出到渲染后的属性中，因此用普通的 `{% if %}`/`{% for %}` 标签拼出的 href 或 src 可能包含多余的空格，生成损坏的 URL。Jinja/Nunjucks 的空白控制标签（`{%- ... -%}`）会去除周围的空白，使属性渲染为一个干净的值。class 属性不受此规则约束，因为类名之间多余的空白是无害的。

不适用于 django 预设：Django 模板标签不支持 `{%- -%}` 空白控制。

错误示例：

```html
<a href="{% if x %}/home{% endif %}"></a>
```

正确示例：

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

HTML 规范将表单 method 关键字定义为小写（get、post）；浏览器只是通过不区分大小写的回退匹配来接受大写形式。保持规范的小写形式可以让模板保持一致、便于 grep，并避免严格的验证器和基于 XHTML 的工具链报错。

错误示例：

```html
<form method="POST"></form>
```

正确示例：

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

搜索引擎会把 meta description 用作搜索结果中页面标题下方的摘要；如果没有，它们会从页面中随意挑选文本拼成摘要，这会降低点击率，页面被分享时生成的链接预览也会很差。

只在包含完整 `<html>`...`</html>` 文档的文件上触发。关于摘要的理由只适用于公开索引的页面；对于需要登录的应用或内网应用，通常会禁用此规则。

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

#### T032

`Extra whitespace found in template tags.`

模板标签参数之间连续的空格或制表符是看不见的噪音：它们会在差异中掩盖真正的变化，让人难以发现缺失的参数，还会偏离 djLint 格式化工具输出的单空格风格，造成不必要的格式化改动。引号括起的字符串中的空白会保留，不会被报告。

错误示例：

```html
{% static  'css/style.css' %}
```

正确示例：

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

表单 action 值开头或结尾的空白会成为渲染后 URL 的一部分。浏览器在解析时会去掉它，但非浏览器客户端和直接使用字面值的测试可能不会；而在 `{% url %}` 标签周围，多余的空格几乎总是意味着一个笔误，它会渲染出一个无法通过服务器端路由匹配的提交 URL。

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

`Did you intend to use {% ... %} instead of {% ... }%?`

}% 几乎总是 %} 的笔误。模板引擎不会把 }% 识别为标签定界符，因此这个标签永远不会被解析：原始的 {% ... }% 文本会泄漏到渲染后的 HTML 中，或者引擎在遇到这个未闭合的标签时抛出语法错误。

错误示例：

```html
{% include "footer.html" }%
```

正确示例：

```html
{% include "footer.html" %}
```

#### H036

`Do not use br tags for spacing.`

html 规范只允许把 `<br>` 用于属于内容本身的换行，例如邮政地址或诗歌中的换行，这种用法不会被报告。被报告的是规范所禁止的表现性用法：连续两个或更多的换行（这是在制造垂直间距），以及紧贴块级元素内侧边缘的换行（它渲染出的效果，元素自身的外边距本来就能做到）。这两种用法都会在窄屏下破坏文本重排，屏幕阅读器还会在没有任何内容可播报的地方播报一次强制换行。

错误示例：

```html
<p>Shipping is free.<br><br>Delivery takes 3 days.</p>
```

正确示例：

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

重复的属性是无效的 HTML，浏览器只保留第一次出现的属性，并悄悄丢弃其余的，因此第二个 class 或 style 值永远不会生效，从而掩盖了真正的错误。此检查能够识别模板语法：在互斥分支（`{% if %}`/`{% else %}`）中重复出现的属性不会被报告，因为只有一份会被渲染。

错误示例：

```html
<div class="card" id="profile" class="active">...</div>
```

正确示例：

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

在 Django 和 Jinja 中，缺少对应结束标签的块标签（例如 `{% if %}`、`{% for %}` 或 `{% macro %}`）是硬性的 TemplateSyntaxError：页面会在请求时渲染失败，而此规则能在部署之前发现它。它还会报告没有开始标签的孤立结束标签，以及错误交错的块（例如 `{% if %}``{% for %}``{% endif %}`）。

`{% block %}`/`{% endblock %}` 的配对以及 endblock 名称不匹配都由此规则检查；T003（默认关闭）还会额外要求每个跨多行的 `{% endblock %}` 都带有名称。通过 custom_blocks 注册的自定义块标签也会被检查，包括其自闭合的 / %} 形式。

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

`Unclosed template tag found.`

以 `{{` 或 `{%` 开启、却从未用对应的 `}}` 或 `%}` 关闭的模板标签不会被解析为标签：Django/Jinja 要么抛出 TemplateSyntaxError，要么把原始的花括号字符渲染到页面中，而且直到下一个定界符之前的所有内容都可能被悄悄吞掉。这类笔误（少了一个花括号、定界符不匹配）在审查时很容易被忽略，因为模板可能仍然能部分渲染。

错误示例：

```html
<p>{{ user.name }</p>
```

正确示例：

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

模板名称缺失、为空或只包含空白的 `{% extends %}` 或 `{% include %}` 标签没有任何内容可加载：名称完全缺失时，Django 会抛出 TemplateSyntaxError；名称为空时，则会在渲染时抛出 TemplateDoesNotExist。因此，即使模板文件本身在语法上看起来没有问题，页面在生产环境中也会返回 500。

错误示例：

```html
{% extends "" %}
```

正确示例：

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

如果一个 HTML 标签在某个 `{% block %}` 中开启，却在另一个块中关闭，那么只覆盖其中一个块的子模板就只会继承这个元素的一半，导致渲染后的页面中标记不平衡；浏览器随后会以无法预测的方式自动关闭或重新嵌套元素，在远离实际编辑过的模板的地方破坏布局和 CSS 选择器。让每个元素都在同一个块内开启和关闭，可以确保每个块都能被安全地单独覆盖。

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

#### T041

`Extends tag should be the first tag in the template.`

如果模板中有其他标签出现在 `{% extends %}` 之前，Django 会拒绝编译该模板；而写在它之前的文本会被渲染，因此会泄漏到页面中，出现在父模板输出的所有内容之前。Jinja 也会渲染这些文本，nunjucks 则会丢弃它们，因此无论在哪个引擎中，模板的实际行为都与看上去不一样。

`{# #}` 注释不渲染任何内容，因此不算在内；`{% comment %}`、<code>{&#37; raw %}</code> 或 `{% verbatim %}` 块（无论是否带名称）中的任何内容、三种写法中任意一种的 `{# djlint:off #}` 区域以及 yaml front matter 也都不算。html 注释则要算在内：引擎会把它写入页面，出现在父模板的 doctype 之前，这正是此规则所针对的泄漏。`{% blocktrans %}` 块、`{% filter %}` 块和 `<?php ?>` 块同样要算，因为它们都会被渲染。只检查第一个 `{% extends %}`；第二个本身就是一个错误。在 jinja 和 nunjucks 预设中，出现在它之前的分支标签不算在内，因为 jinja 的文档将 `{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}` 作为选择父模板的方式；而 django 会把模板的其余部分读入 `{% extends %}`，然后拒绝 `{% endif %}`，因此在 django 预设中，分支标签要算在内。

不适用于 handlebars、golang、liquid 和 angular 预设。

错误示例：

```html
{% load static %}
{% extends "base.html" %}
```

正确示例：

```html
{% extends "base.html" %}
{% load static %}
```

#### H042

`Label for attribute has no matching element id in this file.`

此检查只在能够可靠分析的文件上运行：如果文件中包含任何可能渲染出本文件中看不到的 id 的内容（例如表单控件这样的 `{{ ... }}` 输出、`{% include %}` 或 `{% extends %}`，或者无法识别的模板标签），此规则就不会对该文件报告任何内容。在它运行的地方，每一条报告都是真实存在的关联断开。

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

#### T042

`Content outside a block is not rendered in a template that extends another.`

一旦一个模板继承了另一个模板，输出什么就由父模板决定，子模板只负责填充父模板的块。写在 `{% extends %}` 之后、所有 `{% block %}` 之外的文本或 html 会在渲染时被悄悄丢弃，因此在源码中看起来没问题的段落永远不会出现在页面上。

那里的模板标签仍会执行，因此 `{% load %}`、`{% set %}` 以及包裹在块外面的 `{% if %}` 都不会被报告；`{# #}` 和 `{% comment %}` 注释、html 注释、<code>{&#37; raw %}</code> 和 `{% verbatim %}` 块，以及 `{% macro %}`、块形式的 `{% set %}`、`{% partialdef %}` 或 `{% addtoblock %}` 的主体（它们的内容会被捕获而不是输出）也同样不会被报告。`{% blocktrans %}` 的文本会被报告，因为 `{% blocktrans %}` 并不是 `{% block %}`。只考虑 extends 标签之后的内容，每一段连续的内容只在其开头报告一次。

引擎先于 html 读取模板标签，因此写在 html 注释或 `<pre>` 中的 `{% extends %}` 仍会执行，仍会让该文件成为子模板；只有 `{# #}`、`{% comment %}`、<code>{&#37; raw %}</code> 和 `{% verbatim %}` 才能真正把它隐藏起来。html 注释中的文本无论如何都不会被任何读者看到，因此不会被报告，但写在那里的标签仍会被读取。

不适用于 handlebars、golang、liquid 和 angular 预设。

错误示例：

```html
{% extends "base.html" %}
<p>This paragraph is never shown.</p>
{% block content %}
<h1>Welcome</h1>
{% endblock %}
```

正确示例：

```html
{% extends "base.html" %}
{% block content %}
<h1>Welcome</h1>
<p>This paragraph is shown.</p>
{% endblock %}
```

#### H043

`Button tag should have a type attribute.`

没有 `type` 的 `<button>` 默认是 `submit`，因此原本用来运行脚本的按钮也会提交它所在的表单，导致页面重新加载。明确写出 type 可以避免这种情况。

错误示例：

```html
<form>
  <button onclick="preview()">Preview</button>
</form>
```

正确示例：

```html
<form>
  <button type="button" onclick="preview()">Preview</button>
</form>
```

#### T043

`Block name is used more than once in the template.`

Django、Jinja 和 Nunjucks 都会拒绝解析两个块同名的模板，因此页面根本无法加载。引擎并不在意这两个块是否位于 `{% if %}` 的不同分支中，因此每个块名称在整个模板中都必须唯一，无论这些块是并列的，还是一个嵌套在另一个之中。

只有 `{% block %}` 才算：`{% blocktrans %}` 不是块，而 `{% endblock name %}` 只是标明它所关闭的块。名称按书写形式进行比较，因为引擎会把 `Content` 和 `content` 视为两个块。

只跳过引擎本身从不解析的内容：模板注释、`{% comment %}` 块、<code>{&#37; raw %}</code> 或 `{% verbatim %}` 的主体，以及 `djlint:off` 区域。写在 html 注释、`<script>`、`<style>`、`<pre>` 或 `<textarea>` 的主体，或者 `{% filter %}` 主体中的块仍会被计入，因为引擎会读取所有这些内容，并且照样会因为名称重复而报错。

`{% embed %}` 会开启一个独立的作用域：其中的块填充的是被嵌入的模板而不是当前模板，因此对同一个局部模板的两次 embed 可以各自写一个 `{% block body %}`。在同一个 embed 内部重复的名称仍会被报告。

不适用于 handlebars、golang、liquid 和 angular 预设。

错误示例：

```html
{% block content %}{% endblock %}
{% block content %}{% endblock %}
```

正确示例：

```html
{% block content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

#### H044

`Thead should not mix th and td cells.`

每一行都会单独判断，因此 html 规范在 `thead` 中放在表头行旁边的那一行由 `td` 组成的说明行，不算混用。行首的空 `td` 是第一列为表头的表格的角单元格，这正是 W3C 无障碍教程所要求的标记，因此会被跳过。

`th` 和 `td` 对屏幕阅读器而言含义不同，通常 css 也不同，因此表头行中一个多余的单元格会被读作数据，样式也与旁边的列不一样。这种混用是合法的 html，这也正是它难以被发现的原因。

错误示例：

```html
<thead>
  <tr>
    <th>Name</th>
    <td>Size</td>
  </tr>
</thead>
```

正确示例：

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

不适用于 golang、handlebars 和 angular 预设。

输出标签用于打印一个值，而 `if`、`for`、`url`、`include` 等是语句，应该放在块标签中。Django、Jinja 和 Nunjucks 都会以语法错误拒绝 `{{ if x }}`；而单独的结束关键字（例如 `{{ endif }}`）会被当作一个不渲染任何内容的变量，它本应关闭的块则仍处于开启状态，因此页面要么无法加载，要么显示出本应被条件隐藏的内容。

单独的关键字是一个普通的变量名，因此 `{{ url }}`、`{{ url|default:"/" }}` 和 `{{ set.name }}` 不会被报告。只有带参数的关键字才会被报告，此外还有单独出现的结束或分支关键字，例如 `{{ endif }}` 或 `{{ else }}`。`if` 或 `for` 这样的控制关键字不能作为表达式的开头，因此其后的任何内容（包括运算符）都是参数，`{{ if -1 > count }}` 会被报告。其余的名称同时也可以用作变量和函数，对它们而言，只有带引号的字符串或单词才算参数，因此恰好以其中某个名称开头的表达式不会被报告：`{{ url ~ "/x" }}`、`{{ url if url else "#" }}`、`{{ url ? url : '#' }}`、`{{ block ('title') }}`、`{{ block .super }}` 和 `{{ filter [0] }}` 都不会被报告。

<code>{&#37; raw %}</code> 或 `{% verbatim %}` 块的主体是文本而不是模板语法，会被跳过，带名称的形式 `{% verbatim vueapp %}...{% endverbatim vueapp %}` 也一样，因此以这种方式保护起来的 Vue 或 Handlebars `{{ }}` 不会被报告。写在块标签带引号的参数中的 `{{ }}`，例如 `{% trans "Write {{ if x }} instead" %}`，是引擎会原样打印的文本，同样不会被报告。

错误示例：

```html
{{ if user.is_active }}
```

正确示例：

```html
{% if user.is_active %}
```

#### H045

`Iframe tag should have a title attribute.`

屏幕阅读器通过可访问名称来播报 iframe。如果没有名称，它会读出框架的 url，或者什么都不读，用户在进入之前无从得知嵌入的是什么页面。WCAG 将此归入 4.1.2 名称、角色、值，axe 和 html-validate 也都默认提供此项检查。

名称可以来自 `title`、`aria-label` 或 `aria-labelledby`，三者中任何一个都能满足此规则。由模板标签写入的名称也算，因此按页面设置标题的框架不会被报告。

错误示例：

```html
<iframe src="/report/"></iframe>
```

正确示例：

```html
<iframe src="/report/" title="Quarterly report"></iframe>
```

#### T045

`Template tag inside an html comment still runs; use a template comment to disable it.`

html 注释只能对浏览器隐藏标记，却瞒不过模板引擎。在 Django、Jinja、Nunjucks、Handlebars 和 Go 中，`<!-- {% include "debug.html" %} -->` 照样会渲染该文件，`<!-- {% if debug %}...{% endif %} -->` 照样会求值，因此用这种方式注释掉的标签会继续运行，它写出的内容会落在注释之中；如果其中含有 `-->`，还会跳出注释。只有模板注释才能阻止标签运行：Django 和 Jinja 中的 `{# #}`、Handlebars 中的 `{{! }}` 或 Go 中的 `{{/* */}}`。

只报告语句标签：`{% %}`（在支持它的预设下）、handlebars 的 section、关闭标签或 partial，以及 `{{if}}` 或 `{{end}}` 这样的 Go 关键字。打印到注释中的值（例如 `<!-- built {{ version }} -->`）属于有意为之的用法，不会被报告；模板注释、`{% comment %}` 块或 raw 块中的标签，以及面向 Internet Explorer 的条件注释 `<!--[if IE]> ... <![endif]-->`（其主体是供它所指定的浏览器使用的标记）也不会被报告。

在其他所有引擎中，单独的 Go 关键字都是普通的变量名，因此 `<!-- period {{ start }} to {{ end }} -->` 和 `<!-- Template: {{ template }} -->` 在 Django、Jinja、Nunjucks、Handlebars 和 Liquid 下都是值，只有在 `--profile golang` 下才会被当作语句。带有 Go 操作数的关键字（例如 `{{ if .X }}` 和 `{{ template "footer" . }}`）是其他引擎都不会打印的语句，在任何预设下都会被报告。同样，`{%` 只在支持它的引擎中才会被识别，因此在 `--profile handlebars` 和 `--profile golang` 下它是文本；后面没有闭合花括号的开头，例如 `<!-- battery at 50{% charge -->`，就是它看上去的那段普通文字。条件注释是指确实按条件注释书写的注释：以 `<!--[if` 开头，并由对应的 `<![endif]-->` 关闭（大小写不限）；未闭合的条件注释就是浏览器眼中的普通注释，其中的标签会被报告。

错误示例：

```html
<!-- {% include "banner.html" %} -->
```

正确示例：

```html
{# {% include "banner.html" %} #}
```

#### H046

`Tabindex should not be positive.`

正数的 `tabindex` 会把元素提到 Tab 键顺序的最前面，排在所有没有设置它的元素之前。只要有一个这样的元素，就会为键盘用户打乱整个页面的顺序，之后每个添加控件的模板都必须手动维护这个顺序。WCAG 将此归入 2.4.3 焦点顺序。

`0` 会让元素按照它在文档中的位置进入 Tab 键顺序，`-1` 会把元素移出 Tab 键顺序，但仍可通过脚本使其获得焦点。这两个值都不会被报告，由模板标签写入的值也不会被报告，因为这里无法得知它的数值。

错误示例：

```html
<input tabindex="1">
```

正确示例：

```html
<input tabindex="0">
```

#### H047

`Aria-hidden should not be set on a focusable element.`

`aria-hidden="true"` 会把元素移出无障碍树，但它仍留在 Tab 键顺序中，因此键盘用户仍会定位到它，却听不到任何播报。隐藏装饰性图标是这个属性的正常用法，不会被报告；只有本身能获得焦点的元素才会被报告。

以下元素被视为可获得焦点：`button`、`select`、`textarea`、`iframe` 或 `summary`，带有 `href` 的 `a` 或 `area`，非隐藏的 `input`，带有 `controls` 的 `audio` 或 `video`，以及任何带有 `contenteditable` 或 `tabindex` 为 `0` 及以上的元素。`disabled` 的控件或带有 `tabindex="-1"` 的控件本来就不在 Tab 键顺序中，不会被报告。

错误示例：

```html
<button aria-hidden="true">Close</button>
```

正确示例：

```html
<button type="button" aria-label="Close"><span aria-hidden="true">x</span></button>
```

#### H048

`Aria attribute is not one the specification defines.`

拼错的 aria 属性完全不起作用。浏览器不会警告，屏幕阅读器也不会报告，标记看上去却像是已经做过无障碍处理，因此 `aria-lable` 可能在模板中存在好几年，而它本应命名的控件始终没有名称。

此规则认识的名称就是 ARIA 所定义的名称。由框架写出的绑定不是普通的 aria 名称，因此 `:aria-label`、`v-bind:aria-label` 和 `[attr.aria-label]` 不会被报告。

错误示例：

```html
<button type="button" aria-lable="Close">x</button>
```

正确示例：

```html
<button type="button" aria-label="Close">x</button>
```

#### H049

`Viewport should not stop the page being zoomed.`

`user-scalable=no` 以及小于 2 的 `maximum-scale` 会阻止在手机上放大页面，而对很多人来说，放大是阅读页面的唯一方式。WCAG 在 1.4.4 调整文本大小中要求支持 200% 缩放。浏览器越来越多地忽略这种限制，但在仍然遵守它的地方，这个标签依然会关闭缩放。

无论 name 和 content 以何种顺序书写，都能被找到。

错误示例：

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

正确示例：

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### H050

`Element is obsolete and should be replaced.`

`<center>`、`<font>`、`<big>`、`<strike>` 和 `<tt>` 在 css 接管表现层之后就被废弃了，而 `<marquee>`、`<blink>`、`<nobr>` 和 `<spacer>` 从来就不是标准。如今 html 已不再定义其中任何一个，因此无法保证浏览器会如何布局它们，样式表也无法像选择 class 那样选择它们。

此规则认识的元素有 `acronym`、`applet`、`basefont`、`bgsound`、`big`、`blink`、`center`、`dir`、`font`、`frame`、`frameset`、`isindex`、`keygen`、`marquee`、`menuitem`、`nobr`、`noembed`、`noframes`、`plaintext`、`spacer`、`strike`、`tt` 和 `xmp`。只报告开始标签，因此每个元素只被指出一次；名称只是以其中某个开头的自定义元素（例如 `<font-picker>`）不会被报告。

错误示例：

```html
<center><font color="red">Warning</font></center>
```

正确示例：

```html
<p class="warning">Warning</p>
```

#### H051

`Role is not one ARIA defines for markup.`

任何规范都没有定义的 role 会被直接丢弃，元素保持原有的含义，因此 `role="buton"` 会让 `<div>` 仍然只是一个 `<div>`：对屏幕阅读器毫无意义，而标记看上去却像是被赋予了某种用途。没有任何东西会对此发出警告，这正是值得捕获这种拼写错误的原因。

此规则认识的名称包括 ARIA 为作者定义的角色，以及 DPUB-ARIA（`doc-chapter` 等）和 GRAPHICS-ARIA（`graphics-symbol` 等）所添加的角色。ARIA 的抽象角色（例如 `landmark` 和 `sectionhead`）会被报告：规范指出，它们是为构建其本体而存在的，不得写在标记中。

`role` 可以包含多个名称作为回退列表，每个名称都会被检查。包含模板语法的值无法得知，不会被报告；由框架写出的绑定（例如 `:role` 或 `[attr.role]`）也不会被报告。

错误示例：

```html
<div role="buton">Save</div>
```

正确示例：

```html
<button type="button">Save</button>
```

#### H052

`Meta refresh should not reload or redirect the page on a timer.`

定时刷新会让页面在读者眼前突然变化。阅读速度较慢的人、正在使用屏幕阅读器的人，或者只是被打断了一下的人，会在没有任何警告、也无法阻止的情况下丢失阅读位置，这不符合 WCAG 2.2.1 可调整的时间限制；而重新加载同一页面的刷新还会丢掉用户已经输入的所有内容。

延迟为零是立即重定向而不是定时器，WCAG 允许在无法使用服务器端重定向的情况下这样做，因此不会被报告。无论这两个属性以何种顺序书写，都能被找到。

错误示例：

```html
<meta http-equiv="refresh" content="30">
```

正确示例：

```html
<meta http-equiv="refresh" content="0; url=/next-page">
```

#### H053

`Id is used more than once in the file.`

一个 id 只命名一个元素。第二个带有相同 id 的元素会破坏 `getElementById`、`<label for>`、片段链接和 `aria-labelledby`：浏览器只取第一个，并悄悄忽略其余的，因此标签、链接或脚本会在没有任何警告的情况下落到错误的元素上。

同一个 `{% if %}...{% else %}...{% endif %}` 的互斥分支中的两个 id 永远不会同时渲染，因此不会被报告。`{% for %}` 循环或 `{% block %}` 不是分支：其内部的 id 和外部相同的 id 都会被渲染，后出现的那个会被报告。由模板标签写入的值无法得知，不会被报告，空值也不会被报告。id 按照浏览器的方式精确比较，因此 `save` 和 `Save` 是两个不同的 id。

分支按文件所用的语言来读取，定界符与标签名之间可以有该语言允许的任意空白：`{% elif %}` 和 `{% else %}`，liquid 的 `{% elsif %}` 和 `{% when %}`，go 的 `{{ else }}`，mako 的 `% else:` 行语句，以及 handlebars 的 `{{else}}`、链式的 `{{else if x}}` 和任何 `{{#helper}}` 块（包括自定义 helper）的反向部分。`<template>` 的内容是一个独立的文档片段，`getElementById` 永远无法访问到，因此其中的 id 只与同一个 `<template>` 中的 id 进行比较：两个 template 可以各自包含一行相同 id 的内容，而同一个 template 中出现两个相同 id 时仍会被报告。注释、<code>{&#37; raw %}</code> 或 `{% verbatim %}` 主体，以及 `djlint:off` 区域中的 id 完全不会被读取。

错误示例：

```html
<button type="submit" id="submit">Save</button>
<button type="submit" id="submit">Save and continue</button>
```

正确示例：

```html
<button type="submit" id="submit">Save</button>
<button type="button" id="cancel">Cancel</button>
```

#### H054

`Interactive element should not be nested inside another.`

html 禁止在 `<a>` 和 `<button>` 中放置交互内容。链接中的按钮或按钮中的链接都是无效的标记，各个浏览器会以各自的方式修复它们，屏幕阅读器用户或键盘用户面对的则是一个表现得像两个控件的控件。axe 会将同样的问题报告为 "nested-interactive"。

被监视的容器是带有 `href` 的 `<a>` 和 `<button>`，在其中会被报告的控件是带有 `href` 的链接、`button`、`input`、`select` 和 `textarea`。没有 `href` 的 `<a>` 不是交互元素，无论在哪一侧都不会被报告；隐藏的 input 或 type 由模板标签写入的 input 也不会被报告。`<template>` 的内容不会在其书写位置渲染，因此其中的控件不算嵌套在外面的链接中，不过写在 template 内部的嵌套仍会被报告。

只有在标签写入属性的地方才会读取属性，其他地方都不会：`{% if not href %}` 中的 `href` 是一个变量名，`{# href="{{ url }}" #}` 中的那个被注释掉了，`data-attr=href` 中的那个属于另一个属性；而 `{% if %}` 在其标签之间写入的 `href` 和其他属性没有区别。未关闭的链接或按钮会随其外层元素一起结束，这和浏览器中的行为一样，因此一个笔误不会导致文件其余部分都被报告；而在顶层未关闭的链接或按钮外面没有任何元素可以结束它，因此确实会一直延续到文件末尾，H025 也会在那里报告这个孤立的标签。

错误示例：

```html
<a href="/cart"><button>Add</button></a>
```

正确示例：

```html
<a href="/cart" class="button">Add</a>
```

#### H055

`Lang attribute should be a language tag such as en or pt-BR.`

H005 要求 `<html>` 上有 `lang`，但 `lang="english"` 或 `lang="en_US"` 这样的值虽然能满足它，却没有指明任何浏览器认识的语言。于是屏幕阅读器会回退到默认语音，翻译和断字也会采用错误的规则，或者根本不起作用。该值必须是 BCP 47 标签：两个或三个字母，后面可以跟任意数量的子标签，每个子标签由一到八个字母或数字组成，前面加连字符，例如 `en`、`pt-BR` 或 `zh-Hant-TW`。

与 H005 一致，只检查 `<html>` 标签。空值交给 H005 处理，而只包含空白的值会在这里报告，因为 H005 会把它视为一个值。由模板标签写入的值（例如 `lang="{{ LANGUAGE_CODE }}"`）或由 php 短 echo 标签写入的值（例如 `lang="<?= $lang ?>"`）无法得知，不会被报告；但仅仅以 `$` 或 `{` 开头的值（例如 `lang="$LANG"`）会按照书写形式读取。`xml:lang` 或 `data-lang` 不会被当作 `lang` 读取，写在该属性之前的模板标签中的 `>`（例如 `{% if a > b %}`）也不会把它隐藏起来。

错误示例：

```html
<html lang="english">
```

正确示例：

```html
<html lang="en">
```

#### H056

`Src should not be empty.`

html 规范规定空的 `src` 是无效的，并警告浏览器会根据文档自身的 url 来解析它，因此 `<img src="">` 会把页面再请求一次当作图片，`<script src=""></script>` 会把页面当作脚本请求。它通常是一个本应由脚本填充的占位符，修复方法是在有真正的值之前去掉这个属性，或者把值放在 data 属性中。完全不带值的 `src`（例如 `<img src>`）同样为空，也会被报告。

只检查 `img`、`script`、`iframe`、`embed`、`source`、`track`、`audio` 和 `video`，因为只有这些元素会请求 `src` 所指定的资源。只报告浏览器会读作空值的值，因此不加引号的值（例如 `<img src=/static/logo.png>`）不会被报告，只包含空白的值和由模板标签写入的值也不会；`srcset` 和 `data-src` 是不同的属性，此规则不对它们做判断。

错误示例：

```html
<img src="" alt="Logo">
```

正确示例：

```html
<img src="{% static 'logo.png' %}" alt="Logo">
```

#### H057

`Video should have a captions track.`

有声视频的语音只存在于音频中，因此如果没有字幕，聋人或听障观众就无法从中获得任何信息，而 WCAG 1.2.2 字幕（预录制）要求提供字幕。`<video>` 中包含 `kind` 为 `captions` 或 `subtitles` 的 `<track>` 即可满足此规则，完全没有 `kind` 的 `<track>` 也可以，因为 `subtitles` 是默认值。

`muted` 的视频没有需要配字幕的音频，不会被报告。开始标签或主体中包含模板标签的视频也不会被报告，因为字幕轨道或 `muted` 属性可能由模板写入，而 djLint 看不到。这里的模板标签是指由某种模板语言开启的标签，即 `{{`、`{%`、`{#` 或 `${`，因此 jQuery 处理程序（例如 `onclick="$(this).play()"`）、Alpine 的 `$refs`、css 花括号以及写在后备文本中的价格，都只是它们看上去的普通文本，视频仍会被读取。

只有标记才算标记。`muted` 必须是属性，因此 `<video class=muted>` 是一个名为 muted 的 class，会被报告；被注释掉或写在属性值中的 `<track>` 是文本而不是字幕轨道。值中的 `</video>` 不会结束任何东西，元素以其真正的结束标签关闭的位置为准进行判断，因此未关闭的 `<video>` 交给 `H025` 处理。

错误示例：

```html
<video controls src="talk.mp4"></video>
```

正确示例：

```html
<video controls src="talk.mp4">
  <track kind="captions" src="talk.vtt" srclang="en">
</video>
```

<!-- oxfmt-ignore-end -->

### 添加规则

欢迎提交包含新规则的拉取请求！

一条好的规则包括

- 名称
- 代码
- 消息：发现错误时显示的消息。
- 标志：正则表达式标志。默认为 re.DOTALL。例如：re.I|re.M
- 模式：用于查找错误的正则表达式。
- 排除：可选，不应用此规则的预设列表。

请附上用于验证该规则的测试。

## 自定义规则

你可以在 `pyproject.toml` 旁边创建一个 `.djlint_rules.yaml`，为自己的项目添加自定义规则。在这个文件中添加规则后，djLint 就会读取它们。可以使用 `--rules` 命令行选项指定位于其他位置的规则文件。

### 模式规则

你可以添加在任一正则表达式模式匹配成功时就报错的规则：

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Python 模块规则

你可以添加导入并执行自定义 Python 函数的规则：

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

指定的 `python_module` 必须包含一个 `run()` 函数，该函数会在每个被检查的文件上执行。它必须接受以下参数：

- `rule`：在 `.djlint_rules.yaml` 中表示你的规则的字典。通常用这个变量来获取规则的名称和消息。
- `config`：djLint 的配置对象。
- `html`：文件的完整 html 内容。
- `filepath`：当前正在检查的文件的路径。
- `line_ends`：各行 `start` 和 `end` 字符位置的列表，可以配合 `djlint.lint.get_line()` 使用，根据字符位置得到行号。请参阅示例。
- `*args, **kwargs`：将来我们可能会添加其他参数，因此你应该包含这两个参数，以降低 djLint 升级时出错的风险。

该模块可以位于项目根目录中。如果它返回的 `line` 或 `end` 不是一个位置，djLint 会报错停止，并在错误中指出该规则的名称。

它必须返回一个字典列表，每个错误对应一个字典，包含以下键：

- `code`：报告该错误的规则的代码名称（通常是 `rule['name']`）
- `line`：行号和该行上的字符位置，以 ':' 分隔的字符串。
  例如 `"2:3"` 表示在第 2 行第 3 个字符处发现了错误
- `end`：可选。错误结束的位置，写法与 `line` 相同，指向错误最后一个字符之后的位置。如果没有它，错误在 `match` 结束的位置结束。
- `match`：内容中包含错误的部分
- `message`：用于提示错误而打印出的消息（通常是 `rule['message']`）

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
    """Rule that fails if the html file contains 'bad'.

    This is just an example, in reality it's much simpler to do that with a
    "pattern rule".
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
