---
description: Registro de alterações do djLint. Veja as novidades das versões recentes e quais recursos você pode esperar na próxima atualização.
title: Registro de alterações
keywords: linter de templates, formatador de templates, djLint, HTML, templates, formatador, linter, registro de alterações
---

{% raw %}

# Registro de alterações

O registro de alterações agora está incluído nas [releases](https://github.com/djlint/djLint/releases).

## 1.0.2

::: content

- Correções de bugs [#240](https://github.com/djlint/djLint/issues/240)
:::

## 1.0.1

::: content

- Correções de bugs [#236](https://github.com/djlint/djLint/issues/236)
:::

## 1.0.0

::: content

- Correções de bugs [#224](https://github.com/djlint/djLint/issues/224)
:::

## 0.7.6

::: content

- Correções de bugs [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/197)
- Adicionada a flag `--warn` para retornar os erros como avisos.
:::

## 0.7.5

::: content

- Correções de bugs [#187](https://github.com/djlint/djLint/issues/187)
- Melhorado o suporte a front matter `yaml` em arquivos de template
- Adicionada a regra T032 para [#123](https://github.com/djlint/djLint/issues/123)
- Adicionada a regra H033 para [#124](https://github.com/djlint/djLint/issues/124)
- Os perfis do linter passaram a ser inclusivos em vez de exclusivos para [#178](https://github.com/djlint/djLint/issues/178)
- Adicionada a opção de arquivo de configuração alternativo `.djlintrc` para [#188](https://github.com/djlint/djLint/issues/188)
:::

## 0.7.4

::: content

- Correções de bugs [#177](https://github.com/djlint/djLint/issues/177)
:::

## 0.7.3

::: content

- Correções de bugs [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- Removido o Py3.6 do `pyproject.toml`.
:::

## 0.7.2

::: content

- Correções de bugs [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
:::

## 0.7.1

::: content

- Correções de bugs [#166](https://github.com/djlint/djLint/issues/166)
:::

## 0.7.0

::: content

- Adicionada configuração para tags HTML personalizadas
- Correções de bugs
:::

## 0.6.9

::: content

- Adicionados os perfis HTML e Angular
- Permitidas algumas entidades na regra #H023
- Correções de bugs
:::

## 0.6.8

::: content

- Correções de bugs
- Documentação atualizada
:::

## 0.6.7

::: content

- Adicionada a opção de configuração `format_attribute_template_tags`, opcional, para formatar tags de template dentro de atributos
- Adicionada a opção de configuração `linter_output_format` para personalizar a ordem das variáveis das mensagens do linter
- Adicionadas as regras H030 e H031 para verificar meta tags
:::

## 0.6.6

::: content

- Correções de bugs
:::

## 0.6.5

::: content

- Os caminhos na saída passaram a ser relativos à raiz do projeto
- Correções de bugs
:::

## 0.6.4

::: content

- Correções de bugs
:::

## 0.6.3

::: content

- Adicionado suporte à tag `blocktrans` do django
- Correções de bugs
:::

## 0.6.2

::: content

- Correções de bugs
:::

## 0.6.1

::: content

- Correções de bugs
- A regra T028 ficou mais rígida, com uma mensagem mais clara
:::

## 0.6.0

::: content

- Adicionada a regra T027 para verificar strings não fechadas na sintaxe de template
- Adicionada a regra T028 para verificar a falta de tags sem espaços em atributos
- Adicionada a regra H029 para verificar o method de formulários em minúsculas
- O formatador passou a ignorar as tags blocktranslate do django que não têm "trimmed"
- Correções de bugs
:::

## 0.5.9a

::: content

- Adicionado suporte a testes no python 3.10
- Adicionado hook de pre-commit
:::

## 0.5.9

::: content

- Adicionada a opção `--use-gitignore` para estender as exclusões
- Alterada a correspondência padrão de exclusões
- Corrigidos os caminhos de exclusão no windows
- Corrigida a formatação de tags `{%...%}` em atributos
- Corrigida a formatação de loops for e condições aninhadas em atributos
:::

## 0.5.8

::: content

- Adicionada a opção require_pragma
- A DJ018 foi atualizada para detectar `data-src` e `action` em inputs
- Corrigida a sintaxe de ignorar inline
- Adicionada a opção `--lint` como placeholder para o uso padrão
- Correções de bugs
:::

## 0.5.7

::: content

- Correções de bugs
:::

## 0.5.6

::: content

- Adicionada a regra H026 para encontrar tags id e class vazias
- Correções de bugs
:::

## 0.5.5

::: content

- Configurações consolidadas e código enxugado
- Correções de bugs
:::

## 0.5.4

::: content

- Adicionada a regra H020 para encontrar pares de tags vazios
- Adicionada a regra H021 para encontrar estilos inline
- Adicionada a regra H022 para encontrar links http
- Adicionada a regra H023 para encontrar referências de entidade
- Adicionada a regra H024 para encontrar type em scripts e estilos
- Adicionada a regra H025 para verificar tags órfãs. Agradecimentos a https://stackoverflow.com/a/1736801/10265880
- Melhorada a formatação de atributos
- A opção `blank_line_after_tag` foi atualizada para adicionar uma nova linha independentemente da posição
- Corrigida a formatação da tag `trans` do django
- Adicionada formatação para estilos inline
- Adicionada formatação para condições de template dentro de atributos
- Adicionado srcset como possível local de url nas regras do linter
- Formatação mais rápida
- Agradecimentos especiais a [jayvdb](https://github.com/jayvdb)
:::

## 0.5.3

::: content

- A stdout das opções `--reformat/check` foi alterada para imprimir apenas o novo html ao usar o stdin como entrada
:::

## 0.5.2

::: content

- O requisito de `alt` foi separado da H006 para a H013
- Adicionado um arquivo opcional de regras personalizadas
- Adicionado `golang` como opção de perfil
- Corrigida a formatação de blocos ignorados que contêm comentários inline
- Adicionado texto padrão às opções `--indent` e `-e`
- As regras de url foram atualizadas para aceitar #
- Corrigida a codificação de arquivos no Windows
- Corrigida a regex de tags de template de uma única linha
- Corrigido o `blank_line_after_tag` para tags com espaço no início
:::

## 0.5.1

::: content

- Adicionada a regra H019
- Corrigidos bugs na DJ018 e na H012
:::

## 0.5.0

::: content

- Corrigidos vários bugs de correspondência de regex nas regras do linter
- O linter deixou de retornar erros em blocos ignorados
- Adicionada a opção de ignorar um bloco de código no linter/formatador com as tags `{% djlint:off %}...{% djlint:on %}`
:::

## 0.4.9

::: content

- Corrigido o bug [#35](https://github.com/djlint/djLint/issues/35)
:::

## 0.4.8

::: content

- Corrigido o bug [#34](https://github.com/djlint/djLint/issues/34)
:::

## 0.4.7

::: content

- A tag `source` passou para as tags de uma única linha
:::

## 0.4.6

::: content

- Corrigido o bug [#31](https://github.com/djlint/djLint/issues/31)
:::

## 0.4.5

::: content

- Adicionadas as boas práticas à documentação
- Adicionada a opção `--profile` para definir as regras padrão do linter/formatador
- Adicionadas regras do linter para padrões de url do jinja
:::

## 0.4.4

::: content

- A configuração de indentação passou de string para int. `--indent 3`
:::

## 0.4.3

::: content

- Adicionada uma opção de CLI para o espaçamento da indentação. `--indent=" "`
:::

## 0.4.2

::: content

- Adicionado suporte a espaços em branco adicionais depois de tags com a opção `blank_line_after_tag`
:::

## 0.4.1

::: content

- Adicionado suporte ao processamento de vários arquivos ou pastas de uma só vez
:::

## 0.4.0

::: content

- Corrigida a formatação de tags `{# ... #}` do django
- Adicionado suporte a indentação para as tags figcaption, details e summary
- Adicionado suporte para sobrescrever ou estender a lista de caminhos excluídos no `pyproject.toml`
:::

## 0.3.9

::: content

- Atualizado o tratamento de atributos
:::

## 0.3.8

::: content

- Adicionado suporte ao stdin
:::

## 0.3.7

::: content

- Corrigida a formatação das tags `small`, `dt` e `dd`
:::

## 0.3.6

::: content

- Adicionado suporte do formatador a blocos de abertura `{%-` do Nunjucks
:::

## 0.3.5

::: content

- Adicionado suporte a mais blocos do Django
- Adicionado suporte a blocos personalizados
- Adicionado suporte a configuração no `pyproject.toml`
:::

## 0.3.4

::: content

- Corrigida a formatação da tag sem espaços `-%}` do Nunjucks
:::

## 0.3.3

::: content

- Tags `div` curtas agora podem ficar em uma única linha
:::

## 0.3.2

::: content

- Corrigida a formatação de comentários do Django
- O textarea passou a ser ignorado na formatação
:::

## 0.3.1

::: content

- Atualizada a regex de formatação de atributos
- Atualizada a regra de lint W010
:::

## 0.3.0

::: content

- O código de saída passou a ser 1 quando houver qualquer alteração de formatação
- Adicionado suporte às tags `asset` do Jinja
:::

## 0.2.9

::: content

- Atualizada a regex da W018
- Removidas mensagens de lint duplicadas
- Atualizada a E001 para o Handlebars
:::

## 0.2.8

::: content

- Corrigido o erro da barra de progresso em versões antigas do Click
:::

{% endraw %}
