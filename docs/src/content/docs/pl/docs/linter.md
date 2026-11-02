---
title: "Reguły lintera"
description: "Reguły lintera szablonów HTML djLint oraz sposób dodawania własnych reguł."
sidebar:
  label: "Linter"
---

djLint zawiera wiele reguł, które sprawdzają styl i poprawność szablonów. Aby w pełni wykorzystać linter, skonfiguruj go tak, by korzystał z gotowego profilu dla wybranego języka szablonów.

```bash
djlint /path/to/templates --lint

# z własnymi rozszerzeniami
djlint /path/to/templates -e html.dj --profile=django

# lub dla pojedynczego pliku
djlint /path/to/this.html.j2  --profile=jinja
```

:::tip
[Wszystkie opcje znajdziesz w przewodniku po konfiguracji!](/pl/docs/configuration/)
:::

## Włączanie i wyłączanie reguł

Większość reguł jest domyślnie włączona. Reguły można wyłączyć w wierszu poleceń flagą `--ignore`, a włączyć flagą `--include`.

Na przykład:

```bash
djlint . --lint --include=H006,H017 --ignore=H013,H015
```

Można to też zrobić w pliku konfiguracyjnym (zobacz [Konfiguracja](/pl/docs/configuration)).

## Reguły

| Kod  | Znaczenie                                                                                       | Domyślnie |
| ---- | ----------------------------------------------------------------------------------------------- | --------- |
| T001 | Zmienne powinny być otoczone białymi znakami. Np.: `{{ this }}`                                 | ✔️        |
| T002 | W tagach należy używać podwójnych cudzysłowów. Np. `{% extends "this.html" %}`                  | ✔️        |
| T003 | Endblock powinien mieć nazwę. Np.: `{% endblock body %}`.                                       | -         |
| D004 | (Django) Statyczne adresy URL powinny mieć postać `{% static path/to/file %}`.                  | ✔️        |
| J004 | (Jinja) Statyczne adresy URL powinny mieć postać `{{ url_for('static'..) }}`.                   | ✔️        |
| H005 | Tag html powinien mieć niepusty atrybut `lang`.                                                 | ✔️        |
| H006 | Tag `img` powinien mieć atrybuty `height` i `width`.                                            | -         |
| H007 | Przed tagiem html powinien się znajdować `<!DOCTYPE ... >`.                                     | ✔️        |
| H008 | Wartości atrybutów powinny być w podwójnych cudzysłowach.                                       | ✔️        |
| H009 | Nazwy tagów powinny być pisane małymi literami.                                                 | ✔️        |
| H010 | Nazwy atrybutów powinny być pisane małymi literami.                                             | ✔️        |
| H011 | Wartości atrybutów powinny być ujęte w cudzysłowy.                                              | ✔️        |
| H012 | Wokół `=` w atrybucie nie powinno być spacji.                                                   | ✔️        |
| H013 | Tag `img` powinien mieć atrybut alt.                                                            | ✔️        |
| H014 | Więcej pustych wierszy, niż zachowuje konfiguracja.                                             | ✔️        |
| H015 | Po tagach `h` wstawiaj podział wiersza.                                                         | ✔️        |
| H016 | Brak tagu `title` w html.                                                                       | ✔️        |
| H017 | Tagi void powinny być samozamykające (konflikt z: H018).                                        | -         |
| D018 | (Django) Linki wewnętrzne powinny używać wzorca `{% url ... %}`.                                | ✔️        |
| H018 | Tagi void są z natury samozamykające i muszą kończyć się na „>”, a nie „/>” (konflikt z: H017). | -         |
| J018 | (Jinja) Linki wewnętrzne powinny używać wzorca `{{ url_for() ... }}`.                           | ✔️        |
| H019 | Zastąp `javascript:abc()` zdarzeniem `on_` i prawdziwym adresem URL.                            | ✔️        |
| H020 | Znaleziono pustą parę tagów. Rozważ jej usunięcie.                                              | ✔️        |
| H021 | Należy unikać stylów inline.                                                                    | ✔️        |
| H022 | Używaj HTTPS w linkach zewnętrznych.                                                            | ✔️        |
| H023 | Nie używaj odwołań do encji.                                                                    | ✔️        |
| H024 | Pomijaj atrybut type w skryptach i stylach.                                                     | ✔️        |
| H025 | Tag wygląda na osierocony.                                                                      | ✔️        |
| H026 | Puste atrybuty id i class można usunąć.                                                         | ✔️        |
| T027 | W składni szablonu znaleziono niezamknięty ciąg znaków.                                         | ✔️        |
| T028 | Rozważ użycie tagów usuwających białe znaki w wartościach atrybutów. `{%- if/for -%}`           | -         |
| H029 | Rozważ zapisywanie wartości atrybutu method formularza małymi literami.                         | ✔️        |
| H030 | Rozważ dodanie opisu meta (meta description).                                                   | ✔️        |
| T032 | W tagach szablonu znaleziono nadmiarowe białe znaki.                                            | ✔️        |
| H033 | W atrybucie action formularza znaleziono nadmiarowe białe znaki.                                | ✔️        |
| T034 | Czy chodziło o {% ... %} zamiast {% ... }%?                                                     | ✔️        |
| H036 | Nie używaj tagów `br` do tworzenia odstępów.                                                    | ✔️        |
| H037 | Znaleziono zduplikowany atrybut.                                                                | ✔️        |
| T038 | Tag blokowy nie ma pasującego tagu końcowego.                                                   | ✔️        |
| T039 | Znaleziono niezamknięty tag szablonu.                                                           | ✔️        |
| T040 | Brak nazwy szablonu lub pusta nazwa w tagu extends lub include.                                 | ✔️        |
| H041 | Tag został zamknięty w innym bloku szablonu niż ten, w którym go otwarto.                       | ✔️        |
| T041 | Tag extends powinien być pierwszym tagiem w szablonie.                                          | ✔️        |
| H042 | Atrybut for etykiety nie ma w tym pliku elementu o pasującym id.                                | ✔️        |
| T042 | Treść poza blokiem nie jest renderowana w szablonie, który rozszerza inny szablon.              | ✔️        |
| H043 | Tag button powinien mieć atrybut `type`.                                                        | ✔️        |
| T043 | Nazwa bloku występuje w szablonie więcej niż raz.                                               | ✔️        |
| H044 | Thead nie powinien mieszać komórek `th` i `td`.                                                 | ✔️        |
| T044 | Tag wyjścia zawiera słowo kluczowe instrukcji; użyj tagu blokowego.                             | ✔️        |
| H045 | Tag iframe powinien mieć atrybut `title`.                                                       | ✔️        |
| T045 | Tag szablonu w komentarzu HTML nadal się wykonuje; aby go wyłączyć, użyj komentarza szablonu.   | ✔️        |
| H046 | Tabindex nie powinien być dodatni.                                                              | ✔️        |
| H047 | Aria-hidden nie powinien być ustawiony na elemencie, który może otrzymać fokus.                 | ✔️        |
| H048 | Atrybut aria nie należy do zdefiniowanych w specyfikacji.                                       | ✔️        |
| H049 | Viewport nie powinien blokować powiększania strony.                                             | ✔️        |
| H050 | Element jest przestarzały i należy go zastąpić.                                                 | ✔️        |
| H051 | Rola nie należy do ról, które ARIA definiuje dla znaczników.                                    | ✔️        |
| H052 | Meta refresh nie powinien przeładowywać strony ani przekierowywać po upływie czasu.             | ✔️        |
| H053 | Id występuje w pliku więcej niż raz.                                                            | ✔️        |
| H054 | Element interaktywny nie powinien być zagnieżdżony w innym.                                     | ✔️        |
| H055 | Atrybut lang powinien zawierać znacznik języka, np. en lub pt-BR.                               | ✔️        |
| H056 | Src nie powinien być pusty.                                                                     | ✔️        |
| H057 | Wideo powinno mieć ścieżkę z napisami.                                                          | ✔️        |

### Wzorce kodów

Pierwsza litera kodu oznacza:

- D: dotyczy wyłącznie Django
- H: dotyczy HTML
- J: dotyczy wyłącznie Jinja
- M: dotyczy wyłącznie Handlebars
- N: dotyczy wyłącznie Nunjucks
- T: dotyczy szablonów ogólnie

### Szczegóły reguł

<!-- oxfmt-ignore-start -->

#### T001

`Variables should be wrapped in a whitespace.`

Składnię szablonu w rodzaju `{{user.name}}` bez wewnętrznych odstępów trudniej przeglądać i porównywać w diffach, a niespójne odstępy w bazie kodu sprawiają, że refaktoryzacje oparte na grepie (wyszukiwanie zmiennej lub tagu) są zawodne, bo to samo wyrażenie występuje w kilku zapisach. Przewodniki stylu zarówno Django, jak i Jinja zapisują `{{ var }}` i `{% tag %}` z pojedynczymi spacjami.

