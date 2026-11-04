---
description: Las reglas del linter de plantillas HTML de djLint y cómo añadir las tuyas.
title: Reglas del linter
keywords: linter de plantillas, formateador de plantillas, djLint, HTML, plantillas, formateador, linter, reglas
---

# Uso del linter

djLint incluye muchas reglas para comprobar el estilo y la validez de tus plantillas. Saca el máximo partido al linter configurándolo con un perfil predefinido para el lenguaje de plantillas que elijas.

```bash
djlint /path/to/templates --lint

# con extensiones personalizadas
djlint /path/to/templates -e html.dj --profile=django

# o para un archivo
djlint /path/to/this.html.j2  --profile=jinja
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">¡Consulta la guía de configuración para ver todas las opciones!</a></div>
</div>

## Activar o desactivar reglas

La mayoría de las reglas están activadas por defecto. Las reglas se pueden desactivar en la línea de comandos con la opción `--ignore`, y activar con la opción `--include`.

Por ejemplo:

```bash
djlint . --lint --include=H006,H017 --ignore=H013,H015
```

También se puede hacer desde el archivo de [{{ "configuration" | i18n }}]({{ "lang_code_url" | i18n }}/docs/configuration).

## Reglas

| Código | Significado                                                                                                                   | Por defecto |
| ------ | ----------------------------------------------------------------------------------------------------------------------------- | ----------- |
| T001   | Las variables deben ir rodeadas de espacios. Ej.: {% raw %}`{{ this }}`{% endraw %}                                           | ✔️          |
| T002   | En las etiquetas deben usarse comillas dobles. Ej. {% raw %}`{% extends "this.html" %}`{% endraw %}                           | ✔️          |
| T003   | El endblock debe tener nombre. Ej.: {% raw %}`{% endblock body %}`{% endraw %}.                                               | -           |
| D004   | (Django) Las URL estáticas deben seguir el patrón {% raw %}`{% static path/to/file %}`{% endraw %}.                           | ✔️          |
| J004   | (Jinja) Las URL estáticas deben seguir el patrón {% raw %}`{{ url_for('static'..) }}`{% endraw %}.                            | ✔️          |
| H005   | La etiqueta html debe tener un atributo `lang` no vacío.                                                                      | ✔️          |
| H006   | La etiqueta `img` debe tener los atributos `height` y `width`.                                                                | -           |
| H007   | Debe haber un `<!DOCTYPE ... >` antes de la etiqueta html.                                                                    | ✔️          |
| H008   | Los atributos deben ir entre comillas dobles.                                                                                 | ✔️          |
| H009   | Los nombres de etiqueta deben ir en minúsculas.                                                                               | ✔️          |
| H010   | Los nombres de atributo deben ir en minúsculas.                                                                               | ✔️          |
| H011   | Los valores de atributo deben ir entre comillas.                                                                              | ✔️          |
| H012   | No debe haber espacios alrededor del `=` de un atributo.                                                                      | ✔️          |
| H013   | La etiqueta `img` debe tener atributos alt.                                                                                   | ✔️          |
| H014   | Más líneas en blanco de las que conserva la configuración.                                                                    | ✔️          |
| H015   | Pon un salto de línea después de las etiquetas `h`.                                                                           | ✔️          |
| H016   | Falta la etiqueta `title` en el html.                                                                                         | ✔️          |
| H017   | Las etiquetas vacías deben ser autocerradas (en conflicto con: H018).                                                         | -           |
| D018   | (Django) Los enlaces internos deben usar el patrón {% raw %}`{% url ... %}`{% endraw %}.                                      | ✔️          |
| H018   | Las etiquetas vacías se cierran solas por naturaleza y deben terminar en ">", no en "/>" (en conflicto con: H017).            | -           |
| J018   | (Jinja) Los enlaces internos deben usar el patrón {% raw %}`{{ url_for() ... }}`{% endraw %}.                                 | ✔️          |
| H019   | Sustituye `javascript:abc()` por un evento `on_` y una URL real.                                                              | ✔️          |
| H020   | Se encontró un par de etiquetas vacío. Plantéate eliminarlo.                                                                  | ✔️          |
| H021   | Deben evitarse los estilos en línea.                                                                                          | ✔️          |
| H022   | Usa HTTPS para los enlaces externos.                                                                                          | ✔️          |
| H023   | No uses referencias de entidad.                                                                                               | ✔️          |
| H024   | Omite el type en scripts y estilos.                                                                                           | ✔️          |
| H025   | La etiqueta parece huérfana.                                                                                                  | ✔️          |
| H026   | Las etiquetas id y class vacías se pueden eliminar.                                                                           | ✔️          |
| T027   | Se encontró una cadena sin cerrar en la sintaxis de plantilla.                                                                | ✔️          |
| T028   | Plantéate usar etiquetas con control de espacios dentro de los valores de atributo. {% raw %}`{%- if/for -%}`{% endraw %}     | -           |
| H029   | Plantéate usar valores en minúsculas para el method de los formularios.                                                       | ✔️          |
| H030   | Plantéate añadir una meta description.                                                                                        | ✔️          |
| T032   | Se encontraron espacios en blanco de más en las etiquetas de plantilla.                                                       | ✔️          |
| H033   | Se encontraron espacios en blanco de más en el action del formulario.                                                         | ✔️          |
| T034   | ¿Querías usar {% raw %}{% ... %} en lugar de {% ... }%? {% endraw %}                                                          | ✔️          |
| H036   | No uses etiquetas `br` para crear espacio.                                                                                    | ✔️          |
| H037   | Se encontró un atributo duplicado.                                                                                            | ✔️          |
| T038   | La etiqueta de bloque no tiene su etiqueta de cierre.                                                                         | ✔️          |
| T039   | Se encontró una etiqueta de plantilla sin cerrar.                                                                             | ✔️          |
| T040   | Falta el nombre de plantilla, o está vacío, en una etiqueta extends o include.                                                | ✔️          |
| H041   | La etiqueta se cierra en un bloque de plantilla distinto de aquel en el que se abrió.                                         | ✔️          |
| T041   | La etiqueta extends debe ser la primera etiqueta de la plantilla.                                                             | ✔️          |
| H042   | El atributo for de la etiqueta label no tiene ningún elemento con ese id en este archivo.                                     | ✔️          |
| T042   | El contenido fuera de un bloque no se renderiza en una plantilla que extiende otra.                                           | ✔️          |
| H043   | La etiqueta button debe tener un atributo `type`.                                                                             | ✔️          |
| T043   | El nombre de bloque se usa más de una vez en la plantilla.                                                                    | ✔️          |
| H044   | Thead no debe mezclar celdas `th` y `td`.                                                                                     | ✔️          |
| T044   | La etiqueta de salida contiene una palabra clave de sentencia; usa una etiqueta de bloque.                                    | ✔️          |
| H045   | La etiqueta iframe debe tener un atributo `title`.                                                                            | ✔️          |
| T045   | Una etiqueta de plantilla dentro de un comentario html se sigue ejecutando; usa un comentario de plantilla para desactivarla. | ✔️          |
| H046   | Tabindex no debe ser positivo.                                                                                                | ✔️          |
| H047   | No debe ponerse aria-hidden en un elemento que puede recibir el foco.                                                         | ✔️          |
| H048   | El atributo aria no es uno de los que define la especificación.                                                               | ✔️          |
| H049   | El viewport no debe impedir que se haga zoom en la página.                                                                    | ✔️          |
| H050   | El elemento está obsoleto y debe sustituirse.                                                                                 | ✔️          |
| H051   | El role no es uno de los que ARIA define para el marcado.                                                                     | ✔️          |
| H052   | Meta refresh no debe recargar ni redirigir la página con un temporizador.                                                     | ✔️          |
| H053   | El id se usa más de una vez en el archivo.                                                                                    | ✔️          |
| H054   | Un elemento interactivo no debe ir anidado dentro de otro.                                                                    | ✔️          |
| H055   | El atributo lang debe ser una etiqueta de idioma, como en o pt-BR.                                                            | ✔️          |
| H056   | Src no debe estar vacío.                                                                                                      | ✔️          |
| H057   | El vídeo debe tener una pista de subtítulos.                                                                                  | ✔️          |

### Patrones de los códigos

La primera letra de un código sigue este patrón:

::: content

- D: se aplica específicamente a Django
- H: se aplica a html
- J: se aplica específicamente a Jinja
- M: se aplica específicamente a Handlebars
- N: se aplica específicamente a Nunjucks
- T: se aplica a las plantillas en general
:::

### Detalles de las reglas

<!-- oxfmt-ignore-start -->

{% raw %}

#### T001

`Variables should be wrapped in a whitespace.`

Una sintaxis de plantilla como `{{user.name}}` sin espacios interiores es más difícil de leer de un vistazo y de comparar en un diff, y un espaciado incoherente en todo el código hace poco fiables las refactorizaciones basadas en grep (buscar una variable o una etiqueta), porque la misma expresión aparece escrita de varias formas. Las guías de estilo de Django y de Jinja escriben `{{ var }}` y `{% tag %}` con un solo espacio.

No se aplica a los perfiles handlebars y golang.

No hagas esto:

```html
{{user.name}}
```

Haz esto:

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

Mezclar comillas simples y dobles en las etiquetas de plantilla (`{% extends %}`, `{% include %}`, `{% with %}`, `{% trans %}`, `{% now %}`) hace que el mismo nombre de plantilla aparezca escrito de dos formas, así que las búsquedas y los cambios de nombre masivos se saltan la mitad de las apariciones. Usar siempre comillas dobles mantiene los argumentos de las etiquetas coherentes con el entrecomillado de los atributos HTML del resto del archivo.

Las comillas simples dentro de los valores de atributos HTML (p. ej., `<span title="{% trans 'x' %}">`) no se notifican, ya que las comillas dobles del atributo obligan a usar comillas simples ahí.

Con `quote_style = "single"`, la regla pide comillas simples en su lugar, y el formateador las escribe.

`--reformat` reescribe estas comillas por ti.

No hagas esto:

```html
{% extends 'base.html' %}
```

Haz esto:

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

Cuando un `{% block %}` abarca muchas líneas o hay bloques anidados, un `{% endblock %}` sin nombre no da ninguna pista de qué bloque cierra, así que es fácil cerrar el que no es al editar; las plantillas hijas acaban entonces sobrescribiendo el contenido equivocado. Ponerle nombre al endblock documenta la pareja y permite que tanto djLint como Django (que lanza TemplateSyntaxError cuando el nombre del endblock no coincide) detecten un bloque cerrado en el sitio equivocado. Los errores de emparejamiento (bloques sin cerrar, endblocks huérfanos y nombres que no coinciden) son comprobaciones de corrección de las que se encarga T038.

Desactivada por defecto; actívala con `--include=T003`. `--name-endblocks` escribe el nombre por ti.

No hace falta un nombre cuando el bloque se abre y se cierra en la misma línea, p. ej., `{% block title %}``{% endblock %}`. El formateador pasa a líneas propias el contenido de un bloque que contiene otras etiquetas, así que un bloque escrito en una sola línea puede necesitar un nombre una vez formateado; con `--name-endblocks`, el formateador también escribe ese nombre.

No hagas esto:

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

Haz esto:

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Static urls should follow {% static path/to/file %} pattern.`

