---
title: "Pravidla linteru"
description: "Linter HTML šablon djLint obsahuje přes 30 pravidel! Najdete tu jejich popis. Snadno je rozšíříte o vlastní pravidla!"
sidebar:
  label: "Linter"
---

djLint obsahuje mnoho pravidel, která kontrolují styl a platnost vašich šablon. Linter naplno využijete, když ho nastavíte na připravený profil pro šablonovací jazyk, který používáte.

```bash
djlint /path/to/templates --lint

# s vlastními příponami
djlint /path/to/templates -e html.dj --profile=django

# nebo pro soubor
djlint /path/to/this.html.j2  --profile=jinja
```

:::tip
[Všechny možnosti najdete v průvodci konfigurací!](/cs/docs/configuration/)
:::

## Zapnutí a vypnutí pravidel

Většina pravidel je ve výchozím nastavení zapnutá. Na příkazovém řádku lze pravidla vypnout přepínačem `--ignore` a zapnout přepínačem `--include`.

Například:

```bash
djlint . --lint --include=H006,H017 --ignore=H013,H015
```

Totéž lze nastavit i v konfiguračním souboru (viz [Konfigurace](/cs/docs/configuration)).

## Pravidla

| Kód  | Význam                                                                                                 | Výchozí |
| ---- | ------------------------------------------------------------------------------------------------------ | ------- |
| T001 | Proměnné by měly být obalené prázdnými znaky. Např.: `{{ this }}`                                      | ✔️      |
| T002 | Ve značkách by se měly používat dvojité uvozovky. Např. `{% extends "this.html" %}`                    | ✔️      |
| T003 | Endblock by měl mít název. Např.: `{% endblock body %}`.                                               | -       |
| D004 | (Django) Statické URL by měly mít tvar `{% static path/to/file %}`.                                    | ✔️      |
| J004 | (Jinja) Statické URL by měly mít tvar `{{ url_for('static'..) }}`.                                     | ✔️      |
| H005 | Značka html by měla mít neprázdný atribut `lang`.                                                      | ✔️      |
| H006 | Značka `img` by měla mít atributy `height` a `width`.                                                  | -       |
| H007 | Před značkou html by měl být uveden `<!DOCTYPE ... >`.                                                 | ✔️      |
| H008 | Atributy by měly být ve dvojitých uvozovkách.                                                          | ✔️      |
| H009 | Názvy značek by měly být malými písmeny.                                                               | ✔️      |
| H010 | Názvy atributů by měly být malými písmeny.                                                             | ✔️      |
| H011 | Hodnoty atributů by měly být v uvozovkách.                                                             | ✔️      |
| H012 | Kolem `=` u atributu by neměly být mezery.                                                             | ✔️      |
| H013 | Značka `img` by měla mít atribut alt.                                                                  | ✔️      |
| H014 | Více prázdných řádků, než kolik konfigurace ponechává.                                                 | ✔️      |
| H015 | Za značkami `h` zalamujte řádek.                                                                       | ✔️      |
| H016 | V html chybí značka `title`.                                                                           | ✔️      |
| H017 | Nepárové značky by měly být samouzavírací (v konfliktu s: H018).                                       | -       |
| D018 | (Django) Interní odkazy by měly používat tvar `{% url ... %}`.                                         | ✔️      |
| H018 | Nepárové značky jsou ze své podstaty samouzavírací a musí končit „>“, ne „/>“ (v konfliktu s: H017).   | -       |
| J018 | (Jinja) Interní odkazy by měly používat tvar `{{ url_for() ... }}`.                                    | ✔️      |
| H019 | Nahraďte `javascript:abc()` událostí `on_` a skutečnou URL.                                            | ✔️      |
| H020 | Nalezen prázdný pár značek. Zvažte jeho odstranění.                                                    | ✔️      |
| H021 | Vyhněte se inline stylům.                                                                              | ✔️      |
| H022 | Pro externí odkazy používejte HTTPS.                                                                   | ✔️      |
| H023 | Nepoužívejte znakové entity.                                                                           | ✔️      |
| H024 | U skriptů a stylů vynechte type.                                                                       | ✔️      |
| H025 | Značka se zdá být osiřelá.                                                                             | ✔️      |
| H026 | Prázdné značky id a class lze odstranit.                                                               | ✔️      |
| T027 | V šablonové syntaxi nalezen neuzavřený řetězec.                                                        | ✔️      |
| T028 | Zvažte použití značek bez mezer uvnitř hodnot atributů. `{%- if/for -%}`                               | -       |
| H029 | Zvažte hodnoty method formuláře malými písmeny.                                                        | ✔️      |
| H030 | Zvažte přidání meta description.                                                                       | ✔️      |
| T032 | V šablonových značkách nalezeny nadbytečné prázdné znaky.                                              | ✔️      |
| H033 | V action formuláře nalezeny nadbytečné prázdné znaky.                                                  | ✔️      |
| T034 | Chtěli jste použít {% ... %} místo {% ... }%?                                                          | ✔️      |
| H036 | Nepoužívejte značky `br` k vytváření mezer.                                                            | ✔️      |
| H037 | Nalezen duplicitní atribut.                                                                            | ✔️      |
| T038 | Bloková značka nemá odpovídající koncovou značku.                                                      | ✔️      |
| T039 | Nalezena neuzavřená šablonová značka.                                                                  | ✔️      |
| T040 | Ve značce extends nebo include chybí název šablony nebo je prázdný.                                    | ✔️      |
| H041 | Značka je uzavřena v jiném bloku šablony, než ve kterém byla otevřena.                                 | ✔️      |
| T041 | Značka extends by měla být první značkou v šabloně.                                                    | ✔️      |
| H042 | Atribut for značky label nemá v tomto souboru odpovídající id elementu.                                | ✔️      |
| T042 | Obsah mimo blok se v šabloně, která rozšiřuje jinou, nevykreslí.                                       | ✔️      |
| H043 | Značka button by měla mít atribut `type`.                                                              | ✔️      |
| T043 | Název bloku je v šabloně použit vícekrát.                                                              | ✔️      |
| H044 | Thead by neměl míchat buňky `th` a `td`.                                                               | ✔️      |
| T044 | Výstupní značka obsahuje klíčové slovo příkazu; použijte blokovou značku.                              | ✔️      |
| H045 | Značka iframe by měla mít atribut `title`.                                                             | ✔️      |
| T045 | Šablonová značka uvnitř html komentáře se stále provede; k jejímu vypnutí použijte šablonový komentář. | ✔️      |
| H046 | Tabindex by neměl být kladný.                                                                          | ✔️      |
| H047 | Aria-hidden by nemělo být nastavené na fokusovatelném elementu.                                        | ✔️      |
| H048 | Atribut aria nepatří mezi ty, které definuje specifikace.                                              | ✔️      |
| H049 | Viewport by neměl bránit přiblížení stránky.                                                           | ✔️      |
| H050 | Element je zastaralý a měl by být nahrazen.                                                            | ✔️      |
| H051 | Role nepatří mezi ty, které ARIA definuje pro značkování.                                              | ✔️      |
| H052 | Meta refresh by neměl stránku po uplynutí času znovu načítat ani přesměrovávat.                        | ✔️      |
| H053 | Id je v souboru použito vícekrát.                                                                      | ✔️      |
| H054 | Interaktivní element by neměl být vnořený do jiného.                                                   | ✔️      |
| H055 | Atribut lang by měl obsahovat jazykovou značku, například en nebo pt-BR.                               | ✔️      |
| H056 | Src by neměl být prázdný.                                                                              | ✔️      |
| H057 | Video by mělo mít stopu s titulky.                                                                     | ✔️      |

### Struktura kódů

První písmeno kódu má tento význam:

- D: týká se konkrétně Djanga
- H: týká se html
- J: týká se konkrétně Jinja
- M: týká se konkrétně Handlebars
- N: týká se konkrétně Nunjucks
- T: týká se šablon obecně

### Podrobnosti pravidel

<!-- oxfmt-ignore-start -->

#### T001

`Variables should be wrapped in a whitespace.`

Šablonová syntaxe jako `{{user.name}}` bez vnitřních mezer se hůř čte i porovnává v diffech a nejednotné mezery v kódové základně dělají refaktoring založený na grepu (hledání proměnné nebo značky) nespolehlivým, protože tentýž výraz existuje v několika podobách. Stylové příručky Djanga i Jinja píší `{{ var }}` a `{% tag %}` s jednou mezerou.

