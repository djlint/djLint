---
description: Zainstaluj djLint i lintuj lub formatuj szablony HTML z wiersza poleceń.
title: Pierwsze kroki
keywords: linter szablonów, formater szablonów, djLint, HTML, szablony, formater, linter, użycie
---

# Pierwsze kroki

## Instalacja

djLint jest napisany w [Pythonie](https://python.org) i opublikowany w [PyPI](https://pypi.org/project/djlint/). Za pomocą [uv](https://docs.astral.sh/uv/) dodaj go do projektu jako zależność deweloperską:

```bash
uv add --dev djlint
```

Możesz też zainstalować go jako samodzielne narzędzie:

```bash
uv tool install djlint
```

Albo za pomocą pip:

```bash
pip install djlint
```

Albo za pomocą [pipx](https://pipx.pypa.io/):

```bash
pipx install djlint
```

Albo, w systemie macOS lub Linux, za pomocą rozwijanej przez społeczność [formuły Homebrew](https://formulae.brew.sh/formula/djlint):

```bash
brew install djlint
```

_Albo za pomocą npm. **Uwaga**: pakiet npm jest tylko nakładką. Jego skrypt instalacyjny uruchamia pip dla tego `python3`, który akurat znajduje się w ścieżce systemowej, i instaluje wersję djLint przypisaną do danego wydania pakietu npm, co może zastąpić nowszy djLint starszym. npm nie zarządza właściwym pakietem ani go nie odinstalowuje, więc jeśli możesz, używaj pip._

```bash
npm i djlint
```

Aby uruchamiać djLint przy każdym commicie, zobacz [pre-commit]({{ "lang_code_url" | i18n }}/docs/integrations/#pre-commit).

## Użycie w wierszu poleceń

djLint jest aplikacją wiersza poleceń. Zaawansowaną konfigurację opisuje strona [Konfiguracja]({{ "lang_code_url" | i18n }}/docs/configuration/).

{% include 'src/_includes/cli.md' %}

{% admonition
   "note",
   "Uwaga",
   "Jeśli polecenie `djlint` nie zostanie znalezione, upewnij się, że Python jest [w ścieżce systemowej (PATH)](https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/)."
%}

## Ścieżka a stdin

djLint działa ze ścieżką lub ze standardowym wejściem (stdin).

Uruchomienie ze ścieżką:

```bash
djlint /path/to/templates --lint
```

Albo z konkretnym plikiem:

```bash
djlint /path/to/this.mustache --lint
```

Albo ze stdin:

```bash
echo "<div></div>" | djlint -
```

Stdin można też wykorzystać do przeformatowania kodu. Na wyjściu pojawi się wtedy wyłącznie sformatowany kod, bez komunikatów.

```bash
echo "<div></div>" | djlint - --reformat
```

Wynik:

```html
<div></div>
```

Przy czytaniu ze stdin djLint nie ma prawdziwej ścieżki, którą mógłby dopasować do `per-file-ignores` lub pokazać w komunikatach, więc domyślnie używa `-`. Przekaż `--stdin-filename`, aby podać djLint prawdziwą ścieżkę przekazywanej treści, na przykład gdy integracja z edytorem przesyła przy zapisie zawartość pliku.

```bash
echo "<div></div>" | djlint - --stdin-filename templates/index.html
```

## Kody wyjścia

| Kod | Znaczenie                                                                                                                                                      |
| --- | -------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0` | Wszystko, co djLint miał sprawdzić, jest w porządku albo każdy znaleziony plik został pominięty zgodnie z konfiguracją.                                        |
| `1` | djLint znalazł błędy lintowania lub pliki wymagające przeformatowania. Przy `--warn` są one zgłaszane jako ostrzeżenia, a djLint kończy działanie z kodem `0`. |
| `2` | djLint nie sprawdził tego, o co go poproszono: ścieżki nie pasowały do żadnych plików, wiersz poleceń lub konfiguracja były nieprawidłowe albo djLint zawiódł. |

Tylko kod `1` oznacza, że djLint przejrzał twoje szablony i nie spodobało mu się to, co znalazł. Kod `2` zawsze oznacza, że samo uruchomienie nie spełniło swojego zadania, więc potok CI może traktować te dwa przypadki różnie.

To właśnie kod `2` wychwytuje uruchomienie, które niczego nie sprawdziło: błędną ścieżkę, `--extension`, które już do niczego nie pasuje, albo szablony, które zostały przeniesione. Bez niego takie uruchomienie po cichu kończy się sukcesem.

Pliki, które djLint _znalazł_, a potem celowo pominął z powodu `exclude`, `extend_exclude`, `use_gitignore` lub `require_pragma`, nie są błędem. Takie uruchomienie kończy się kodem `0`, ponieważ konfiguracja zrobiła dokładnie to, co jej kazano. Dzięki temu `exclude` działa też w pre-commit, który przekazuje nazwy plików dodanych do indeksu (staged) niezależnie od tego, czy chcesz, żeby djLint je sprawdzał.

Jeśli w twoim potoku CI ścieżka, w której z założenia nie ma szablonów, jest czymś normalnym, wyłącz kod `2` opcją `allow_empty_input`:

```bash
djlint /path/to/templates --lint --allow-empty-input
```
