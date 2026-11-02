---
description: Journal des modifications de djLint. Retrouvez les nouveautés des dernières versions et les fonctionnalités à attendre lors de votre prochaine mise à jour.
title: Journal des modifications
keywords: linter de templates, formateur de templates, djLint, HTML, templates, formateur, linter, journal des modifications
---

{% raw %}

# Journal des modifications

Le journal des modifications figure désormais dans les [releases](https://github.com/djlint/djLint/releases).

## 1.0.2

::: content

- Corrections de bugs [#240](https://github.com/djlint/djLint/issues/240)
  :::

## 1.0.1

::: content

- Corrections de bugs [#236](https://github.com/djlint/djLint/issues/236)
  :::

## 1.0.0

::: content

- Corrections de bugs [#224](https://github.com/djlint/djLint/issues/224)
  :::

## 0.7.6

::: content

- Corrections de bugs [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/189)
- Ajout de l'option `--warn` pour renvoyer les erreurs sous forme d'avertissements.
  :::

## 0.7.5

::: content

- Corrections de bugs [#187](https://github.com/djlint/djLint/issues/187)
- Meilleure prise en charge du front matter `yaml` dans les fichiers de templates
- Ajout de la règle T032 pour [#123](https://github.com/djlint/djLint/issues/123)
- Ajout de la règle H033 pour [#124](https://github.com/djlint/djLint/issues/124)
- Les profils du linter deviennent inclusifs plutôt qu'exclusifs pour [#178](https://github.com/djlint/djLint/issues/178)
- Ajout de `.djlintrc` comme fichier de configuration alternatif pour [#188](https://github.com/djlint/djLint/issues/188)
  :::

## 0.7.4

::: content

- Corrections de bugs [#177](https://github.com/djlint/djLint/issues/177)
  :::

## 0.7.3

::: content

- Corrections de bugs [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- Retrait de Py3.6 de `pyproject.toml`.
  :::

## 0.7.2

::: content

- Corrections de bugs [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
  :::

## 0.7.1

::: content

- Corrections de bugs [#166](https://github.com/djlint/djLint/issues/166)
  :::

## 0.7.0

::: content

- Ajout d'une configuration pour les balises HTML personnalisées
- Corrections de bugs
  :::

## 0.6.9

::: content

- Ajout des profils HTML et Angular
- Certaines entités sont autorisées dans la règle #H023
- Corrections de bugs
  :::

## 0.6.8

::: content

- Corrections de bugs
- Mise à jour de la documentation
  :::

## 0.6.7

::: content

- Ajout de l'option de configuration `format_attribute_template_tags` pour activer, au choix, le formatage des balises de template à l'intérieur des attributs
- Ajout de l'option de configuration `linter_output_format` pour personnaliser l'ordre des variables du message du linter
- Ajout des règles H030 et H031 pour vérifier les balises meta
  :::

## 0.6.6

::: content

- Corrections de bugs
  :::

## 0.6.5

::: content

- Les chemins affichés en sortie sont désormais relatifs à la racine du projet
- Corrections de bugs
  :::

## 0.6.4

::: content

- Corrections de bugs
  :::

## 0.6.3

::: content

- Prise en charge de la balise django `blocktrans`
- Corrections de bugs
  :::

## 0.6.2

::: content

- Corrections de bugs
  :::

## 0.6.1

::: content

- Corrections de bugs
- La règle T028 devient plus stricte, avec un message plus clair
  :::

## 0.6.0

::: content

- Ajout de la règle T027 pour repérer les chaînes non fermées dans la syntaxe de template
- Ajout de la règle T028 pour repérer les balises sans espaces manquantes dans les attributs
- Ajout de la règle H029 pour vérifier que la méthode des formulaires est en minuscules
- Le formateur ignore les balises django blocktranslate qui n'ont pas « trimmed »
- Corrections de bugs
  :::

## 0.5.9a

::: content

- Ajout de la prise en charge de python 3.10 dans les tests
- Ajout d'un hook pre-commit
  :::

## 0.5.9

::: content

- Ajout de l'option `--use-gitignore` pour étendre les exclusions
- Modification de la correspondance des exclusions par défaut
- Correction des chemins d'exclusion sous Windows
- Correction du formatage des balises `{%...%}` dans les attributs
- Correction du formatage des boucles for et des conditions imbriquées dans les attributs
  :::

## 0.5.8

::: content

- Ajout de l'option require_pragma
- DJ018 détecte désormais `data-src` et `action` sur les inputs
- Correction de la syntaxe d'ignorance en ligne
- Ajout de l'option `--lint`, qui correspond à l'utilisation par défaut
- Corrections de bugs
  :::

## 0.5.7

::: content

- Corrections de bugs
  :::

## 0.5.6

::: content

- Ajout de la règle H026 pour repérer les attributs id et class vides
- Corrections de bugs
  :::

## 0.5.5

::: content

- Regroupement des réglages et allègement du code
- Corrections de bugs
  :::

## 0.5.4

::: content

- Ajout de la règle H020 pour repérer les paires de balises vides
- Ajout de la règle H021 pour repérer les styles en ligne
- Ajout de la règle H022 pour repérer les liens http
- Ajout de la règle H023 pour repérer les références d'entités
- Ajout de la règle H024 pour repérer l'attribut type sur les scripts et les styles
- Ajout de la règle H025 pour vérifier les balises orphelines. Merci à https://stackoverflow.com/a/1736801/10265880
- Amélioration du formatage des attributs
- L'option `blank_line_after_tag` ajoute désormais un saut de ligne quel que soit l'emplacement
- Correction du formatage de la balise django `trans`
- Ajout du formatage des styles en ligne
- Ajout du formatage des conditions de template à l'intérieur des attributs
- srcset est désormais un emplacement d'URL possible dans les règles du linter
- Formatage plus rapide
- Remerciements particuliers à [jayvdb](https://github.com/jayvdb)
  :::

## 0.5.3

::: content

- Avec les options `--reformat/check`, stdout n'affiche plus que le nouveau html quand l'entrée est stdin
  :::

## 0.5.2

::: content

- L'exigence d'`alt` passe de H006 à H013
- Ajout d'un fichier facultatif de règles personnalisées
- Ajout de `golang` comme option de profil
- Correction du formatage des blocs ignorés contenant des commentaires en ligne
- Ajout d'un texte par défaut pour les options `--indent` et `-e`
- Les règles sur les URL acceptent désormais #
- Correction de l'encodage des fichiers sous Windows
- Correction de l'expression régulière des balises de template sur une seule ligne
- Correction de `blank_line_after_tag` pour les balises précédées d'espaces
  :::

## 0.5.1

::: content

- Ajout de la règle H019
- Correction de bugs dans DJ018 et H012
  :::

## 0.5.0

::: content

- Correction de plusieurs bugs de correspondance d'expressions régulières dans les règles du linter
- Le linter ne renvoie plus d'erreurs dans les blocs ignorés
- Ajout d'une option pour exclure un bloc de code du linter et du formateur avec les balises `{% djlint:off %}...{% djlint:on %}`
  :::

## 0.4.9

::: content

- Correction du bug [#35](https://github.com/djlint/djLint/issues/35)
  :::

## 0.4.8

::: content

- Correction du bug [#34](https://github.com/djlint/djLint/issues/34)
  :::

## 0.4.7

::: content

- La balise `source` rejoint les balises sur une seule ligne
  :::

## 0.4.6

::: content

- Correction du bug [#31](https://github.com/djlint/djLint/issues/31)
  :::

## 0.4.5

::: content

- Ajout des bonnes pratiques à la documentation
- Ajout de l'option `--profile` pour définir les règles par défaut du linter et du formateur
- Ajout de règles du linter pour les motifs d'URL jinja
  :::

## 0.4.4

::: content

- La configuration de l'indentation passe d'une chaîne à un entier. `--indent 3`
  :::

## 0.4.3

::: content

- Ajout d'une option en ligne de commande pour l'espacement de l'indentation. `--indent=" "`
  :::

## 0.4.2

::: content

- Prise en charge d'espaces supplémentaires après les balises avec l'option `blank_line_after_tag`
  :::

## 0.4.1

::: content

- Prise en charge du traitement de plusieurs fichiers ou dossiers à la fois
  :::

## 0.4.0

::: content

- Correction du formatage des balises django `{# ... #}`
- Ajout de la prise en charge de l'indentation pour les balises figcaption, details et summary
- Possibilité de remplacer ou d'étendre la liste des chemins exclus dans `pyproject.toml`
  :::

## 0.3.9

::: content

- Mise à jour de la gestion des attributs
  :::

## 0.3.8

::: content

- Prise en charge de stdin
  :::

## 0.3.7

::: content

- Correction du formatage des balises `small`, `dt` et `dd`
  :::

## 0.3.6

::: content

- Prise en charge, dans le formateur, des blocs ouvrants Nunjucks `{%-`
  :::

## 0.3.5

::: content

- Prise en charge de davantage de blocs Django
- Prise en charge des blocs personnalisés
- Prise en charge de la configuration dans `pyproject.toml`
  :::

## 0.3.4

::: content

- Correction du format de la balise sans espaces Nunjucks `-%}`
  :::

## 0.3.3

::: content

- Les balises `div` courtes peuvent tenir sur une seule ligne
  :::

## 0.3.2

::: content

- Correction du formatage des commentaires Django
- Les textarea sont exclus du formatage
  :::

## 0.3.1

::: content

- Mise à jour de l'expression régulière de formatage des attributs
- Mise à jour de la règle de lint W010
  :::

## 0.3.0

::: content

- Le code de sortie passe à 1 en cas de modification de formatage
- Prise en charge des balises Jinja `asset`
  :::

## 0.2.9

::: content

- Mise à jour de l'expression régulière de W018
- Suppression des messages de lint en double
- Mise à jour de E001 pour Handlebars
  :::

## 0.2.8

::: content

- Correction d'une erreur de barre de progression avec les anciennes versions de Click
  :::

{% endraw %}