Escribir a mano las rutas /static/ se salta la etiqueta `{% static %}` de Django, así que las plantillas se rompen cuando cambia STATIC_URL (p. ej., al mover los recursos a una CDN o al desplegar en una subruta) y nunca recogen los nombres de archivo con hash de ManifestStaticFilesStorage, lo que provoca errores 404 o recursos obsoletos en caché en producción. La regla busca el prefijo literal `/static/`, así que un proyecto que sirve sus archivos estáticos desde otra ruta no queda cubierto.

No hagas esto:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Haz esto:

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

Escribir a mano las rutas /static/ se salta el url_for('static', ...) de Flask/Jinja, así que los recursos dan 404 cuando la aplicación se monta bajo un prefijo de URL o cambia la carpeta o el host de los estáticos, y se pierden las cadenas de consulta para invalidar la caché que añade el framework. La regla busca el prefijo literal `/static/`, así que un proyecto que sirve sus archivos estáticos desde otra ruta no queda cubierto.

No hagas esto:

```html
<link rel="stylesheet" href="/static/css/style.css">
```

Haz esto:

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have a non-empty lang attribute.`

Sin un atributo lang en `<html>`, los lectores de pantalla adivinan las reglas de pronunciación y pueden leer la página en el idioma equivocado, y los navegadores no pueden ofrecer correctamente la traducción, la división de palabras ni las comillas propias del idioma. Declarar el idioma de la página es el criterio de conformidad 3.1.1 de las WCAG 2.1 (nivel A).

`lang=""` y un `lang` sin valor indican ambos que el idioma es desconocido, así que se notifican igual que si faltara el atributo.

No hagas esto:

```html
<!DOCTYPE html>
<html>
</html>
```

Haz esto:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`Img tag should have height and width attributes.`

Desactivada por defecto; actívala con `--include=H006`.

Cuando un `<img>` no tiene width ni height, el navegador no puede reservar espacio antes de que se descargue la imagen, así que el contenido de alrededor salta a medida que se cargan las imágenes. Este desplazamiento del diseño empeora el Cumulative Layout Shift (una métrica de las Core Web Vitals) y puede hacer que los usuarios hagan clic donde no querían mientras la página se estabiliza.

No hagas esto:

```html
<img src="cat.png" alt="Cat">
```

Haz esto:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

Sin un `<!DOCTYPE>` antes de la etiqueta `<html>`, los navegadores renderizan la página en modo quirks, emulando el antiguo modelo de caja y el comportamiento de diseño heredado, así que el CSS se renderiza de forma distinta en cada navegador. Las etiquetas de plantilla y los comentarios antes del doctype no son un problema; solo la etiqueta `<html>` en sí debe ir precedida por él.

No hagas esto:

```html
<html lang="en">
</html>
```

Haz esto:

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Attributes should be double quoted.`

Mezclar estilos de comillas hace que los valores de atributo sean más difíciles de leer de un vistazo y de buscar con grep, y los valores entre comillas simples se rompen en cuanto el contenido incluye un apóstrofo. Las comillas dobles son la convención que usan las especificaciones de HTML, los formateadores y la mayoría de las guías de estilo, así que usarlas siempre mantiene las plantillas coherentes con el resto del ecosistema.

No hagas esto:

```html
<div class='content'></div>
```

Haz esto:

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

Los analizadores de HTML aceptan nombres de etiqueta en mayúsculas, pero las serializaciones XHTML y XML distinguen mayúsculas y minúsculas y los rechazan, y mezclar mayúsculas y minúsculas hace poco fiables la búsqueda de texto y la revisión de diffs (buscar `<h1>` con grep no encuentra `<H1>`). Los nombres de etiqueta en minúsculas mantienen las plantillas portables y coherentes.

No se notifica con `--ignore-case`, que le indica al formateador que no toque las mayúsculas y minúsculas.

No hagas esto:

```html
<H1>Welcome</H1>
```

Haz esto:

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

Los nombres de atributo en mayúsculas no son válidos en las serializaciones XHTML/XML y frustran la búsqueda de texto en las plantillas (buscar src= con grep no encuentra SRC=). El DOM normaliza de todos modos los nombres de atributo HTML a minúsculas, así que escribirlos en mayúsculas añade incoherencia sin ningún beneficio. Solo se notifican los nombres que el formateador pasa a minúsculas: `class`, `id`, `src`, `width`, `height`, `alt`, `style`, `lang`, `title`, `media` y `srcset`. `--reformat` los corrige por ti, y un enlace de datos de un framework como `:itemID` o un nombre más largo como `data-ID` conserva sus mayúsculas.

No se notifica con `--ignore-case`, que le indica al formateador que no toque las mayúsculas y minúsculas.

No hagas esto:

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

Haz esto:

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

Los valores de atributo sin comillas terminan en el primer espacio en blanco, así que un valor como class=btn primary pierde sin avisar todo lo que va después del espacio (el navegador trata "primary" como un atributo booleano aparte). Los valores que vienen de variables de plantilla son especialmente frágiles: cualquier espacio, "=" o ">" que se renderice corrompe la etiqueta. Las comillas hacen explícito y seguro el límite del valor.

