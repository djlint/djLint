---
description: O linter de templates HTML do djLint inclui mais de 30 regras! Veja as definições aqui. Amplie facilmente com regras personalizadas!
title: Regras do linter
keywords: linter de templates, formatador de templates, djLint, HTML, templates, formatador, linter, regras
---

# Uso do linter

O djLint inclui muitas regras para verificar o estilo e a validade dos seus templates. Aproveite ao máximo o linter configurando-o para usar um perfil predefinido para a linguagem de template de sua preferência.

```bash
djlint /path/to/templates --lint

# com extensões personalizadas
djlint /path/to/templates -e html.dj --profile=django

# ou para um arquivo
djlint /path/to/this.html.j2  --profile=jinja
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Confira o guia de configuração para ver todas as opções!</a></div>
</div>

## Ativando ou desativando regras

A maioria das regras vem ativada por padrão. As regras podem ser desativadas na linha de comando com a flag `--ignore`. As regras podem ser ativadas com a flag `--include`.

Por exemplo:

```bash
djlint . --lint --include=H006,H017 --ignore=H013,H015
```

Isso também pode ser feito pelo arquivo de [{{ "configuration" | i18n }}]({{ "lang_code_url" | i18n }}/docs/configuration).

## Regras

| Código | Significado                                                                                                                | Padrão |
| ------ | -------------------------------------------------------------------------------------------------------------------------- | ------ |
| T001   | As variáveis devem ser envolvidas por espaços. Ex.: {% raw %}`{{ this }}`{% endraw %}                                      | ✔️     |
| T002   | Use aspas duplas nas tags. Ex. {% raw %}`{% extends "this.html" %}`{% endraw %}                                            | ✔️     |
| T003   | O endblock deve ter um nome. Ex.: {% raw %}`{% endblock body %}`{% endraw %}.                                              | -      |
| D004   | (Django) URLs estáticas devem seguir o padrão {% raw %}`{% static path/to/file %}`{% endraw %}.                            | ✔️     |
| J004   | (Jinja) URLs estáticas devem seguir o padrão {% raw %}`{{ url_for('static'..) }}`{% endraw %}.                             | ✔️     |
| H005   | A tag html deve ter um atributo `lang` não vazio.                                                                          | ✔️     |
| H006   | A tag `img` deve ter os atributos `height` e `width`.                                                                      | -      |
| H007   | `<!DOCTYPE ... >` deve estar presente antes da tag html.                                                                   | ✔️     |
| H008   | Os atributos devem usar aspas duplas.                                                                                      | ✔️     |
| H009   | Os nomes de tags devem estar em minúsculas.                                                                                | ✔️     |
| H010   | Os nomes de atributos devem estar em minúsculas.                                                                           | ✔️     |
| H011   | Os valores de atributos devem estar entre aspas.                                                                           | ✔️     |
| H012   | Não deve haver espaços em torno do `=` de um atributo.                                                                     | ✔️     |
| H013   | A tag `img` deve ter atributos alt.                                                                                        | ✔️     |
| H014   | Mais linhas em branco do que a configuração mantém.                                                                        | ✔️     |
| H015   | Coloque uma quebra de linha após as tags `h`.                                                                              | ✔️     |
| H016   | Falta a tag `title` no html.                                                                                               | ✔️     |
| H017   | As tags vazias (void) devem ser autofechadas (conflita com: H018).                                                         | -      |
| D018   | (Django) Links internos devem usar o padrão {% raw %}`{% url ... %}`{% endraw %}.                                          | ✔️     |
| H018   | As tags vazias (void) já são autofechadas por natureza e devem terminar com ">", não "/>" (conflita com: H017).            | -      |
| J018   | (Jinja) Links internos devem usar o padrão {% raw %}`{{ url_for() ... }}`{% endraw %}.                                     | ✔️     |
| H019   | Substitua `javascript:abc()` por um evento `on_` e uma URL real.                                                           | ✔️     |
| H020   | Par de tags vazio encontrado. Considere removê-lo.                                                                         | ✔️     |
| H021   | Evite estilos inline.                                                                                                      | ✔️     |
| H022   | Use HTTPS para links externos.                                                                                             | ✔️     |
| H023   | Não use referências de entidade.                                                                                           | ✔️     |
| H024   | Omita o type em scripts e estilos.                                                                                         | ✔️     |
| H025   | A tag parece estar órfã.                                                                                                   | ✔️     |
| H026   | Tags id e class vazias podem ser removidas.                                                                                | ✔️     |
| T027   | String não fechada encontrada na sintaxe de template.                                                                      | ✔️     |
| T028   | Considere usar tags sem espaços dentro de valores de atributos. {% raw %}`{%- if/for -%}`{% endraw %}                      | -      |
| H029   | Considere usar valores em minúsculas no method de formulários.                                                             | ✔️     |
| H030   | Considere adicionar uma meta description.                                                                                  | ✔️     |
| T032   | Espaço em branco extra encontrado em tags de template.                                                                     | ✔️     |
| H033   | Espaço em branco extra encontrado no action do formulário.                                                                 | ✔️     |
| T034   | Você quis usar {% raw %}{% ... %} em vez de {% ... }%? {% endraw %}                                                        | ✔️     |
| H036   | Não use tags `br` para criar espaçamento.                                                                                  | ✔️     |
| H037   | Atributo duplicado encontrado.                                                                                             | ✔️     |
| T038   | A tag de bloco não tem uma tag de fechamento correspondente.                                                               | ✔️     |
| T039   | Tag de template não fechada encontrada.                                                                                    | ✔️     |
| T040   | Nome de template ausente ou vazio na tag extends ou include.                                                               | ✔️     |
| H041   | A tag é fechada em um bloco de template diferente daquele em que foi aberta.                                               | ✔️     |
| T041   | A tag extends deve ser a primeira tag do template.                                                                         | ✔️     |
| H042   | O atributo for do label não corresponde a nenhum id de elemento neste arquivo.                                             | ✔️     |
| T042   | Conteúdo fora de um bloco não é renderizado em um template que estende outro.                                              | ✔️     |
| H043   | A tag button deve ter um atributo `type`.                                                                                  | ✔️     |
| T043   | O nome do bloco é usado mais de uma vez no template.                                                                       | ✔️     |
| H044   | O thead não deve misturar células `th` e `td`.                                                                             | ✔️     |
| T044   | A tag de saída contém uma palavra-chave de instrução; use uma tag de bloco.                                                | ✔️     |
| H045   | A tag iframe deve ter um atributo `title`.                                                                                 | ✔️     |
| T045   | Uma tag de template dentro de um comentário html continua sendo executada; use um comentário de template para desativá-la. | ✔️     |
| H046   | O tabindex não deve ser positivo.                                                                                          | ✔️     |
| H047   | O aria-hidden não deve ser definido em um elemento focalizável.                                                            | ✔️     |
| H048   | O atributo aria não é um dos definidos pela especificação.                                                                 | ✔️     |
| H049   | O viewport não deve impedir que a página seja ampliada.                                                                    | ✔️     |
| H050   | O elemento está obsoleto e deve ser substituído.                                                                           | ✔️     |
| H051   | O role não é um dos que o ARIA define para a marcação.                                                                     | ✔️     |
| H052   | O meta refresh não deve recarregar nem redirecionar a página com um temporizador.                                          | ✔️     |
| H053   | O id é usado mais de uma vez no arquivo.                                                                                   | ✔️     |
| H054   | Um elemento interativo não deve ficar aninhado dentro de outro.                                                            | ✔️     |
| H055   | O atributo lang deve ser uma tag de idioma, como en ou pt-BR.                                                              | ✔️     |
| H056   | O src não deve estar vazio.                                                                                                | ✔️     |
| H057   | O vídeo deve ter uma faixa de legendas.                                                                                    | ✔️     |

### Padrões de código

A primeira letra de um código segue este padrão:

::: content

- D: aplica-se especificamente ao Django
- H: aplica-se ao html
- J: aplica-se especificamente ao Jinja
- M: aplica-se especificamente ao Handlebars
- N: aplica-se especificamente ao Nunjucks
- T: aplica-se aos templates em geral
:::

### Detalhes das regras

<!-- oxfmt-ignore-start -->

{% raw %}

#### T001

`Variables should be wrapped in a whitespace.`

Uma sintaxe de template como `{{user.name}}`, sem espaçamento interno, é mais difícil de ler e de comparar em diffs, e um espaçamento inconsistente na base de código torna pouco confiáveis as refatorações baseadas em grep (buscar uma variável ou tag), porque a mesma expressão existe em várias grafias. Os guias de estilo do Django e do Jinja escrevem `{{ var }}` e `{% tag %}` com um único espaço.

Não se aplica aos perfis handlebars e golang.

Não faça:

```html
{{user.name}}
```

Faça:

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

Misturar aspas simples e duplas em tags de template (`{% extends %}`, `{% include %}`, `{% with %}`, `{% trans %}`, `{% now %}`) faz o mesmo nome de template aparecer em duas grafias, de modo que buscas e renomeações em massa deixam passar metade dos casos. Padronizar com aspas duplas mantém os argumentos das tags consistentes com as aspas dos atributos HTML no restante do arquivo.

Aspas simples dentro de valores de atributos HTML (por exemplo, `<span title="{% trans 'x' %}">`) não são apontadas, já que as aspas duplas do atributo obrigam o uso de aspas simples ali.

Com `quote_style = "single"`, a regra exige aspas simples, e o formatador as escreve.

O `--reformat` reescreve essas aspas para você, então uma ocorrência nunca exige trabalho manual.

Não faça:

```html
{% extends 'base.html' %}
```

Faça:

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

Quando um `{% block %}` se estende por muitas linhas ou há blocos aninhados, um `{% endblock %}` sem nome não dá nenhuma pista de qual bloco ele fecha, então é fácil fechar o bloco errado durante a edição; os templates filhos passam então a sobrescrever o conteúdo errado. Dar nome ao endblock documenta o pareamento e permite que tanto o djLint quanto o Django (que lança TemplateSyntaxError quando o nome do endblock não corresponde) detectem um bloco fechado no lugar errado. Os erros de pareamento (blocos não fechados, endblocks órfãos e nomes que não correspondem) são verificações de correção tratadas pela T038.

Desativada por padrão; ative com `--include=T003`. O `--name-endblocks` escreve o nome para você, então uma ocorrência nunca exige trabalho manual.

O nome não é exigido quando o bloco abre e fecha na mesma linha, por exemplo `{% block title %}``{% endblock %}`. O formatador move o conteúdo de um bloco que contém outras tags para linhas próprias, então um bloco escrito em uma única linha pode precisar de um nome depois de formatado; com `--name-endblocks`, o formatador também escreve esse nome.

Não faça:

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

Faça:

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Static urls should follow {% static path/to/file %} pattern.`

