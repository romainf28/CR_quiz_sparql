# CR_quiz_sparql

## 1. Comment utiliser le repo?

Pour lancer notre quiz, il faut utiliser la commande <h1>python main.py</h1>. Cela lancera l'application tkinter pour 10 questions.

## 2. Comment on a construit le quiz?

### 2.1 Construction des requêtes
Les requêtes ont été créées dans le fichier queries.py. Nous avons structuré notre code avec différents types de questions. Chaque type de question est associé à une requête. Voici les différents type de question et informations disponibles: 

Infos disponibles : 
- Infos sur les départements (nom_dpt, code_insee_dpt, capitale, population, surface)
- Infos sur les communes (region, dpt, code_insee_dpt, commune_label, commune_population, code_commune)
- Infos sur les lieux connus
- Drapeaux des départements

Questions possibles : 
    
    Sur les départements : 
        - Quel est le code du département X ? 
        - Quel est le département correspondant au code X ? 
        - Quelle est la capitale du département X ?
        - Quelle est la population du département X ?
        (- Quel département à une population de X ?)
        - Quelle est la surface du département X ?
        (- Quel département à une surface de X ?)
            
    Sur les communes : 
        - A quelle région appartient la commune X ?
        - A quel département appartient la commune X ?
        - Quelle est la population de la commune X ?
        (-Quelle commune a une population de X ?)
        - Quel est le code commune de la commune X ?
        - Quelle commune correspond au code commune X ?
    
    Sur les drapeaux : 
        - A quel département ce drapeau appartient-il ?
        - Quel est le drapeau de ce département ?
        
    Sur les lieux connus : 
        - A quel département appartient ce lieu ?

### 2.2 Création de la base de données
Toutes les requêtes textuelles sont sauvegardées dans des csv après leur première execution. Les requêtes concernant des images les sauvegarde également dans le dossier assets après la première execution. Cela permet que l'interface soit plus rapide et que l'interface puisse être utilisée sans internet après la première execution.

### 2.3 Interface
Notre interface a été codé avec tkinter, elle se situe principalement dans interface.py. 10 questions sont choisies aléatoirement dans la base. On recuppère les réponses et codons une question à choix multiples. 

