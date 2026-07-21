---
description: djLint HTML Template linter comprend plus de 30 règles ! Trouvez les définitions ici. Vous pouvez facilement l'étendre en incluant des règles personnalisées !
title: Règles du Linter
keywords: template linter, template formatter, djLint, HTML, modèles, formatter, linter, règles
---

# Utilisation de djLint

djLint inclut de nombreuses règles pour vérifier le style et la validité de vos modèles. Profitez pleinement du linter en le configurant pour utiliser un profil prédéfini pour la langue du modèle de votre choix.

```bash
djlint /path/to/templates --lint

# with custom extensions
djlint /path/to/templates -e html.dj --profile=django

# or to file
djlint /path/to/this.html.j2  --profile=jinja
```

<div class="box notification is-info is-light">
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="{{ "lang_code_url" | i18n }}/docs/configuration/">Consultez le guide de configuration pour connaître toutes les options !</a></div>
</div>

## Activation ou désactivation des règles

La plupart des règles sont activées par défaut. Les règles peuvent être désactivées en ligne de commande avec l'option `--ignore`. Les règles peuvent être activées avec l'option `--include`.

Par exemple :

```bash
djlint . --lint --include=H017,H035 --ignore=H013,H015
```

Cela peut également se faire par l'intermédiaire de l'option [{{ "configuration" | i18n }}]({{ "lang_code_url" | i18n }}/docs/configuration) fichier.

## Rules

| Code | Signification                                                                                                             | Défaut |
| ---- | ------------------------------------------------------------------------------------------------------------------------- | ------ |
| D004 | (Django) Les urls statiques doivent suivre le modèle {% raw %}`{% static path/to/file %}`{% endraw %}.                    | ✔️     |
| D018 | (Django) Les liens internes doivent utiliser le modèle {% raw %}`{% url ... %}`{% endraw %}.                              | ✔️     |
| H005 | La balise Html doit avoir l'attribut `lang`.                                                                              | ✔️     |
| H006 | La balise `img` doit avoir les attributs `height` et `width`.                                                             | -      |
| H007 | LA BALISE `<!DOCTYPE ... >` doit être présent avant la balise html.                                                       | ✔️     |
| H008 | Les attributs doivent être entre guillemets.                                                                              | ✔️     |
| H009 | Les noms de balises doivent être en minuscules.                                                                           | ✔️     |
| H010 | Les noms d'attributs doivent être en minuscules.                                                                          | ✔️     |
| H011 | Les valeurs des attributs doivent être citées.                                                                            | ✔️     |
| H012 | Il ne doit pas y avoir d'espace autour de l'attribut `=`.                                                                 | ✔️     |
| H013 | La balise `img` doit avoir des attributs alt.                                                                             | ✔️     |
| H014 | Plus de 2 lignes vides.                                                                                                   | ✔️     |
| H015 | Les balises "h" doivent être suivies d'un retour à la ligne.                                                              | ✔️     |
| H016 | Balise `title` manquante dans le html.                                                                                    | ✔️     |
| H017 | Les balises vides doivent être auto-fermantes (incompatible avec : H018).                                                 | -      |
| H018 | Les balises vides sont auto-fermantes par nature et doivent se terminer par ">", et non "/>" (incompatible avec : H017).  | -      |
| H019 | Remplacez `javascript:abc()` par l'événement `on_` et l'url réelle.                                                       | ✔️     |
| H020 | Couple de balises vide trouvé. Envisagez de le supprimer.                                                                 | ✔️     |
| H021 | Les styles en ligne doivent être évités.                                                                                  | ✔️     |
| H022 | Utilisez HTTPS pour les liens externes.                                                                                   | ✔️     |
| H023 | N'utilisez pas de références d'entités.                                                                                   | ✔️     |
| H024 | Omettre le type sur les scripts et les styles.                                                                            | ✔️     |
| H025 | La balise semble être orpheline.                                                                                          | ✔️     |
| H026 | Les balises id et class vides peuvent être supprimées.                                                                    | ✔️     |
| H029 | Pensez à utiliser des valeurs de méthode de formulaire en minuscules.                                                     | ✔️     |
| H030 | Pensez à ajouter une méta-description.                                                                                    | ✔️     |
| H031 | Pensez à ajouter des méta keywords.                                                                                       | -      |
| H033 | Espace supplémentaire dans l'action du formulaire.                                                                        | ✔️     |
| J004 | (Jinja) Les urls statiques doivent suivre le modèle {% raw %}`{ url_for('static'..) }}`{% endraw %}.                      | ✔️     |
| J018 | (Jinja) Les liens internes doivent utiliser le modèle {% raw %}`{% url ... %}`{% endraw %}.                               | ✔️     |
| T001 | Les variables doivent être entourées d'un espace. Ex : {% raw %}`{{ this }}`{% endraw %}                                  | ✔️     |
| T002 | Les doubles quotes doivent être utilisées dans les balises. Ex : {% raw %}`{% extends "this.html" %}`{% endraw %}         | -      |
| T003 | Le bloc de fin doit avoir un nom. Ex : {% raw %}`{% endblock body %}`{% endraw %}.                                        | -      |
| T027 | Chaîne non fermée trouvée dans la syntaxe du modèle.                                                                      | ✔️     |
| T028 | Envisagez d'utiliser des balises sans espace à l'intérieur des valeurs d'attributs. {% raw %}`{%- if/for -%}`{% endraw %} | ✔️     |
| T032 | Espace blanc supplémentaire trouvé dans les balises du modèle.                                                            | ✔️     |
| T034 | Aviez-vous l'intention d'utiliser {% raw %}{% ... %} au lieu de {% ... }% ? {% endraw %}                                  | ✔️     |
| H035 | Meta doivent se fermer d'elles-mêmes.                                                                                     | -      |
| H036 | Évitez d'utiliser les balises `br`.                                                                                       | -      |
| H037 | Attribut en double trouvé.                                                                                                | ✔️     |
| T038 | La balise de bloc n'a pas de balise de fin correspondante.                                                                | ✔️     |
| T039 | Balise de template non fermée trouvée.                                                                                    | ✔️     |
| T040 | Nom de template manquant ou vide dans une balise extends ou include.                                                      | ✔️     |
| H041 | La balise est fermée dans un bloc de template différent de celui où elle a été ouverte.                                   | ✔️     |
| H042 | L'attribut for d'un label n'a pas d'id correspondant dans ce fichier.                                                     | ✔️     |

