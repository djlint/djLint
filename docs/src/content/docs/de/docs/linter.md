---
title: "Linter-Regeln"
description: "Die Regeln des HTML-Template-Linters von djLint und wie Sie eigene hinzufügen."
sidebar:
  label: "Linter"
---

djLint enthält viele Regeln, die Stil und Gültigkeit Ihrer Templates prüfen. Schöpfen Sie den Linter voll aus, indem Sie ihn ein vordefiniertes Profil für die Template-Sprache Ihrer Wahl verwenden lassen.

```bash
djlint /path/to/templates --lint

# mit eigenen Dateiendungen
djlint /path/to/templates -e html.dj --profile=django

# oder für eine Datei
djlint /path/to/this.html.j2  --profile=jinja
```

:::tip
[Alle Optionen finden Sie in der Anleitung zur Konfiguration!](/de/docs/configuration/)
:::

## Regeln aktivieren oder deaktivieren

Die meisten Regeln sind standardmäßig aktiviert. Auf der Befehlszeile lassen sich Regeln mit der Option `--ignore` deaktivieren und mit der Option `--include` aktivieren.

Zum Beispiel:

```bash
djlint . --lint --include=H006,H017 --ignore=H013,H015
```

Das geht auch in der Konfigurationsdatei (siehe [Konfiguration](/de/docs/configuration)).

## Regeln

| Code | Bedeutung                                                                                                    | Standard |
| ---- | ------------------------------------------------------------------------------------------------------------ | -------- |
| T001 | Variablen sollten von Leerraum umschlossen sein. Bsp.: `{{ this }}`                                          | ✔️       |
| T002 | In Tags sollten doppelte Anführungszeichen verwendet werden. Bsp. `{% extends "this.html" %}`                | ✔️       |
| T003 | Ein Endblock sollte einen Namen haben. Bsp.: `{% endblock body %}`.                                          | -        |
| D004 | (Django) Statische URLs sollten dem Muster `{% static path/to/file %}` folgen.                               | ✔️       |
| J004 | (Jinja) Statische URLs sollten dem Muster `{{ url_for('static'..) }}` folgen.                                | ✔️       |
| H005 | Das html-Tag sollte ein nicht leeres `lang`-Attribut haben.                                                  | ✔️       |
| H006 | Das `img`-Tag sollte die Attribute `height` und `width` haben.                                               | -        |
| H007 | `<!DOCTYPE ... >` sollte vor dem html-Tag stehen.                                                            | ✔️       |
| H008 | Attribute sollten in doppelten Anführungszeichen stehen.                                                     | ✔️       |
| H009 | Tag-Namen sollten kleingeschrieben sein.                                                                     | ✔️       |
| H010 | Attributnamen sollten kleingeschrieben sein.                                                                 | ✔️       |
| H011 | Attributwerte sollten in Anführungszeichen stehen.                                                           | ✔️       |
| H012 | Um das `=` eines Attributs sollten keine Leerzeichen stehen.                                                 | ✔️       |
| H013 | Das `img`-Tag sollte alt-Attribute haben.                                                                    | ✔️       |
| H014 | Mehr Leerzeilen, als die Konfiguration beibehält.                                                            | ✔️       |
| H015 | Auf `h`-Tags sollte ein Zeilenumbruch folgen.                                                                | ✔️       |
| H016 | Fehlendes `title`-Tag in HTML.                                                                               | ✔️       |
| H017 | Void-Tags sollten selbstschließend sein (Konflikt mit: H018).                                                | -        |
| D018 | (Django) Interne Links sollten das Muster `{% url ... %}` verwenden.                                         | ✔️       |
| H018 | Void-Tags sind von Natur aus selbstschließend und müssen mit „>“ enden, nicht mit „/>“ (Konflikt mit: H017). | -        |
| J018 | (Jinja) Interne Links sollten das Muster `{{ url_for() ... }}` verwenden.                                    | ✔️       |
| H019 | Ersetzen Sie `javascript:abc()` durch ein `on_`-Ereignis und eine echte URL.                                 | ✔️       |
| H020 | Leeres Tag-Paar gefunden. Erwägen Sie, es zu entfernen.                                                      | ✔️       |
| H021 | Inline-Styles sollten vermieden werden.                                                                      | ✔️       |
| H022 | Verwenden Sie HTTPS für externe Links.                                                                       | ✔️       |
| H023 | Verwenden Sie keine Entity-Referenzen.                                                                       | ✔️       |
| H024 | Lassen Sie type bei Skripten und Styles weg.                                                                 | ✔️       |
| H025 | Das Tag scheint verwaist zu sein.                                                                            | ✔️       |
| H026 | Leere id- und class-Tags können entfernt werden.                                                             | ✔️       |
| T027 | Nicht geschlossener String in Template-Syntax gefunden.                                                      | ✔️       |
| T028 | Erwägen Sie Tags mit Whitespace-Kontrolle in Attributwerten. `{%- if/for -%}`                                | -        |
| H029 | Erwägen Sie kleingeschriebene Werte für die Formularmethode.                                                 | ✔️       |
| H030 | Erwägen Sie, eine Meta-Description hinzuzufügen.                                                             | ✔️       |
| T032 | Überflüssiger Leerraum in Template-Tags gefunden.                                                            | ✔️       |
| H033 | Überflüssiger Leerraum in der Formular-Action gefunden.                                                      | ✔️       |
| T034 | Wollten Sie {% ... %} statt {% ... }% verwenden?                                                             | ✔️       |
| H036 | Verwenden Sie keine `br`-Tags für Abstände.                                                                  | ✔️       |
| H037 | Doppeltes Attribut gefunden.                                                                                 | ✔️       |
| T038 | Das Block-Tag hat kein passendes End-Tag.                                                                    | ✔️       |
| T039 | Nicht geschlossenes Template-Tag gefunden.                                                                   | ✔️       |
| T040 | Fehlender oder leerer Template-Name im extends- oder include-Tag.                                            | ✔️       |
| H041 | Das Tag wird in einem anderen Template-Block geschlossen, als es geöffnet wurde.                             | ✔️       |
| T041 | Das extends-Tag sollte das erste Tag im Template sein.                                                       | ✔️       |
| H042 | Zum for-Attribut des Labels gibt es in dieser Datei keine passende Element-id.                               | ✔️       |
| T042 | Inhalt außerhalb eines Blocks wird in einem Template, das ein anderes erweitert, nicht gerendert.            | ✔️       |
| H043 | Das button-Tag sollte ein `type`-Attribut haben.                                                             | ✔️       |
| T043 | Ein Blockname wird im Template mehr als einmal verwendet.                                                    | ✔️       |
| H044 | Ein thead sollte `th`- und `td`-Zellen nicht mischen.                                                        | ✔️       |
| T044 | Das Ausgabe-Tag enthält das Schlüsselwort einer Anweisung; verwenden Sie ein Block-Tag.                      | ✔️       |
| H045 | Das iframe-Tag sollte ein `title`-Attribut haben.                                                            | ✔️       |
| T045 | Ein Template-Tag in einem HTML-Kommentar läuft trotzdem; deaktivieren Sie es mit einem Template-Kommentar.   | ✔️       |
| H046 | Tabindex sollte nicht positiv sein.                                                                          | ✔️       |
| H047 | Aria-hidden sollte nicht auf einem fokussierbaren Element gesetzt sein.                                      | ✔️       |
| H048 | Das aria-Attribut ist keines, das die Spezifikation definiert.                                               | ✔️       |
| H049 | Der Viewport sollte das Zoomen der Seite nicht verhindern.                                                   | ✔️       |
| H050 | Das Element ist veraltet und sollte ersetzt werden.                                                          | ✔️       |
| H051 | Die Rolle ist keine, die ARIA für Markup definiert.                                                          | ✔️       |
| H052 | Ein Meta-Refresh sollte die Seite nicht zeitgesteuert neu laden oder weiterleiten.                           | ✔️       |
| H053 | Eine id wird in der Datei mehr als einmal verwendet.                                                         | ✔️       |
| H054 | Ein interaktives Element sollte nicht in einem anderen verschachtelt sein.                                   | ✔️       |
| H055 | Das lang-Attribut sollte ein Sprach-Tag wie en oder pt-BR sein.                                              | ✔️       |
| H056 | Src sollte nicht leer sein.                                                                                  | ✔️       |
| H057 | Ein Video sollte eine Untertitelspur haben.                                                                  | ✔️       |

### Code-Muster

Der erste Buchstabe eines Codes folgt diesem Muster:

- D: gilt speziell für Django
- H: gilt für HTML
- J: gilt speziell für Jinja
- M: gilt speziell für Handlebars
- N: gilt speziell für Nunjucks
- T: gilt allgemein für Templates

### Regeln im Detail

<!-- oxfmt-ignore-start -->

#### T001

`Variables should be wrapped in a whitespace.`

Template-Syntax wie `{{user.name}}` ohne inneren Abstand ist schwerer zu überfliegen und zu vergleichen, und uneinheitliche Abstände in einer Codebasis machen Refactorings per grep (die Suche nach einer Variablen oder einem Tag) unzuverlässig, weil derselbe Ausdruck in mehreren Schreibweisen vorkommt. Die Styleguides von Django und Jinja schreiben beide `{{ var }}` und `{% tag %}` mit einfachen Leerzeichen.

Gilt nicht für die Profile handlebars und golang.