Escrever caminhos /static/ fixos no código ignora a tag `{% static %}` do Django, então os templates quebram quando o STATIC_URL muda (por exemplo, ao mover os assets para uma CDN ou fazer o deploy em um subcaminho) e nunca recebem os nomes de arquivo com hash do ManifestStaticFilesStorage, o que causa erros 404 ou assets desatualizados em cache em produção. A regra procura o prefixo literal `/static/`, então um projeto que serve seus arquivos estáticos a partir de outro caminho não é coberto.

Não faça:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Faça:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

Escrever caminhos /static/ fixos no código ignora o url_for('static', ...) do Flask/Jinja, então os assets retornam 404 quando a aplicação é montada sob um prefixo de URL ou quando a pasta ou o host estático muda, e as query strings de cache-busting adicionadas pelo framework se perdem. A regra procura o prefixo literal `/static/`, então um projeto que serve seus arquivos estáticos a partir de outro caminho não é coberto.

Não faça:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Faça:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have a non-empty lang attribute.`

Sem um atributo lang no `<html>`, os leitores de tela tentam adivinhar as regras de pronúncia e podem ler a página no idioma errado, e os navegadores não conseguem oferecer corretamente tradução, hifenização ou aspas adequadas ao idioma. Declarar o idioma da página é o critério de sucesso 3.1.1 (Nível A) das WCAG 2.1.

`lang=""` e um `lang` sem valor indicam que o idioma é desconhecido, então são relatados da mesma forma que um atributo ausente.

Não faça:

```html
<!DOCTYPE html>
<html>
</html>
```

Faça:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`Img tag should have height and width attributes.`

Desativada por padrão; ative com `--include=H006`.

Quando uma `<img>` não tem largura e altura, o navegador não consegue reservar espaço antes de baixar a imagem, então o conteúdo ao redor salta à medida que as imagens carregam. Esse deslocamento de layout piora o Cumulative Layout Shift (uma métrica das Core Web Vitals) e pode fazer o usuário clicar no lugar errado enquanto a página se acomoda.

Não faça:

```html
<img src="cat.png" alt="Cat">
```

Faça:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

Sem um `<!DOCTYPE>` antes da tag `<html>`, os navegadores renderizam a página em modo quirks, emulando o comportamento legado do box model e do layout, e o CSS é renderizado de forma inconsistente entre navegadores. Tags de template e comentários antes do doctype não são problema; apenas a própria tag `<html>` precisa ser precedida por ele.

Não faça:

```html
<html lang="en">
</html>
```

Faça:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Attributes should be double quoted.`

Estilos de aspas misturados tornam os valores dos atributos mais difíceis de ler e de buscar com grep, e valores entre aspas simples quebram assim que o conteúdo contém um apóstrofo. Aspas duplas são a convenção usada pelas especificações do HTML, pelos formatadores e pela maioria dos guias de estilo, então padronizar com elas mantém os templates consistentes com o ecossistema em geral.

Não faça:

```html
<div class='content'></div>
```

Faça:

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

Os parsers de HTML aceitam nomes de tags em maiúsculas, mas as serializações XHTML e XML diferenciam maiúsculas de minúsculas e os rejeitam, e misturar maiúsculas e minúsculas torna a busca de texto e a revisão de diffs pouco confiáveis (um grep por `<h1>` não encontra `<H1>`). Nomes de tags em minúsculas mantêm os templates portáveis e consistentes.

Não é relatada com `--ignore-case`, que instrui o formatador a não mexer em maiúsculas e minúsculas.

Não faça:

```html
<H1>Welcome</H1>
```

Faça:

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

Nomes de atributos em maiúsculas são inválidos nas serializações XHTML/XML e frustram a busca de texto nos templates (um grep por src= não encontra SRC=). O DOM normaliza de qualquer forma os nomes de atributos HTML para minúsculas, então grafias em maiúsculas adicionam inconsistência sem nenhum benefício. Apenas os nomes que o formatador converte para minúsculas são relatados: `class`, `id`, `src`, `width`, `height`, `alt`, `style`, `lang`, `title`, `media` e `srcset`. O `--reformat` os corrige para você, e um binding de framework como `:itemID` ou um nome mais longo como `data-ID` mantém suas maiúsculas e minúsculas.

Não é relatada com `--ignore-case`, que instrui o formatador a não mexer em maiúsculas e minúsculas.

Não faça:

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

Faça:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

Valores de atributos sem aspas terminam no primeiro espaço em branco, então um valor como class=btn primary descarta silenciosamente tudo o que vem depois do espaço (o navegador trata "primary" como um atributo booleano separado). Valores que vêm de variáveis de template são especialmente frágeis: qualquer espaço, "=" ou ">" renderizado corrompe a tag. As aspas deixam o limite do valor explícito e seguro.

Não faça:

```html
<div class=test></div>
```

Faça:

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

