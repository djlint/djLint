---
description: djLint 更新日志。了解近期版本的更新内容，以及下次升级时可以期待哪些功能。
title: 更新日志
keywords: 模板代码检查工具, 模板格式化工具, djLint, HTML, 模板, 格式化工具, 代码检查工具, 更新日志
---

{% raw %}

# 更新日志

更新日志现在包含在[发布版本](https://github.com/djlint/djLint/releases)中。

## 1.0.2

::: content

- 修复问题 [#240](https://github.com/djlint/djLint/issues/240)
:::

## 1.0.1

::: content

- 修复问题 [#236](https://github.com/djlint/djLint/issues/236)
:::

## 1.0.0

::: content

- 修复问题 [#224](https://github.com/djlint/djLint/issues/224)
:::

## 0.7.6

::: content

- 修复问题 [#189](https://github.com/djlint/djLint/issues/189)、[#197](https://github.com/djlint/djLint/issues/189)
- 新增 `--warn` 参数，以警告形式返回错误。
:::

## 0.7.5

::: content

- 修复问题 [#187](https://github.com/djlint/djLint/issues/187)
- 改进了对模板文件中 `yaml` front matter 的支持
- 针对 [#123](https://github.com/djlint/djLint/issues/123) 新增规则 T032
- 针对 [#124](https://github.com/djlint/djLint/issues/124) 新增规则 H033
- 针对 [#178](https://github.com/djlint/djLint/issues/178)，将代码检查预设从排除式改为包含式
- 针对 [#188](https://github.com/djlint/djLint/issues/188) 新增备选配置文件 `.djlintrc`
:::

## 0.7.4

::: content

- 修复问题 [#177](https://github.com/djlint/djLint/issues/177)
:::

## 0.7.3

::: content

- 修复问题 [#173](https://github.com/djlint/djLint/issues/173)、[#174](https://github.com/djlint/djLint/issues/174)
- 从 `pyproject.toml` 中移除了 Py3.6。
:::

## 0.7.2

::: content

- 修复问题 [#167](https://github.com/djlint/djLint/issues/167)、[#166](https://github.com/djlint/djLint/issues/166)、[#171](https://github.com/djlint/djLint/issues/171)、[#169](https://github.com/djlint/djLint/issues/169)
:::

## 0.7.1

::: content

- 修复问题 [#166](https://github.com/djlint/djLint/issues/166)
:::

## 0.7.0

::: content

- 新增自定义 HTML 标签配置
- 问题修复
:::

## 0.6.9

::: content

- 新增 HTML 和 Angular 预设
- 规则 #H023 允许部分实体
- 问题修复
:::

## 0.6.8

::: content

- 问题修复
- 更新了文档
:::

## 0.6.7

::: content

- 新增配置选项 `format_attribute_template_tags`，可选择启用对属性中模板标签的格式化
- 新增配置选项 `linter_output_format`，用于自定义代码检查消息中变量的顺序
- 新增规则 H030 和 H031，用于检查 meta 标签
:::

## 0.6.6

::: content

- 问题修复
:::

## 0.6.5

::: content

- 输出路径改为相对于项目根目录
- 问题修复
:::

## 0.6.4

::: content

- 问题修复
:::

## 0.6.3

::: content

- 新增对 django `blocktrans` 标签的支持
- 问题修复
:::

## 0.6.2

::: content

- 问题修复
:::

## 0.6.1

::: content

- 问题修复
- 规则 T028 更加严格，消息也更加清晰
:::

## 0.6.0

::: content

- 新增规则 T027，用于检查模板语法中未闭合的内容
- 新增规则 T028，用于检查属性中缺少的无空白标签
- 新增规则 H029，用于检查小写的表单 method
- 格式化工具会忽略不带 "trimmed" 的 django blocktranslate 标签
- 问题修复
:::

## 0.5.9a

::: content

- 新增对 python 3.10 的测试支持
- 新增 pre-commit 钩子
:::

## 0.5.9

::: content

- 新增选项 `--use-gitignore`，用于扩展排除列表
- 更改了默认的排除匹配方式
- 修复了 Windows 上的排除路径
- 修复了属性中 `{%...%}` 标签的格式化
- 修复了属性中 for 循环和嵌套条件的格式化
:::

## 0.5.8

::: content

- 新增 require_pragma 选项
- 更新 DJ018，可以捕获 input 上的 `data-src` 和 `action`
- 修复了内联忽略语法
- 新增 `--lint` 选项，作为默认用法的占位符
- 问题修复
:::

## 0.5.7

::: content

- 问题修复
:::

## 0.5.6

::: content

- 新增规则 H026，用于查找空的 id 和 class 标签
- 问题修复
:::

## 0.5.5

::: content

- 整合了设置并精简了代码
- 问题修复
:::

## 0.5.4

::: content

- 新增规则 H020，用于查找空的标签对
- 新增规则 H021，用于查找内联样式
- 新增规则 H022，用于查找 http 链接
- 新增规则 H023，用于查找实体引用
- 新增规则 H024，用于查找 script 和 style 上的 type
- 新增规则 H025，用于检查孤立标签。感谢 https://stackoverflow.com/a/1736801/10265880
- 改进了属性格式化
- 更新 `blank_line_after_tag` 选项，无论位置如何都会添加换行
- 修复了 django `trans` 标签的格式化
- 新增对内联样式的格式化
- 新增对属性中模板条件的格式化
- 在代码检查规则中，将 srcset 作为可能出现 url 的位置
- 提升了格式化速度
- 特别感谢 [jayvdb](https://github.com/jayvdb)
:::

## 0.5.3

::: content

- 更改 `--reformat/check` 选项的 stdout 输出：仅在使用 stdin 作为输入时打印新的 html
:::

## 0.5.2

::: content

- 将 `alt` 要求从 H006 拆分到 H013
- 新增可选的自定义规则文件
- 新增 `golang` 预设选项
- 修复了包含内联注释的忽略块的格式化
- 为 `--indent` 和 `-e` 选项添加了默认文本
- 更新 url 规则，允许使用 #
- 修复了 Windows 操作系统上的文件编码问题
- 修复了单行模板标签的正则表达式
- 修复了带有前导空格的标签的 `blank_line_after_tag`
:::

## 0.5.1

::: content

- 新增规则 H019
- 修复了 DJ018 和 H012 中的错误
:::

## 0.5.0

::: content

- 修复了代码检查规则中的多个正则匹配错误
- 代码检查工具不再在忽略块中返回错误
- 新增选项，可以使用 `{% djlint:off %}...{% djlint:on %}` 标签让代码检查工具/格式化工具忽略代码块
:::

## 0.4.9

::: content

- 修复错误 [#35](https://github.com/djlint/djLint/issues/35)
:::

## 0.4.8

::: content

- 修复错误 [#34](https://github.com/djlint/djLint/issues/34)
:::

## 0.4.7

::: content

- 将 `source` 标签移入单行标签
:::

## 0.4.6

::: content

- 修复错误 [#31](https://github.com/djlint/djLint/issues/31)
:::

## 0.4.5

::: content

- 在文档中加入了最佳实践
- 新增 `--profile` 选项，用于设置默认的代码检查/格式化规则
- 新增针对 jinja url 模式的代码检查规则
:::

## 0.4.4

::: content

- 将缩进配置从字符串改为整数。`--indent 3`
:::

## 0.4.3

::: content

- 新增用于设置缩进空格的命令行选项。`--indent=" "`
:::

## 0.4.2

::: content

- 新增 `blank_line_after_tag` 选项，支持在标签后添加额外的空白
:::

## 0.4.1

::: content

- 支持一次处理多个文件或文件夹
:::

## 0.4.0

::: content

- 修复了 django `{# ... #}` 标签的格式化
- 新增对 figcaption、details 和 summary 标签的缩进支持
- 支持在 `pyproject.toml` 中覆盖或扩展排除路径列表
:::

## 0.3.9

::: content

- 更新了属性处理
:::

## 0.3.8

::: content

- 新增对 stdin 的支持
:::

## 0.3.7

::: content

- 修复了 `small`、`dt` 和 `dd` 标签的格式化
:::

## 0.3.6

::: content

- 格式化工具新增对 Nunjucks `{%-` 开始块的支持
:::

## 0.3.5

::: content

- 新增对更多 Django 块的支持
- 新增对自定义块的支持
- 新增对 `pyproject.toml` 中配置的支持
:::

## 0.3.4

::: content

- 修复了 Nunjucks 无空白标签 `-%}` 的格式
:::

## 0.3.3

::: content

- 允许较短的 `div` 标签保持在单行
:::

## 0.3.2

::: content

- 修复了 Django 注释的格式化
- 格式化时忽略 textarea
:::

## 0.3.1

::: content

- 更新了属性格式化的正则表达式
- 更新了代码检查规则 W010
:::

## 0.3.0

::: content

- 存在任何格式化更改时，退出码改为 1
- 新增对 Jinja `asset` 标签的支持
:::

## 0.2.9

::: content

- 更新了 W018 的正则表达式
- 移除了重复的代码检查消息
- 针对 Handlebars 更新了 E001
:::

## 0.2.8

::: content

- 修复了旧版 Click 中的进度条错误
:::

{% endraw %}
