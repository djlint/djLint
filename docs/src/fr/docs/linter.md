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
    <span class="icon is-large"><i class="fas fa-2x fa-arrow-circle-right"></i></span><div class="my-auto ml-3 is-inline-block"><a href="/fr/docs/configuration/">Consultez le guide de configuration pour connaître toutes les options !</a></div>
</div>


## Règles personnalisées

Créez un fichier `.djlint_rules.yaml` à côté de votre `pyproject.toml`. Des règles peuvent être ajoutées à ce fichier et djLint les reprendra.

Une bonne règle suit ce modèle :

```yaml
- règle :
    name : T001
    message : Trouver la Trichotillomanie
    indicateurs : re.DOTALL|re.I
    modèles :
      - Trichotillomanie
```

## Rules

| Code | Signification                                                                                                             |
| ---- | ------------------------------------------------------------------------------------------------------------------------- |
| T001 | Les variables doivent être entourées d'un seul espace. Ex : {% raw %}`{{ this }}`{% endraw %}                             |
| T002 | Les doubles quotes doivent être utilisées dans les balises. Ex : {% raw %}`{% extends "this.html" %}`{% endraw %}         |
| T003 | Le bloc de fin doit avoir un nom. Ex : {% raw %}`{% endblock body %}`{% endraw %}.                                        |
| D004 | (Django) Les urls statiques doivent suivre le modèle {% raw %}`{% static path/to/file %}`{% endraw %}.                    |
| J004 | (Jinja) Les urls statiques doivent suivre le modèle {% raw %}`{ url_for('static'..) }}`{% endraw %}.                      |
| H005 | La balise Html doit avoir l'attribut `lang`.                                                                              |
| H006 | La balise `img` doit avoir les attributs `height` et `width`.                                                             |
| H007 | LA BALISE `<!DOCTYPE ... >` doit être présent avant la balise html.                                                       |
| H008 | Les attributs doivent être entre guillemets.                                                                              |
| H009 | Les noms de balises doivent être en minuscules.                                                                           |
| H010 | Les noms d'attributs doivent être en minuscules.                                                                          |
| H011 | Les valeurs des attributs doivent être citées.                                                                            |
| H012 | Il ne doit pas y avoir d'espace autour de l'attribut `=`.                                                                 |
| H013 | La balise `img` doit avoir des attributs alt.                                                                             |
| H014 | Plus de 2 lignes vides.                                                                                                   |
| H015 | Les balises "h" doivent être suivies d'un retour à la ligne.                                                              |
| H016 | Balise `title` manquante dans le html.                                                                                    |
| H017 | La balise doit se fermer automatiquement.                                                                                 |
| D018 | (Django) Les liens internes doivent utiliser le modèle {% raw %}`{% url ... %}`{% endraw %}.                              |
| J018 | (Jinja) Les liens internes doivent utiliser le modèle {% raw %}`{% url ... %}`{% endraw %}.                               |
| H019 | Remplacez `javascript:abc()` par l'événement `on_` et l'url réelle.                                                       |
| H020 | Couple de balises vide trouvé. Envisagez de le supprimer.                                                                 |
| H021 | Les styles en ligne doivent être évités.                                                                                  |
| H022 | Utilisez HTTPS pour les liens externes.                                                                                   |
| H023 | N'utilisez pas de références d'entités.                                                                                   |
| H024 | Omettre le type sur les scripts et les styles.                                                                            |
| H025 | La balise semble être orpheline.                                                                                          |
| H026 | Les balises Emtpy id et class peuvent être supprimées.                                                                    |
| T027 | Chaîne non fermée trouvée dans la syntaxe du modèle.                                                                      |
| T028 | Envisagez d'utiliser des balises sans espace à l'intérieur des valeurs d'attributs. {% raw %}`{%- if/for -%}`{% endraw %} |
| H029 | Pensez à utiliser des valeurs de méthode de formulaire en minuscules.                                                     |
| H030 | Pensez à ajouter une méta-description.                                                                                    |
| H031 | Pensez à ajouter des méta keywords.                                                                                       |
| T032 | Espace blanc supplémentaire trouvé dans les balises du modèle.                                                            |
| H033 | Espace supplémentaire dans l'action du formulaire.                                                                        |


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

### Modèles de code

La première lettre d'un code suit le modèle :

::: content

- T : s'applique généralement aux modèles
- H : s'applique au html
- D : s'applique spécifiquement à Django
- J : s'applique spécifiquement à Jinja
- N : s'applique spécifiquement à Nunjucks
- M : s'applique spécifiquement à Handlebars
  :::