Nicht so:

```html
{{user.name}}
```

Sondern so:

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

Wer in Template-Tags (`{% extends %}`, `{% include %}`, `{% with %}`, `{% trans %}`, `{% now %}`) einfache und doppelte Anführungszeichen mischt, schreibt denselben Template-Namen auf zwei Arten, sodass Suchen und Massenumbenennungen die Hälfte der Vorkommen übersehen. Wer sich auf doppelte Anführungszeichen festlegt, hält die Tag-Argumente im Einklang mit den Anführungszeichen der HTML-Attribute im Rest der Datei.

Einfache Anführungszeichen in HTML-Attributwerten (z. B. `<span title="{% trans 'x' %}">`) werden nicht gemeldet, da die doppelten Anführungszeichen des Attributs dort einfache erzwingen.

Mit `quote_style = "single"` verlangt die Regel stattdessen einfache Anführungszeichen, und der Formatter schreibt diese.

`--reformat` schreibt diese Anführungszeichen für Sie um.

Nicht so:

```html
{% extends 'base.html' %}
```

Sondern so:

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

Erstreckt sich ein `{% block %}` über viele Zeilen oder sind Blöcke verschachtelt, verrät ein bloßes `{% endblock %}` nicht, welchen Block es schließt. Beim Bearbeiten beendet man so leicht den falschen, und Kind-Templates überschreiben dann den falschen Inhalt. Ein benannter Endblock dokumentiert die Zuordnung und lässt sowohl djLint als auch Django (das bei einem nicht passenden Endblock-Namen einen TemplateSyntaxError auslöst) einen an der falschen Stelle geschlossenen Block erkennen. Zuordnungsfehler (nicht geschlossene Blöcke, verwaiste Endblocks und nicht passende Namen) sind Korrektheitsprüfungen, die T038 übernimmt.

Standardmäßig deaktiviert; aktivieren Sie die Regel mit `--include=T003`. `--name-endblocks` schreibt den Namen für Sie.

Ein Name ist nicht erforderlich, wenn der Block in derselben Zeile geöffnet und geschlossen wird, z. B. `{% block title %}``{% endblock %}`. Der Formatter verschiebt den Inhalt eines Blocks, der andere Tags enthält, in eigene Zeilen, sodass ein in einer Zeile geschriebener Block nach dem Formatieren einen Namen benötigen kann; mit `--name-endblocks` schreibt der Formatter auch diesen Namen.

Nicht so:

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

Sondern so:

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Static urls should follow {% static path/to/file %} pattern.`

Fest codierte /static/-Pfade umgehen Djangos `{% static %}`-Tag. Templates gehen dann kaputt, wenn sich STATIC_URL ändert (z. B. beim Umzug der Assets auf ein CDN oder bei einem Deployment unter einem Unterpfad), und erhalten nie die gehashten Dateinamen von ManifestStaticFilesStorage, was in der Produktion zu 404-Fehlern oder veralteten Assets aus dem Cache führt. Die Regel sucht nach dem wörtlichen Präfix `/static/`; ein Projekt, das seine statischen Dateien unter einem anderen Pfad ausliefert, wird also nicht erfasst.

Nicht so:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Sondern so:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

Fest codierte /static/-Pfade umgehen url_for('static', ...) von Flask/Jinja. Assets liefern dann 404, wenn die App unter einem URL-Präfix eingehängt wird oder sich der static-Ordner oder -Host ändert, und die vom Framework angehängten Query-Strings zum Cache-Busting gehen verloren. Die Regel sucht nach dem wörtlichen Präfix `/static/`; ein Projekt, das seine statischen Dateien unter einem anderen Pfad ausliefert, wird also nicht erfasst.

Nicht so:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Sondern so:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have a non-empty lang attribute.`

Ohne lang-Attribut auf `<html>` raten Screenreader die Ausspracheregeln und lesen die Seite womöglich in der falschen Sprache vor, und Browser können Übersetzung, Silbentrennung oder sprachabhängige Anführungszeichen nicht korrekt anbieten. Die Angabe der Seitensprache ist WCAG-2.1-Erfolgskriterium 3.1.1 (Stufe A).

`lang=""` und ein `lang` ohne Wert besagen beide, dass die Sprache unbekannt ist, und werden daher genauso gemeldet wie ein fehlendes Attribut.

Nicht so:

```html
<!DOCTYPE html>
<html>
</html>
```

Sondern so:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`Img tag should have height and width attributes.`

Standardmäßig deaktiviert; aktivieren Sie die Regel mit `--include=H006`.

Hat ein `<img>` weder Breite noch Höhe, kann der Browser keinen Platz reservieren, bevor das Bild heruntergeladen ist, sodass der umgebende Inhalt springt, während die Bilder laden. Diese Layoutverschiebung verschlechtert den Cumulative Layout Shift (eine Core-Web-Vitals-Metrik) und kann Nutzer danebenklicken lassen, während sich die Seite noch aufbaut.

Nicht so:

```html
<img src="cat.png" alt="Cat">
```

Sondern so:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

Ohne `<!DOCTYPE>` vor dem `<html>`-Tag rendern Browser die Seite im Quirks-Modus, der veraltetes Verhalten von Box-Modell und Layout nachahmt, sodass CSS in verschiedenen Browsern uneinheitlich dargestellt wird. Template-Tags und Kommentare vor dem Doctype sind kein Problem; nur dem `<html>`-Tag selbst muss er vorangehen.

Nicht so:

```html
<html lang="en">
</html>
```

Sondern so:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Attributes should be double quoted.`

Gemischte Anführungszeichen machen Attributwerte schwerer zu überfliegen und mit grep zu finden, und Werte in einfachen Anführungszeichen brechen, sobald der Inhalt einen Apostroph enthält. Doppelte Anführungszeichen sind die Konvention der HTML-Spezifikationen, der Formatter und der meisten Styleguides; wer sich auf sie festlegt, bleibt im Einklang mit dem übrigen Ökosystem.

Nicht so:

```html
<div class='content'></div>
```

Sondern so:

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

HTML-Parser akzeptieren großgeschriebene Tag-Namen, doch XHTML- und XML-Serialisierungen unterscheiden Groß- und Kleinschreibung und lehnen sie ab, und gemischte Schreibweisen machen Textsuche und Diff-Reviews unzuverlässig (eine Suche nach `<h1>` übersieht `<H1>`). Kleingeschriebene Tag-Namen halten Templates portabel und einheitlich.

Wird unter `--ignore-case` nicht gemeldet, da diese Option den Formatter anweist, die Groß-/Kleinschreibung unverändert zu lassen.

Nicht so:

```html
<H1>Welcome</H1>
```

Sondern so:

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

Großgeschriebene Attributnamen sind in XHTML-/XML-Serialisierungen ungültig und vereiteln die Textsuche über Templates hinweg (eine Suche nach src= übersieht SRC=). Das DOM normalisiert HTML-Attributnamen ohnehin zu Kleinbuchstaben, großgeschriebene Varianten bringen also nur Uneinheitlichkeit ohne jeden Nutzen. Gemeldet werden nur die Namen, die der Formatter kleinschreibt: `class`, `id`, `src`, `width`, `height`, `alt`, `style`, `lang`, `title`, `media` und `srcset`. `--reformat` korrigiert sie für Sie, und ein Framework-Binding wie `:itemID` oder ein längerer Name wie `data-ID` behält seine Schreibweise.

Wird unter `--ignore-case` nicht gemeldet, da diese Option den Formatter anweist, die Groß-/Kleinschreibung unverändert zu lassen.

Nicht so:

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

Sondern so:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

Attributwerte ohne Anführungszeichen enden am ersten Leerraum, sodass bei einem Wert wie class=btn primary alles nach dem Leerzeichen stillschweigend wegfällt (der Browser behandelt „primary“ als eigenes boolesches Attribut). Besonders anfällig sind Werte aus Template-Variablen: Jedes gerenderte Leerzeichen, „=“ oder „>“ zerstört das Tag. Anführungszeichen machen die Grenze des Werts eindeutig und sicher.

Nicht so:

```html
<div class=test></div>
```

Sondern so:

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

Mit Leerzeichen um das „=“ liest sich das Tag als drei getrennte Token und fällt bei der nächsten Bearbeitung leicht auseinander: Ein Zeilenumbruch oder eine Kürzung in der Mitte hinterlässt ein bloßes boolesches Attribut plus verirrten Text. Einfache Textwerkzeuge (grep, Suchen und Ersetzen) gehen außerdem von einem zusammenhängenden name="value" aus, sodass gemischte Abstände es erschweren, Attribute zuverlässig zu finden und zu refaktorieren. `--reformat` entfernt die Leerzeichen für Sie.

Nicht so:

```html
<div class = "test"></div>
```

Sondern so:

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

Ohne alt-Attribut lesen Screenreader den Dateinamen des Bildes oder gar nichts vor, womit WCAG 1.1.1 (Nicht-Text-Inhalt) verletzt ist. Den Alternativtext sehen Nutzer auch, wenn das Bild nicht geladen werden kann. Dekorative Bilder sollten ein explizit leeres alt="" tragen, damit assistive Technologien sie überspringen; auch das erfüllt diese Regel.

Ein `alt` ohne Wert entspricht `alt=""`, also dem Fall des dekorativen Bildes, und wird daher akzeptiert.

Nicht so:

```html
<img src="cat.jpg" height="200" width="300">
```

Sondern so:

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

Folgen von Leerzeilen wirken sich nicht auf die gerenderte Seite aus (HTML fasst Leerraum zusammen), blähen aber Templates auf und erzeugen unruhige Diffs, wenn sich benachbarte Zeilen ändern. Der Formatter von djLint entfernt sie standardmäßig vollständig (er behält höchstens `max_blank_lines` Leerzeilen, standardmäßig 0); übrig gebliebene Folgen deuten also auf unformatierten Code hin.

Nicht so:

```html
<div>one</div>


