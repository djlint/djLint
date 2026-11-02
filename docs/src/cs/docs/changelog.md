---
description: Seznam změn djLint. Podívejte se na novinky z posledních vydání a na to, jaké funkce můžete čekat při příští aktualizaci.
title: Seznam změn
keywords: linter šablon, formátovač šablon, djLint, HTML, šablony, formátovač, linter, seznam změn
---

{% raw %}

# Seznam změn

Seznam změn je nyní součástí [vydání](https://github.com/djlint/djLint/releases).

## 1.0.2

::: content

- Opravy chyb [#240](https://github.com/djlint/djLint/issues/240)
:::

## 1.0.1

::: content

- Opravy chyb [#236](https://github.com/djlint/djLint/issues/236)
:::

## 1.0.0

::: content

- Opravy chyb [#224](https://github.com/djlint/djLint/issues/224)
:::

## 0.7.6

::: content

- Opravy chyb [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/197)
- Přidán přepínač `--warn`, který vrací chyby jako varování.
:::

## 0.7.5

::: content

- Opravy chyb [#187](https://github.com/djlint/djLint/issues/187)
- Přidána lepší podpora pro `yaml` front matter v souborech šablon
- Přidáno pravidlo T032 pro [#123](https://github.com/djlint/djLint/issues/123)
- Přidáno pravidlo H033 pro [#124](https://github.com/djlint/djLint/issues/124)
- Profily linteru nyní pravidla zahrnují, místo aby je vylučovaly, pro [#178](https://github.com/djlint/djLint/issues/178)
- Přidán alternativní konfigurační soubor `.djlintrc` pro [#188](https://github.com/djlint/djLint/issues/188)
:::

## 0.7.4

::: content

- Opravy chyb [#177](https://github.com/djlint/djLint/issues/177)
:::

## 0.7.3

::: content

- Opravy chyb [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- Z `pyproject.toml` odstraněn Py3.6.
:::

## 0.7.2

::: content

- Opravy chyb [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
:::

## 0.7.1

::: content

- Opravy chyb [#166](https://github.com/djlint/djLint/issues/166)
:::

## 0.7.0

::: content

- Přidána konfigurace pro vlastní HTML značky
- Opravy chyb
:::

## 0.6.9

::: content

- Přidány profily HTML a Angular
- V pravidle #H023 povoleny některé entity
- Opravy chyb
:::

## 0.6.8

::: content

- Opravy chyb
- Aktualizována dokumentace
:::

## 0.6.7

::: content

- Přidána konfigurační možnost `format_attribute_template_tags` jako volitelné formátování šablonových značek uvnitř atributů
- Přidána konfigurační možnost `linter_output_format` pro přizpůsobení pořadí proměnných ve zprávách linteru
- Přidána pravidla H030 a H031 pro kontrolu meta značek
:::

## 0.6.6

::: content

- Opravy chyb
:::

## 0.6.5

::: content

- Výstupní cesty jsou nyní relativní ke kořeni projektu
- Opravy chyb
:::

## 0.6.4

::: content

- Opravy chyb
:::

## 0.6.3

::: content

- Přidána podpora pro značku django `blocktrans`
- Opravy chyb
:::

## 0.6.2

::: content

- Opravy chyb
:::

## 0.6.1

::: content

- Opravy chyb
- Pravidlo T028 je přísnější a má srozumitelnější zprávu
:::

## 0.6.0

::: content

- Přidáno pravidlo T027 pro kontrolu neuzavřených řetězců v šablonové syntaxi
- Přidáno pravidlo T028 pro kontrolu chybějících značek bez mezer v atributech
- Přidáno pravidlo H029 pro kontrolu hodnot method formuláře malými písmeny
- Formátovač ignoruje značky django blocktranslate, které nemají „trimmed“
- Opravy chyb
:::

## 0.5.9a

::: content

- Přidána podpora testů pro python 3.10
- Přidán hook pre-commit
:::

## 0.5.9

::: content

- Přidána možnost `--use-gitignore` pro rozšíření vyloučených cest
- Změněno výchozí porovnávání vyloučených cest
- Opraveny vyloučené cesty ve Windows
- Opraveno formátování značek `{%...%}` v atributech
- Opraveno formátování cyklů for a vnořených podmínek v atributech
:::

## 0.5.8

::: content

- Přidána možnost require_pragma
- DJ018 nově zachytí `data-src` a `action` u inputů
- Opravena syntaxe pro ignorování přímo v kódu
- Přidána možnost `--lint` jako zástupná hodnota pro výchozí použití
- Opravy chyb
:::

## 0.5.7

::: content

- Opravy chyb
:::

## 0.5.6

::: content

- Přidáno pravidlo H026 pro hledání prázdných značek id a class
- Opravy chyb
:::

## 0.5.5

::: content

- Sloučena nastavení a zeštíhlen kód
- Opravy chyb
:::

## 0.5.4

::: content

- Přidáno pravidlo H020 pro hledání prázdných párů značek
- Přidáno pravidlo H021 pro hledání inline stylů
- Přidáno pravidlo H022 pro hledání odkazů http
- Přidáno pravidlo H023 pro hledání znakových entit
- Přidáno pravidlo H024 pro hledání atributu type u skriptů a stylů
- Přidáno pravidlo H025 pro kontrolu osiřelých značek. Díky https://stackoverflow.com/a/1736801/10265880
- Vylepšeno formátování atributů
- Možnost `blank_line_after_tag` nyní přidává nový řádek bez ohledu na umístění
- Opraveno formátování značky django `trans`
- Přidáno formátování inline stylů
- Přidáno formátování šablonových podmínek uvnitř atributů
- Přidán srcset jako možné umístění URL v pravidlech linteru
- Zrychleno formátování
- Zvláštní poděkování patří [jayvdb](https://github.com/jayvdb)
:::

## 0.5.3

::: content

- Výstup na stdout u možností `--reformat/check` nyní vypisuje nové html jen při použití stdin jako vstupu
:::

## 0.5.2

::: content

- Požadavek na `alt` oddělen z H006 do H013
- Přidán volitelný soubor s vlastními pravidly
- Přidán `golang` jako možnost profilu
- Opraveno formátování ignorovaných bloků obsahujících inline komentáře
- Přidán výchozí text k možnostem `--indent` a `-e`
- Pravidla pro URL nyní přijímají #
- Opraveno kódování souborů ve Windows
- Oprava regulárního výrazu pro jednořádkové šablonové značky
- Oprava `blank_line_after_tag` u značek s úvodní mezerou
:::

## 0.5.1

::: content

- Přidáno pravidlo H019
- Opraveny chyby v DJ018 a H012
:::

## 0.5.0

::: content

- Opraveno několik chyb s porovnáváním regulárních výrazů v pravidlech linteru
- Linter už nevrací chyby v ignorovaných blocích
- Přidána možnost ignorovat blok kódu v linteru/formátovači pomocí značek `{% djlint:off %}...{% djlint:on %}`
:::

## 0.4.9

::: content

- Opravena chyba [#35](https://github.com/djlint/djLint/issues/35)
:::

## 0.4.8

::: content

- Opravena chyba [#34](https://github.com/djlint/djLint/issues/34)
:::

## 0.4.7

::: content

- Značka `source` přesunuta mezi jednořádkové značky
:::

## 0.4.6

::: content

- Opravena chyba [#31](https://github.com/djlint/djLint/issues/31)
:::

## 0.4.5

::: content

- Do dokumentace přidány osvědčené postupy
- Přidána možnost `--profile` pro nastavení výchozích pravidel linteru/formátovače
- Přidána pravidla linteru pro vzory URL v jinja
:::

## 0.4.4

::: content

- Konfigurace odsazení změněna z řetězce na celé číslo. `--indent 3`
:::

## 0.4.3

::: content

- Přidána možnost příkazového řádku pro velikost odsazení. `--indent=" "`
:::

## 0.4.2

::: content

- Přidána podpora pro další prázdné řádky za značkami pomocí možnosti `blank_line_after_tag`
:::

## 0.4.1

::: content

- Přidána podpora pro zpracování více souborů nebo složek najednou
:::

## 0.4.0

::: content

- Opraveno formátování značek django `{# ... #}`
- Přidána podpora odsazení pro značky figcaption, details a summary
- Přidána podpora pro přepsání nebo rozšíření seznamu vyloučených cest v `pyproject.toml`
:::

## 0.3.9

::: content

- Aktualizováno zpracování atributů
:::

## 0.3.8

::: content

- Přidána podpora pro stdin
:::

## 0.3.7

::: content

- Opraveno formátování značek `small`, `dt` a `dd`
:::

## 0.3.6

::: content

- Přidána podpora formátovače pro otevírací bloky `{%-` v Nunjucks
:::

## 0.3.5

::: content

- Přidána podpora pro další bloky Djanga
- Přidána podpora pro vlastní bloky
- Přidána podpora pro konfiguraci v `pyproject.toml`
:::

## 0.3.4

::: content

- Opraven formát značky bez mezer `-%}` v Nunjucks
:::

## 0.3.3

::: content

- Krátké značky `div` mohou být na jednom řádku
:::

## 0.3.2

::: content

- Opraveno formátování komentářů Djanga
- Textarea se z formátování vynechává
:::

## 0.3.1

::: content

- Aktualizován regulární výraz pro formátování atributů
- Aktualizováno pravidlo lintování W010
:::

## 0.3.0

::: content

- Návratový kód změněn na 1, pokud došlo k jakýmkoli změnám formátování
- Přidána podpora pro značky `asset` v Jinja
:::

## 0.2.9

::: content

- Aktualizován regulární výraz W018
- Odstraněny duplicitní zprávy lintování
- Aktualizováno E001 pro Handlebars
:::

## 0.2.8

::: content

- Opravena chyba ukazatele průběhu u starší verze Click
:::

{% endraw %}
