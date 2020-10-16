# CSV Validator

## Execution

Dans l'invite de commande naviguer vers le répertoire qui contient le script

```shell
py csv_validator.py <fichier_csv> [<fichier_config>]
```

**fichier_csv**: chemin vers le fichier csv à parser
**fichier_config**: chemin vers le fichier JSON de configuration _(optionnel, valeur par défaut : ./config.json)_

## Fichier de configuration

Il décrit les vérifications à faire sur le fichier CSV.
Il doit être au format JSON. et contenir les objets suivants

```json
{
  // Vérifications concernant le nom du fichier
  "filename": {
    "rules": [
      {
        "name": "", // nom de la régle (affiché dans le fichier de sortie)
        "description": "", // description pour comprendre l'expression régulière
        "regex": ".*" // expression régulière de vérification
      },
      {...}
    ]
  },
  // Vérifications concernant le contenu du fichier
  // 1 objet par colonne, l'ordre est vérifié
  "cols": [
    {
      "title": "", // nom de la colonne
      "rules": [
        {
          "name": "", // nom de la régle (affiché dans le fichier de sortie)
          // description pour comprendre l'expression régulière
        "regex": ".*" // expression régulière de vérification
        }
      ]
    },
    {...}
  ]
}
```

## Vérifications automatiques

En plus des régles définies dans le fichier de configuration le script détecte les erreurs suivantes :

- Ligne vide (toutes les cellules d'une ligne sont vide)
- Colonne supplémentaire ou manquante

## fichier de sortie

Le résultat de l'analyse est écrit dans un fichier `output.json` qui est créé dans le répertoire courant

**Si aucune erreur n'est détectée** le message ` "TOUT EST OK - GO POUR DIFFUSION :D` est écrit dans le fichier

**Si des erreurs sont détectées**, le fichier est composé d'un dictionnaire dont la clef est soit

- "filename" pour les erreurs sur le nom de fichier
- le numéro de la colonne (commence à 1) pour les erreurs de contenu

```json
{
  "filename": {
    "Prefix": 1, // La règle dont le nom est "Prefix" a été 1 fois en erreur
  },
  // Première colonne
  "1": {
    "Header": "expected: 'Type', actual: 'Toto'", // Le nom de la colonne n'est pas le bon
    "Only Numbers": 3 // La règle dont le nom est "Only Numbers" a été 3 fois en erreur
  },
  // 5ème colonne
  "5": {...}
}
```

Si une colonne (ou une catégorie) n'est pas mentionnée, cela veut dire qu'aucune erreur n'a été détecté pour cette colonne
