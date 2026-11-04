---
description: Le regole del linter di template HTML di djLint e come aggiungerne di tue.
title: Regole del linter
keywords: linter per template, formattatore per template, djLint, HTML, template, formattatore, linter, regole
---

# Uso del linter

djLint include molte regole per verificare lo stile e la validità dei tuoi template. Sfrutta al meglio il linter configurandolo per usare un profilo predefinito per il linguaggio di template che preferisci.

```bash
djlint /path/to/templates --lint

# con estensioni personalizzate
djlint /path/to/templates -e html.dj --profile=django

# oppure su un singolo file
djlint /path/to/this.html.j2  --profile=jinja
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Consulta la guida alla configurazione per conoscere tutte le opzioni!</a></div>
</div>

## Attivare o disattivare le regole

La maggior parte delle regole è attiva per impostazione predefinita. Le regole si possono disattivare dalla riga di comando con il flag `--ignore`. Le regole si possono attivare con il flag `--include`.

Ad esempio:

```bash
djlint . --lint --include=H006,H017 --ignore=H013,H015
```

Si può fare anche tramite il file di [{{ "configuration" | i18n }}]({{ "lang_code_url" | i18n }}/docs/configuration).

## Regole

| Codice | Significato                                                                                                       | Predefinita |
| ------ | ----------------------------------------------------------------------------------------------------------------- | ----------- |
| T001   | Le variabili devono essere racchiuse tra spazi. Es.: {% raw %}`{{ this }}`{% endraw %}                            | ✔️          |
| T002   | Nei tag vanno usate le virgolette doppie. Es. {% raw %}`{% extends "this.html" %}`{% endraw %}                    | ✔️          |
| T003   | Endblock deve avere un nome. Es.: {% raw %}`{% endblock body %}`{% endraw %}.                                     | -           |
| D004   | (Django) Gli URL statici devono seguire lo schema {% raw %}`{% static path/to/file %}`{% endraw %}.               | ✔️          |
| J004   | (Jinja) Gli URL statici devono seguire lo schema {% raw %}`{{ url_for('static'..) }}`{% endraw %}.                | ✔️          |
| H005   | Il tag html deve avere un attributo `lang` non vuoto.                                                             | ✔️          |
| H006   | Il tag `img` deve avere gli attributi `height` e `width`.                                                         | -           |
| H007   | `<!DOCTYPE ... >` deve essere presente prima del tag html.                                                        | ✔️          |
| H008   | Gli attributi devono essere tra virgolette doppie.                                                                | ✔️          |
| H009   | I nomi dei tag devono essere in minuscolo.                                                                        | ✔️          |
| H010   | I nomi degli attributi devono essere in minuscolo.                                                                | ✔️          |
| H011   | I valori degli attributi devono essere tra virgolette.                                                            | ✔️          |
| H012   | Non devono esserci spazi attorno al `=` degli attributi.                                                          | ✔️          |
| H013   | Il tag `img` deve avere attributi alt.                                                                            | ✔️          |
| H014   | Più righe vuote di quante ne mantenga la configurazione.                                                          | ✔️          |
| H015   | Fai seguire i tag `h` da un a capo.                                                                               | ✔️          |
| H016   | Tag `title` mancante nell'html.                                                                                   | ✔️          |
| H017   | I tag void devono essere autochiudenti (in conflitto con: H018).                                                  | -           |
| D018   | (Django) I link interni devono usare lo schema {% raw %}`{% url ... %}`{% endraw %}.                              | ✔️          |
| H018   | I tag void sono autochiudenti per natura e devono terminare con ">", non con "/>" (in conflitto con: H017).       | -           |
| J018   | (Jinja) I link interni devono usare lo schema {% raw %}`{{ url_for() ... }}`{% endraw %}.                         | ✔️          |
| H019   | Sostituisci `javascript:abc()` con un evento `on_` e un URL reale.                                                | ✔️          |
| H020   | Trovata una coppia di tag vuota. Valuta di rimuoverla.                                                            | ✔️          |
| H021   | Evita gli stili inline.                                                                                           | ✔️          |
| H022   | Usa HTTPS per i link esterni.                                                                                     | ✔️          |
| H023   | Non usare riferimenti a entità.                                                                                   | ✔️          |
| H024   | Ometti type negli script e negli stili.                                                                           | ✔️          |
| H025   | Il tag sembra orfano.                                                                                             | ✔️          |
| H026   | I tag id e class vuoti si possono rimuovere.                                                                      | ✔️          |
| T027   | Trovata una stringa non chiusa nella sintassi del template.                                                       | ✔️          |
| T028   | Valuta di usare tag senza spazi nei valori degli attributi. {% raw %}`{%- if/for -%}`{% endraw %}                 | -           |
| H029   | Valuta di usare valori in minuscolo per il method dei form.                                                       | ✔️          |
| H030   | Valuta di aggiungere una meta description.                                                                        | ✔️          |
| T032   | Trovati spazi in eccesso nei tag di template.                                                                     | ✔️          |
| H033   | Trovati spazi in eccesso nell'action del form.                                                                    | ✔️          |
| T034   | Intendevi usare {% raw %}{% ... %} invece di {% ... }%? {% endraw %}                                              | ✔️          |
| H036   | Non usare tag `br` per la spaziatura.                                                                             | ✔️          |
| H037   | Trovato un attributo duplicato.                                                                                   | ✔️          |
| T038   | Il tag di blocco non ha un tag di chiusura corrispondente.                                                        | ✔️          |
| T039   | Trovato un tag di template non chiuso.                                                                            | ✔️          |
| T040   | Nome del template mancante o vuoto nel tag extends o include.                                                     | ✔️          |
| H041   | Il tag viene chiuso in un blocco di template diverso da quello in cui è stato aperto.                             | ✔️          |
| T041   | Il tag extends deve essere il primo tag del template.                                                             | ✔️          |
| H042   | L'attributo for della label non ha un id di elemento corrispondente in questo file.                               | ✔️          |
| T042   | Il contenuto al di fuori di un blocco non viene renderizzato in un template che ne estende un altro.              | ✔️          |
| H043   | Il tag button deve avere un attributo `type`.                                                                     | ✔️          |
| T043   | Il nome del blocco è usato più di una volta nel template.                                                         | ✔️          |
| H044   | Thead non deve mescolare celle `th` e `td`.                                                                       | ✔️          |
| T044   | Il tag di output contiene una parola chiave di istruzione; usa un tag di blocco.                                  | ✔️          |
| H045   | Il tag iframe deve avere un attributo `title`.                                                                    | ✔️          |
| T045   | Un tag di template dentro un commento html viene comunque eseguito; usa un commento di template per disattivarlo. | ✔️          |
| H046   | Tabindex non deve essere positivo.                                                                                | ✔️          |
| H047   | Aria-hidden non deve essere impostato su un elemento focalizzabile.                                               | ✔️          |
| H048   | L'attributo aria non è tra quelli definiti dalla specifica.                                                       | ✔️          |
| H049   | Il viewport non deve impedire lo zoom della pagina.                                                               | ✔️          |
| H050   | L'elemento è obsoleto e va sostituito.                                                                            | ✔️          |
| H051   | Il ruolo non è tra quelli che ARIA definisce per il markup.                                                       | ✔️          |
| H052   | Il meta refresh non deve ricaricare o reindirizzare la pagina a tempo.                                            | ✔️          |
| H053   | L'id è usato più di una volta nel file.                                                                           | ✔️          |
| H054   | Un elemento interattivo non deve essere annidato in un altro.                                                     | ✔️          |
| H055   | L'attributo lang deve essere un tag di lingua, come en o pt-BR.                                                   | ✔️          |
| H056   | Src non deve essere vuoto.                                                                                        | ✔️          |
| H057   | Il video deve avere una traccia di sottotitoli.                                                                   | ✔️          |

### Schema dei codici

La prima lettera di un codice segue questo schema:

::: content

- D: si applica specificamente a Django
- H: si applica all'html
- J: si applica specificamente a Jinja
- M: si applica specificamente a Handlebars
- N: si applica specificamente a Nunjucks
- T: si applica in generale ai template
:::

### Dettagli delle regole

<!-- oxfmt-ignore-start -->

{% raw %}

#### T001

`Variables should be wrapped in a whitespace.`

Una sintassi di template come `{{user.name}}` senza spazi interni è più difficile da scorrere e da confrontare nei diff, e una spaziatura incoerente nel codice rende inaffidabili i refactoring basati su grep (la ricerca di una variabile o di un tag), perché la stessa espressione esiste in più grafie. Le guide di stile di Django e di Jinja scrivono entrambe `{{ var }}` e `{% tag %}` con un singolo spazio.

Non si applica ai profili handlebars e golang.

Da evitare:

```html
{{user.name}}
```

Da preferire:

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

Mescolare virgolette singole e doppie nei tag di template (`{% extends %}`, `{% include %}`, `{% with %}`, `{% trans %}`, `{% now %}`) fa comparire lo stesso nome di template in due grafie, così le ricerche e le rinomine in blocco perdono metà delle occorrenze. Uniformare tutto sulle virgolette doppie mantiene gli argomenti dei tag coerenti con le virgolette degli attributi HTML nel resto del file.

Le virgolette singole all'interno dei valori degli attributi HTML (ad es. `<span title="{% trans 'x' %}">`) non vengono segnalate, perché lì le virgolette doppie dell'attributo impongono quelle singole.

Con `quote_style = "single"` la regola richiede invece le virgolette singole, e il formattatore scrive quelle.

`--reformat` riscrive queste virgolette al posto tuo.

Da evitare:

```html
{% extends 'base.html' %}
```

Da preferire:

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

Quando un `{% block %}` si estende su molte righe o i blocchi sono annidati, un `{% endblock %}` senza nome non dà alcun indizio su quale blocco chiuda, quindi durante la modifica è facile chiudere quello sbagliato; i template figli finiscono poi per sovrascrivere il contenuto sbagliato. Dare un nome all'endblock documenta l'abbinamento e permette sia a djLint sia a Django (che solleva TemplateSyntaxError quando il nome dell'endblock non corrisponde) di intercettare un blocco chiuso nel punto sbagliato. Gli errori di abbinamento (blocchi non chiusi, endblock orfani e nomi non corrispondenti) sono controlli di correttezza gestiti da T038.

Disattivata per impostazione predefinita; attivala con `--include=T003`. `--name-endblocks` scrive il nome al posto tuo.

Il nome non è richiesto quando il blocco si apre e si chiude sulla stessa riga, ad es. `{% block title %}``{% endblock %}`. Il formattatore sposta su righe proprie il contenuto di un blocco che contiene altri tag, quindi un blocco scritto su una riga può aver bisogno di un nome una volta formattato; con `--name-endblocks` il formattatore scrive anche quel nome.

Da evitare:

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

Da preferire:

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Static urls should follow {% static path/to/file %} pattern.`