### Modèles de code

La première lettre d'un code suit le modèle :

::: content

- D : s'applique spécifiquement à Django
- H : s'applique au html
- J : s'applique spécifiquement à Jinja
- M : s'applique spécifiquement à Handlebars
- N : s'applique spécifiquement à Nunjucks
- T : s'applique généralement aux modèles
  :::

### Détails des règles

<!-- prettier-ignore-start -->
<!-- the examples below are verified against djlint itself; prettier's html style would change what they demonstrate -->

{% raw %}

#### T001

`Les variables doivent être entourées d'un espace. Ex : {{ this }}`

Une syntaxe de modèle comme `{{user.name}}` sans espaces intérieurs est plus difficile à parcourir et à comparer dans les diffs, et un espacement incohérent à travers une base de code rend les refactorisations à base de grep (recherche d'une variable ou d'une balise) peu fiables, car la même expression existe sous plusieurs orthographes. Les guides de style de Django comme de Jinja écrivent `{{ var }}` et `{% tag %}` avec des espaces simples.

Non appliquée aux profils handlebars et golang.

À éviter :

```html
{{user.name}}
```

À faire :

```html
{{ user.name }}
```

#### T002

`Les doubles quotes doivent être utilisées dans les balises. Ex : {% extends "this.html" %}`

Désactivée par défaut ; à activer avec `--include=T002`.

Mélanger guillemets simples et doubles dans les balises de modèle (`{% extends %}`, `{% include %}`, `{% with %}`, `{% trans %}`, `{% now %}`) fait apparaître le même nom de modèle sous deux orthographes : les recherches et les renommages en masse manquent alors la moitié des occurrences. Standardiser sur les guillemets doubles garde les arguments des balises cohérents avec les guillemets des attributs HTML dans le reste du fichier.

Les guillemets simples à l'intérieur des valeurs d'attributs HTML (par exemple `<span title="{% trans 'x' %}">`) ne sont pas signalés, puisque les guillemets doubles de l'attribut y imposent des guillemets simples.

À éviter :

```html
{% extends 'base.html' %}
```

À faire :

```html
{% extends "base.html" %}
```

#### T003

`Le bloc de fin doit avoir un nom. Ex : {% endblock body %}.`

Lorsqu'un `{% block %}` s'étend sur de nombreuses lignes ou que des blocs sont imbriqués, un simple `{% endblock %}` ne donne aucun indice sur le bloc qu'il ferme : il est alors facile de fermer le mauvais bloc en éditant ; les modèles enfants remplacent alors le mauvais contenu. Nommer le endblock documente l'appariement et permet à djLint comme à Django (qui lève une TemplateSyntaxError en cas de nom de endblock non concordant) de détecter un bloc fermé au mauvais endroit. Les erreurs d'appariement (blocs non fermés, endblock orphelins et noms non concordants) sont des vérifications de justesse assurées par T038.

Désactivée par défaut ; à activer avec `--include=T003`.

Un nom n'est pas requis lorsque le bloc s'ouvre et se ferme sur la même ligne, par exemple `{% block title %}``{% endblock %}`.

À éviter :

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

À faire :

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Les urls statiques doivent suivre le modèle {% static path/to/file %}.`

Coder en dur les chemins /static/ contourne la balise `{% static %}` de Django : les modèles cassent dès que STATIC_URL change (par exemple lors du déplacement des ressources vers un CDN ou d'un déploiement sous un sous-chemin) et ne récupèrent jamais les noms de fichiers hachés de ManifestStaticFilesStorage, ce qui provoque des erreurs 404 ou des ressources obsolètes en cache en production.

À éviter :

```html
<link rel="stylesheet" href="/static/css/style.css">
```

À faire :

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Les urls statiques doivent suivre le modèle { url_for('static'..) }}.`