No hagas esto:

```html
<div class=test></div>
```

Haz esto:

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

HTML admite espacios en blanco alrededor del "=", así que esta es una regla de estilo. Escribir nombre="valor" sin espacios es el estilo habitual, y es lo que dan por hecho las herramientas de texto sencillas, como grep o buscar y reemplazar, así que un espaciado mezclado hace más difícil encontrar los atributos y refactorizarlos. `--reformat` quita los espacios por ti.

No hagas esto:

```html
<div class = "test"></div>
```

Haz esto:

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

Sin un atributo alt, los lectores de pantalla anuncian el nombre del archivo de la imagen o nada en absoluto, lo que incumple el criterio 1.1.1 de las WCAG (Contenido no textual). El texto alternativo es también lo que ven los usuarios cuando la imagen no se carga. Las imágenes decorativas deben llevar un alt="" vacío explícito para que las tecnologías de asistencia sepan que deben saltárselas; eso también cumple esta regla.

Un `alt` sin valor equivale a `alt=""`, el caso de la imagen decorativa, así que se acepta.

No hagas esto:

```html
<img src="cat.jpg" height="200" width="300">
```

Haz esto:

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

Las líneas en blanco seguidas no tienen ningún efecto en la página renderizada (HTML colapsa los espacios en blanco), pero inflan las plantillas y generan diffs ruidosos cuando cambian las líneas vecinas. El formateador de djLint las elimina por completo por defecto (conserva como mucho `max_blank_lines` líneas en blanco, que por defecto es 0), así que las que quedan indican código sin formatear.

No hagas esto:

```html
<div>one</div>


<p>two</p>
```

Haz esto:

```html
<div>one</div>

<p>two</p>
```

#### H015

`Follow h tags with a line break.`

Los encabezados son puntos de referencia de nivel de bloque que definen el esquema del documento; meter el siguiente elemento en la misma línea que la etiqueta h de cierre oculta esa estructura en el código fuente y hace que cualquier cambio en uno de los dos elementos aparezca en los diffs como un cambio en ambos. Un salto de línea después de cada encabezado mantiene la estructura visual de la plantilla alineada con el esquema renderizado.

No hagas esto:

```html
<h1>Heading</h1><p>Intro text.</p>
```

Haz esto:

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Missing title tag in html.`

La especificación de HTML exige un elemento title en todo documento. Sin él, las pestañas del navegador, los marcadores y el historial muestran una URL sin más en lugar del nombre de la página, los buscadores pierden la etiqueta principal de la página y los usuarios de lectores de pantalla pierden lo primero que se anuncia al cargarla, lo que incumple el criterio 2.4.2 de las WCAG (Titulado de páginas, nivel A).

Solo salta en archivos que contienen un documento `<html>`...`</html>` completo, así que nunca se notifican los parciales ni las plantillas hijas que extienden una base. Las aplicaciones SPA que definen el título en el cliente siguen necesitando un `<title>` estático: es lo que aparece en el primer renderizado, para los rastreadores y cuando falla JavaScript.

No hagas esto:

```html
<html lang="en">
<body>Content</body>
</html>
```

Haz esto:

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

Las plantillas que también deben poder analizarse como XML/XHTML (o alimentar herramientas basadas en XML) rechazan los elementos vacíos escritos sin barra de cierre, y mezclar `<br>` con `<br />` en el mismo código produce diffs incoherentes. Esta regla impone la convención de estilo XHTML para que todos los elementos vacíos se cierren de la misma manera.

Desactivada por defecto; actívala con `--include=H017`. Es mutuamente excluyente con H018; activa solo una de las dos convenciones. `--close-void-tags` añade la barra por ti a las etiquetas vacías de html. Un `<path>` de svg se deja como está escrito, así que ciérralo a mano.

No hagas esto:

```html
<br>
<meta charset="utf-8">
```

Haz esto:

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Internal links should use the {% url ... %} pattern.`

Las URL internas escritas a mano quedan obsoletas sin avisar cuando cambia la ruta en urls.py, lo que produce enlaces rotos y actions de formulario muertos que ninguna prueba sobre el URLconf detectará. `{% url %}` resuelve la ruta a partir del nombre de la ruta, así que al renombrar una ruta se actualizan todos los enlaces a la vez.

No hagas esto:

```html
<a href="/accounts/login">Login</a>
```

Haz esto:

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

En el HTML Living Standard, la barra final de un elemento vacío no significa nada (el analizador la ignora), así que escribir `<br />` sugiere un comportamiento de autocierre al estilo XML que HTML no tiene y puede llevar a quien lee a añadir barras a etiquetas que no son vacías, donde una / suelta se descarta sin avisar y oculta errores de etiquetas sin cerrar. Esta regla impone terminaciones > simples en los elementos vacíos.

Desactivada por defecto; actívala con `--include=H018`. Es mutuamente excluyente con H017; activa solo una de las dos convenciones. El `<path />` de SVG queda exento, ya que SVG es XML y exige la barra. No se notifica con `--close-void-tags`, ya que entonces el formateador escribe la barra que esta regla notifica.

No hagas esto:

```html
<br />
<meta charset="utf-8" />
```

Haz esto:

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

Las URL internas escritas a mano se rompen sin avisar cuando cambia la ruta o la aplicación se monta bajo un prefijo, lo que deja enlaces muertos y actions de formulario que envían a páginas 404. url_for() construye la URL a partir del nombre del endpoint, así que los cambios de ruta llegan automáticamente a todas las plantillas.

No hagas esto:

```html
<a href="/accounts/login">Login</a>
```

Haz esto:

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

Las URL javascript: rompen el clic con el botón central y la opción de abrir en una pestaña nueva, no hacen nada cuando JavaScript está desactivado o no se carga, las bloquean las Content Security Policies estrictas y son un punto clásico de inyección XSS. Usa una URL real en el href y asocia el comportamiento con un manejador de eventos. Con una CSP estricta, los manejadores on* en línea también se bloquean: el onclick del ejemplo es la corrección mínima dentro de la plantilla; es preferible asociar el listener con addEventListener desde un archivo de script.

No hagas esto:

```html
<a href="javascript:openPopup()">Open popup</a>
```

Haz esto:

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

Un par de etiquetas vacío no renderiza ningún contenido, pero sigue creando un nodo del DOM que puede recibir márgenes, bordes o huecos de flex/grid de las hojas de estilo, lo que produce espacios fantasma difíciles de rastrear; suele ser marcado sobrante de una edición anterior. Las etiquetas que están vacías legítimamente en el marcado normal (td, th, li, dt, dd, slot) quedan exentas. Las etiquetas con cualquier atributo (puntos de montaje de JS como `<div id="app">``</div>`, elementos de fuentes de iconos como `<i class="fa fa-user">``</i>`) tampoco se notifican; solo coinciden los pares vacíos sin ningún atributo.

No hagas esto:

```html
<p>Saved.</p>
<span> </span>
```

Haz esto:

```html
<p>Saved.</p>
```

#### H021

`Inline styles should be avoided.`

Los estilos en línea tienen más especificidad que cualquier selector de una hoja de estilo, así que para sobrescribirlos después hace falta !important; las Content Security Policies sin 'unsafe-inline' en style-src los bloquean; y dispersan la presentación por las plantillas, así que un cambio de tema o de diseño obliga a editar el marcado en lugar de una sola hoja de estilo. Pasa la declaración a una clase CSS. Una excepción legítima: las plantillas de correo HTML, donde muchos clientes de correo eliminan los bloques `<style>` y los estilos en línea son la técnica habitual; excluye los directorios de tus plantillas de correo o desactiva esta regla para ellos.

No hagas esto:

```html
<div style="color: red;">Wrong username or password.</div>
```

Haz esto:

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

Los subrecursos http:// sin cifrar en una página servida por HTTPS son contenido mixto: los navegadores bloquean directamente los scripts, las hojas de estilo y los iframes, y actualizan automáticamente las imágenes o muestran una advertencia. Un enlace `<a>` a una página http:// no es contenido mixto, pero aun así envía a los visitantes por una conexión sin cifrar, expuesta a interceptaciones y manipulaciones. También se notificarán las referencias a hosts internos que de verdad no tienen TLS; silencia esos puntos con un bloque `{# djlint:off H022 #}` en lugar de desactivar la regla.