Scrivere a mano i percorsi /static/ aggira il tag `{% static %}` di Django, quindi i template si rompono quando cambia STATIC_URL (ad es. spostando gli asset su una CDN o con un deployment in un sottopercorso) e non usano mai i nomi di file con hash di ManifestStaticFilesStorage, causando errori 404 o asset obsoleti in cache in produzione. La regola cerca il prefisso letterale `/static/`, quindi un progetto che serve i propri file statici da un altro percorso non è coperto.

Da evitare:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Da preferire:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

Scrivere a mano i percorsi /static/ aggira url_for('static', ...) di Flask/Jinja, quindi gli asset danno 404 quando l'app è montata sotto un prefisso URL o quando cambiano la cartella o l'host dei file statici, e si perdono le query string di cache busting aggiunte dal framework. La regola cerca il prefisso letterale `/static/`, quindi un progetto che serve i propri file statici da un altro percorso non è coperto.

Da evitare:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Da preferire:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have a non-empty lang attribute.`

Senza un attributo lang su `<html>`, gli screen reader tirano a indovinare le regole di pronuncia e possono leggere la pagina nella lingua sbagliata, e i browser non possono offrire correttamente traduzione, sillabazione o virgolette adatte alla lingua. Dichiarare la lingua della pagina è il criterio di successo 3.1.1 delle WCAG 2.1 (livello A).

`lang=""` e un `lang` senza valore dicono entrambi che la lingua è sconosciuta, quindi vengono segnalati come un attributo mancante.

Da evitare:

```html
<!DOCTYPE html>
<html>
</html>
```

Da preferire:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`Img tag should have height and width attributes.`

Disattivata per impostazione predefinita; attivala con `--include=H006`.

Quando un `<img>` non ha larghezza e altezza, il browser non può riservare lo spazio prima che l'immagine venga scaricata, quindi il contenuto circostante salta mentre le immagini si caricano. Questo spostamento del layout peggiora il Cumulative Layout Shift (una metrica dei Core Web Vitals) e può far cliccare gli utenti nel punto sbagliato mentre la pagina si assesta.

Da evitare:

```html
<img src="cat.png" alt="Cat">
```

Da preferire:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

Senza un `<!DOCTYPE>` prima del tag `<html>`, i browser renderizzano la pagina in quirks mode, emulando il vecchio comportamento del box model e del layout, quindi il CSS viene reso in modo incoerente tra un browser e l'altro. Tag di template e commenti prima del doctype vanno bene; solo il tag `<html>` stesso deve esserne preceduto.

Da evitare:

```html
<html lang="en">
</html>
```

Da preferire:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Attributes should be double quoted.`

Stili di virgolette misti rendono i valori degli attributi più difficili da scorrere e da cercare con grep, e i valori tra virgolette singole si rompono non appena il contenuto contiene un apostrofo. Le virgolette doppie sono la convenzione usata dalle specifiche HTML, dai formattatori e dalla maggior parte delle guide di stile, quindi uniformare tutto su di esse mantiene i template coerenti con il resto dell'ecosistema.

Da evitare:

```html
<div class='content'></div>
```

Da preferire:

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

I parser HTML accettano nomi di tag in maiuscolo, ma le serializzazioni XHTML e XML distinguono tra maiuscole e minuscole e li rifiutano, e un uso misto rende inaffidabili la ricerca testuale e la revisione dei diff (cercare `<h1>` con grep non trova `<H1>`). I nomi di tag in minuscolo mantengono i template portabili e coerenti.

Non viene segnalata con `--ignore-case`, che dice al formattatore di non toccare maiuscole e minuscole.

Da evitare:

```html
<H1>Welcome</H1>
```

Da preferire:

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

I nomi di attributo in maiuscolo non sono validi nelle serializzazioni XHTML/XML e vanificano la ricerca testuale nei template (cercare src= con grep non trova SRC=). Il DOM normalizza comunque in minuscolo i nomi degli attributi HTML, quindi le grafie in maiuscolo aggiungono incoerenza senza alcun vantaggio. Vengono segnalati solo i nomi che il formattatore converte in minuscolo: `class`, `id`, `src`, `width`, `height`, `alt`, `style`, `lang`, `title`, `media` e `srcset`. `--reformat` li corregge al posto tuo, e un binding di un framework come `:itemID` o un nome più lungo come `data-ID` mantiene le sue maiuscole.

Non viene segnalata con `--ignore-case`, che dice al formattatore di non toccare maiuscole e minuscole.

Da evitare:

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

Da preferire:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

I valori di attributo senza virgolette terminano al primo spazio, quindi un valore come class=btn primary perde silenziosamente tutto ciò che segue lo spazio (il browser tratta "primary" come un attributo booleano separato). I valori che provengono da variabili di template sono particolarmente fragili: qualsiasi spazio, "=" o ">" renderizzato corrompe il tag. Le virgolette rendono esplicito e sicuro il confine del valore.

Da evitare:

```html
<div class=test></div>
```

Da preferire:

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

L'HTML ammette spazi attorno a "=", quindi questa è una regola di stile. Scrivere name="value" senza spazi è lo stile abituale, ed è ciò che presuppongono i semplici strumenti testuali come grep o cerca e sostituisci, quindi una spaziatura mista rende gli attributi più difficili da trovare e da rifattorizzare. `--reformat` rimuove gli spazi al posto tuo.

Da evitare:

```html
<div class = "test"></div>
```

Da preferire:

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

