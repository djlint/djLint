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
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block">详情请参考 <a href="/docs/configuration/">配置</a> 章节</div>
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
| H006 | `img` 标签应包含 `height` 和 `width` 属性。                                        | ✔️       |
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
| H017 | 空元素标签应自关闭。                                                               | -        |
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
| H031 | 建议添加 meta 关键字。                                                             | ✔️       |
| H033 | 表单 action 发现多余空格。                                                         | ✔️       |
| J004 | (Jinja) 静态 URL 应遵循 {% raw %}`{{ url_for('static'..) }}`{% endraw %} 形式。    | ✔️       |
| J018 | (Jinja) 内部链接应使用 {% raw %}`{% url ... %}`{% endraw %} 形式。                 | ✔️       |
| T001 | 变量外包含空格。示例：{% raw %}`{{ this }}`{% endraw %}                            | ✔️       |
| T002 | 标签中应使用双引号。示例：{% raw %}`{% extends "this.html" %}`{% endraw %}         | ✔️       |
| T003 | `Endblock` 应包含名称。示例：{% raw %}`{% endblock body %}`{% endraw %}.           | ✔️       |
| T027 | 模板语法中发现未闭合的字符串。.                                                    | ✔️       |
| T028 | 建议在属性值中使用无空格标签，例如：{% raw %}`{%- if/for -%}`{% endraw %}          | ✔️       |
| T032 | 模板标签中发现多余空格。                                                           | ✔️       |
| T034 | 使用 {% raw %}{% ... %} 代替 {% ... }%? {% endraw %}。                             | ✔️       |
| H035 | Meta 标签应自闭合。                                                                | -        |
| H036 | 避免使用 `<br>` 标签。                                                             | -        |
| H037 | 发现重复属性。                                                                     | ✔️       |

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
    config: djlint.settings.Config,
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
        errors.append(
            {
                "code": rule["name"],
                "line": get_line(match.start(), line_ends),
                "match": match.group().strip()[:20],
                "message": rule["message"],
            }
        )
    return errors
```
