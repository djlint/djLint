---
description: djLint 更新日志。查看近期版本的更新内容，以及您在下次升级时可以期待的新功能。
title: 更新日志
keywords: 模板检查, 模板格式化, djLint, HTML, 模板语言, 格式化, 检查, 更新日志
---

{% raw %}

# 更新日志

更新日志请查看 [release](https://github.com/djlint/djLint/releases).

<!--## {{ "next_release" i18n }}-->

## 1.0.2

::: content

- Bug fixes [#240](https://github.com/djlint/djLint/issues/240)
  :::

## 1.0.1

::: content

- 修复了已知问题 [#236](https://github.com/djlint/djLint/issues/236)
  :::

## 1.0.0

::: content

- 修复了已知问题 [#224](https://github.com/djlint/djLint/issues/224)
  :::

## 0.7.6

::: content

- 修复了已知问题 [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/189)
- 添加 `--warn` 参数用于返回报错和警告
  :::

## 0.7.5

::: content

- 修复了已知问题 [#187](https://github.com/djlint/djLint/issues/187)
- 添加了对模板文件中 `yaml` front matter 的更好支持
- 新增 T032 规则，针对 [#123](https://github.com/djlint/djLint/issues/123)
- 新增 H033 规则，针对 [#124](https://github.com/djlint/djLint/issues/124)
- 将代码检查配置文件修改为包含而非排除，针对 [#178](https://github.com/djlint/djLint/issues/178)
- 添加替代的配置文件形式 `.djlintrc`，针对 [#188](https://github.com/djlint/djLint/issues/188)
  :::

## 0.7.4

::: content

- 修复了已知问题 [#177](https://github.com/djlint/djLint/issues/177)
  :::

## 0.7.3

::: content

- 修复了已知问题 [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- 从 `pyproject.toml` 中移除对 Python3.6 的支持
  :::

## 0.7.2

::: content

- 修复了已知问题 [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
  :::

## 0.7.1

::: content

- 修复了已知问题 [#166](https://github.com/djlint/djLint/issues/166)
  :::

## 0.7.0

::: content

- 添加了对于自定义 HTML 标签的配置
- 修复了已知问题
  :::

## 0.6.9

::: content

- 添加 HTML 和 Angular 模板文件
- 允许了 #H023 中的一些实体
- 修复了已知问题
  :::

## 0.6.8

::: content

- 修复了已知问题
- 更新文档
  :::

## 0.6.7

::: content

- 新增了配置选项 `format_attribute_template_tags`，用于选择性地启用属性内部的模板标签格式化功能
- 新增了配置选项 `linter_output_format`，以自定义代码检查器消息中变量的显示顺序
- 新增了规则 H030 和 H031，用于检查 <meta> 标签
  :::

## 0.6.6

::: content

- 修复了已知问题
  :::

## 0.6.5

::: content

- 更新输出路径为相对于项目根路径
- 修复了已知问题
  :::

## 0.6.4

::: content

- 修复了已知问题
  :::

## 0.6.3

::: content

- 添加了对 django `blocktrans` 标签的支持
- 修复了已知问题
  :::

## 0.6.2

::: content

- 修复了已知问题
  :::

## 0.6.1

::: content

- 修复了已知问题
- 使用更清晰的信息使 规则 T028 更严格
  :::

## 0.6.0

::: content

- 新增规则 T027，用于检查模板语法中未闭合的标签
- 新增规则 T028，用于检查属性中缺失的无空格标签
- 新增规则 H029，用于检查表单方法是否为小写形式
- 在格式化过程中，忽略未包含 `trimmed` 的 Django blocktranslate 标签
- 修复了已知错误
  :::

## 0.5.9a

::: content

- 添加对 Python 3.10 的测试支持
- 添加 Pre-commit hook
  :::

## 0.5.9

::: content

- 新增 --use-gitignore 选项以扩展排除文件规则
- 修改了默认排除匹配逻辑
- 修复了 Windows 系统的路径排除问题
- 修复了属性内 {%...%} 模板标签的格式化问题
- 修复了属性内循环和嵌套条件的格式化问题
  :::

## 0.5.8

::: content

- 新增 require_pragma 配置选项
- 更新 DJ018 规则以检测 data-src 和 action 属性
- 修复了行内忽略语法的问题
- 新增 --lint 选项作为默认行为的占位符
- 修复了已知问题
  :::

## 0.5.7

::: content

- 修复了已知问题
  :::

## 0.5.6

::: content

- 新增规则 H026，用于检测空的 id 和 class 属性
- 修复了已知问题
  :::

## 0.5.5

::: content

- 优化配置系统并精简代码
- 修复了已知问题
  :::

## 0.5.4

::: content

- 新增规则 H020，用于匹配空标签对
- 新增规则 H021，用于检测内联样式
- 新增规则 H022，用于检测 HTTP 链接
- 新增规则 H023，用于检测实体引用
- 新增规则 H024，用于检测脚本和样式的类型
- 新增规则 H025，用于检查孤立标签。感谢 https://stackoverflow.com/a/1736801/10265880
- 改进属性格式化功能
- 更新 `blank_line_after_tag` 选项使其在任何位置都添加空行
- 修复 Django `trans` 标签格式化问题
- 新增对内联样式的格式化支持
- 新增对属性内模板条件的格式化支持
- 在代码检查规则中新增 srcset 作为 URL 检测位置
- 提升格式化速度
- 特别鸣谢 [jayvdb](https://github.com/jayvdb)
  :::

## 0.5.3

::: content

- 修改 `--reformat/check` 选项的输出行为：当使用 stdin 输入时只输出新 HTML
  :::

## 0.5.2

::: content

- 将 `alt` 属性检测从 H006 规则拆分到 H013 规则
- 新增自定义规则文件支持
- 新增 `golang` 作为配置预设选项
- 修复了包含行内注释的忽略块的格式化问题
- 为 `--indent` 和 `-e` 选项添加默认文本说明
- 更新 URL 规则以接受 # 符号
- 修复 Windows 系统的文件编码问题
- 修复单行模板标签的正则表达式
- 修复带前导空格的标签的 `blank_line_after_tag` 问题
  :::

## 0.5.1

::: content

- 新增规则 H019
- 修复规则 DJ018 和 H012 的问题
  :::

## 0.5.0

::: content

- 修复多个代码检查规则的正则匹配问题
- 阻止检查器在忽略块中报错
- 新增 `{% djlint:off %}` 和 `{% djlint:on %}` 标签用于临时禁用检查/格式化
  :::

## 0.4.9

::: content

- 修复了已知问题 [#35](https://github.com/djlint/djLint/issues/35)
  :::

## 0.4.8

::: content

- 修复了已知问题 [#34](https://github.com/djlint/djLint/issues/34)
  :::

## 0.4.7

::: content

- 将 `source` 标签归类为单行标签
  :::

## 0.4.6

::: content

- 修复了已知问题 [#31](https://github.com/djlint/djLint/issues/31)
  :::

## 0.4.5

::: content

- 在文档中添加最佳实践指南
- 新增 `--profile` 选项用于设置默认检查/格式化规则
- 新增针对 Jinja URL 模式的检查规则
  :::

## 0.4.4

::: content

- 将缩进配置从字符串改为整型：`--indent 3`
  :::

## 0.4.3

::: content

- 新增缩进空格 CLI 选项：`--indent=" "`
  :::

## 0.4.2

::: content

- 通过 `blank_line_after_tag` 选项支持在标签后添加额外空行
  :::

## 0.4.1

::: content

- 新增支持同时处理多个文件或文件夹
  :::

## 0.4.0

::: content

- 修复 Django `{# ... #}` 注释标签的格式化问题
- 新增对 figcaption/details/summary 标签的缩进支持
- 支持在 `pyproject.toml` 中覆盖或扩展排除路径列表
  :::

## 0.3.9

::: content

- 更新属性处理逻辑
  :::

## 0.3.8

::: content

- 新增标准输入（stdin）支持
  :::

## 0.3.7

::: content

- 修复 `small`、`dt` 和 `dd` 标签的格式化问题
  :::

## 0.3.6

::: content

- 新增对 Nunjucks `{%-` 开始块的格式化支持
  :::

## 0.3.5

::: content

- 新增更多 Django 块标签支持
- 新增自定义块标签支持
- 新增 `pyproject.toml` 配置支持
  :::

## 0.3.4

::: content

- 修复 Nunjucks spaceless 标签 `-%}` 的格式化问题
  :::

## 0.3.3

::: content

- 允许简短的 `div` 标签保持单行格式
  :::

## 0.3.2

::: content

- 修复 Django 注释格式化问题
- 忽略 textarea 标签的格式化
  :::

## 0.3.1

::: content

- 更新属性格式化正则表达式
- 更新规则 W010 检查规则
  :::

## 0.3.0

::: content

- 当存在格式化变更时将退出码改为 1
- 新增对 Jinja `asset` 标签的支持
  :::

## 0.2.9

::: content

- 更新规则 W018 的正则表达式
- 移除重复的检查信息
- 更新 Handlebars 的 E001 规则
  :::

## 0.2.8

::: content

- 修复旧版 Click 的进度条显示问题
  :::

{% endraw %}
