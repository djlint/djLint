---
title: "API Python"
description: "Formate e faça o lint de templates a partir do seu próprio código Python com a API do djLint."
---

`djlint.api` formata e faz o lint de texto a partir de um programa Python, com os mesmos resultados da linha de comando. Ele foi feito para editores, ferramentas de build e qualquer outra coisa que mantenha um template em memória. Todo o restante do pacote pode mudar em qualquer versão, então use este módulo em vez de `djlint.settings` ou `djlint.lint`. As funções auxiliares que o [exemplo de regra personalizada](/pt-br/docs/linter/#regras-com-modulo-python) importa, `djlint.lint.get_line`, `djlint.helpers.inside_ignored_rule` e `djlint.helpers.inside_ignored_linter_block`, também continuam funcionando.

```python
from djlint.api import format_text, lint_text, load_config

config = load_config("templates", profile="django", indent=2)

formatted = format_text(config, "<div><p>hi</p></div>")

for finding in lint_text(config, '<img src="a.png">', "templates/home.html"):
    print(finding.line, finding.column, finding.code, finding.message)
```

## load_config

`load_config(folder=".", *, python_rules=True, on_warning=None, **options)` lê a configuração que se aplica aos arquivos de uma pasta. Ela a procura subindo a partir da pasta, como a linha de comando [faz](/pt-br/docs/configuration/) a partir do primeiro caminho que recebe, e não altera o diretório atual.

As opções usam os nomes das opções da linha de comando, com sublinhados, e funcionam como lá: um valor definido prevalece sobre o arquivo de configuração, enquanto `False`, uma string vazia e, para a maioria das opções, `0` contam como não informados. Caminhos são passados como `pathlib.Path`.

Ler a configuração leva algum tempo, então guarde o resultado enquanto os arquivos de onde ela foi lida não mudarem. Ele pode ser usado para qualquer quantidade de textos.

Com `python_rules=False`, as regras personalizadas com um `python_module` não são carregadas, o que impede que o código de um projeto em que você não confia seja executado. Os nomes delas ficam em `config.skipped_rules`.

`on_warning`, uma função que recebe uma mensagem, recebe cada aviso sobre as configurações, como um nome digitado errado ou um código de regra que nenhuma regra tem. Sem ela, cada aviso vai para o stderr uma vez por processo. Um arquivo de configuração que não pode ser lido, ou um valor inválido, levanta `click.UsageError`.

## format_text

`format_text(config, text)` retorna o texto formatado. Um texto cuja primeira linha termina em CRLF volta em CRLF, e qualquer outro, em LF. Com `require_pragma`, um texto sem o pragma volta inalterado. Ela pega `indent` e `max_line_length` do `.editorconfig` que se aplica à pasta passada para `load_config`, enquanto a linha de comando os pega para cada arquivo pelo seu caminho.

## lint_text

`lint_text(config, text, filename="-")` retorna uma lista de `Finding`, na ordem do documento. `filename` é o que é comparado com `per-file-ignores`. Com `require_pragma`, um texto sem o pragma não tem ocorrências.

`Finding` é uma named tuple com estes campos:

- `code`: O código da regra, como `H013`.
- `message`: O que a regra diz.
- `match`: O início do texto encontrado, com até 20 caracteres.
- `line`, `column`: Onde a ocorrência começa. As linhas são contadas a partir de 1, e as colunas, a partir de 0.
- `end_line`, `end_column`: Logo depois de onde ela termina, o que pode ser em uma linha posterior.

As colunas contam caracteres, não bytes nem unidades de código UTF-16.

## is_excluded

`is_excluded(config, path)` informa se `exclude`, `extend_exclude` ou o gitignore deixam um arquivo de fora, como a linha de comando faz. `format_text` e `lint_text` não verificam isso por conta própria.

## Módulos de regras

O `python_module` de uma regra personalizada é importado uma vez por processo, a partir da raiz do projeto da configuração. Para ler as regras de outro projeto, um programa que continua em execução precisa remover de `sys.modules` tudo o que importou do primeiro projeto, e remover a raiz desse projeto do final de `sys.path`.
