---
description: Changelog de djLint. Trouvez les mises à jour des versions récentes et les fonctionnalités que vous pouvez attendre lors de votre prochaine mise à jour.
title: Changelog
keywords: template linter, template formatter, djLint, HTML, templates, formatter, linter, changelog
---

{% raw %}

# Changelog

Changelog est maintenant inclus dans la [release](https://github.com/djlint/djLint/releases).

<!--## {{ "next_release" i18n }}-->

## 1.0.2

::: content

- Correction de bugs [#240](https://github.com/djlint/djLint/issues/240)
  :::

## 1.0.1

::: content

- Correction de bugs [#236](https://github.com/djlint/djLint/issues/236)
  :::

## 1.0.0

::: content

- Correction de bugs [#224](https://github.com/djlint/djLint/issues/224)
  :::

## 0.7.6

::: content

- Correction de bugs [#189](https://github.com/djlint/djLint/issues/189), [#197](https://github.com/djlint/djLint/issues/189)
- Ajouté le drapeau `--warn` pour retourner les erreurs de retour comme des avertissements.
  :::

## 0.7.5

::: content

- Correction de bugs [#187](https://github.com/djlint/djLint/issues/187)
- Ajout d'une meilleure prise en charge de la matière première `yaml` dans les fichiers modèles
- Ajouté la règle T032 pour [#123](https://github.com/djlint/djLint/issues/123)
- Ajouté la règle H033 pour [#124](https://github.com/djlint/djLint/issues/124)
- Modification des profils des liners pour qu'ils soient inclusifs et non exclusifs pour [#178](https://github.com/djlint/djLint/issues/178)
- Ajout d'une option alternative pour le fichier de configuration `.djlintrc`. pour [#188](https://github.com/djlint/djLint/issues/188)
  :::

## 0.7.4

::: content

- Correction de bugs [#177](https://github.com/djlint/djLint/issues/177)
  :::

## 0.7.3

::: content

- Correction de bugs [#173](https://github.com/djlint/djLint/issues/173), [#174](https://github.com/djlint/djLint/issues/174)
- Suppression de Py3.6 de `pyproject.toml`..
  :::

## 0.7.2

::: content

- Correction de bugs [#167](https://github.com/djlint/djLint/issues/167), [#166](https://github.com/djlint/djLint/issues/166), [#171](https://github.com/djlint/djLint/issues/171), [#169](https://github.com/djlint/djLint/issues/169)
  :::

## 0.7.1

::: content

- Correction de bugs [#166](https://github.com/djlint/djLint/issues/166)
  :::

## 0.7.0

::: content

- Ajout d'une configuration pour les balises HTML personnalisées
- Correction de bugs
  :::

## 0.6.9

::: content

- Ajout des profils HTML et Angular
- Autorisé certaines entités dans la règle #H023
- Correction de bugs
  :::

## 0.6.8

::: content

- Correction de bugs
- Documents mis à jour
  :::

## 0.6.7

::: content

- Ajouté l'option de configuration `format_attribute_template_tags` comme option pour le formatage des balises de modèle dans les attributs.
- Ajouté l'option de configuration `linter_output_format` pour personnaliser l'ordre des variables des messages linter.
- Ajout des règles H030 et H031 pour vérifier les balises méta.
  :::

## 0.6.6

::: content

- Correction de bugs
  :::

## 0.6.5

::: content

- Mise à jour des chemins de sortie pour être relatifs à la racine du projet
- Correction de bugs
  :::

## 0.6.4

::: content

- Correction de bugs
  :::

## 0.6.3

::: content

- Ajout du support pour la balise `blocktrans` de django
- Correction de bugs
  :::

## 0.6.2

::: content

- Correction de bugs
  :::

## 0.6.1

::: content

- Correction de bugs
- Rendre la règle T028 plus stricte avec un message plus clair
  :::

## 0.6.0

::: content

- La règle T027 a été ajoutée pour vérifier la présence de balises non fermées dans la syntaxe des modèles.
- Ajout de la règle T028 pour vérifier l'absence de balises sans espace dans les attributs.
- Ajout de la règle H029 pour vérifier la présence de minuscules dans la méthode du formulaire
- Ignorer les balises djagno blocktranslate qui n'ont pas "trimmed" du formateur
- Correction de bugs
  :::

## 0.5.9a

::: content

- Ajout du support des tests pour python 3.10
- Ajout d'un hook pre-commit
  :::

## 0.5.9

::: content

- Ajout de l'option `--use-gitignore` pour étendre les exclusions
- Modification de la correspondance des exclusions par défaut
- Correction des chemins d'exclusion des fenêtres
- Correction du formatage des balises `{%...%}` dans les attributs
- Correction du formatage des boucles for et des conditions imbriquées dans les attributs
  :::

## 0.5.8

::: content

- Ajout de l'option require_pragma
- Mise à jour de DJ018 pour attraper `data-src` et `action` sur les entrées
- Correction de la syntaxe inline ignore
- Ajout de l'option `--lint` comme substitut à l'utilisation par défaut.
- Correction de bugs
  :::

## 0.5.7

::: content

- Correction de bugs
  :::

## 0.5.6

::: content

- Ajout de la règle H026 pour trouver les balises id et class vides
- Correction de bugs
  :::

## 0.5.5

::: content

- Paramètres consolidés et code allégé
- Correction de bugs
  :::

## 0.5.4

::: content

- Ajout de la règle H020 pour trouver les paires de balises vides
- Ajout de la règle H021 pour trouver les styles en ligne
- Ajouté la règle H022 pour trouver les liens http
- Ajouté la règle H023 pour trouver les références d'entités
- Ajouté la règle H024 pour trouver les types de scripts et de styles.
- Ajout de la règle H025 pour vérifier les balises orphelines. Merci à https://stackoverflow.com/a/1736801/10265880
- Amélioration du formatage des attributs
- Mise à jour de l'option `blank_line_after_tag` pour ajouter une nouvelle ligne indépendamment de l'emplacement.
- Correction du formatage des balises `trans` de django
- Ajout du formatage pour les styles en ligne
- Ajout du formatage des conditions de modèle dans les attributs
- Ajout de srcset comme emplacement d'url possible dans les règles de linter
- Accélération du formatage
- Remerciements spéciaux à [jayvdb](https://github.com/jayvdb)
  :::

## 0.5.3

::: content

- Modifier stdout pour les options `--reformat/check` afin de n'imprimer le nouveau html que lorsque stdin est utilisé comme entrée
  :::

## 0.5.2

::: content

- Diviser l'exigence `alt` de H006 à H013
- Ajout d'un fichier de règles personnalisées facultatif
- Ajout de `golang` comme option de profil
- Correction du formatage des blocs ignorés contenant des commentaires en ligne
- Ajout d'un texte par défaut aux options `--indent` et `-e`.
- Mise à jour des règles url pour accepter le #
- Correction de l'encodage des fichiers sous Windows OS
- Correction du regex de la balise de modèle à ligne unique
- Correction de l'option `blank_line_after_tag` pour les balises avec espace avant
  :::

## 0.5.1

::: content

- Ajout de la règle H019
- Correction de bugs dans DJ018 et H012
  :::

## 0.5.0

::: content

- Correction de plusieurs bogues de correspondance regex dans les règles de linter
- Empêche linter de retourner des erreurs dans les blocs ignorés
- Ajout d'une option pour ignorer les blocs de code de linter/formatter avec les balises `{% djlint:off %}...{% djlint:on %}`.
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

- Déplacement de la balise `source` vers les balises à ligne unique
  :::

## 0.4.6

::: content

- Correction du bug [#31](https://github.com/djlint/djLint/issues/31)
  :::

## 0.4.5

::: content

- Ajout des meilleures pratiques à la documentation
- Ajout de l'option `--profile` pour définir les règles de linter/formater par défaut
- Ajout de règles de linter pour les modèles d'url jinja
  :::

## 0.4.4

::: content

- Changez la configuration de l'indentation d'une chaîne de caractères à un nombre entier. `--indent 3`
  :::

## 0.4.3

::: content

- Ajout d'une option cli pour l'espacement des indentations. `--indent=" "`
  :::

## 0.4.2

::: content

- Ajout de la prise en charge d'espaces supplémentaires après les balises avec l'option `blank_line_after_tag`.
  :::

## 0.4.1

::: content

- Ajout d'un support pour le traitement de plusieurs fichiers ou dossiers à la fois
  :::

## 0.4.0

::: content

- Correction du formatage des balises `{# .... #}` de django
- Ajout de la prise en charge de l'indentation pour les balises figcaption, details et summary
- Ajout d'une prise en charge pour remplacer ou étendre la liste des chemins exclus dans `pyproject.toml`.
  :::

## 0.3.9

::: content

- Mise à jour de la gestion des attributs
  :::

## 0.3.8

::: content

- Ajout de la prise en charge de stdin
  :::

## 0.3.7

::: content

- Correction du formatage des balises `small`, `dt` et `dd`.
  :::

## 0.3.6

::: content

- Ajout de la prise en charge du formateur pour les blocs d'ouverture `{%-` de Nunjucks
  :::

## 0.3.5

::: content

- Ajout de la prise en charge d'un plus grand nombre de blocs Django
- Ajout de la prise en charge des blocs personnalisés
- Ajout de la prise en charge de la configuration dans `pyproject.toml`.
  :::

## 0.3.4

::: content

- Correction du format de la balise sans espace `-%}` de Nunjucks
  :::

## 0.3.3

::: content

- Permettre aux balises `div` courtes d'être sur une seule ligne
  :::

## 0.3.2

::: content

- Correction du formatage des commentaires Django
- Ignorer la mise en forme des zones de texte
  :::

## 0.3.1

::: content

- Mise à jour de la regex pour le formatage des attributs
- Mise à jour de la règle de lint W010
  :::

## 0.3.0

::: content

- Changement du code de sortie à 1 s'il y a eu des changements de formatage
- Ajout de la prise en charge des balises `asset` de Jinja
  :::

## 0.2.9

::: content

- Mise à jour de la regex W018
- Suppression des messages lint dupliqués
- Mise à jour de E001 pour Handlebars
  :::

## 0.2.8

::: content

- Correction de l'erreur de la barre de progression pour l'ancienne version de Click
  :::

{% endraw %}
