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
    <span class="icon is-large"><i class="fas fa-2x fa-circle-arrow-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/fr/docs/configuration/">Consultez le guide de configuration pour connaître toutes les options !</a></div>
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
| H006 | La balise `img` doit avoir les attributs `height` et `width`.                                                             | ✔️     |
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
| H017 | Les étiquettes vides doivent se refermer automatiquement.                                                                 | -      |
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
| H031 | Pensez à ajouter des méta keywords.                                                                                       | ✔️     |
| H033 | Espace supplémentaire dans l'action du formulaire.                                                                        | ✔️     |
| J004 | (Jinja) Les urls statiques doivent suivre le modèle {% raw %}`{ url_for('static'..) }}`{% endraw %}.                      | ✔️     |
| J018 | (Jinja) Les liens internes doivent utiliser le modèle {% raw %}`{% url ... %}`{% endraw %}.                               | ✔️     |
| T001 | Les variables doivent être entourées d'un espace. Ex : {% raw %}`{{ this }}`{% endraw %}                                  | ✔️     |
| T002 | Les doubles quotes doivent être utilisées dans les balises. Ex : {% raw %}`{% extends "this.html" %}`{% endraw %}         | ✔️     |
| T003 | Le bloc de fin doit avoir un nom. Ex : {% raw %}`{% endblock body %}`{% endraw %}.                                        | ✔️     |
| T027 | Chaîne non fermée trouvée dans la syntaxe du modèle.                                                                      | ✔️     |
| T028 | Envisagez d'utiliser des balises sans espace à l'intérieur des valeurs d'attributs. {% raw %}`{%- if/for -%}`{% endraw %} | ✔️     |
| T032 | Espace blanc supplémentaire trouvé dans les balises du modèle.                                                            | ✔️     |
| T034 | Aviez-vous l'intention d'utiliser {% raw %}{% ... %} au lieu de {% ... }% ? {% endraw %}                                  | ✔️     |
| H035 | Meta doivent se fermer d'elles-mêmes.                                                                                     | -      |
| H036 | Évitez d'utiliser les balises <br>.                                                                                       | -      |
| H037 | Attribut en double trouvé.                                                                                                | ✔️     |

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
    config: djlint.settings.Config,
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
        errors.append(
            {
                "code": rule["name"],
                "line": get_line(match.start(), line_ends),
                "match": match.group().strip()[:20],
                "message": rule["message"],
            }
        )
    return errors
```
