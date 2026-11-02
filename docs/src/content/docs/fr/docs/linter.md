---
title: "Règles du linter"
description: "Les règles du linter de templates HTML de djLint, et comment ajouter les vôtres."
sidebar:
  label: "Linter"
---

djLint comprend de nombreuses règles pour vérifier le style et la validité de vos templates. Tirez pleinement parti du linter en le configurant avec un profil prédéfini pour le langage de templates de votre choix.

```bash
djlint /path/to/templates --lint

# avec des extensions personnalisées
djlint /path/to/templates -e html.dj --profile=django

# ou sur un fichier
djlint /path/to/this.html.j2  --profile=jinja
```

:::tip
[Consultez le guide de configuration pour découvrir toutes les options !](/fr/docs/configuration/)
:::

## Activer ou désactiver des règles

La plupart des règles sont activées par défaut. En ligne de commande, vous pouvez désactiver des règles avec l'option `--ignore` et en activer avec l'option `--include`.

Par exemple :

```bash
djlint . --lint --include=H006,H017 --ignore=H013,H015
```

Vous pouvez aussi le faire dans le fichier de [configuration](/fr/docs/configuration).

## Règles

| Code | Signification                                                                                                                  | Par défaut |
| ---- | ------------------------------------------------------------------------------------------------------------------------------ | ---------- |
| T001 | Les variables doivent être entourées d'espaces. Ex. : `{{ this }}`                                                             | ✔️         |
| T002 | Les balises doivent utiliser des guillemets doubles. Ex. : `{% extends "this.html" %}`                                         | ✔️         |
| T003 | Un endblock doit porter un nom. Ex. : `{% endblock body %}`.                                                                   | -          |
| D004 | (Django) Les URL statiques doivent suivre la forme `{% static path/to/file %}`.                                                | ✔️         |
| J004 | (Jinja) Les URL statiques doivent suivre la forme `{{ url_for('static'..) }}`.                                                 | ✔️         |
| H005 | La balise html doit avoir un attribut `lang` non vide.                                                                         | ✔️         |
| H006 | La balise `img` doit avoir des attributs `height` et `width`.                                                                  | -          |
| H007 | `<!DOCTYPE ... >` doit figurer avant la balise html.                                                                           | ✔️         |
| H008 | Les attributs doivent être entre guillemets doubles.                                                                           | ✔️         |
| H009 | Les noms de balises doivent être en minuscules.                                                                                | ✔️         |
| H010 | Les noms d'attributs doivent être en minuscules.                                                                               | ✔️         |
| H011 | Les valeurs d'attributs doivent être entre guillemets.                                                                         | ✔️         |
| H012 | Pas d'espaces autour du `=` d'un attribut.                                                                                     | ✔️         |
| H013 | La balise `img` doit avoir un attribut alt.                                                                                    | ✔️         |
| H014 | Plus de lignes vides que la configuration n'en conserve.                                                                       | ✔️         |
| H015 | Les balises `h` doivent être suivies d'un saut de ligne.                                                                       | ✔️         |
| H016 | Balise `title` manquante dans le html.                                                                                         | ✔️         |
| H017 | Les balises vides doivent être auto-fermantes (en conflit avec : H018).                                                        | -          |
| D018 | (Django) Les liens internes doivent utiliser la forme `{% url ... %}`.                                                         | ✔️         |
| H018 | Les balises vides sont auto-fermantes par nature et doivent se terminer par « > », et non « /> » (en conflit avec : H017).     | -          |
| J018 | (Jinja) Les liens internes doivent utiliser la forme `{{ url_for() ... }}`.                                                    | ✔️         |
| H019 | Remplacer `javascript:abc()` par un événement `on_` et une vraie URL.                                                          | ✔️         |
| H020 | Paire de balises vide trouvée. Envisagez de la supprimer.                                                                      | ✔️         |
| H021 | Les styles en ligne sont à éviter.                                                                                             | ✔️         |
| H022 | Utiliser HTTPS pour les liens externes.                                                                                        | ✔️         |
| H023 | Ne pas utiliser de références d'entités.                                                                                       | ✔️         |
| H024 | Omettre type sur les scripts et les styles.                                                                                    | ✔️         |
| H025 | La balise semble orpheline.                                                                                                    | ✔️         |
| H026 | Les attributs id et class vides peuvent être supprimés.                                                                        | ✔️         |
| T027 | Chaîne non fermée dans la syntaxe de template.                                                                                 | ✔️         |
| T028 | Envisagez des balises sans espaces dans les valeurs d'attributs. `{%- if/for -%}`                                              | -          |
| H029 | Envisagez des valeurs en minuscules pour la méthode des formulaires.                                                           | ✔️         |
| H030 | Envisagez d'ajouter une meta description.                                                                                      | ✔️         |
| T032 | Espaces superflus dans les balises de template.                                                                                | ✔️         |
| H033 | Espaces superflus dans l'action d'un formulaire.                                                                               | ✔️         |
| T034 | Vouliez-vous écrire {% ... %} au lieu de {% ... }% ?                                                                           | ✔️         |
| H036 | Ne pas utiliser de balises `br` pour créer de l'espacement.                                                                    | ✔️         |
| H037 | Attribut en double.                                                                                                            | ✔️         |
| T038 | La balise de bloc n'a pas de balise de fin correspondante.                                                                     | ✔️         |
| T039 | Balise de template non fermée.                                                                                                 | ✔️         |
| T040 | Nom de template manquant ou vide dans une balise extends ou include.                                                           | ✔️         |
| H041 | La balise est fermée dans un autre bloc de template que celui où elle est ouverte.                                             | ✔️         |
| T041 | La balise extends doit être la première balise du template.                                                                    | ✔️         |
| H042 | L'attribut for du label ne correspond à aucun id d'élément dans ce fichier.                                                    | ✔️         |
| T042 | Le contenu hors d'un bloc n'est pas rendu dans un template qui en étend un autre.                                              | ✔️         |
| H043 | La balise button doit avoir un attribut `type`.                                                                                | ✔️         |
| T043 | Le nom de bloc est utilisé plus d'une fois dans le template.                                                                   | ✔️         |
| H044 | Un thead ne doit pas mélanger cellules `th` et `td`.                                                                           | ✔️         |
| T044 | La balise d'affichage contient un mot-clé d'instruction ; utilisez une balise de bloc.                                         | ✔️         |
| H045 | La balise iframe doit avoir un attribut `title`.                                                                               | ✔️         |
| T045 | Une balise de template dans un commentaire html s'exécute quand même ; utilisez un commentaire de template pour la désactiver. | ✔️         |
| H046 | Tabindex ne doit pas être positif.                                                                                             | ✔️         |
| H047 | Aria-hidden ne doit pas être défini sur un élément focalisable.                                                                | ✔️         |
| H048 | L'attribut aria ne fait pas partie de ceux que définit la spécification.                                                       | ✔️         |
| H049 | Le viewport ne doit pas empêcher de zoomer sur la page.                                                                        | ✔️         |
| H050 | L'élément est obsolète et doit être remplacé.                                                                                  | ✔️         |
| H051 | Le rôle ne fait pas partie de ceux que définit ARIA pour le balisage.                                                          | ✔️         |
| H052 | Meta refresh ne doit pas recharger ni rediriger la page après un délai.                                                        | ✔️         |
| H053 | L'id est utilisé plus d'une fois dans le fichier.                                                                              | ✔️         |
| H054 | Un élément interactif ne doit pas être imbriqué dans un autre.                                                                 | ✔️         |
| H055 | L'attribut lang doit être une étiquette de langue, comme en ou pt-BR.                                                          | ✔️         |
| H056 | Src ne doit pas être vide.                                                                                                     | ✔️         |
| H057 | Une vidéo doit avoir une piste de sous-titres.                                                                                 | ✔️         |

### Forme des codes

La première lettre d'un code suit ce schéma :

- D : s'applique spécifiquement à Django
- H : s'applique au html
- J : s'applique spécifiquement à Jinja
- M : s'applique spécifiquement à Handlebars
- N : s'applique spécifiquement à Nunjucks
- T : s'applique aux templates en général

### Détail des règles

<!-- oxfmt-ignore-start -->

#### T001

`Variables should be wrapped in a whitespace.`

Une syntaxe de template comme `{{user.name}}` sans espaces intérieurs est plus difficile à parcourir et à comparer, et un espacement incohérent dans une base de code rend peu fiables les refactorisations à base de grep (recherche d'une variable ou d'une balise), car la même expression existe sous plusieurs graphies. Les guides de style de Django comme de Jinja écrivent `{{ var }}` et `{% tag %}` avec des espaces simples.

Ne s'applique pas aux profils handlebars et golang.

À éviter :

```html
{{user.name}}
```

À privilégier :

```html
{{ user.name }}
```

#### T002

`Double quotes should be used in tags.`