<p>two</p>
```

Sondern so:

```html
<div>one</div>

<p>two</p>
```

#### H015

`Follow h tags with a line break.`

Überschriften sind Orientierungspunkte auf Blockebene, die die Gliederung des Dokuments festlegen. Wer das nächste Element in dieselbe Zeile wie das schließende h-Tag zwängt, verbirgt diese Struktur im Quelltext, und Änderungen an einem der beiden Elemente erscheinen im Diff als Änderungen an beiden. Ein Zeilenumbruch nach jeder Überschrift hält die sichtbare Struktur des Templates im Einklang mit der gerenderten Gliederung.

Nicht so:

```html
<h1>Heading</h1><p>Intro text.</p>
```

Sondern so:

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Missing title tag in html.`

Die HTML-Spezifikation verlangt in jedem Dokument ein title-Element. Fehlt es, zeigen Browser-Tabs, Lesezeichen und Verlauf statt eines Seitennamens die rohe URL, Suchmaschinen verlieren die wichtigste Bezeichnung der Seite, und Screenreader-Nutzer verlieren das Erste, was beim Laden angesagt wird, womit WCAG 2.4.2 (Seite mit Titel, Stufe A) verletzt ist.

Schlägt nur bei Dateien an, die ein vollständiges `<html>`...`</html>`-Dokument enthalten; Partials und Kind-Templates, die eine Basis erweitern, werden also nie gemeldet. SPA-Shells, die den Titel clientseitig setzen, brauchen trotzdem ein statisches `<title>`: Es erscheint beim ersten Rendern, bei Crawlern und wenn JavaScript fehlschlägt.

Nicht so:

```html
<html lang="en">
<body>Content</body>
</html>
```

Sondern so:

```html
<html lang="en">
<head>
<title>My page</title>
</head>
<body>Content</body>
</html>
```

#### H017

`Void tags should be self closing.`

Templates, die auch als XML/XHTML geparst werden müssen (oder XML-basierte Werkzeuge speisen), vertragen keine Void-Elemente ohne schließenden Schrägstrich, und eine Mischung aus `<br>` und `<br />` in einer Codebasis erzeugt uneinheitliche Diffs. Diese Regel setzt die Konvention im Stil von XHTML durch, sodass jedes Void-Element auf dieselbe Weise geschlossen wird.

Standardmäßig deaktiviert; aktivieren Sie die Regel mit `--include=H017`. Schließt sich mit H018 gegenseitig aus; aktivieren Sie nur eine der beiden Konventionen. `--close-void-tags` ergänzt den Schrägstrich bei HTML-Void-Tags für Sie. Ein SVG-`<path>` bleibt so, wie es geschrieben ist; schließen Sie es also von Hand.

Nicht so:

```html
<br>
<meta charset="utf-8">
```

