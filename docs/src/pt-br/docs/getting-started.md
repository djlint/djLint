---
description: Instale o djLint e faça o lint ou formate templates HTML pela linha de comando.
title: Primeiros passos
keywords: linter de templates, formatador de templates, djLint, HTML, templates, formatador, linter, uso
---

# Primeiros passos

## Instalação

O djLint é feito em [Python](https://python.org) e publicado no [PyPI](https://pypi.org/project/djlint/). Com o [uv](https://docs.astral.sh/uv/), adicione-o ao seu projeto como dependência de desenvolvimento:

```bash
uv add --dev djlint
```

Ou instale-o como uma ferramenta independente:

```bash
uv tool install djlint
```

Ou com o pip:

```bash
pip install djlint
```

Ou com o [pipx](https://pipx.pypa.io/):

```bash
pipx install djlint
```

Ou com a [fórmula do Homebrew](https://formulae.brew.sh/formula/djlint) mantida pela comunidade, no macOS ou no Linux:

```bash
brew install djlint
```

_Ou com o npm. **Atenção**: o pacote npm é apenas um wrapper. O script de instalação dele executa `pip install --upgrade djlint` com o `python3` que estiver no PATH do seu sistema, e o npm não vai gerenciar nem desinstalar o pacote de fato, então prefira o pip sempre que puder._

```bash
npm i djlint
```

Para executar o djLint a cada commit, consulte [pre-commit]({{ "lang_code_url" | i18n }}/docs/integrations/#pre-commit).

## Uso da CLI

O djLint é um aplicativo de linha de comando. Consulte a página de [configuração]({{ "lang_code_url" | i18n }}/docs/configuration/) para a configuração avançada.

{% include 'src/_includes/cli.md' %}

{% admonition
   "note",
   "Observação",
   "Se o comando `djlint` não for encontrado, verifique se o Python está [no seu PATH](https://www.geeksforgeeks.org/how-to-add-python-to-windows-path/)."
%}

## Usando caminho ou stdin

O djLint funciona com um caminho ou com o stdin.

Executando com um caminho -

```bash
djlint /path/to/templates --lint
```

Ou com um arquivo específico -

```bash
djlint /path/to/this.mustache --lint
```

Ou com o stdin -

```bash
echo "<div></div>" | djlint -
```

O stdin também pode ser usado para reformatar código. A saída será apenas o código formatado, sem mensagens.

```bash
echo "<div></div>" | djlint - --reformat
```

Saída -

```html
<div></div>
```

Ao ler do stdin, o djLint não tem um caminho real para comparar com `per-file-ignores` nem para mostrar nas mensagens, então usa `-` por padrão. Passe `--stdin-filename` para informar ao djLint o caminho real do conteúdo recebido pelo pipe, por exemplo quando uma integração com editor envia o conteúdo de um arquivo pelo pipe ao salvar.

```bash
echo "<div></div>" | djlint - --stdin-filename templates/index.html
```

## Códigos de saída

| Código | Significado                                                                                                                                                      |
| ------ | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| `0`    | Tudo o que você pediu para o djLint verificar está limpo, ou todos os arquivos encontrados foram ignorados pela sua configuração.                                |
| `1`    | O djLint encontrou erros de lint ou arquivos que precisam ser reformatados. `--warn` relata esses casos como avisos e, em vez disso, sai com `0`.                |
| `2`    | O djLint não verificou o que você pediu: os caminhos não corresponderam a nenhum arquivo, a linha de comando ou a configuração era inválida, ou o djLint falhou. |

Somente o código `1` significa que o djLint analisou seus templates e não gostou do que encontrou. O código `2` sempre significa que a própria execução não cumpriu seu papel, então um pipeline pode tratar os dois de forma diferente.

O código `2` é o que detecta uma execução que não verificou absolutamente nada: um caminho errado, uma `--extension` que não corresponde mais a nada, ou templates que foram movidos. Sem ele, uma execução assim passa silenciosamente.

Arquivos que o djLint _encontrou_ e depois ignorou de propósito, por meio de `exclude`, `extend_exclude`, `use_gitignore` ou `require_pragma`, não são um erro. Essa execução sai com `0`, porque a configuração fez exatamente o que lhe foi pedido. É também isso que permite que `exclude` funcione com o pre-commit, que passa os nomes dos seus arquivos preparados para commit, quer você queira ou não que o djLint os analise.

Se um caminho que legitimamente não tem templates for normal no seu pipeline, desative o código `2` com `allow_empty_input`:

```bash
djlint /path/to/templates --lint --allow-empty-input
```