Coder en dur les chemins /static/ contourne url_for('static', ...) de Flask/Jinja : les ressources renvoient des 404 lorsque l'application est montée sous un préfixe d'URL ou que le dossier ou l'hôte statique change, et les chaînes de requête anti-cache ajoutées par le framework sont perdues.

À éviter :

```html
<link rel="stylesheet" href="/static/css/style.css">
```

À faire :

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`La balise Html doit avoir l'attribut lang.`

Sans attribut lang sur `<html>`, les lecteurs d'écran devinent les règles de prononciation et peuvent lire la page dans la mauvaise langue, et les navigateurs ne peuvent pas proposer correctement la traduction, la césure ou les guillemets adaptés à la locale. Déclarer la langue de la page correspond au critère de succès 3.1.1 de WCAG 2.1 (niveau A).

À éviter :

```html
<!DOCTYPE html>
<html>
</html>
```

À faire :

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`La balise img doit avoir les attributs height et width.`

Désactivée par défaut ; à activer avec `--include=H006`.

Lorsqu'une `<img>` n'a ni width ni height, le navigateur ne peut pas réserver l'espace avant le téléchargement de l'image, donc le contenu environnant saute pendant le chargement des images. Ce décalage de mise en page dégrade le Cumulative Layout Shift (une métrique Core Web Vitals) et peut amener les utilisateurs à cliquer au mauvais endroit pendant que la page se stabilise.

À éviter :

```html
<img src="cat.png" alt="Cat">
```

À faire :

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`LA BALISE <!DOCTYPE ... > doit être présent avant la balise html.`

Sans `<!DOCTYPE>` avant la balise `<html>`, les navigateurs rendent la page en mode quirks, en imitant le modèle de boîte et les comportements de mise en page hérités, si bien que le CSS se rend de manière incohérente d'un navigateur à l'autre. Les balises de modèle et les commentaires avant le doctype ne posent pas de problème ; seule la balise `<html>` elle-même doit en être précédée.

À éviter :

```html
<html lang="en">
</html>
```

À faire :

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Les attributs doivent être entre guillemets.`

Des styles de guillemets mélangés rendent les valeurs d'attributs plus difficiles à parcourir et à rechercher, et les valeurs entre guillemets simples cassent dès que le contenu contient une apostrophe. Les guillemets doubles sont la convention utilisée par les spécifications HTML, les formateurs et la plupart des guides de style : les adopter garde les modèles cohérents avec l'écosystème.

À éviter :

```html
<div class='content'></div>
```

À faire :

```html
<div class="content"></div>
```

#### H009

`Les noms de balises doivent être en minuscules.`

Les analyseurs HTML acceptent les noms de balises en majuscules, mais les sérialisations XHTML et XML sont sensibles à la casse et les rejettent, et une casse mélangée rend la recherche de texte et la relecture des diffs peu fiables (un grep sur `<h1>` manque `<H1>`). Des noms de balises en minuscules gardent les modèles portables et cohérents.

À éviter :

```html
<H1>Welcome</H1>
```

À faire :

```html
<h1>Welcome</h1>
```

#### H010

`Les noms d'attributs doivent être en minuscules.`

Les noms d'attributs en majuscules sont invalides dans les sérialisations XHTML/XML et mettent en échec la recherche de texte dans les modèles (un grep sur src= manque SRC=). Le DOM normalise de toute façon les noms d'attributs HTML en minuscules, donc les orthographes en majuscules ajoutent de l'incohérence sans aucun bénéfice.

À éviter :

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

À faire :

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Les valeurs des attributs doivent être citées.`

Les valeurs d'attributs sans guillemets s'arrêtent au premier espace : une valeur comme class=btn primary perd silencieusement tout ce qui suit l'espace (le navigateur traite "primary" comme un attribut booléen séparé). Les valeurs issues de variables de modèle sont particulièrement fragiles : tout espace, "=" ou ">" rendu corrompt la balise. Les guillemets rendent la limite de la valeur explicite et sûre.

À éviter :

```html
<div class=test></div>
```

À faire :

```html
<div class="test"></div>
```

#### H012

`Il ne doit pas y avoir d'espace autour de l'attribut =.`

Avec des espaces autour de "=", la balise se lit comme trois éléments séparés, et elle est à une modification près de se disloquer : un retour à la ligne ou une troncature au milieu laisse un attribut booléen nu plus du texte parasite. Garder name="value" d'un seul tenant est aussi ce que supposent les outils texte simples (grep, rechercher-remplacer) : un espacement hétérogène rend les attributs difficiles à trouver et à refactoriser de manière fiable.

À éviter :

```html
<div class = "test"></div>
```

À faire :

```html
<div class="test"></div>
```

#### H013

`La balise img doit avoir des attributs alt.`

Sans attribut alt, les lecteurs d'écran annoncent le nom de fichier de l'image, ou rien du tout, ce qui enfreint WCAG 1.1.1 (Contenu non textuel). Le texte alternatif est aussi ce que voient les utilisateurs lorsque l'image ne se charge pas. Les images décoratives doivent porter un alt="" explicitement vide pour que les technologies d'assistance sachent les ignorer ; cela satisfait également cette règle.

À éviter :

```html
<img src="cat.jpg" height="200" width="300">
```

À faire :

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Plus de 2 lignes vides.`