Senza un attributo alt, gli screen reader annunciano il nome del file dell'immagine o niente del tutto, violando il criterio WCAG 1.1.1 (Contenuti non testuali). Il testo alternativo è anche ciò che gli utenti vedono quando l'immagine non si carica. Le immagini decorative dovrebbero avere un alt="" esplicitamente vuoto, così le tecnologie assistive sanno di doverle saltare; anche questo soddisfa la regola.

Un `alt` senza valore equivale a `alt=""`, il caso dell'immagine decorativa, quindi è accettato.

Da evitare:

```html
<img src="cat.jpg" height="200" width="300">
```

Da preferire:

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

Le sequenze di righe vuote non hanno effetto sulla pagina renderizzata (l'HTML comprime gli spazi bianchi) ma appesantiscono i template e creano diff rumorosi quando cambiano le righe vicine. Il formattatore di djLint le rimuove del tutto per impostazione predefinita (mantenendo al massimo `max_blank_lines` righe vuote, che per impostazione predefinita vale 0), quindi le sequenze rimaste indicano codice non formattato.

Da evitare:

```html
<div>one</div>


<p>two</p>
```

Da preferire:

```html
<div>one</div>

<p>two</p>
```

#### H015

`Follow h tags with a line break.`

I titoli sono punti di riferimento a livello di blocco che definiscono la struttura del documento; stipare l'elemento successivo sulla stessa riga del tag h di chiusura nasconde quella struttura nel sorgente e fa sì che le modifiche a uno dei due elementi compaiano nei diff come modifiche a entrambi. Un a capo dopo ogni titolo mantiene la struttura visiva del template allineata con quella renderizzata.

Da evitare:

```html
<h1>Heading</h1><p>Intro text.</p>
```

Da preferire:

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Missing title tag in html.`

La specifica HTML richiede un elemento title in ogni documento. Senza, le schede del browser, i segnalibri e la cronologia mostrano un URL grezzo invece del nome della pagina, i motori di ricerca perdono l'etichetta principale della pagina e chi usa uno screen reader perde la prima cosa annunciata al caricamento, violando il criterio WCAG 2.4.2 (Titolazione della pagina, livello A).

Si attiva solo sui file che contengono un documento `<html>`...`</html>` completo, quindi i partial e i template figli che estendono una base non vengono mai segnalati. Le shell SPA che impostano il titolo lato client hanno comunque bisogno di un `<title>` statico: è ciò che compare al primo paint, nei crawler e quando JavaScript non funziona.

Da evitare:

```html
<html lang="en">
<body>Content</body>
</html>
```

Da preferire:

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

I template che devono essere interpretabili anche come XML/XHTML (o alimentare strumenti basati su XML) rifiutano gli elementi void scritti senza la barra di chiusura, e mescolare `<br>` e `<br />` nel codice produce diff incoerenti. Questa regola impone la convenzione in stile XHTML, così ogni elemento void viene chiuso allo stesso modo.

Disattivata per impostazione predefinita; attivala con `--include=H017`. Si esclude a vicenda con H018; attiva solo una delle due convenzioni. `--close-void-tags` aggiunge la barra ai tag void html al posto tuo. Un `<path>` svg resta com'è scritto, quindi chiudilo a mano.

Da evitare:

```html
<br>
<meta charset="utf-8">
```

Da preferire:

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Internal links should use the {% url ... %} pattern.`

Gli URL interni scritti a mano diventano silenziosamente obsoleti quando il percorso di una route cambia in urls.py, producendo link rotti e action di form non funzionanti che nessun test sull'URLconf rileverà. `{% url %}` risolve il percorso a partire dal nome della route, quindi rinominare un percorso aggiorna tutti i link in un colpo solo.

Da evitare:

```html
<a href="/accounts/login">Login</a>
```

Da preferire:

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

Nell'HTML living standard la barra finale su un elemento void non ha alcun significato (il parser la ignora), quindi scrivere `<br />` suggerisce un comportamento di autochiusura in stile XML che l'HTML non ha e può indurre chi legge ad aggiungere barre ai tag non void, dove una / di troppo viene scartata silenziosamente e maschera bug di tag non chiusi. Questa regola impone terminazioni semplici con > sugli elementi void.

Disattivata per impostazione predefinita; attivala con `--include=H018`. Si esclude a vicenda con H017; attiva solo una delle due convenzioni. `<path />` in SVG è esente, perché SVG è XML e richiede la barra. Non viene segnalata con `--close-void-tags`, perché in quel caso il formattatore scrive proprio la barra che questa regola segnala.

Da evitare:

```html
<br />
<meta charset="utf-8" />
```

Da preferire:

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

Gli URL interni scritti a mano si rompono silenziosamente quando il percorso di una route cambia o l'app viene montata sotto un prefisso, lasciando link morti e action di form che inviano a pagine 404. url_for() costruisce l'URL a partire dal nome dell'endpoint, quindi le modifiche alle route si propagano automaticamente a ogni template.

Da evitare:

```html
<a href="/accounts/login">Login</a>
```

Da preferire:

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

Gli URL javascript: rompono il clic centrale e l'apertura in una nuova scheda, non fanno nulla quando JavaScript è disattivato o non si carica, vengono bloccati dalle Content Security Policy restrittive e sono un classico punto di iniezione XSS. Usa invece un URL reale per l'href e collega il comportamento con un gestore di eventi. Con una CSP restrittiva anche i gestori inline on* vengono bloccati: l'onclick mostrato è la correzione minima all'interno del template; è preferibile collegare il listener con addEventListener da un file di script.

Da evitare:

```html
<a href="javascript:openPopup()">Open popup</a>
```

Da preferire:

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

Una coppia di tag vuota non renderizza alcun contenuto ma crea comunque un nodo DOM che può ricevere margini, bordi o gap flex/grid dai fogli di stile, producendo spaziature fantasma difficili da rintracciare; di solito è markup rimasto da una modifica precedente. I tag che sono legittimamente vuoti nel markup normale (td, th, li, dt, dd, slot) sono esenti. Non vengono segnalati nemmeno i tag con un qualsiasi attributo (punti di montaggio JS come `<div id="app">``</div>`, elementi di icon font come `<i class="fa fa-user">``</i>`); corrispondono solo le coppie vuote del tutto prive di attributi.

Da evitare:

```html
<p>Saved.</p>
<span> </span>
```

Da preferire:

```html
<p>Saved.</p>
```

#### H021

`Inline styles should be avoided.`

Gli stili inline hanno una specificità maggiore di qualsiasi selettore di un foglio di stile, quindi sovrascriverli in seguito richiede !important; vengono bloccati dalle Content Security Policy che non hanno 'unsafe-inline' in style-src; e disperdono la presentazione nei template, così un cambio di tema o di design costringe a modificare il markup invece di un unico foglio di stile. Sposta la dichiarazione in una classe CSS. Un'eccezione legittima: i template di email HTML, dove molti client di posta eliminano i blocchi `<style>` e gli stili inline sono la tecnica standard; escludi le directory dei template email o disattiva questa regola per loro.

Da evitare:

```html
<div style="color: red;">Wrong username or password.</div>
```

Da preferire:

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

Le sottorisorse in semplice http:// su una pagina servita via HTTPS sono contenuti misti: i browser bloccano del tutto script, fogli di stile e iframe, e per le immagini passano automaticamente a HTTPS o mostrano un avviso. Un link `<a>` a una pagina http:// non è contenuto misto, ma manda comunque i visitatori su una connessione non cifrata, esposta a intercettazioni e manomissioni. Verranno segnalati anche i riferimenti a host interni che davvero non hanno TLS; silenzia quei punti con un blocco `{# djlint:off H022 #}` anziché disattivare la regola.

Da evitare:

```html
<a href="http://example.com">Example</a>
```

Da preferire:

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

I documenti HTML5 sono in UTF-8, quindi il carattere letterale funziona ovunque ed è ciò che chi revisiona legge davvero; un refuso in un riferimento a entità (ad es. `&mdsah;`) non viene rilevato dal browser e compare così com'è come testo rotto. djLint ammette le entità che hanno un ruolo sintattico (`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;`, e le parentesi graffe `&lbrace;` e `&rbrace;` insieme a `&percnt;`, `&num;` e `&dollar;`, che scritte per esteso completerebbero un delimitatore di template) e quelle che indicano un carattere invisibile, che quindi non si può revisionare come letterale: gli spazi (`&nbsp;`, `&thinsp;`, `&hairsp;`), i joiner e i marcatori (`&zwnj;`, `&zwj;`, `&lrm;`, `&rlm;`) e `&shy;`, in forma nominale, decimale ed esadecimale allo stesso modo.

`--reformat` riscrive l'entità come carattere al posto tuo. Un'entità scritta all'interno di un tag di template fa parte del tag e non della pagina, quindi né la regola né il formattatore la toccano. `--no-entity-formatting` disattiva la riscrittura ma lascia attiva la regola, quindi un'entità viene comunque segnalata. Aggiungi `H023` a `ignore` per mantenere le entità.

Da evitare:

```html
<p>Dates 1900 &mdash; 2000</p>
```

Da preferire:

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript e text/css sono i valori predefiniti di HTML5 per `<script>` e `<style>`, quindi l'attributo è un peso morto che il browser ignora; la specifica WHATWG dice esplicitamente di ometterlo. Toglierlo evita anche stringhe MIME obsolete che rompono l'elemento quando vengono copiate su script modulo (dove type="module" conta davvero).

Da evitare:

```html
<script type="text/javascript" src="app.js">
```

Da preferire:

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

Un tag senza il corrispondente tag di apertura o di chiusura costringe il meccanismo di recupero dagli errori del browser a indovinare dove termina l'elemento, quindi il markup successivo viene inglobato nell'elemento sbagliato; layout, selettori CSS e query DOM in JavaScript si rompono allora silenziosamente, e in modo diverso da un browser all'altro. H025 segnala anche un `<ol>` o un `<ul>` aperto dentro un `<p>`: il parser HTML chiude il paragrafo prima della lista, quindi il markup non viene mai annidato come è scritto.

Da evitare:

```html
<div>
  <p>Hello</p>
```

Da preferire:

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Empty id and class tags can be removed.`

Nessun selettore di classe o di id corrisponde a un attributo vuoto, e un id vuoto è HTML non valido (il valore dell'id non deve essere la stringa vuota). Un selettore di presenza dell'attributo come `div[class]` invece lo seleziona comunque, quindi rimuoverne uno ha effetto su un foglio di stile scritto in quel modo. Di solito indica un bug del template in cui doveva essere interpolata una variabile, quindi rimuoverlo o riempirlo evita che quel bug resti nascosto in piena vista.

Da evitare:

```html
<div id="" class="">content</div>
```

Da preferire:

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

Una virgoletta aperta ma mai chiusa dentro `{% ... %}` o `{{ ... }}` fa sì che il motore di template interpreti male il tag: Django e Jinja sollevano un TemplateSyntaxError al momento del rendering oppure inglobano silenziosamente il resto degli argomenti del tag come contenuto della stringa, quindi la pagina dà un errore 500 o viene renderizzata con argomenti mancanti.

Da evitare:

```html
{% trans "Welcome %}
```

Da preferire:

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

Disattivata per impostazione predefinita; attivala con `--include=T028`.

Gli spazi che un tag senza spazi elimina sono spazi che vengono renderizzati, quindi applicala solo dove l'attributo non ha spazi da perdere. `alt="{%- if brand -%}Acme{%- endif -%} logo"` viene renderizzato come `Acmelogo`, e in un svg `d="M12 {%- if big -%}20{%- endif -%} 4Z"` diventa un tracciato diverso. Per questo la regola va attivata esplicitamente.

I tag di template all'interno del valore di un attributo emettono nell'attributo renderizzato gli spazi e gli a capo che li circondano, quindi un href o un src costruito con semplici tag `{% if %}`/`{% for %}` può contenere spazi indesiderati e produrre URL non validi. I tag di controllo degli spazi di Jinja/Nunjucks (`{%- ... -%}`) eliminano quegli spazi circostanti, così l'attributo viene renderizzato come un unico valore pulito. L'attributo class è esente, perché gli spazi in più tra i nomi delle classi sono innocui.

Non si applica al profilo django: i tag di template di Django non supportano il controllo degli spazi `{%- -%}`.

Da evitare:

```html
<a href="{% if x %}/home{% endif %}"></a>
```

Da preferire:

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

La specifica HTML definisce in minuscolo le parole chiave del method dei form (get, post); i browser accettano le varianti in maiuscolo solo grazie a un confronto di ripiego che non distingue maiuscole e minuscole. Mantenere la forma canonica in minuscolo rende i template coerenti e facili da cercare con grep, ed evita le lamentele dei validatori rigorosi e delle toolchain basate su XHTML.

Da evitare:

```html
<form method="POST"></form>
```

Da preferire:

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

I motori di ricerca usano la meta description come snippet sotto il titolo della pagina nei risultati; senza, ne compongono uno a partire da testo arbitrario della pagina, il che riduce la percentuale di clic e produce anteprime scadenti dei link quando la pagina viene condivisa.

Si attiva solo sui file che contengono un documento `<html>`...`</html>` completo. Il discorso dello snippet vale per le pagine indicizzate pubblicamente; per le app protette da autenticazione o intranet questa regola viene comunemente disattivata.

Da evitare:

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

Da preferire:

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

Le sequenze di spazi o tabulazioni tra gli argomenti di un tag di template sono rumore invisibile: nascondono le differenze reali nei diff, possono rendere difficile notare un argomento mancante e si discostano dallo stile a spazio singolo prodotto dal formattatore di djLint, causando riformattazioni inutili. Gli spazi all'interno delle stringhe tra virgolette vengono preservati e non segnalati.

Da evitare:

```html
{% static  'css/style.css' %}
```

Da preferire:

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

Gli spazi iniziali o finali nel valore action di un form diventano parte dell'URL renderizzato. I browser li rimuovono durante il parsing, ma i client diversi dai browser e i test che usano il valore letterale potrebbero non farlo, e attorno a un tag `{% url %}` lo spazio di troppo indica quasi sempre un refuso che produce un URL di invio che non corrisponde a nessuna route lato server.

Da evitare:

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

Da preferire:

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Did you intend to use {% ... %} instead of {% ... }%?`

}% è quasi sempre un refuso per %}. Il motore di template non riconosce }% come delimitatore di tag, quindi il tag non viene mai interpretato: il testo grezzo {% ... }% finisce nell'HTML renderizzato, oppure il motore solleva un errore di sintassi quando incontra il tag non chiuso.

