---
description: Configuration de djLint pour le linting et le formatage des modèles HTML. Profitez des nombreuses options de formatage.
title: Configuration
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, configuration
---

# {{ "configuration" | i18n }}

La configuration se fait soit à travers le fichier `pyproject.toml` de votre projet, soit à travers un fichier `.djlintrc`. Les arguments de la ligne de commande remplaceront toujours les paramètres du fichier `pyproject.toml`.

Le format du fichier ``pyproject.toml`` est ``toml``.

```ini
[tool.djlint]
<options de configuration>
```
Le format du fichier ``djlintrc`` est ``json``.

```json
{
  "option" : "valeur"
}
```

## ignore

Ignore les codes de linter.

Utilisation :

**pyproject.toml**

```ini
ignore="H014,H015"
```

**.djlintrc**

```json
{
  "ignore" : "H014,H015"
}
```

## extension

Permet de trouver uniquement les fichiers ayant une extension spécifique.

Utilisation:

**pyproject.toml**

```ini
extension="html.dj"
```

**.djlintrc**

```json
{
  "extension": "html.dj"
}
```

## custom_blocks

Sert à indenter les blocs de code personnalisés. Par exemple {% raw %}`{% toc %}...{% endtoc %}`{% endraw %}

Utilisation:

**pyproject.toml**

```ini
custom_blocks="toc,example"
```

**.djlintrc**

```json
{
  "custom_blocks": "toc,example"
}
```

## custom_html

Permet d'indenter les balises HTML personnalisées. Par exemple, `<mjml>` ou `<simple-greeting>` ou `<mj-\w+>`.


Utilisation:

**pyproject.toml**

```ini
custom_html="mjml,simple-greeting,mj-\\w+"
```

**.djlintrc**

```json
{
  "custom_html": "mjml,simple-greeting,mj-\\w+"
}
```

## indent

Permet de modifier l'indentation du code. La valeur par défaut est 4 (quatre espaces).

Utilisation:

**pyproject.toml**

```ini
indent=3
```

**.djlintrc**

```json
{
  "indent": "3"
}
```

## exclude

Remplacer les chemins d'exclusion par défaut.

Utilisation:

**pyproject.toml**

```ini
exclude=".venv,venv,.tox,.eggs,..."
```

**.djlintrc**

```json
{
  "exclude": ".venv,venv,.tox,.eggs,..."
}
```

## extend_exclude

Ajouter des chemins supplémentaires à l'exclusion par défaut.

Utilisation:

**pyproject.toml**

```ini
extend_exclude=".custom"
```

**.djlintrc**

```json
{
  "extend_exclude": ".custom"
}
```

## blank_line_after_tag

Ajout d'une ligne vide supplémentaire après les groupes de balises {% raw %}`{% <tag> ... %}`{% endraw %}.

Utilisation:

**pyproject.toml**

```ini
blank_line_after_tag="load,extends,include"
```

**.djlintrc**

```json
{
  "blank_line_after_tag": "load,extends,include"
}
```
## profile

Définissez un profil pour la langue du modèle. Le profil activera les règles de linter qui s'appliquent à votre langage de modèle, et peut également changer le reformatage. Par exemple, dans `handlebars`, il n'y a pas d'espaces dans les balises {% raw %}`{{#if}}`{% endraw %}.

Options:

:::content

- html (par défaut)
- django
- jinja
- nunjucks (pour nunjucks et twig)
- handlebars (pour handlebars et mustache)
- golang
- angulaire
  :::

Utilisation:

**pyproject.toml**

```ini
profile="django"
```

**.djlintrc**

```json
{
  "profile": "django"
}
```

## require_pragma

Ne formatez ou ne limez que les fichiers qui commencent par un commentaire contenant uniquement le texte 'djlint:on'. Le commentaire peut être un commentaire HTML ou un commentaire dans le langage de modèle défini par le paramètre de profil. Si aucun profil n'est spécifié, un commentaire dans l'un des langages de modèle est accepté.

Utilisation:

**pyproject.toml**

```ini
require_pragma=true
```

**.djlintrc**

```json
{
  "require_pragma": "true"
}
```

{% raw %}

```html
<!-- djlint:on -->
ou {# djlint:on #} ou {% comment %} djlint:on {% endcomment %} ou {{ /*
djlint:on */ }} ou {{!-- djlint:on --}}
```

{% endraw %}

## max_line_length

Le formateur essaiera de mettre certaines balises html et template sur une seule ligne au lieu de les envelopper si la longueur de la ligne ne dépasse pas cette valeur.

Utilisation:

**pyproject.toml**

```ini
max_line_length=120
```

**.djlintrc**

```json
{
  "max_line_length": "120"
}
```

## max_attribute_length

Le formateur tentera d'envelopper les attributs de la balise si la longueur de l'attribut dépasse cette valeur.

Utilisation:

**pyproject.toml**

```ini
max_attribute_length=10
```

**.djlintrc**

```json
{
  "max_attribute_length": "10"
}
```

## use_gitignore

Ajouter les exclusions .gitignore à l'exclusion par défaut.

Utilisation:

**pyproject.toml**

```ini
use_gitignore=True
```

**.djlintrc**

```json
{
  "use_gitignore": "True"
}
```

## format_attribute_template_tags

Le formateur tentera de formater la syntaxe des modèles à l'intérieur des attributs des balises. Désactivé par défaut.

Utilisation:

**pyproject.toml**

```ini
format_attribute_template_tags=true
```

**.djlintrc**

```json
{
  "format_attribute_template_tags": "true"
}
```

Par exemple, avec cette option activée, le html suivant sera acceptable :

```html
{% raw %}
<input class="{% if this %}
                  then something neat
              {% else %}
                  that is long stuff asdf and more even
              {% endif %}"
/>
{% endraw %}
```

## linter_output_format

Personnalise l'ordre du message de sortie. Défaut="{code} {ligne} {message} {match}". Si `{filename}` n'est pas inclus dans le message, alors la sortie sera groupée par fichier et un en-tête sera automatiquement ajouté à chaque groupe.

Variables facultatives :
::: content
- `{filename}`
- `{line}`
- `{code}`
- `{message}`
- `{match}`
:::

Utilisation:

**pyproject.toml**

```ini
linter_output_format="{filename}:{line}: {code} {message} {match}"
```

**.djlintrc**

```json
{
  "linter_output_format": "{filename}:{line}: {code} {message} {match}"
}
```

## preserve_leading_space

Préserve l'espace de tête du texte, dans la mesure du possible. Idéal pour les fichiers de modèles non-html où l'indentation du texte est intentionnelle.

Utilisation:

**flag**

```bash
--preserve-leading-space
```

**pyproject.toml**

```ini
preserve_leading_space=true
```

**.djlintrc**

```json
{
  "preserve_leading_space": true
}
```