Neuplatňuje se v profilech handlebars a golang.

Špatně:

```html
{{user.name}}
```

Správně:

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

Míchání jednoduchých a dvojitých uvozovek v šablonových značkách (`{% extends %}`, `{% include %}`, `{% with %}`, `{% trans %}`, `{% now %}`) způsobí, že se tentýž název šablony objevuje ve dvou podobách, takže hledání a hromadné přejmenování mine polovinu výskytů. Sjednocení na dvojité uvozovky udržuje argumenty značek v souladu s uvozovkami HTML atributů ve zbytku souboru.

Jednoduché uvozovky uvnitř hodnot HTML atributů (např. `<span title="{% trans 'x' %}">`) se nehlásí, protože dvojité uvozovky atributu si tam jednoduché uvozovky vynucují.

S `quote_style = "single"` pravidlo naopak vyžaduje jednoduché uvozovky a formátovač je také zapisuje.

`--reformat` tyto uvozovky přepíše za vás, takže nález nikdy nevyžaduje ruční práci.

Špatně:

```html
{% extends 'base.html' %}
```

Správně:

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

Když `{% block %}` zabírá mnoho řádků nebo jsou bloky vnořené, holý `{% endblock %}` nijak nenaznačuje, který blok uzavírá, takže se při úpravách snadno ukončí nesprávný blok; podřízené šablony pak přepisují nesprávný obsah. Pojmenovaný endblock dokumentuje párování a umožňuje djLint i Djangu (které při nesouhlasném názvu v endblock vyvolá TemplateSyntaxError) zachytit blok uzavřený na nesprávném místě. Chyby párování (neuzavřené bloky, osiřelé endblocky a nesouhlasné názvy) jsou kontroly správnosti, které řeší T038.

Ve výchozím nastavení vypnuto; zapněte ho pomocí `--include=T003`. `--name-endblocks` název zapíše za vás, takže nález nikdy nevyžaduje ruční práci.

Název není nutný, když se blok otevírá i zavírá na stejném řádku, např. `{% block title %}``{% endblock %}`. Formátovač přesouvá obsah bloku, který obsahuje další značky, na samostatné řádky, takže blok zapsaný na jednom řádku může po naformátování název potřebovat; s `--name-endblocks` formátovač zapíše i tento název.

Špatně:

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

Správně:

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Static urls should follow {% static path/to/file %} pattern.`

Napevno zapsané cesty /static/ obcházejí značku `{% static %}` Djanga, takže se šablony rozbijí, když se změní STATIC_URL (např. při přesunu souborů na CDN nebo při nasazení do podcesty), a nikdy nepoužijí hashované názvy souborů z ManifestStaticFilesStorage, což v produkci způsobí chyby 404 nebo zastaralé soubory v mezipaměti. Pravidlo hledá doslovnou předponu `/static/`, takže projekt, který statické soubory obsluhuje z jiné cesty, nepokrývá.

Špatně:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Správně:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

Napevno zapsané cesty /static/ obcházejí url_for('static', ...) z Flasku/Jinja, takže soubory skončí chybou 404, když je aplikace připojená pod předponou URL nebo se změní složka či hostitel statických souborů, a ztratí se i řetězce dotazu pro vynechání mezipaměti, které přidává framework. Pravidlo hledá doslovnou předponu `/static/`, takže projekt, který statické soubory obsluhuje z jiné cesty, nepokrývá.

Špatně:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Správně:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have a non-empty lang attribute.`

Bez atributu lang na `<html>` odhadují čtečky obrazovky pravidla výslovnosti a mohou stránku číst v nesprávném jazyce a prohlížeče nedokážou správně nabídnout překlad, dělení slov ani uvozovky podle národního prostředí. Uvedení jazyka stránky je kritérium úspěšnosti 3.1.1 WCAG 2.1 (úroveň A).

`lang=""` i `lang` bez hodnoty říkají, že jazyk není znám, a proto se hlásí stejně jako chybějící atribut.

Špatně:

```html
<!DOCTYPE html>
<html>
</html>
```

Správně:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`Img tag should have height and width attributes.`

Ve výchozím nastavení vypnuto; zapněte ho pomocí `--include=H006`.

Když `<img>` nemá šířku a výšku, prohlížeč nemůže před stažením obrázku vyhradit místo, takže okolní obsah při načítání obrázků poskakuje. Tento posun rozvržení zhoršuje Cumulative Layout Shift (metriku Core Web Vitals) a může způsobit, že uživatel klikne vedle, než se stránka ustálí.

Špatně:

```html
<img src="cat.png" alt="Cat">
```

Správně:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

Bez `<!DOCTYPE>` před značkou `<html>` vykreslují prohlížeče stránku v režimu quirks, který napodobuje zastaralý box model a chování rozvržení, takže se CSS v různých prohlížečích vykresluje nejednotně. Šablonové značky a komentáře před doctype nevadí; předcházet musí jen samotné značce `<html>`.

Špatně:

```html
<html lang="en">
</html>
```

Správně:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Attributes should be double quoted.`

Míchání stylů uvozovek ztěžuje čtení hodnot atributů i jejich hledání grepem a hodnoty v jednoduchých uvozovkách se rozbijí, jakmile obsah obsahuje apostrof. Dvojité uvozovky jsou konvencí, kterou používají specifikace HTML, formátovače i většina stylových příruček, takže sjednocení na ně udržuje šablony v souladu se širším ekosystémem.

Špatně:

```html
<div class='content'></div>
```

Správně:

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

Parsery HTML přijímají názvy značek velkými písmeny, ale serializace XHTML a XML rozlišují velikost písmen a odmítají je, a nejednotná velikost písmen dělá hledání v textu i revizi diffů nespolehlivými (grep na `<h1>` mine `<H1>`). Názvy značek malými písmeny udržují šablony přenositelné a jednotné.

S `--ignore-case`, které formátovači říká, aby velikost písmen neměnil, se nehlásí.

Špatně:

```html
<H1>Welcome</H1>
```

Správně:

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

Názvy atributů velkými písmeny jsou v serializacích XHTML/XML neplatné a maří hledání v šablonách (grep na src= mine SRC=). DOM názvy HTML atributů stejně převádí na malá písmena, takže velká písmena jen přidávají nejednotnost bez jakéhokoli přínosu. Hlásí se jen ty názvy, které formátovač převádí na malá písmena: `class`, `id`, `src`, `width`, `height`, `alt`, `style`, `lang`, `title`, `media` a `srcset`. `--reformat` je opraví za vás a vazba frameworku jako `:itemID` nebo delší název jako `data-ID` si velikost písmen zachová.

S `--ignore-case`, které formátovači říká, aby velikost písmen neměnil, se nehlásí.

Špatně:

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

Správně:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

Hodnoty atributů bez uvozovek končí prvním prázdným znakem, takže hodnota jako class=btn primary tiše zahodí vše za mezerou (prohlížeč považuje „primary“ za samostatný logický atribut). Obzvlášť křehké jsou hodnoty pocházející ze šablonových proměnných: jakákoli vykreslená mezera, „=“ nebo „>“ značku poškodí. Uvozovky dělají hranici hodnoty explicitní a bezpečnou.

Špatně:

```html
<div class=test></div>
```

Správně:

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

S mezerami kolem „=“ se značka čte jako tři samostatné tokeny a od rozpadnutí ji dělí jediná úprava: zalomení nebo zkrácení řádku uprostřed zanechá holý logický atribut a k tomu zatoulaný text. Souvislý zápis name="value" také předpokládají jednoduché textové nástroje (grep, hledání a nahrazování), takže nejednotné mezery ztěžují spolehlivé hledání a refaktoring atributů. `--reformat` mezery odstraní za vás.

Špatně:

```html
<div class = "test"></div>
```

Správně:

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

Bez atributu alt čtečky obrazovky ohlásí název souboru obrázku, nebo vůbec nic, čímž stránka nesplňuje WCAG 1.1.1 (Netextový obsah). Text v alt je také to, co uživatelé uvidí, když se obrázek nepodaří načíst. Dekorativní obrázky by měly mít výslovně prázdný alt="", aby asistivní technologie věděly, že je mají přeskočit; i to toto pravidlo splňuje.

`alt` bez hodnoty je totéž co `alt=""`, tedy případ dekorativního obrázku, a proto se přijímá.

Špatně:

```html
<img src="cat.jpg" height="200" width="300">
```

Správně:

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

Řady prázdných řádků nemají na vykreslenou stránku žádný vliv (HTML prázdné znaky slučuje), ale nafukují šablony a vytvářejí zašuměné diffy, když se změní sousední řádky. Formátovač djLint je ve výchozím nastavení úplně odstraní (ponechá nejvýše `max_blank_lines` prázdných řádků, výchozí hodnota je 0), takže zbylé řady ukazují na nenaformátovaný kód.

Špatně:

```html
<div>one</div>


