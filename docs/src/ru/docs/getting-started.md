---
description: Начало работы с djLint для линтинга и форматирования HTML-шаблонов. Воспользуйтесь простым интерфейсом cli и множеством опций форматирования.
title: Начало работы
keywords: облицовка шаблонов, форматер шаблонов, djLint, HTML, шаблоны, форматер, линтер, использование
---

# {{ "getting_started" | i18n }}

## Установка от [Pypi](https://pypi.org/project/djlint/)

djLint собирается с [Python](https://python.org), он может быть установлен простым запуском:

```bash
pip install djlint
```

Или как отдельный инструмент с помощью [uv](https://docs.astral.sh/uv/):

```bash
uv tool install djlint
```

Или с помощью [pipx](https://pipx.pypa.io/):

```bash
pipx install djlint
```

Или с помощью формулы [Homebrew](https://formulae.brew.sh/formula/djlint), поддерживаемой сообществом, на macOS или Linux:

```bash
brew install djlint
```

_Или с помощью npm - **внимание**: npm-пакет - это лишь обёртка, его установочный скрипт запускает `pip install --upgrade djlint` для того `python3`, который находится в вашем системном пути. npm не управляет установленным пакетом и не удалит его - по возможности используйте pip напрямую._

```bash
npm i djlint
```

## Использование CLI

djLint - это приложение командной строки. Для расширенной настройки смотрите `конфигурация`.

{% include 'src/_includes/cli.md' %}

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
