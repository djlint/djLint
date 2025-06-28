---
description: 使用 djLint 格式化你的 HTML 模板。又快又准的使你的模板焕发光彩。
title: 代码格式化
keywords: 模板检查, 模板格式化, djLint, HTML, 模板语言, 格式化, 检查, 格式化工具
---

# 代码格式化

djLint 的格式化工具可以处理混乱的HTML模板，使之变得格式统一且易于模仿！

代码格式化是个 beta 工具。在确认修改之前使用 `--check` 查看输出。

预览格式化修改内容：

```bash
djlint . --check
```

直接格式化：

```bash
djlint . --reformat

# 顺带格式化一下脚本和样式？
djlint . --reformat --format-css --format-js
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/docs/configuration/">详情请参考 `配置` 章节</a></div>
</div>

{% admonition
   "note",
   "注意",
   "对于嵌入属性中的长段 JSON/HTML 内容，不会进行格式化。"
%}

{% admonition
   "note",
   "注意",
   "djLint 并非 HTML 解析器或语法验证器。"
%}

## 示例

### 处理前

下面是一段急需处理的 HTML 代码块 -
{% raw %}

```
{% load admin_list %}{% load i18n %}<p class="paginator">{% if pagination_required %}{% for i in page_range %}{% paginator_number cl i %}{% endfor %}{% endif %}{{ cl.result_count }}{% if cl.result_count == 1 %}{{ cl.opts.verbose_name }}   {% else %}{{ cl.opts.verbose_name_plural }}       {% endif %}{% if show_all_url %} <a href="{{ show_all_url }}" class="showall">{% translate 'Show all' %}          </a>  {% endif %}{% if cl.formset and cl.result_count %}<input type="submit" name="_save" class="default" value="{% translate 'Save' %}">{% endif %}      </p>
```

{% endraw %}

### 处理后

看起来好多了…… 至少我们能读得下去了：

{% raw %}

```html
{% load admin_list %} {% load i18n %}
<p class="paginator">
  {% if pagination_required %} {% for i in page_range %} {% paginator_number cl
  i %} {% endfor %} {% endif %} {{ cl.result_count }} {% if cl.result_count == 1
  %} {{ cl.opts.verbose_name }} {% else %} {{ cl.opts.verbose_name_plural }} {%
  endif %} {% if show_all_url %}
  <a href="{{ show_all_url }}" class="showall"> {% translate 'Show all' %} </a>
  {% endif %} {% if cl.formset and cl.result_count %}
  <input
    type="submit"
    name="_save"
    class="default"
    value="{% translate 'Save' %}"
  />
  {% endif %}
</p>
```

{% endraw %}