Les suites de lignes vides n'ont aucun effet sur la page rendue (le HTML replie les espaces) mais alourdissent les modèles et créent des diffs bruyants quand les lignes voisines changent. Le formateur de djLint les supprime entièrement par défaut (en conservant au plus `max_blank_lines` lignes vides, valeur par défaut 0), donc des suites restantes indiquent du code non formaté.

À éviter :

```html
<div>one</div>


<p>two</p>
```

À faire :

```html
<div>one</div>

<p>two</p>
```

#### H015

`Les balises "h" doivent être suivies d'un retour à la ligne.`

Les titres sont des repères de niveau bloc qui définissent le plan du document ; entasser l'élément suivant sur la même ligne que la balise h fermante masque cette structure dans le source et fait apparaître toute modification de l'un des deux éléments comme un changement des deux dans les diffs. Un saut de ligne après chaque titre garde la structure visuelle du modèle alignée sur le plan rendu.

À éviter :

```html
<h1>Heading</h1><p>Intro text.</p>
```

À faire :

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Balise title manquante dans le html.`

La spécification HTML exige un élément title dans chaque document. Sans lui, les onglets du navigateur, les favoris et l'historique affichent une URL brute au lieu d'un nom de page, les moteurs de recherche perdent l'étiquette principale de la page, et les utilisateurs de lecteurs d'écran perdent la première chose annoncée au chargement, un manquement à WCAG 2.4.2 (Titre de page, niveau A).

Ne se déclenche que sur les fichiers contenant un document `<html>`...`</html>` complet, donc les partiels et les modèles enfants qui étendent une base ne sont jamais signalés. Les coquilles de SPA qui définissent le titre côté client ont quand même besoin d'un `<title>` statique : c'est ce qui apparaît au premier rendu, pour les robots d'indexation et lorsque JavaScript échoue.

À éviter :

```html
<html lang="en">
<body>Content</body>
</html>
```

À faire :

```html
<html lang="en">
<head>
<title>My page</title>
</head>
<body>Content</body>
</html>
```

#### H017

`Les balises vides doivent être auto-fermantes (incompatible avec : H018).`

Les modèles qui doivent aussi être analysés comme du XML/XHTML (ou alimenter des outils basés sur XML) rejettent les éléments vides écrits sans barre oblique de fermeture, et mélanger `<br>` et `<br />` à travers une base de code produit des diffs incohérents. Cette règle impose la convention de style XHTML afin que chaque élément vide soit fermé de la même manière.

Désactivée par défaut ; à activer avec `--include=H017`. Mutuellement exclusive avec H018 : n'activez qu'une seule des deux conventions.

À éviter :

```html
<br>
<meta charset="utf-8">
```

À faire :

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Les liens internes doivent utiliser le modèle {% url ... %}.`

Les URLs internes codées en dur deviennent silencieusement obsolètes lorsque le chemin d'une route change dans urls.py, produisant des liens cassés et des actions de formulaire mortes qu'aucun test sur l'URLconf ne détectera. `{% url %}` résout le chemin à partir du nom de la route, donc renommer un chemin met à jour tous les liens d'un coup.

À éviter :

```html
<a href="/accounts/login">Login</a>
```

À faire :

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Les balises vides sont auto-fermantes par nature et doivent se terminer par ">", et non "/>" (incompatible avec : H017).`

Dans le standard vivant HTML, la barre oblique finale d'un élément vide n'a aucune signification (l'analyseur l'ignore), donc écrire `<br />` suggère un comportement d'auto-fermeture à la XML que le HTML n'a pas, et peut inciter les lecteurs à ajouter des barres obliques à des balises non vides, où un / parasite est silencieusement ignoré et masque des bugs de balises non fermées. Cette règle impose des fins simples en > sur les éléments vides.

Désactivée par défaut ; à activer avec `--include=H018`. Mutuellement exclusive avec H017 : n'activez qu'une seule des deux conventions. Le `<path />` SVG est exempté, car SVG est du XML et exige la barre oblique.

À éviter :

```html
<br />
<meta charset="utf-8" />
```

À faire :

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Les liens internes doivent utiliser le modèle {% url ... %}.`

Les URLs internes codées en dur cassent silencieusement lorsque le chemin d'une route change ou que l'application est montée sous un préfixe, laissant des liens morts et des actions de formulaire qui envoient vers des 404. url_for() construit l'URL à partir du nom de l'endpoint, donc les changements de routes se propagent automatiquement à tous les modèles.

À éviter :

```html
<a href="/accounts/login">Login</a>
```

À faire :

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Remplacez javascript:abc() par l'événement on_ et l'url réelle.`

Les URLs javascript: cassent le clic du milieu et l'ouverture dans un nouvel onglet, ne font rien quand JavaScript est désactivé ou ne se charge pas, sont bloquées par les Content Security Policies strictes, et constituent un point d'injection XSS classique. Utilisez plutôt une véritable URL pour le href et attachez le comportement avec un gestionnaire d'événement. Sous une CSP stricte, les gestionnaires on* en ligne sont eux aussi bloqués : le onclick montré est le correctif minimal dans le modèle ; préférez attacher l'écouteur avec addEventListener depuis un fichier de script.

À éviter :

```html
<a href="javascript:openPopup()">Open popup</a>
```

À faire :

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Couple de balises vide trouvé. Envisagez de le supprimer.`