Da evitare:

```html
{% include "footer.html" }%
```

Da preferire:

```html
{% include "footer.html" %}
```

#### H036

`Do not use br tags for spacing.`

La specifica html ammette `<br>` solo per un a capo che fa parte del contenuto stesso, come in un indirizzo postale o in una poesia, e quell'uso non viene toccato. Viene segnalato l'uso presentazionale che la specifica esclude: una sequenza di due o più a capo, che è spazio verticale, e un a capo a ridosso del bordo interno di un elemento di blocco, che non produce nulla che il suo stesso margine non produrrebbe. Entrambi impediscono al testo di riadattarsi alle larghezze ridotte, e uno screen reader annuncia un a capo forzato dove non c'è nulla da annunciare.

Da evitare:

```html
<p>Shipping is free.<br><br>Delivery takes 3 days.</p>
```

Da preferire:

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

Gli attributi duplicati sono HTML non valido, e i browser mantengono solo la prima occorrenza scartando silenziosamente le altre, quindi il secondo valore di class o style non ha mai effetto, e questo nasconde bug reali. Il controllo tiene conto dei template: un attributo ripetuto in rami che si escludono a vicenda (`{% if %}`/`{% else %}`) non viene segnalato, perché solo una copia può essere renderizzata.

Da evitare:

```html
<div class="card" id="profile" class="active">...</div>
```

Da preferire:

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

Un tag di blocco come `{% if %}`, `{% for %}` o `{% macro %}` senza il corrispondente tag di chiusura è un TemplateSyntaxError bloccante in Django e Jinja: la pagina non viene renderizzata al momento della richiesta, e questa regola lo intercetta prima del deploy. Segnala anche i tag di chiusura orfani, privi di tag di apertura, e i blocchi intrecciati in modo errato (ad es. `{% if %}``{% for %}``{% endif %}`).