Com espaços em torno do "=", a tag é lida como três tokens separados e fica a uma edição de se desfazer: uma quebra de linha ou um corte no meio deixa um atributo booleano solto mais um texto avulso. Manter name="value" contíguo também é o que ferramentas simples de texto (grep, buscar e substituir) pressupõem, então um espaçamento misto torna os atributos difíceis de encontrar e refatorar com confiança. O `--reformat` remove os espaços para você.

Não faça:

```html
<div class = "test"></div>
```

Faça:

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

Sem um atributo alt, os leitores de tela anunciam o nome do arquivo da imagem ou nada, o que viola o critério 1.1.1 (Conteúdo não textual) das WCAG. O texto alternativo também é o que o usuário vê quando a imagem não carrega. Imagens decorativas devem ter um alt="" vazio explícito para que as tecnologias assistivas saibam que devem ignorá-las; isso também satisfaz esta regra.

Um `alt` sem valor equivale a `alt=""`, o caso da imagem decorativa, então é aceito.

Não faça:

```html
<img src="cat.jpg" height="200" width="300">
```

Faça:

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

Sequências de linhas em branco não têm efeito na página renderizada (o HTML colapsa os espaços em branco), mas incham os templates e geram diffs ruidosos quando as linhas vizinhas mudam. O formatador do djLint as remove completamente por padrão (mantendo no máximo `max_blank_lines` linhas em branco, cujo padrão é 0), então sequências remanescentes indicam código não formatado.

Não faça:

```html
<div>one</div>


<p>two</p>
```

Faça:

```html
<div>one</div>

<p>two</p>
```

#### H015

`Follow h tags with a line break.`

Os títulos são marcos de nível de bloco que definem a estrutura do documento; espremer o próximo elemento na mesma linha da tag h de fechamento esconde essa estrutura no código-fonte e faz com que edições em qualquer um dos elementos apareçam nos diffs como alterações em ambos. Uma quebra de linha após cada título mantém a estrutura visual do template alinhada com a estrutura renderizada.

Não faça:

```html
<h1>Heading</h1><p>Intro text.</p>
```

Faça:

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Missing title tag in html.`

A especificação do HTML exige um elemento title em todo documento. Sem ele, as abas do navegador, os favoritos e o histórico mostram uma URL crua em vez do nome da página, os mecanismos de busca perdem o rótulo principal da página e os usuários de leitores de tela perdem a primeira coisa anunciada no carregamento, o que viola o critério 2.4.2 (Página com título, Nível A) das WCAG.

Só é disparada em arquivos que contêm um documento `<html>`...`</html>` completo, então parciais e templates filhos que estendem um template base nunca são apontados. Shells de SPA que definem o título no lado do cliente ainda precisam de um `<title>` estático: é ele que aparece na primeira renderização, nos crawlers e quando o JavaScript falha.

Não faça:

```html
<html lang="en">
<body>Content</body>
</html>
```

Faça:

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

Templates que também precisam ser interpretados como XML/XHTML (ou alimentar ferramentas baseadas em XML) rejeitam elementos vazios escritos sem a barra de fechamento, e misturar `<br>` com `<br />` na base de código produz diffs inconsistentes. Esta regra impõe a convenção no estilo XHTML, para que todo elemento vazio seja fechado da mesma forma.

Desativada por padrão; ative com `--include=H017`. É mutuamente exclusiva com a H018; ative apenas uma das duas convenções. O `--close-void-tags` adiciona a barra às tags vazias do html para você. Um `<path>` de svg é mantido como foi escrito, então feche-o manualmente.

Não faça:

```html
<br>
<meta charset="utf-8">
```

Faça:

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Internal links should use the {% url ... %} pattern.`

URLs internas fixas no código ficam silenciosamente desatualizadas quando o caminho de uma rota muda no urls.py, produzindo links quebrados e actions de formulário mortas que nenhum teste do URLconf vai detectar. O `{% url %}` resolve o caminho a partir do nome da rota, então renomear um caminho atualiza todos os links de uma vez.

Não faça:

```html
<a href="/accounts/login">Login</a>
```

Faça:

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

No HTML living standard, a barra final em um elemento vazio não tem significado (o parser a ignora), então escrever `<br />` sugere um comportamento de autofechamento no estilo XML que o HTML não tem e pode levar quem lê a adicionar barras a tags não vazias, onde uma / avulsa é descartada silenciosamente e mascara bugs de tags não fechadas. Esta regra impõe terminações simples com > nos elementos vazios.

Desativada por padrão; ative com `--include=H018`. É mutuamente exclusiva com a H017; ative apenas uma das duas convenções. O `<path />` do SVG é uma exceção, já que SVG é XML e exige a barra. Não é relatada com `--close-void-tags`, já que o formatador passa a escrever a barra que esta regra aponta.

Não faça:

```html
<br />
<meta charset="utf-8" />
```

Faça:

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

URLs internas fixas no código quebram silenciosamente quando o caminho de uma rota muda ou quando a aplicação é montada sob um prefixo, deixando links mortos e actions de formulário que enviam para páginas 404. O url_for() monta a URL a partir do nome do endpoint, então as mudanças de rota se propagam automaticamente para todos os templates.

Não faça:

```html
<a href="/accounts/login">Login</a>
```

Faça:

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

URLs javascript: quebram o clique com o botão do meio e a opção de abrir em nova aba, não fazem nada quando o JavaScript está desativado ou não carrega, são bloqueadas por Content Security Policies rígidas e são um ponto clássico de injeção de XSS. Use uma URL real no href e associe o comportamento com um handler de evento. Com uma CSP rígida, os handlers inline on* também são bloqueados: o onclick mostrado é a correção mínima dentro do template; prefira associar o listener com addEventListener a partir de um arquivo de script.

Não faça:

```html
<a href="javascript:openPopup()">Open popup</a>
```

Faça:

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

Um par de tags vazio não renderiza nenhum conteúdo, mas ainda cria um nó no DOM que pode receber margens, bordas ou gaps de flex/grid das folhas de estilo, produzindo espaçamentos fantasmas difíceis de rastrear; geralmente é marcação que sobrou de uma edição anterior. Tags que ficam legitimamente vazias em marcação normal (td, th, li, dt, dd, slot) são exceções. Tags com qualquer atributo (pontos de montagem de JS como `<div id="app">``</div>`, elementos de fontes de ícones como `<i class="fa fa-user">``</i>`) também não são apontadas; apenas pares vazios totalmente sem atributos correspondem.

Não faça:

```html
<p>Saved.</p>
<span> </span>
```

Faça:

```html
<p>Saved.</p>
```

#### H021

`Inline styles should be avoided.`

Estilos inline têm especificidade maior do que qualquer seletor de folha de estilo, então sobrescrevê-los depois exige !important; são bloqueados por Content Security Policies sem 'unsafe-inline' em style-src; e espalham a apresentação pelos templates, de modo que uma mudança de tema ou de design exige editar a marcação em vez de uma única folha de estilo. Mova a declaração para uma classe CSS. Uma exceção legítima: templates de e-mail em HTML, em que muitos clientes de e-mail removem os blocos `<style>` e os estilos inline são a técnica padrão; exclua os diretórios dos seus templates de e-mail ou desative esta regra para eles.

Não faça:

```html
<div style="color: red;">Wrong username or password.</div>
```

Faça:

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

Sub-recursos em http:// simples em uma página servida por HTTPS são conteúdo misto: os navegadores bloqueiam de imediato scripts, folhas de estilo e iframes, e atualizam automaticamente ou emitem avisos para imagens. Um link `<a>` para uma página http:// não é conteúdo misto, mas ainda envia os visitantes por uma conexão não criptografada, sujeita a interceptação e adulteração. Referências a hosts internos que realmente não têm TLS também serão apontadas; silencie esses pontos com um bloco `{# djlint:off H022 #}` em vez de desativar a regra.

