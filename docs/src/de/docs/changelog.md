---
description: Changelog von djLint. Erfahren Sie, was sich in den letzten Releases geändert hat und welche Funktionen Sie beim nächsten Upgrade erwarten.
title: Changelog
keywords: Template-Linter, Template-Formatter, djLint, HTML, Templates, Formatter, Linter, Changelog
---

{% raw %}

# Changelog

Der Changelog ist jetzt im [Release](https://github.com/djlint/djLint/releases) enthalten.

## 1.0.2

::: content

- Fehlerbehebungen [#240](https://github.com/djlint/djLint/issues/240)
  :::

## 1.0.1

::: content

- Fehlerbehebungen [#236](https://github.com/djlint/djLint/issues/236)
  :::

## 1.0.0

::: content

- Fehlerbehebungen [#224](https://github.com/djlint/djLint/issues/224)
  :::

## 0.7.6

::: content

- Fehlerbehebungen [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/189)
- Option `--warn` hinzugefügt, die Fehler als Warnungen zurückgibt.
  :::

## 0.7.5

::: content

- Fehlerbehebungen [#187](https://github.com/djlint/djLint/issues/187)
- Bessere Unterstützung für `yaml`-Front-Matter in Template-Dateien hinzugefügt
- Regel T032 für [#123](https://github.com/djlint/djLint/issues/123) hinzugefügt
- Regel H033 für [#124](https://github.com/djlint/djLint/issues/124) hinzugefügt
- Linter-Profile sind jetzt einschließend statt ausschließend, für [#178](https://github.com/djlint/djLint/issues/178)
- Alternative Konfigurationsdatei `.djlintrc` hinzugefügt, für [#188](https://github.com/djlint/djLint/issues/188)
  :::

## 0.7.4

::: content

- Fehlerbehebungen [#177](https://github.com/djlint/djLint/issues/177)
  :::

## 0.7.3

::: content

- Fehlerbehebungen [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- Py3.6 aus `pyproject.toml` entfernt.
  :::

## 0.7.2

::: content

- Fehlerbehebungen [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
  :::

## 0.7.1

::: content

- Fehlerbehebungen [#166](https://github.com/djlint/djLint/issues/166)
  :::

## 0.7.0

::: content

- Konfiguration für eigene HTML-Tags hinzugefügt
- Fehlerbehebungen
  :::

## 0.6.9

::: content

- Profile für HTML und Angular hinzugefügt
- Einige Entities in Regel #H023 erlaubt
- Fehlerbehebungen
  :::

## 0.6.8

::: content

- Fehlerbehebungen
- Dokumentation aktualisiert
  :::

## 0.6.7

::: content

- Konfigurationsoption `format_attribute_template_tags` hinzugefügt, mit der sich das Formatieren von Template-Tags in Attributen einschalten lässt
- Konfigurationsoption `linter_output_format` hinzugefügt, mit der sich die Reihenfolge der Variablen in Linter-Meldungen anpassen lässt
- Regeln H030 und H031 zur Prüfung von Meta-Tags hinzugefügt
  :::

## 0.6.6

::: content

- Fehlerbehebungen
  :::

## 0.6.5

::: content

- Ausgabepfade sind jetzt relativ zum Projektstamm
- Fehlerbehebungen
  :::

## 0.6.4

::: content

- Fehlerbehebungen
  :::

## 0.6.3

::: content

- Unterstützung für das Django-Tag `blocktrans` hinzugefügt
- Fehlerbehebungen
  :::

## 0.6.2

::: content

- Fehlerbehebungen
  :::

## 0.6.1

::: content

- Fehlerbehebungen
- Regel T028 verschärft, mit klarerer Meldung
  :::

## 0.6.0

::: content

- Regel T027 hinzugefügt, die nicht Geschlossenes in Template-Syntax erkennt
- Regel T028 hinzugefügt, die fehlende Tags mit Whitespace-Kontrolle in Attributen erkennt
- Regel H029 hinzugefügt, die auf eine kleingeschriebene Formularmethode prüft
- Django-Tags blocktranslate ohne „trimmed“ werden vom Formatter ignoriert
- Fehlerbehebungen
  :::

## 0.5.9a

::: content

- Testunterstützung für Python 3.10 hinzugefügt
- pre-commit-Hook hinzugefügt
  :::

## 0.5.9

::: content

- Option `--use-gitignore` zum Erweitern der Ausschlüsse hinzugefügt
- Standardabgleich für Ausschlüsse geändert
- Ausschlusspfade unter Windows korrigiert
- Formatierung von `{%...%}`-Tags in Attributen korrigiert
- Formatierung von for-Schleifen und verschachtelten Bedingungen in Attributen korrigiert
  :::

## 0.5.8

::: content

- Option require_pragma hinzugefügt
- DJ018 erkennt jetzt auch `data-src` und `action` an Inputs
- Syntax zum Ignorieren inline korrigiert
- Option `--lint` als Platzhalter für die Standardverwendung hinzugefügt
- Fehlerbehebungen
  :::

## 0.5.7

::: content

- Fehlerbehebungen
  :::

## 0.5.6

::: content

- Regel H026 hinzugefügt, die leere id- und class-Tags findet
- Fehlerbehebungen
  :::

## 0.5.5

::: content

- Einstellungen zusammengeführt und Code verschlankt
- Fehlerbehebungen
  :::

## 0.5.4

::: content

- Regel H020 hinzugefügt, die leere Tag-Paare findet
- Regel H021 hinzugefügt, die Inline-Styles findet
- Regel H022 hinzugefügt, die http-Links findet
- Regel H023 hinzugefügt, die Entity-Referenzen findet
- Regel H024 hinzugefügt, die type bei Skripten und Styles findet
- Regel H025 hinzugefügt, die verwaiste Tags erkennt. Danke an https://stackoverflow.com/a/1736801/10265880
- Formatierung von Attributen verbessert
- Option `blank_line_after_tag` fügt den Zeilenumbruch jetzt unabhängig von der Position ein
- Formatierung des Django-Tags `trans` korrigiert
- Formatierung von Inline-Styles hinzugefügt
- Formatierung von Template-Bedingungen innerhalb von Attributen hinzugefügt
- srcset als mögliche Fundstelle für URLs in Linter-Regeln hinzugefügt
- Formatieren beschleunigt
- Besonderer Dank an [jayvdb](https://github.com/jayvdb)
  :::

## 0.5.3

::: content

- Die Optionen `--reformat/check` geben auf stdout nur noch das neue HTML aus, wenn stdin als Eingabe dient
  :::

## 0.5.2

::: content

- Anforderung `alt` aus H006 in H013 ausgelagert
- Optionale Datei für benutzerdefinierte Regeln hinzugefügt
- `golang` als Profiloption hinzugefügt
- Formatierung ignorierter Blöcke mit Inline-Kommentaren korrigiert
- Standardtext für die Optionen `--indent` und `-e` hinzugefügt
- URL-Regeln akzeptieren jetzt #
- Dateikodierung unter Windows korrigiert
- Regex für einzeilige Template-Tags korrigiert
- `blank_line_after_tag` für Tags mit führendem Leerzeichen korrigiert
  :::

## 0.5.1

::: content

- Regel H019 hinzugefügt
- Fehler in DJ018 und H012 behoben
  :::

## 0.5.0

::: content

- Mehrere Regex-Fehler in Linter-Regeln behoben
- Der Linter meldet keine Fehler mehr in ignorierten Blöcken
- Option hinzugefügt, mit der sich Codeblöcke über die Tags `{% djlint:off %}...{% djlint:on %}` vor Linter und Formatter verbergen lassen
  :::

## 0.4.9

::: content

- Fehler [#35](https://github.com/djlint/djLint/issues/35) behoben
  :::

## 0.4.8

::: content

- Fehler [#34](https://github.com/djlint/djLint/issues/34) behoben
  :::

## 0.4.7

::: content

- Tag `source` zu den einzeiligen Tags verschoben
  :::

## 0.4.6

::: content

- Fehler [#31](https://github.com/djlint/djLint/issues/31) behoben
  :::

## 0.4.5

::: content

- Best Practices zur Dokumentation hinzugefügt
- Option `--profile` hinzugefügt, mit der sich die Standardregeln für Linter und Formatter festlegen lassen
- Linter-Regeln für URL-Muster in Jinja hinzugefügt
  :::

## 0.4.4

::: content

- Konfiguration der Einrückung von String auf Integer umgestellt. `--indent 3`
  :::

## 0.4.3

::: content

- Befehlszeilenoption für die Einrückung hinzugefügt. `--indent=" "`
  :::

## 0.4.2

::: content

- Unterstützung für zusätzlichen Leerraum nach Tags mit der Option `blank_line_after_tag` hinzugefügt
  :::

## 0.4.1

::: content

- Unterstützung für die Verarbeitung mehrerer Dateien oder Ordner auf einmal hinzugefügt
  :::

## 0.4.0

::: content

- Formatierung von Django-Tags `{# ... #}` korrigiert
- Einrückung für die Tags figcaption, details und summary hinzugefügt
- Unterstützung für das Überschreiben oder Erweitern der Liste ausgeschlossener Pfade in `pyproject.toml` hinzugefügt
  :::

## 0.3.9

::: content

- Behandlung von Attributen aktualisiert
  :::

## 0.3.8

::: content

- Unterstützung für stdin hinzugefügt
  :::

## 0.3.7

::: content

- Formatierung der Tags `small`, `dt` und `dd` korrigiert
  :::

## 0.3.6

::: content

- Unterstützung des Formatters für öffnende Nunjucks-Blöcke mit `{%-` hinzugefügt
  :::

## 0.3.5

::: content

- Unterstützung für weitere Django-Blöcke hinzugefügt
- Unterstützung für eigene Blöcke hinzugefügt
- Unterstützung für Konfiguration in `pyproject.toml` hinzugefügt
  :::

## 0.3.4

::: content

- Formatierung des Nunjucks-Tags mit Whitespace-Kontrolle `-%}` korrigiert
  :::

## 0.3.3

::: content

- Kurze `div`-Tags dürfen einzeilig sein
  :::

## 0.3.2

::: content

- Formatierung von Django-Kommentaren korrigiert
- textarea wird beim Formatieren ignoriert
  :::

## 0.3.1

::: content

- Regex für die Formatierung von Attributen aktualisiert
- Lint-Regel W010 aktualisiert
  :::

## 0.3.0

::: content

- Exit-Code ist jetzt 1, wenn es Formatierungsänderungen gab
- Unterstützung für Jinja-Tags `asset` hinzugefügt
  :::

## 0.2.9

::: content

- Regex von W018 aktualisiert
- Doppelte Lint-Meldungen entfernt
- E001 für Handlebars aktualisiert
  :::

## 0.2.8

::: content

- Fehler der Fortschrittsanzeige bei alten Click-Versionen behoben
  :::

{% endraw %}