Mélanger guillemets simples et doubles dans les balises de template (`{% extends %}`, `{% include %}`, `{% with %}`, `{% trans %}`, `{% now %}`) fait apparaître un même nom de template sous deux graphies, si bien que les recherches et les renommages en masse manquent la moitié des occurrences. S'en tenir aux guillemets doubles garde les arguments des balises cohérents avec les guillemets des attributs HTML dans le reste du fichier.

Les guillemets simples dans les valeurs d'attributs HTML (par ex. `<span title="{% trans 'x' %}">`) ne sont pas signalés, puisque les guillemets doubles de l'attribut imposent des guillemets simples à cet endroit.

Avec `quote_style = "single"`, la règle demande au contraire des guillemets simples, et le formateur les écrit.

`--reformat` réécrit ces guillemets pour vous.

À éviter :

```html
{% extends 'base.html' %}
```

À privilégier :

```html
{% extends "base.html" %}
```

#### T003

`Endblock should have name. Ex: {% endblock body %}.`

Quand un `{% block %}` s'étend sur de nombreuses lignes ou que des blocs sont imbriqués, un `{% endblock %}` nu ne dit pas quel bloc il ferme : il est alors facile de fermer le mauvais en cours d'édition, et les templates enfants remplacent le mauvais contenu. Nommer l'endblock documente l'appariement et permet à djLint comme à Django (qui lève TemplateSyntaxError sur un nom d'endblock qui ne correspond pas) de repérer un bloc fermé au mauvais endroit. Les erreurs d'appariement (blocs non fermés, endblocks orphelins et noms qui ne correspondent pas) sont des vérifications de validité prises en charge par T038.

Désactivée par défaut ; activez-la avec `--include=T003`. `--name-endblocks` écrit le nom pour vous.

Aucun nom n'est requis quand le bloc s'ouvre et se ferme sur la même ligne, par ex. `{% block title %}``{% endblock %}`. Le formateur place le contenu d'un bloc qui contient d'autres balises sur des lignes séparées : un bloc écrit sur une seule ligne peut donc avoir besoin d'un nom une fois formaté ; avec `--name-endblocks`, le formateur écrit aussi ce nom.

À éviter :

```html
{% block content %}
<p>hello</p>
{% endblock %}
```

À privilégier :

```html
{% block content %}
<p>hello</p>
{% endblock content %}
```

#### D004

`(Django) Static urls should follow {% static path/to/file %} pattern.`

Coder en dur des chemins /static/ contourne la balise `{% static %}` de Django : les templates cassent quand STATIC_URL change (par ex. en déplaçant les ressources vers un CDN ou en déployant sous un sous-chemin) et ne récupèrent jamais les noms de fichiers hachés de ManifestStaticFilesStorage, ce qui provoque des 404 ou des ressources périmées en cache en production. La règle recherche le préfixe littéral `/static/` : un projet qui sert ses fichiers statiques depuis un autre chemin n'est donc pas couvert.

À éviter :

```html
<link rel="stylesheet" href="/static/css/style.css">
```

À privilégier :

```html
<link rel="stylesheet" href="{% static 'css/style.css' %}">
```

#### J004

`(Jinja) Static urls should follow {{ url_for('static'..) }} pattern.`

Coder en dur des chemins /static/ contourne le url_for('static', ...) de Flask/Jinja : les ressources renvoient des 404 quand l'application est montée sous un préfixe d'URL ou que le dossier ou l'hôte statique change, et les paramètres de requête anti-cache ajoutés par le framework sont perdus. La règle recherche le préfixe littéral `/static/` : un projet qui sert ses fichiers statiques depuis un autre chemin n'est donc pas couvert.

À éviter :

```html
<link rel="stylesheet" href="/static/css/style.css">
```

À privilégier :

```html
<link rel="stylesheet" href="{{ url_for('static', filename='css/style.css') }}">
```

#### H005

`Html tag should have a non-empty lang attribute.`

Sans attribut lang sur `<html>`, les lecteurs d'écran devinent les règles de prononciation et peuvent lire la page dans la mauvaise langue, et les navigateurs ne peuvent pas proposer correctement la traduction, la césure ou des guillemets adaptés à la langue. Déclarer la langue de la page correspond au critère de succès 3.1.1 des WCAG 2.1 (niveau A).

`lang=""` et un `lang` sans valeur indiquent tous deux que la langue est inconnue : ils sont donc signalés comme un attribut manquant.

À éviter :

```html
<!DOCTYPE html>
<html>
</html>
```

À privilégier :

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H006

`Img tag should have height and width attributes.`

Désactivée par défaut ; activez-la avec `--include=H006`.

Quand une `<img>` n'a ni largeur ni hauteur, le navigateur ne peut pas réserver d'espace avant le téléchargement de l'image : le contenu environnant saute à mesure que les images se chargent. Ce décalage de mise en page dégrade le Cumulative Layout Shift (une métrique des Core Web Vitals) et peut faire cliquer l'utilisateur au mauvais endroit pendant que la page se stabilise.

À éviter :

```html
<img src="cat.png" alt="Cat">
```

À privilégier :

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H007

`<!DOCTYPE ... > should be present before the html tag.`

Sans `<!DOCTYPE>` avant la balise `<html>`, les navigateurs affichent la page en mode quirks, en émulant l'ancien modèle de boîte et l'ancien comportement de mise en page : le CSS s'affiche alors différemment d'un navigateur à l'autre. Les balises de template et les commentaires avant le doctype ne posent pas de problème ; seule la balise `<html>` elle-même doit en être précédée.

À éviter :

```html
<html lang="en">
</html>
```

À privilégier :

```html
<!DOCTYPE html>
<html lang="en">
</html>
```

#### H008

`Attributes should be double quoted.`

Mélanger les styles de guillemets rend les valeurs d'attributs plus difficiles à parcourir et à rechercher avec grep, et les valeurs entre guillemets simples cassent dès que le contenu contient une apostrophe. Les guillemets doubles sont la convention des spécifications HTML, des formateurs et de la plupart des guides de style : s'y tenir garde les templates cohérents avec le reste de l'écosystème.

À éviter :

```html
<div class='content'></div>
```

À privilégier :

```html
<div class="content"></div>
```

#### H009

`Tag names should be lowercase.`

Les parseurs HTML acceptent les noms de balises en majuscules, mais les sérialisations XHTML et XML sont sensibles à la casse et les rejettent, et une casse mélangée rend peu fiables la recherche textuelle et la relecture des diffs (chercher `<h1>` avec grep manque `<H1>`). Des noms de balises en minuscules gardent les templates portables et cohérents.

Non signalée avec `--ignore-case`, qui demande au formateur de ne pas toucher à la casse.

À éviter :

```html
<H1>Welcome</H1>
```

À privilégier :

```html
<h1>Welcome</h1>
```

#### H010

`Attribute names should be lowercase.`

Les noms d'attributs en majuscules sont invalides dans les sérialisations XHTML/XML et faussent la recherche textuelle dans les templates (chercher src= avec grep manque SRC=). Le DOM normalise de toute façon les noms d'attributs HTML en minuscules : les graphies en majuscules ajoutent donc de l'incohérence sans aucun avantage. Seuls les noms que le formateur met en minuscules sont signalés : `class`, `id`, `src`, `width`, `height`, `alt`, `style`, `lang`, `title`, `media` et `srcset`. `--reformat` les corrige pour vous, et une liaison de framework comme `:itemID` ou un nom plus long comme `data-ID` garde sa casse.

Non signalée avec `--ignore-case`, qui demande au formateur de ne pas toucher à la casse.

À éviter :

```html
<img SRC="cat.png" alt="Cat" width="120" height="80">
```

À privilégier :

```html
<img src="cat.png" alt="Cat" width="120" height="80">
```

#### H011

`Attribute values should be quoted.`

Une valeur d'attribut sans guillemets s'arrête au premier espace : une valeur comme class=btn primary perd silencieusement tout ce qui suit l'espace (le navigateur traite « primary » comme un attribut booléen distinct). Les valeurs issues de variables de template sont particulièrement fragiles : tout espace, « = » ou « > » rendu corrompt la balise. Les guillemets rendent la limite de la valeur explicite et sûre.

À éviter :

```html
<div class=test></div>
```

À privilégier :

```html
<div class="test"></div>
```

#### H012

`There should be no spaces around attribute =.`

Avec des espaces autour de « = », la balise se lit comme trois éléments distincts, et il suffit d'une modification pour qu'elle se disloque : un retour à la ligne ou une troncature au milieu laisse un attribut booléen isolé suivi de texte parasite. Garder nom="valeur" d'un seul tenant est aussi ce que supposent les outils textuels simples (grep, rechercher-remplacer) : un espacement mélangé rend les attributs difficiles à trouver et à refactoriser de manière fiable. `--reformat` supprime les espaces pour vous.

À éviter :

```html
<div class = "test"></div>
```

À privilégier :

```html
<div class="test"></div>
```

#### H013

`Img tag should have an alt attribute.`

Sans attribut alt, les lecteurs d'écran annoncent le nom de fichier de l'image, ou rien du tout, ce qui enfreint le critère 1.1.1 des WCAG (Contenu non textuel). Le texte alternatif est aussi ce que voient les utilisateurs quand l'image ne se charge pas. Les images décoratives doivent porter un alt="" explicitement vide pour que les technologies d'assistance sachent les ignorer ; cela satisfait aussi cette règle.

Un `alt` sans valeur équivaut à `alt=""`, le cas de l'image décorative : il est donc accepté.

À éviter :

```html
<img src="cat.jpg" height="200" width="300">
```

À privilégier :

```html
<img src="cat.jpg" height="200" width="300" alt="A sleeping cat">
```

#### H014

`Found extra blank lines.`

Les suites de lignes vides n'ont aucun effet sur la page rendue (HTML fusionne les espaces), mais elles alourdissent les templates et créent des diffs bruyants quand les lignes voisines changent. Par défaut, le formateur de djLint les supprime entièrement (il conserve au plus `max_blank_lines` lignes vides, valeur qui vaut 0 par défaut) : des suites restantes signalent donc du code non formaté.

À éviter :

```html
<div>one</div>


<p>two</p>
```

À privilégier :

```html
<div>one</div>

<p>two</p>
```

#### H015

`Follow h tags with a line break.`

Les titres sont des repères de niveau bloc qui définissent le plan du document ; tasser l'élément suivant sur la même ligne que la balise h fermante masque cette structure dans le source, et une modification de l'un ou l'autre élément apparaît dans les diffs comme une modification des deux. Un saut de ligne après chaque titre garde la structure visuelle du template alignée sur le plan rendu.

À éviter :

```html
<h1>Heading</h1><p>Intro text.</p>
```

À privilégier :

```html
<h1>Heading</h1>
<p>Intro text.</p>
```

#### H016

`Missing title tag in html.`

La spécification HTML exige un élément title dans chaque document. Sans lui, les onglets du navigateur, les favoris et l'historique affichent une URL brute au lieu d'un nom de page, les moteurs de recherche perdent l'intitulé principal de la page, et les utilisateurs de lecteurs d'écran perdent la première chose annoncée au chargement, ce qui enfreint le critère 2.4.2 des WCAG (Titre de page, niveau A).

Ne se déclenche que sur les fichiers contenant un document `<html>`...`</html>` complet : les partiels et les templates enfants qui étendent une base ne sont donc jamais signalés. Les coquilles de SPA qui définissent le titre côté client ont tout de même besoin d'un `<title>` statique : c'est lui qui apparaît au premier affichage, pour les robots d'indexation et quand JavaScript échoue.

À éviter :

```html
<html lang="en">
<body>Content</body>
</html>
```

À privilégier :

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

Les templates qui doivent aussi être analysables en XML/XHTML (ou alimenter des outils basés sur XML) rejettent les éléments vides écrits sans barre oblique fermante, et mélanger `<br>` et `<br />` dans une base de code produit des diffs incohérents. Cette règle impose la convention de style XHTML pour que chaque élément vide soit fermé de la même façon.

Désactivée par défaut ; activez-la avec `--include=H017`. Incompatible avec H018 ; n'activez qu'une des deux conventions. `--close-void-tags` ajoute la barre oblique aux balises vides html pour vous. Un `<path>` svg est laissé tel qu'il est écrit : fermez-le donc à la main.

À éviter :

```html
<br>
<meta charset="utf-8">
```

À privilégier :

```html
<br />
<meta charset="utf-8" />
```

#### D018

`(Django) Internal links should use the {% url ... %} pattern.`

Les URL internes codées en dur deviennent silencieusement obsolètes quand le chemin d'une route change dans urls.py, ce qui produit des liens cassés et des actions de formulaire mortes qu'aucun test sur l'URLconf ne détectera. `{% url %}` résout le chemin à partir du nom de la route : renommer un chemin met donc à jour tous les liens à la fois.

À éviter :

```html
<a href="/accounts/login">Login</a>
```

À privilégier :

```html
<a href="{% url 'login' %}">Login</a>
```

#### H018

`Void tags are self closing by nature and must end with ">", not "/>"`

Dans le HTML living standard, la barre oblique finale d'un élément vide n'a aucune signification (le parseur l'ignore) : écrire `<br />` suggère un comportement auto-fermant à la XML que HTML n'a pas, et peut inciter les lecteurs à ajouter des barres obliques à des balises non vides, où une / égarée est silencieusement ignorée et masque des bugs de balises non fermées. Cette règle impose des terminaisons > simples sur les éléments vides.

Désactivée par défaut ; activez-la avec `--include=H018`. Incompatible avec H017 ; n'activez qu'une des deux conventions. Le `<path />` SVG est exempté, puisque SVG est du XML et exige la barre oblique. Non signalée avec `--close-void-tags`, puisque le formateur écrit alors la barre oblique que cette règle signale.

À éviter :

```html
<br />
<meta charset="utf-8" />
```

À privilégier :

```html
<br>
<meta charset="utf-8">
```

#### J018

`(Jinja) Internal links should use the {{ url_for() ... }} pattern.`

Les URL internes codées en dur cassent silencieusement quand le chemin d'une route change ou que l'application est montée sous un préfixe, ce qui laisse des liens morts et des actions de formulaire qui envoient vers des 404. url_for() construit l'URL à partir du nom de l'endpoint : les changements de routes se propagent donc automatiquement à tous les templates.

À éviter :

```html
<a href="/accounts/login">Login</a>
```

À privilégier :

```html
<a href="{{ url_for('login') }}">Login</a>
```

#### H019

`Replace 'javascript:abc()' with on_ event and real url.`

Les URL javascript: cassent le clic du milieu et l'ouverture dans un nouvel onglet, ne font rien quand JavaScript est désactivé ou ne se charge pas, sont bloquées par les Content Security Policies strictes, et sont un point d'injection XSS classique. Utilisez une vraie URL pour le href et attachez plutôt le comportement avec un gestionnaire d'événement. Sous une CSP stricte, les gestionnaires on* en ligne sont bloqués eux aussi : le onclick montré est la correction minimale dans le template ; préférez attacher l'écouteur avec addEventListener depuis un fichier de script.

À éviter :

```html
<a href="javascript:openPopup()">Open popup</a>
```

À privilégier :

```html
<a href="{% url 'popup' %}" onclick="openPopup(event)">Open popup</a>
```

#### H020

`Empty tag pair found. Consider removing.`

Une paire de balises vide n'affiche aucun contenu mais crée tout de même un nœud DOM qui peut recevoir des marges, des bordures ou des espacements flex/grid des feuilles de style, ce qui produit des espacements fantômes difficiles à retrouver ; il s'agit généralement d'un reste de balisage d'une modification antérieure. Les balises légitimement vides dans un balisage normal (td, th, li, dt, dd, slot) sont exemptées. Les balises portant un attribut quelconque (points de montage JS comme `<div id="app">``</div>`, éléments de police d'icônes comme `<i class="fa fa-user">``</i>`) ne sont pas signalées non plus ; seules les paires vides sans aucun attribut correspondent.

À éviter :

```html
<p>Saved.</p>
<span> </span>
```

À privilégier :

```html
<p>Saved.</p>
```

#### H021

`Inline styles should be avoided.`

Les styles en ligne ont une spécificité supérieure à celle de tout sélecteur de feuille de style, si bien que les surcharger plus tard exige !important ; ils sont bloqués par les Content Security Policies dont style-src ne contient pas 'unsafe-inline' ; et ils dispersent la présentation dans les templates, si bien qu'un changement de thème ou de design oblige à modifier le balisage au lieu d'une seule feuille de style. Déplacez la déclaration dans une classe CSS. Une exception légitime : les templates d'e-mails HTML, où de nombreux clients de messagerie suppriment les blocs `<style>` et où les styles en ligne sont la technique standard ; excluez vos répertoires de templates d'e-mails ou désactivez cette règle pour eux.

À éviter :

```html
<div style="color: red;">Wrong username or password.</div>
```

À privilégier :

```html
<div class="error">Wrong username or password.</div>
```

#### H022

`Use HTTPS for external links.`

Des sous-ressources en http:// simple sur une page servie en HTTPS constituent du contenu mixte : les navigateurs bloquent purement et simplement les scripts, les feuilles de style et les iframes, et mettent à niveau automatiquement les images ou affichent un avertissement. Un lien `<a>` vers une page en http:// n'est pas du contenu mixte, mais il envoie tout de même les visiteurs sur une connexion non chiffrée, exposée à l'interception et à la falsification. Les références à des hôtes internes qui n'ont réellement pas de TLS seront signalées elles aussi ; faites taire ces endroits avec un bloc `{# djlint:off H022 #}` plutôt que de désactiver la règle.

À éviter :

```html
<a href="http://example.com">Example</a>
```

À privilégier :

```html
<a href="https://example.com">Example</a>
```

#### H023

`Do not use entity references.`

Les documents HTML5 sont en UTF-8 : le caractère littéral fonctionne donc partout et c'est ce que les relecteurs lisent réellement ; une faute de frappe dans une référence d'entité (par ex. `&mdsah;`) n'est pas détectée par le navigateur et s'affiche telle quelle sous forme de texte cassé. djLint autorise les entités porteuses de syntaxe (`&lt;`, `&gt;`, `&amp;`, `&quot;`, `&apos;`, ainsi que les accolades `&lbrace;` et `&rbrace;` avec `&percnt;`, `&num;` et `&dollar;`, qui, écrites en clair, compléteraient un délimiteur de template) et celles qui désignent un caractère invisible, donc impossible à relire sous forme littérale : les espaces (`&nbsp;`, `&thinsp;`, `&hairsp;`), les liants et marques (`&zwnj;`, `&zwj;`, `&lrm;`, `&rlm;`) et `&shy;`, sous forme nommée, décimale comme hexadécimale.

`--reformat` réécrit l'entité sous forme de caractère pour vous. Une entité écrite à l'intérieur d'une balise de template fait partie de la balise plutôt que de la page : ni la règle ni le formateur n'y touchent. `--no-entity-formatting` désactive la réécriture mais laisse la règle active : une entité est donc toujours signalée. Ajoutez `H023` à `ignore` pour conserver les entités.

À éviter :

```html
<p>Dates 1900 &mdash; 2000</p>
```

À privilégier :

```html
<p>Dates 1900 — 2000</p>
```

#### H024

`Omit type on scripts and styles.`

text/javascript et text/css sont les valeurs par défaut HTML5 pour `<script>` et `<style>` : l'attribut est donc un poids mort que le navigateur ignore, et la spécification WHATWG dit explicitement de l'omettre. Le supprimer évite aussi des chaînes MIME périmées qui cassent l'élément quand elles sont recopiées sur des scripts de module (où type="module" compte réellement).

À éviter :

```html
<script type="text/javascript" src="app.js">
```

À privilégier :

```html
<script src="app.js"></script>
```

#### H025

`Tag seems to be an orphan.`

Une balise sans sa balise ouvrante ou fermante correspondante oblige la récupération d'erreurs du navigateur à deviner où l'élément se termine : le balisage qui suit est alors absorbé dans le mauvais élément, et la mise en page, les sélecteurs CSS et les requêtes DOM en JavaScript cassent silencieusement, et différemment selon les navigateurs. H025 signale aussi une `<ol>` ou une `<ul>` ouverte à l'intérieur d'un `<p>` : le parseur HTML ferme le paragraphe avant la liste, si bien que le balisage ne s'imbrique jamais comme il est écrit.

À éviter :

```html
<div>
  <p>Hello</p>
```

À privilégier :

```html
<div>
  <p>Hello</p>
</div>
```

#### H026

`Empty id and class tags can be removed.`

Aucun sélecteur de classe ou d'id ne correspond à un attribut vide, et un id vide est du HTML invalide (la valeur d'un id ne doit pas être la chaîne vide). Un sélecteur de présence d'attribut comme `div[class]` y correspond tout de même : en supprimer un est donc visible pour une feuille de style écrite de cette façon. Cela signale généralement un bug de template où une variable devait être interpolée : le supprimer ou le remplir évite que ce bug passe inaperçu.

À éviter :

```html
<div id="" class="">content</div>
```

À privilégier :

```html
<div>content</div>
```

#### T027

`Unclosed string found in template syntax.`

Un guillemet ouvert mais jamais fermé dans `{% ... %}` ou `{{ ... }}` empêche le moteur de templates d'analyser correctement la balise : Django et Jinja lèvent une TemplateSyntaxError au rendu, ou absorbent silencieusement le reste des arguments de la balise comme contenu de la chaîne, si bien que la page renvoie une erreur 500 ou s'affiche avec des arguments manquants.

À éviter :

```html
{% trans "Welcome %}
```

À privilégier :

```html
{% trans "Welcome" %}
```

#### T028

`Consider using spaceless tags inside attribute values. {%- if/for -%}`

Désactivée par défaut ; activez-la avec `--include=T028`.

Les espaces qu'une balise sans espaces supprime sont des espaces qui s'affichent : ne l'appliquez donc que là où l'attribut n'a rien à perdre. `alt="{%- if brand -%}Acme{%- endif -%} logo"` s'affiche `Acmelogo`, et un `d="M12 {%- if big -%}20{%- endif -%} 4Z"` svg devient un tracé différent. C'est pourquoi la règle est facultative.

Les balises de template dans une valeur d'attribut émettent les espaces et sauts de ligne qui les entourent dans l'attribut rendu : un href ou un src construit avec de simples balises `{% if %}`/`{% for %}` peut donc contenir des espaces parasites et produire des URL cassées. Les balises de contrôle des espaces de Jinja/Nunjucks (`{%- ... -%}`) suppriment ces espaces environnants pour que l'attribut s'affiche comme une seule valeur propre. L'attribut class est exempté, puisque des espaces superflus entre noms de classes sont sans conséquence.

Ne s'applique pas au profil django : les balises de template de Django ne prennent pas en charge le contrôle des espaces `{%- -%}`.

À éviter :

```html
<a href="{% if x %}/home{% endif %}"></a>
```

À privilégier :

```html
<a href="{%- if x -%}/home{%- endif -%}"></a>
```

#### H029

`Consider using lowercase form method values.`

La spécification HTML définit les mots-clés de méthode de formulaire en minuscules (get, post) ; les navigateurs n'acceptent les variantes en majuscules que par une correspondance de repli insensible à la casse. Conserver la forme canonique en minuscules rend les templates cohérents et faciles à rechercher avec grep, et évite les plaintes des validateurs stricts et des chaînes d'outils basées sur XHTML.

À éviter :

```html
<form method="POST"></form>
```

À privilégier :

```html
<form method="post"></form>
```

#### H030

`Consider adding a meta description.`

Les moteurs de recherche utilisent la meta description comme extrait sous le titre de votre page dans les résultats ; sans elle, ils composent un extrait à partir d'un texte quelconque de la page, ce qui nuit au taux de clics et produit de mauvais aperçus de liens quand la page est partagée.

Ne se déclenche que sur les fichiers contenant un document `<html>`...`</html>` complet. L'argument de l'extrait vaut pour les pages indexées publiquement ; pour les applications derrière une authentification ou sur un intranet, cette règle est couramment désactivée.

À éviter :

```html
<html lang="en">
  <head><title>Home</title></head>
  <body>Welcome</body>
</html>
```

À privilégier :

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

Des suites d'espaces ou de tabulations entre les arguments d'une balise de template sont un bruit invisible : elles masquent les vraies différences dans les diffs, peuvent rendre difficile le repérage d'un argument manquant, et s'écartent du style à espace unique que produit le formateur de djLint, ce qui entraîne des reformatages inutiles. Les espaces à l'intérieur des chaînes entre guillemets sont préservés et ne sont pas signalés.

À éviter :

```html
{% static  'css/style.css' %}
```

À privilégier :

```html
{% static 'css/style.css' %}
```

#### H033

`Extra whitespace found in form action.`

Les espaces en début ou en fin de la valeur action d'un formulaire font partie de l'URL rendue. Les navigateurs les suppriment à l'analyse, mais les clients non navigateurs et les tests qui utilisent la valeur littérale peuvent ne pas le faire, et autour d'une balise `{% url %}`, l'espace parasite signale presque toujours une faute de frappe qui produit une URL de soumission ne correspondant à aucune route côté serveur.

À éviter :

```html
<form action="{% url 'search' %} " method="get">
    <button>Search</button>
</form>
```

À privilégier :

```html
<form action="{% url 'search' %}" method="get">
    <button>Search</button>
</form>
```

#### T034

`Did you intend to use {% ... %} instead of {% ... }%?`

}% est presque toujours une faute de frappe pour %}. Le moteur de templates ne reconnaît pas }% comme délimiteur de balise : la balise n'est donc jamais analysée, et le texte brut {% ... }% s'échappe dans le HTML rendu, ou le moteur lève une erreur de syntaxe en rencontrant la balise non fermée.