Sondern so:

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Internal links should use the {% url ... %} pattern.`

Fest codierte interne URLs veralten stillschweigend, wenn sich der Pfad einer Route in urls.py ändert. Das Ergebnis sind kaputte Links und tote Formular-Actions, die kein Test der URLconf bemerkt. `{% url %}` ermittelt den Pfad aus dem Routennamen, sodass das Umbenennen eines Pfads alle Links auf einmal aktualisiert.

Nicht so:

```html
<a href="/accounts/login">Login</a>
```

Sondern so:

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

Im HTML Living Standard hat der abschließende Schrägstrich an einem Void-Element keine Bedeutung (der Parser ignoriert ihn). `<br />` suggeriert also ein selbstschließendes Verhalten im Stil von XML, das HTML nicht kennt, und kann Leser dazu verleiten, auch Nicht-Void-Tags mit Schrägstrichen zu versehen, wo ein verirrter / stillschweigend verworfen wird und Fehler durch nicht geschlossene Tags verschleiert. Diese Regel setzt bei Void-Elementen das schlichte Ende mit > durch.

Standardmäßig deaktiviert; aktivieren Sie die Regel mit `--include=H018`. Schließt sich mit H017 gegenseitig aus; aktivieren Sie nur eine der beiden Konventionen. SVG-`<path />` ist ausgenommen, da SVG XML ist und den Schrägstrich verlangt. Wird unter `--close-void-tags` nicht gemeldet, da der Formatter dann genau den Schrägstrich schreibt, den diese Regel meldet.

Nicht so:

```html
<br />
<meta charset="utf-8" />
```

Sondern so:

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

Fest codierte interne URLs gehen stillschweigend kaputt, wenn sich der Pfad einer Route ändert oder die App unter einem Präfix eingehängt wird. Zurück bleiben tote Links und Formular-Actions, die an 404-Seiten senden. url_for() baut die URL aus dem Namen des Endpunkts, sodass Änderungen an Routen automatisch in jedes Template übernommen werden.

Nicht so:

```html
<a href="/accounts/login">Login</a>
```

Sondern so:

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

javascript:-URLs machen Mittelklick und „In neuem Tab öffnen“ unbrauchbar, tun nichts, wenn JavaScript deaktiviert ist oder nicht lädt, werden von strengen Content Security Policies blockiert und sind ein klassisches Einfallstor für XSS. Verwenden Sie stattdessen eine echte URL für das href und hängen Sie das Verhalten über einen Event-Handler an. Unter einer strengen CSP werden auch Inline-Handler wie on* blockiert: Das gezeigte onclick ist die minimale Korrektur im Template; besser ist es, den Listener mit addEventListener aus einer Skriptdatei anzuhängen.

Nicht so:

```html
<a href="javascript:openPopup()">Open popup</a>
```

Sondern so:

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

Ein leeres Tag-Paar rendert keinen Inhalt, erzeugt aber trotzdem einen DOM-Knoten, der aus Stylesheets Außenabstände, Rahmen oder Flex-/Grid-Lücken übernehmen kann. Das ergibt Phantomabstände, die schwer aufzuspüren sind; meist handelt es sich um Markup-Reste einer früheren Bearbeitung. Tags, die in normalem Markup legitim leer sind (td, th, li, dt, dd, slot), sind ausgenommen. Tags mit irgendeinem Attribut (JS-Einhängepunkte wie `<div id="app">``</div>`, Icon-Font-Elemente wie `<i class="fa fa-user">``</i>`) werden ebenfalls nicht gemeldet; nur völlig attributlose leere Paare sind betroffen.

Nicht so:

```html
<p>Saved.</p>
<span> </span>
```

Sondern so:

```html
<p>Saved.</p>
```

#### H021

`Inline styles should be avoided.`

Inline-Styles haben eine höhere Spezifität als jeder Selektor eines Stylesheets, sodass man sie später nur mit !important überschreiben kann; sie werden von Content Security Policies ohne 'unsafe-inline' in style-src blockiert; und sie verteilen die Darstellung über die Templates, sodass eine Änderung am Theme oder Design Änderungen am Markup statt an einem einzigen Stylesheet bedeutet. Verschieben Sie die Deklaration in eine CSS-Klasse. Eine legitime Ausnahme sind HTML-E-Mail-Templates: Viele E-Mail-Clients entfernen `<style>`-Blöcke, und Inline-Styles sind dort die übliche Technik. Schließen Sie Ihre Verzeichnisse mit E-Mail-Templates aus oder deaktivieren Sie die Regel für sie.

Nicht so:

```html
<div style="color: red;">Wrong username or password.</div>
```

Sondern so:

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

Einfache http://-Unterressourcen auf einer über HTTPS ausgelieferten Seite sind Mixed Content: Browser blockieren Skripte, Stylesheets und iframes rundweg und werten Bilder automatisch auf HTTPS auf oder warnen. Ein `<a>`-Link auf eine http://-Seite ist kein Mixed Content, schickt Besucher aber trotzdem über eine unverschlüsselte Verbindung, die abgehört und manipuliert werden kann. Verweise auf interne Hosts, die tatsächlich kein TLS haben, werden ebenfalls gemeldet; schalten Sie diese Stellen mit einem `{# djlint:off H022 #}`-Block stumm, statt die Regel zu deaktivieren.

Nicht so:

```html
<a href="http://example.com">Example</a>
```

Sondern so:

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

HTML5-Dokumente sind UTF-8, das Zeichen selbst funktioniert also überall und ist das, was Reviewer tatsächlich lesen; ein Tippfehler in einer Entity-Referenz (z. B. `&mdsah;`) wird vom Browser nicht erkannt und erscheint unverändert als kaputter Text. djLint erlaubt die Entities, die Syntax tragen (`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;` sowie die geschweiften Klammern `&lbrace;` und `&rbrace;` zusammen mit `&percnt;`, `&num;` und `&dollar;`, die ausgeschrieben einen Template-Begrenzer vervollständigen würden), und jene, die ein unsichtbares Zeichen bezeichnen, das sich daher nicht als Zeichen selbst prüfen lässt: die Leerzeichen (`&nbsp;`, `&thinsp;`, `&hairsp;`), die Verbinder und Richtungsmarken (`&zwnj;`, `&zwj;`, `&lrm;`, `&rlm;`) und `&shy;`, jeweils in benannter, dezimaler und hexadezimaler Form.

`--reformat` ersetzt die Entity für Sie durch das Zeichen. Eine Entity innerhalb eines Template-Tags gehört zum Tag und nicht zur Seite, daher fassen weder die Regel noch der Formatter sie an. `--no-entity-formatting` schaltet das Ersetzen ab, lässt die Regel aber aktiv, sodass eine Entity weiterhin gemeldet wird. Fügen Sie `H023` zu `ignore` hinzu, um Entities zu behalten.

Nicht so:

```html
<p>Dates 1900 &mdash; 2000</p>
```

Sondern so:

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript und text/css sind in HTML5 die Standardwerte für `<script>` und `<style>`, das Attribut ist also Ballast, den der Browser ignoriert; die WHATWG-Spezifikation sagt ausdrücklich, es wegzulassen. Wer es weglässt, vermeidet außerdem veraltete MIME-Strings, die das Element kaputtmachen, wenn sie auf Modul-Skripte übertragen werden (wo type="module" tatsächlich eine Rolle spielt).

Nicht so:

```html
<script type="text/javascript" src="app.js">
```

Sondern so:

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

Ein Tag ohne sein passendes öffnendes oder schließendes Tag zwingt die Fehlerbehandlung des Browsers zu raten, wo das Element endet, sodass nachfolgendes Markup im falschen Element landet; Layout, CSS-Selektoren und DOM-Abfragen in JavaScript gehen dann stillschweigend und je nach Browser unterschiedlich kaputt. H025 meldet auch ein `<ol>` oder `<ul>`, das innerhalb eines `<p>` geöffnet wird: Der HTML-Parser schließt den Absatz vor der Liste, sodass das Markup nie so verschachtelt ist, wie es geschrieben steht.

Nicht so:

```html
<div>
  <p>Hello</p>
```

Sondern so:

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Empty id and class tags can be removed.`

Kein Klassen- oder id-Selektor trifft auf ein leeres Attribut zu, und eine leere id ist ungültiges HTML (der id-Wert darf nicht der leere String sein). Ein Selektor auf das bloße Vorhandensein des Attributs wie `div[class]` trifft es dagegen schon, sodass das Entfernen für ein so geschriebenes Stylesheet sichtbar ist. Meist weist es auf einen Template-Fehler hin, bei dem eigentlich eine Variable eingesetzt werden sollte; wer es entfernt oder füllt, sorgt dafür, dass dieser Fehler nicht unbemerkt bleibt.

Nicht so:

```html
<div id="" class="">content</div>
```

Sondern so:

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

Ein Anführungszeichen, das innerhalb von `{% ... %}` oder `{{ ... }}` geöffnet, aber nie geschlossen wird, lässt die Template-Engine das Tag falsch parsen: Django und Jinja lösen entweder beim Rendern einen TemplateSyntaxError aus oder verschlucken die restlichen Argumente des Tags stillschweigend als String-Inhalt, sodass die Seite mit einem 500er abbricht oder mit fehlenden Argumenten gerendert wird.

Nicht so:

```html
{% trans "Welcome %}
```

Sondern so:

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

Standardmäßig deaktiviert; aktivieren Sie die Regel mit `--include=T028`.

Der Leerraum, den ein Tag mit Whitespace-Kontrolle entfernt, ist Leerraum, der gerendert wird. Wenden Sie die Regel daher nur dort an, wo das Attribut keinen zu verlieren hat. `alt="{%- if brand -%}Acme{%- endif -%} logo"` wird als `Acmelogo` gerendert, und ein SVG-`d="M12 {%- if big -%}20{%- endif -%} 4Z"` wird zu einem anderen Pfad. Deshalb muss die Regel ausdrücklich aktiviert werden.

Template-Tags innerhalb eines Attributwerts geben den Leerraum und die Zeilenumbrüche um sie herum in das gerenderte Attribut aus, sodass ein mit einfachen `{% if %}`/`{% for %}`-Tags gebautes href oder src verirrte Leerzeichen enthalten und kaputte URLs erzeugen kann. Die Tags mit Whitespace-Kontrolle von Jinja/Nunjucks (`{%- ... -%}`) entfernen diesen umgebenden Leerraum, sodass das Attribut als ein einziger sauberer Wert gerendert wird. Das class-Attribut ist ausgenommen, da zusätzlicher Leerraum zwischen Klassennamen harmlos ist.

Gilt nicht für das Profil django: Django-Template-Tags unterstützen keine Whitespace-Kontrolle mit `{%- -%}`.

Nicht so:

```html
<a href="{% if x %}/home{% endif %}"></a>
```

Sondern so:

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

Die HTML-Spezifikation definiert die Schlüsselwörter für die Formularmethode in Kleinbuchstaben (get, post); großgeschriebene Varianten akzeptieren Browser nur dank eines Abgleichs, der Groß- und Kleinschreibung ignoriert. Die kanonische Kleinschreibung hält Templates einheitlich und mit grep durchsuchbar und vermeidet Beanstandungen durch strenge Validatoren und XHTML-basierte Toolchains.

Nicht so:

```html
<form method="POST"></form>
```

Sondern so:

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

Suchmaschinen verwenden die Meta-Description als Snippet unter Ihrem Seitentitel in den Ergebnissen; fehlt sie, bauen sie ein Snippet aus beliebigem Seitentext zusammen, was die Klickrate senkt und schwache Linkvorschauen erzeugt, wenn die Seite geteilt wird.

Schlägt nur bei Dateien an, die ein vollständiges `<html>`...`</html>`-Dokument enthalten. Das Argument mit dem Snippet gilt für öffentlich indexierte Seiten; bei Apps hinter einer Anmeldung oder im Intranet wird diese Regel häufig deaktiviert.

Nicht so:

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

Sondern so:

```html
<html lang="en">
  <head>
    <title>Home</title>
    <meta name="description" content="A short summary of this page.">
  </head>
  <body>Welcome</body>
</html>
```

#### T032

`Extra whitespace found in template tags.`

Folgen von Leerzeichen oder Tabs zwischen den Argumenten eines Template-Tags sind unsichtbares Rauschen: Sie verbergen echte Unterschiede in Diffs, lassen ein fehlendes Argument leicht übersehen und weichen vom Stil mit einfachen Leerzeichen ab, den der Formatter von djLint erzeugt, was unnötige Änderungen beim Neuformatieren verursacht. Leerraum innerhalb von Strings in Anführungszeichen bleibt erhalten und wird nicht gemeldet.

Nicht so:

```html
{% static  'css/style.css' %}
```

Sondern so:

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

Leerraum am Anfang oder Ende des action-Werts eines Formulars wird Teil der gerenderten URL. Browser entfernen ihn beim Parsen, Clients ohne Browser und Tests, die den wörtlichen Wert verwenden, aber womöglich nicht, und rund um ein `{% url %}`-Tag deutet das verirrte Leerzeichen fast immer auf einen Tippfehler hin, der eine Absende-URL rendert, die beim serverseitigen Routing nicht passt.

Nicht so:

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

Sondern so:

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Did you intend to use {% ... %} instead of {% ... }%?`

}% ist fast immer ein Tippfehler für %}. Die Template-Engine erkennt }% nicht als Tag-Begrenzer, sodass das Tag nie geparst wird: Der rohe Text {% ... }% landet im gerenderten HTML, oder die Engine löst einen Syntaxfehler aus, wenn sie auf das nicht geschlossene Tag stößt.

Nicht so:

```html
{% include "footer.html" }%
```

Sondern so:

```html
{% include "footer.html" %}
```

#### H036

`Do not use br tags for spacing.`

Die HTML-Spezifikation erlaubt `<br>` nur für einen Zeilenumbruch, der Teil des Inhalts selbst ist, etwa in einer Postanschrift oder einem Gedicht, und diese Verwendung bleibt unangetastet. Gemeldet wird die darstellende Verwendung, die die Spezifikation ausschließt: eine Folge von zwei oder mehr Umbrüchen, also vertikaler Abstand, und ein Umbruch direkt an der Innenkante eines Block-Elements, der nichts rendert, was dessen eigener Außenabstand nicht auch täte. Beides stört den Textumbruch bei schmalen Breiten, und ein Screenreader sagt einen erzwungenen Umbruch an, wo es nichts anzusagen gibt.

Nicht so:

```html
<p>Shipping is free.<br><br>Delivery takes 3 days.</p>
```

Sondern so:

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

Doppelte Attribute sind ungültiges HTML, und Browser behalten nur das erste Vorkommen und verwerfen den Rest stillschweigend, sodass der zweite class- oder style-Wert nie wirkt und echte Fehler verborgen bleiben. Die Prüfung kennt Templates: Ein Attribut, das in sich gegenseitig ausschließenden Zweigen (`{% if %}`/`{% else %}`) wiederholt wird, wird nicht gemeldet, da nur eine Kopie gerendert werden kann.

Nicht so:

```html
<div class="card" id="profile" class="active">...</div>
```

Sondern so:

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