<p>two</p>
```

Správně:

```html
<div>one</div>

<p>two</p>
```

#### H015

`Follow h tags with a line break.`

Nadpisy jsou blokové orientační body, které určují osnovu dokumentu; když se další element natlačí na stejný řádek jako uzavírací značka h, tato struktura se ve zdrojovém kódu ztratí a úpravy kteréhokoli z obou elementů se v diffech projeví jako změny obou. Zalomení řádku za každým nadpisem udržuje vizuální strukturu šablony v souladu s vykreslenou osnovou.

Špatně:

```html
<h1>Heading</h1><p>Intro text.</p>
```

Správně:

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Missing title tag in html.`

Specifikace HTML vyžaduje v každém dokumentu element title. Bez něj ukazují karty prohlížeče, záložky i historie místo názvu stránky holou URL, vyhledávače přijdou o hlavní popisek stránky a uživatelé čteček obrazovky o první věc, která se po načtení ohlásí, čímž stránka nesplňuje WCAG 2.4.2 (Název stránky, úroveň A).

Spouští se jen na souborech obsahujících úplný dokument `<html>`...`</html>`, takže dílčí šablony a podřízené šablony, které rozšiřují základní šablonu, se nikdy nehlásí. Kostry SPA, které nastavují titulek na straně klienta, stále potřebují statický `<title>`: zobrazí se při prvním vykreslení, v crawlerech a při selhání JavaScriptu.

Špatně:

```html
<html lang="en">
<body>Content</body>
</html>
```

Správně:

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

Šablony, které musí jít zpracovat také jako XML/XHTML (nebo slouží jako vstup pro nástroje založené na XML), odmítají nepárové elementy zapsané bez uzavíracího lomítka a míchání `<br>` s `<br />` napříč kódovou základnou vytváří nejednotné diffy. Toto pravidlo vynucuje konvenci ve stylu XHTML, takže každý nepárový element je uzavřený stejně.

Ve výchozím nastavení vypnuto; zapněte ho pomocí `--include=H017`. Vzájemně se vylučuje s H018; zapněte jen jednu z obou konvencí. `--close-void-tags` přidá lomítko k nepárovým značkám html za vás. Svg `<path>` zůstává tak, jak je zapsaný, proto ho uzavřete ručně.

Špatně:

```html
<br>
<meta charset="utf-8">
```