Não faça:

```html
<a href="http://example.com">Example</a>
```

Faça:

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

Documentos HTML5 são UTF-8, então o caractere literal funciona em qualquer lugar e é o que os revisores realmente leem; um erro de digitação em uma referência de entidade (por exemplo, `&mdsah;`) não é detectado pelo navegador e é renderizado literalmente como texto quebrado. O djLint permite as entidades que carregam sintaxe (`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;` e as chaves `&lbrace;` e `&rbrace;`, junto com `&percnt;`, `&num;` e `&dollar;`, que, escritas por extenso, completariam um delimitador de template) e as que nomeiam um caractere invisível, que por isso não pode ser revisado como literal: os espaços (`&nbsp;`, `&thinsp;`, `&hairsp;`), os joiners e marcas (`&zwnj;`, `&zwj;`, `&lrm;`, `&rlm;`) e `&shy;`, tanto na forma nomeada quanto na decimal e na hexadecimal.

O `--reformat` reescreve a entidade como o caractere para você, então uma ocorrência nunca exige trabalho manual. Uma entidade escrita dentro de uma tag de template faz parte da tag, e não da página, então nem a regra nem o formatador mexem nela. O `--no-entity-formatting` desativa a reescrita, mas mantém a regra ativa, então uma entidade continua sendo relatada. Adicione `H023` a `ignore` para manter as entidades.

Não faça:

```html
<p>Dates 1900 &mdash; 2000</p>
```

Faça:

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript e text/css são os padrões do HTML5 para `<script>` e `<style>`, então o atributo é um peso morto que o navegador ignora; a especificação do WHATWG diz explicitamente para omiti-lo. Removê-lo também evita strings MIME obsoletas que quebram o elemento quando copiadas para scripts de módulo (em que type="module" realmente importa).

Não faça:

```html
<script type="text/javascript" src="app.js">
```

Faça:

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

Uma tag sem a tag de abertura ou de fechamento correspondente obriga a recuperação de erros do navegador a adivinhar onde o elemento termina, então a marcação seguinte acaba engolida pelo elemento errado; o layout, os seletores CSS e as consultas ao DOM em JavaScript então quebram silenciosamente, e de formas diferentes em cada navegador. A H025 também relata um `<ol>` ou `<ul>` aberto dentro de um `<p>`: o parser de HTML fecha o parágrafo antes da lista, então a marcação nunca fica aninhada da forma como foi escrita.

Não faça:

```html
<div>
  <p>Hello</p>
```

Faça:

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Empty id and class tags can be removed.`

Nenhum seletor de classe ou de id corresponde a um atributo vazio, e um id vazio é HTML inválido (o valor do id não pode ser a string vazia). Um seletor de presença de atributo como `div[class]` ainda corresponde a ele, então removê-lo é perceptível para uma folha de estilo escrita dessa forma. Geralmente ele indica um bug de template em que uma variável deveria ter sido interpolada, então removê-lo ou preenchê-lo evita que esse bug fique escondido à vista de todos.

Não faça:

```html
<div id="" class="">content</div>
```

Faça:

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

Uma aspa aberta e nunca fechada dentro de `{% ... %}` ou `{{ ... }}` faz o motor de templates interpretar a tag de forma errada: o Django e o Jinja lançam um TemplateSyntaxError no momento da renderização ou engolem silenciosamente o restante dos argumentos da tag como conteúdo da string, então a página retorna um erro 500 ou é renderizada com argumentos faltando.

Não faça:

```html
{% trans "Welcome %}
```

Faça:

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

Desativada por padrão; ative com `--include=T028`.

O espaço em branco que uma tag sem espaços remove é um espaço que é renderizado, então aplique-a apenas onde o atributo não tem nada a perder. `alt="{%- if brand -%}Acme{%- endif -%} logo"` é renderizado como `Acmelogo`, e um `d="M12 {%- if big -%}20{%- endif -%} 4Z"` de svg vira outro caminho. É por isso que a regra é opcional.

Tags de template dentro de um valor de atributo emitem os espaços e quebras de linha ao seu redor no atributo renderizado, então um href ou src montado com tags `{% if %}`/`{% for %}` simples pode conter espaços avulsos e produzir URLs quebradas. As tags de controle de espaços do Jinja/Nunjucks (`{%- ... -%}`) removem esses espaços ao redor para que o atributo seja renderizado como um único valor limpo. O atributo class é uma exceção, já que espaços extras entre nomes de classes são inofensivos.

Não se aplica ao perfil django: as tags de template do Django não suportam o controle de espaços `{%- -%}`.

Não faça:

```html
<a href="{% if x %}/home{% endif %}"></a>
```

Faça:

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

A especificação do HTML define as palavras-chave do method de formulários em minúsculas (get, post); os navegadores só aceitam as variantes em maiúsculas por meio de uma correspondência alternativa que não diferencia maiúsculas de minúsculas. Manter a forma canônica em minúsculas deixa os templates consistentes e fáceis de buscar com grep, e evita reclamações de validadores rígidos e de toolchains baseadas em XHTML.

Não faça:

```html
<form method="POST"></form>
```

Faça:

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

Os mecanismos de busca usam a meta description como o trecho exibido abaixo do título da sua página nos resultados; sem ela, eles montam um trecho a partir de um texto qualquer da página, o que prejudica a taxa de cliques e gera prévias de link ruins quando a página é compartilhada.

Só é disparada em arquivos que contêm um documento `<html>`...`</html>` completo. O argumento do trecho se aplica a páginas indexadas publicamente; em aplicações protegidas por autenticação ou de intranet, esta regra costuma ser desativada.

Não faça:

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

Faça:

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

Sequências de espaços ou tabulações entre os argumentos de uma tag de template são ruído invisível: escondem diferenças reais nos diffs, podem dificultar a percepção de um argumento faltando e se afastam do estilo de espaço único que o formatador do djLint produz, causando reformatações desnecessárias. Espaços dentro de strings entre aspas são preservados e não são apontados.

Não faça:

```html
{% static  'css/style.css' %}
```

Faça:

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

Espaços no início ou no fim do valor do action de um formulário passam a fazer parte da URL renderizada. Os navegadores os removem ao interpretar o valor, mas clientes que não são navegadores e testes que usam o valor literal podem não remover, e, em torno de uma tag `{% url %}`, o espaço avulso quase sempre indica um erro de digitação que renderiza uma URL de envio que não corresponde a nenhuma rota no servidor.

Não faça:

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

Faça:

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Did you intend to use {% ... %} instead of {% ... }%?`

}% é quase sempre um erro de digitação de %}. O motor de templates não reconhece }% como delimitador de tag, então a tag nunca é interpretada: o texto cru {% ... }% vaza para o HTML renderizado, ou o motor lança um erro de sintaxe ao encontrar a tag não fechada.

Não faça:

```html
{% include "footer.html" }%
```

Faça:

```html
{% include "footer.html" %}
```

#### H036

`Do not use br tags for spacing.`

A especificação do html permite `<br>` apenas para uma quebra de linha que faz parte do próprio conteúdo, como em um endereço postal ou em um poema, e esse uso não é apontado. O que é relatado é o uso para apresentação que a especificação proíbe: uma sequência de duas ou mais quebras, que é espaço vertical, e uma quebra encostada na borda interna de um elemento de bloco, que não renderiza nada que a própria margem dele não renderizaria. Ambos quebram o refluxo do texto em larguras estreitas, e um leitor de tela anuncia uma quebra forçada onde não há nada a anunciar.

Não faça:

```html
<p>Shipping is free.<br><br>Delivery takes 3 days.</p>
```

Faça:

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

Atributos duplicados são HTML inválido, e os navegadores mantêm apenas a primeira ocorrência e descartam silenciosamente as demais, então o segundo valor de class ou de style nunca tem efeito, o que esconde bugs reais. A verificação entende templates: um atributo repetido em ramos mutuamente exclusivos (`{% if %}`/`{% else %}`) não é apontado, já que apenas uma das cópias pode ser renderizada.