Nie dotyczy profili handlebars i golang.

Źle:

```html
{{user.name}}
```

Dobrze:

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

Mieszanie pojedynczych i podwójnych cudzysłowów w tagach szablonu (`{% extends %}`, `{% include %}`, `{% with %}`, `{% trans %}`, `{% now %}`) sprawia, że ta sama nazwa szablonu występuje w dwóch zapisach, więc wyszukiwanie i masowe zmiany nazw pomijają połowę wystąpień. Ujednolicenie zapisu na podwójne cudzysłowy utrzymuje argumenty tagów w zgodzie z cudzysłowami atrybutów HTML w pozostałej części pliku.

Pojedyncze cudzysłowy wewnątrz wartości atrybutów HTML (np. `<span title="{% trans 'x' %}">`) nie są zgłaszane, ponieważ podwójne cudzysłowy atrybutu wymuszają tam pojedyncze.

Przy `quote_style = "single"` reguła wymaga zamiast tego pojedynczych cudzysłowów, a formater je wstawia.

`--reformat` sam poprawia te cudzysłowy.

Źle:

```html
{% extends 'base.html' %}
```

Dobrze:

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

Gdy `{% block %}` obejmuje wiele wierszy lub bloki są zagnieżdżone, samo `{% endblock %}` nie mówi, który blok zamyka, więc podczas edycji łatwo zakończyć niewłaściwy; szablony potomne nadpisują wtedy niewłaściwą treść. Nazwa w endblock dokumentuje, co z czym tworzy parę, i pozwala zarówno djLint, jak i Django (które zgłasza TemplateSyntaxError przy niezgodnej nazwie w endblock) wychwycić blok zamknięty w złym miejscu. Błędy parowania (niezamknięte bloki, osierocone endblocki i niezgodne nazwy) to kontrole poprawności, którymi zajmuje się T038.

Domyślnie wyłączona; włącz ją za pomocą `--include=T003`. `--name-endblocks` sam wpisuje nazwę.

Nazwa nie jest wymagana, gdy blok otwiera się i zamyka w tym samym wierszu, np. `{% block title %}``{% endblock %}`. Formater przenosi zawartość bloku zawierającego inne tagi do osobnych wierszy, więc blok zapisany w jednym wierszu może po sformatowaniu wymagać nazwy; z `--name-endblocks` formater wpisze także tę nazwę.

Źle:

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

Dobrze:

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Static urls should follow {% static path/to/file %} pattern.`

Wpisywanie ścieżek /static/ na sztywno omija tag `{% static %}` z Django, więc szablony psują się, gdy zmienia się STATIC_URL (np. przy przeniesieniu zasobów do CDN lub wdrożeniu pod podścieżką), i nigdy nie korzystają z nazw plików z hashem z ManifestStaticFilesStorage, co na produkcji powoduje błędy 404 lub nieaktualne zasoby z pamięci podręcznej. Reguła szuka dosłownego prefiksu `/static/`, więc nie obejmuje projektu, który serwuje pliki statyczne z innej ścieżki.

Źle:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Dobrze:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

Wpisywanie ścieżek /static/ na sztywno omija url_for('static', ...) z Flask/Jinja, więc zasoby zwracają 404, gdy aplikacja jest zamontowana pod prefiksem URL albo zmieni się folder lub host plików statycznych, a parametry zapytania unieważniające pamięć podręczną, które dodaje framework, przepadają. Reguła szuka dosłownego prefiksu `/static/`, więc nie obejmuje projektu, który serwuje pliki statyczne z innej ścieżki.

Źle:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Dobrze:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have a non-empty lang attribute.`

Bez atrybutu lang w `<html>` czytniki ekranu zgadują zasady wymowy i mogą czytać stronę w niewłaściwym języku, a przeglądarki nie mogą poprawnie zaproponować tłumaczenia, dzielenia wyrazów ani cudzysłowów właściwych dla języka. Deklaracja języka strony to kryterium sukcesu WCAG 2.1 3.1.1 (poziom A).

`lang=""` i `lang` bez wartości oznaczają, że język jest nieznany, więc są zgłaszane tak samo jak brak atrybutu.

Źle:

```html
<!DOCTYPE html>
<html>
</html>
```

Dobrze:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`Img tag should have height and width attributes.`

Domyślnie wyłączona; włącz ją za pomocą `--include=H006`.

Gdy `<img>` nie ma szerokości i wysokości, przeglądarka nie może zarezerwować miejsca, zanim obraz się pobierze, więc otaczająca treść przeskakuje w miarę ładowania obrazów. To przesunięcie układu pogarsza wskaźnik Cumulative Layout Shift (jedna z metryk Core Web Vitals) i może sprawić, że użytkownik kliknie w niewłaściwe miejsce, zanim strona się ustabilizuje.

Źle:

```html
<img src="cat.png" alt="Cat">
```

Dobrze:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

Bez `<!DOCTYPE>` przed tagiem `<html>` przeglądarki renderują stronę w trybie quirks, emulując dawne zachowanie modelu pudełkowego i układu, więc CSS renderuje się niespójnie w różnych przeglądarkach. Tagi szablonu i komentarze przed doctype są w porządku; tylko sam tag `<html>` musi być nim poprzedzony.

Źle:

```html
<html lang="en">
</html>
```

Dobrze:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Attributes should be double quoted.`

Mieszane style cudzysłowów utrudniają przeglądanie i wyszukiwanie wartości atrybutów, a wartości w pojedynczych cudzysłowach psują się, gdy tylko treść zawiera apostrof. Podwójne cudzysłowy to konwencja stosowana w specyfikacjach HTML, formaterach i większości przewodników stylu, więc ujednolicenie zapisu na nie utrzymuje szablony w zgodzie z szerszym ekosystemem.

Źle:

```html
<div class='content'></div>
```

Dobrze:

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

Parsery HTML akceptują nazwy tagów pisane wielkimi literami, ale serializacje XHTML i XML rozróżniają wielkość liter i je odrzucają, a mieszana wielkość liter sprawia, że wyszukiwanie tekstu i przegląd diffów są zawodne (grep `<h1>` pomija `<H1>`). Nazwy tagów pisane małymi literami zapewniają przenośność i spójność szablonów.

Nie jest zgłaszana przy `--ignore-case`, które każe formaterowi zostawić wielkość liter bez zmian.

Źle:

```html
<H1>Welcome</H1>
```

Dobrze:

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

Nazwy atrybutów pisane wielkimi literami są nieprawidłowe w serializacjach XHTML/XML i uniemożliwiają wyszukiwanie tekstu w szablonach (grep src= pomija SRC=). DOM i tak normalizuje nazwy atrybutów HTML do małych liter, więc zapis wielkimi literami wprowadza niespójność bez żadnej korzyści. Zgłaszane są tylko nazwy, które formater zamienia na małe litery: `class`, `id`, `src`, `width`, `height`, `alt`, `style`, `lang`, `title`, `media` i `srcset`. `--reformat` sam je poprawia, a powiązanie frameworka, takie jak `:itemID`, lub dłuższa nazwa, taka jak `data-ID`, zachowuje swoją wielkość liter.

Nie jest zgłaszana przy `--ignore-case`, które każe formaterowi zostawić wielkość liter bez zmian.

Źle:

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

Dobrze:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

Wartość atrybutu bez cudzysłowów kończy się na pierwszym białym znaku, więc wartość taka jak class=btn primary po cichu gubi wszystko, co następuje po spacji (przeglądarka traktuje „primary” jako osobny atrybut logiczny). Szczególnie podatne są wartości pochodzące ze zmiennych szablonu: każda wyrenderowana spacja, „=” lub „>” psuje tag. Cudzysłowy wyznaczają granice wartości jednoznacznie i bezpiecznie.

Źle:

```html
<div class=test></div>
```

Dobrze:

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

Ze spacjami wokół „=” tag czyta się jak trzy osobne tokeny i wystarczy jedna edycja, by się rozpadł: zawinięcie wiersza lub obcięcie w środku zostawia samotny atrybut logiczny i zbłąkany tekst. Proste narzędzia tekstowe (grep, wyszukiwanie i zamiana) też zakładają ciągły zapis name="value", więc mieszane odstępy utrudniają niezawodne odnajdywanie i refaktoryzację atrybutów. `--reformat` sam usuwa te spacje.

Źle:

```html
<div class = "test"></div>
```

Dobrze:

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

Bez atrybutu alt czytniki ekranu odczytują nazwę pliku obrazu albo nic, co narusza WCAG 1.1.1 (Treść nietekstowa). Tekst alternatywny widzą też użytkownicy, gdy obraz się nie załaduje. Obrazy dekoracyjne powinny mieć jawnie pusty alt="", aby technologie wspomagające wiedziały, że należy je pominąć; to również spełnia tę regułę.

`alt` bez wartości jest równoważny `alt=""`, czyli przypadkowi obrazu dekoracyjnego, więc jest akceptowany.

Źle:

```html
<img src="cat.jpg" height="200" width="300">
```

Dobrze:

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

Ciągi pustych wierszy nie mają wpływu na wyrenderowaną stronę (HTML zwija białe znaki), ale rozdymają szablony i zaśmiecają diffy, gdy zmieniają się sąsiednie wiersze. Formater djLint domyślnie usuwa je całkowicie (zostawiając co najwyżej `max_blank_lines` pustych wierszy, domyślnie 0), więc pozostałe ciągi wskazują na niesformatowany kod.

Źle:

```html
<div>one</div>