À éviter :

```html
{% include "footer.html" }%
```

À privilégier :

```html
{% include "footer.html" %}
```

#### H036

`Do not use br tags for spacing.`

La spécification html n'autorise `<br>` que pour un saut de ligne qui fait partie du contenu lui-même, comme dans une adresse postale ou un poème, et cet usage n'est pas touché. Ce qui est signalé, c'est l'usage de présentation que la spécification exclut : une suite de deux sauts ou plus, qui crée un espace vertical, et un saut collé au bord intérieur d'un élément de bloc, qui n'affiche rien que sa propre marge n'afficherait déjà. Les deux cassent la remise en forme du texte aux faibles largeurs, et un lecteur d'écran annonce un saut forcé là où il n'y a rien à annoncer.

À éviter :

```html
<p>Shipping is free.<br><br>Delivery takes 3 days.</p>
```

À privilégier :

```html
<p>Shipping is free.</p>
<p>Delivery takes 3 days.</p>
```

#### H037

`Duplicate attribute found.`

Les attributs en double sont du HTML invalide, et les navigateurs ne gardent que la première occurrence et ignorent silencieusement les autres : la deuxième valeur de class ou de style ne prend jamais effet, ce qui masque de vrais bugs. La vérification tient compte des templates : un attribut répété dans des branches mutuellement exclusives (`{% if %}`/`{% else %}`) n'est pas signalé, puisqu'une seule copie peut être rendue.