Não faça:

```html
<div class="card" id="profile" class="active">...</div>
```

Faça:

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

Uma tag de bloco como `{% if %}`, `{% for %}` ou `{% macro %}` sem a tag de fechamento correspondente é um TemplateSyntaxError fatal no Django e no Jinja: a página falha ao ser renderizada no momento da requisição, e esta regra detecta isso antes do deploy. Ela também aponta tags de fechamento órfãs, sem tag de abertura, e blocos intercalados incorretamente (por exemplo, `{% if %}``{% for %}``{% endif %}`).

O pareamento de `{% block %}`/`{% endblock %}` e os nomes de endblock que não correspondem são verificados por esta regra; a T003 (desativada por padrão) exige, além disso, um nome em todo `{% endblock %}` de várias linhas. As tags de bloco personalizadas registradas via custom_blocks também são verificadas, incluindo a forma autofechada com / %}.

Não faça:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

Faça:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Unclosed template tag found.`

Uma tag de template aberta com `{{` ou `{%`, mas nunca fechada com o `}}` ou `%}` correspondente, não é interpretada como tag: o Django/Jinja lançam um TemplateSyntaxError ou renderizam as chaves cruas na página, e tudo até o próximo delimitador pode ser engolido silenciosamente. Esses erros de digitação (uma única chave faltando, um delimitador que não corresponde) passam despercebidos facilmente na revisão, porque o template ainda pode ser renderizado parcialmente.

Não faça:

```html
<p>{{ user.name }</p>
```

Faça:

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

Uma tag `{% extends %}` ou `{% include %}` com um nome de template ausente, vazio ou formado apenas por espaços não tem nada para carregar: o Django lança TemplateSyntaxError quando o nome está totalmente ausente, e TemplateDoesNotExist no momento da renderização quando está vazio, então a página retorna um erro 500 em produção, mesmo que o arquivo de template em si pareça sintaticamente plausível.

Não faça:

```html
{% extends "" %}
```

Faça:

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

Quando uma tag HTML é aberta em um `{% block %}` mas fechada em outro, um template filho que sobrescreve apenas um desses blocos herda metade do elemento, produzindo marcação desbalanceada na página renderizada; os navegadores então fecham ou reaninham os elementos de forma imprevisível, quebrando o layout e os seletores CSS longe do template que de fato foi editado. Manter cada elemento aberto e fechado dentro do mesmo bloco torna seguro sobrescrever cada bloco de forma independente.

Não faça:

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

Faça:

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

O Django se recusa a compilar um template em que outra tag vem antes do `{% extends %}`, e o texto escrito antes dele é renderizado, então vaza para a página antes de tudo o que o template pai produz. O Jinja também renderiza esse texto, e o nunjucks o descarta, então, em qualquer motor, o template não faz o que parece fazer.

Um comentário `{# #}` não renderiza nada e não conta, assim como nada dentro de um bloco `{% comment %}`, <code>{&#37; raw %}</code> ou `{% verbatim %}`, nomeado ou não, uma região `{# djlint:off #}` em qualquer uma das suas três grafias, ou front matter yaml. Um comentário html conta: o motor o escreve na página antes do doctype do template pai, que é justamente o vazamento de que trata esta regra. O mesmo vale para um bloco `{% blocktrans %}`, um bloco `{% filter %}` e um bloco `<?php ?>`, já que todos eles renderizam algo. Apenas o primeiro `{% extends %}` é verificado; um segundo é um erro à parte. Nos perfis jinja e nunjucks, uma tag de ramificação antes dele não conta, já que o jinja documenta `{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}` como a forma de escolher um template pai; o django lê o restante do template como parte do `{% extends %}` e depois rejeita o `{% endif %}`, então, nesse perfil, uma tag de ramificação conta.

Não se aplica aos perfis handlebars, golang, liquid e angular.

Não faça:

```html
{% load static %}
{% extends "base.html" %}
```

Faça:

```html
{% extends "base.html" %}
{% load static %}
```

#### H042

`Label for attribute has no matching element id in this file.`

A verificação só é executada em arquivos que ela consegue analisar com segurança: se o arquivo contém qualquer coisa que possa renderizar um id que este arquivo nunca mostra (uma saída `{{ ... }}`, como um widget de formulário, um `{% include %}` ou `{% extends %}`, ou uma tag de template não reconhecida), a regra fica em silêncio para esse arquivo. Onde ela é executada, um relato é uma associação realmente quebrada.

Não faça:

```html
<label for="email">Email</label>
<input id="username">
```

Faça:

```html
<label for="email">Email</label>
<input id="email">
```

#### T042

`Content outside a block is not rendered in a template that extends another.`

Quando um template estende outro, o template pai decide o que é gerado na saída e o filho apenas preenche os blocos do pai. Texto ou html escrito depois do `{% extends %}` e fora de qualquer `{% block %}` é descartado silenciosamente no momento da renderização, então um parágrafo que parece correto no código-fonte nunca chega à página.

Uma tag de template nesse lugar continua sendo executada, então `{% load %}`, `{% set %}` e um `{% if %}` em volta de um bloco são ignorados, assim como comentários `{# #}` e `{% comment %}`, comentários html, blocos <code>{&#37; raw %}</code> e `{% verbatim %}`, e o corpo de um `{% macro %}`, de um `{% set %}` em forma de bloco, de um `{% partialdef %}` ou de um `{% addtoblock %}`, que é capturado em vez de ir para a saída. O texto de um `{% blocktrans %}` é relatado, já que um `{% blocktrans %}` não é um `{% block %}`. Apenas o conteúdo depois da tag extends é considerado, e cada trecho contínuo dele é relatado uma única vez, no seu início.

O motor lê as tags de template antes do html, então um `{% extends %}` escrito dentro de um comentário html ou de um `<pre>` continua sendo executado e continua tornando o arquivo um template filho; apenas `{# #}`, `{% comment %}`, <code>{&#37; raw %}</code> e `{% verbatim %}` realmente o escondem. O texto dentro de um comentário html não chega a nenhum leitor de qualquer forma e não é relatado, mas as tags escritas ali continuam sendo lidas.

Não se aplica aos perfis handlebars, golang, liquid e angular.

Não faça:

```html
{% extends "base.html" %}
<p>This paragraph is never shown.</p>
{% block content %}
<h1>Welcome</h1>
{% endblock %}
```

Faça:

```html
{% extends "base.html" %}
{% block content %}
<h1>Welcome</h1>
<p>This paragraph is shown.</p>
{% endblock %}
```

#### H043

`Button tag should have a type attribute.`

Um `<button>` sem `type` assume `submit` por padrão, então um botão criado para executar um script também envia o formulário ao seu redor e a página é recarregada. Escrever o type explicitamente evita isso.

Não faça:

```html
<form>
  <button onclick="preview()">Preview</button>
</form>
```

Faça:

```html
<form>
  <button type="button" onclick="preview()">Preview</button>
</form>
```

#### T043

`Block name is used more than once in the template.`

O Django, o Jinja e o Nunjucks se recusam a interpretar um template que dá o mesmo nome a dois blocos, então a página simplesmente não carrega. Para os motores, não importa que os dois blocos estejam em ramos diferentes de um `{% if %}`, então cada nome de bloco precisa ser único em todo o template, quer os blocos estejam lado a lado, quer um esteja aninhado no outro.

Só `{% block %}` conta: um `{% blocktrans %}` não é um bloco, e um `{% endblock name %}` apenas nomeia o bloco que fecha. Os nomes são comparados como foram escritos, já que os motores tratam `Content` e `content` como dois blocos diferentes.

Só é ignorado o que o próprio motor nunca interpreta: um comentário de template, um bloco `{% comment %}`, o corpo de um <code>{&#37; raw %}</code> ou `{% verbatim %}` e uma região `djlint:off`. Um bloco escrito dentro de um comentário html, no corpo de um `<script>`, `<style>`, `<pre>` ou `<textarea>`, ou no corpo de um `{% filter %}` continua sendo contado, já que o motor lê tudo isso e lança o erro do nome duplicado da mesma forma.

Um `{% embed %}` abre um escopo próprio: os blocos dentro dele preenchem o template incorporado, e não este, então dois embeds do mesmo parcial podem, cada um, escrever `{% block body %}`. Um nome repetido dentro de um único embed continua sendo relatado.

Não se aplica aos perfis handlebars, golang, liquid e angular.

Não faça:

```html
{% block content %}{% endblock %}
{% block content %}{% endblock %}
```

Faça:

```html
{% block content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

#### H044

`Thead should not mix th and td cells.`

Cada linha é avaliada isoladamente, então a linha de explicação com `td` que a especificação do html coloca em um `thead` ao lado da linha de cabeçalhos não é uma mistura. Um `td` vazio abrindo a linha é a célula de canto de uma tabela com cabeçalhos ao longo da primeira coluna, que é a marcação recomendada pelo tutorial de acessibilidade do W3C, então ele é ignorado.

Um `th` e um `td` têm significados diferentes para um leitor de tela e geralmente CSS diferente, então uma única célula avulsa em uma linha de cabeçalho é lida como dado e recebe um estilo diferente das colunas ao lado. A mistura é html válido, e é isso que a torna difícil de perceber.

Não faça:

```html
<thead>
  <tr>
    <th>Name</th>
    <td>Size</td>
  </tr>
</thead>
```

Faça:

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

Não se aplica aos perfis golang, handlebars e angular.

Uma tag de saída imprime um valor, e `if`, `for`, `url`, `include` e as demais são instruções que pertencem a uma tag de bloco. O Django, o Jinja e o Nunjucks rejeitam `{{ if x }}` com um erro de sintaxe, e uma palavra-chave de fechamento sozinha, como `{{ endif }}`, é lida como uma variável que não renderiza nada, enquanto o bloco que ela deveria fechar continua aberto, então a página não carrega ou mostra o que a condição deveria ter escondido.

Uma palavra-chave sozinha é um nome de variável comum, então `{{ url }}`, `{{ url|default:"/" }}` e `{{ set.name }}` não são relatados. Só é relatada uma palavra-chave que recebe um argumento, além de uma palavra-chave de fechamento ou de ramificação sozinha, como `{{ endif }}` ou `{{ else }}`. Uma palavra-chave de controle como `if` ou `for` não pode iniciar uma expressão, então tudo o que vem depois dela é um argumento, inclusive um operador, e `{{ if -1 > count }}` é relatado. Os demais nomes também servem como variáveis e funções, e, para eles, só uma string entre aspas ou uma palavra conta como argumento, então uma expressão que por acaso começa com um deles é ignorada: `{{ url ~ "/x" }}`, `{{ url if url else "#" }}`, `{{ url ? url : '#' }}`, `{{ block ('title') }}`, `{{ block .super }}` e `{{ filter [0] }}` não geram nenhum relato.

O corpo de um bloco <code>{&#37; raw %}</code> ou `{% verbatim %}` é texto, e não sintaxe de template, e é ignorado, incluindo a forma nomeada `{% verbatim vueapp %}...{% endverbatim vueapp %}`, então um `{{ }}` do Vue ou do Handlebars protegido dessa forma não é relatado. Um `{{ }}` escrito dentro de um argumento entre aspas de uma tag de bloco, como em `{% trans "Write {{ if x }} instead" %}`, é texto que o motor imprime e também é ignorado.

Não faça:

```html
{{ if user.is_active }}
```

Faça:

```html
{% if user.is_active %}
```

#### H045

`Iframe tag should have a title attribute.`

Um leitor de tela anuncia um iframe pelo seu nome acessível. Sem ele, lê a url do frame, ou nada, e não há como saber qual é a página incorporada antes de entrar nela. As WCAG tratam disso no critério 4.1.2 Nome, Função, Valor, e tanto o axe quanto o html-validate trazem essa verificação por padrão.

O nome pode vir de `title`, `aria-label` ou `aria-labelledby`, e qualquer um dos três satisfaz a regra. Um nome escrito por uma tag de template conta, então um frame com título definido por página não é relatado.

Não faça:

```html
<iframe src="/report/"></iframe>
```

Faça:

```html
<iframe src="/report/" title="Quarterly report"></iframe>
```

#### T045

`Template tag inside an html comment still runs; use a template comment to disable it.`

Um comentário html esconde a marcação do navegador, não do motor de templates. `<!-- {% include "debug.html" %} -->` continua renderizando o arquivo, e `<!-- {% if debug %}...{% endif %} -->` continua sendo avaliado, no Django, no Jinja, no Nunjucks, no Handlebars e no Go, então uma tag comentada dessa forma continua sendo executada, e o que ela escreve vai parar dentro do comentário ou, se contiver `-->`, escapa dele. Só um comentário de template, `{# #}` no Django e no Jinja, `{{! }}` no Handlebars ou `{{/* */}}` no Go, impede que uma tag seja executada.

Só é relatada uma tag de instrução: `{% %}` nos perfis que a têm, uma seção, um fechamento ou um parcial do handlebars, e uma palavra-chave do Go como `{{if}}` ou `{{end}}`. Um valor impresso em um comentário, como em `<!-- built {{ version }} -->`, é um uso deliberado e é ignorado, assim como uma tag dentro de um comentário de template, de um bloco `{% comment %}` ou de um bloco raw, e um comentário condicional para o Internet Explorer, `<!--[if IE]> ... <![endif]-->`, cujo corpo é marcação para o navegador que ele indica.

Uma palavra-chave do Go sozinha é um nome de variável comum em qualquer outro motor, então `<!-- period {{ start }} to {{ end }} -->` e `<!-- Template: {{ template }} -->` são valores no Django, no Jinja, no Nunjucks, no Handlebars e no Liquid, e só são lidos como instruções com `--profile golang`. Uma que tenha um operando do Go, como `{{ if .X }}` e `{{ template "footer" . }}`, é uma instrução que nenhum outro motor imprime e é relatada com qualquer perfil. Da mesma forma, `{%` só é lido onde o motor o tem, então é texto com `--profile handlebars` e `--profile golang`, e uma abertura não seguida de nenhuma chave de fechamento, como em `<!-- battery at 50{% charge -->`, é a prosa que parece ser. Um comentário condicional é aquele escrito como tal, abrindo com `<!--[if` e fechado pelo seu `<![endif]-->`, em maiúsculas ou minúsculas; um que fique sem fechamento é o comentário comum que o navegador entende que ele é, e as tags dentro dele são relatadas.

Não faça:

```html
<!-- {% include "banner.html" %} -->
```

Faça:

```html
{# {% include "banner.html" %} #}
```

#### H046

`Tabindex should not be positive.`

Um `tabindex` positivo leva um elemento para o início da ordem de tabulação, à frente de tudo o que não tem um. Um só deles reorganiza a página inteira para quem usa o teclado, e a ordem passa então a ter de ser mantida manualmente em todo template que adiciona um controle. As WCAG tratam disso no critério 2.4.3 Ordem do foco.

`0` coloca um elemento na ordem de tabulação no lugar que o documento lhe dá, e `-1` o tira dela, mas o mantém focalizável por script. Nenhum dos dois é relatado, assim como um valor escrito por uma tag de template, cujo número não é conhecido aqui.

Não faça:

```html
<input tabindex="1">
```

Faça:

```html
<input tabindex="0">
```

#### H047

`Aria-hidden should not be set on a focusable element.`

`aria-hidden="true"` tira um elemento da árvore de acessibilidade, mas o deixa na ordem de tabulação, então quem usa o teclado ainda chega até ele e não ouve nada ser anunciado. Esconder um ícone decorativo é o uso comum do atributo e não é relatado; só é relatado um elemento que recebe foco por si só.

Um elemento é considerado focalizável quando é um `button`, `select`, `textarea`, `iframe` ou `summary`, um `a` ou `area` com `href`, um `input` que não seja hidden, um `audio` ou `video` com `controls`, ou qualquer elemento com `contenteditable` ou com um `tabindex` de `0` ou mais. Um controle `disabled`, ou com `tabindex="-1"`, já está fora da ordem de tabulação e é ignorado.

Não faça:

```html
<button aria-hidden="true">Close</button>
```

Faça:

```html
<button type="button" aria-label="Close"><span aria-hidden="true">x</span></button>
```

#### H048

`Aria attribute is not one the specification defines.`

Um atributo aria com erro de digitação não faz absolutamente nada. Nenhum navegador avisa, nenhum leitor de tela o relata, e a marcação continua com a aparência de ter sido tornada acessível, então um `aria-lable` pode ficar anos em um template enquanto o controle que ele deveria nomear continua sem nome.

Os nomes que a regra conhece são os que o ARIA define. Um binding escrito por um framework não é um nome aria simples, então `:aria-label`, `v-bind:aria-label` e `[attr.aria-label]` são ignorados.

Não faça:

```html
<button type="button" aria-lable="Close">x</button>
```

Faça:

```html
<button type="button" aria-label="Close">x</button>
```

#### H049

`Viewport should not stop the page being zoomed.`

`user-scalable=no`, e um `maximum-scale` abaixo de 2, impedem que uma página seja ampliada em um celular, o que, para muitas pessoas, é a única forma de lê-la. As WCAG exigem 200% no critério 1.4.4 Redimensionar texto. Os navegadores ignoram cada vez mais essa restrição, mas a tag ainda desativa o zoom onde quer que seja respeitada.

O name e o content são encontrados em qualquer ordem em que os dois sejam escritos.

Não faça:

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

Faça:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### H050

`Element is obsolete and should be replaced.`

`<center>`, `<font>`, `<big>`, `<strike>` e `<tt>` foram abandonados quando o css assumiu a apresentação, e `<marquee>`, `<blink>`, `<nobr>` e `<spacer>` nunca foram padrão. O html não define mais nenhum deles, então nada garante como um navegador vai dispô-los, e uma folha de estilo não consegue selecioná-los como seleciona uma classe.

Os elementos que a regra conhece são `acronym`, `applet`, `basefont`, `bgsound`, `big`, `blink`, `center`, `dir`, `font`, `frame`, `frameset`, `isindex`, `keygen`, `marquee`, `menuitem`, `nobr`, `noembed`, `noframes`, `plaintext`, `spacer`, `strike`, `tt` e `xmp`. Só a tag de abertura é relatada, então cada elemento é citado uma única vez, e um custom element cujo nome apenas começa com um deles, como `<font-picker>`, é ignorado.

Não faça:

```html
<center><font color="red">Warning</font></center>
```

Faça:

```html
<p class="warning">Warning</p>
```

#### H051

`Role is not one ARIA defines for markup.`

Um role que nenhuma especificação define é simplesmente descartado, e o elemento mantém o significado que já tinha, então `role="buton"` deixa um `<div>` como um `<div>`: nada para um leitor de tela, enquanto a marcação parece ter recebido uma finalidade. Nada avisa sobre isso, e é isso que faz valer a pena detectar o erro de digitação.

Os nomes que a regra conhece são os roles que o ARIA define para autores, junto com os que o DPUB-ARIA (`doc-chapter` e os demais) e o GRAPHICS-ARIA (`graphics-symbol` e os demais) acrescentam. Os roles abstratos do ARIA, como `landmark` e `sectionhead`, são relatados: a especificação diz que eles existem para construir a sua ontologia e não devem ser escritos na marcação.

Um `role` pode conter vários nomes, como uma lista de alternativas, e cada um é verificado. Um valor com sintaxe de template não pode ser conhecido e é ignorado, assim como um binding escrito por um framework, como em `:role` ou `[attr.role]`.

Não faça:

```html
<div role="buton">Save</div>
```

Faça:

```html
<button type="button">Save</button>
```

#### H052

`Meta refresh should not reload or redirect the page on a timer.`

Uma atualização temporizada tira a página de quem a está lendo. Quem lê devagar, usa um leitor de tela ou simplesmente foi interrompido perde o ponto em que estava, sem aviso e sem como impedir, o que viola o critério 2.2.1 Tempo ajustável das WCAG, e uma atualização que recarrega a mesma página descarta tudo o que foi digitado nela.

Um atraso de zero é um redirecionamento imediato, e não um temporizador, o que as WCAG permitem quando não é possível usar um redirecionamento no servidor, então ele não é relatado. Os dois atributos são encontrados em qualquer ordem em que sejam escritos.

Não faça:

```html
<meta http-equiv="refresh" content="30">
```

Faça:

```html
<meta http-equiv="refresh" content="0; url=/next-page">
```

#### H053

`Id is used more than once in the file.`

Um id nomeia um único elemento. Um segundo elemento com o mesmo id quebra `getElementById`, `<label for>`, links de fragmento e `aria-labelledby`: o navegador pega o primeiro e ignora silenciosamente os demais, então um label, um link ou um script vai parar no elemento errado sem nenhum aviso.

Dois ids em ramos exclusivos de um mesmo `{% if %}...{% else %}...{% endif %}` nunca são renderizados juntos, então não são relatados. Um loop `{% for %}` ou um `{% block %}` não é um ramo: um id dentro dele e o mesmo id fora dele são ambos renderizados, e o que vem depois é relatado. Um valor escrito por uma tag de template não pode ser conhecido e é ignorado, assim como um valor vazio. Os ids são comparados exatamente, como faz o navegador, então `save` e `Save` são dois ids diferentes.

Os ramos são lidos na linguagem em que o arquivo está escrito, e com qualquer espaçamento que a linguagem permita entre os delimitadores e o nome da tag: `{% elif %}` e `{% else %}`, `{% elsif %}` e `{% when %}` do liquid, `{{ else }}` do go, uma instrução de linha `% else:` do mako, e `{{else}}` do handlebars, o seu encadeamento `{{else if x}}` e a seção inversa de qualquer bloco `{{#helper}}`, incluindo helpers personalizados. O conteúdo de um `<template>` é um fragmento de documento próprio que o `getElementById` nunca alcança, então um id ali é comparado apenas com os ids desse mesmo `<template>`: dois templates podem conter, cada um, uma linha com o mesmo id, enquanto dois ids iguais dentro de um mesmo template continuam sendo relatados. Um id dentro de um comentário, do corpo de um <code>{&#37; raw %}</code> ou `{% verbatim %}`, ou de uma região `djlint:off` não é lido.

Não faça:

```html
<button type="submit" id="submit">Save</button>
<button type="submit" id="submit">Save and continue</button>
```

Faça:

```html
<button type="submit" id="submit">Save</button>
<button type="button" id="cancel">Cancel</button>
```

#### H054

`Interactive element should not be nested inside another.`

O html proíbe conteúdo interativo dentro de `<a>` e de `<button>`. Um botão dentro de um link, ou um link dentro de um botão, é marcação inválida que cada navegador corrige à sua maneira, e quem usa leitor de tela ou teclado recebe um único controle que se comporta como dois. O axe relata a mesma coisa como "nested-interactive".

Os contêineres observados são um `<a>` com `href` e um `<button>`, e os controles relatados dentro deles são um link com `href`, `button`, `input`, `select` e `textarea`. Um `<a>` sem `href` não é interativo e é ignorado de ambos os lados, assim como um input hidden ou um cujo type é escrito por uma tag de template. O conteúdo de um `<template>` não é renderizado onde é escrito, então um controle dentro dele não está aninhado no link ao seu redor, embora um aninhamento escrito dentro do template continue sendo relatado.

Um atributo é lido onde uma tag escreve um, e em nenhum outro lugar: o `href` de `{% if not href %}` nomeia uma variável, o de `{# href="{{ url }}" #}` está comentado e o de `data-attr=href` pertence a outro atributo, enquanto o `href` que um `{% if %}` escreve entre as suas tags é um atributo como qualquer outro. Um link ou botão deixado aberto termina junto com o elemento ao seu redor, como aconteceria em um navegador, então um único erro de digitação não faz o restante do arquivo ser relatado; um deixado aberto no nível superior não tem nada ao redor que o encerre e se estende até o fim do arquivo, onde a H025 também relata a tag órfã.

Não faça:

```html
<a href="/cart"><button>Add</button></a>
```

Faça:

```html
<a href="/cart" class="button">Add</a>
```

#### H055

`Lang attribute should be a language tag such as en or pt-BR.`

A H005 exige um `lang` no `<html>`, mas um valor como `lang="english"` ou `lang="en_US"` a satisfaz sem nomear nenhum idioma que um navegador conheça. Um leitor de tela passa então a usar a sua voz padrão, e a tradução e a hifenização escolhem as regras erradas ou nenhuma. O valor precisa ser uma tag BCP 47: duas ou três letras, seguidas de qualquer número de subtags de uma a oito letras ou dígitos, cada uma depois de um hífen, como em `en`, `pt-BR` ou `zh-Hant-TW`.

Só a tag `<html>` é verificada, assim como na H005. Um valor vazio fica a cargo daquela regra, enquanto um valor formado apenas por espaços é relatado aqui, já que a H005 o considera um valor. Um valor escrito por uma tag de template, como em `lang="{{ LANGUAGE_CODE }}"`, ou por um short echo do php, como em `lang="<?= $lang ?>"`, não pode ser conhecido e é ignorado, mas um valor que apenas começa com `$` ou `{`, como em `lang="$LANG"`, é lido como foi escrito. `xml:lang` ou `data-lang` não são lidos como `lang`, e um `>` escrito dentro de uma tag de template antes do atributo, como em `{% if a > b %}`, não o esconde.

Não faça:

```html
<html lang="english">
```

Faça:

```html
<html lang="en">
```

#### H056

`Src should not be empty.`

A especificação do html diz que um `src` vazio é inválido e avisa que o navegador o resolve em relação à url do próprio documento, então `<img src="">` busca a página de novo como imagem e `<script src=""></script>` a busca como script. Geralmente é um placeholder que um script deveria preencher, e a correção é remover o atributo, ou guardar o valor em um atributo data, até que exista um valor real. Um `src` escrito sem nenhum valor, como em `<img src>`, também é vazio e é relatado.

Só `img`, `script`, `iframe`, `embed`, `source`, `track`, `audio` e `video` são verificados, já que são esses os elementos que buscam o que o `src` indica. Só é relatado um valor que o navegador lê como vazio, então um valor sem aspas como `<img src=/static/logo.png>` é ignorado, assim como um valor formado apenas por espaços e um valor escrito por uma tag de template, e `srcset` e `data-src` são atributos diferentes, que a regra não avalia.

Não faça:

```html
<img src="" alt="Logo">
```

Faça:

```html
<img src="{% static 'logo.png' %}" alt="Logo">
```

#### H057

`Video should have a captions track.`

Um vídeo com som transmite a fala apenas no áudio, então um espectador surdo ou com deficiência auditiva não aproveita nada dele sem legendas, que o critério 1.2.2 Legendas (pré-gravadas) das WCAG exige. Um `<track>` com `kind` igual a `captions` ou `subtitles` dentro do `<video>` satisfaz a regra, assim como um `<track>` sem nenhum `kind`, já que `subtitles` é o padrão.

Um vídeo `muted` não tem áudio para legendar e não é relatado. Também não é relatado um vídeo cuja tag de abertura ou cujo corpo contenha uma tag de template, já que as faixas, ou o atributo `muted`, podem ser escritos pelo template onde o djLint não consegue vê-los. Uma tag de template é uma que uma linguagem de template abre, `{{`, `{%`, `{#` ou `${`, então um handler do jQuery como `onclick="$(this).play()"`, um `$refs` do Alpine, uma chave de css e um preço escrito no texto alternativo são o texto comum que parecem ser, e o vídeo continua sendo lido.

Só marcação conta como marcação. `muted` precisa ser o atributo, então `<video class=muted>` é uma classe chamada muted e é relatado, e um `<track>` comentado ou escrito dentro de um valor de atributo é texto, e não uma faixa. Um `</video>` dentro de um valor não encerra nada, e o elemento é avaliado onde a sua tag de fechamento real o fecha, então um `<video>` deixado aberto fica a cargo da `H025`.

Não faça:

```html
<video controls src="talk.mp4"></video>
```

Faça:

```html
<video controls src="talk.mp4">
  <track kind="captions" src="talk.vtt" srclang="en">
</video>
```

{% endraw %}

<!-- oxfmt-ignore-end -->

### Adicionando regras

Pull requests com novas regras são bem-vindos!

Uma boa regra é composta de

::: content

- Nome
- Código
- Mensagem - Mensagem a ser exibida quando o erro é encontrado.
- Flags - Flags de regex. O padrão é re.DOTALL. Ex.: re.I|re.M
- Padrões - expressões regulares que vão encontrar o erro.
- Exclusão - Lista opcional de perfis dos quais a regra deve ser excluída.
:::

Inclua um teste para validar a regra.

## Regras personalizadas

Você pode adicionar regras personalizadas só para o seu projeto criando um `.djlint_rules.yaml` ao lado do seu `pyproject.toml`. As regras podem ser adicionadas a esse arquivo, e o djLint vai carregá-las. Um arquivo de regras em outro local pode ser informado com a opção de CLI `--rules`.

### Regras de padrão

Você pode adicionar regras que falham se um dos padrões de regex encontrar uma correspondência:

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Regras com módulo Python

Você pode adicionar regras que importam e executam uma função Python personalizada:

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

O `python_module` especificado deve conter uma função `run()`, que será executada em cada arquivo verificado. Ela deve aceitar os seguintes argumentos:

::: content

- `rule`: O dict que representa a sua regra no `.djlint_rules.yaml`. Normalmente você vai usar essa variável para acessar o nome e a mensagem da regra.
- `config`: O objeto de configuração do DJLint.
- `html`: O conteúdo html completo do arquivo.
- `filepath`: O caminho do arquivo que está sendo verificado.
- `line_ends`: Lista das posições de caractere de `start` e `end` de cada linha, que você pode usar com `djlint.lint.get_line()` para obter números de linha a partir de uma posição de caractere. Veja o exemplo.
- `*args, **kwargs`: Podemos adicionar outros argumentos no futuro, então você deve incluir esses dois argumentos para reduzir o risco de falha ao atualizar o djLint.
:::

O módulo pode ficar na raiz do projeto. Se ele retornar uma `line` ou um `end` que não seja uma posição, o djLint para com um erro que indica o nome da regra.

Ela deve retornar uma lista de dicts, um para cada erro, com as seguintes chaves:

::: content

- `code`: O nome do código da regra que relata o erro (normalmente `rule['name']`)
- `line`: O número da linha e o número do caractere nessa linha, separados por ':', como string.
  Por exemplo, `"2:3"` significa que o erro foi encontrado na linha 2, caractere 3
- `end`: Opcional. Onde o erro termina, escrito como `line`, logo depois do seu último caractere. Sem ele, o erro termina onde o `match` termina.
- `match`: A parte do conteúdo que contém o erro
- `message`: A mensagem que será exibida para indicar o erro (normalmente `rule['message']`)
:::

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