L'abbinamento `{% block %}`/`{% endblock %}` e i nomi di endblock non corrispondenti vengono controllati da questa regola; T003 (disattivata per impostazione predefinita) richiede inoltre un nome su ogni `{% endblock %}` su più righe. Vengono controllati anche i tag di blocco personalizzati registrati tramite custom_blocks, compresa la loro forma autochiudente / %}.

Da evitare:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

Da preferire:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Unclosed template tag found.`

Un tag di template aperto con `{{` o `{%` ma mai chiuso con il corrispondente `}}` o `%}` non viene interpretato come tag: Django/Jinja sollevano un TemplateSyntaxError oppure renderizzano nella pagina le parentesi graffe grezze, e tutto ciò che si trova fino al delimitatore successivo può essere inglobato silenziosamente. Questi refusi (una parentesi graffa mancante, un delimitatore non corrispondente) sfuggono facilmente in revisione, perché il template può comunque essere renderizzato in parte.

Da evitare:

```html
<p>{{ user.name }</p>
```

Da preferire:

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

Un tag `{% extends %}` o `{% include %}` con un nome di template mancante, vuoto o composto solo da spazi non ha nulla da caricare: Django solleva TemplateSyntaxError quando il nome manca del tutto, e TemplateDoesNotExist al momento del rendering quando è vuoto, quindi in produzione la pagina dà un errore 500 anche se il file del template sembra sintatticamente plausibile.

Da evitare:

```html
{% extends "" %}
```

Da preferire:

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

Quando un tag HTML viene aperto in un `{% block %}` ma chiuso in un altro, un template figlio che sovrascrive solo uno di quei blocchi eredita metà dell'elemento, producendo markup sbilanciato nella pagina renderizzata; i browser allora chiudono automaticamente o riannidano gli elementi in modo imprevedibile, rompendo layout e selettori CSS lontano dal template effettivamente modificato. Aprire e chiudere ogni elemento all'interno dello stesso blocco permette di sovrascrivere ogni blocco in modo sicuro e indipendente.

Da evitare:

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

Da preferire:

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

Django si rifiuta di compilare un template in cui un altro tag precede `{% extends %}`, e il testo scritto prima viene renderizzato, quindi finisce nella pagina prima di tutto ciò che produce il template padre. Anche Jinja renderizza quel testo, mentre nunjucks lo scarta, quindi in nessun motore il template fa ciò che sembra fare.

Un commento `{# #}` non renderizza nulla e non conta, e lo stesso vale per qualsiasi cosa all'interno di un blocco `{% comment %}`, <code>{&#37; raw %}</code> o `{% verbatim %}`, con o senza nome, per una regione `{# djlint:off #}` in una qualsiasi delle sue tre grafie e per il front matter yaml. Un commento html invece conta: il motore lo scrive nella pagina prima del doctype del template padre, ed è proprio questa la fuoriuscita di cui si occupa la regola. Contano anche un blocco `{% blocktrans %}`, un blocco `{% filter %}` e un blocco `<?php ?>`, ognuno dei quali viene renderizzato. Viene controllato solo il primo `{% extends %}`; un secondo è un errore a sé. Nei profili jinja e nunjucks un tag di ramificazione che lo precede non conta, perché jinja documenta `{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}` come il modo per scegliere un template padre; django legge il resto del template dentro `{% extends %}` e poi rifiuta `{% endif %}`, quindi in quel profilo un tag di ramificazione conta.

Non si applica ai profili handlebars, golang, liquid e angular.

Da evitare:

```html
{% load static %}
{% extends "base.html" %}
```

Da preferire:

```html
{% extends "base.html" %}
{% load static %}
```

#### H042

`Label for attribute has no matching element id in this file.`

Il controllo viene eseguito solo sui file che può analizzare in modo affidabile: se il file contiene qualcosa che potrebbe renderizzare un id che questo file non mostra mai (un output `{{ ... }}` come il widget di un form, un `{% include %}` o un `{% extends %}`, oppure un tag di template non riconosciuto), la regola resta in silenzio per quel file. Dove viene eseguito, una segnalazione indica un'associazione realmente rotta.

Da evitare:

```html
<label for="email">Email</label>
<input id="username">
```

Da preferire:

```html
<label for="email">Email</label>
<input id="email">
```

#### T042

`Content outside a block is not rendered in a template that extends another.`

Quando un template ne estende un altro, è il padre a decidere cosa viene prodotto e il figlio si limita a riempire i blocchi del padre. Il testo o l'html scritto dopo `{% extends %}` e al di fuori di qualsiasi `{% block %}` viene scartato silenziosamente al momento del rendering, quindi un paragrafo che nel sorgente sembra a posto non arriva mai alla pagina.

Un tag di template in quella posizione viene comunque eseguito, quindi `{% load %}`, `{% set %}` e un `{% if %}` che racchiude un blocco non vengono toccati, così come i commenti `{# #}` e `{% comment %}`, i commenti html, i blocchi <code>{&#37; raw %}</code> e `{% verbatim %}`, e il corpo di un `{% macro %}`, di un `{% set %}` in forma di blocco, di un `{% partialdef %}` o di un `{% addtoblock %}`, che viene catturato anziché prodotto in output. Il testo di un `{% blocktrans %}` viene segnalato, perché un `{% blocktrans %}` non è un `{% block %}`. Viene considerato solo il contenuto dopo il tag extends, e ogni sequenza di contenuto viene segnalata una sola volta, nel punto in cui inizia.

Il motore legge i tag di template prima dell'html, quindi un `{% extends %}` scritto dentro un commento html o un `<pre>` viene comunque eseguito e rende comunque il file un template figlio; solo `{# #}`, `{% comment %}`, <code>{&#37; raw %}</code> e `{% verbatim %}` lo nascondono davvero. Il testo dentro un commento html non raggiunge in ogni caso nessun lettore e non viene segnalato, ma i tag scritti lì vengono comunque letti.

Non si applica ai profili handlebars, golang, liquid e angular.

Da evitare:

```html
{% extends "base.html" %}
<p>This paragraph is never shown.</p>
{% block content %}
<h1>Welcome</h1>
{% endblock %}
```

Da preferire:

```html
{% extends "base.html" %}
{% block content %}
<h1>Welcome</h1>
<p>This paragraph is shown.</p>
{% endblock %}
```

#### H043

`Button tag should have a type attribute.`

Un `<button>` senza `type` ha come valore predefinito `submit`, quindi un pulsante pensato per eseguire uno script invia anche il form che lo contiene e la pagina si ricarica. Indicare esplicitamente il type lo evita.

Da evitare:

```html
<form>
  <button onclick="preview()">Preview</button>
</form>
```

Da preferire:

```html
<form>
  <button type="button" onclick="preview()">Preview</button>
</form>
```

#### T043

`Block name is used more than once in the template.`

Django, Jinja e Nunjucks si rifiutano tutti di interpretare un template che assegna lo stesso nome a due blocchi, quindi la pagina non si carica affatto. Ai motori non importa che i due blocchi si trovino in rami diversi di un `{% if %}`, quindi ogni nome di blocco deve essere unico nell'intero template, che i blocchi siano uno accanto all'altro o uno annidato nell'altro.

Conta solo `{% block %}`: un `{% blocktrans %}` non è un blocco e un `{% endblock name %}` si limita a nominare il blocco che chiude. I nomi vengono confrontati così come sono scritti, perché i motori trattano `Content` e `content` come due blocchi diversi.

Viene saltato solo ciò che il motore stesso non interpreta mai: un commento di template, un blocco `{% comment %}`, il corpo di un <code>{&#37; raw %}</code> o di un `{% verbatim %}` e una regione `djlint:off`. Un blocco scritto dentro un commento html, nel corpo di un `<script>`, `<style>`, `<pre>` o `<textarea>`, o nel corpo di un `{% filter %}` viene comunque contato, perché il motore legge tutti questi contenuti e solleva comunque un errore sul nome duplicato.

Un `{% embed %}` apre un proprio ambito: i blocchi al suo interno riempiono il template incorporato e non questo, quindi due embed dello stesso partial possono scrivere ciascuno `{% block body %}`. Un nome ripetuto all'interno di un singolo embed viene comunque segnalato.

Non si applica ai profili handlebars, golang, liquid e angular.

Da evitare:

```html
{% block content %}{% endblock %}
{% block content %}{% endblock %}
```

Da preferire:

```html
{% block content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

#### H044

`Thead should not mix th and td cells.`

Ogni riga viene valutata a sé, quindi la riga di spiegazione composta da `td` che la specifica html colloca in un `thead` accanto alla riga delle intestazioni non è una mescolanza. Un `td` vuoto all'inizio della riga è la cella d'angolo di una tabella con intestazioni lungo la prima colonna, che è il markup richiesto dal tutorial sull'accessibilità del W3C, quindi viene saltato.

Un `th` e un `td` hanno un significato diverso per uno screen reader e di solito un css diverso, quindi una singola cella fuori posto in una riga di intestazione viene letta come dato e ha uno stile diverso dalle colonne accanto. La mescolanza è html valido, ed è proprio questo che la rende difficile da notare.

Da evitare:

```html
<thead>
  <tr>
    <th>Name</th>
    <td>Size</td>
  </tr>
</thead>
```

Da preferire:

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

Non si applica ai profili golang, handlebars e angular.

Un tag di output stampa un valore, mentre `if`, `for`, `url`, `include` e gli altri sono istruzioni che vanno in un tag di blocco. Django, Jinja e Nunjucks rifiutano tutti `{{ if x }}` con un errore di sintassi, e una parola chiave di chiusura da sola, come `{{ endif }}`, viene letta come una variabile che non renderizza nulla mentre il blocco che doveva chiudere resta aperto, quindi la pagina o non si carica o mostra ciò che la condizione avrebbe dovuto nascondere.

Una parola chiave da sola è un normale nome di variabile, quindi `{{ url }}`, `{{ url|default:"/" }}` e `{{ set.name }}` non vengono segnalati. Viene segnalata solo una parola chiave seguita da un argomento, insieme a una parola chiave di chiusura o di ramificazione da sola, come `{{ endif }}` o `{{ else }}`. Una parola chiave di controllo come `if` o `for` non può iniziare un'espressione, quindi tutto ciò che la segue è un argomento, operatori compresi, e `{{ if -1 > count }}` viene segnalato. Gli altri nomi fungono anche da variabili e funzioni, e lì conta come argomento solo una stringa tra virgolette o una parola, quindi un'espressione che inizia per caso con uno di essi non viene toccata: `{{ url ~ "/x" }}`, `{{ url if url else "#" }}`, `{{ url ? url : '#' }}`, `{{ block ('title') }}`, `{{ block .super }}` e `{{ filter [0] }}` non producono segnalazioni.

Il corpo di un blocco <code>{&#37; raw %}</code> o `{% verbatim %}` è testo e non sintassi di template, e viene saltato, compresa la forma con nome `{% verbatim vueapp %}...{% endverbatim vueapp %}`, quindi un `{{ }}` di Vue o Handlebars protetto in questo modo non viene segnalato. Anche un `{{ }}` scritto all'interno di un argomento tra virgolette di un tag di blocco, come in `{% trans "Write {{ if x }} instead" %}`, è testo che il motore stampa e non viene toccato.

Da evitare:

```html
{{ if user.is_active }}
```

Da preferire:

```html
{% if user.is_active %}
```

#### H045

`Iframe tag should have a title attribute.`

Uno screen reader annuncia un iframe tramite il suo nome accessibile. Senza nome, legge l'url del frame o niente del tutto, e non c'è modo di sapere cosa sia la pagina incorporata prima di entrarci. Le WCAG trattano questo caso al criterio 4.1.2 Nome, ruolo, valore, e sia axe sia html-validate includono questo controllo per impostazione predefinita.

Il nome può provenire da `title`, `aria-label` o `aria-labelledby`, e uno qualsiasi dei tre soddisfa la regola. Conta anche un nome scritto da un tag di template, quindi un frame con un titolo diverso per ogni pagina non viene segnalato.

Da evitare:

```html
<iframe src="/report/"></iframe>
```

Da preferire:

```html
<iframe src="/report/" title="Quarterly report"></iframe>
```

#### T045

`Template tag inside an html comment still runs; use a template comment to disable it.`

Un commento html nasconde il markup al browser, non al motore di template. `<!-- {% include "debug.html" %} -->` renderizza comunque il file, e `<!-- {% if debug %}...{% endif %} -->` viene comunque valutato, in Django, Jinja, Nunjucks, Handlebars e Go allo stesso modo, quindi un tag commentato in questo modo continua a essere eseguito, e ciò che scrive finisce dentro il commento oppure, se contiene `-->`, ne esce. Solo un commento di template, `{# #}` in Django e Jinja, `{{! }}` in Handlebars o `{{/* */}}` in Go, impedisce a un tag di essere eseguito.

Viene segnalato solo un tag di istruzione: `{% %}` nei profili che lo prevedono, una sezione, una chiusura o un partial di handlebars, e una parola chiave di Go come `{{if}}` o `{{end}}`. Un valore stampato in un commento, come in `<!-- built {{ version }} -->`, è un uso intenzionale e non viene toccato, così come un tag dentro un commento di template, un blocco `{% comment %}` o un blocco raw, e un commento condizionale per Internet Explorer, `<!--[if IE]> ... <![endif]-->`, il cui corpo è markup per il browser che nomina.

Una parola chiave di Go da sola è un normale nome di variabile in ogni altro motore, quindi `<!-- period {{ start }} to {{ end }} -->` e `<!-- Template: {{ template }} -->` sono valori in Django, Jinja, Nunjucks, Handlebars e Liquid, e vengono letti come istruzioni solo con `--profile golang`. Una parola chiave con un operando Go, come in `{{ if .X }}` e `{{ template "footer" . }}`, è un'istruzione che nessun altro motore stampa e viene segnalata con qualsiasi profilo. Allo stesso modo `{%` viene letto solo dove il motore lo prevede, quindi è testo con `--profile handlebars` e `--profile golang`, e un'apertura non seguita da alcuna parentesi di chiusura, come in `<!-- battery at 50{% charge -->`, è semplice prosa, come appare. Un commento condizionale è tale solo se è scritto come tale, cioè se si apre con `<!--[if` ed è chiuso dal suo `<![endif]-->`, in maiuscolo o in minuscolo; uno lasciato aperto è il normale commento che il browser vi legge, e i tag al suo interno vengono segnalati.

Da evitare:

```html
<!-- {% include "banner.html" %} -->
```

Da preferire:

```html
{# {% include "banner.html" %} #}
```

#### H046

`Tabindex should not be positive.`

Un `tabindex` positivo porta un elemento in cima all'ordine di tabulazione, davanti a tutto ciò che non ne ha uno. Ne basta uno per riorganizzare l'intera pagina per chi usa la tastiera, e l'ordine deve poi essere mantenuto a mano in ogni template che aggiunge un controllo. Le WCAG trattano questo caso al criterio 2.4.3 Ordine del focus.

`0` inserisce un elemento nell'ordine di tabulazione nella posizione che gli assegna il documento, e `-1` lo toglie, lasciandolo però focalizzabile da script. Nessuno dei due viene segnalato, né un valore scritto da un tag di template, il cui numero qui non è noto.

Da evitare:

```html
<input tabindex="1">
```

Da preferire:

```html
<input tabindex="0">
```

#### H047

`Aria-hidden should not be set on a focusable element.`

`aria-hidden="true"` toglie un elemento dall'albero di accessibilità ma lo lascia nell'ordine di tabulazione, quindi chi usa la tastiera ci arriva comunque e non sente annunciare nulla. Nascondere un'icona decorativa è l'uso normale dell'attributo e non viene segnalato; viene segnalato solo un elemento che riceve il focus di per sé.

Un elemento è considerato focalizzabile quando è un `button`, `select`, `textarea`, `iframe` o `summary`, un `a` o `area` con un `href`, un `input` non nascosto, un `audio` o `video` con `controls`, o qualsiasi elemento con `contenteditable` o con un `tabindex` pari a `0` o superiore. Un controllo `disabled`, o uno con `tabindex="-1"`, è già fuori dall'ordine di tabulazione e non viene toccato.

Da evitare:

```html
<button aria-hidden="true">Close</button>
```

Da preferire:

```html
<button type="button" aria-label="Close"><span aria-hidden="true">x</span></button>
```

#### H048

`Aria attribute is not one the specification defines.`

Un attributo aria scritto male non fa assolutamente nulla. Nessun browser avvisa, nessuno screen reader lo segnala, e il markup conserva l'apparenza di essere stato reso accessibile, così `aria-lable` può restare in un template per anni mentre il controllo che doveva nominare resta senza nome.

I nomi che la regola conosce sono quelli definiti da ARIA. Un binding scritto da un framework non è un semplice nome aria, quindi `:aria-label`, `v-bind:aria-label` e `[attr.aria-label]` non vengono toccati.

Da evitare:

```html
<button type="button" aria-lable="Close">x</button>
```

Da preferire:

```html
<button type="button" aria-label="Close">x</button>
```

#### H049

`Viewport should not stop the page being zoomed.`

`user-scalable=no`, e un `maximum-scale` inferiore a 2, impediscono di ingrandire una pagina su un telefono, che per molte persone è l'unico modo per leggerla. Le WCAG chiedono il 200% al criterio 1.4.4 Ridimensionamento del testo. I browser ignorano sempre più spesso questa restrizione, ma il tag disattiva comunque lo zoom ovunque venga rispettato.

Il nome e il contenuto vengono trovati in qualunque ordine siano scritti.

Da evitare:

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

Da preferire:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### H050

`Element is obsolete and should be replaced.`

`<center>`, `<font>`, `<big>`, `<strike>` e `<tt>` sono stati abbandonati quando il css ha preso in carico la presentazione, e `<marquee>`, `<blink>`, `<nobr>` e `<spacer>` non sono mai stati standard. L'html non ne definisce più nessuno, quindi nulla garantisce come un browser li disponga, e un foglio di stile non può selezionarli come seleziona una classe.

Gli elementi che la regola conosce sono `acronym`, `applet`, `basefont`, `bgsound`, `big`, `blink`, `center`, `dir`, `font`, `frame`, `frameset`, `isindex`, `keygen`, `marquee`, `menuitem`, `nobr`, `noembed`, `noframes`, `plaintext`, `spacer`, `strike`, `tt` e `xmp`. Viene segnalato solo il tag di apertura, così ogni elemento viene nominato una sola volta, e un elemento personalizzato il cui nome inizia semplicemente con uno di essi, come `<font-picker>`, non viene toccato.

Da evitare:

```html
<center><font color="red">Warning</font></center>
```

Da preferire:

```html
<p class="warning">Warning</p>
```

#### H051

`Role is not one ARIA defines for markup.`

Un ruolo che nessuna specifica nomina viene scartato del tutto e l'elemento conserva il significato che aveva già, quindi `role="buton"` lascia un `<div>` un semplice `<div>`: nulla per uno screen reader, mentre il markup sembra avergli dato uno scopo. Nulla avvisa del problema, ed è proprio questo che rende utile intercettare il refuso.

I nomi che la regola conosce sono i ruoli che ARIA definisce per gli autori, insieme a quelli aggiunti da DPUB-ARIA (`doc-chapter` e gli altri) e da GRAPHICS-ARIA (`graphics-symbol` e gli altri). I ruoli astratti di ARIA, come `landmark` e `sectionhead`, vengono segnalati: la specifica dice che esistono per costruirne l'ontologia e non devono essere scritti nel markup.

Un `role` può contenere più nomi, come lista di ripiego, e ognuno viene controllato. Un valore che contiene sintassi di template non è determinabile e non viene toccato, e lo stesso vale per un binding scritto da un framework, come in `:role` o `[attr.role]`.

Da evitare:

```html
<div role="buton">Save</div>
```

Da preferire:

```html
<button type="button">Save</button>
```

#### H052

`Meta refresh should not reload or redirect the page on a timer.`

Un aggiornamento a tempo sposta la pagina sotto gli occhi di chi la sta leggendo. Chi legge lentamente, usa uno screen reader o è stato semplicemente interrotto perde il segno senza preavviso e senza modo di fermarlo, il che viola il criterio WCAG 2.2.1 Regolazione tempi di esecuzione, e un aggiornamento che ricarica la stessa pagina butta via tutto ciò che vi era stato digitato.

Un ritardo pari a zero è un reindirizzamento immediato e non un timer, che le WCAG ammettono dove non si può usare un reindirizzamento lato server, quindi non viene segnalato. I due attributi vengono trovati in qualunque ordine siano scritti.

Da evitare:

```html
<meta http-equiv="refresh" content="30">
```

Da preferire:

```html
<meta http-equiv="refresh" content="0; url=/next-page">
```

#### H053

`Id is used more than once in the file.`

Un id identifica un solo elemento. Un secondo elemento con lo stesso id rompe `getElementById`, `<label for>`, i link a frammenti e `aria-labelledby`: il browser prende il primo e ignora silenziosamente gli altri, quindi una label, un link o uno script finisce sull'elemento sbagliato senza alcun avviso.

Due id in rami esclusivi di uno stesso `{% if %}...{% else %}...{% endif %}` non vengono mai renderizzati entrambi, quindi non vengono segnalati. Un ciclo `{% for %}` o un `{% block %}` non è un ramo: un id al suo interno e lo stesso id al di fuori vengono renderizzati entrambi, e viene segnalato quello successivo. Un valore scritto da un tag di template non è determinabile e non viene toccato, così come un valore vuoto. Gli id vengono confrontati in modo esatto, come fa il browser, quindi `save` e `Save` sono due id diversi.

I rami vengono letti in qualunque linguaggio sia scritto il file, e con qualsiasi spaziatura il linguaggio ammetta tra i delimitatori e il nome del tag: `{% elif %}` e `{% else %}`, `{% elsif %}` e `{% when %}` di liquid, `{{ else }}` di go, una riga di istruzione mako `% else:`, e `{{else}}` di handlebars, il suo `{{else if x}}` concatenato e la sezione inversa di qualsiasi blocco `{{#helper}}`, helper personalizzati compresi. Il contenuto di un `<template>` è un frammento di documento a sé, che `getElementById` non raggiunge mai, quindi un id al suo interno viene confrontato solo con gli id dello stesso `<template>`: due template possono contenere ciascuno una riga con lo stesso id, mentre due id uguali all'interno di uno stesso template vengono comunque segnalati. Un id dentro un commento, nel corpo di un <code>{&#37; raw %}</code> o di un `{% verbatim %}`, o in una regione `djlint:off` non viene letto affatto.

Da evitare:

```html
<button type="submit" id="submit">Save</button>
<button type="submit" id="submit">Save and continue</button>
```

Da preferire:

```html
<button type="submit" id="submit">Save</button>
<button type="button" id="cancel">Cancel</button>
```

#### H054

`Interactive element should not be nested inside another.`

L'html vieta i contenuti interattivi all'interno di `<a>` e `<button>`. Un pulsante dentro un link, o un link dentro un pulsante, è markup non valido che ogni browser ripara a modo suo, e chi usa uno screen reader o la tastiera si trova davanti a un unico controllo che si comporta come due. axe segnala la stessa cosa come "nested-interactive".

I contenitori controllati sono un `<a>` con un `href` e un `<button>`, e i controlli segnalati al loro interno sono un link con un `href`, `button`, `input`, `select` e `textarea`. Un `<a>` senza `href` non è interattivo e non viene toccato da nessuna delle due parti, così come un input nascosto o uno il cui type è scritto da un tag di template. Il contenuto di un `<template>` non viene renderizzato dove è scritto, quindi un controllo al suo interno non è annidato nel link che lo circonda, anche se un annidamento scritto all'interno del template viene comunque segnalato.

Un attributo viene letto dove un tag ne scrive uno e in nessun altro punto: l'`href` di `{% if not href %}` è il nome di una variabile, quello in `{# href="{{ url }}" #}` è commentato e quello in `data-attr=href` appartiene a un altro attributo, mentre l'`href` che un `{% if %}` scrive tra i propri tag è un attributo come gli altri. Un link o un pulsante lasciato aperto termina con l'elemento che lo circonda, come avverrebbe in un browser, così un solo refuso non fa segnalare il resto del file; uno lasciato aperto al livello più alto non ha nulla intorno che lo termini e arriva davvero fino alla fine del file, dove anche H025 segnala il tag orfano.

Da evitare:

```html
<a href="/cart"><button>Add</button></a>
```

Da preferire:

```html
<a href="/cart" class="button">Add</a>
```

#### H055

`Lang attribute should be a language tag such as en or pt-BR.`

H005 richiede un `lang` su `<html>`, ma un valore come `lang="english"` o `lang="en_US"` lo soddisfa pur non indicando nessuna lingua nota a un browser. Uno screen reader ripiega allora sulla voce predefinita, e traduzione e sillabazione applicano le regole sbagliate o nessuna. Il valore deve essere un tag BCP 47: due o tre lettere, seguite da un numero qualsiasi di sottotag da una a otto lettere o cifre, ciascuno preceduto da un trattino, come in `en`, `pt-BR` o `zh-Hant-TW`.

Viene controllato solo il tag `<html>`, come per H005. Un valore vuoto è lasciato a quella regola, mentre un valore composto solo da spazi viene segnalato qui, perché H005 lo considera un valore. Un valore scritto da un tag di template, come in `lang="{{ LANGUAGE_CODE }}"`, o da un echo breve di php, come in `lang="<?= $lang ?>"`, non è determinabile e non viene toccato, ma un valore che si limita a iniziare con `$` o `{`, come in `lang="$LANG"`, viene letto così com'è scritto. `xml:lang` o `data-lang` non vengono letti come `lang`, e un `>` scritto dentro un tag di template prima dell'attributo, come in `{% if a > b %}`, non lo nasconde.

Da evitare:

```html
<html lang="english">
```

Da preferire:

```html
<html lang="en">
```

#### H056

`Src should not be empty.`

La specifica html dice che un `src` vuoto non è valido e avverte che un browser lo risolve rispetto all'url del documento stesso, quindi `<img src="">` scarica di nuovo la pagina come immagine e `<script src=""></script>` la scarica come script. Di solito è un segnaposto che uno script doveva riempire, e la soluzione è togliere l'attributo, o tenere il valore in un attributo data, finché non ce n'è uno reale. Anche un `src` scritto senza alcun valore, come in `<img src>`, è vuoto e viene segnalato.

Vengono controllati solo `img`, `script`, `iframe`, `embed`, `source`, `track`, `audio` e `video`, perché sono gli elementi che scaricano ciò che `src` indica. Viene segnalato solo un valore che un browser legge come vuoto, quindi un valore senza virgolette come `<img src=/static/logo.png>` non viene toccato, così come un valore composto solo da spazi e un valore scritto da un tag di template, e `srcset` e `data-src` sono attributi diversi che la regola non valuta.

Da evitare:

```html
<img src="" alt="Logo">
```

Da preferire:

```html
<img src="{% static 'logo.png' %}" alt="Logo">
```

#### H057

`Video should have a captions track.`

Un video con audio trasmette il parlato solo attraverso l'audio, quindi una persona sorda o con problemi di udito non ne ricava nulla senza sottotitoli, richiesti dal criterio WCAG 1.2.2 Sottotitoli (preregistrati). Un `<track>` con un `kind` pari a `captions` o `subtitles` all'interno del `<video>` soddisfa la regola, e lo stesso vale per un `<track>` senza alcun `kind`, perché `subtitles` è il valore predefinito.

Un video `muted` non ha audio da sottotitolare e non viene segnalato. Né lo è un video il cui tag di apertura o il cui corpo contiene un tag di template, perché le tracce, o l'attributo `muted`, potrebbero essere scritte dal template dove djLint non può vederle. Per tag di template si intende uno che un linguaggio di template apre, `{{`, `{%`, `{#` o `${`, quindi un gestore jQuery come `onclick="$(this).play()"`, un `$refs` di Alpine, una parentesi graffa css e un prezzo scritto nel testo di ripiego sono normale testo, come appaiono, e il video viene comunque letto.

`muted` deve essere l'attributo, quindi `<video class=muted>` è una classe chiamata muted e viene segnalato, e un `<track>` commentato o scritto all'interno del valore di un attributo è testo e non una traccia. Un `</video>` dentro un valore non chiude nulla, e l'elemento viene valutato dove lo chiude il suo vero tag di chiusura, quindi un `<video>` lasciato aperto è lasciato a `H025`.

Da evitare:

```html
<video controls src="talk.mp4"></video>
```

Da preferire:

```html
<video controls src="talk.mp4">
  <track kind="captions" src="talk.vtt" srclang="en">
</video>
```

{% endraw %}

<!-- oxfmt-ignore-end -->

### Aggiungere regole

Le pull request con nuove regole sono benvenute!

Una buona regola è composta da

::: content

- Nome
- Codice
- Messaggio: messaggio da mostrare quando viene trovato l'errore.
- Flag: flag delle regex, ad esempio re.I|re.M. Il valore predefinito è re.DOTALL.
- Pattern: espressioni regolari che trovano l'errore.
- Esclusioni: lista opzionale dei profili a cui la regola non si applica.
:::

Includi un test che verifichi la regola.

## Regole personalizzate

Puoi aggiungere regole personalizzate solo per il tuo progetto creando un file `.djlint_rules.yaml` accanto al tuo `pyproject.toml`. Le regole aggiunte a questo file vengono rilevate da djLint. Un file di regole in un'altra posizione può essere indicato con l'opzione `--rules` della CLI.

### Regole basate su pattern

Puoi aggiungere regole che falliscono se uno dei pattern regex trova una corrispondenza:

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Regole con modulo Python

Puoi aggiungere regole che importano ed eseguono una funzione Python personalizzata:

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

Il `python_module` indicato deve contenere una funzione `run()` che verrà eseguita su ogni file controllato. Deve accettare i seguenti argomenti:

::: content

- `rule`: il dict che rappresenta la tua regola in `.djlint_rules.yaml`. Di solito userai questa variabile per accedere al nome e al messaggio della regola.
- `config`: l'oggetto di configurazione di djLint.
- `html`: l'intero contenuto html del file.
- `filepath`: il percorso del file che si sta controllando.
- `line_ends`: la lista delle posizioni dei caratteri di inizio (`start`) e fine (`end`) di ogni riga, che puoi usare con `djlint.api.get_line()` per ricavare i numeri di riga da una posizione di carattere. Vedi l'esempio.
- `*args, **kwargs`: in futuro potremmo aggiungere altri argomenti, quindi conviene includere questi due per ridurre il rischio di errori quando aggiorni djLint.
:::

Il modulo può trovarsi nella radice del progetto. Se restituisce un `line` o un `end` che non è una posizione, djLint si interrompe con un errore che indica il nome della regola.

Deve restituire una lista di dict, uno per ogni errore, con le seguenti chiavi:

::: content

- `code`: il nome del codice della regola che segnala l'errore (di solito `rule['name']`)
- `line`: numero di riga e numero di carattere su quella riga, separati da ':', come stringa.
  Ad esempio `"2:3"` significa che l'errore è stato trovato alla riga 2, carattere 3
- `end`: opzionale. Dove termina l'errore, scritto come `line`, subito dopo il suo ultimo carattere. Senza di esso, l'errore termina dove termina `match`.
- `match`: la parte del contenuto che contiene l'errore
- `message`: il messaggio che verrà stampato per segnalare l'errore (di solito `rule['message']`)
:::

```python
from __future__ import annotations

import re
from typing import TYPE_CHECKING

from djlint.api import get_line, inside_ignored_linter_block, inside_ignored_rule

if TYPE_CHECKING:
    from typing import Any

    from djlint.api import Config, LintError


def run(
    rule: dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: list[dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> list[LintError]:
    """Regola che fallisce se il file html contiene 'bad'.

    È solo un esempio: in realtà è molto più semplice farlo con una
    "regola basata su pattern".
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
