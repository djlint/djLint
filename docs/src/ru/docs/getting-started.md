---
description: Начало работы с djLint для линтинга и форматирования HTML-шаблонов. Воспользуйтесь простым интерфейсом cli и множеством опций форматирования.
title: Начало работы
keywords: облицовка шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, использование
---

# {{ "getting_started" | i18n }}

## Установка от [Pypi](https://pypi.org/project/djlint/)

djLint собирается с [Python 3.7+](https://python.org), он может быть установлен простым запуском:

```bash
pip install djlint
```

## Использование CLI

djLint - это приложение командной строки. Для расширенной настройки смотрите `конфигурация`.

```bash
Usage: python -m djlint [OPTIONS] SRC ...

  djLint · lint and reformat HTML templates.

Options:
  --version             Show the version and exit.
  -e, --extension TEXT  File extension to check [default: html]
  -i, --ignore TEXT     Codes to ignore. ex: "H014,H017"
  --reformat            Reformat the file(s).
  --check               Check formatting on the file(s).
  --indent INTEGER      Indent spacing. [default: 4]
  --quiet               Do not print diff when reformatting.
  --profile TEXT        Enable defaults by template language. ops: django,
                        jinja, nunjucks, handlebars, golang, angular,
                        html [default: html]
  --require-pragma      Only format or lint files that starts with a comment
                        with the text 'djlint:on'
  --lint                Lint for common issues. [default option]
  --use-gitignore       Use .gitignore file to extend excludes.
  -h, --help            Show this message and exit.
```

{% admonition
   "note",
   "Note",
   "Если команда `djlint` не найдена, убедитесь, что Python находится [в вашем пути](https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/)."
%}

## Использование Path против Stdin

djLint работает с путем или stdin.

Бег с тропинкой -

```bash
djlint /path/to/templates --lint
```

Или конкретный файл -

```bash
djlint /path/to/this.mustache --lint
```

Или с помощью stdin -

```bash
echo "<div></div>" | djlint -
```

Stdin также может быть использован для переформатирования кода. На выходе будет только отформатированный код без сообщений.

```bash
echo "<div></div>" | djlint - --reformat
```

Выход -

```html
<div></div>
```