Une paire de balises vide ne rend aucun contenu mais crée quand même un nœud DOM qui peut récupérer des marges, des bordures ou des espacements flex/grid depuis les feuilles de style, produisant un espacement fantôme difficile à tracer ; c'est généralement un reste de balisage d'une modification antérieure. Les balises légitimement vides dans un balisage normal (td, th, li, dt, dd, slot) sont exemptées. Les balises portant un attribut quelconque (points de montage JS comme `<div id="app">``</div>`, éléments de police d'icônes comme `<i class="fa fa-user">``</i>`) ne sont pas signalées non plus ; seules les paires vides totalement dépourvues d'attributs sont concernées.

À éviter :

```html
<p>Saved.</p>
<span> </span>
```

À faire :

```html
<p>Saved.</p>
```

#### H021

`Les styles en ligne doivent être évités.`

Les styles en ligne ont une spécificité supérieure à n'importe quel sélecteur de feuille de style, donc les surcharger ensuite exige !important ; ils sont bloqués par les Content Security Policies sans 'unsafe-inline' dans style-src ; et ils éparpillent la présentation dans les modèles, si bien qu'un changement de thème ou de design signifie éditer le balisage plutôt qu'une seule feuille de style. Déplacez la déclaration vers une classe CSS. Une exception légitime : les modèles d'e-mails HTML, où de nombreux clients de messagerie suppriment les blocs `<style>` et où les styles en ligne sont la technique standard ; excluez vos répertoires de modèles d'e-mails ou désactivez cette règle pour eux.

À éviter :

```html
<div style="color: red;">Wrong username or password.</div>
```

À faire :

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Utilisez HTTPS pour les liens externes.`

Les sous-ressources en simple http:// sur une page servie en HTTPS constituent du contenu mixte : les navigateurs bloquent purement et simplement les scripts, feuilles de style et iframes, et mettent automatiquement à niveau les images ou affichent un avertissement. Un lien `<a>` vers une page http:// n'est pas du contenu mixte, mais il envoie tout de même les visiteurs sur une connexion non chiffrée, exposée à l'interception et à la falsification. Les références à des hôtes internes qui n'ont réellement pas de TLS seront signalées aussi ; faites taire ces endroits avec un bloc `{# djlint:off H022 #}` plutôt qu'en désactivant la règle.

À éviter :

```html
<a href="http://example.com">Example</a>
```

À faire :

```html
<a href="https://example.com">Example</a>
```

#### H023

`N'utilisez pas de références d'entités.`

Les documents HTML5 sont en UTF-8, donc le caractère littéral fonctionne partout et c'est ce que les relecteurs lisent réellement ; une faute de frappe dans une référence d'entité (par exemple `&mdsah;`) n'est pas détectée par le navigateur et s'affiche telle quelle comme du texte cassé. djLint n'autorise que les entités qui portent une signification syntaxique ou sont invisibles à l'écran, comme `&lt;`, `&gt;`, `&amp;`, `&quot;`, `&nbsp;` et `&shy;`.

À éviter :

```html
<p>Dates 1900 &mdash; 2000</p>
```

À faire :

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omettre le type sur les scripts et les styles.`

text/javascript et text/css sont les valeurs par défaut de HTML5 pour `<script>` et `<style>`, donc l'attribut est un poids mort que le navigateur ignore ; la spécification WHATWG dit explicitement de l'omettre. Le supprimer évite aussi les chaînes MIME périmées qui cassent l'élément une fois copié sur des scripts de module (où type="module" compte réellement).

À éviter :

```html
<script type="text/javascript" src="app.js">
```

À faire :

```html
<script src="app.js"></script>
```

#### H025

`La balise semble être orpheline.`

Une balise sans sa balise d'ouverture ou de fermeture correspondante force la récupération d'erreur du navigateur à deviner où l'élément se termine : le balisage qui suit se fait avaler par le mauvais élément ; la mise en page, les sélecteurs CSS et les requêtes DOM de JavaScript cassent alors silencieusement, et différemment selon les navigateurs. H025 signale aussi un `<ol>` ou `<ul>` ouvert à l'intérieur d'un `<p>` : l'analyseur HTML ferme le paragraphe avant la liste, donc le balisage ne s'imbrique jamais comme il est écrit.

À éviter :

```html
<div>
  <p>Hello</p>
```

À faire :

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Les balises id et class vides peuvent être supprimées.`

Un attribut id ou class vide ne fait rien (aucun style ni script ne peut le cibler) et un id vide est du HTML invalide (la valeur de l'id ne doit pas être la chaîne vide). Cela signale généralement un bug de modèle où une variable devait être interpolée : le supprimer ou le remplir empêche ce bug de se cacher au grand jour.

À éviter :

```html
<div id="" class="">content</div>
```

À faire :

```html
<div>content</div>
```

#### T027

`Chaîne non fermée trouvée dans la syntaxe du modèle.`

Un guillemet ouvert mais jamais fermé à l'intérieur de `{% ... %}` ou `{{ ... }}` fait mal analyser la balise par le moteur de modèles : Django et Jinja lèvent une TemplateSyntaxError au rendu ou avalent silencieusement le reste des arguments de la balise comme contenu de chaîne, si bien que la page renvoie une erreur 500 ou s'affiche avec des arguments manquants.

À éviter :

```html
{% trans "Welcome %}
```

À faire :

```html
{% trans "Welcome" %}
```

#### T028

`Envisagez d'utiliser des balises sans espace à l'intérieur des valeurs d'attributs. {%- if/for -%}`

Les balises de modèle à l'intérieur d'une valeur d'attribut émettent dans l'attribut rendu les espaces et sauts de ligne qui les entourent : un href ou un src construit avec de simples balises `{% if %}`/`{% for %}` peut donc contenir des espaces parasites et produire des URLs cassées. Les balises de contrôle des espaces de Jinja/Nunjucks (`{%- ... -%}`) suppriment ces espaces environnants, si bien que l'attribut se rend comme une seule valeur propre. L'attribut class est exempté, car des espaces supplémentaires entre noms de classes sont sans conséquence.

Non appliquée au profil django : les balises de modèle Django ne prennent pas en charge le contrôle des espaces `{%- -%}`.

À éviter :

```html
<a href="{% if x %}/home{% endif %}"></a>
```

À faire :

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Pensez à utiliser des valeurs de méthode de formulaire en minuscules.`

La spécification HTML définit les mots-clés de méthode de formulaire en minuscules (get, post) ; les navigateurs n'acceptent les variantes en majuscules que par une correspondance de repli insensible à la casse. Conserver la forme canonique en minuscules garde les modèles cohérents et faciles à rechercher, et évite les plaintes des validateurs stricts et des chaînes d'outils basées sur XHTML.

À éviter :

```html
<form method="POST"></form>
```

À faire :

```html
<form method="post"></form>
```

#### H030

`Pensez à ajouter une méta-description.`

Les moteurs de recherche utilisent la meta description comme extrait affiché sous le titre de votre page dans les résultats ; sans elle, ils synthétisent un extrait à partir d'un texte arbitraire de la page, ce qui nuit au taux de clic et produit de mauvais aperçus de lien lorsque la page est partagée.

Ne se déclenche que sur les fichiers contenant un document `<html>`...`</html>` complet. L'argument de l'extrait s'applique aux pages indexées publiquement ; pour les applications derrière authentification ou en intranet, cette règle est couramment désactivée.

À éviter :

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

À faire :

```html
<html lang="en">
  <head>
    <title>Home</title>
    <meta name="description" content="A short summary of this page.">
  </head>
  <body>Welcome</body>
</html>
```

#### H031

`Pensez à ajouter des méta keywords.`

Désactivée par défaut ; à activer avec `--include=H031`.

Les métadonnées de mots-clés sont encore consommées par certains outils de recherche de site, indexeurs d'intranet et robots plus anciens : une page qui ne déclare jamais `<meta name="keywords">` peut être invisible pour ces systèmes. Les grands moteurs de recherche publics l'ignorent toutefois, si bien que les équipes qui ne dépendent pas de tels outils désactivent couramment cette règle.

Ne se déclenche que sur les fichiers contenant un document `<html>...</html>` complet.

À éviter :

```html
<!DOCTYPE html>
<html lang="en">
<head>
<title>Home</title>
<meta name="description" content="A short summary.">
</head>
</html>
```

À faire :

```html
<!DOCTYPE html>
<html lang="en">
<head>
<title>Home</title>
<meta name="description" content="A short summary.">
<meta name="keywords" content="django, templates">
</head>
</html>
```

#### T032

`Espace blanc supplémentaire trouvé dans les balises du modèle.`

Les suites d'espaces ou de tabulations entre les arguments d'une balise de modèle sont du bruit invisible : elles masquent les vraies différences dans les diffs, peuvent rendre difficile de repérer un argument manquant, et s'écartent du style à espace unique produit par le formateur de djLint, provoquant des reformatages inutiles. Les espaces à l'intérieur des chaînes entre guillemets sont préservés et ne sont pas signalés.

À éviter :

```html
{% static  'css/style.css' %}
```

À faire :

```html
{% static 'css/style.css' %}
```

#### H033

`Espace supplémentaire dans l'action du formulaire.`

Les espaces en début ou en fin de la valeur action d'un formulaire deviennent partie intégrante de l'URL rendue. Les navigateurs les suppriment à l'analyse, mais les clients hors navigateur et les tests qui utilisent la valeur littérale peuvent ne pas le faire, et autour d'une balise `{% url %}` l'espace parasite signale presque toujours une faute de frappe produisant une URL de soumission que le routage côté serveur ne reconnaît pas.

À éviter :

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

À faire :

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Aviez-vous l'intention d'utiliser {% ... %} au lieu de {% ... }% ?`

}% est presque toujours une faute de frappe pour %}. Le moteur de modèles ne reconnaît pas }% comme délimiteur de balise, donc la balise n'est jamais analysée : le texte brut {% ... }% fuit dans le HTML rendu, ou le moteur lève une erreur de syntaxe en rencontrant la balise non fermée.

À éviter :

```html
{% include "footer.html" }%
```

À faire :

```html
{% include "footer.html" %}
```

#### H035

`Meta doivent se fermer d'elles-mêmes.`

En HTML5 pur, la barre oblique finale sur `<meta>` est facultative, mais les modèles qui passent aussi par des outils XML/XHTML (validateurs XML, pipelines d'e-mails, XSLT) échouent à l'analyse quand les éléments vides ne sont pas auto-fermés. Activer cette règle maintient les balises `<meta>` sous la forme compatible XHTML `<meta ... />` afin que le même balisage survive aux deux analyseurs.

Désactivée par défaut ; à activer avec `--include=H035`. Sous-ensemble de H017 (qui impose la barre oblique finale sur toutes les balises vides, meta comprise) ; n'activez H035 seule que si vous voulez la forme XHTML uniquement pour meta. Mutuellement exclusive avec H018 ; n'activez pas les deux.

À éviter :

```html
<meta name="viewport" content="width=device-width">
```

À faire :

```html
<meta name="viewport" content="width=device-width" />
```

#### H036

`Évitez d'utiliser les balises br.`

`<br>` encode de la présentation dans le balisage : l'utiliser pour l'espacement ou pour simuler des paragraphes casse le renvoi à la ligne du texte aux largeurs étroites et dégrade l'accessibilité, puisque les lecteurs d'écran annoncent des sauts forcés au lieu d'une pause naturelle entre les blocs. Les idées distinctes relèvent d'éléments de bloc distincts, et l'espacement vertical relève des marges CSS. Notez que `<br>` est légitime lorsque le saut de ligne fait partie du contenu lui-même (adresses postales, poèmes, paroles de chansons) et cette règle ne peut pas distinguer ces cas de l'usage purement présentationnel : elle signale chaque `<br>`. Laissez-la désactivée si vos modèles rendent ce type de contenu.

Désactivée par défaut ; à activer avec `--include=H036`.

À éviter :

```html
<p>Shipping is free.<br>Delivery takes 3 days.</p>
```

À faire :

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Attribut en double trouvé.`

Les attributs en double sont du HTML invalide, et les navigateurs ne conservent que la première occurrence et abandonnent silencieusement les suivantes : la deuxième valeur de class ou de style ne prend donc jamais effet, ce qui cache de vrais bugs. La vérification tient compte des modèles : un attribut répété dans des branches mutuellement exclusives (`{% if %}`/`{% else %}`) n'est pas signalé, puisqu'une seule copie peut être rendue.

À éviter :

```html
<div class="card" id="profile" class="active">...</div>
```

À faire :

```html
<div class="card active" id="profile">...</div>
```

#### T038

`La balise de bloc n'a pas de balise de fin correspondante.`

Une balise de bloc telle que `{% if %}`, `{% for %}` ou `{% macro %}` sans sa balise de fin correspondante est une TemplateSyntaxError pure et simple dans Django et Jinja : la page échoue au rendu au moment de la requête, ce que cette règle détecte avant le déploiement. Elle signale aussi les balises de fin orphelines sans balise d'ouverture et les blocs incorrectement entrelacés (par exemple `{% if %}``{% for %}``{% endif %}`).

L'appariement `{% block %}`/`{% endblock %}` et les noms de endblock non concordants sont vérifiés par cette règle ; T003 (désactivée par défaut) exige en plus un nom sur chaque `{% endblock %}` multiligne. Les balises de bloc personnalisées enregistrées via custom_blocks sont également vérifiées, y compris leur forme auto-fermante / %}.

À éviter :

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

À faire :

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Balise de template non fermée trouvée.`

Une balise de modèle ouverte avec `{{` ou `{%` mais jamais fermée par le `}}` ou `%}` correspondant n'est pas analysée comme une balise : Django/Jinja lèvent une TemplateSyntaxError ou rendent les accolades brutes dans la page, et tout ce qui suit jusqu'au prochain délimiteur peut être silencieusement avalé. Ces fautes de frappe (une seule accolade manquante, un délimiteur non concordant) sont faciles à manquer en relecture, car le modèle peut encore se rendre partiellement.

À éviter :

```html
<p>{{ user.name }</p>
```

À faire :

```html
<p>{{ user.name }}</p>
```

#### T040

`Nom de template manquant ou vide dans une balise extends ou include.`

Une balise `{% extends %}` ou `{% include %}` dont le nom de modèle est manquant, vide ou composé uniquement d'espaces n'a rien à charger : Django lève une TemplateSyntaxError lorsque le nom est totalement absent, et TemplateDoesNotExist au rendu lorsqu'il est vide, si bien que la page renvoie une erreur 500 en production alors même que le fichier de modèle semble syntaxiquement plausible.

À éviter :

```html
{% extends "" %}
```

À faire :

```html
{% extends "base.html" %}
```

#### H041

`La balise est fermée dans un bloc de template différent de celui où elle a été ouverte.`

Lorsqu'une balise HTML est ouverte dans un `{% block %}` mais fermée dans un autre, un modèle enfant qui ne remplace qu'un seul de ces blocs hérite de la moitié de l'élément, produisant un balisage déséquilibré dans la page rendue : les navigateurs ferment ou réimbriquent alors les éléments de façon imprévisible, cassant la mise en page et les sélecteurs CSS loin du modèle réellement modifié. Garder chaque élément ouvert et fermé dans le même bloc rend chaque bloc sûr à remplacer indépendamment.

À éviter :

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

À faire :

```html
{% block content %}
<div class="wrapper">
</div>
{% endblock content %}
{% block footer %}
{% endblock footer %}
```

#### H042

`L'attribut for d'un label n'a pas d'id correspondant dans ce fichier.`

La vérification ne s'exécute que sur les fichiers analysables de façon fiable : si le fichier contient quoi que ce soit pouvant rendre un id invisible ici (une sortie `{{ ... }}` telle qu'un widget de formulaire, un `{% include %}` ou `{% extends %}`, ou une balise de modèle inconnue), la règle reste silencieuse pour ce fichier. Là où elle s'exécute, un signalement est une association réellement cassée.

À éviter :

```html
<label for="email">Email</label>
<input id="username">
```

À faire :

```html
<label for="email">Email</label>
<input id="email">
```

{% endraw %}

<!-- prettier-ignore-end -->

### Ajout de règles

Nous accueillons volontiers les pull requests contenant de nouvelles règles !

Une bonne règle consiste en

::: content

- Name
- Code
- Message - Message à afficher lorsqu'une erreur est trouvée.
- Flags - Drapeaux de regex. La valeur par défaut est re.DOTALL. ex : re.I|re.M
- Patterns - Expressions regex qui trouveront l'erreur.
- Exclude - Liste facultative de profils dont la règle doit être exclue.
  :::

Veuillez inclure un test pour valider la règle.

## Règles personnalisées

Il est possible d'ajouter des règles personnalisées directement au sein de votre projet.
Pour cela, créez un fichier `.djlint_rules.yaml` à côté de votre `pyproject.toml`.
Un fichier de règles situé ailleurs peut être indiqué avec l'option CLI `--rules`.
Des règles peuvent être ajoutées à ce fichier et djLint les reprendra.

### Règle basé sur la recherche d'un regex

Vous pouvez ajouter une règle qui échouera si l'un des regex listés dans `patterns`
est trouvé dans le code html.

```yaml
- rule:
    name: T001
    message: Trouver la Trichotillomanie
    flags: re.DOTALL|re.I
    pattern:
      - Trichotillomanie
```

### Règle utilisant un module python externe

Vous pouvez ajouter une règle qui va importer et executer une fonction python
personalisée.

```yaml
- rule:
    name: T001
    message: Le mot 'bad' a été trouvé
    python_module: votre_package.votre_module
```

Le module indiqué dans `python_module` doit contenir une fonction `run()` qui sera
executé sur chacun des fichiers testés. La fonction doit accepter les arguments suivants :

::: content

- `rule`: Le dictionnaire python qui représente votre règle dans `.djlint_rules.yaml`.
  Utilisez cette variable pour accéder aux `name` et `message` que vous avez défini dans
  le `yaml`.
- `config`: L'objet de configuration global de DJLint.
- `html`: Le contenu html complet du fichier testé.
- `filepath`: Chemin du fichier testé.
- `line_ends`: Liste qui, pour chacune des lignes du fichier html testé, contient un
  dictionnaire avec `start` et `end` qui donnent les indexes globaux dans le fichier du
  début et fin de la ligne. Cette variable peut être utilisée avec `djlint.lint.get_line()`
  pour récupérer le numéro de ligne à partir de l'indexe du caractère dans le fichier html.
- `*args, **kwargs`: Il est possible que nous ajoutions d'autres arguments à l'avenir,
  il est donc fortement conseillé d'ajouter ces deux arguments pour diminuer les risques
  de bugs en cas de mise à jour de djLint.
  :::

La fonction doit retourner une liste de dictionnaire, un pour chacune des erreurs
trouvées. Le dictionnaire doit contenir les clées suivantes :

::: content

- `code`: Code de la règle qui rapporte l'erreur (généralement `rule['name']`)
- `line`: Numéro de ligne et numéro de caractère dans cette ligne, séparées par un `:`.
  Par exemple, `"2:3"` veut dire que l'erreur a été trouvée sur la ligne 2, au caractère 3.
- `match`: La partie du contenu qui contient l'erreur
- `message`: Le message qui serra affiché pour signaler l'erreur (généralement `rule['message']`)
  :::

```python
from typing import Any, Dict, List
from djlint.settings import Config
from djlint.lint import get_line
import re


def run(
    rule: Dict[str, Any],
    config: Config,
    html: str,
    filepath: str,
    line_ends: List[Dict[str, int]],
    *args: Any,
    **kwargs: Any,
) -> List[Dict[str, str]]:
    """
    Rule that fails if if the html file contains 'bad'. This is just an exemple, in
    reality it's much simpler to do that with "pattern rule".
    """
    errors: List[Dict[str, str]] = []
    for match in re.finditer(r"bad", html):
        errors.append({
            "code": rule["name"],
            "line": get_line(match.start(), line_ends),
            "match": match.group().strip()[:20],
            "message": rule["message"],
        })
    return errors
```
