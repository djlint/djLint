---
description: Registro delle modifiche di djLint. Scopri le novità delle ultime release e le funzionalità che puoi aspettarti dal prossimo aggiornamento.
title: Registro delle modifiche
keywords: linter per template, formattatore per template, djLint, HTML, template, formattatore, linter, registro delle modifiche
---

{% raw %}

# Registro delle modifiche

Il registro delle modifiche è ora incluso nelle [release](https://github.com/djlint/djLint/releases).

## 1.0.2

::: content

- Correzioni di bug [#240](https://github.com/djlint/djLint/issues/240)
:::

## 1.0.1

::: content

- Correzioni di bug [#236](https://github.com/djlint/djLint/issues/236)
:::

## 1.0.0

::: content

- Correzioni di bug [#224](https://github.com/djlint/djLint/issues/224)
:::

## 0.7.6

::: content

- Correzioni di bug [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/197)
- Aggiunto il flag `--warn` per restituire gli errori come avvisi.
:::

## 0.7.5

::: content

- Correzioni di bug [#187](https://github.com/djlint/djLint/issues/187)
- Migliorato il supporto al front matter `yaml` nei file di template
- Aggiunta la regola T032 per [#123](https://github.com/djlint/djLint/issues/123)
- Aggiunta la regola H033 per [#124](https://github.com/djlint/djLint/issues/124)
- I profili del linter ora sono inclusivi anziché esclusivi, per [#178](https://github.com/djlint/djLint/issues/178)
- Aggiunto il file di configurazione alternativo `.djlintrc` per [#188](https://github.com/djlint/djLint/issues/188)
:::

## 0.7.4

::: content

- Correzioni di bug [#177](https://github.com/djlint/djLint/issues/177)
:::

## 0.7.3

::: content

- Correzioni di bug [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- Rimosso Py3.6 da `pyproject.toml`.
:::

## 0.7.2

::: content

- Correzioni di bug [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
:::

## 0.7.1

::: content

- Correzioni di bug [#166](https://github.com/djlint/djLint/issues/166)
:::

## 0.7.0

::: content

- Aggiunta la configurazione per i tag HTML personalizzati
- Correzioni di bug
:::

## 0.6.9

::: content

- Aggiunti i profili HTML e Angular
- Ammesse alcune entità nella regola #H023
- Correzioni di bug
:::

## 0.6.8

::: content

- Correzioni di bug
- Aggiornata la documentazione
:::

## 0.6.7

::: content

- Aggiunta l'opzione di configurazione `format_attribute_template_tags`, da attivare esplicitamente, per formattare i tag di template all'interno degli attributi
- Aggiunta l'opzione di configurazione `linter_output_format` per personalizzare l'ordine delle variabili nei messaggi del linter
- Aggiunte le regole H030 e H031 per controllare i meta tag
:::

## 0.6.6

::: content

- Correzioni di bug
:::

## 0.6.5

::: content

- I percorsi nell'output ora sono relativi alla radice del progetto
- Correzioni di bug
:::

## 0.6.4

::: content

- Correzioni di bug
:::

## 0.6.3

::: content

- Aggiunto il supporto al tag `blocktrans` di django
- Correzioni di bug
:::

## 0.6.2

::: content

- Correzioni di bug
:::

## 0.6.1

::: content

- Correzioni di bug
- Resa più rigorosa la regola T028, con un messaggio più chiaro
:::

## 0.6.0

::: content

- Aggiunta la regola T027 per controllare le stringhe non chiuse nella sintassi dei template
- Aggiunta la regola T028 per controllare i tag senza spazi mancanti negli attributi
- Aggiunta la regola H029 per controllare che il method dei form sia in minuscolo
- Esclusi dal formattatore i tag blocktranslate di django privi di "trimmed"
- Correzioni di bug
:::

## 0.5.9a

::: content

- Aggiunto il supporto ai test per python 3.10
- Aggiunto l'hook di pre-commit
:::

## 0.5.9

::: content

- Aggiunta l'opzione `--use-gitignore` per estendere le esclusioni
- Modificata la corrispondenza predefinita delle esclusioni
- Corretti i percorsi di esclusione su windows
- Corretta la formattazione dei tag `{%...%}` negli attributi
- Corretta la formattazione dei cicli for e delle condizioni annidate negli attributi
:::

## 0.5.8

::: content

- Aggiunta l'opzione require_pragma
- Aggiornata DJ018 per intercettare `data-src` e `action` negli input
- Corretta la sintassi per ignorare il codice inline
- Aggiunta l'opzione `--lint` come segnaposto per l'uso predefinito
- Correzioni di bug
:::

## 0.5.7

::: content

- Correzioni di bug
:::

## 0.5.6

::: content

- Aggiunta la regola H026 per trovare i tag id e class vuoti
- Correzioni di bug
:::

## 0.5.5

::: content

- Accorpate le impostazioni e snellito il codice
- Correzioni di bug
:::

## 0.5.4

::: content

- Aggiunta la regola H020 per trovare le coppie di tag vuote
- Aggiunta la regola H021 per trovare gli stili inline
- Aggiunta la regola H022 per trovare i link http
- Aggiunta la regola H023 per trovare i riferimenti a entità
- Aggiunta la regola H024 per trovare type su script e stili
- Aggiunta la regola H025 per controllare i tag orfani. Grazie a https://stackoverflow.com/a/1736801/10265880
- Migliorata la formattazione degli attributi
- Aggiornata l'opzione `blank_line_after_tag` per aggiungere un a capo indipendentemente dalla posizione
- Corretta la formattazione del tag `trans` di django
- Aggiunta la formattazione degli stili inline
- Aggiunta la formattazione delle condizioni di template all'interno degli attributi
- Aggiunto srcset tra le possibili posizioni degli url nelle regole del linter
- Velocizzata la formattazione
- Un ringraziamento speciale a [jayvdb](https://github.com/jayvdb)
:::

## 0.5.3

::: content

- Modificato lo stdout delle opzioni `--reformat/check` in modo da stampare il nuovo html solo quando l'input è stdin
:::

## 0.5.2

::: content

- Separato il requisito di `alt` da H006 in H013
- Aggiunto un file opzionale di regole personalizzate
- Aggiunto `golang` come opzione di profilo
- Corretta la formattazione dei blocchi ignorati che contengono commenti inline
- Aggiunto il testo predefinito alle opzioni `--indent` e `-e`
- Aggiornate le regole sugli url per accettare #
- Corretta la codifica dei file su sistemi operativi Windows
- Corretta la regex dei tag di template su una sola riga
- Corretto `blank_line_after_tag` per i tag con spazio iniziale
:::

## 0.5.1

::: content

- Aggiunta la regola H019
- Corretti i bug in DJ018 e H012
:::

## 0.5.0

::: content

- Corretti diversi bug di corrispondenza delle regex nelle regole del linter
- Il linter non restituisce più errori nei blocchi ignorati
- Aggiunta l'opzione per escludere un blocco di codice dal linter/formattatore con i tag `{% djlint:off %}...{% djlint:on %}`
:::

## 0.4.9

::: content

- Corretto il bug [#35](https://github.com/djlint/djLint/issues/35)
:::

## 0.4.8

::: content

- Corretto il bug [#34](https://github.com/djlint/djLint/issues/34)
:::

## 0.4.7

::: content

- Spostato il tag `source` tra i tag su una sola riga
:::

## 0.4.6

::: content

- Corretto il bug [#31](https://github.com/djlint/djLint/issues/31)
:::

## 0.4.5

::: content

- Aggiunte le buone pratiche alla documentazione
- Aggiunta l'opzione `--profile` per impostare le regole predefinite del linter/formattatore
- Aggiunte regole del linter per gli schemi degli url di jinja
:::

## 0.4.4

::: content

- La configurazione dell'indentazione passa da stringa a intero. `--indent 3`
:::

## 0.4.3

::: content

- Aggiunta l'opzione della cli per gli spazi di indentazione. `--indent=" "`
:::

## 0.4.2

::: content

- Aggiunto il supporto a spazi aggiuntivi dopo i tag con l'opzione `blank_line_after_tag`
:::

## 0.4.1

::: content

- Aggiunto il supporto all'elaborazione di più file o cartelle in una volta
:::

## 0.4.0

::: content

- Corretta la formattazione dei tag `{# ... #}` di django
- Aggiunto il supporto all'indentazione per i tag figcaption, details e summary
- Aggiunto il supporto alla sovrascrittura o all'estensione dell'elenco dei percorsi esclusi in `pyproject.toml`
:::

## 0.3.9

::: content

- Aggiornata la gestione degli attributi
:::

## 0.3.8

::: content

- Aggiunto il supporto a stdin
:::

## 0.3.7

::: content

- Corretta la formattazione dei tag `small`, `dt` e `dd`
:::

## 0.3.6

::: content

- Aggiunto il supporto del formattatore ai blocchi di apertura `{%-` di Nunjucks
:::

## 0.3.5

::: content

- Aggiunto il supporto a più blocchi di Django
- Aggiunto il supporto ai blocchi personalizzati
- Aggiunto il supporto alla configurazione in `pyproject.toml`
:::

## 0.3.4

::: content

- Corretto il formato del tag senza spazi `-%}` di Nunjucks
:::

## 0.3.3

::: content

- I tag `div` brevi possono stare su una sola riga
:::

## 0.3.2

::: content

- Corretta la formattazione dei commenti di Django
- Textarea esclusa dalla formattazione
:::

## 0.3.1

::: content

- Aggiornata la regex di formattazione degli attributi
- Aggiornata la regola di lint W010
:::

## 0.3.0

::: content

- Il codice di uscita diventa 1 se ci sono state modifiche di formattazione
- Aggiunto il supporto ai tag `asset` di Jinja
:::

## 0.2.9

::: content

- Aggiornata la regex di W018
- Rimossi i messaggi di lint duplicati
- Aggiornata E001 per Handlebars
:::

## 0.2.8

::: content

- Corretto l'errore della barra di avanzamento con le vecchie versioni di Click
:::

{% endraw %}