No hagas esto:

```html
<a href="http://example.com">Example</a>
```

Haz esto:

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

Los documentos HTML5 son UTF-8, así que el carácter literal funciona en todas partes y es lo que de verdad leen los revisores; una errata en una referencia de entidad (p. ej., `&mdsah;`) no la detecta el navegador y se renderiza tal cual como texto roto. djLint permite las entidades que tienen función sintáctica (`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;`, y las llaves `&lbrace;` y `&rbrace;` junto con `&percnt;`, `&num;` y `&dollar;`, que escritas literalmente completarían un delimitador de plantilla) y las que nombran un carácter invisible, que por tanto no se puede revisar como literal: los espacios (`&nbsp;`, `&thinsp;`, `&hairsp;`), los caracteres de unión y las marcas (`&zwnj;`, `&zwj;`, `&lrm;`, `&rlm;`) y `&shy;`, tanto en forma con nombre como decimal o hexadecimal.

`--reformat` reescribe la entidad como el carácter por ti. Una entidad escrita dentro de una etiqueta de plantilla forma parte de la etiqueta y no de la página, así que ni la regla ni el formateador la tocan. `--no-entity-formatting` desactiva la reescritura pero deja la regla activa, así que la entidad se sigue notificando. Añade `H023` a `ignore` para conservar las entidades.

No hagas esto:

```html
<p>Dates 1900 &mdash; 2000</p>
```

Haz esto:

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript y text/css son los valores por defecto de HTML5 para `<script>` y `<style>`, así que el atributo es un peso muerto que el navegador ignora; la especificación del WHATWG dice explícitamente que se omita. Quitarlo también evita cadenas MIME obsoletas que rompen el elemento cuando se copian en scripts de módulo (donde type="module" sí importa).

No hagas esto:

```html
<script type="text/javascript" src="app.js">
```

Haz esto:

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

Una etiqueta sin su etiqueta de apertura o de cierre correspondiente obliga a la recuperación de errores del navegador a adivinar dónde termina el elemento, así que el marcado siguiente queda absorbido por el elemento equivocado; el diseño, los selectores CSS y las consultas al DOM desde JavaScript se rompen entonces sin avisar, y de forma distinta en cada navegador. H025 también notifica un `<ol>` o `<ul>` abierto dentro de un `<p>`: el analizador de HTML cierra el párrafo antes de la lista, así que el marcado nunca queda anidado como está escrito.

No hagas esto:

```html
<div>
  <p>Hello</p>
```

Haz esto:

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Empty id and class tags can be removed.`

Ningún selector de clase o de id coincide con un atributo vacío, y un id vacío es HTML no válido (el valor del id no puede ser la cadena vacía). Un selector de presencia de atributo como `div[class]` sí coincide con él, así que eliminarlo se nota en una hoja de estilo escrita de esa forma. Suele indicar un error en la plantilla, donde se pretendía interpolar una variable, así que eliminarlo o rellenarlo evita que ese error pase desapercibido.

No hagas esto:

```html
<div id="" class="">content</div>
```

Haz esto:

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

Una comilla que se abre pero nunca se cierra dentro de `{% ... %}` o `{{ ... }}` hace que el motor de plantillas interprete mal la etiqueta: Django y Jinja lanzan un TemplateSyntaxError al renderizar o absorben sin avisar el resto de los argumentos de la etiqueta como contenido de la cadena, así que la página da un error 500 o se renderiza sin algunos argumentos.

No hagas esto:

```html
{% trans "Welcome %}
```

Haz esto:

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

Desactivada por defecto; actívala con `--include=T028`.

Los espacios en blanco que elimina una etiqueta con control de espacios son espacios que se renderizan, así que aplica esto solo donde el atributo no tenga ninguno que perder. `alt="{%- if brand -%}Acme{%- endif -%} logo"` se renderiza como `Acmelogo`, y un `d="M12 {%- if big -%}20{%- endif -%} 4Z"` de svg se convierte en un trazado distinto. Por eso la regla hay que activarla expresamente.

Las etiquetas de plantilla dentro de un valor de atributo emiten al atributo renderizado los espacios y saltos de línea que las rodean, así que un href o src construido con etiquetas `{% if %}`/`{% for %}` normales puede contener espacios sueltos y producir URL rotas. Las etiquetas de control de espacios de Jinja/Nunjucks (`{%- ... -%}`) eliminan esos espacios de alrededor para que el atributo se renderice como un único valor limpio. El atributo class queda exento, ya que los espacios de más entre nombres de clase son inofensivos.

No se aplica al perfil django: las etiquetas de plantilla de Django no admiten el control de espacios `{%- -%}`.

No hagas esto:

```html
<a href="{% if x %}/home{% endif %}"></a>
```

Haz esto:

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

La especificación de HTML define las palabras clave del method de los formularios en minúsculas (get, post); los navegadores solo aceptan las variantes en mayúsculas porque comparan sin distinguir mayúsculas y minúsculas como alternativa. Mantener la forma canónica en minúsculas hace que las plantillas sean coherentes y fáciles de buscar con grep, y evita las quejas de los validadores estrictos y de las cadenas de herramientas basadas en XHTML.

No hagas esto:

```html
<form method="POST"></form>
```

Haz esto:

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

Los buscadores usan la meta description como el fragmento que aparece bajo el título de tu página en los resultados; sin ella, generan un fragmento a partir de un texto cualquiera de la página, lo que reduce la tasa de clics y produce vistas previas pobres cuando se comparte el enlace.

Solo salta en archivos que contienen un documento `<html>`...`</html>` completo. El argumento del fragmento se aplica a las páginas indexadas públicamente; en aplicaciones con inicio de sesión o de intranet, es habitual desactivar esta regla.

No hagas esto:

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

Haz esto:

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

Los espacios o tabulaciones seguidos entre los argumentos de una etiqueta de plantilla son ruido invisible: ocultan diferencias reales en los diffs, pueden dificultar ver que falta un argumento y se alejan del estilo de un solo espacio que produce el formateador de djLint, lo que provoca cambios de formato innecesarios. Los espacios dentro de las cadenas entre comillas se conservan y no se notifican.

No hagas esto:

```html
{% static  'css/style.css' %}
```

Haz esto:

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

Los espacios al principio o al final del valor del action de un formulario pasan a formar parte de la URL renderizada. Los navegadores los eliminan al analizarla, pero puede que los clientes que no son navegadores y las pruebas que usan el valor literal no lo hagan, y alrededor de una etiqueta `{% url %}` ese espacio suelto casi siempre indica una errata que produce una URL de envío que no coincide con ninguna ruta del servidor.

No hagas esto:

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

Haz esto:

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Did you intend to use {% ... %} instead of {% ... }%?`

}% es casi siempre una errata de %}. El motor de plantillas no reconoce }% como delimitador de etiqueta, así que la etiqueta nunca se interpreta: el texto {% ... }% en bruto se cuela en el HTML renderizado, o el motor lanza un error de sintaxis al encontrarse con la etiqueta sin cerrar.

No hagas esto:

```html
{% include "footer.html" }%
```

Haz esto:

```html
{% include "footer.html" %}
```

#### H036

`Do not use br tags for spacing.`

La especificación de html solo permite `<br>` para un salto de línea que forma parte del propio contenido, como en una dirección postal o un poema, y ese uso se respeta. Lo que se notifica es el uso presentacional que la especificación descarta: una serie de dos o más saltos, que es espacio vertical, y un salto pegado al borde interior de un elemento de bloque, que no renderiza nada que no hiciera ya su propio margen. Ambos rompen el reajuste del texto en anchos estrechos, y un lector de pantalla anuncia un salto forzado donde no hay nada que anunciar.

No hagas esto:

```html
<p>Shipping is free.<br><br>Delivery takes 3 days.</p>
```

Haz esto:

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

