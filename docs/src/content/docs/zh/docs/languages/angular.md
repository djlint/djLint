---
title: "Angular 模板代码检查工具"
description: "djLint 可以检查 Angular 模板。设置 angular 预设，让规则适合这类模板。"
sidebar:
  label: "Angular"
---

djLint 可以检查 Angular 模板。设置 `angular` 预设，让规则适合这类模板。

**[什么是 Angular？](https://angular.dev/guide/templates)**

## 使用命令行

```bash
djlint /path/to/templates --profile=angular
```

## 在配置文件中

在项目的 `pyproject.toml`、`djlint.toml` / `.djlint.toml` 或 `.djlintrc` 文件中配置 djLint。

```toml title="pyproject.toml"
[tool.djlint]
profile = "angular"
```

```toml title="djlint.toml / .djlint.toml"
profile = "angular"
```

```json title=".djlintrc"
{ "profile": "angular" }
```
