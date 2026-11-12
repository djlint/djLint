---
title: "API Python"
description: "Formatta e analizza i template dal tuo codice Python con l'API di djLint."
---

`djlint.api` formatta e analizza testo da un programma Python, con gli stessi risultati della riga di comando. È pensato per editor, strumenti di build e qualsiasi altra cosa che tenga un template in memoria. Tutto il resto del pacchetto può cambiare in qualsiasi release, quindi usa questo modulo anziché `djlint.settings` o `djlint.lint`.

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, **options)` legge la configurazione che si applica ai file di una cartella. La cerca risalendo a partire dalla cartella, come fa la riga di comando a partire dalla directory corrente, e non cambia la directory corrente.

Le opzioni usano i nomi delle opzioni della riga di comando, con i trattini bassi, e funzionano allo stesso modo: un valore impostato ha la precedenza sul file di configurazione, mentre `False`, una stringa vuota e, per la maggior parte delle opzioni, `0` contano come non specificati. I percorsi si passano come `pathlib.Path`.

La lettura della configurazione richiede un po' di tempo, quindi conserva il risultato finché i file da cui è stata letta non cambiano. Si può usare per un numero qualsiasi di testi.

Con `python_rules=False`, le regole personalizzate con un `python_module` non vengono caricate, il che impedisce l'esecuzione del codice di un progetto di cui non ti fidi. I loro nomi si trovano in `config.skipped_rules`.

## format_text

`format_text(config, text)` restituisce il testo formattato. Un testo la cui prima riga termina con CRLF viene restituito con CRLF, qualsiasi altro con LF. Con `require_pragma`, un testo senza il pragma viene restituito invariato.

## lint_text

`lint_text(config, text, filename="-")` restituisce una lista di `Finding`, nell'ordine del documento. `filename` è ciò con cui viene confrontato `per-file-ignores`. Con `require_pragma`, un testo senza il pragma non ha segnalazioni.

`Finding` è una named tuple con questi campi:

- `code`: il codice della regola, ad esempio `H013`.
- `message`: ciò che dice la regola.
- `match`: l'inizio del testo trovato, fino a 20 caratteri.
- `line`, `column`: dove inizia la segnalazione. Le righe si contano da 1 e le colonne da 0.
- `end_line`, `end_column`: subito dopo il punto in cui finisce, che può trovarsi su una riga successiva.

Le colonne contano i caratteri, non i byte né le unità di codice UTF-16.

## is_excluded

`is_excluded(config, path)` indica se `exclude`, `extend_exclude` o il gitignore escludono un file, come fa la riga di comando. `format_text` e `lint_text` non effettuano questo controllo da sé.

## Moduli delle regole

Il `python_module` di una regola personalizzata viene importato una volta per processo, dalla radice del progetto della configurazione. Un programma che resta in esecuzione e lavora con più progetti, per leggere quelli di un altro progetto, deve rimuovere da `sys.modules` tutto ciò che è stato importato dal progetto, e da `sys.path` la radice del progetto, che vi resta in fondo.
