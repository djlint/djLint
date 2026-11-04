---
description: Formátujte a lintujte šablony z vlastního kódu v Pythonu pomocí API djLint.
title: Python API
keywords: linter šablon, formátovač šablon, djLint, HTML, šablony, formátovač, linter, python, api
---

# Python API

`djlint.api` formátuje a lintuje text z programu v Pythonu se stejnými výsledky jako příkazový řádek. Je určené pro editory, nástroje pro sestavení a cokoli dalšího, co má šablonu v paměti. Cokoli jiného v balíčku se může změnit v kterékoli verzi, proto používejte tento modul, a ne `djlint.settings` nebo `djlint.lint`.

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', filename="templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", /, *, python_rules=True, **options)` načte konfiguraci, která platí pro soubory dané složky. Hledá ji od složky směrem nahoru, stejně jako ji příkazový řádek hledá od aktuálního adresáře, a aktuální adresář nemění.

Možnosti mají názvy jako možnosti příkazového řádku, jen s podtržítky, a fungují stejně jako tam: nastavená hodnota má přednost před konfiguračním souborem, zatímco `False`, prázdný řetězec a u většiny možností i `0` se berou, jako by zadané nebyly. Cesty se zadávají jako `pathlib.Path`.

Načtení konfigurace chvíli trvá, proto si výsledek ponechte tak dlouho, dokud se nezmění soubory, ze kterých byl načten. Lze ho použít pro libovolný počet textů.

S `python_rules=False` se nenačítají vlastní pravidla s `python_module`, takže se nespustí kód projektu, kterému nedůvěřujete. Jejich názvy jsou v `config.skipped_rules`.

## format_text

`format_text(config, text, /)` vrátí naformátovaný text. Text, jehož první řádek končí znaky CRLF, se vrátí s CRLF, jakýkoli jiný s LF. S `require_pragma` se text bez pragmy vrátí beze změny.

## lint_text

`lint_text(config, text, /, *, filename="-")` vrátí seznam objektů `Finding` v pořadí, v jakém jsou v dokumentu. Proti `filename` se porovnává `per-file-ignores`. S `require_pragma` nemá text bez pragmy žádné nálezy.

`Finding` je pojmenovaná n-tice s těmito poli:

::: content

- `code`: Kód pravidla, například `H013`.
- `message`: Co pravidlo hlásí.
- `match`: Začátek nalezeného textu, nejvýše 20 znaků.
- `line`, `column`: Kde nález začíná. Řádky se počítají od 1 a sloupce od 0.
- `end_line`, `end_column`: Pozice hned za jeho koncem, který může být na pozdějším řádku.
:::

Sloupce počítají znaky, ne bajty ani kódové jednotky UTF-16.

## is_excluded

`is_excluded(config, path, /)` zjistí, zda `exclude`, `extend_exclude` nebo gitignore soubor vynechávají, stejně jako to dělá příkazový řádek. `format_text` a `lint_text` to samy nekontrolují.

## Moduly pravidel

`python_module` vlastního pravidla se importuje jednou za proces, z kořene projektu dané konfigurace. Program, který zůstává spuštěný a pracuje s více projekty, musí před načtením modulů jiného projektu odebrat ze `sys.modules` vše, co z projektu importoval, a také kořen projektu, který zůstává na konci `sys.path`.
