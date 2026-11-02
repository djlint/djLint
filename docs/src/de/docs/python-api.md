---
description: Formatieren und linten Sie Templates mit der djLint-API aus Ihrem eigenen Python-Code.
title: Python-API
keywords: Template-Linter, Template-Formatter, djLint, HTML, Templates, Formatter, Linter, python, api
---

# Python-API

`djlint.api` formatiert und lintet Text aus einem Python-Programm heraus, mit denselben Ergebnissen wie auf der Befehlszeile. Das Modul ist für Editoren, Build-Tools und alles andere gedacht, was ein Template im Speicher hält. Alles andere im Paket kann sich mit jedem Release ändern, verwenden Sie also dieses Modul und nicht `djlint.settings` oder `djlint.lint`.

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, **options)` liest die Konfiguration, die für die Dateien eines Ordners gilt. Es sucht sie vom Ordner aus aufwärts, so wie die Befehlszeile vom aktuellen Verzeichnis aus, und wechselt dabei nicht das aktuelle Verzeichnis.

Optionen tragen die Namen der Befehlszeilenoptionen, mit Unterstrichen, und wirken wie dort: Ein gesetzter Wert hat Vorrang vor der Konfigurationsdatei, während `False`, ein leerer String und bei den meisten Optionen auch `0` als nicht angegeben gelten. Pfade werden als `pathlib.Path` übergeben.

Das Lesen der Konfiguration dauert etwas. Behalten Sie das Ergebnis daher, solange sich die Dateien, aus denen es gelesen wurde, nicht ändern. Es lässt sich für beliebig viele Texte verwenden.

Mit `python_rules=False` werden benutzerdefinierte Regeln mit einem `python_module` nicht geladen. So wird der Code eines Projekts, dem Sie nicht vertrauen, nicht ausgeführt. Ihre Namen stehen in `config.skipped_rules`.

## format_text

`format_text(config, text)` gibt den formatierten Text zurück. Ein Text, dessen erste Zeile auf CRLF endet, kommt mit CRLF zurück, jeder andere mit LF. Mit `require_pragma` kommt ein Text ohne das Pragma unverändert zurück.

## lint_text

`lint_text(config, text, filename="-")` gibt eine Liste von `Finding` in der Reihenfolge des Dokuments zurück. `filename` ist der Wert, mit dem `per-file-ignores` abgeglichen wird. Mit `require_pragma` hat ein Text ohne das Pragma keine Befunde.

`Finding` ist ein benanntes Tupel mit diesen Feldern:

::: content

- `code`: Der Code der Regel, etwa `H013`.
- `message`: Was die Regel meldet.
- `match`: Der Anfang des gefundenen Textes, höchstens 20 Zeichen.
- `line`, `column`: Wo der Befund beginnt. Zeilen werden ab 1 gezählt, Spalten ab 0.
- `end_line`, `end_column`: Die Stelle direkt hinter seinem Ende, das auch in einer späteren Zeile liegen kann.
:::

Spalten zählen Zeichen, nicht Bytes oder UTF-16-Codeeinheiten.

## is_excluded

`is_excluded(config, path)` gibt an, ob `exclude`, `extend_exclude` oder die gitignore eine Datei ausschließen, so wie es die Befehlszeile tut. `format_text` und `lint_text` prüfen das nicht selbst.

## Regelmodule

Das `python_module` einer benutzerdefinierten Regel wird einmal pro Prozess importiert, und zwar aus dem Projektstamm der Konfiguration. Ein Programm, das weiterläuft und mit mehreren Projekten arbeitet, muss alles, was aus dem Projekt importiert wurde, aus `sys.modules` entfernen und ebenso den Projektstamm, der am Ende von `sys.path` stehen bleibt, um die Regelmodule eines anderen Projekts zu lesen.