Správně:

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Internal links should use the {% url ... %} pattern.`

Napevno zapsané interní URL tiše zastarají, když se cesta routy změní v urls.py, a vzniknou nefunkční odkazy a mrtvé akce formulářů, které žádný test URLconf nezachytí. `{% url %}` sestaví cestu z názvu routy, takže přejmenování cesty aktualizuje všechny odkazy najednou.

Špatně:

```html
<a href="/accounts/login">Login</a>
```

Správně:

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

Podle HTML Living Standard nemá koncové lomítko u nepárového elementu žádný význam (parser ho ignoruje), takže zápis `<br />` naznačuje samouzavírací chování ve stylu XML, které HTML nemá, a může čtenáře svést k přidávání lomítek i k párovým značkám, kde se zatoulané / tiše zahodí a zakryje chyby s neuzavřenými značkami. Toto pravidlo vynucuje u nepárových elementů prosté zakončení >.

Ve výchozím nastavení vypnuto; zapněte ho pomocí `--include=H018`. Vzájemně se vylučuje s H017; zapněte jen jednu z obou konvencí. SVG `<path />` je výjimkou, protože SVG je XML a lomítko vyžaduje. S `--close-void-tags` se nehlásí, protože formátovač pak zapisuje právě to lomítko, které toto pravidlo hlásí.

Špatně:

```html
<br />
<meta charset="utf-8" />
```

Správně:

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

Napevno zapsané interní URL se tiše rozbijí, když se cesta routy změní nebo je aplikace připojená pod předponou, a zůstanou po nich mrtvé odkazy a akce formulářů odesílané na 404. url_for() sestaví URL z názvu endpointu, takže se změny rout automaticky promítnou do všech šablon.

Špatně:

```html
<a href="/accounts/login">Login</a>
```

Správně:

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

URL javascript: znemožňují kliknutí prostředním tlačítkem i otevření na nové kartě, nedělají nic, když je JavaScript vypnutý nebo se nenačte, blokují je přísné zásady Content Security Policy a jsou klasickým místem pro injekci XSS. Pro href použijte skutečnou URL a chování připojte obslužnou rutinou události. Při přísné CSP jsou blokované i inline obslužné rutiny on*: uvedený onclick je minimální oprava přímo v šabloně; raději připojte posluchač pomocí addEventListener ze souboru skriptu.

Špatně:

```html
<a href="javascript:openPopup()">Open popup</a>
```

Správně:

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

Prázdný pár značek nevykreslí žádný obsah, ale přesto vytvoří uzel DOM, na který se mohou ze stylů uplatnit okraje, rámečky nebo mezery flex/grid, a vzniká tak fantomové odsazení, které se těžko dohledává; obvykle jde o zbytek značkování z dřívější úpravy. Značky, které jsou v běžném značkování oprávněně prázdné (td, th, li, dt, dd, slot), jsou výjimkou. Nehlásí se ani značky s jakýmkoli atributem (body pro připojení JS jako `<div id="app">``</div>`, elementy ikonových fontů jako `<i class="fa fa-user">``</i>`); pravidlu odpovídají jen prázdné páry zcela bez atributů.

Špatně:

```html
<p>Saved.</p>
<span> </span>
```

Správně:

```html
<p>Saved.</p>
```

#### H021

`Inline styles should be avoided.`

Inline styly mají vyšší specificitu než jakýkoli selektor ve stylopisu, takže jejich pozdější přepsání vyžaduje !important; blokují je zásady Content Security Policy bez 'unsafe-inline' ve style-src; a rozptylují vzhled po šablonách, takže změna motivu nebo designu znamená upravovat značkování místo jednoho stylopisu. Přesuňte deklaraci do třídy CSS. Jedna oprávněná výjimka: HTML šablony e-mailů, kde mnoho e-mailových klientů bloky `<style>` odstraňuje a inline styly jsou standardní technikou; adresáře s šablonami e-mailů vylučte nebo pro ně toto pravidlo vypněte.

Špatně:

```html
<div style="color: red;">Wrong username or password.</div>
```

Správně:

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

Prosté podzdroje http:// na stránce obsluhované přes HTTPS jsou smíšeným obsahem: prohlížeče skripty, stylopisy a iframy rovnou blokují a u obrázků provedou automatický upgrade nebo varují. Odkaz `<a>` na stránku http:// smíšeným obsahem není, ale přesto posílá návštěvníky přes nešifrované spojení, které je otevřené odposlechu i manipulaci. Hlásit se budou i odkazy na interní hostitele, kteří TLS opravdu nemají; taková místa umlčte blokem `{# djlint:off H022 #}`, místo abyste pravidlo vypínali.

Špatně:

```html
<a href="http://example.com">Example</a>
```

Správně:

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

Dokumenty HTML5 jsou v UTF-8, takže doslovný znak funguje všude a právě ten recenzenti skutečně čtou; překlep ve znakové entitě (např. `&mdsah;`) prohlížeč nezachytí a vykreslí ho doslova jako rozbitý text. djLint povoluje entity, které nesou syntaxi (`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;` a složené závorky `&lbrace;` a `&rbrace;` spolu s `&percnt;`, `&num;` a `&dollar;`, které by po vypsání dokončily oddělovač šablony), a ty, které označují neviditelný znak, a proto ho nelze zkontrolovat jako doslovný znak: mezery (`&nbsp;`, `&thinsp;`, `&hairsp;`), spojovače a značky (`&zwnj;`, `&zwj;`, `&lrm;`, `&rlm;`) a `&shy;`, a to v pojmenované, desítkové i šestnáctkové podobě.

`--reformat` entitu přepíše na znak za vás, takže nález nikdy nevyžaduje ruční práci. Entita zapsaná uvnitř šablonové značky je součástí značky, a ne stránky, takže se jí nedotkne pravidlo ani formátovač. `--no-entity-formatting` přepisování vypne, ale pravidlo nechá zapnuté, takže se entita stále hlásí. Chcete-li entity zachovat, přidejte `H023` do `ignore`.

Špatně:

```html
<p>Dates 1900 &mdash; 2000</p>
```

Správně:

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript a text/css jsou výchozí hodnoty HTML5 pro `<script>` a `<style>`, takže atribut je jen přítěží, kterou prohlížeč ignoruje; specifikace WHATWG výslovně říká, že se má vynechávat. Jeho odstraněním se také vyhnete zastaralým řetězcům MIME, které element rozbijí, když se zkopírují do modulových skriptů (kde na type="module" skutečně záleží).

Špatně:

```html
<script type="text/javascript" src="app.js">
```

Správně:

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

Značka bez odpovídající otevírací nebo uzavírací značky nutí obnovu po chybách v prohlížeči hádat, kde element končí, takže se následující značkování pohltí do nesprávného elementu; rozvržení, selektory CSS i dotazy JavaScriptu na DOM se pak tiše rozbijí, a v každém prohlížeči jinak. H025 hlásí také `<ol>` nebo `<ul>` otevřený uvnitř `<p>`: parser HTML uzavře odstavec před seznamem, takže se značkování nikdy nevnoří tak, jak je zapsané.

Špatně:

```html
<div>
  <p>Hello</p>
```

Správně:

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Empty id and class tags can be removed.`

Prázdnému atributu neodpovídá žádný selektor třídy ani id a prázdné id je neplatné HTML (hodnota id nesmí být prázdný řetězec). Selektor přítomnosti atributu jako `div[class]` mu ale stále odpovídá, takže odstranění atributu se ve stylopisu napsaném tímto způsobem projeví. Obvykle signalizuje chybu v šabloně, kde se měla dosadit proměnná, takže jeho odstranění nebo vyplnění zabrání tomu, aby tato chyba zůstala skrytá na očích.

Špatně:

```html
<div id="" class="">content</div>
```

Správně:

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

Uvozovka, která je uvnitř `{% ... %}` nebo `{{ ... }}` otevřená, ale nikdy neuzavřená, způsobí, že šablonovací systém značku zpracuje chybně: Django a Jinja buď při vykreslování vyvolají TemplateSyntaxError, nebo tiše pohltí zbytek argumentů značky jako obsah řetězce, takže stránka skončí chybou 500 nebo se vykreslí s chybějícími argumenty.

Špatně:

```html
{% trans "Welcome %}
```

Správně:

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

Ve výchozím nastavení vypnuto; zapněte ho pomocí `--include=T028`.

Prázdné znaky, které značka bez mezer odstraní, jsou prázdné znaky, které se vykreslují, proto ji používejte jen tam, kde atribut nemá co ztratit. `alt="{%- if brand -%}Acme{%- endif -%} logo"` se vykreslí jako `Acmelogo` a svg `d="M12 {%- if big -%}20{%- endif -%} 4Z"` se stane jinou cestou. Proto je toto pravidlo volitelné.

Šablonové značky uvnitř hodnoty atributu vypisují prázdné znaky a nové řádky kolem sebe do vykresleného atributu, takže href nebo src sestavené pomocí prostých značek `{% if %}`/`{% for %}` může obsahovat zatoulané mezery a vytvořit nefunkční URL. Značky pro řízení prázdných znaků v Jinja/Nunjucks (`{%- ... -%}`) tyto okolní prázdné znaky odstraní, takže se atribut vykreslí jako jedna čistá hodnota. Atribut class je výjimkou, protože nadbytečné prázdné znaky mezi názvy tříd neškodí.

Neuplatňuje se v profilu django: šablonové značky Djanga řízení prázdných znaků `{%- -%}` nepodporují.

Špatně:

```html
<a href="{% if x %}/home{% endif %}"></a>
```

Správně:

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

Specifikace HTML definuje klíčová slova pro method formuláře malými písmeny (get, post); varianty velkými písmeny prohlížeče přijímají jen díky náhradnímu porovnávání bez ohledu na velikost písmen. Dodržování kanonického tvaru malými písmeny udržuje šablony jednotné a dohledatelné grepem a předchází stížnostem přísných validátorů a nástrojů založených na XHTML.

Špatně:

```html
<form method="POST"></form>
```

Správně:

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

Vyhledávače používají meta description jako úryvek pod názvem stránky ve výsledcích; bez něj si úryvek poskládají z libovolného textu stránky, což snižuje míru prokliku a vytváří špatné náhledy odkazů, když je stránka sdílena.

Spouští se jen na souborech obsahujících úplný dokument `<html>`...`</html>`. Argument s úryvkem se týká veřejně indexovaných stránek; u aplikací za přihlášením nebo intranetových aplikací se toto pravidlo běžně vypíná.

Špatně:

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

Správně:

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

Řady mezer nebo tabulátorů mezi argumenty šablonové značky jsou neviditelný šum: skrývají skutečné rozdíly v diffech, mohou ztížit odhalení chybějícího argumentu a odchylují se od stylu s jednou mezerou, který vytváří formátovač djLint, což způsobuje zbytečné přeformátovávání. Prázdné znaky uvnitř řetězců v uvozovkách se zachovávají a nehlásí se.

Špatně:

```html
{% static  'css/style.css' %}
```

Správně:

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

Prázdné znaky na začátku nebo na konci hodnoty action formuláře se stanou součástí vykreslené URL. Prohlížeče je při zpracování odstraní, ale klienti mimo prohlížeč a testy pracující s doslovnou hodnotou nemusí, a kolem značky `{% url %}` zatoulaná mezera téměř vždy signalizuje překlep, který vykreslí URL pro odeslání, jež na serveru neodpovídá žádné routě.

Špatně:

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

Správně:

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Did you intend to use {% ... %} instead of {% ... }%?`

}% je téměř vždy překlep za %}. Šablonovací systém }% nerozpozná jako oddělovač značky, takže se značka nikdy nezpracuje: surový text {% ... }% prosákne do vykresleného HTML, nebo systém vyvolá chybu syntaxe, když narazí na neuzavřenou značku.

Špatně:

```html
{% include "footer.html" }%
```

Správně:

```html
{% include "footer.html" %}
```

#### H036

`Do not use br tags for spacing.`

Specifikace html povoluje `<br>` jen pro zalomení řádku, které je součástí samotného obsahu, jako v poštovní adrese nebo v básni, a takové použití zůstává bez povšimnutí. Hlásí se prezentační použití, které specifikace vylučuje: řada dvou a více zalomení, která vytváří svislou mezeru, a zalomení u vnitřního okraje blokového elementu, které nevykreslí nic, co by nevykreslil jeho vlastní okraj. Obojí rozbíjí přelévání textu při malé šířce a čtečka obrazovky ohlásí vynucené zalomení tam, kde není co ohlašovat.

Špatně:

```html
<p>Shipping is free.<br><br>Delivery takes 3 days.</p>
```

Správně:

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

Duplicitní atributy jsou neplatné HTML a prohlížeče si ponechají jen první výskyt a ostatní tiše zahodí, takže druhá hodnota class nebo style se nikdy neuplatní, což skrývá skutečné chyby. Kontrola rozumí šablonám: atribut opakovaný ve vzájemně se vylučujících větvích (`{% if %}`/`{% else %}`) se nehlásí, protože se může vykreslit jen jedna kopie.

Špatně:

```html
<div class="card" id="profile" class="active">...</div>
```

Správně:

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

Bloková značka jako `{% if %}`, `{% for %}` nebo `{% macro %}` bez odpovídající koncové značky je v Djangu a Jinja tvrdou chybou TemplateSyntaxError: stránka se při požadavku nevykreslí, což toto pravidlo zachytí ještě před nasazením. Hlásí také osiřelé koncové značky bez otevírací značky a nesprávně prokládané bloky (např. `{% if %}``{% for %}``{% endif %}`).