<p>two</p>
```

Dobrze:

```html
<div>one</div>

<p>two</p>
```

#### H015

`Follow h tags with a line break.`

Nagłówki to blokowe punkty orientacyjne, które wyznaczają strukturę dokumentu; upchnięcie następnego elementu w tym samym wierszu co zamykający tag h ukrywa tę strukturę w kodzie źródłowym i sprawia, że edycja któregokolwiek z elementów wygląda w diffach jak zmiana obu. Podział wiersza po każdym nagłówku utrzymuje wizualną strukturę szablonu w zgodzie z wyrenderowanym konspektem.

Źle:

```html
<h1>Heading</h1><p>Intro text.</p>
```

Dobrze:

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Missing title tag in html.`

Specyfikacja HTML wymaga elementu title w każdym dokumencie. Bez niego karty przeglądarki, zakładki i historia pokazują surowy URL zamiast nazwy strony, wyszukiwarki tracą główną etykietę strony, a użytkownicy czytników ekranu tracą pierwszą informację odczytywaną po załadowaniu, co narusza WCAG 2.4.2 (Tytuł strony, poziom A).

Działa tylko na plikach zawierających kompletny dokument `<html>`...`</html>`, więc fragmenty szablonów i szablony potomne rozszerzające szablon bazowy nigdy nie są zgłaszane. Powłoki SPA, które ustawiają tytuł po stronie klienta, nadal potrzebują statycznego `<title>`: to on pojawia się przy pierwszym wyrenderowaniu, w robotach indeksujących i wtedy, gdy JavaScript zawiedzie.

Źle:

```html
<html lang="en">
<body>Content</body>
</html>
```

Dobrze:

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

Szablony, które muszą się też parsować jako XML/XHTML (lub zasilają narzędzia oparte na XML), odrzucają elementy void zapisane bez ukośnika zamykającego, a mieszanie `<br>` z `<br />` w bazie kodu daje niespójne diffy. Ta reguła wymusza konwencję w stylu XHTML, aby każdy element void był zamykany tak samo.

Domyślnie wyłączona; włącz ją za pomocą `--include=H017`. Wyklucza się z H018; włącz tylko jedną z tych dwóch konwencji. `--close-void-tags` sam dodaje ukośnik do tagów void HTML. `<path>` w svg pozostaje w zapisanej postaci, więc zamknij go ręcznie.

Źle:

```html
<br>
<meta charset="utf-8">
```