Ein Block-Tag wie `{% if %}`, `{% for %}` oder `{% macro %}` ohne passendes End-Tag ist in Django und Jinja ein harter TemplateSyntaxError: Die Seite lässt sich bei der Anfrage nicht rendern, und diese Regel fängt das vor dem Deployment ab. Sie meldet auch verwaiste End-Tags ohne öffnendes Tag und falsch verschränkte Blöcke (z. B. `{% if %}``{% for %}``{% endif %}`).

Die Zuordnung von `{% block %}`/`{% endblock %}` und nicht passende Endblock-Namen prüft diese Regel; T003 (standardmäßig deaktiviert) verlangt zusätzlich einen Namen an jedem mehrzeiligen `{% endblock %}`. Eigene Block-Tags, die über custom_blocks registriert sind, werden ebenfalls geprüft, einschließlich ihrer selbstschließenden Form mit / %}.

Nicht so:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

Sondern so:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Unclosed template tag found.`

Ein Template-Tag, das mit `{{` oder `{%` geöffnet, aber nie mit dem passenden `}}` oder `%}` geschlossen wird, wird nicht als Tag geparst: Django/Jinja lösen entweder einen TemplateSyntaxError aus oder rendern die rohen Klammerzeichen in die Seite, und alles bis zum nächsten Begrenzer kann stillschweigend verschluckt werden. Solche Tippfehler (eine einzelne fehlende Klammer, ein nicht passender Begrenzer) übersieht man im Review leicht, weil das Template womöglich noch teilweise gerendert wird.

Nicht so:

```html
<p>{{ user.name }</p>
```

Sondern so:

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

Ein `{% extends %}`- oder `{% include %}`-Tag mit fehlendem, leerem oder nur aus Leerraum bestehendem Template-Namen hat nichts zu laden: Django löst einen TemplateSyntaxError aus, wenn der Name ganz fehlt, und beim Rendern einen TemplateDoesNotExist, wenn er leer ist. Die Seite bricht in der Produktion also mit einem 500er ab, obwohl die Template-Datei selbst syntaktisch plausibel aussieht.

Nicht so:

```html
{% extends "" %}
```

Sondern so:

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

Wird ein HTML-Tag in einem `{% block %}` geöffnet, aber in einem anderen geschlossen, erbt ein Kind-Template, das nur einen dieser Blöcke überschreibt, das halbe Element, und die gerenderte Seite enthält unausgeglichenes Markup. Browser schließen oder verschachteln Elemente dann unvorhersehbar neu, was Layout und CSS-Selektoren weit entfernt von dem Template zerstört, das tatsächlich bearbeitet wurde. Wird jedes Element im selben Block geöffnet und geschlossen, lässt sich jeder Block gefahrlos unabhängig überschreiben.

Nicht so:

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

Sondern so:

```html
{% block content %}
<div class="wrapper">
</div>
{% endblock content %}
{% block footer %}
{% endblock footer %}
```

#### T041

`Extends tag should be the first tag in the template.`

Django weigert sich, ein Template zu kompilieren, in dem ein anderes Tag vor `{% extends %}` steht, und Text, der davor steht, wird gerendert und landet so in der Seite noch vor allem, was das Eltern-Template erzeugt. Jinja rendert diesen Text ebenfalls, und nunjucks verwirft ihn, sodass das Template in keiner Engine tut, wonach es aussieht.

Ein `{# #}`-Kommentar rendert nichts und zählt nicht, ebenso wenig alles innerhalb eines `{% comment %}`-, <code>{&#37; raw %}</code>- oder `{% verbatim %}`-Blocks, ob benannt oder nicht, ein `{# djlint:off #}`-Bereich in jeder seiner drei Schreibweisen oder YAML-Front-Matter. Ein HTML-Kommentar zählt dagegen: Die Engine schreibt ihn vor dem Doctype des Eltern-Templates in die Seite, und genau um dieses Durchsickern geht es bei dieser Regel. Dasselbe gilt für einen `{% blocktrans %}`-Block, einen `{% filter %}`-Block und einen `<?php ?>`-Block, die alle etwas rendern. Geprüft wird nur das erste `{% extends %}`; ein zweites ist ein eigener Fehler. In den Profilen jinja und nunjucks zählt ein Verzweigungs-Tag davor nicht, da jinja `{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}` als Weg dokumentiert, ein Eltern-Template zu wählen; django liest den Rest des Templates in das `{% extends %}` ein und lehnt dann das `{% endif %}` ab, daher zählt in diesem Profil ein Verzweigungs-Tag.

Gilt nicht für die Profile handlebars, golang, liquid und angular.

Nicht so:

```html
{% load static %}
{% extends "base.html" %}
```

Sondern so:

```html
{% extends "base.html" %}
{% load static %}
```

#### H042

`Label for attribute has no matching element id in this file.`

Die Prüfung läuft nur bei Dateien, die sie zuverlässig analysieren kann: Enthält die Datei irgendetwas, das eine in dieser Datei nicht sichtbare id rendern könnte (eine `{{ ... }}`-Ausgabe wie ein Formular-Widget, ein `{% include %}` oder `{% extends %}` oder ein unbekanntes Template-Tag), bleibt die Regel für diese Datei stumm. Wo sie läuft, ist eine Meldung eine tatsächlich kaputte Zuordnung.

Nicht so:

```html
<label for="email">Email</label>
<input id="username">
```

Sondern so:

```html
<label for="email">Email</label>
<input id="email">
```

#### T042

`Content outside a block is not rendered in a template that extends another.`

Sobald ein Template ein anderes erweitert, entscheidet das Eltern-Template, was ausgegeben wird, und das Kind füllt nur dessen Blöcke. Text oder HTML, das nach `{% extends %}` und außerhalb jedes `{% block %}` steht, wird beim Rendern stillschweigend verworfen, sodass ein Absatz, der im Quelltext gut aussieht, nie auf der Seite ankommt.

Ein Template-Tag an dieser Stelle wird trotzdem ausgeführt, daher bleiben `{% load %}`, `{% set %}` und ein `{% if %}` um einen Block herum unangetastet, ebenso `{# #}`- und `{% comment %}`-Kommentare, HTML-Kommentare, <code>{&#37; raw %}</code>- und `{% verbatim %}`-Blöcke sowie der Rumpf eines `{% macro %}`, eines `{% set %}` in Blockform, eines `{% partialdef %}` oder eines `{% addtoblock %}`, der erfasst statt ausgegeben wird. Der Text eines `{% blocktrans %}` wird gemeldet, da ein `{% blocktrans %}` kein `{% block %}` ist. Berücksichtigt wird nur Inhalt nach dem extends-Tag, und jeder zusammenhängende Abschnitt davon wird einmal gemeldet, an seinem Anfang.

Die Engine liest Template-Tags vor HTML, daher wird ein `{% extends %}` in einem HTML-Kommentar oder einem `<pre>` trotzdem ausgeführt und macht die Datei trotzdem zu einem Kind; nur `{# #}`, `{% comment %}`, <code>{&#37; raw %}</code> und `{% verbatim %}` verbergen eines wirklich. Text in einem HTML-Kommentar erreicht ohnehin keinen Leser und wird nicht gemeldet, die dort geschriebenen Tags werden aber trotzdem gelesen.

Gilt nicht für die Profile handlebars, golang, liquid und angular.

Nicht so:

```html
{% extends "base.html" %}
<p>This paragraph is never shown.</p>
{% block content %}
<h1>Welcome</h1>
{% endblock %}
```

Sondern so:

```html
{% extends "base.html" %}
{% block content %}
<h1>Welcome</h1>
<p>This paragraph is shown.</p>
{% endblock %}
```

#### H043

`Button tag should have a type attribute.`

Ein `<button>` ohne `type` ist standardmäßig `submit`, sodass ein Button, der ein Skript ausführen soll, auch das umgebende Formular absendet und die Seite neu lädt. Wer den Typ ausschreibt, verhindert das.

Nicht so:

```html
<form>
  <button onclick="preview()">Preview</button>
</form>
```

Sondern so:

```html
<form>
  <button type="button" onclick="preview()">Preview</button>
</form>
```

#### T043

`Block name is used more than once in the template.`

Django, Jinja und Nunjucks weigern sich alle, ein Template zu parsen, das zwei Blöcken denselben Namen gibt, sodass die Seite gar nicht erst lädt. Den Engines ist es egal, ob die beiden Blöcke in verschiedenen Zweigen eines `{% if %}` stehen; jeder Blockname muss daher im gesamten Template eindeutig sein, ob die Blöcke nebeneinander stehen oder einer im anderen verschachtelt ist.

Nur `{% block %}` zählt: Ein `{% blocktrans %}` ist kein Block, und ein `{% endblock name %}` nennt lediglich den Block, den es schließt. Namen werden so verglichen, wie sie geschrieben sind, da die Engines `Content` und `content` als zwei Blöcke behandeln.

Übersprungen wird nur, was die Engine selbst nie parst: ein Template-Kommentar, ein `{% comment %}`-Block, der Rumpf eines <code>{&#37; raw %}</code> oder `{% verbatim %}` und ein `djlint:off`-Bereich. Ein Block in einem HTML-Kommentar, im Rumpf eines `<script>`, `<style>`, `<pre>` oder `<textarea>` oder im Rumpf eines `{% filter %}` wird trotzdem gezählt, da die Engine all diese liest und beim doppelten Namen genauso einen Fehler auslöst.

Ein `{% embed %}` öffnet einen eigenen Gültigkeitsbereich: Die Blöcke darin füllen das eingebettete Template und nicht dieses, sodass zwei Embeds desselben Partials jeweils `{% block body %}` schreiben dürfen. Ein Name, der innerhalb eines einzigen Embeds wiederholt wird, wird trotzdem gemeldet.

Gilt nicht für die Profile handlebars, golang, liquid und angular.

Nicht so:

```html
{% block content %}{% endblock %}
{% block content %}{% endblock %}
```

Sondern so:

```html
{% block content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

#### H044

`Thead should not mix th and td cells.`

Jede Zeile wird für sich beurteilt, daher ist die Erklärungszeile aus `td`, die die HTML-Spezifikation in einem `thead` neben die Zeile mit den Überschriften setzt, keine Mischung. Ein leeres `td` am Anfang der Zeile ist die Eckzelle einer Tabelle mit Überschriften in der ersten Spalte, also genau das Markup, das das Barrierefreiheits-Tutorial des W3C verlangt, und wird daher übersprungen.

Ein `th` und ein `td` haben für einen Screenreader eine unterschiedliche Bedeutung und meist auch unterschiedliches CSS, sodass eine einzelne verirrte Zelle in einer Kopfzeile als Daten gelesen und anders gestaltet wird als die Spalten daneben. Die Mischung ist gültiges HTML, und gerade deshalb fällt sie schwer auf.

Nicht so:

```html
<thead>
  <tr>
    <th>Name</th>
    <td>Size</td>
  </tr>
</thead>
```

Sondern so:

```html
<thead>
  <tr>
    <th>Name</th>
    <th>Size</th>
  </tr>
</thead>
```

#### T044

`Output tag holds a statement keyword; use a block tag.`

Gilt nicht für die Profile golang, handlebars und angular.

Ein Ausgabe-Tag gibt einen Wert aus, und `if`, `for`, `url`, `include` und die übrigen sind Anweisungen, die in ein Block-Tag gehören. Django, Jinja und Nunjucks lehnen `{{ if x }}` alle mit einem Syntaxfehler ab, und ein schließendes Schlüsselwort für sich allein, etwa `{{ endif }}`, wird als Variable gelesen, die nichts rendert, während der Block, den es schließen sollte, offen bleibt. Die Seite lädt also entweder gar nicht oder zeigt, was die Bedingung hätte verbergen sollen.

Ein bloßes Schlüsselwort ist ein gewöhnlicher Variablenname, daher werden `{{ url }}`, `{{ url|default:"/" }}` und `{{ set.name }}` nicht gemeldet. Gemeldet wird nur ein Schlüsselwort mit Argument sowie ein schließendes oder verzweigendes Schlüsselwort für sich allein wie `{{ endif }}` oder `{{ else }}`. Ein Steuerschlüsselwort wie `if` oder `for` kann keinen Ausdruck einleiten, daher ist alles, was danach kommt, ein Argument, auch ein Operator, und `{{ if -1 > count }}` wird gemeldet. Die übrigen Namen dienen auch als Variablen und Funktionen, und dort zählt nur ein String in Anführungszeichen oder ein Wort als Argument, sodass ein Ausdruck, der zufällig mit einem davon beginnt, unangetastet bleibt: `{{ url ~ "/x" }}`, `{{ url if url else "#" }}`, `{{ url ? url : '#' }}`, `{{ block ('title') }}`, `{{ block .super }}` und `{{ filter [0] }}` lösen alle keine Meldung aus.

Der Rumpf eines <code>{&#37; raw %}</code>- oder `{% verbatim %}`-Blocks ist Text und keine Template-Syntax und wird übersprungen, die benannte Form `{% verbatim vueapp %}...{% endverbatim vueapp %}` eingeschlossen, sodass ein auf diese Weise geschütztes `{{ }}` von Vue oder Handlebars nicht gemeldet wird. Ein `{{ }}` innerhalb eines Arguments in Anführungszeichen eines Block-Tags, wie in `{% trans "Write {{ if x }} instead" %}`, ist Text, den die Engine ausgibt, und bleibt ebenfalls unangetastet.

Nicht so:

```html
{{ if user.is_active }}
```

Sondern so:

```html
{% if user.is_active %}
```

#### H045

`Iframe tag should have a title attribute.`

Ein Screenreader kündigt ein iframe mit seinem zugänglichen Namen an. Fehlt dieser, liest er die URL des Frames vor oder gar nichts, und man kann nicht erkennen, was die eingebettete Seite ist, bevor man sie betritt. WCAG ordnet das unter 4.1.2 Name, Rolle, Wert ein, und axe wie html-validate liefern die Prüfung standardmäßig mit.

Der Name kann aus `title`, `aria-label` oder `aria-labelledby` stammen, und jedes der drei erfüllt die Regel. Ein von einem Template-Tag geschriebener Name zählt, sodass ein Frame mit seitenabhängigem Titel nicht gemeldet wird.

Nicht so:

```html
<iframe src="/report/"></iframe>
```

Sondern so:

```html
<iframe src="/report/" title="Quarterly report"></iframe>
```

#### T045

`Template tag inside an html comment still runs; use a template comment to disable it.`

Ein HTML-Kommentar verbirgt Markup vor dem Browser, nicht vor der Template-Engine. `<!-- {% include "debug.html" %} -->` rendert die Datei trotzdem, und `<!-- {% if debug %}...{% endif %} -->` wird trotzdem ausgewertet, in Django, Jinja, Nunjucks, Handlebars und Go gleichermaßen. Ein so auskommentiertes Tag läuft also weiter, und was es schreibt, landet im Kommentar oder bricht, wenn es `-->` enthält, aus ihm aus. Nur ein Template-Kommentar, `{# #}` in Django und Jinja, `{{! }}` in Handlebars oder `{{/* */}}` in Go, hindert ein Tag daran, ausgeführt zu werden.

Gemeldet wird nur ein Anweisungs-Tag: `{% %}` in den Profilen, die es kennen, eine Section, ein schließendes Tag oder ein Partial von Handlebars und ein Go-Schlüsselwort wie `{{if}}` oder `{{end}}`. Ein in einen Kommentar ausgegebener Wert, wie in `<!-- built {{ version }} -->`, ist eine bewusste Verwendung und bleibt unangetastet, ebenso ein Tag in einem Template-Kommentar, einem `{% comment %}`-Block oder einem raw-Block und ein bedingter Kommentar für den Internet Explorer, `<!--[if IE]> ... <![endif]-->`, dessen Rumpf Markup für den genannten Browser ist.

Ein bloßes Go-Schlüsselwort ist in jeder anderen Engine ein gewöhnlicher Variablenname, daher sind `<!-- period {{ start }} to {{ end }} -->` und `<!-- Template: {{ template }} -->` unter Django, Jinja, Nunjucks, Handlebars und Liquid Werte und gelten nur unter `--profile golang` als Anweisungen. Eines mit einem Go-Operanden, wie bei `{{ if .X }}` und `{{ template "footer" . }}`, ist eine Anweisung, die keine andere Engine ausgibt, und wird in jedem Profil gemeldet. `{%` wird ebenso nur dort gelesen, wo die Engine es kennt, unter `--profile handlebars` und `--profile golang` ist es also Text, und eine Öffnung, auf die keine schließende Klammer folgt, wie in `<!-- battery at 50{% charge -->`, ist der Fließtext, nach dem sie aussieht. Ein bedingter Kommentar ist einer, der als solcher geschrieben ist: Er beginnt mit `<!--[if` und wird durch sein `<![endif]-->` in beliebiger Groß-/Kleinschreibung geschlossen. Bleibt er ungeschlossen, ist er der gewöhnliche Kommentar, als den ein Browser ihn liest, und die Tags darin werden gemeldet.

Nicht so:

```html
<!-- {% include "banner.html" %} -->
```

Sondern so:

```html
{# {% include "banner.html" %} #}
```

#### H046

`Tabindex should not be positive.`

Ein positiver `tabindex` zieht ein Element an den Anfang der Tab-Reihenfolge, vor alles, was keinen hat. Schon ein einziges davon ordnet die ganze Seite für Tastaturnutzer neu, und die Reihenfolge muss dann in jedem Template, das ein Bedienelement hinzufügt, von Hand gepflegt werden. WCAG behandelt das unter 2.4.3 Fokus-Reihenfolge.

`0` setzt ein Element an die Stelle der Tab-Reihenfolge, die ihm das Dokument gibt, und `-1` nimmt es heraus, lässt es aber per Skript fokussierbar. Keines von beiden wird gemeldet, ebenso wenig ein von einem Template-Tag geschriebener Wert, dessen Zahl hier nicht bekannt ist.

Nicht so:

```html
<input tabindex="1">
```

Sondern so:

```html
<input tabindex="0">
```

#### H047

`Aria-hidden should not be set on a focusable element.`

`aria-hidden="true"` nimmt ein Element aus dem Barrierefreiheitsbaum, lässt es aber in der Tab-Reihenfolge, sodass Tastaturnutzer trotzdem darauf landen und nichts angesagt bekommen. Ein dekoratives Icon auszublenden ist die übliche Verwendung des Attributs und wird nicht gemeldet; gemeldet wird nur ein Element, das von sich aus den Fokus erhält.

Ein Element gilt als fokussierbar, wenn es ein `button`, `select`, `textarea`, `iframe` oder `summary` ist, ein `a` oder `area` mit `href`, ein `input`, das nicht hidden ist, ein `audio` oder `video` mit `controls` oder irgendein Element mit `contenteditable` oder einem `tabindex` von `0` oder mehr. Ein `disabled`-Bedienelement oder eines mit `tabindex="-1"` ist bereits nicht in der Tab-Reihenfolge und bleibt unangetastet.

Nicht so:

```html
<button aria-hidden="true">Close</button>
```

Sondern so:

```html
<button type="button" aria-label="Close"><span aria-hidden="true">x</span></button>
```

#### H048

`Aria attribute is not one the specification defines.`

Ein falsch geschriebenes aria-Attribut bewirkt überhaupt nichts. Kein Browser warnt, kein Screenreader meldet es, und das Markup erweckt weiterhin den Anschein, barrierefrei gemacht worden zu sein. So kann `aria-lable` jahrelang in einem Template stehen, während das Bedienelement, das es benennen sollte, unbenannt bleibt.

Die Regel kennt die Namen, die ARIA definiert. Ein von einem Framework geschriebenes Binding ist kein einfacher aria-Name, daher bleiben `:aria-label`, `v-bind:aria-label` und `[attr.aria-label]` unangetastet.

Nicht so:

```html
<button type="button" aria-lable="Close">x</button>
```

Sondern so:

```html
<button type="button" aria-label="Close">x</button>
```

#### H049

`Viewport should not stop the page being zoomed.`

`user-scalable=no` und eine `maximum-scale` unter 2 verhindern, dass eine Seite auf dem Smartphone vergrößert werden kann, und für viele Menschen ist das die einzige Möglichkeit, sie zu lesen. WCAG verlangt unter 1.4.4 Textgröße ändern 200 %. Browser ignorieren die Einschränkung zunehmend, doch überall, wo sie beachtet wird, schaltet das Tag den Zoom weiterhin ab.

Name und Inhalt werden gefunden, egal in welcher Reihenfolge die beiden geschrieben sind.

Nicht so:

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

Sondern so:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### H050

`Element is obsolete and should be replaced.`

`<center>`, `<font>`, `<big>`, `<strike>` und `<tt>` wurden gestrichen, als CSS die Darstellung übernahm, und `<marquee>`, `<blink>`, `<nobr>` und `<spacer>` waren nie Standard. HTML definiert keines davon mehr, daher garantiert nichts, wie ein Browser sie darstellt, und ein Stylesheet kann sie nicht so ansprechen wie eine Klasse.

Die Regel kennt die Elemente `acronym`, `applet`, `basefont`, `bgsound`, `big`, `blink`, `center`, `dir`, `font`, `frame`, `frameset`, `isindex`, `keygen`, `marquee`, `menuitem`, `nobr`, `noembed`, `noframes`, `plaintext`, `spacer`, `strike`, `tt` und `xmp`. Gemeldet wird nur das öffnende Tag, sodass jedes Element einmal genannt wird, und ein Custom Element, dessen Name lediglich mit einem davon beginnt, wie `<font-picker>`, bleibt unangetastet.

Nicht so:

```html
<center><font color="red">Warning</font></center>
```

Sondern so:

```html
<p class="warning">Warning</p>
```

#### H051

`Role is not one ARIA defines for markup.`

Eine Rolle, die keine Spezifikation nennt, wird kurzerhand verworfen, und das Element behält die Bedeutung, die es schon hatte. `role="buton"` lässt ein `<div>` also ein `<div>` sein: für einen Screenreader nichts, während das Markup aussieht, als hätte es einen Zweck bekommen. Nichts warnt davor, und gerade deshalb lohnt es sich, den Tippfehler abzufangen.

Die Regel kennt die Rollen, die ARIA für Autoren definiert, zusammen mit denen, die DPUB-ARIA (`doc-chapter` und die übrigen) und GRAPHICS-ARIA (`graphics-symbol` und die übrigen) hinzufügen. Die abstrakten Rollen von ARIA, etwa `landmark` und `sectionhead`, werden gemeldet: Laut Spezifikation existieren sie, um ihre Ontologie aufzubauen, und dürfen nicht in Markup geschrieben werden.

Eine `role` kann als Fallback-Liste mehrere Namen enthalten, und jeder wird geprüft. Ein Wert mit Template-Syntax ist nicht bestimmbar und bleibt unangetastet, ebenso ein von einem Framework geschriebenes Binding wie `:role` oder `[attr.role]`.

Nicht so:

```html
<div role="buton">Save</div>
```

Sondern so:

```html
<button type="button">Save</button>
```

#### H052

`Meta refresh should not reload or redirect the page on a timer.`

Ein zeitgesteuerter Refresh verändert die Seite, während jemand sie noch liest. Wer langsam liest, einen Screenreader nutzt oder einfach unterbrochen wurde, verliert ohne Vorwarnung und ohne Möglichkeit, es zu verhindern, die Stelle, an der er war, was gegen WCAG 2.2.1 Zeiteinteilung anpassbar verstößt, und ein Refresh, der dieselbe Seite neu lädt, verwirft alles, was darin eingegeben wurde.

Eine Verzögerung von null ist eine sofortige Weiterleitung und kein Timer, was WCAG dort erlaubt, wo keine serverseitige Weiterleitung möglich ist; sie wird daher nicht gemeldet. Die beiden Attribute werden gefunden, egal in welcher Reihenfolge sie geschrieben sind.

Nicht so:

```html
<meta http-equiv="refresh" content="30">
```

Sondern so:

```html
<meta http-equiv="refresh" content="0; url=/next-page">
```

#### H053

`Id is used more than once in the file.`

Eine id benennt ein Element. Ein zweites Element mit derselben id macht `getElementById`, `<label for>`, Fragment-Links und `aria-labelledby` kaputt: Der Browser nimmt das erste und ignoriert die übrigen stillschweigend, sodass ein Label, ein Link oder ein Skript ohne jede Warnung beim falschen Element landet.

Zwei ids in sich gegenseitig ausschließenden Zweigen eines `{% if %}...{% else %}...{% endif %}` werden nie beide gerendert und daher nicht gemeldet. Eine `{% for %}`-Schleife oder ein `{% block %}` ist kein Zweig: Eine id darin und dieselbe id außerhalb werden beide gerendert, und die spätere wird gemeldet. Ein von einem Template-Tag geschriebener Wert ist nicht bestimmbar und bleibt unangetastet, ebenso ein leerer Wert. Die ids werden exakt verglichen, wie es der Browser tut, daher sind `save` und `Save` zwei ids.

Zweige werden in der Sprache gelesen, in der die Datei geschrieben ist, und mit jedem Leerraum, den die Sprache zwischen den Begrenzern und dem Tag-Namen erlaubt: `{% elif %}` und `{% else %}`, `{% elsif %}` und `{% when %}` von Liquid, `{{ else }}` von Go, eine Mako-Zeilenanweisung `% else:` sowie `{{else}}` von Handlebars, sein verkettetes `{{else if x}}` und die inverse Section jedes `{{#helper}}`-Blocks, eigene Helper eingeschlossen. Der Inhalt eines `<template>` ist ein eigenes Dokumentfragment, das `getElementById` nie erreicht, daher wird eine id dort nur mit den ids desselben `<template>` verglichen: Zwei `<template>`-Elemente dürfen jeweils eine Zeile mit derselben id enthalten, zwei solche innerhalb eines `<template>` werden aber trotzdem gemeldet. Eine id in einem Kommentar, im Rumpf eines <code>{&#37; raw %}</code> oder `{% verbatim %}` oder in einem `djlint:off`-Bereich wird gar nicht gelesen.

Nicht so:

```html
<button type="submit" id="submit">Save</button>
<button type="submit" id="submit">Save and continue</button>
```

Sondern so:

```html
<button type="submit" id="submit">Save</button>
<button type="button" id="cancel">Cancel</button>
```

#### H054

`Interactive element should not be nested inside another.`

HTML verbietet interaktive Inhalte innerhalb von `<a>` und `<button>`. Ein Button in einem Link oder ein Link in einem Button ist ungültiges Markup, das jeder Browser auf seine eigene Weise repariert, und Screenreader- oder Tastaturnutzer bekommen ein Bedienelement, das sich wie zwei verhält. axe meldet dasselbe als „nested-interactive“.

Überwacht werden als Container ein `<a>` mit `href` und ein `<button>`, und gemeldet werden darin als Bedienelemente ein Link mit `href`, `button`, `input`, `select` und `textarea`. Ein `<a>` ohne `href` ist nicht interaktiv und bleibt auf beiden Seiten unangetastet, ebenso ein verstecktes Input oder eines, dessen Typ ein Template-Tag schreibt. Der Inhalt eines `<template>` wird nicht dort gerendert, wo er steht, daher ist ein Bedienelement darin nicht in den umgebenden Link verschachtelt; eine Verschachtelung innerhalb des Templates wird aber trotzdem gemeldet.

Ein Attribut wird dort gelesen, wo ein Tag eines schreibt, und nirgendwo sonst: Das `href` von `{% if not href %}` bezeichnet eine Variable, das in `{# href="{{ url }}" #}` ist auskommentiert, und das in `data-attr=href` gehört zu einem anderen Attribut, während das `href`, das ein `{% if %}` zwischen seine eigenen Tags schreibt, ein Attribut wie jedes andere ist. Ein offen gelassener Link oder Button endet mit dem Element um ihn herum, so wie im Browser, sodass ein einzelner Tippfehler nicht den Rest der Datei meldet; einer, der auf oberster Ebene offen bleibt, hat nichts um sich, was ihn beendet, und reicht tatsächlich bis zum Ende der Datei, wo H025 das verwaiste Tag ebenfalls meldet.

Nicht so:

```html
<a href="/cart"><button>Add</button></a>
```

Sondern so:

```html
<a href="/cart" class="button">Add</a>
```

#### H055

`Lang attribute should be a language tag such as en or pt-BR.`

H005 verlangt ein `lang` auf `<html>`, doch ein Wert wie `lang="english"` oder `lang="en_US"` erfüllt diese Regel, ohne eine Sprache zu nennen, die ein Browser kennt. Ein Screenreader greift dann auf seine Standardstimme zurück, und Übersetzung und Silbentrennung wählen die falschen Regeln oder gar keine. Der Wert muss ein BCP-47-Tag sein: zwei oder drei Buchstaben, dann beliebig viele Subtags aus einem bis acht Buchstaben oder Ziffern, jeweils nach einem Bindestrich, wie in `en`, `pt-BR` oder `zh-Hant-TW`.

Geprüft wird nur das `<html>`-Tag, passend zu H005. Ein leerer Wert bleibt jener Regel überlassen, während ein Wert, der nur aus Leerraum besteht, hier gemeldet wird, da H005 ihn als Wert liest. Ein Wert, den ein Template-Tag schreibt, wie in `lang="{{ LANGUAGE_CODE }}"`, oder ein PHP-Short-Echo, wie in `lang="<?= $lang ?>"`, ist nicht bestimmbar und bleibt unangetastet, ein Wert, der lediglich mit `$` oder `{` beginnt, wie in `lang="$LANG"`, wird dagegen so gelesen, wie er geschrieben ist. `xml:lang` oder `data-lang` wird nicht als `lang` gelesen, und ein `>` innerhalb eines Template-Tags vor dem Attribut, wie in `{% if a > b %}`, verbirgt es nicht.

Nicht so:

```html
<html lang="english">
```

Sondern so:

```html
<html lang="en">
```

#### H056

`Src should not be empty.`

Die HTML-Spezifikation erklärt ein leeres `src` für ungültig und warnt, dass ein Browser es relativ zur URL des Dokuments selbst auflöst, sodass `<img src="">` die Seite erneut als Bild und `<script src=""></script>` sie als Skript abruft. Meist ist es ein Platzhalter, den ein Skript füllen sollte, und die Lösung besteht darin, das Attribut wegzulassen oder den Wert in einem data-Attribut zu halten, bis es einen echten gibt. Ein `src` ganz ohne Wert, wie in `<img src>`, ist ebenfalls leer und wird gemeldet.

Geprüft werden nur `img`, `script`, `iframe`, `embed`, `source`, `track`, `audio` und `video`, da dies die Elemente sind, die abrufen, was `src` nennt. Gemeldet wird nur ein Wert, den ein Browser als leer liest; ein Wert ohne Anführungszeichen wie `<img src=/static/logo.png>` bleibt also unangetastet, ebenso ein Wert, der nur aus Leerraum besteht, und ein von einem Template-Tag geschriebener Wert, und `srcset` und `data-src` sind andere Attribute, die die Regel nicht beurteilt.

Nicht so:

```html
<img src="" alt="Logo">
```

Sondern so:

```html
<img src="{% static 'logo.png' %}" alt="Logo">
```

#### H057

`Video should have a captions track.`

Ein Video mit Ton transportiert seine Sprache nur über die Tonspur, sodass gehörlose oder schwerhörige Zuschauer ohne Untertitel nichts davon haben; WCAG 1.2.2 Untertitel (aufgezeichnet) verlangt sie. Ein `<track>` mit einem `kind` von `captions` oder `subtitles` innerhalb des `<video>` erfüllt die Regel, ebenso ein `<track>` ganz ohne `kind`, da `subtitles` der Standardwert ist.

Ein `muted`-Video hat keinen Ton, der untertitelt werden müsste, und wird nicht gemeldet. Ebenso wenig ein Video, dessen öffnendes Tag oder Rumpf ein Template-Tag enthält, da die Spuren oder das `muted`-Attribut vom Template geschrieben werden könnten, wo djLint sie nicht sieht. Als Template-Tag gilt eines, das eine Template-Sprache öffnet, `{{`, `{%`, `{#` oder `${`, daher sind ein jQuery-Handler wie `onclick="$(this).play()"`, ein `$refs` von Alpine, eine CSS-Klammer und ein Preis im Fallback-Text der gewöhnliche Text, nach dem sie aussehen, und das Video wird trotzdem gelesen.

`muted` muss das Attribut sein, daher ist `<video class=muted>` eine Klasse namens muted und wird gemeldet, und ein auskommentiertes oder in einen Attributwert geschriebenes `<track>` ist Text und keine Spur. Ein `</video>` in einem Wert beendet nichts, und das Element wird dort beurteilt, wo sein echtes End-Tag es schließt; ein offen gelassenes `<video>` bleibt also `H025` überlassen.

Nicht so:

```html
<video controls src="talk.mp4"></video>
```

Sondern so:

```html
<video controls src="talk.mp4">
  <track kind="captions" src="talk.vtt" srclang="en">
</video>
```

<!-- oxfmt-ignore-end -->

### Regeln hinzufügen

Pull Requests mit neuen Regeln sind willkommen!

Eine gute Regel besteht aus

- Name
- Code
- Meldung: die Meldung, die angezeigt wird, wenn der Fehler gefunden wird.
- Flags: Regex-Flags, zum Beispiel re.I|re.M. Standard ist re.DOTALL.
- Muster: reguläre Ausdrücke, die den Fehler finden.
- Ausschluss: optionale Liste von Profilen, für die die Regel nicht gilt.

Bitte fügen Sie einen Test hinzu, der die Regel überprüft.

## Benutzerdefinierte Regeln

Sie können eigene Regeln nur für Ihr Projekt hinzufügen, indem Sie neben Ihrer `pyproject.toml` eine Datei `.djlint_rules.yaml` anlegen. Regeln, die Sie in diese Datei schreiben, greift djLint automatisch auf. Eine Regeldatei an einem anderen Ort lässt sich mit der Befehlszeilenoption `--rules` angeben.

### Musterregeln

Sie können Regeln hinzufügen, die fehlschlagen, wenn eines der Regex-Muster einen Treffer hat:

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Regeln als Python-Modul

Sie können Regeln hinzufügen, die eine eigene Python-Funktion importieren und ausführen:

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

Das angegebene `python_module` muss eine Funktion `run()` enthalten, die für jede geprüfte Datei ausgeführt wird. Sie muss die folgenden Argumente akzeptieren:

- `rule`: Das Dict, das Ihre Regel in `.djlint_rules.yaml` darstellt. Über diese Variable greifen Sie typischerweise auf den Namen und die Meldung der Regel zu.
- `config`: Das Konfigurationsobjekt von djLint.
- `html`: Der vollständige HTML-Inhalt der Datei.
- `filepath`: Der Pfad der Datei, die gerade geprüft wird.
- `line_ends`: Liste der Zeichenpositionen `start` und `end` jeder Zeile, mit der Sie über `djlint.lint.get_line()` aus einer Zeichenposition Zeilennummern ermitteln können. Siehe das Beispiel.
- `*args, **kwargs`: Möglicherweise kommen künftig weitere Argumente hinzu. Nehmen Sie diese beiden Argumente daher auf, um das Risiko zu verringern, dass bei einem Upgrade von djLint etwas fehlschlägt.

Das Modul kann im Projektstamm liegen. Gibt es eine `line` oder ein `end` zurück, das keine Position ist, bricht djLint mit einem Fehler ab, der die Regel nennt.

Sie muss eine Liste von Dicts zurückgeben, eines pro Fehler, mit den folgenden Schlüsseln:

- `code`: Der Codename der Regel, die den Fehler meldet (typischerweise `rule['name']`)
- `line`: Zeilennummer und Zeichennummer in dieser Zeile, getrennt durch „:“, als String.
  Zum Beispiel bedeutet `"2:3"`, dass der Fehler in Zeile 2, Zeichen 3 gefunden wurde.
- `end`: Optional. Wo der Fehler endet, geschrieben wie `line`, direkt hinter seinem letzten Zeichen. Ohne diesen Schlüssel endet der Fehler dort, wo `match` endet.
- `match`: Der Teil des Inhalts, der den Fehler enthält
- `message`: Die Meldung, die ausgegeben wird, um den Fehler anzuzeigen (typischerweise `rule['message']`)

```python
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from djlint.helpers import inside_ignored_linter_block, inside_ignored_rule
from djlint.lint import get_line

if TYPE_CHECKING:
    from typing import Any

    from djlint.settings import Config
    from djlint.types import LintError


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> list[LintError]:
    """Rule that fails if the html file contains 'bad'.

    This is just an example, in reality it's much simpler to do that with a
    "pattern rule".
    """
    return [
        {
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "end": get_line(match.end(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        }
        for match in re.finditer(r"bad", html)
        if not inside_ignored_rule(config, html, match, rule["name"])
        and not inside_ignored_linter_block(config, html, match)
    ]
```