Los atributos duplicados son HTML no válido, y los navegadores conservan solo la primera aparición y descartan las demás sin avisar, así que el segundo valor de class o de style nunca surte efecto, lo que oculta errores reales. La comprobación tiene en cuenta la sintaxis de plantillas: un atributo repetido en ramas mutuamente excluyentes (`{% if %}`/`{% else %}`) no se notifica, ya que solo puede renderizarse una de las copias.

No hagas esto:

```html
<div class="card" id="profile" class="active">...</div>
```

Haz esto:

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

Una etiqueta de bloque como `{% if %}`, `{% for %}` o `{% macro %}` sin su etiqueta de cierre correspondiente es un TemplateSyntaxError seguro en Django y en Jinja: la página no se renderiza al recibir la petición, y esta regla lo detecta antes del despliegue. También notifica las etiquetas de cierre huérfanas, sin etiqueta de apertura, y los bloques mal entrelazados (p. ej., `{% if %}``{% for %}``{% endif %}`).

Esta regla comprueba el emparejamiento de `{% block %}`/`{% endblock %}` y los nombres de endblock que no coinciden; T003 (desactivada por defecto) exige además un nombre en cada `{% endblock %}` de varias líneas. También se comprueban las etiquetas de bloque personalizadas registradas mediante custom_blocks, incluida su forma autocerrada / %}.

No hagas esto:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