Dobrze:

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Internal links should use the {% url ... %} pattern.`

Wpisane na sztywno wewnętrzne adresy URL po cichu się dezaktualizują, gdy zmienia się ścieżka trasy w urls.py, co daje niedziałające linki i martwe akcje formularzy, których nie wychwyci żaden test URLconf. `{% url %}` wyznacza ścieżkę na podstawie nazwy trasy, więc zmiana ścieżki od razu aktualizuje wszystkie linki.

Źle:

```html
<a href="/accounts/login">Login</a>
```

Dobrze:

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

W HTML Living Standard ukośnik na końcu elementu void nie ma znaczenia (parser go ignoruje), więc zapis `<br />` sugeruje samozamykanie w stylu XML, którego HTML nie ma, i może skłonić czytelników do dodawania ukośników do tagów, które nie są void, a tam zbłąkany / jest po cichu pomijany i maskuje błędy niezamkniętych tagów. Ta reguła wymusza zwykłe zakończenie > w elementach void.

Domyślnie wyłączona; włącz ją za pomocą `--include=H018`. Wyklucza się z H017; włącz tylko jedną z tych dwóch konwencji. SVG `<path />` jest wyłączony z reguły, bo SVG to XML i wymaga ukośnika. Nie jest zgłaszana przy `--close-void-tags`, ponieważ formater wstawia wtedy ukośnik, który ta reguła zgłasza.

Źle:

```html
<br />
<meta charset="utf-8" />
```

Dobrze:

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

Wpisane na sztywno wewnętrzne adresy URL po cichu przestają działać, gdy zmienia się ścieżka trasy lub aplikacja zostaje zamontowana pod prefiksem, co zostawia martwe linki i formularze wysyłające dane pod adresy zwracające 404. url_for() buduje URL z nazwy endpointu, więc zmiany tras automatycznie trafiają do każdego szablonu.

Źle:

```html
<a href="/accounts/login">Login</a>
```

Dobrze:

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

Adresy URL javascript: psują kliknięcie środkowym przyciskiem i otwieranie w nowej karcie, nic nie robią, gdy JavaScript jest wyłączony lub się nie załaduje, są blokowane przez ścisłe Content Security Policy i są klasycznym miejscem wstrzyknięcia XSS. Zamiast tego użyj w href prawdziwego adresu URL i podepnij zachowanie przez procedurę obsługi zdarzenia. Przy ścisłym CSP blokowane są również procedury obsługi on* zapisane inline: pokazany onclick to minimalna poprawka w samym szablonie; lepiej dodać nasłuchiwanie przez addEventListener z pliku skryptu.

Źle:

```html
<a href="javascript:openPopup()">Open popup</a>
```

Dobrze:

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

Pusta para tagów nie renderuje żadnej treści, ale nadal tworzy węzeł DOM, który może przejąć marginesy, obramowania lub odstępy flex/grid z arkuszy stylów, dając trudne do wyśledzenia widmowe odstępy; zwykle jest to pozostałość po wcześniejszej edycji. Tagi, które w zwykłych znacznikach bywają puste z uzasadnionych powodów (td, th, li, dt, dd, slot), są wyłączone z reguły. Nie są też zgłaszane tagi z jakimkolwiek atrybutem (punkty montowania JS, takie jak `<div id="app">``</div>`, elementy fontów z ikonami, takie jak `<i class="fa fa-user">``</i>`); dopasowywane są tylko puste pary całkowicie pozbawione atrybutów.

Źle:

```html
<p>Saved.</p>
<span> </span>
```

Dobrze:

```html
<p>Saved.</p>
```

#### H021

`Inline styles should be avoided.`

Style inline mają wyższą specyficzność niż jakikolwiek selektor arkusza stylów, więc późniejsze ich nadpisanie wymaga !important; są blokowane przez Content Security Policy bez 'unsafe-inline' w style-src; rozpraszają też warstwę prezentacji po szablonach, więc zmiana motywu lub projektu oznacza edycję znaczników zamiast jednego arkusza stylów. Przenieś deklarację do klasy CSS. Jeden uzasadniony wyjątek to szablony e-maili HTML, w których wiele klientów poczty usuwa bloki `<style>`, a style inline to standardowa technika; wyklucz katalogi z szablonami e-maili lub wyłącz dla nich tę regułę.

Źle:

```html
<div style="color: red;">Wrong username or password.</div>
```

Dobrze:

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

Zasoby podrzędne ładowane przez zwykłe http:// na stronie serwowanej przez HTTPS to treść mieszana: przeglądarki od razu blokują skrypty, arkusze stylów i ramki iframe, a w przypadku obrazów automatycznie przełączają je na HTTPS lub ostrzegają. Link `<a>` do strony http:// nie jest treścią mieszaną, ale nadal kieruje odwiedzających przez nieszyfrowane połączenie narażone na podsłuch i manipulację. Odwołania do hostów wewnętrznych, które rzeczywiście nie mają TLS, również zostaną zgłoszone; wycisz te miejsca blokiem `{# djlint:off H022 #}`, zamiast wyłączać regułę.

Źle:

```html
<a href="http://example.com">Example</a>
```

Dobrze:

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

Dokumenty HTML5 są zapisane w UTF-8, więc dosłowny znak działa wszędzie i to go faktycznie czytają recenzenci; przeglądarka nie wychwyci literówki w odwołaniu do encji (np. `&mdsah;`) i wyrenderuje je dosłownie jako zepsuty tekst. djLint dopuszcza encje, które niosą składnię (`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;` oraz nawiasy klamrowe `&lbrace;` i `&rbrace;` razem z `&percnt;`, `&num;` i `&dollar;`, które zapisane dosłownie dopełniłyby ogranicznik szablonu), a także encje oznaczające znaki niewidoczne, których nie da się sprawdzić w postaci dosłownej: spacje (`&nbsp;`, `&thinsp;`, `&hairsp;`), znaki łączące i znaczniki kierunku (`&zwnj;`, `&zwj;`, `&lrm;`, `&rlm;`) oraz `&shy;`, zarówno w postaci nazwanej, jak i dziesiętnej czy szesnastkowej.

`--reformat` sam zamienia encję na znak. Encja zapisana wewnątrz tagu szablonu jest częścią tagu, a nie strony, więc nie ruszają jej ani reguła, ani formater. `--no-entity-formatting` wyłącza zamianę, ale zostawia regułę włączoną, więc encja nadal jest zgłaszana. Aby zachować encje, dodaj `H023` do `ignore`.

Źle:

```html
<p>Dates 1900 &mdash; 2000</p>
```

Dobrze:

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript i text/css to domyślne wartości HTML5 dla `<script>` i `<style>`, więc ten atrybut to zbędny balast, który przeglądarka ignoruje; specyfikacja WHATWG wprost zaleca jego pominięcie. Usunięcie go pozwala też uniknąć przestarzałych typów MIME, które psują element po skopiowaniu do skryptów modułowych (gdzie type="module" rzeczywiście ma znaczenie).

Źle:

```html
<script type="text/javascript" src="app.js">
```

Dobrze:

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

Tag bez pasującego tagu otwierającego lub zamykającego zmusza mechanizm naprawy błędów przeglądarki do zgadywania, gdzie kończy się element, więc kolejne znaczniki zostają wchłonięte przez niewłaściwy element; układ, selektory CSS i zapytania DOM w JavaScripcie psują się wtedy po cichu i w każdej przeglądarce inaczej. H025 zgłasza również `<ol>` lub `<ul>` otwarte wewnątrz `<p>`: parser HTML zamyka akapit przed listą, więc znaczniki nigdy nie zagnieżdżają się tak, jak je zapisano.

Źle:

```html
<div>
  <p>Hello</p>
```

Dobrze:

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Empty id and class tags can be removed.`

Żaden selektor klasy ani id nie pasuje do pustego atrybutu, a pusty id to nieprawidłowy HTML (wartość id nie może być pustym ciągiem znaków). Selektor obecności atrybutu, taki jak `div[class]`, nadal do niego pasuje, więc usunięcie takiego atrybutu będzie widoczne dla arkusza stylów napisanego w ten sposób. Zwykle sygnalizuje to błąd w szablonie, w którym miała zostać wstawiona zmienna, więc usunięcie lub wypełnienie atrybutu nie pozwala temu błędowi ukrywać się na widoku.

Źle:

```html
<div id="" class="">content</div>
```

Dobrze:

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

Cudzysłów otwarty i nigdy niezamknięty wewnątrz `{% ... %}` lub `{{ ... }}` sprawia, że silnik szablonów błędnie parsuje tag: Django i Jinja albo zgłaszają TemplateSyntaxError podczas renderowania, albo po cichu wchłaniają resztę argumentów tagu jako treść ciągu znaków, więc strona zwraca błąd 500 lub renderuje się bez części argumentów.

Źle:

```html
{% trans "Welcome %}
```

Dobrze:

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

Domyślnie wyłączona; włącz ją za pomocą `--include=T028`.

Tag usuwający białe znaki usuwa białe znaki, które się renderują, więc stosuj to tylko tam, gdzie atrybut nie ma czego stracić. `alt="{%- if brand -%}Acme{%- endif -%} logo"` renderuje się jako `Acmelogo`, a w svg `d="M12 {%- if big -%}20{%- endif -%} 4Z"` staje się inną ścieżką. Dlatego regułę trzeba włączyć samodzielnie.

Tagi szablonu wewnątrz wartości atrybutu wstawiają do wyrenderowanego atrybutu otaczające je białe znaki i znaki nowego wiersza, więc href lub src zbudowany za pomocą zwykłych tagów `{% if %}`/`{% for %}` może zawierać zbłąkane spacje i dawać niedziałające adresy URL. Tagi kontroli białych znaków z Jinja/Nunjucks (`{%- ... -%}`) usuwają te otaczające białe znaki, dzięki czemu atrybut renderuje się jako jedna czysta wartość. Atrybut class jest wyłączony z reguły, ponieważ dodatkowe białe znaki między nazwami klas są nieszkodliwe.

Nie dotyczy profilu django: tagi szablonów Django nie obsługują kontroli białych znaków `{%- -%}`.

Źle:

```html
<a href="{% if x %}/home{% endif %}"></a>
```

Dobrze:

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

Specyfikacja HTML definiuje słowa kluczowe metody formularza małymi literami (get, post); przeglądarki akceptują warianty pisane wielkimi literami tylko dzięki dopasowywaniu bez rozróżniania wielkości liter. Trzymanie się kanonicznego zapisu małymi literami zapewnia spójność szablonów, ułatwia wyszukiwanie grepem i pozwala uniknąć zastrzeżeń ze strony ścisłych walidatorów i narzędzi opartych na XHTML.

Źle:

```html
<form method="POST"></form>
```

Dobrze:

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

Wyszukiwarki używają opisu meta jako fragmentu wyświetlanego w wynikach pod tytułem strony; bez niego same składają fragment z przypadkowego tekstu strony, co obniża współczynnik klikalności i daje słabe podglądy linku przy udostępnianiu strony.

Działa tylko na plikach zawierających kompletny dokument `<html>`...`</html>`. Argument dotyczący fragmentu w wynikach wyszukiwania odnosi się do stron indeksowanych publicznie; w aplikacjach wymagających logowania i w aplikacjach intranetowych ta reguła jest często wyłączana.

Źle:

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

Dobrze:

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

Ciągi spacji lub tabulatorów między argumentami tagu szablonu to niewidoczny szum: ukrywają rzeczywiste różnice w diffach, mogą utrudnić zauważenie brakującego argumentu i odbiegają od stylu z pojedynczą spacją, który stosuje formater djLint, co powoduje niepotrzebne zmiany przy formatowaniu. Białe znaki wewnątrz ciągów w cudzysłowach są zachowywane i nie są zgłaszane.

Źle:

```html
{% static  'css/style.css' %}
```

Dobrze:

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

Białe znaki na początku lub na końcu wartości action formularza stają się częścią wyrenderowanego adresu URL. Przeglądarki usuwają je podczas parsowania, ale klienty niebędące przeglądarkami i testy używające dosłownej wartości mogą tego nie robić, a wokół tagu `{% url %}` zbłąkana spacja niemal zawsze oznacza literówkę, przez którą renderuje się adres wysyłki formularza niepasujący do żadnej trasy po stronie serwera.

Źle:

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

Dobrze:

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Did you intend to use {% ... %} instead of {% ... }%?`

}% to niemal zawsze literówka zamiast %}. Silnik szablonów nie rozpoznaje }% jako ogranicznika tagu, więc tag w ogóle nie jest parsowany: surowy tekst {% ... }% wycieka do wyrenderowanego HTML-a albo silnik zgłasza błąd składni, gdy natrafi na niezamknięty tag.

Źle:

```html
{% include "footer.html" }%
```

Dobrze:

```html
{% include "footer.html" %}
```

#### H036

`Do not use br tags for spacing.`

Specyfikacja HTML dopuszcza `<br>` tylko dla podziału wiersza, który jest częścią samej treści, jak w adresie pocztowym czy w poezji, i takie użycie pozostaje bez zgłoszenia. Zgłaszane jest użycie prezentacyjne, które specyfikacja wyklucza: ciąg dwóch lub więcej podziałów, czyli pionowy odstęp, oraz podział przy wewnętrznej krawędzi elementu blokowego, który nie renderuje niczego, czego nie dałby jego własny margines. Jedno i drugie psuje przepływ tekstu przy małych szerokościach, a czytnik ekranu ogłasza wymuszony podział tam, gdzie nie ma nic do ogłoszenia.

Źle:

```html
<p>Shipping is free.<br><br>Delivery takes 3 days.</p>
```

Dobrze:

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

Zduplikowane atrybuty to nieprawidłowy HTML, a przeglądarki zachowują tylko pierwsze wystąpienie i po cichu odrzucają resztę, więc druga wartość class lub style nigdy nie zaczyna działać, co ukrywa prawdziwe błędy. Sprawdzanie uwzględnia składnię szablonów: atrybut powtórzony we wzajemnie wykluczających się gałęziach (`{% if %}`/`{% else %}`) nie jest zgłaszany, ponieważ wyrenderować może się tylko jedna kopia.

Źle:

```html
<div class="card" id="profile" class="active">...</div>
```

Dobrze:

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