À éviter :

```html
<div class="card" id="profile" class="active">...</div>
```

À privilégier :

```html
<div class="card active" id="profile">...</div>
```

#### T038

`Block tag has no matching end tag.`

Une balise de bloc comme `{% if %}`, `{% for %}` ou `{% macro %}` sans sa balise de fin correspondante est une TemplateSyntaxError bloquante dans Django et Jinja : la page ne s'affiche pas au moment de la requête, ce que cette règle détecte avant le déploiement. Elle signale aussi les balises de fin orphelines sans balise ouvrante et les blocs mal entrelacés (par ex. `{% if %}``{% for %}``{% endif %}`).

L'appariement `{% block %}`/`{% endblock %}` et les noms d'endblock qui ne correspondent pas sont vérifiés par cette règle ; T003 (désactivée par défaut) exige en plus un nom sur chaque `{% endblock %}` multiligne. Les balises de bloc personnalisées déclarées via custom_blocks sont aussi vérifiées, y compris leur forme auto-fermante / %}.

À éviter :

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
```

À privilégier :

```html
{% if user.is_authenticated %}
<p>Welcome back!</p>
{% endif %}
```

#### T039

`Unclosed template tag found.`

Une balise de template ouverte avec `{{` ou `{%` mais jamais fermée par le `}}` ou le `%}` correspondant n'est pas analysée comme une balise : Django/Jinja lèvent une TemplateSyntaxError ou affichent les accolades brutes dans la page, et tout ce qui précède le délimiteur suivant peut être silencieusement absorbé. Ces fautes de frappe (une seule accolade manquante, un délimiteur dépareillé) passent facilement inaperçues en relecture, car le template peut tout de même s'afficher en partie.

À éviter :

```html
<p>{{ user.name }</p>
```

À privilégier :

```html
<p>{{ user.name }}</p>
```

#### T040

`Missing or empty template name in extends or include tag.`

Une balise `{% extends %}` ou `{% include %}` dont le nom de template est absent, vide ou composé uniquement d'espaces n'a rien à charger : Django lève TemplateSyntaxError quand le nom est complètement absent, et TemplateDoesNotExist au rendu quand il est vide, si bien que la page renvoie une erreur 500 en production alors que le fichier de template lui-même semble syntaxiquement plausible.

À éviter :

```html
{% extends "" %}
```

À privilégier :

```html
{% extends "base.html" %}
```

#### H041

`Tag is closed in a different template block than it was opened.`

Quand une balise HTML est ouverte dans un `{% block %}` mais fermée dans un autre, un template enfant qui ne remplace qu'un de ces blocs hérite de la moitié de l'élément, ce qui produit un balisage déséquilibré dans la page rendue ; les navigateurs ferment ou réimbriquent alors les éléments de façon imprévisible, cassant la mise en page et les sélecteurs CSS loin du template réellement modifié. Ouvrir et fermer chaque élément dans le même bloc permet de remplacer chaque bloc indépendamment, sans risque.

À éviter :

```html
{% block content %}
<div class="wrapper">
{% endblock content %}
{% block footer %}
</div>
{% endblock footer %}
```

À privilégier :

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

Django refuse de compiler un template dans lequel une autre balise précède `{% extends %}`, et le texte écrit avant est rendu : il s'échappe donc dans la page avant tout ce que produit le template parent. Jinja rend aussi ce texte, et nunjucks le supprime : quel que soit le moteur, le template ne fait pas ce qu'il semble faire.

Un commentaire `{# #}` n'affiche rien et ne compte pas, pas plus que le contenu d'un bloc `{% comment %}`, <code>{&#37; raw %}</code> ou `{% verbatim %}`, nommé ou non, une région `{# djlint:off #}` sous l'une de ses trois graphies, ou un front matter yaml. Un commentaire html compte, lui : le moteur l'écrit dans la page avant le doctype du template parent, ce qui est la fuite que vise cette règle. Comptent aussi un bloc `{% blocktrans %}`, un bloc `{% filter %}` et un bloc `<?php ?>`, qui produisent chacun un rendu. Seul le premier `{% extends %}` est vérifié ; un second est une erreur à part entière. Avec les profils jinja et nunjucks, une balise de branche placée avant ne compte pas, puisque jinja documente `{% if x %}{% extends "a.html" %}{% else %}{% extends "b.html" %}{% endif %}` comme la façon de choisir un parent ; django lit le reste du template dans le `{% extends %}` puis rejette le `{% endif %}` : avec ce profil, une balise de branche compte donc.

Ne s'applique pas aux profils handlebars, golang, liquid et angular.

À éviter :

```html
{% load static %}
{% extends "base.html" %}
```

À privilégier :

```html
{% extends "base.html" %}
{% load static %}
```

#### H042

`Label for attribute has no matching element id in this file.`

La vérification ne s'exécute que sur les fichiers qu'elle peut analyser de façon fiable : si le fichier contient quoi que ce soit qui pourrait produire un id que ce fichier ne montre jamais (une sortie `{{ ... }}` comme un widget de formulaire, un `{% include %}` ou un `{% extends %}`, ou une balise de template non reconnue), la règle reste silencieuse pour ce fichier. Là où elle s'exécute, un signalement correspond à une vraie association cassée.

À éviter :

```html
<label for="email">Email</label>
<input id="username">
```

À privilégier :

```html
<label for="email">Email</label>
<input id="email">
```

#### T042

`Content outside a block is not rendered in a template that extends another.`

Dès qu'un template en étend un autre, c'est le parent qui décide de ce qui est produit, et l'enfant ne fait que remplir les blocs du parent. Le texte ou le html écrit après `{% extends %}` et en dehors de tout `{% block %}` est silencieusement écarté au rendu : un paragraphe qui semble correct dans le source n'atteint jamais la page.

Une balise de template placée là s'exécute quand même : `{% load %}`, `{% set %}` et un `{% if %}` entourant un bloc ne sont donc pas touchés, pas plus que les commentaires `{# #}` et `{% comment %}`, les commentaires html, les blocs <code>{&#37; raw %}</code> et `{% verbatim %}`, et le corps d'un `{% macro %}`, d'un `{% set %}` sous forme de bloc, d'un `{% partialdef %}` ou d'un `{% addtoblock %}`, qui est capturé plutôt que produit. Le texte d'un `{% blocktrans %}` est signalé, puisqu'un `{% blocktrans %}` n'est pas un `{% block %}`. Seul le contenu situé après la balise extends est pris en compte, et chaque portion de ce contenu est signalée une seule fois, à son début.

Le moteur lit les balises de template avant le html : un `{% extends %}` écrit dans un commentaire html ou dans un `<pre>` s'exécute donc quand même et fait tout de même du fichier un enfant ; seuls `{# #}`, `{% comment %}`, <code>{&#37; raw %}</code> et `{% verbatim %}` en cachent vraiment un. Le texte d'un commentaire html n'atteint de toute façon aucun lecteur et n'est pas signalé, mais les balises qui y sont écrites sont tout de même lues.

Ne s'applique pas aux profils handlebars, golang, liquid et angular.

À éviter :

```html
{% extends "base.html" %}
<p>This paragraph is never shown.</p>
{% block content %}
<h1>Welcome</h1>
{% endblock %}
```

À privilégier :

```html
{% extends "base.html" %}
{% block content %}
<h1>Welcome</h1>
<p>This paragraph is shown.</p>
{% endblock %}
```

#### H043

`Button tag should have a type attribute.`

Un `<button>` sans `type` vaut `submit` par défaut : un bouton écrit pour exécuter un script soumet donc aussi le formulaire qui l'entoure, et la page se recharge. Écrire le type explicitement l'évite.

À éviter :

```html
<form>
  <button onclick="preview()">Preview</button>
</form>
```

À privilégier :

```html
<form>
  <button type="button" onclick="preview()">Preview</button>
</form>
```

#### T043

`Block name is used more than once in the template.`

Django, Jinja et Nunjucks refusent tous d'analyser un template qui donne le même nom à deux blocs : la page ne se charge pas du tout. Les moteurs ne tiennent pas compte du fait que les deux blocs se trouvent dans des branches différentes d'un `{% if %}` : chaque nom de bloc doit donc être unique dans tout le template, que les blocs soient côte à côte ou imbriqués l'un dans l'autre.

Seul `{% block %}` compte : un `{% blocktrans %}` n'est pas un bloc, et un `{% endblock name %}` ne fait que nommer le bloc qu'il ferme. Les noms sont comparés tels qu'ils sont écrits, puisque les moteurs traitent `Content` et `content` comme deux blocs.

Seul ce que le moteur lui-même n'analyse jamais est ignoré : un commentaire de template, un bloc `{% comment %}`, le corps d'un <code>{&#37; raw %}</code> ou d'un `{% verbatim %}`, et une région `djlint:off`. Un bloc écrit dans un commentaire html, dans le corps d'un `<script>`, `<style>`, `<pre>` ou `<textarea>`, ou dans le corps d'un `{% filter %}` est tout de même compté, puisque le moteur lit tout cela et lève une erreur sur le nom en double de la même façon.

Un `{% embed %}` ouvre sa propre portée : les blocs qu'il contient remplissent le template intégré plutôt que celui-ci, si bien que deux embeds du même partiel peuvent chacun écrire `{% block body %}`. Un nom répété au sein d'un même embed est tout de même signalé.

Ne s'applique pas aux profils handlebars, golang, liquid et angular.

À éviter :

```html
{% block content %}{% endblock %}
{% block content %}{% endblock %}
```

À privilégier :

```html
{% block content %}{% endblock %}
{% block sidebar %}{% endblock %}
```

#### H044

`Thead should not mix th and td cells.`

Chaque ligne est jugée isolément : la ligne d'explication en `td` que la spécification html place dans un `thead` à côté de la ligne d'en-têtes n'est donc pas un mélange. Un `td` vide en début de ligne est la cellule d'angle d'un tableau dont les en-têtes descendent le long de la première colonne, ce qui est le balisage que demande le tutoriel d'accessibilité du W3C : il est donc ignoré.

Un `th` et un `td` n'ont pas la même signification pour un lecteur d'écran, et généralement pas le même css : une seule cellule égarée dans une ligne d'en-tête se lit comme une donnée et n'a pas le style des colonnes voisines. Ce mélange est du html valide, ce qui le rend difficile à repérer.

À éviter :

```html
<thead>
  <tr>
    <th>Name</th>
    <td>Size</td>
  </tr>
</thead>
```

À privilégier :

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

Ne s'applique pas aux profils golang, handlebars et angular.

Une balise d'affichage imprime une valeur, alors que `if`, `for`, `url`, `include` et les autres sont des instructions qui ont leur place dans une balise de bloc. Django, Jinja et Nunjucks rejettent tous `{{ if x }}` avec une erreur de syntaxe, et un mot-clé de fermeture isolé, comme `{{ endif }}`, est lu comme une variable qui n'affiche rien, tandis que le bloc qu'il devait fermer reste ouvert : la page ne se charge pas, ou affiche ce que la condition aurait dû masquer.

Un mot-clé seul est un nom de variable ordinaire : `{{ url }}`, `{{ url|default:"/" }}` et `{{ set.name }}` ne sont donc pas signalés. Seul l'est un mot-clé suivi d'un argument, ainsi qu'un mot-clé de fermeture ou de branche isolé comme `{{ endif }}` ou `{{ else }}`. Un mot-clé de contrôle comme `if` ou `for` ne peut pas commencer une expression : tout ce qui le suit est donc un argument, opérateur compris, et `{{ if -1 > count }}` est signalé. Les autres noms servent aussi de variables et de fonctions, et seule une chaîne entre guillemets ou un mot y compte comme argument : une expression qui commence par l'un d'eux est donc laissée telle quelle. `{{ url ~ "/x" }}`, `{{ url if url else "#" }}`, `{{ url ? url : '#' }}`, `{{ block ('title') }}`, `{{ block .super }}` et `{{ filter [0] }}` ne déclenchent rien.

Le corps d'un bloc <code>{&#37; raw %}</code> ou `{% verbatim %}` est du texte plutôt que de la syntaxe de template et il est ignoré, y compris sous la forme nommée `{% verbatim vueapp %}...{% endverbatim vueapp %}` : un `{{ }}` de Vue ou de Handlebars ainsi protégé n'est pas signalé. Un `{{ }}` écrit dans un argument entre guillemets d'une balise de bloc, comme dans `{% trans "Write {{ if x }} instead" %}`, est du texte que le moteur imprime et il est lui aussi laissé tel quel.

À éviter :

```html
{{ if user.is_active }}
```

À privilégier :

```html
{% if user.is_active %}
```

#### H045

`Iframe tag should have a title attribute.`

Un lecteur d'écran annonce une iframe par son nom accessible. Sans nom, il lit l'url du cadre, ou rien du tout, et il n'y a aucun moyen de savoir ce qu'est la page intégrée avant d'y entrer. Les WCAG rangent cela sous le critère 4.1.2 Nom, rôle et valeur, et axe comme html-validate effectuent cette vérification par défaut.

Le nom peut venir de `title`, `aria-label` ou `aria-labelledby`, et n'importe lequel des trois satisfait la règle. Un nom écrit par une balise de template compte : un cadre dont le titre varie selon la page n'est donc pas signalé.

À éviter :

```html
<iframe src="/report/"></iframe>
```

À privilégier :

```html
<iframe src="/report/" title="Quarterly report"></iframe>
```

#### T045

`Template tag inside an html comment still runs; use a template comment to disable it.`

Un commentaire html cache le balisage au navigateur, pas au moteur de templates. `<!-- {% include "debug.html" %} -->` rend toujours le fichier, et `<!-- {% if debug %}...{% endif %} -->` est toujours évalué, dans Django, Jinja, Nunjucks, Handlebars comme dans Go : une balise ainsi commentée continue de s'exécuter, et ce qu'elle écrit atterrit dans le commentaire ou, s'il contient `-->`, en sort. Seul un commentaire de template, `{# #}` dans Django et Jinja, `{{! }}` dans Handlebars ou `{{/* */}}` dans Go, empêche une balise de s'exécuter.

Seule une balise d'instruction est signalée : `{% %}` avec les profils qui en disposent, une section, une fermeture ou un partiel handlebars, et un mot-clé Go comme `{{if}}` ou `{{end}}`. Une valeur imprimée dans un commentaire, comme dans `<!-- built {{ version }} -->`, est un usage délibéré et n'est pas touchée, pas plus qu'une balise dans un commentaire de template, un bloc `{% comment %}` ou un bloc raw, ni un commentaire conditionnel pour Internet Explorer, `<!--[if IE]> ... <![endif]-->`, dont le corps est du balisage destiné au navigateur qu'il nomme.

Un mot-clé Go seul est un nom de variable ordinaire dans tous les autres moteurs : `<!-- period {{ start }} to {{ end }} -->` et `<!-- Template: {{ template }} -->` sont des valeurs sous Django, Jinja, Nunjucks, Handlebars et Liquid, et ne se lisent comme des instructions qu'avec `--profile golang`. Un mot-clé accompagné d'un opérande Go, comme `{{ if .X }}` et `{{ template "footer" . }}`, est une instruction qu'aucun autre moteur n'imprime, et il est signalé quel que soit le profil. De même, `{%` n'est lu que là où le moteur en dispose : c'est du texte avec `--profile handlebars` et `--profile golang`, et une ouverture qu'aucune accolade fermante ne suit, comme dans `<!-- battery at 50{% charge -->`, est la prose qu'elle semble être. Un commentaire conditionnel est un commentaire écrit comme tel, qui s'ouvre par `<!--[if` et se ferme par son `<![endif]-->`, quelle que soit la casse ; s'il reste non fermé, c'est le commentaire ordinaire qu'y voit un navigateur, et les balises qu'il contient sont signalées.

À éviter :

```html
<!-- {% include "banner.html" %} -->
```

À privilégier :

```html
{# {% include "banner.html" %} #}
```

#### H046

`Tabindex should not be positive.`

Un `tabindex` positif place un élément en tête de l'ordre de tabulation, avant tout ce qui n'en a pas. Un seul suffit à réorganiser toute la page pour un utilisateur au clavier, et l'ordre doit ensuite être maintenu à la main dans chaque template qui ajoute un contrôle. Les WCAG traitent ce point sous le critère 2.4.3 Parcours du focus.

`0` place un élément dans l'ordre de tabulation à l'endroit que lui donne le document, et `-1` l'en retire tout en le laissant focalisable par script. Aucun des deux n'est signalé, pas plus qu'une valeur écrite par une balise de template, dont le nombre n'est pas connu ici.

À éviter :

```html
<input tabindex="1">
```

À privilégier :

```html
<input tabindex="0">
```

#### H047

`Aria-hidden should not be set on a focusable element.`

`aria-hidden="true"` retire un élément de l'arbre d'accessibilité mais le laisse dans l'ordre de tabulation : un utilisateur au clavier y arrive donc quand même et n'entend rien d'annoncé. Masquer une icône décorative est l'usage ordinaire de l'attribut et n'est pas signalé ; seul l'est un élément qui prend le focus par lui-même.

Un élément est considéré comme focalisable lorsqu'il s'agit d'un `button`, `select`, `textarea`, `iframe` ou `summary`, d'un `a` ou `area` avec un `href`, d'un `input` qui n'est pas masqué, d'un `audio` ou `video` avec `controls`, ou de tout élément portant `contenteditable` ou un `tabindex` de `0` ou plus. Un contrôle `disabled`, ou doté de `tabindex="-1"`, est déjà hors de l'ordre de tabulation et n'est pas touché.

À éviter :

```html
<button aria-hidden="true">Close</button>
```

À privilégier :

```html
<button type="button" aria-label="Close"><span aria-hidden="true">x</span></button>
```

#### H048

`Aria attribute is not one the specification defines.`

Un attribut aria mal orthographié ne fait absolument rien. Aucun navigateur ne prévient, aucun lecteur d'écran ne le signale, et le balisage garde l'apparence d'avoir été rendu accessible : `aria-lable` peut ainsi rester des années dans un template pendant que le contrôle qu'il devait nommer reste sans nom.

Les noms que connaît la règle sont ceux que définit ARIA. Une liaison écrite par un framework n'est pas un simple nom aria : `:aria-label`, `v-bind:aria-label` et `[attr.aria-label]` ne sont donc pas touchés.

À éviter :

```html
<button type="button" aria-lable="Close">x</button>
```

À privilégier :

```html
<button type="button" aria-label="Close">x</button>
```

#### H049

`Viewport should not stop the page being zoomed.`

`user-scalable=no`, ainsi qu'un `maximum-scale` inférieur à 2, empêchent d'agrandir une page sur un téléphone, ce qui, pour beaucoup de gens, est le seul moyen de la lire. Les WCAG demandent 200 % sous le critère 1.4.4 Redimensionnement du texte. Les navigateurs ignorent de plus en plus cette restriction, mais la balise désactive tout de même le zoom partout où elle est respectée.

Le nom et le contenu sont trouvés quel que soit l'ordre dans lequel ils sont écrits.

À éviter :

```html
<meta name="viewport" content="width=device-width, user-scalable=no">
```

À privilégier :

```html
<meta name="viewport" content="width=device-width, initial-scale=1">
```

#### H050

`Element is obsolete and should be replaced.`

`<center>`, `<font>`, `<big>`, `<strike>` et `<tt>` ont été abandonnés quand le css a pris en charge la présentation, et `<marquee>`, `<blink>`, `<nobr>` et `<spacer>` n'ont jamais été standard. Le html n'en définit plus aucun : rien ne garantit donc comment un navigateur les met en page, et une feuille de style ne peut pas les cibler comme elle cible une classe.

Les éléments que connaît la règle sont `acronym`, `applet`, `basefont`, `bgsound`, `big`, `blink`, `center`, `dir`, `font`, `frame`, `frameset`, `isindex`, `keygen`, `marquee`, `menuitem`, `nobr`, `noembed`, `noframes`, `plaintext`, `spacer`, `strike`, `tt` et `xmp`. Seule la balise ouvrante est signalée, pour que chaque élément ne soit nommé qu'une fois, et un élément personnalisé dont le nom commence simplement par l'un d'eux, comme `<font-picker>`, n'est pas touché.

À éviter :

```html
<center><font color="red">Warning</font></center>
```

À privilégier :

```html
<p class="warning">Warning</p>
```

#### H051

`Role is not one ARIA defines for markup.`

Un rôle qu'aucune spécification ne nomme est purement et simplement ignoré, et l'élément garde la signification qu'il avait déjà : `role="buton"` laisse donc un `<div>` être un `<div>`, c'est-à-dire rien pour un lecteur d'écran, alors que le balisage donne l'impression de lui avoir attribué une fonction. Rien ne signale l'erreur, d'où l'intérêt de repérer cette faute de frappe.

Les noms que connaît la règle sont les rôles que définit ARIA pour les auteurs, ainsi que ceux qu'ajoutent DPUB-ARIA (`doc-chapter` et les autres) et GRAPHICS-ARIA (`graphics-symbol` et les autres). Les rôles abstraits d'ARIA, comme `landmark` et `sectionhead`, sont signalés : la spécification indique qu'ils servent à construire son ontologie et ne doivent pas être écrits dans le balisage.

Un `role` peut contenir plusieurs noms, sous forme de liste de repli, et chacun est vérifié. Une valeur contenant de la syntaxe de template est impossible à connaître et n'est pas touchée, pas plus qu'une liaison écrite par un framework, comme `:role` ou `[attr.role]`.

À éviter :

```html
<div role="buton">Save</div>
```

À privilégier :

```html
<button type="button">Save</button>
```

#### H052

`Meta refresh should not reload or redirect the page on a timer.`

Un rafraîchissement temporisé retire la page à la personne en train de la lire. Quelqu'un qui lit lentement, qui utilise un lecteur d'écran ou qui a simplement été interrompu perd sa place sans avertissement et sans moyen de l'empêcher, ce qui enfreint le critère 2.2.1 Réglage du délai des WCAG, et un rafraîchissement qui recharge la même page fait perdre tout ce qui y avait été saisi.

Un délai nul est une redirection immédiate plutôt qu'une temporisation, ce que les WCAG autorisent quand une redirection côté serveur n'est pas possible : il n'est donc pas signalé. Les deux attributs sont trouvés quel que soit l'ordre dans lequel ils sont écrits.

À éviter :

```html
<meta http-equiv="refresh" content="30">
```

À privilégier :

```html
<meta http-equiv="refresh" content="0; url=/next-page">
```

#### H053

`Id is used more than once in the file.`

Un id nomme un seul élément. Un second élément portant le même id casse `getElementById`, `<label for>`, les liens vers des fragments et `aria-labelledby` : le navigateur prend le premier et ignore silencieusement les autres, si bien qu'un label, un lien ou un script atterrit sur le mauvais élément sans le moindre avertissement.

Deux ids placés dans des branches exclusives d'un même `{% if %}...{% else %}...{% endif %}` ne sont jamais rendus tous les deux : ils ne sont donc pas signalés. Une boucle `{% for %}` ou un `{% block %}` n'est pas une branche : un id à l'intérieur et le même id à l'extérieur sont tous deux rendus, et c'est le second qui est signalé. Une valeur écrite par une balise de template est impossible à connaître et n'est pas touchée, pas plus qu'une valeur vide. Les ids sont comparés exactement, comme le fait le navigateur : `save` et `Save` sont donc deux ids.

Les branches sont lues dans le langage dans lequel le fichier est écrit, et avec tous les espaces que ce langage autorise entre les délimiteurs et le nom de la balise : `{% elif %}` et `{% else %}`, le `{% elsif %}` et le `{% when %}` de liquid, le `{{ else }}` de go, une instruction de ligne mako `% else:`, et le `{{else}}` de handlebars, son `{{else if x}}` chaîné et la section inverse de tout bloc `{{#helper}}`, helpers personnalisés compris. Le contenu d'un `<template>` est un fragment de document à part que `getElementById` n'atteint jamais : un id qui s'y trouve n'est donc comparé qu'aux ids de ce même `<template>`. Deux templates peuvent ainsi contenir chacun une ligne portant le même id, alors que deux de ces lignes dans un même template sont tout de même signalées. Un id situé dans un commentaire, dans le corps d'un <code>{&#37; raw %}</code> ou d'un `{% verbatim %}`, ou dans une région `djlint:off` n'est pas lu du tout.

À éviter :

```html
<button type="submit" id="submit">Save</button>
<button type="submit" id="submit">Save and continue</button>
```

À privilégier :

```html
<button type="submit" id="submit">Save</button>
<button type="button" id="cancel">Cancel</button>
```

#### H054

`Interactive element should not be nested inside another.`

Le html interdit le contenu interactif à l'intérieur de `<a>` et de `<button>`. Un bouton dans un lien, ou un lien dans un bouton, est un balisage invalide que chaque navigateur répare à sa manière, et un utilisateur de lecteur d'écran ou de clavier se retrouve face à un contrôle qui se comporte comme deux. axe signale la même chose sous le nom « nested-interactive ».

Les conteneurs surveillés sont un `<a>` avec un `href` et un `<button>`, et les contrôles signalés à l'intérieur sont un lien avec un `href`, `button`, `input`, `select` et `textarea`. Un `<a>` sans `href` n'est pas interactif et n'est pas touché, d'un côté comme de l'autre, pas plus qu'un input masqué ou un input dont une balise de template écrit le type. Le contenu d'un `<template>` n'est pas rendu là où il est écrit : un contrôle qui s'y trouve n'est donc pas imbriqué dans le lien qui l'entoure, mais une imbrication écrite à l'intérieur du template est tout de même signalée.

Un attribut est lu là où une balise en écrit un, et nulle part ailleurs : le `href` de `{% if not href %}` nomme une variable, celui de `{# href="{{ url }}" #}` est commenté, et celui de `data-attr=href` appartient à un autre attribut, tandis que le `href` qu'un `{% if %}` écrit entre ses propres balises est un attribut comme un autre. Un lien ou un bouton laissé ouvert se termine avec l'élément qui l'entoure, comme dans un navigateur : une seule faute de frappe ne fait donc pas signaler le reste du fichier ; un lien ou bouton laissé ouvert au niveau racine n'a rien autour de lui pour le terminer et court donc jusqu'à la fin du fichier, où H025 signale aussi l'orphelin.

À éviter :

```html
<a href="/cart"><button>Add</button></a>
```

À privilégier :

```html
<a href="/cart" class="button">Add</a>
```

#### H055

`Lang attribute should be a language tag such as en or pt-BR.`

H005 demande un `lang` sur `<html>`, mais une valeur comme `lang="english"` ou `lang="en_US"` la satisfait sans désigner aucune langue connue d'un navigateur. Un lecteur d'écran se rabat alors sur sa voix par défaut, et la traduction et la césure appliquent les mauvaises règles, ou aucune. La valeur doit être une étiquette BCP 47 : deux ou trois lettres, puis un nombre quelconque de sous-étiquettes d'une à huit lettres ou chiffres, chacune précédée d'un trait d'union, comme dans `en`, `pt-BR` ou `zh-Hant-TW`.

Seule la balise `<html>` est vérifiée, comme pour H005. Une valeur vide est laissée à cette règle, tandis qu'une valeur composée uniquement d'espaces est signalée ici, puisque H005 la considère comme une valeur. Une valeur écrite par une balise de template, comme dans `lang="{{ LANGUAGE_CODE }}"`, ou par un short echo php, comme dans `lang="<?= $lang ?>"`, est impossible à connaître et n'est pas touchée, mais une valeur qui commence simplement par `$` ou `{`, comme dans `lang="$LANG"`, est lue telle qu'elle est écrite. `xml:lang` ou `data-lang` ne sont pas lus comme `lang`, et un `>` écrit dans une balise de template avant l'attribut, comme dans `{% if a > b %}`, ne le cache pas.

À éviter :

```html
<html lang="english">
```

À privilégier :

```html
<html lang="en">
```

#### H056

`Src should not be empty.`

La spécification html déclare un `src` vide invalide, et prévient qu'un navigateur le résout par rapport à l'url du document lui-même : `<img src="">` récupère donc à nouveau la page en tant qu'image, et `<script src=""></script>` la récupère en tant que script. Il s'agit généralement d'un emplacement qu'un script devait remplir, et la correction consiste à supprimer l'attribut, ou à conserver la valeur dans un attribut data, jusqu'à ce qu'il y ait une vraie valeur. Un `src` écrit sans aucune valeur, comme dans `<img src>`, est vide lui aussi et il est signalé.

Seuls `img`, `script`, `iframe`, `embed`, `source`, `track`, `audio` et `video` sont vérifiés, puisque ce sont les éléments qui récupèrent ce que `src` désigne. Seule une valeur qu'un navigateur lit comme vide est signalée : une valeur sans guillemets comme `<img src=/static/logo.png>` n'est donc pas touchée, pas plus qu'une valeur composée uniquement d'espaces ou qu'une valeur écrite par une balise de template, et `srcset` et `data-src` sont des attributs différents que la règle ne juge pas.

À éviter :

```html
<img src="" alt="Logo">
```

À privilégier :

```html
<img src="{% static 'logo.png' %}" alt="Logo">
```

#### H057

`Video should have a captions track.`

Dans une vidéo avec du son, la parole ne passe que par l'audio : une personne sourde ou malentendante n'en tire donc rien sans sous-titres, ce qu'exige le critère 1.2.2 Sous-titres (pré-enregistrés) des WCAG. Un `<track>` dont le `kind` vaut `captions` ou `subtitles` à l'intérieur de la `<video>` satisfait la règle, tout comme un `<track>` sans aucun `kind`, puisque `subtitles` est la valeur par défaut.

Une vidéo `muted` n'a pas d'audio à sous-titrer et n'est pas signalée. Une vidéo dont la balise ouvrante ou le corps contient une balise de template ne l'est pas non plus, puisque les pistes, ou l'attribut `muted`, peuvent être écrits par le template là où djLint ne peut pas les voir. Une balise de template s'entend d'une balise qu'ouvre un langage de templates, `{{`, `{%`, `{#` ou `${` : un gestionnaire jQuery comme `onclick="$(this).play()"`, un `$refs` Alpine, une accolade css et un prix écrit dans le texte de repli sont donc le texte ordinaire qu'ils semblent être, et la vidéo est tout de même lue.

`muted` doit être l'attribut : `<video class=muted>` est donc une classe nommée muted et il est signalé, et un `<track>` commenté ou écrit dans une valeur d'attribut est du texte plutôt qu'une piste. Un `</video>` dans une valeur ne termine rien, et l'élément est jugé là où sa vraie balise de fin le ferme : une `<video>` laissée ouverte est donc laissée à `H025`.

À éviter :

```html
<video controls src="talk.mp4"></video>
```

À privilégier :

```html
<video controls src="talk.mp4">
  <track kind="captions" src="talk.vtt" srclang="en">
</video>
```

<!-- oxfmt-ignore-end -->

### Ajouter des règles

Les pull requests proposant de nouvelles règles sont les bienvenues !

Une bonne règle se compose de

- Nom
- Code
- Message : message à afficher quand l'erreur est trouvée.
- Drapeaux : drapeaux d'expression régulière, par exemple re.I|re.M. Par défaut re.DOTALL.
- Motifs : expressions régulières qui trouvent l'erreur.
- Exclusions : liste facultative des profils auxquels la règle ne s'applique pas.

Merci d'inclure un test qui valide la règle.

## Règles personnalisées

Vous pouvez ajouter des règles personnalisées propres à votre projet en créant un fichier `.djlint_rules.yaml` à côté de votre `pyproject.toml`. Les règles ajoutées à ce fichier sont prises en compte par djLint. Un fichier de règles situé ailleurs peut être indiqué avec l'option CLI `--rules`.

### Règles à motifs

Vous pouvez ajouter des règles qui échouent si l'un des motifs d'expression régulière trouve une correspondance :

```yaml
- rule:
    name: T001
    message: Find Trichotillomania
    flags: re.DOTALL|re.I
    patterns:
      - Trichotillomania
```

### Règles en module Python

Vous pouvez ajouter des règles qui importent et exécutent une fonction Python personnalisée :

```yaml
- rule:
    name: T001
    message: Found the 'bad' word
    python_module: your_package.your_module
```

Le `python_module` indiqué doit contenir une fonction `run()` qui sera exécutée sur chaque fichier vérifié. Elle doit accepter les arguments suivants :

- `rule` : le dict qui représente votre règle dans `.djlint_rules.yaml`. Vous utiliserez généralement cette variable pour accéder au nom et au message de la règle.
- `config` : l'objet de configuration de DJLint.
- `html` : le contenu html complet du fichier.
- `filepath` : le chemin du fichier en cours de vérification.
- `line_ends` : la liste des positions de caractère `start` et `end` des lignes, que vous pouvez utiliser avec `djlint.lint.get_line()` pour obtenir des numéros de ligne à partir d'une position de caractère. Voir l'exemple.
- `*args, **kwargs` : nous pourrions ajouter d'autres arguments à l'avenir ; incluez donc ces deux arguments pour réduire le risque d'échec lors d'une mise à jour de djLint.

Le module peut se trouver à la racine du projet. S'il renvoie une `line` ou un `end` qui n'est pas une position, djLint s'arrête avec une erreur qui nomme la règle.

Elle doit renvoyer une liste de dicts, un par erreur, avec les clés suivantes :

- `code` : le nom de code de la règle qui signale l'erreur (généralement `rule['name']`)
- `line` : le numéro de ligne et le numéro de caractère sur cette ligne, séparés par un « : », sous forme de chaîne.
  Par exemple, `"2:3"` signifie que l'erreur a été trouvée à la ligne 2, au caractère 3
- `end` : facultatif. L'endroit où l'erreur se termine, écrit comme `line`, juste après son dernier caractère. Sans lui, l'erreur se termine là où se termine `match`.
- `match` : la partie du contenu qui contient l'erreur
- `message` : le message qui sera affiché pour signaler l'erreur (généralement `rule['message']`)

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
    """Règle qui échoue si le fichier html contient 'bad'.

    Ce n'est qu'un exemple : en réalité, c'est bien plus simple à faire avec
    une "règle à motifs".
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