Toto pravidlo kontroluje párování `{% block %}`/`{% endblock %}` i nesouhlasné názvy v endblock; T003 (ve výchozím nastavení vypnuté) navíc vyžaduje název u každého víceřádkového `{% endblock %}`. Kontrolují se i vlastní blokové značky registrované přes custom_blocks, včetně jejich samouzavírací podoby / %}.

Špatně:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

Správně:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Unclosed template tag found.`

Šablonová značka otevřená pomocí `{{` nebo `{%`, ale nikdy neuzavřená odpovídajícím `}}` nebo `%}`, se jako značka nezpracuje: Django/Jinja buď vyvolají TemplateSyntaxError, nebo vykreslí surové složené závorky do stránky, a vše až po další oddělovač se může tiše pohltit. Tyto překlepy (jediná chybějící závorka, nesouhlasný oddělovač) se při revizi snadno přehlédnou, protože se šablona může stále částečně vykreslit.

Špatně:

```html
<p>{{ user.name }</p>
```

Správně:

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

Značka `{% extends %}` nebo `{% include %}` s chybějícím, prázdným nebo jen z prázdných znaků složeným názvem šablony nemá co načíst: Django vyvolá TemplateSyntaxError, když název úplně chybí, a TemplateDoesNotExist při vykreslování, když je prázdný, takže stránka v produkci skončí chybou 500, přestože samotný soubor šablony vypadá syntakticky věrohodně.

Špatně:

```html
{% extends "" %}
```

Správně:

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

Když je HTML značka otevřená v jednom `{% block %}`, ale uzavřená v jiném, podřízená šablona, která přepíše jen jeden z těchto bloků, zdědí polovinu elementu a ve vykreslené stránce vznikne nevyvážené značkování; prohlížeče pak elementy nepředvídatelně automaticky uzavírají nebo znovu vnořují, a rozbíjejí tak rozvržení i selektory CSS daleko od šablony, která se skutečně upravovala. Když se každý element otevírá i zavírá ve stejném bloku, lze každý blok bezpečně přepsat samostatně.

Špatně:

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

Správně:

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

Django odmítne zkompilovat šablonu, ve které před `{% extends %}` stojí jiná značka, a text zapsaný před ní se vykreslí, takže prosákne do stránky před vše, co vytvoří rodičovská šablona. Jinja tento text také vykreslí a nunjucks ho zahodí, takže v žádném systému šablona nedělá to, co se zdá, že dělá.

Komentář `{# #}` nic nevykresluje a nepočítá se, stejně jako cokoli uvnitř bloku `{% comment %}`, <code>{&#37; raw %}</code> nebo `{% verbatim %}`, ať pojmenovaného, nebo ne, oblast `{# djlint:off #}` v kterémkoli ze tří zápisů nebo yaml front matter. HTML komentář se počítá: systém ho zapíše do stránky před doctype rodičovské šablony, a to je právě ten únik, o který v tomto pravidle jde. Počítá se také blok `{% blocktrans %}`, blok `{% filter %}` a blok `<?php ?>`, protože každý z nich něco vykreslí. Kontroluje se jen první `{% extends %}`; druhý je chybou sám o sobě. V profilech jinja a nunjucks se značka větvení před ním nepočítá, protože jinja dokumentuje `{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}` jako způsob, jak zvolit rodiče; django načte zbytek šablony do `{% extends %}` a pak odmítne `{% endif %}`, takže v tomto profilu se značka větvení počítá.

Neuplatňuje se v profilech handlebars, golang, liquid a angular.

Špatně:

```html
{% load static %}
{% extends "base.html" %}
```

Správně:

```html
{% extends "base.html" %}
{% load static %}
```

#### H042

`Label for attribute has no matching element id in this file.`

Kontrola se spouští jen na souborech, které dokáže spolehlivě analyzovat: pokud soubor obsahuje cokoli, co by mohlo vykreslit id, které tento soubor nikde neukazuje (výstup `{{ ... }}` jako widget formuláře, `{% include %}` nebo `{% extends %}` nebo nerozpoznanou šablonovou značku), pravidlo u tohoto souboru mlčí. Tam, kde se spustí, je každé hlášení skutečně nefunkční vazbou.

Špatně:

```html
<label for="email">Email</label>
<input id="username">
```

Správně:

```html
<label for="email">Email</label>
<input id="email">
```

#### T042

`Content outside a block is not rendered in a template that extends another.`

Jakmile šablona rozšiřuje jinou, o výstupu rozhoduje rodič a potomek jen vyplňuje bloky rodiče. Text nebo html zapsané za `{% extends %}` a mimo všechny `{% block %}` se při vykreslování tiše zahodí, takže odstavec, který ve zdrojovém kódu vypadá v pořádku, se na stránku nikdy nedostane.

Šablonová značka se tam stále provede, takže `{% load %}`, `{% set %}` a `{% if %}` obalující blok zůstávají bez povšimnutí, stejně jako komentáře `{# #}` a `{% comment %}`, html komentáře, bloky <code>{&#37; raw %}</code> a `{% verbatim %}` a tělo `{% macro %}`, blokové podoby `{% set %}`, `{% partialdef %}` nebo `{% addtoblock %}`, které se zachytí, místo aby se vypsalo. Text `{% blocktrans %}` se hlásí, protože `{% blocktrans %}` není `{% block %}`. Zohledňuje se jen obsah za značkou extends a každý jeho souvislý úsek se hlásí jednou, na svém začátku.

Šablonovací systém čte šablonové značky dřív než html, takže `{% extends %}` zapsané uvnitř html komentáře nebo `<pre>` se stále provede a ze souboru stále udělá potomka; skutečně ho skryjí jen `{# #}`, `{% comment %}`, <code>{&#37; raw %}</code> a `{% verbatim %}`. Text uvnitř html komentáře se tak či tak k žádnému čtenáři nedostane a nehlásí se, ale značky v něm zapsané se stále čtou.

Neuplatňuje se v profilech handlebars, golang, liquid a angular.

Špatně:

```html
{% extends "base.html" %}
<p>This paragraph is never shown.</p>
{% block content %}
<h1>Welcome</h1>
{% endblock %}
```

Správně:

```html
{% extends "base.html" %}
{% block content %}
<h1>Welcome</h1>
<p>This paragraph is shown.</p>
{% endblock %}
```

#### H043

`Button tag should have a type attribute.`

`<button>` bez `type` má výchozí hodnotu `submit`, takže tlačítko napsané pro spuštění skriptu zároveň odešle formulář, ve kterém je, a stránka se znovu načte. Výslovné uvedení typu tomu zabrání.

Špatně:

```html
<form>
  <button onclick="preview()">Preview</button>
</form>
```

Správně:

```html
<form>
  <button type="button" onclick="preview()">Preview</button>
</form>
```

#### T043

`Block name is used more than once in the template.`

Django, Jinja i Nunjucks odmítnou zpracovat šablonu, která pojmenuje dva bloky stejně, takže se stránka vůbec nenačte. Šablonovacím systémům nezáleží na tom, že oba bloky leží v různých větvích `{% if %}`, takže každý název bloku musí být jedinečný v celé šabloně, ať už bloky stojí vedle sebe, nebo je jeden vnořený do druhého.

Počítá se jen `{% block %}`: `{% blocktrans %}` není blok a `{% endblock name %}` jen pojmenovává blok, který uzavírá. Názvy se porovnávají tak, jak jsou zapsané, protože šablonovací systémy považují `Content` a `content` za dva bloky.

Přeskakuje se jen to, co šablonovací systém sám nikdy nezpracovává: šablonový komentář, blok `{% comment %}`, tělo <code>{&#37; raw %}</code> nebo `{% verbatim %}` a oblast `djlint:off`. Blok zapsaný uvnitř html komentáře, v těle `<script>`, `<style>`, `<pre>` nebo `<textarea>` nebo v těle `{% filter %}` se stále počítá, protože systém všechny tyto části čte a na duplicitní název stejně vyvolá chybu.

`{% embed %}` otevírá vlastní obor: bloky v něm vyplňují vloženou šablonu, a ne tuto, takže dvě vložení stejné dílčí šablony mohou každé obsahovat `{% block body %}`. Název opakovaný uvnitř jednoho embed se stále hlásí.

Neuplatňuje se v profilech handlebars, golang, liquid a angular.

Špatně:

```html
{% block content %}{% endblock %}
{% block content %}{% endblock %}
```

Správně:

```html
{% block content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

#### H044

`Thead should not mix th and td cells.`

Každý řádek se posuzuje samostatně, takže vysvětlující řádek s `td`, který specifikace html umisťuje do `thead` vedle řádku záhlaví, není směsí. Prázdná `td` na začátku řádku je rohová buňka tabulky se záhlavími v prvním sloupci, což je přesně značkování, které vyžaduje tutoriál W3C o přístupnosti, a proto se přeskakuje.

`th` a `td` mají pro čtečku obrazovky odlišný význam a obvykle i odlišné css, takže jedna zatoulaná buňka v řádku záhlaví se čte jako data a má jiný styl než sloupce vedle ní. Taková směs je platné html, a právě proto se těžko odhaluje.

Špatně:

```html
<thead>
  <tr>
    <th>Name</th>
    <td>Size</td>
  </tr>
</thead>
```

Správně:

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

Neuplatňuje se v profilech golang, handlebars a angular.

Výstupní značka vypisuje hodnotu, kdežto `if`, `for`, `url`, `include` a ostatní jsou příkazy, které patří do blokové značky. Django, Jinja i Nunjucks odmítnou `{{ if x }}` s chybou syntaxe a samotné uzavírací klíčové slovo, například `{{ endif }}`, se čte jako proměnná, která nic nevykreslí, zatímco blok, který měla uzavřít, zůstává otevřený, takže se stránka buď nenačte, nebo ukáže to, co měla podmínka skrýt.

Samotné klíčové slovo je obyčejný název proměnné, takže `{{ url }}`, `{{ url|default:"/" }}` a `{{ set.name }}` se nehlásí. Hlásí se jen klíčové slovo s argumentem a vedle toho samotné uzavírací nebo větvicí klíčové slovo jako `{{ endif }}` nebo `{{ else }}`. Řídicím klíčovým slovem jako `if` nebo `for` výraz začínat nemůže, takže cokoli za ním je argument, včetně operátoru, a `{{ if -1 > count }}` se hlásí. Ostatní názvy slouží zároveň jako proměnné a funkce a u nich se za argument považuje jen řetězec v uvozovkách nebo slovo, takže výraz, který jedním z nich náhodou začíná, zůstává bez povšimnutí: `{{ url ~ "/x" }}`, `{{ url if url else "#" }}`, `{{ url ? url : '#' }}`, `{{ block ('title') }}`, `{{ block .super }}` i `{{ filter [0] }}` se nehlásí.

Tělo bloku <code>{&#37; raw %}</code> nebo `{% verbatim %}` je text, nikoli šablonová syntaxe, a přeskakuje se, včetně pojmenované podoby `{% verbatim vueapp %}...{% endverbatim vueapp %}`, takže `{{ }}` z Vue nebo Handlebars chráněné tímto způsobem se nehlásí. `{{ }}` zapsané uvnitř argumentu blokové značky v uvozovkách, jako v `{% trans "Write {{ if x }} instead" %}`, je text, který systém vypíše, a také zůstává bez povšimnutí.

Špatně:

```html
{{ if user.is_active }}
```

Správně:

```html
{% if user.is_active %}
```

#### H045

`Iframe tag should have a title attribute.`

Čtečka obrazovky ohlašuje iframe podle jeho přístupného názvu. Bez něj přečte URL rámce, nebo vůbec nic, a neexistuje způsob, jak zjistit, co je vložená stránka zač, dřív než do ní uživatel vstoupí. WCAG to řadí pod 4.1.2 Název, role, hodnota a axe i html-validate mají tuto kontrolu ve výchozím nastavení.

Název může pocházet z `title`, `aria-label` nebo `aria-labelledby` a pravidlo splní kterýkoli z nich. Název zapsaný šablonovou značkou se počítá, takže rámec s titulkem nastaveným pro každou stránku zvlášť se nehlásí.

Špatně:

```html
<iframe src="/report/"></iframe>
```

Správně:

```html
<iframe src="/report/" title="Quarterly report"></iframe>
```

#### T045

`Template tag inside an html comment still runs; use a template comment to disable it.`

Html komentář skrývá značkování před prohlížečem, ne před šablonovacím systémem. `<!-- {% include "debug.html" %} -->` soubor stále vykreslí a `<!-- {% if debug %}...{% endif %} -->` se stále vyhodnotí, v Djangu, Jinja, Nunjucks, Handlebars i Go, takže takto zakomentovaná značka dál běží a cokoli vypíše, skončí uvnitř komentáře, nebo pokud obsahuje `-->`, z něj vyskočí. Spuštění značky zabrání jen šablonový komentář, `{# #}` v Djangu a Jinja, `{{! }}` v Handlebars nebo `{{/* */}}` v Go.

Hlásí se jen příkazová značka: `{% %}` v profilech, které ji mají, sekce, uzavření nebo partial v handlebars a klíčové slovo Go jako `{{if}}` nebo `{{end}}`. Hodnota vypsaná do komentáře, jako v `<!-- built {{ version }} -->`, je záměrné použití a zůstává bez povšimnutí, stejně jako značka uvnitř šablonového komentáře, bloku `{% comment %}` nebo raw bloku a podmíněný komentář pro Internet Explorer, `<!--[if IE]> ... <![endif]-->`, jehož tělo je značkování pro prohlížeč, který jmenuje.

Samotné klíčové slovo Go je v každém jiném šablonovacím systému obyčejný název proměnné, takže `<!-- period {{ start }} to {{ end }} -->` a `<!-- Template: {{ template }} -->` jsou v Djangu, Jinja, Nunjucks, Handlebars a Liquid hodnoty a jako příkazy se čtou jen s `--profile golang`. Klíčové slovo s operandem Go, jako v `{{ if .X }}` a `{{ template "footer" . }}`, je příkaz, který žádný jiný systém nevypíše, a hlásí se v libovolném profilu. `{%` se obdobně čte jen tam, kde ho systém má, takže s `--profile handlebars` a `--profile golang` je to text, a otevření, za kterým nenásleduje žádná uzavírací závorka, jako v `<!-- battery at 50{% charge -->`, je běžný text, jak se zdá. Podmíněný komentář je jen ten, který je jako takový zapsaný, tedy začíná `<!--[if` a uzavírá ho jeho `<![endif]-->` v libovolné velikosti písmen; neuzavřený je obyčejný komentář, za jaký ho prohlížeč považuje, a značky v něm se hlásí.

Špatně:

```html
<!-- {% include "banner.html" %} -->
```

Správně:

```html
{# {% include "banner.html" %} #}
```

#### H046

`Tabindex should not be positive.`

Kladný `tabindex` přesune element na začátek pořadí tabulátoru, před vše, co ho nemá. Jediný takový element přeuspořádá celou stránku pro uživatele klávesnice a pořadí se pak musí ručně udržovat v každé šabloně, která přidá ovládací prvek. WCAG to pokrývá v kritériu 2.4.3 Pořadí fokusu.

`0` zařadí element do pořadí tabulátoru na místo, které mu dává dokument, a `-1` ho z něj vyřadí, ale ponechá ho fokusovatelný ze skriptu. Ani jedno se nehlásí, stejně jako hodnota zapsaná šablonovou značkou, jejíž číslo zde není známo.

Špatně:

```html
<input tabindex="1">
```

Správně:

```html
<input tabindex="0">
```

#### H047

`Aria-hidden should not be set on a focusable element.`

`aria-hidden="true"` vyjme element ze stromu přístupnosti, ale ponechá ho v pořadí tabulátoru, takže uživatel klávesnice na něj stále narazí a neuslyší žádné ohlášení. Skrytí dekorativní ikony je běžné použití tohoto atributu a nehlásí se; hlásí se jen element, který sám získává fokus.

Element se považuje za fokusovatelný, pokud je to `button`, `select`, `textarea`, `iframe` nebo `summary`, `a` nebo `area` s `href`, `input`, který není skrytý, `audio` nebo `video` s `controls`, nebo cokoli s `contenteditable` nebo `tabindex` s hodnotou `0` či vyšší. Ovládací prvek s `disabled` nebo s `tabindex="-1"` už v pořadí tabulátoru není a zůstává bez povšimnutí.

Špatně:

```html
<button aria-hidden="true">Close</button>
```

Správně:

```html
<button type="button" aria-label="Close"><span aria-hidden="true">x</span></button>
```

#### H048

`Aria attribute is not one the specification defines.`

Atribut aria s překlepem nedělá vůbec nic. Žádný prohlížeč nevaruje, žádná čtečka obrazovky ho nenahlásí a značkování dál vypadá, jako by bylo přístupné, takže `aria-lable` může v šabloně zůstat celé roky, zatímco ovládací prvek, který měl pojmenovat, zůstává bez názvu.

Pravidlo zná názvy, které definuje ARIA. Vazba zapsaná frameworkem není prostý název aria, takže `:aria-label`, `v-bind:aria-label` a `[attr.aria-label]` zůstávají bez povšimnutí.

Špatně:

```html
<button type="button" aria-lable="Close">x</button>
```

Správně:

```html
<button type="button" aria-label="Close">x</button>
```

#### H049

`Viewport should not stop the page being zoomed.`

`user-scalable=no` a `maximum-scale` pod 2 brání zvětšení stránky v telefonu, což je pro mnoho lidí jediný způsob, jak ji přečíst. WCAG v kritériu 1.4.4 Změna velikosti textu požaduje 200 %. Prohlížeče toto omezení stále častěji ignorují, ale značka přesto vypíná přiblížení všude, kde se respektuje.

Název i obsah se najdou bez ohledu na to, v jakém pořadí jsou zapsané.

Špatně:

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

Správně:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### H050

`Element is obsolete and should be replaced.`

`<center>`, `<font>`, `<big>`, `<strike>` a `<tt>` byly vypuštěny, když vzhled převzalo css, a `<marquee>`, `<blink>`, `<nobr>` a `<spacer>` nikdy standardní nebyly. Html už žádný z nich nedefinuje, takže nic nezaručuje, jak je prohlížeč rozvrhne, a stylopis na ně nemůže cílit tak, jako cílí na třídu.

Pravidlo zná elementy `acronym`, `applet`, `basefont`, `bgsound`, `big`, `blink`, `center`, `dir`, `font`, `frame`, `frameset`, `isindex`, `keygen`, `marquee`, `menuitem`, `nobr`, `noembed`, `noframes`, `plaintext`, `spacer`, `strike`, `tt` a `xmp`. Hlásí se jen otevírací značka, takže každý element je zmíněn jednou, a vlastní element, jehož název jedním z nich jen začíná, například `<font-picker>`, zůstává bez povšimnutí.

Špatně:

```html
<center><font color="red">Warning</font></center>
```

Správně:

```html
<p class="warning">Warning</p>
```

#### H051

`Role is not one ARIA defines for markup.`

Role, kterou žádná specifikace nezná, se rovnou zahodí a element si ponechá význam, který už měl, takže `role="buton"` ponechá `<div>` obyčejným `<div>`: pro čtečku obrazovky nic, zatímco značkování vypadá, jako by dostalo nějaký účel. Nic na to neupozorní, a právě proto se vyplatí tento překlep zachytit.

Pravidlo zná role, které ARIA definuje pro autory, spolu s těmi, které přidávají DPUB-ARIA (`doc-chapter` a další) a GRAPHICS-ARIA (`graphics-symbol` a další). Abstraktní role ARIA, jako `landmark` a `sectionhead`, se hlásí: specifikace říká, že existují pro sestavení její ontologie a nesmí se v značkování používat.

`role` může obsahovat několik názvů jako záložní seznam a kontroluje se každý z nich. Hodnota se šablonovou syntaxí je nepoznatelná a zůstává bez povšimnutí, stejně jako vazba zapsaná frameworkem, jako v `:role` nebo `[attr.role]`.

Špatně:

```html
<div role="buton">Save</div>
```

Správně:

```html
<button type="button">Save</button>
```

#### H052

`Meta refresh should not reload or redirect the page on a timer.`

Časované obnovení přesune stránku čtenáři pod rukama. Kdo čte pomalu, používá čtečku obrazovky nebo byl prostě vyrušen, ztratí místo, kde byl, bez varování a bez možnosti tomu zabránit, což nesplňuje WCAG 2.2.1 Nastavitelné časování, a obnovení, které znovu načte stejnou stránku, zahodí vše, co do ní bylo napsáno.

Nulová prodleva je okamžité přesměrování, nikoli časovač, což WCAG povoluje tam, kde nelze použít přesměrování na serveru, a proto se nehlásí. Oba atributy se najdou bez ohledu na to, v jakém pořadí jsou zapsané.

Špatně:

```html
<meta http-equiv="refresh" content="30">
```

Správně:

```html
<meta http-equiv="refresh" content="0; url=/next-page">
```

#### H053

`Id is used more than once in the file.`

Id pojmenovává jeden element. Druhý element se stejným id rozbije `getElementById`, `<label for>`, odkazy na fragmenty i `aria-labelledby`: prohlížeč vezme první a ostatní tiše ignoruje, takže popisek, odkaz nebo skript skončí u nesprávného elementu bez jakéhokoli varování.

Dvě id ve vzájemně se vylučujících větvích jednoho `{% if %}...{% else %}...{% endif %}` se nikdy nevykreslí obě, a proto se nehlásí. Cyklus `{% for %}` ani `{% block %}` větví není: id uvnitř něj i stejné id mimo něj se vykreslí obě a hlásí se to pozdější. Hodnota zapsaná šablonovou značkou je nepoznatelná a zůstává bez povšimnutí, stejně jako prázdná hodnota. Id se porovnávají přesně, stejně jako to dělá prohlížeč, takže `save` a `Save` jsou dvě různá id.

Větve se čtou v jazyce, ve kterém je soubor napsaný, a s jakýmikoli prázdnými znaky, které jazyk mezi oddělovači a názvem značky dovoluje: `{% elif %}` a `{% else %}`, `{% elsif %}` a `{% when %}` z liquid, `{{ else }}` z go, řádkový příkaz `% else:` z mako a `{{else}}` z handlebars, jeho řetězené `{{else if x}}` a inverzní sekce libovolného bloku `{{#helper}}`, včetně vlastních helperů. Obsah `<template>` je samostatný fragment dokumentu, ke kterému `getElementById` nikdy nedosáhne, takže id v něm se porovnává jen s id téhož `<template>`: dvě šablony mohou každá obsahovat řádek se stejným id, ale dvě taková id uvnitř jedné šablony se stále hlásí. Id uvnitř komentáře, těla <code>{&#37; raw %}</code> nebo `{% verbatim %}` nebo oblasti `djlint:off` se vůbec nečte.

Špatně:

```html
<button type="submit" id="submit">Save</button>
<button type="submit" id="submit">Save and continue</button>
```

Správně:

```html
<button type="submit" id="submit">Save</button>
<button type="button" id="cancel">Cancel</button>
```

#### H054

`Interactive element should not be nested inside another.`

Html zakazuje interaktivní obsah uvnitř `<a>` a `<button>`. Tlačítko uvnitř odkazu nebo odkaz uvnitř tlačítka je neplatné značkování, které každý prohlížeč opraví po svém, a uživatel čtečky obrazovky nebo klávesnice dostane jeden ovládací prvek, který se chová jako dva. axe hlásí totéž jako „nested-interactive“.

Sledovanými kontejnery jsou `<a>` s `href` a `<button>` a ovládací prvky, které se v nich hlásí, jsou odkaz s `href`, `button`, `input`, `select` a `textarea`. `<a>` bez `href` není interaktivní a zůstává bez povšimnutí na obou stranách, stejně jako skrytý input nebo input, jehož typ zapisuje šablonová značka. Obsah `<template>` se nevykresluje tam, kde je zapsaný, takže ovládací prvek uvnitř něj není vnořený do odkazu kolem něj, ale vnoření zapsané uvnitř šablony se stále hlásí.

Atribut se čte tam, kde ho značka zapisuje, a nikde jinde: `href` v `{% if not href %}` je název proměnné, ten v `{# href="{{ url }}" #}` je zakomentovaný a ten v `data-attr=href` patří k jinému atributu, zatímco `href`, které `{% if %}` zapisuje mezi svými značkami, je atribut jako každý jiný. Odkaz nebo tlačítko, které zůstanou otevřené, končí s elementem kolem nich, stejně jako v prohlížeči, takže jeden překlep nezpůsobí hlášení ve zbytku souboru; ty, které zůstanou otevřené na nejvyšší úrovni, nemají kolem sebe nic, co by je ukončilo, a sahají až na konec souboru, kde H025 navíc nahlásí osiřelou značku.

Špatně:

```html
<a href="/cart"><button>Add</button></a>
```

Správně:

```html
<a href="/cart" class="button">Add</a>
```

#### H055

`Lang attribute should be a language tag such as en or pt-BR.`

H005 vyžaduje `lang` na `<html>`, ale hodnota jako `lang="english"` nebo `lang="en_US"` ho splní, přestože neoznačuje žádný jazyk, který by prohlížeč znal. Čtečka obrazovky se pak vrátí ke svému výchozímu hlasu a překlad i dělení slov použijí nesprávná pravidla, nebo žádná. Hodnota musí být jazyková značka BCP 47: dvě nebo tři písmena a za nimi libovolný počet podznaček o jednom až osmi písmenech nebo číslicích, každá za spojovníkem, jako v `en`, `pt-BR` nebo `zh-Hant-TW`.

Kontroluje se jen značka `<html>`, stejně jako u H005. Prázdná hodnota se ponechává tomuto pravidlu, kdežto hodnota složená jen z prázdných znaků se hlásí zde, protože H005 ji čte jako hodnotu. Hodnota zapsaná šablonovou značkou, jako v `lang="{{ LANGUAGE_CODE }}"`, nebo zkráceným echem php, jako v `lang="<?= $lang ?>"`, je nepoznatelná a zůstává bez povšimnutí, ale hodnota, která jen začíná znakem `$` nebo `{`, jako v `lang="$LANG"`, se čte tak, jak je zapsaná. `xml:lang` ani `data-lang` se nečte jako `lang` a `>` zapsané uvnitř šablonové značky před atributem, jako v `{% if a > b %}`, ho neskryje.

Špatně:

```html
<html lang="english">
```

Správně:

```html
<html lang="en">
```

#### H056

`Src should not be empty.`

Specifikace html říká, že prázdný `src` je neplatný, a varuje, že ho prohlížeč vyhodnotí vůči vlastní URL dokumentu, takže `<img src="">` stáhne stránku znovu jako obrázek a `<script src=""></script>` ji stáhne jako skript. Obvykle jde o zástupnou hodnotu, kterou měl doplnit skript, a řešením je atribut vynechat, nebo hodnotu uchovávat v datovém atributu, dokud nebude skutečná. `src` zapsaný úplně bez hodnoty, jako v `<img src>`, je také prázdný a hlásí se.

Kontrolují se jen `img`, `script`, `iframe`, `embed`, `source`, `track`, `audio` a `video`, protože to jsou elementy, které stahují to, co `src` uvádí. Hlásí se jen hodnota, kterou prohlížeč čte jako prázdnou, takže hodnota bez uvozovek jako `<img src=/static/logo.png>` zůstává bez povšimnutí, stejně jako hodnota složená jen z prázdných znaků a hodnota zapsaná šablonovou značkou, a `srcset` a `data-src` jsou jiné atributy, které pravidlo neposuzuje.

Špatně:

```html
<img src="" alt="Logo">
```

Správně:

```html
<img src="{% static 'logo.png' %}" alt="Logo">
```

#### H057

`Video should have a captions track.`

Video se zvukem nese řeč jen ve zvukové stopě, takže neslyšící nebo nedoslýchavý divák z něj bez titulků nic nemá, a titulky proto vyžaduje WCAG 1.2.2 Titulky (záznam). Pravidlo splňuje `<track>` s `kind` nastaveným na `captions` nebo `subtitles` uvnitř `<video>`, stejně jako `<track>` úplně bez `kind`, protože výchozí hodnotou je `subtitles`.

Video s `muted` nemá žádný zvuk, ke kterému by bylo třeba titulky, a nehlásí se. Nehlásí se ani video, jehož otevírací značka nebo tělo obsahuje šablonovou značku, protože stopy nebo atribut `muted` může zapisovat šablona tam, kde je djLint nevidí. Šablonovou značkou se rozumí značka, kterou otevírá šablonovací jazyk, tedy `{{`, `{%`, `{#` nebo `${`, takže obslužná rutina jQuery jako `onclick="$(this).play()"`, `$refs` z Alpine, složená závorka css a cena uvedená v záložním textu jsou obyčejný text, jak se zdají, a video se stále čte.

Za značkování se považuje jen značkování. `muted` musí být atribut, takže `<video class=muted>` je třída pojmenovaná muted a hlásí se, a `<track>`, který je zakomentovaný nebo zapsaný uvnitř hodnoty atributu, je text, nikoli stopa. `</video>` uvnitř hodnoty nic neukončuje a element se posuzuje tam, kde ho uzavírá jeho skutečná koncová značka, takže `<video>` ponechaný otevřený se nechává na `H025`.

Špatně:

```html
<video controls src="talk.mp4"></video>
```

Správně:

```html
<video controls src="talk.mp4">
  <track kind="captions" src="talk.vtt" srclang="en">
</video>
```

<!-- oxfmt-ignore-end -->

### Přidávání pravidel

Pull requesty s novými pravidly vítáme!

Dobré pravidlo se skládá z těchto částí:

- Název
- Kód
- Zpráva – zpráva, která se zobrazí při nalezení chyby.
- Příznaky – příznaky regulárního výrazu. Výchozí je re.DOTALL. Např.: re.I|re.M
- Vzory – regulární výrazy, které chybu najdou.
- Vyloučení – volitelný seznam profilů, ze kterých se má pravidlo vyloučit.

K pravidlu prosím přidejte test, který ho ověří.

## Vlastní pravidla

Vlastní pravidla jen pro svůj projekt můžete přidat tak, že vedle souboru `pyproject.toml` vytvoříte soubor `.djlint_rules.yaml`. Pravidla přidaná do tohoto souboru djLint načte. Soubor pravidel v jiném umístění lze zadat možností příkazového řádku `--rules`.

### Pravidla se vzory

Můžete přidat pravidla, která selžou, pokud některý z regulárních výrazů najde shodu:

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Pravidla s modulem Pythonu

Můžete přidat pravidla, která importují a spustí vlastní funkci v Pythonu:

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

Zadaný `python_module` musí obsahovat funkci `run()`, která se spustí pro každý kontrolovaný soubor. Musí přijímat tyto argumenty:

- `rule`: Slovník, který představuje vaše pravidlo v `.djlint_rules.yaml`. Obvykle tuto proměnnou použijete k získání názvu a zprávy pravidla.
- `config`: Objekt konfigurace djLint.
- `html`: Celý html obsah souboru.
- `filepath`: Cesta k právě kontrolovanému souboru.
- `line_ends`: Seznam pozic znaků `start` a `end` jednotlivých řádků, který můžete použít s `djlint.lint.get_line()` k získání čísla řádku z pozice znaku. Viz příklad.
- `*args, **kwargs`: V budoucnu můžeme přidat další argumenty, proto byste tyto dva argumenty měli uvést, abyste snížili riziko selhání po aktualizaci djLint.

Modul může být v kořeni projektu. Pokud vrátí `line` nebo `end`, které není pozicí, djLint skončí s chybou, která uvádí název pravidla.

Musí vracet seznam slovníků, jeden pro každou chybu, s těmito klíči:

- `code`: Kódové označení pravidla, které chybu hlásí (obvykle `rule['name']`)
- `line`: Číslo řádku a číslo znaku na tomto řádku oddělené znakem „:“, jako řetězec.
  Například `"2:3"` znamená, že chyba byla nalezena na řádku 2, znak 3
- `end`: Volitelné. Kde chyba končí, zapsané stejně jako `line`, hned za jejím posledním znakem. Bez něj chyba končí tam, kde končí `match`.
- `match`: Část obsahu, která chybu obsahuje
- `message`: Zpráva, která se vypíše k ohlášení chyby (obvykle `rule['message']`)

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
    """Pravidlo, které selže, pokud soubor html obsahuje 'bad'.

    Je to jen příklad, ve skutečnosti je mnohem jednodušší to udělat
    „pravidlem se vzory“.
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
