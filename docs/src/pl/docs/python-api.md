---
description: Formatuj i lintuj szablony z poziomu własnego kodu w Pythonie za pomocą API djLint.
title: API Pythona
keywords: linter szablonów, formater szablonów, djLint, HTML, szablony, formater, linter, python, api
---

# API Pythona

`djlint.api` formatuje i lintuje tekst z poziomu programu w Pythonie, z takimi samymi wynikami jak wiersz poleceń. Jest przeznaczony dla edytorów, narzędzi do budowania i wszystkiego innego, co przechowuje szablon w pamięci. Cała reszta pakietu może się zmienić w dowolnym wydaniu, więc używaj tego modułu, a nie `djlint.settings` czy `djlint.lint`.

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', filename="templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", /, *, python_rules=True, **options)` wczytuje konfigurację obowiązującą dla plików danego folderu. Szuka jej, idąc w górę od tego folderu, tak jak wiersz poleceń robi to od bieżącego katalogu, i nie zmienia bieżącego katalogu.

Opcje mają nazwy opcji wiersza poleceń, zapisane z podkreśleniami, i działają tak samo jak tam: ustawiona wartość ma pierwszeństwo przed plikiem konfiguracyjnym, a `False`, pusty ciąg znaków oraz, w przypadku większości opcji, `0` są traktowane jak niepodane. Ścieżki podaje się jako `pathlib.Path`.

Wczytanie konfiguracji zajmuje trochę czasu, więc zachowaj wynik, dopóki nie zmienią się pliki, z których ją wczytano. Można go użyć dla dowolnej liczby tekstów.

Przy `python_rules=False` własne reguły z `python_module` nie są wczytywane, dzięki czemu nie uruchomi się kod projektu, któremu nie ufasz. Ich nazwy trafiają do `config.skipped_rules`.

## format_text

`format_text(config, text, /)` zwraca sformatowany tekst. Tekst, którego pierwszy wiersz kończy się znakami CRLF, jest zwracany z CRLF, a każdy inny z LF. Przy `require_pragma` tekst bez pragmy jest zwracany bez zmian.

## lint_text

`lint_text(config, text, /, *, filename="-")` zwraca listę obiektów `Finding` w kolejności, w jakiej występują w dokumencie. Do `filename` dopasowywane jest `per-file-ignores`. Przy `require_pragma` tekst bez pragmy nie ma żadnych zgłoszeń.

`Finding` to krotka nazwana (named tuple) z następującymi polami:

::: content

- `code`: kod reguły, na przykład `H013`.
- `message`: komunikat reguły.
- `match`: początek znalezionego tekstu, maksymalnie 20 znaków.
- `line`, `column`: miejsce, w którym zaczyna się zgłoszenie. Wiersze są liczone od 1, a kolumny od 0.
- `end_line`, `end_column`: pozycja tuż za jego końcem, który może wypadać w jednym z dalszych wierszy.
:::

Kolumny liczą znaki, a nie bajty ani jednostki kodowe UTF-16.

## is_excluded

`is_excluded(config, path, /)` informuje, czy `exclude`, `extend_exclude` lub gitignore wykluczają plik, tak jak robi to wiersz poleceń. `format_text` i `lint_text` same tego nie sprawdzają.

## Moduły reguł

`python_module` własnej reguły jest importowany raz na proces, z katalogu głównego projektu, do którego należy konfiguracja. Program, który działa bez przerwy i obsługuje kilka projektów, musi usunąć z `sys.modules` wszystko, co zaimportowano z projektu, a także katalog główny projektu, który pozostaje na końcu `sys.path`, aby móc wczytać moduły innego projektu.
