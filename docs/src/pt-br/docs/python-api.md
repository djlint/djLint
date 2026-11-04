---
description: Formate e faça o lint de templates a partir do seu próprio código Python com a API do djLint.
title: API Python
keywords: linter de templates, formatador de templates, djLint, HTML, templates, formatador, linter, python, api
---

# API Python

`djlint.api` formata e faz o lint de texto a partir de um programa Python, com os mesmos resultados da linha de comando. Ele foi feito para editores, ferramentas de build e qualquer outra coisa que mantenha um template em memória. Todo o restante do pacote pode mudar em qualquer versão, então use este módulo em vez de `djlint.settings` ou `djlint.lint`.

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, **options)` lê a configuração que se aplica aos arquivos de uma pasta. Ela a procura subindo a partir da pasta, como a linha de comando faz a partir do diretório atual, e não altera o diretório atual.

As opções usam os nomes das opções da linha de comando, com sublinhados, e funcionam como lá: um valor definido prevalece sobre o arquivo de configuração, enquanto `False`, uma string vazia e, para a maioria das opções, `0` contam como não informados. Caminhos são passados como `pathlib.Path`.

Ler a configuração leva algum tempo, então guarde o resultado enquanto os arquivos de onde ela foi lida não mudarem. Ele pode ser usado para qualquer quantidade de textos.

Com `python_rules=False`, as regras personalizadas com um `python_module` não são carregadas, o que impede que o código de um projeto em que você não confia seja executado. Os nomes delas ficam em `config.skipped_rules`.

## format_text

`format_text(config, text)` retorna o texto formatado. Um texto cuja primeira linha termina em CRLF volta em CRLF, e qualquer outro, em LF. Com `require_pragma`, um texto sem o pragma volta inalterado.

## lint_text

`lint_text(config, text, filename="-")` retorna uma lista de `Finding`, na ordem do documento. `filename` é o que é comparado com `per-file-ignores`. Com `require_pragma`, um texto sem o pragma não tem ocorrências.

`Finding` é uma named tuple com estes campos:

::: content

- `code`: O código da regra, como `H013`.
- `message`: O que a regra diz.
- `match`: O início do texto encontrado, com até 20 caracteres.
- `line`, `column`: Onde a ocorrência começa. As linhas são contadas a partir de 1, e as colunas, a partir de 0.
- `end_line`, `end_column`: Logo depois de onde ela termina, o que pode ser em uma linha posterior.
:::

As colunas contam caracteres, não bytes nem unidades de código UTF-16.

## is_excluded

`is_excluded(config, path)` informa se `exclude`, `extend_exclude` ou o gitignore deixam um arquivo de fora, como a linha de comando faz. `format_text` e `lint_text` não verificam isso por conta própria.

## Módulos de regras

O `python_module` de uma regra personalizada é importado uma vez por processo, a partir da raiz do projeto da configuração. Um programa que continua em execução e trabalha com vários projetos precisa remover de `sys.modules` tudo o que foi importado do projeto, e também a raiz do projeto, que fica no final de `sys.path`, para ler os módulos de outro projeto.
