---
description: Lista zmian djLint. Sprawdź, co nowego w ostatnich wydaniach i jakich funkcji możesz się spodziewać po następnej aktualizacji.
title: Lista zmian
keywords: linter szablonów, formater szablonów, djLint, HTML, szablony, formater, linter, lista zmian
---

{% raw %}

# Lista zmian

Lista zmian znajduje się teraz w opisach [wydań](https://github.com/djlint/djLint/releases).

## 1.0.2

::: content

- Poprawki błędów [#240](https://github.com/djlint/djLint/issues/240)
  :::

## 1.0.1

::: content

- Poprawki błędów [#236](https://github.com/djlint/djLint/issues/236)
  :::

## 1.0.0

::: content

- Poprawki błędów [#224](https://github.com/djlint/djLint/issues/224)
  :::

## 0.7.6

::: content

- Poprawki błędów [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/189)
- Dodano flagę `--warn`, która zwraca błędy jako ostrzeżenia.
  :::

## 0.7.5

::: content

- Poprawki błędów [#187](https://github.com/djlint/djLint/issues/187)
- Ulepszono obsługę front matter w `yaml` w plikach szablonów
- Dodano regułę T032 w związku z [#123](https://github.com/djlint/djLint/issues/123)
- Dodano regułę H033 w związku z [#124](https://github.com/djlint/djLint/issues/124)
- Zmieniono profile lintera z wykluczających na włączające w związku z [#178](https://github.com/djlint/djLint/issues/178)
- Dodano alternatywny plik konfiguracyjny `.djlintrc` w związku z [#188](https://github.com/djlint/djLint/issues/188)
  :::

## 0.7.4

::: content

- Poprawki błędów [#177](https://github.com/djlint/djLint/issues/177)
  :::

## 0.7.3

::: content

- Poprawki błędów [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- Usunięto Py3.6 z `pyproject.toml`.
  :::

## 0.7.2

::: content

- Poprawki błędów [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
  :::

## 0.7.1

::: content

- Poprawki błędów [#166](https://github.com/djlint/djLint/issues/166)
  :::

## 0.7.0

::: content

- Dodano konfigurację własnych tagów HTML
- Poprawki błędów
  :::

## 0.6.9

::: content

- Dodano profile HTML i Angular
- Dopuszczono niektóre encje w regule #H023
- Poprawki błędów
  :::

## 0.6.8

::: content

- Poprawki błędów
- Zaktualizowano dokumentację
  :::

## 0.6.7

::: content

- Dodano opcję konfiguracji `format_attribute_template_tags`, która włącza formatowanie tagów szablonu wewnątrz atrybutów
- Dodano opcję konfiguracji `linter_output_format` do dostosowywania kolejności zmiennych w komunikatach lintera
- Dodano reguły H030 i H031 sprawdzające tagi meta
  :::

## 0.6.6

::: content

- Poprawki błędów
  :::

## 0.6.5

::: content

- Ścieżki na wyjściu są teraz względne wobec katalogu głównego projektu
- Poprawki błędów
  :::

## 0.6.4

::: content

- Poprawki błędów
  :::

## 0.6.3

::: content

- Dodano obsługę tagu django `blocktrans`
- Poprawki błędów
  :::

## 0.6.2

::: content

- Poprawki błędów
  :::

## 0.6.1

::: content

- Poprawki błędów
- Zaostrzono regułę T028 i doprecyzowano jej komunikat
  :::

## 0.6.0

::: content

- Dodano regułę T027 sprawdzającą niezamknięte ciągi znaków w składni szablonu
- Dodano regułę T028 sprawdzającą brak tagów usuwających białe znaki w atrybutach
- Dodano regułę H029 sprawdzającą, czy metoda formularza jest zapisana małymi literami
- Formater pomija tagi django blocktranslate bez „trimmed”
- Poprawki błędów
  :::

## 0.5.9a

::: content

- Dodano obsługę pythona 3.10 w testach
- Dodano hook pre-commit
  :::

## 0.5.9

::: content

- Dodano opcję `--use-gitignore`, która rozszerza wykluczenia
- Zmieniono domyślne dopasowywanie wykluczeń
- Poprawiono ścieżki wykluczeń w systemie Windows
- Poprawiono formatowanie tagów `{%...%}` w atrybutach
- Poprawiono formatowanie pętli for i zagnieżdżonych warunków w atrybutach
  :::

## 0.5.8

::: content

- Dodano opcję require_pragma
- DJ018 wychwytuje teraz `data-src` i `action` w polach input
- Poprawiono składnię ignorowania bezpośrednio w kodzie
- Dodano opcję `--lint` jako jawny odpowiednik domyślnego użycia
- Poprawki błędów
  :::

## 0.5.7

::: content

- Poprawki błędów
  :::

## 0.5.6

::: content

- Dodano regułę H026 wyszukującą puste atrybuty id i class
- Poprawki błędów
  :::

## 0.5.5

::: content

- Uporządkowano ustawienia i odchudzono kod
- Poprawki błędów
  :::

## 0.5.4

::: content

- Dodano regułę H020 wyszukującą puste pary tagów
- Dodano regułę H021 wyszukującą style inline
- Dodano regułę H022 wyszukującą linki http
- Dodano regułę H023 wyszukującą odwołania do encji
- Dodano regułę H024 wyszukującą atrybut type w skryptach i stylach
- Dodano regułę H025 sprawdzającą osierocone tagi. Podziękowania dla https://stackoverflow.com/a/1736801/10265880
- Ulepszono formatowanie atrybutów
- Opcja `blank_line_after_tag` dodaje teraz nowy wiersz niezależnie od położenia
- Poprawiono formatowanie tagu django `trans`
- Dodano formatowanie stylów inline
- Dodano formatowanie warunków szablonu wewnątrz atrybutów
- Reguły lintera uwzględniają srcset jako możliwe miejsce adresu url
- Przyspieszono formatowanie
- Specjalne podziękowania dla [jayvdb](https://github.com/jayvdb)
  :::

## 0.5.3

::: content

- Przy użyciu stdin jako wejścia opcje `--reformat/check` wypisują na stdout tylko nowy html
  :::

## 0.5.2

::: content

- Wydzielono wymaganie `alt` z H006 do H013
- Dodano opcjonalny plik z własnymi regułami
- Dodano `golang` jako wartość profilu
- Poprawiono formatowanie ignorowanych bloków zawierających komentarze w wierszu
- Dodano tekst domyślny do opcji `--indent` i `-e`
- Reguły dotyczące adresów url akceptują teraz #
- Poprawiono kodowanie plików w systemie Windows
- Poprawiono wyrażenie regularne dla jednowierszowych tagów szablonu
- Poprawiono `blank_line_after_tag` dla tagów poprzedzonych spacją
  :::

## 0.5.1

::: content

- Dodano regułę H019
- Poprawiono błędy w DJ018 i H012
  :::

## 0.5.0

::: content

- Poprawiono kilka błędów dopasowywania wyrażeń regularnych w regułach lintera
- Linter nie zwraca już błędów w ignorowanych blokach
- Dodano możliwość wyłączenia bloku kodu z lintowania/formatowania za pomocą tagów `{% djlint:off %}...{% djlint:on %}`
  :::

## 0.4.9

::: content

- Poprawiono błąd [#35](https://github.com/djlint/djLint/issues/35)
  :::

## 0.4.8

::: content

- Poprawiono błąd [#34](https://github.com/djlint/djLint/issues/34)
  :::

## 0.4.7

::: content

- Przeniesiono tag `source` do tagów jednowierszowych
  :::

## 0.4.6

::: content

- Poprawiono błąd [#31](https://github.com/djlint/djLint/issues/31)
  :::

## 0.4.5

::: content

- Dodano do dokumentacji dobre praktyki
- Dodano opcję `--profile`, która ustawia domyślne reguły lintera/formatera
- Dodano reguły lintera dla wzorców url w jinja
  :::

## 0.4.4

::: content

- Zmieniono typ konfiguracji wcięcia z ciągu znaków na liczbę całkowitą. `--indent 3`
  :::

## 0.4.3

::: content

- Dodano opcję wiersza poleceń do ustawiania wcięcia. `--indent=" "`
  :::

## 0.4.2

::: content

- Dodano obsługę dodatkowych odstępów po tagach za pomocą opcji `blank_line_after_tag`
  :::

## 0.4.1

::: content

- Dodano obsługę przetwarzania kilku plików lub folderów naraz
  :::

## 0.4.0

::: content

- Poprawiono formatowanie tagów django `{# ... #}`
- Dodano obsługę wcięć dla tagów figcaption, details i summary
- Dodano możliwość nadpisywania lub rozszerzania listy wykluczonych ścieżek w `pyproject.toml`
  :::

## 0.3.9

::: content

- Zaktualizowano obsługę atrybutów
  :::

## 0.3.8

::: content

- Dodano obsługę stdin
  :::

## 0.3.7

::: content

- Poprawiono formatowanie tagów `small`, `dt` i `dd`
  :::

## 0.3.6

::: content

- Dodano w formaterze obsługę bloków Nunjucks otwieranych przez `{%-`
  :::

## 0.3.5

::: content

- Dodano obsługę kolejnych bloków Django
- Dodano obsługę własnych bloków
- Dodano obsługę konfiguracji w `pyproject.toml`
  :::

## 0.3.4

::: content

- Poprawiono formatowanie tagu Nunjucks usuwającego białe znaki `-%}`
  :::

## 0.3.3

::: content

- Krótkie tagi `div` mogą być teraz jednowierszowe
  :::

## 0.3.2

::: content

- Poprawiono formatowanie komentarzy Django
- Formatowanie pomija teraz textarea
  :::

## 0.3.1

::: content

- Zaktualizowano wyrażenie regularne do formatowania atrybutów
- Zaktualizowano regułę lintera W010
  :::

## 0.3.0

::: content

- Kod wyjścia wynosi teraz 1, jeśli formatowanie cokolwiek zmieniło
- Dodano obsługę tagów Jinja `asset`
  :::

## 0.2.9

::: content

- Zaktualizowano wyrażenie regularne W018
- Usunięto zduplikowane komunikaty lintera
- Zaktualizowano E001 dla Handlebars
  :::

## 0.2.8

::: content

- Poprawiono błąd paska postępu w starszych wersjach Click
  :::

{% endraw %}