Haz esto:

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Unclosed template tag found.`

Una etiqueta de plantilla abierta con `{{` o `{%` pero nunca cerrada con su `}}` o `%}` correspondiente no se interpreta como etiqueta: Django/Jinja lanzan un TemplateSyntaxError o renderizan las llaves en bruto en la página, y todo lo que haya hasta el siguiente delimitador puede quedar absorbido sin avisar. Estas erratas (una sola llave que falta, un delimitador que no coincide) se pasan por alto fácilmente en una revisión, porque la plantilla puede seguir renderizándose en parte.

No hagas esto:

```html
<p>{{ user.name }</p>
```

Haz esto:

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

Una etiqueta `{% extends %}` o `{% include %}` cuyo nombre de plantilla falta, está vacío o solo contiene espacios no tiene nada que cargar: Django lanza TemplateSyntaxError cuando falta el nombre por completo, y TemplateDoesNotExist al renderizar cuando está vacío, así que la página da un error 500 en producción aunque el archivo de plantilla parezca sintácticamente correcto.

No hagas esto:

```html
{% extends "" %}
```

Haz esto:

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

Cuando una etiqueta HTML se abre en un `{% block %}` pero se cierra en otro, una plantilla hija que sobrescribe solo uno de esos bloques hereda la mitad del elemento, lo que produce marcado desequilibrado en la página renderizada; los navegadores entonces cierran o reanidan elementos de forma impredecible, y rompen el diseño y los selectores CSS lejos de la plantilla que de verdad se editó. Abrir y cerrar cada elemento dentro del mismo bloque permite sobrescribir cada bloque de forma independiente sin riesgo.

No hagas esto:

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

Haz esto:

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

Django se niega a compilar una plantilla en la que otra etiqueta va antes de `{% extends %}`, y el texto escrito antes se renderiza, así que se cuela en la página por delante de todo lo que produce la plantilla padre. Jinja también renderiza ese texto, y nunjucks lo descarta, así que en cualquier motor la plantilla no hace lo que parece que hace.

Un comentario `{# #}` no renderiza nada y no cuenta, como tampoco nada dentro de un bloque `{% comment %}`, <code>{&#37; raw %}</code> o `{% verbatim %}`, con nombre o sin él, una región `{# djlint:off #}` en cualquiera de sus tres formas, ni el front matter de yaml. Un comentario html sí cuenta: el motor lo escribe en la página por delante del doctype de la plantilla padre, que es justo la fuga de la que trata esta regla. También cuentan un bloque `{% blocktrans %}`, un bloque `{% filter %}` y un bloque `<?php ?>`, ya que cada uno de ellos renderiza algo. Solo se comprueba el primer `{% extends %}`; un segundo es un error en sí mismo. En los perfiles jinja y nunjucks, una etiqueta de rama antes de él no cuenta, ya que jinja documenta `{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}` como la forma de elegir una plantilla padre; django lee el resto de la plantilla dentro del `{% extends %}` y luego rechaza el `{% endif %}`, así que en ese perfil una etiqueta de rama sí cuenta.

No se aplica a los perfiles handlebars, golang, liquid y angular.

No hagas esto:

```html
{% load static %}
{% extends "base.html" %}
```

Haz esto:

```html
{% extends "base.html" %}
{% load static %}
```

#### H042

`Label for attribute has no matching element id in this file.`

La comprobación solo se ejecuta en los archivos que puede analizar con garantías: si el archivo contiene algo que podría renderizar un id que no aparece en él (una salida `{{ ... }}`, como un widget de formulario, un `{% include %}` o `{% extends %}`, o una etiqueta de plantilla no reconocida), la regla no dice nada sobre ese archivo. Donde sí se ejecuta, cada aviso es una asociación rota de verdad.

No hagas esto:

```html
<label for="email">Email</label>
<input id="username">
```

Haz esto:

```html
<label for="email">Email</label>
<input id="email">
```

#### T042

`Content outside a block is not rendered in a template that extends another.`

En cuanto una plantilla extiende otra, la plantilla padre decide qué se genera y la hija solo rellena los bloques de la padre. El texto o el html escrito después de `{% extends %}` y fuera de todo `{% block %}` se descarta sin avisar al renderizar, así que un párrafo que se ve bien en el código fuente nunca llega a la página.

Una etiqueta de plantilla en ese lugar sí se ejecuta, así que `{% load %}`, `{% set %}` y un `{% if %}` que envuelve un bloque se respetan, igual que los comentarios `{# #}` y `{% comment %}`, los comentarios html, los bloques <code>{&#37; raw %}</code> y `{% verbatim %}`, y el cuerpo de un `{% macro %}`, de un `{% set %}` en forma de bloque, de un `{% partialdef %}` o de un `{% addtoblock %}`, que se captura en lugar de generarse. El texto de un `{% blocktrans %}` sí se notifica, ya que un `{% blocktrans %}` no es un `{% block %}`. Solo se tiene en cuenta el contenido posterior a la etiqueta extends, y cada tramo de ese contenido se notifica una sola vez, en su inicio.

El motor lee las etiquetas de plantilla antes que el html, así que un `{% extends %}` escrito dentro de un comentario html o de un `<pre>` sigue ejecutándose y sigue convirtiendo el archivo en una plantilla hija; solo `{# #}`, `{% comment %}`, <code>{&#37; raw %}</code> y `{% verbatim %}` lo ocultan de verdad. El texto dentro de un comentario html no llega a ningún lector en ningún caso y no se notifica, pero las etiquetas escritas ahí se siguen leyendo.

No se aplica a los perfiles handlebars, golang, liquid y angular.

No hagas esto:

```html
{% extends "base.html" %}
<p>This paragraph is never shown.</p>
{% block content %}
<h1>Welcome</h1>
{% endblock %}
```

Haz esto:

```html
{% extends "base.html" %}
{% block content %}
<h1>Welcome</h1>
<p>This paragraph is shown.</p>
{% endblock %}
```

#### H043

`Button tag should have a type attribute.`

Un `<button>` sin `type` es `submit` por defecto, así que un botón escrito para ejecutar un script también envía el formulario que lo rodea y la página se recarga. Escribir el type explícitamente lo evita.

No hagas esto:

```html
<form>
  <button onclick="preview()">Preview</button>
</form>
```

Haz esto:

```html
<form>
  <button type="button" onclick="preview()">Preview</button>
</form>
```

#### T043

`Block name is used more than once in the template.`

Django, Jinja y Nunjucks se niegan a interpretar una plantilla que da el mismo nombre a dos bloques, así que la página no llega a cargarse. A los motores no les importa que los dos bloques estén en ramas distintas de un `{% if %}`, así que cada nombre de bloque tiene que ser único en toda la plantilla, tanto si los bloques están uno al lado del otro como si uno está anidado dentro del otro.

Solo cuenta `{% block %}`: un `{% blocktrans %}` no es un bloque, y un `{% endblock name %}` simplemente nombra el bloque que cierra. Los nombres se comparan tal como están escritos, ya que los motores tratan `Content` y `content` como dos bloques distintos.

Solo se omite lo que el propio motor nunca interpreta: un comentario de plantilla, un bloque `{% comment %}`, el cuerpo de un <code>{&#37; raw %}</code> o de un `{% verbatim %}` y una región `djlint:off`. Un bloque escrito dentro de un comentario html, del cuerpo de un `<script>`, `<style>`, `<pre>` o `<textarea>`, o del cuerpo de un `{% filter %}` sí se cuenta, ya que el motor lee todo eso y falla igualmente con el nombre duplicado.

Un `{% embed %}` abre un ámbito propio: los bloques que contiene rellenan la plantilla incrustada y no esta, así que dos embeds del mismo parcial pueden escribir cada uno `{% block body %}`. Un nombre repetido dentro de un mismo embed sí se notifica.

No se aplica a los perfiles handlebars, golang, liquid y angular.

No hagas esto:

```html
{% block content %}{% endblock %}
{% block content %}{% endblock %}
```

Haz esto:

```html
{% block content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

#### H044

`Thead should not mix th and td cells.`

Cada fila se evalúa por separado, así que la fila explicativa de celdas `td` que la especificación de html coloca en un `thead` junto a la fila de encabezados no es una mezcla. Un `td` vacío al principio de la fila es la celda de la esquina de una tabla con encabezados en su primera columna, que es el marcado que pide el tutorial de accesibilidad del W3C, así que se omite.

Un `th` y un `td` tienen un significado distinto para un lector de pantalla y normalmente un css distinto, así que una sola celda descolocada en una fila de encabezados se lee como un dato y tiene un estilo diferente al de las columnas de al lado. La mezcla es html válido, y eso es lo que la hace difícil de detectar.

No hagas esto:

```html
<thead>
  <tr>
    <th>Name</th>
    <td>Size</td>
  </tr>
</thead>
```

Haz esto:

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

No se aplica a los perfiles golang, handlebars y angular.

Una etiqueta de salida imprime un valor, mientras que `if`, `for`, `url`, `include` y las demás son sentencias que corresponden a una etiqueta de bloque. Django, Jinja y Nunjucks rechazan `{{ if x }}` con un error de sintaxis, y una palabra clave de cierre por sí sola, como `{{ endif }}`, se lee como una variable que no renderiza nada mientras el bloque que debía cerrar sigue abierto, así que la página no llega a cargarse o muestra lo que la condición debería haber ocultado.

Una palabra clave suelta es un nombre de variable corriente, así que `{{ url }}`, `{{ url|default:"/" }}` y `{{ set.name }}` no se notifican. Solo se notifica una palabra clave con un argumento, además de una palabra clave de cierre o de rama por sí sola, como `{{ endif }}` o `{{ else }}`. Una palabra clave de control como `if` o `for` no puede empezar una expresión, así que todo lo que venga después es un argumento, incluido un operador, y `{{ if -1 > count }}` se notifica. Los demás nombres sirven también como variables y funciones, y en ellos solo cuenta como argumento una cadena entre comillas o una palabra, así que una expresión que da la casualidad de empezar por uno de ellos se respeta: `{{ url ~ "/x" }}`, `{{ url if url else "#" }}`, `{{ url ? url : '#' }}`, `{{ block ('title') }}`, `{{ block .super }}` y `{{ filter [0] }}` no generan ningún aviso.

El cuerpo de un bloque <code>{&#37; raw %}</code> o `{% verbatim %}` es texto y no sintaxis de plantilla, así que se omite, incluida la forma con nombre `{% verbatim vueapp %}...{% endverbatim vueapp %}`, de modo que un `{{ }}` de Vue o de Handlebars protegido de esa forma no se notifica. Un `{{ }}` escrito dentro de un argumento entre comillas de una etiqueta de bloque, como en `{% trans "Write {{ if x }} instead" %}`, es texto que el motor imprime y también se respeta.

No hagas esto:

```html
{{ if user.is_active }}
```

Haz esto:

```html
{% if user.is_active %}
```

#### H045

`Iframe tag should have a title attribute.`

Un lector de pantalla anuncia un iframe por su nombre accesible. Sin él, lee en voz alta la url del marco, o nada en absoluto, y no hay forma de saber qué es la página incrustada antes de entrar en ella. Las WCAG lo recogen en el criterio 4.1.2 Nombre, función, valor, y tanto axe como html-validate incluyen esta comprobación por defecto.

El nombre puede venir de `title`, `aria-label` o `aria-labelledby`, y cualquiera de los tres cumple la regla. Un nombre escrito por una etiqueta de plantilla cuenta, así que un marco con un título distinto en cada página no se notifica.

No hagas esto:

```html
<iframe src="/report/"></iframe>
```

Haz esto:

```html
<iframe src="/report/" title="Quarterly report"></iframe>
```

#### T045

`Template tag inside an html comment still runs; use a template comment to disable it.`

Un comentario html oculta el marcado al navegador, no al motor de plantillas. `<!-- {% include "debug.html" %} -->` sigue renderizando el archivo, y `<!-- {% if debug %}...{% endif %} -->` se sigue evaluando, en Django, Jinja, Nunjucks, Handlebars y Go por igual, así que una etiqueta comentada de esta forma se sigue ejecutando, y lo que escriba acaba dentro del comentario o, si contiene `-->`, se sale de él. Solo un comentario de plantilla, `{# #}` en Django y Jinja, `{{! }}` en Handlebars o `{{/* */}}` en Go, impide que una etiqueta se ejecute.

Solo se notifican las etiquetas de sentencia: `{% %}` en los perfiles que la tienen, una sección, un cierre o un parcial de handlebars, y una palabra clave de Go como `{{if}}` o `{{end}}`. Un valor impreso dentro de un comentario, como en `<!-- built {{ version }} -->`, es un uso intencionado y se respeta, igual que una etiqueta dentro de un comentario de plantilla, de un bloque `{% comment %}` o de un bloque raw, y un comentario condicional para Internet Explorer, `<!--[if IE]> ... <![endif]-->`, cuyo cuerpo es marcado para el navegador que nombra.

Una palabra clave de Go suelta es un nombre de variable corriente en cualquier otro motor, así que `<!-- period {{ start }} to {{ end }} -->` y `<!-- Template: {{ template }} -->` son valores en Django, Jinja, Nunjucks, Handlebars y Liquid, y solo se leen como sentencias con `--profile golang`. Una que lleva un operando de Go, como `{{ if .X }}` y `{{ template "footer" . }}`, es una sentencia que ningún otro motor imprime y se notifica con cualquier perfil. `{%` también se lee solo donde el motor lo tiene, así que es texto con `--profile handlebars` y `--profile golang`, y una apertura a la que no sigue ninguna llave de cierre, como en `<!-- battery at 50{% charge -->`, es el texto normal que parece. Un comentario condicional es uno escrito como tal, que se abre con `<!--[if` y se cierra con su `<![endif]-->`, en mayúsculas o minúsculas; uno que se deja sin cerrar es el comentario corriente que el navegador ve en él, y las etiquetas que contiene se notifican.

No hagas esto:

```html
<!-- {% include "banner.html" %} -->
```

Haz esto:

```html
{# {% include "banner.html" %} #}
```

#### H046

`Tabindex should not be positive.`

Un `tabindex` positivo lleva un elemento al principio del orden de tabulación, por delante de todo lo que no lo tiene. Uno solo reorganiza toda la página para quien usa el teclado, y a partir de ahí el orden hay que mantenerlo a mano en cada plantilla que añada un control. Las WCAG lo recogen en el criterio 2.4.3 Orden del foco.

`0` coloca un elemento en el orden de tabulación en el lugar que le da el documento, y `-1` lo saca de ese orden sin que deje de poder recibir el foco desde un script. Ninguno de los dos se notifica, como tampoco un valor escrito por una etiqueta de plantilla, cuyo número aquí no se conoce.

No hagas esto:

```html
<input tabindex="1">
```

Haz esto:

```html
<input tabindex="0">
```

#### H047

`Aria-hidden should not be set on a focusable element.`

`aria-hidden="true"` saca un elemento del árbol de accesibilidad pero lo deja en el orden de tabulación, así que quien usa el teclado sigue llegando a él y no oye que se anuncie nada. Ocultar un icono decorativo es el uso normal del atributo y no se notifica; solo se notifica un elemento que recibe el foco por sí mismo.

Un elemento se considera enfocable cuando es un `button`, `select`, `textarea`, `iframe` o `summary`, un `a` o `area` con `href`, un `input` que no es de tipo hidden, un `audio` o `video` con `controls`, o cualquier elemento con `contenteditable` o con un `tabindex` de `0` o más. Un control `disabled`, o uno con `tabindex="-1"`, ya está fuera del orden de tabulación y se respeta.

No hagas esto:

```html
<button aria-hidden="true">Close</button>
```

Haz esto:

```html
<button type="button" aria-label="Close"><span aria-hidden="true">x</span></button>
```

#### H048

`Aria attribute is not one the specification defines.`

Un atributo aria mal escrito no hace absolutamente nada. Ningún navegador avisa, ningún lector de pantalla lo indica, y el marcado sigue dando la impresión de haberse hecho accesible, así que un `aria-lable` puede pasar años en una plantilla mientras el control al que debía dar nombre sigue sin tenerlo.

Los nombres que conoce la regla son los que define ARIA. Un enlace de datos escrito por un framework no es un nombre aria simple, así que `:aria-label`, `v-bind:aria-label` y `[attr.aria-label]` se respetan.

No hagas esto:

```html
<button type="button" aria-lable="Close">x</button>
```

Haz esto:

```html
<button type="button" aria-label="Close">x</button>
```

#### H049

`Viewport should not stop the page being zoomed.`

`user-scalable=no`, y un `maximum-scale` inferior a 2, impiden ampliar una página en un teléfono, que para mucha gente es la única forma de leerla. Las WCAG piden un 200 % en el criterio 1.4.4 Cambio de tamaño del texto. Los navegadores ignoran cada vez más esta restricción, pero la etiqueta sigue desactivando el zoom allí donde se respeta.

El nombre y el contenido se detectan en cualquier orden en que estén escritos.

No hagas esto:

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

Haz esto:

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### H050

`Element is obsolete and should be replaced.`

`<center>`, `<font>`, `<big>`, `<strike>` y `<tt>` se abandonaron cuando css asumió la presentación, y `<marquee>`, `<blink>`, `<nobr>` y `<spacer>` nunca fueron estándar. Html ya no define ninguno de ellos, así que nada garantiza cómo los compone un navegador, y una hoja de estilo no puede seleccionarlos como selecciona una clase.

Los elementos que conoce la regla son `acronym`, `applet`, `basefont`, `bgsound`, `big`, `blink`, `center`, `dir`, `font`, `frame`, `frameset`, `isindex`, `keygen`, `marquee`, `menuitem`, `nobr`, `noembed`, `noframes`, `plaintext`, `spacer`, `strike`, `tt` y `xmp`. Solo se notifica la etiqueta de apertura, así que cada elemento se nombra una sola vez, y un elemento personalizado cuyo nombre simplemente empieza por uno de ellos, como `<font-picker>`, se respeta.

No hagas esto:

```html
<center><font color="red">Warning</font></center>
```

Haz esto:

```html
<p class="warning">Warning</p>
```

#### H051

`Role is not one ARIA defines for markup.`

Un role que ninguna especificación nombra se descarta sin más y el elemento conserva el significado que ya tuviera, así que `role="buton"` deja un `<div>` como un `<div>`: nada para un lector de pantalla, mientras el marcado aparenta haberle dado una función. Nada avisa de ello, y eso es lo que hace que merezca la pena detectar la errata.

Los nombres que conoce la regla son los roles que ARIA define para los autores, junto con los que añaden DPUB-ARIA (`doc-chapter` y los demás) y GRAPHICS-ARIA (`graphics-symbol` y los demás). Los roles abstractos de ARIA, como `landmark` y `sectionhead`, se notifican: la especificación dice que existen para construir su ontología y que no deben escribirse en el marcado.

Un `role` puede contener varios nombres, como lista de alternativas, y se comprueba cada uno. Un valor que contiene sintaxis de plantilla no se puede conocer y se respeta, igual que un enlace de datos escrito por un framework, como en `:role` o `[attr.role]`.

No hagas esto:

```html
<div role="buton">Save</div>
```

Haz esto:

```html
<button type="button">Save</button>
```

#### H052

`Meta refresh should not reload or redirect the page on a timer.`

Una actualización temporizada cambia la página mientras alguien la está leyendo. Quien lee despacio, usa un lector de pantalla o simplemente ha sufrido una interrupción pierde el punto en el que estaba sin previo aviso y sin forma de impedirlo, lo que incumple el criterio 2.2.1 Tiempo ajustable de las WCAG, y una actualización que recarga la misma página descarta todo lo que se hubiera escrito en ella.

Un retraso de cero es una redirección inmediata y no un temporizador, algo que las WCAG permiten cuando no se puede usar una redirección del servidor, así que no se notifica. Los dos atributos se detectan en cualquier orden en que estén escritos.

No hagas esto:

```html
<meta http-equiv="refresh" content="30">
```

Haz esto:

```html
<meta http-equiv="refresh" content="0; url=/next-page">
```

#### H053

`Id is used more than once in the file.`

Un id nombra un único elemento. Un segundo elemento con el mismo id rompe `getElementById`, `<label for>`, los enlaces a fragmentos y `aria-labelledby`: el navegador toma el primero e ignora los demás sin avisar, así que una etiqueta, un enlace o un script acaba en el elemento equivocado sin ninguna advertencia.

Dos ids en ramas excluyentes de un mismo `{% if %}...{% else %}...{% endif %}` nunca se renderizan a la vez, así que no se notifican. Un bucle `{% for %}` o un `{% block %}` no es una rama: un id dentro de uno y el mismo id fuera de él se renderizan los dos, y se notifica el segundo. Un valor escrito por una etiqueta de plantilla no se puede conocer y se respeta, igual que un valor vacío. Los ids se comparan de forma exacta, como hace el navegador, así que `save` y `Save` son dos ids distintos.

Las ramas se leen en el lenguaje en que esté escrito el archivo, y con cualquier espacio en blanco que el lenguaje permita entre los delimitadores y el nombre de la etiqueta: `{% elif %}` y `{% else %}`, `{% elsif %}` y `{% when %}` de liquid, `{{ else }}` de go, una sentencia de línea `% else:` de mako, y `{{else}}` de handlebars, su forma encadenada `{{else if x}}` y la sección inversa de cualquier bloque `{{#helper}}`, incluidos los helpers personalizados. El contenido de un `<template>` es un fragmento de documento independiente al que `getElementById` nunca llega, así que un id ahí dentro solo se compara con los ids de ese mismo `<template>`: dos plantillas pueden contener cada una una fila con el mismo id, mientras que dos dentro de una misma plantilla sí se notifican. Un id dentro de un comentario, del cuerpo de un <code>{&#37; raw %}</code> o `{% verbatim %}`, o de una región `djlint:off` no se lee en absoluto.

No hagas esto:

```html
<button type="submit" id="submit">Save</button>
<button type="submit" id="submit">Save and continue</button>
```

Haz esto:

```html
<button type="submit" id="submit">Save</button>
<button type="button" id="cancel">Cancel</button>
```

#### H054

`Interactive element should not be nested inside another.`

Html prohíbe el contenido interactivo dentro de `<a>` y de `<button>`. Un botón dentro de un enlace, o un enlace dentro de un botón, es marcado no válido que cada navegador repara a su manera, y quien usa un lector de pantalla o el teclado recibe un solo control que se comporta como dos. axe informa de lo mismo como "nested-interactive".

Los contenedores que se vigilan son un `<a>` con `href` y un `<button>`, y los controles que se notifican dentro de ellos son un enlace con `href`, `button`, `input`, `select` y `textarea`. Un `<a>` sin `href` no es interactivo y se respeta en ambos lados, igual que un input de tipo hidden o uno cuyo type escribe una etiqueta de plantilla. El contenido de un `<template>` no se renderiza donde está escrito, así que un control dentro de uno no está anidado en el enlace que lo rodea, aunque el anidamiento escrito dentro de la plantilla sí se notifica.

Un atributo se lee donde una etiqueta lo escribe y en ningún otro sitio: el `href` de `{% if not href %}` nombra una variable, el de `{# href="{{ url }}" #}` está comentado y el de `data-attr=href` pertenece a otro atributo, mientras que el `href` que un `{% if %}` escribe entre sus propias etiquetas es un atributo como cualquier otro. Un enlace o un botón que se deja abierto termina con el elemento que lo rodea, como ocurriría en un navegador, así que una errata no hace que se notifique el resto del archivo; uno que se deja abierto en el nivel superior no tiene nada alrededor que lo termine y sí llega hasta el final del archivo, donde H025 también notifica la etiqueta huérfana.

No hagas esto:

```html
<a href="/cart"><button>Add</button></a>
```

Haz esto:

```html
<a href="/cart" class="button">Add</a>
```

#### H055

`Lang attribute should be a language tag such as en or pt-BR.`

H005 pide un `lang` en `<html>`, pero un valor como `lang="english"` o `lang="en_US"` lo cumple sin nombrar ningún idioma que conozca un navegador. Un lector de pantalla recurre entonces a su voz por defecto, y la traducción y la división de palabras eligen reglas equivocadas o ninguna. El valor tiene que ser una etiqueta BCP 47: dos o tres letras y después cualquier número de subetiquetas de una a ocho letras o dígitos, cada una tras un guion, como en `en`, `pt-BR` o `zh-Hant-TW`.

Solo se comprueba la etiqueta `<html>`, igual que en H005. Un valor vacío se deja a esa regla, mientras que un valor que solo contiene espacios se notifica aquí, ya que H005 lo lee como un valor. Un valor escrito por una etiqueta de plantilla, como en `lang="{{ LANGUAGE_CODE }}"`, o por un echo corto de php, como en `lang="<?= $lang ?>"`, no se puede conocer y se respeta, pero un valor que simplemente empieza por `$` o `{`, como en `lang="$LANG"`, se lee tal como está escrito. `xml:lang` o `data-lang` no se leen como `lang`, y un `>` escrito dentro de una etiqueta de plantilla antes del atributo, como en `{% if a > b %}`, no lo oculta.

No hagas esto:

```html
<html lang="english">
```

Haz esto:

```html
<html lang="en">
```

#### H056

`Src should not be empty.`

La especificación de html dice que un `src` vacío no es válido, y advierte de que el navegador lo resuelve con respecto a la url del propio documento, así que `<img src="">` vuelve a pedir la página como imagen y `<script src=""></script>` la pide como script. Suele ser un marcador de posición que un script debía rellenar, y la solución es quitar el atributo, o guardar el valor en un atributo data, hasta que haya uno real. Un `src` escrito sin ningún valor, como en `<img src>`, también está vacío y se notifica.

Solo se comprueban `img`, `script`, `iframe`, `embed`, `source`, `track`, `audio` y `video`, ya que son los elementos que descargan lo que nombra `src`. Solo se notifica un valor que el navegador lee como vacío, así que un valor sin comillas como `<img src=/static/logo.png>` se respeta, igual que un valor que solo contiene espacios y un valor escrito por una etiqueta de plantilla, y `srcset` y `data-src` son atributos distintos que la regla no evalúa.

No hagas esto:

```html
<img src="" alt="Logo">
```

Haz esto:

```html
<img src="{% static 'logo.png' %}" alt="Logo">
```

#### H057

`Video should have a captions track.`

Un vídeo con sonido transmite el habla solo a través del audio, así que una persona sorda o con dificultades auditivas no obtiene nada de él sin subtítulos, que exige el criterio 1.2.2 Subtítulos (grabados) de las WCAG. Un `<track>` con un `kind` de `captions` o `subtitles` dentro del `<video>` cumple la regla, igual que un `<track>` sin ningún `kind`, ya que `subtitles` es el valor por defecto.

Un vídeo `muted` no tiene audio que subtitular y no se notifica. Tampoco un vídeo cuya etiqueta de apertura o cuyo cuerpo contiene una etiqueta de plantilla, ya que las pistas, o el atributo `muted`, pueden estar escritos por la plantilla donde djLint no los ve. Una etiqueta de plantilla es una que abre un lenguaje de plantillas, `{{`, `{%`, `{#` o `${`, así que un manejador de jQuery como `onclick="$(this).play()"`, un `$refs` de Alpine, una llave de css y un precio escrito en el texto alternativo son el texto normal que parecen, y el vídeo se sigue leyendo.

`muted` tiene que ser el atributo, así que `<video class=muted>` es una clase llamada muted y se notifica, y un `<track>` comentado o escrito dentro de un valor de atributo es texto y no una pista. Un `</video>` dentro de un valor no cierra nada, y el elemento se evalúa donde lo cierra su verdadera etiqueta de cierre, así que un `<video>` que se deja abierto se deja a `H025`.

No hagas esto:

```html
<video controls src="talk.mp4"></video>
```

Haz esto:

```html
<video controls src="talk.mp4">
  <track kind="captions" src="talk.vtt" srclang="en">
</video>
```

{% endraw %}

<!-- oxfmt-ignore-end -->

### Añadir reglas

¡Las pull requests con reglas nuevas son bienvenidas!

Una buena regla consta de

::: content

- Nombre
- Código
- Mensaje: el mensaje que se muestra cuando se encuentra el error.
- Flags: flags de la expresión regular, por ejemplo re.I|re.M. Por defecto, re.DOTALL.
- Patrones: expresiones regulares que encuentran el error.
- Exclusiones: lista opcional de perfiles a los que no se aplica la regla.
:::

Incluye una prueba que valide la regla.

## Reglas personalizadas

Puedes añadir reglas personalizadas solo para tu proyecto creando un archivo `.djlint_rules.yaml` junto a tu `pyproject.toml`. Puedes añadir reglas a este archivo y djLint las tendrá en cuenta. Se puede indicar un archivo de reglas en otra ubicación con la opción `--rules` de la línea de comandos.

### Reglas de patrón

Puedes añadir reglas que fallan si alguno de los patrones de expresión regular encuentra una coincidencia:

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Reglas con módulos de Python

Puedes añadir reglas que importan y ejecutan una función de Python personalizada:

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

El `python_module` indicado debe contener una función `run()` que se ejecutará en cada archivo comprobado. Debe aceptar los siguientes argumentos:

::: content

- `rule`: el dict que representa tu regla en `.djlint_rules.yaml`. Normalmente usarás esta variable para acceder al nombre y al mensaje de la regla.
- `config`: el objeto de configuración de djLint.
- `html`: el contenido html completo del archivo.
- `filepath`: la ruta del archivo que se está comprobando.
- `line_ends`: lista con las posiciones de carácter `start` y `end` de cada línea, que puedes usar con `djlint.api.get_line()` para obtener números de línea a partir de una posición de carácter. Consulta el ejemplo.
- `*args, **kwargs`: puede que añadamos otros argumentos en el futuro, así que deberías incluir estos dos para reducir el riesgo de fallos al actualizar djLint.
:::

El módulo puede estar en la raíz del proyecto. Si devuelve un `line` o un `end` que no es una posición, djLint se detiene con un error que nombra la regla.

Debe devolver una lista de dicts, uno por cada error, con las siguientes claves:

::: content

- `code`: el código de la regla que informa del error (normalmente `rule['name']`)
- `line`: el número de línea y el número de carácter en esa línea, separados por ':', como cadena.
  Por ejemplo, `"2:3"` significa que el error se encontró en la línea 2, carácter 3
- `end`: opcional. Dónde termina el error, escrito igual que `line`, justo después de su último carácter. Si no se indica, el error termina donde termina `match`.
- `match`: la parte del contenido que contiene el error
- `message`: el mensaje que se imprimirá para señalar el error (normalmente `rule['message']`)
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
    """Regla que falla si el archivo html contiene 'bad'.

    Es solo un ejemplo; en realidad es mucho más sencillo hacerlo con una
    "regla de patrón".
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