Tag blokowy, taki jak `{% if %}`, `{% for %}` czy `{% macro %}`, bez pasującego tagu końcowego to twardy TemplateSyntaxError w Django i Jinja: strona nie renderuje się w chwili obsługi żądania, a ta reguła wychwytuje to przed wdrożeniem. Zgłasza też osierocone tagi końcowe bez tagu otwierającego oraz nieprawidłowo przeplecione bloki (np. `{% if %}``{% for %}``{% endif %}`).

Ta reguła sprawdza parowanie `{% block %}`/`{% endblock %}` i niezgodności nazw w endblock; T003 (domyślnie wyłączona) dodatkowo wymaga nazwy w każdym wielowierszowym `{% endblock %}`. Sprawdzane są też własne tagi blokowe zarejestrowane przez custom_blocks, łącznie z ich samozamykającą formą / %}.

Źle:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

Dobrze:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Unclosed template tag found.`

Tag szablonu otwarty przez `{{` lub `{%`, ale nigdy niezamknięty pasującym `}}` lub `%}`, nie jest parsowany jako tag: Django/Jinja albo zgłaszają TemplateSyntaxError, albo renderują na stronie surowe nawiasy klamrowe, a wszystko aż do następnego ogranicznika może zostać po cichu wchłonięte. Takie literówki (jeden brakujący nawias, niepasujący ogranicznik) łatwo przeoczyć podczas przeglądu kodu, bo szablon może nadal częściowo się renderować.

Źle:

```html
<p>{{ user.name }</p>
```

Dobrze:

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

Tag `{% extends %}` lub `{% include %}` z brakującą, pustą lub złożoną wyłącznie z białych znaków nazwą szablonu nie ma czego wczytać: Django zgłasza TemplateSyntaxError, gdy nazwy w ogóle brak, i TemplateDoesNotExist podczas renderowania, gdy jest pusta, więc strona zwraca na produkcji błąd 500, choć sam plik szablonu wygląda na poprawny składniowo.

Źle:

```html
{% extends "" %}
```

Dobrze:

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

Gdy tag HTML zostaje otwarty w jednym `{% block %}`, a zamknięty w innym, szablon potomny, który nadpisuje tylko jeden z tych bloków, dziedziczy połowę elementu, co daje niezrównoważone znaczniki na wyrenderowanej stronie; przeglądarki automatycznie zamykają wtedy elementy lub nieprzewidywalnie zmieniają ich zagnieżdżenie, psując układ i selektory CSS daleko od szablonu, który faktycznie edytowano. Otwieranie i zamykanie każdego elementu w tym samym bloku sprawia, że każdy blok można bezpiecznie nadpisać niezależnie od innych.

Źle:

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

Dobrze:

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

Django odmawia skompilowania szablonu, w którym przed `{% extends %}` znajduje się inny tag, a tekst zapisany przed nim jest renderowany, więc wycieka na stronę przed wszystkim, co generuje szablon nadrzędny. Jinja również renderuje ten tekst, a nunjucks go odrzuca, więc w każdym silniku szablon nie robi tego, na co wygląda.

Komentarz `{# #}` niczego nie renderuje i się nie liczy; nie liczy się też nic wewnątrz bloku `{% comment %}`, <code>{&#37; raw %}</code> ani `{% verbatim %}`, nazwanego czy nie, obszar `{# djlint:off #}` w dowolnym z trzech zapisów ani front matter w yaml. Komentarz HTML się liczy: silnik zapisuje go na stronie przed doctype szablonu nadrzędnego, a właśnie o taki wyciek chodzi w tej regule. Liczą się również blok `{% blocktrans %}`, blok `{% filter %}` i blok `<?php ?>`, bo każdy z nich coś renderuje. Sprawdzane jest tylko pierwsze `{% extends %}`; drugie jest osobnym błędem. W profilach jinja i nunjucks tag gałęzi przed nim się nie liczy, ponieważ jinja dokumentuje `{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}` jako sposób wyboru szablonu nadrzędnego; django wczytuje resztę szablonu do `{% extends %}`, a potem odrzuca `{% endif %}`, więc w tym profilu tag gałęzi się liczy.

Nie dotyczy profili handlebars, golang, liquid i angular.

Źle:

```html
{% load static %}
{% extends "base.html" %}
```

Dobrze:

```html
{% extends "base.html" %}
{% load static %}
```

#### H042

`Label for attribute has no matching element id in this file.`

Sprawdzanie działa tylko na plikach, które da się rzetelnie przeanalizować: jeśli plik zawiera cokolwiek, co mogłoby wyrenderować id niewidoczne w tym pliku (wyjście `{{ ... }}`, np. widżet formularza, `{% include %}` lub `{% extends %}` albo nierozpoznany tag szablonu), reguła milczy dla tego pliku. Tam, gdzie działa, zgłoszenie oznacza rzeczywiście zerwane powiązanie.

Źle:

```html
<label for="email">Email</label>
<input id="username">
```

Dobrze:

```html
<label for="email">Email</label>
<input id="email">
```

#### T042

`Content outside a block is not rendered in a template that extends another.`

Gdy szablon rozszerza inny, o tym, co trafia na wyjście, decyduje szablon nadrzędny, a potomny jedynie wypełnia jego bloki. Tekst lub HTML zapisany po `{% extends %}` i poza wszystkimi `{% block %}` jest podczas renderowania po cichu odrzucany, więc akapit, który w źródle wygląda dobrze, nigdy nie trafia na stronę.

Tag szablonu w tym miejscu nadal się wykonuje, więc `{% load %}`, `{% set %}` i `{% if %}` otaczający blok pozostają bez zgłoszenia, podobnie jak komentarze `{# #}` i `{% comment %}`, komentarze HTML, bloki <code>{&#37; raw %}</code> i `{% verbatim %}` oraz treść `{% macro %}`, blokowej formy `{% set %}`, `{% partialdef %}` lub `{% addtoblock %}`, która jest przechwytywana, a nie wypisywana. Tekst `{% blocktrans %}` jest zgłaszany, ponieważ `{% blocktrans %}` nie jest `{% block %}`. Brana jest pod uwagę tylko treść po tagu extends, a każdy jej ciągły fragment jest zgłaszany raz, w miejscu, w którym się zaczyna.

Silnik czyta tagi szablonu przed HTML-em, więc `{% extends %}` zapisany wewnątrz komentarza HTML lub `<pre>` nadal się wykonuje i nadal czyni plik szablonem potomnym; naprawdę ukrywają go tylko `{# #}`, `{% comment %}`, <code>{&#37; raw %}</code> i `{% verbatim %}`. Tekst wewnątrz komentarza HTML i tak nie trafia do żadnego czytelnika i nie jest zgłaszany, ale zapisane tam tagi nadal są odczytywane.

Nie dotyczy profili handlebars, golang, liquid i angular.

Źle:

```html
{% extends "base.html" %}
<p>This paragraph is never shown.</p>
{% block content %}
<h1>Welcome</h1>
{% endblock %}
```

Dobrze:

```html
{% extends "base.html" %}
{% block content %}
<h1>Welcome</h1>
<p>This paragraph is shown.</p>
{% endblock %}
```

#### H043

`Button tag should have a type attribute.`

`<button>` bez `type` domyślnie ma typ `submit`, więc przycisk, który miał tylko uruchomić skrypt, wysyła też otaczający go formularz, a strona się przeładowuje. Jawne podanie typu temu zapobiega.

Źle:

```html
<form>
  <button onclick="preview()">Preview</button>
</form>
```

Dobrze:

```html
<form>
  <button type="button" onclick="preview()">Preview</button>
</form>
```

#### T043

`Block name is used more than once in the template.`

Django, Jinja i Nunjucks odmawiają sparsowania szablonu, w którym dwa bloki mają tę samą nazwę, więc strona w ogóle się nie wczytuje. Silnikom jest obojętne, że oba bloki znajdują się w różnych gałęziach `{% if %}`, więc każda nazwa bloku musi być unikalna w całym szablonie, niezależnie od tego, czy bloki stoją obok siebie, czy jeden jest zagnieżdżony w drugim.

Liczy się tylko `{% block %}`: `{% blocktrans %}` nie jest blokiem, a `{% endblock name %}` jedynie nazywa blok, który zamyka. Nazwy są porównywane dokładnie w zapisanej postaci, ponieważ silniki traktują `Content` i `content` jako dwa bloki.

Pomijane jest tylko to, czego sam silnik nigdy nie parsuje: komentarz szablonu, blok `{% comment %}`, treść <code>{&#37; raw %}</code> lub `{% verbatim %}` oraz obszar `djlint:off`. Blok zapisany wewnątrz komentarza HTML, w treści `<script>`, `<style>`, `<pre>` lub `<textarea>` albo w treści `{% filter %}` nadal jest liczony, ponieważ silnik czyta to wszystko i tak samo zgłasza błąd zduplikowanej nazwy.

`{% embed %}` otwiera własny zakres: bloki w nim wypełniają osadzany szablon, a nie bieżący, więc dwa osadzenia tego samego fragmentu szablonu mogą każde zawierać `{% block body %}`. Nazwa powtórzona w obrębie jednego osadzenia nadal jest zgłaszana.

Nie dotyczy profili handlebars, golang, liquid i angular.

Źle:

```html
{% block content %}{% endblock %}
{% block content %}{% endblock %}
```

Dobrze:

```html
{% block content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

#### H044

`Thead should not mix th and td cells.`

Każdy wiersz jest oceniany osobno, więc wiersz objaśnień z komórkami `td`, który specyfikacja HTML umieszcza w `thead` obok wiersza nagłówków, nie jest mieszanką. Pusta komórka `td` otwierająca wiersz to komórka narożna tabeli z nagłówkami w pierwszej kolumnie, czyli znaczniki, których wymaga samouczek dostępności W3C, więc jest pomijana.

`th` i `td` niosą dla czytnika ekranu różne znaczenie i zwykle mają różny CSS, więc jedna zbłąkana komórka w wierszu nagłówka jest odczytywana jako dane i wygląda inaczej niż sąsiednie kolumny. Takie pomieszanie to poprawny HTML i właśnie dlatego trudno je zauważyć.

Źle:

```html
<thead>
  <tr>
    <th>Name</th>
    <td>Size</td>
  </tr>
</thead>
```

Dobrze:

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

Nie dotyczy profili golang, handlebars i angular.

Tag wyjścia wypisuje wartość, a `if`, `for`, `url`, `include` i pozostałe to instrukcje, których miejsce jest w tagu blokowym. Django, Jinja i Nunjucks odrzucają `{{ if x }}` z błędem składni, a samo słowo zamykające, takie jak `{{ endif }}`, jest odczytywane jako zmienna, która niczego nie renderuje, podczas gdy blok, który miało zamknąć, pozostaje otwarty, więc strona albo się nie wczytuje, albo pokazuje to, co warunek powinien był ukryć.

Samo słowo kluczowe jest zwykłą nazwą zmiennej, więc `{{ url }}`, `{{ url|default:"/" }}` i `{{ set.name }}` nie są zgłaszane. Zgłaszane jest tylko słowo kluczowe z argumentem, a także samo słowo zamykające lub słowo gałęzi, takie jak `{{ endif }}` lub `{{ else }}`. Słowo kluczowe sterujące, takie jak `if` czy `for`, nie może rozpoczynać wyrażenia, więc wszystko, co po nim następuje, jest argumentem, łącznie z operatorem, i `{{ if -1 > count }}` jest zgłaszane. Pozostałe nazwy służą też jako zmienne i funkcje i w ich przypadku za argument uznaje się tylko ciąg znaków w cudzysłowach lub słowo, więc wyrażenie, które akurat zaczyna się od jednej z nich, pozostaje bez zgłoszenia: `{{ url ~ "/x" }}`, `{{ url if url else "#" }}`, `{{ url ? url : '#' }}`, `{{ block ('title') }}`, `{{ block .super }}` i `{{ filter [0] }}` nie są zgłaszane.

Treść bloku <code>{&#37; raw %}</code> lub `{% verbatim %}` jest tekstem, a nie składnią szablonu, i jest pomijana, łącznie z nazwaną formą `{% verbatim vueapp %}...{% endverbatim vueapp %}`, więc chronione w ten sposób `{{ }}` z Vue lub Handlebars nie jest zgłaszane. `{{ }}` zapisane w argumencie tagu blokowego w cudzysłowach, jak w `{% trans "Write {{ if x }} instead" %}`, to tekst, który silnik wypisuje, więc również pozostaje bez zgłoszenia.

Źle:

```html
{{ if user.is_active }}
```

Dobrze:

```html
{% if user.is_active %}
```

#### H045

`Iframe tag should have a title attribute.`

Czytnik ekranu ogłasza ramkę iframe za pomocą jej nazwy dostępnej (accessible name). Bez niej odczytuje adres URL ramki albo nic i nie da się dowiedzieć, czym jest osadzona strona, zanim się do niej wejdzie. WCAG ujmuje to w kryterium 4.1.2 Nazwa, rola, wartość, a axe i html-validate domyślnie zawierają to sprawdzenie.

Nazwa może pochodzić z `title`, `aria-label` lub `aria-labelledby` i każdy z tych trzech atrybutów spełnia regułę. Nazwa zapisana przez tag szablonu też się liczy, więc ramka z tytułem ustalanym dla każdej strony nie jest zgłaszana.

Źle:

```html
<iframe src="/report/"></iframe>
```

Dobrze:

```html
<iframe src="/report/" title="Quarterly report"></iframe>
```

#### T045

`Template tag inside an html comment still runs; use a template comment to disable it.`

Komentarz HTML ukrywa znaczniki przed przeglądarką, ale nie przed silnikiem szablonów. `<!-- {% include "debug.html" %} -->` nadal renderuje plik, a `<!-- {% if debug %}...{% endif %} -->` nadal jest obliczane, tak samo w Django, Jinja, Nunjucks, Handlebars i Go, więc tag zakomentowany w ten sposób nadal się wykonuje, a to, co zapisuje, trafia do komentarza albo, jeśli zawiera `-->`, wydostaje się z niego. Wykonanie tagu powstrzymuje tylko komentarz szablonu: `{# #}` w Django i Jinja, `{{! }}` w Handlebars lub `{{/* */}}` w Go.

Zgłaszany jest tylko tag instrukcji: `{% %}` w profilach, które go mają, sekcja, tag zamykający lub partial w handlebars oraz słowo kluczowe Go, takie jak `{{if}}` lub `{{end}}`. Wartość wypisana w komentarzu, jak w `<!-- built {{ version }} -->`, to celowe użycie i pozostaje bez zgłoszenia, podobnie jak tag wewnątrz komentarza szablonu, bloku `{% comment %}` lub bloku raw oraz komentarz warunkowy dla Internet Explorera, `<!--[if IE]> ... <![endif]-->`, którego treść to znaczniki dla wskazanej w nim przeglądarki.

Samo słowo kluczowe Go jest zwykłą nazwą zmiennej w każdym innym silniku, więc `<!-- period {{ start }} to {{ end }} -->` i `<!-- Template: {{ template }} -->` to wartości w Django, Jinja, Nunjucks, Handlebars i Liquid, a jako instrukcje są odczytywane tylko przy `--profile golang`. Słowo z operandem Go, jak w `{{ if .X }}` i `{{ template "footer" . }}`, to instrukcja, której żaden inny silnik nie wypisuje, więc jest zgłaszane w każdym profilu. `{%` jest podobnie odczytywane tylko tam, gdzie silnik je obsługuje, więc przy `--profile handlebars` i `--profile golang` jest tekstem, a otwarcie, po którym nie następuje nawias zamykający, jak w `<!-- battery at 50{% charge -->`, jest zwykłym tekstem, na jaki wygląda. Komentarz warunkowy to komentarz zapisany jako taki: otwierający się od `<!--[if` i zamknięty przez `<![endif]-->` w dowolnej wielkości liter; niezamknięty jest zwykłym komentarzem, za jaki uznaje go przeglądarka, a tagi w nim są zgłaszane.

Źle:

```html
<!-- {% include "banner.html" %} -->
```

Dobrze:

```html
{# {% include "banner.html" %} #}
```

#### H046

`Tabindex should not be positive.`

Dodatni `tabindex` przesuwa element na początek kolejności tabulacji, przed wszystko, co go nie ma. Jeden taki element zmienia kolejność na całej stronie dla użytkownika klawiatury, a kolejność trzeba potem ręcznie utrzymywać w każdym szablonie, który dodaje kontrolkę. WCAG obejmuje to kryterium 2.4.3 Kolejność fokusu.

`0` umieszcza element w kolejności tabulacji w miejscu wynikającym z dokumentu, a `-1` usuwa go z niej, zostawiając możliwość ustawienia na nim fokusu ze skryptu. Żadna z tych wartości nie jest zgłaszana, podobnie jak wartość zapisana przez tag szablonu, której liczby nie da się tu poznać.

Źle:

```html
<input tabindex="1">
```

Dobrze:

```html
<input tabindex="0">
```

#### H047

`Aria-hidden should not be set on a focusable element.`

`aria-hidden="true"` usuwa element z drzewa dostępności, ale zostawia go w kolejności tabulacji, więc użytkownik klawiatury nadal na niego trafia i nie słyszy żadnego komunikatu. Ukrycie dekoracyjnej ikony to zwykłe zastosowanie tego atrybutu i nie jest zgłaszane; zgłaszany jest tylko element, który sam może otrzymać fokus.

Element uznaje się za fokusowalny, jeśli jest to `button`, `select`, `textarea`, `iframe` lub `summary`, `a` lub `area` z `href`, `input` inny niż ukryty, `audio` lub `video` z `controls` albo cokolwiek z `contenteditable` lub z `tabindex` równym `0` lub większym. Kontrolka z `disabled` lub z `tabindex="-1"` jest już poza kolejnością tabulacji i pozostaje bez zgłoszenia.

Źle:

```html
<button aria-hidden="true">Close</button>
```

Dobrze:

```html
<button type="button" aria-label="Close"><span aria-hidden="true">x</span></button>
```

#### H048

`Aria attribute is not one the specification defines.`

Atrybut aria z literówką nie robi zupełnie nic. Żadna przeglądarka nie ostrzega, żaden czytnik ekranu tego nie zgłasza, a znaczniki sprawiają wrażenie dostępnych, więc `aria-lable` może latami tkwić w szablonie, podczas gdy kontrolka, której miał nadać nazwę, pozostaje bez nazwy.

Reguła zna nazwy zdefiniowane przez ARIA. Powiązanie zapisane przez framework nie jest zwykłą nazwą aria, więc `:aria-label`, `v-bind:aria-label` i `[attr.aria-label]` pozostają bez zgłoszenia.

Źle:

```html
<button type="button" aria-lable="Close">x</button>
```

Dobrze:

```html
<button type="button" aria-label="Close">x</button>
```

#### H049

`Viewport should not stop the page being zoomed.`

`user-scalable=no` oraz `maximum-scale` poniżej 2 uniemożliwiają powiększenie strony na telefonie, co dla wielu osób jest jedynym sposobem, by ją przeczytać. WCAG wymaga 200% w kryterium 1.4.4 Zmiana rozmiaru tekstu. Przeglądarki coraz częściej ignorują to ograniczenie, ale tag nadal wyłącza powiększanie wszędzie tam, gdzie jest respektowany.

Nazwa i treść są wykrywane niezależnie od kolejności, w jakiej je zapisano.

Źle:

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

Dobrze:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### H050

`Element is obsolete and should be replaced.`

`<center>`, `<font>`, `<big>`, `<strike>` i `<tt>` wycofano, gdy prezentację przejął CSS, a `<marquee>`, `<blink>`, `<nobr>` i `<spacer>` nigdy nie były standardem. HTML nie definiuje już żadnego z nich, więc nic nie gwarantuje, jak przeglądarka je rozmieści, a arkusz stylów nie może się do nich odwoływać tak, jak do klasy.

Reguła zna elementy `acronym`, `applet`, `basefont`, `bgsound`, `big`, `blink`, `center`, `dir`, `font`, `frame`, `frameset`, `isindex`, `keygen`, `marquee`, `menuitem`, `nobr`, `noembed`, `noframes`, `plaintext`, `spacer`, `strike`, `tt` i `xmp`. Zgłaszany jest tylko tag otwierający, więc każdy element jest wymieniany raz, a własny element, którego nazwa jedynie zaczyna się od jednej z nich, np. `<font-picker>`, pozostaje bez zgłoszenia.

Źle:

```html
<center><font color="red">Warning</font></center>
```

Dobrze:

```html
<p class="warning">Warning</p>
```

#### H051

`Role is not one ARIA defines for markup.`

Rola, której nie wymienia żadna specyfikacja, jest po prostu odrzucana, a element zachowuje dotychczasowe znaczenie, więc `role="buton"` pozostawia `<div>` zwykłym `<div>`: dla czytnika ekranu nic nie znaczy, choć znaczniki wyglądają, jakby nadano mu jakieś przeznaczenie. Nic o tym nie ostrzega i właśnie dlatego warto wyłapywać taką literówkę.

Reguła zna role, które ARIA definiuje dla autorów, wraz z rolami dodawanymi przez DPUB-ARIA (`doc-chapter` i pozostałe) oraz GRAPHICS-ARIA (`graphics-symbol` i pozostałe). Abstrakcyjne role ARIA, takie jak `landmark` i `sectionhead`, są zgłaszane: specyfikacja mówi, że służą do budowy jej ontologii i nie wolno ich zapisywać w znacznikach.

`role` może zawierać kilka nazw jako listę zastępczą i każda z nich jest sprawdzana. Wartości zawierającej składnię szablonu nie da się ustalić, więc pozostaje bez zgłoszenia, podobnie jak powiązanie zapisane przez framework, jak w `:role` lub `[attr.role]`.

Źle:

```html
<div role="buton">Save</div>
```

Dobrze:

```html
<button type="button">Save</button>
```

#### H052

`Meta refresh should not reload or redirect the page on a timer.`

Odświeżenie po upływie czasu podmienia stronę w trakcie czytania. Ktoś, kto czyta powoli, korzysta z czytnika ekranu albo po prostu mu przerwano, traci miejsce, w którym był, bez ostrzeżenia i bez możliwości zatrzymania odświeżenia, co narusza WCAG 2.2.1 Dostosowanie czasu, a odświeżenie, które przeładowuje tę samą stronę, wyrzuca wszystko, co w niej wpisano.

Opóźnienie równe zero to natychmiastowe przekierowanie, a nie odliczanie czasu, i WCAG zezwala na nie tam, gdzie nie można użyć przekierowania po stronie serwera, więc nie jest zgłaszane. Oba atrybuty są wykrywane niezależnie od kolejności, w jakiej je zapisano.

Źle:

```html
<meta http-equiv="refresh" content="30">
```

Dobrze:

```html
<meta http-equiv="refresh" content="0; url=/next-page">
```

#### H053

`Id is used more than once in the file.`

Id nazywa jeden element. Drugi element z tym samym id psuje `getElementById`, `<label for>`, linki do fragmentów i `aria-labelledby`: przeglądarka bierze pierwszy, a resztę po cichu ignoruje, więc etykieta, link lub skrypt trafia w niewłaściwy element bez żadnego ostrzeżenia.

Dwa id w wykluczających się gałęziach jednego `{% if %}...{% else %}...{% endif %}` nigdy nie są renderowane jednocześnie, więc nie są zgłaszane. Pętla `{% for %}` ani `{% block %}` nie są gałęzią: id wewnątrz nich i to samo id na zewnątrz są renderowane oba, a późniejsze jest zgłaszane. Wartości zapisanej przez tag szablonu nie da się ustalić, więc pozostaje bez zgłoszenia, podobnie jak wartość pusta. Id są porównywane dokładnie, tak jak robi to przeglądarka, więc `save` i `Save` to dwa różne id.

Gałęzie są odczytywane w języku, w którym napisano plik, z dowolnymi białymi znakami, jakie ten język dopuszcza między ogranicznikami a nazwą tagu: `{% elif %}` i `{% else %}`, `{% elsif %}` i `{% when %}` z liquid, `{{ else }}` z go, instrukcja wierszowa `% else:` z mako oraz `{{else}}` z handlebars, jego łańcuchowe `{{else if x}}` i sekcja odwrócona dowolnego bloku `{{#helper}}`, łącznie z własnymi helperami. Zawartość `<template>` to osobny fragment dokumentu, do którego `getElementById` nigdy nie sięga, więc id w nim jest porównywane tylko z id z tego samego `<template>`: dwa elementy template mogą każdy zawierać wiersz z tym samym id, a dwa takie id w jednym elemencie template nadal są zgłaszane. Id wewnątrz komentarza, treści <code>{&#37; raw %}</code> lub `{% verbatim %}` albo obszaru `djlint:off` w ogóle nie jest odczytywane.

Źle:

```html
<button type="submit" id="submit">Save</button>
<button type="submit" id="submit">Save and continue</button>
```

Dobrze:

```html
<button type="submit" id="submit">Save</button>
<button type="button" id="cancel">Cancel</button>
```

#### H054

`Interactive element should not be nested inside another.`

HTML zabrania umieszczania treści interaktywnej wewnątrz `<a>` i `<button>`. Przycisk w linku albo link w przycisku to nieprawidłowe znaczniki, które każda przeglądarka naprawia po swojemu, a użytkownik czytnika ekranu lub klawiatury dostaje jedną kontrolkę, która zachowuje się jak dwie. axe zgłasza to samo jako „nested-interactive”.

Obserwowanymi kontenerami są `<a>` z `href` oraz `<button>`, a kontrolkami zgłaszanymi wewnątrz nich są link z `href`, `button`, `input`, `select` i `textarea`. `<a>` bez `href` nie jest interaktywny i pozostaje bez zgłoszenia po obu stronach, podobnie jak ukryty input lub taki, którego typ zapisuje tag szablonu. Zawartość `<template>` nie jest renderowana tam, gdzie ją zapisano, więc kontrolka w niej nie jest zagnieżdżona w otaczającym linku, choć zagnieżdżenie zapisane wewnątrz samego elementu template nadal jest zgłaszane.

Atrybut jest odczytywany tam, gdzie tag go zapisuje, i nigdzie indziej: `href` w `{% if not href %}` to nazwa zmiennej, ten w `{# href="{{ url }}" #}` jest zakomentowany, a ten w `data-attr=href` należy do innego atrybutu, natomiast `href`, który `{% if %}` zapisuje między swoimi tagami, jest atrybutem jak każdy inny. Link lub przycisk pozostawiony otwarty kończy się wraz z otaczającym go elementem, tak jak w przeglądarce, więc jedna literówka nie powoduje zgłoszeń w całej reszcie pliku; pozostawiony otwarty na najwyższym poziomie nie ma wokół siebie niczego, co by go zakończyło, więc ciągnie się do końca pliku, gdzie H025 dodatkowo zgłasza osierocony tag.

Źle:

```html
<a href="/cart"><button>Add</button></a>
```

Dobrze:

```html
<a href="/cart" class="button">Add</a>
```

#### H055

`Lang attribute should be a language tag such as en or pt-BR.`

H005 wymaga atrybutu `lang` w `<html>`, ale wartość taka jak `lang="english"` lub `lang="en_US"` spełnia tę regułę, nie wskazując żadnego języka znanego przeglądarce. Czytnik ekranu wraca wtedy do domyślnego głosu, a tłumaczenie i dzielenie wyrazów stosują niewłaściwe reguły albo żadnych. Wartość musi być znacznikiem BCP 47: dwie lub trzy litery, a po nich dowolna liczba podznaczników złożonych z od jednej do ośmiu liter lub cyfr, każdy poprzedzony łącznikiem, jak w `en`, `pt-BR` lub `zh-Hant-TW`.

Sprawdzany jest tylko tag `<html>`, tak jak w H005. Pustą wartość obsługuje tamta reguła, natomiast wartość złożona wyłącznie z białych znaków jest zgłaszana tutaj, ponieważ H005 traktuje ją jako wartość. Wartości zapisanej przez tag szablonu, jak w `lang="{{ LANGUAGE_CODE }}"`, lub przez krótkie echo PHP, jak w `lang="<?= $lang ?>"`, nie da się ustalić, więc pozostaje bez zgłoszenia, ale wartość, która jedynie zaczyna się od `$` lub `{`, jak w `lang="$LANG"`, jest odczytywana dosłownie. `xml:lang` ani `data-lang` nie są odczytywane jako `lang`, a `>` zapisany wewnątrz tagu szablonu przed atrybutem, jak w `{% if a > b %}`, go nie ukrywa.

Źle:

```html
<html lang="english">
```

Dobrze:

```html
<html lang="en">
```

#### H056

`Src should not be empty.`

Specyfikacja HTML mówi, że pusty `src` jest nieprawidłowy, i ostrzega, że przeglądarka interpretuje go względem adresu URL samego dokumentu, więc `<img src="">` ponownie pobiera stronę jako obraz, a `<script src=""></script>` pobiera ją jako skrypt. Zwykle jest to symbol zastępczy, który miał wypełnić skrypt, a rozwiązaniem jest usunięcie atrybutu albo przechowanie wartości w atrybucie data, dopóki nie pojawi się prawdziwa. `src` zapisany w ogóle bez wartości, jak w `<img src>`, również jest pusty i jest zgłaszany.

Sprawdzane są tylko `img`, `script`, `iframe`, `embed`, `source`, `track`, `audio` i `video`, ponieważ to te elementy pobierają to, co wskazuje `src`. Zgłaszana jest tylko wartość, którą przeglądarka odczytuje jako pustą, więc wartość bez cudzysłowów, taka jak `<img src=/static/logo.png>`, pozostaje bez zgłoszenia, podobnie jak wartość złożona wyłącznie z białych znaków i wartość zapisana przez tag szablonu, a `srcset` i `data-src` to inne atrybuty, których reguła nie ocenia.

Źle:

```html
<img src="" alt="Logo">
```

Dobrze:

```html
<img src="{% static 'logo.png' %}" alt="Logo">
```

#### H057

`Video should have a captions track.`

Wideo z dźwiękiem przekazuje mowę wyłącznie w ścieżce dźwiękowej, więc osoba głucha lub niedosłysząca nie otrzymuje z niego nic bez napisów, których wymaga WCAG 1.2.2 Napisy rozszerzone (nagranie). Regułę spełnia `<track>` z `kind` równym `captions` lub `subtitles` wewnątrz `<video>`, a także `<track>` w ogóle bez `kind`, ponieważ `subtitles` jest wartością domyślną.

Wideo z atrybutem `muted` nie ma dźwięku, który wymagałby napisów, i nie jest zgłaszane. Nie jest też zgłaszane wideo, którego tag otwierający lub treść zawiera tag szablonu, ponieważ ścieżki lub atrybut `muted` mogą być zapisywane przez szablon tam, gdzie djLint ich nie widzi. Tag szablonu oznacza tu tag otwierany przez język szablonów: `{{`, `{%`, `{#` lub `${`, więc procedura obsługi z jQuery, taka jak `onclick="$(this).play()"`, `$refs` z Alpine, nawias klamrowy z CSS i cena zapisana w tekście zastępczym są zwykłym tekstem, na jaki wyglądają, a wideo nadal jest odczytywane.

`muted` musi być atrybutem, więc `<video class=muted>` to klasa o nazwie muted i jest zgłaszane, a zakomentowany `<track>` lub zapisany wewnątrz wartości atrybutu jest tekstem, a nie ścieżką. `</video>` wewnątrz wartości niczego nie kończy, a element jest oceniany tam, gdzie zamyka go jego prawdziwy tag końcowy, więc pozostawiony otwarty `<video>` obsługuje reguła `H025`.

Źle:

```html
<video controls src="talk.mp4"></video>
```

Dobrze:

```html
<video controls src="talk.mp4">
  <track kind="captions" src="talk.vtt" srclang="en">
</video>
```

<!-- oxfmt-ignore-end -->

### Dodawanie reguł

Chętnie przyjmujemy pull requesty z nowymi regułami!

Dobra reguła składa się z następujących elementów:

- Nazwa
- Kod
- Komunikat: komunikat wyświetlany po znalezieniu błędu.
- Flagi: flagi wyrażeń regularnych, na przykład re.I|re.M. Domyślnie re.DOTALL.
- Wzorce: wyrażenia regularne, które znajdują błąd.
- Wykluczenia: opcjonalna lista profili, do których reguła się nie stosuje.

Dołącz test, który sprawdza regułę.

## Własne reguły

Możesz dodać własne reguły tylko dla swojego projektu, tworząc plik `.djlint_rules.yaml` obok `pyproject.toml`. Reguły dodane do tego pliku zostaną wczytane przez djLint. Plik reguł w innej lokalizacji można wskazać opcją wiersza poleceń `--rules`.

### Reguły oparte na wzorcach

Możesz dodawać reguły, które zgłaszają błąd, gdy któryś ze wzorców wyrażeń regularnych zostanie dopasowany:

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Reguły w modułach Pythona

Możesz dodawać reguły, które importują i wykonują własną funkcję w Pythonie:

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

Wskazany `python_module` musi zawierać funkcję `run()`, która zostanie wykonana dla każdego sprawdzanego pliku. Musi ona przyjmować następujące argumenty:

- `rule`: słownik reprezentujący regułę w `.djlint_rules.yaml`. Zwykle używa się tej zmiennej, aby odczytać nazwę i komunikat reguły.
- `config`: obiekt konfiguracji DJLint.
- `html`: pełna treść HTML pliku.
- `filepath`: ścieżka do aktualnie sprawdzanego pliku.
- `line_ends`: lista pozycji znaków `start` i `end` wierszy, której możesz użyć z `djlint.lint.get_line()`, aby uzyskać numery wierszy na podstawie pozycji znaku. Zobacz przykład.
- `*args, **kwargs`: w przyszłości możemy dodać inne argumenty, więc warto uwzględnić te dwa, aby zmniejszyć ryzyko awarii po aktualizacji djLint.

Moduł może znajdować się w katalogu głównym projektu. Jeśli zwróci `line` lub `end`, które nie są pozycją, djLint zatrzyma się z błędem podającym nazwę reguły.

Funkcja musi zwracać listę słowników, po jednym dla każdego błędu, z następującymi kluczami:

- `code`: kod reguły, która zgłasza błąd (zwykle `rule['name']`)
- `line`: numer wiersza i numer znaku w tym wierszu, oddzielone znakiem „:”, w postaci ciągu znaków.
  Na przykład `"2:3"` oznacza, że błąd znaleziono w wierszu 2, w znaku 3
- `end`: opcjonalny. Miejsce, w którym kończy się błąd, zapisane tak jak `line`, tuż za jego ostatnim znakiem. Bez niego błąd kończy się tam, gdzie `match`.
- `match`: fragment treści zawierający błąd
- `message`: komunikat, który zostanie wypisany, aby zasygnalizować błąd (zwykle `rule['message']`)

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
