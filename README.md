# CR_quiz_sparql

## 1. Comment utiliser le repo?

Pour lancer notre quiz, il faut utiliser la commande ```python main.py```. Cela lance une application tkinter. Il faut alors choisir entre deux modes : le mode standard, dasn lequel un nombre fixe de questions est posé à l'utilisateur, et le mode survie, dans lequel l'utilisateur peut répondre à des questions jusqu'à ce qu'il n'ait plus de vies. Pour le quiz standard, le nombre de questions posées dans le quiz ainsi que le type de questions posées sont paramétrables via les arguments ```nb_questions``` et ```question_types``` de la classe ```StandardQuiz``` (définie dans interface.py). Pour le quiz en mode survie, on peut paramétrer le nombre de vies via le paramètre ```nb_lives``` de la classe ```SurvivalQuiz```. Les types de questions autorisés que l'on peut passer dans la liste ```question_types``` sont définis dans le dictionnaire ```AVAILABLE_QUESTION_TYPES```, dans le fichier ```queries.py```.

## 2. Comment a-t-on construit le quiz?

### 2.1 Construction des requêtes
Les requêtes ont été écrites dans le fichier ```queries.py```. Il s'agit de requêtes SPARQL faites à wikidata via un handler défini dans le fichier ```query_handler.py```. Nous avons structuré notre code avec différents types de questions. Chaque type de question est associé à une requête. Voici les différents type de question et informations disponibles: 

Infos disponibles : 

    - Infos sur les départements (nom_dpt, code_insee_dpt, capitale, population, surface)
    - Infos sur les communes (region, dpt, code_insee_dpt, commune_label, commune_population, code_commune)
    - Infos sur les lieux connus ('attraction touristiques' dans wikidata)
    - Drapeaux des départements (et oui, ça existe !)

Questions possibles : 
    
    Sur les départements : 
        - Quel est le code du département X ? 
        - Quel est le département correspondant au code X ? 
        - Quelle est la capitale du département X ?
        - Quelle est la population du département X ?
        (- Quel département a une population de X ?)
        - Quelle est la surface du département X ?
        (- Quel département a une surface de X ?)
            
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
Toutes les requêtes textuelles sont sauvegardées dans des csv, dans le dossier ```./dataframes``` après leur première execution. Pour les requêtes concernant des images, les url des images sont stockés dans le dataframe. Les fichiers ```save_flags.py``` et ```save_places.py``` permettent alors de peupler le dossier ```./assets``` en fetchant les images via leurs urls et en les sauvegardant au format png. Cela permet à la fois de réduire la latence entre les questions une fois le quiz lancé (après la première exécution) et de permettre un lancement du quiz hors-ligne, sans accès à Internet.

Notons que contrairement aux autres départements, le département 75 n'appartient pas à la classe Q6465 des départements français dans wikidata. De plus, Paris n'est plus considérée comme une commune française depuis 2018. Nous avons donc dû adapter les requêtes en faisant des UNION de façon à ne pas manquer les informations relatives au département 75 dans notre quiz !


### 2.3 Interface
Notre interface a été codée avec tkinter. Elle se situe principalement dans ```interface.py```. Le quiz prend la forme d'une questionnaire à choix multiples, avec réponse unique et 4 options par question. Par défaut, 10 questions sont choisies aléatoirement parmi l'ensemble des types de questions possibles. En pratique, une fois le type de question choisi aléatoirement, on va chercher dans le dossier ```./dataframes``` (et éventuellement ```./assets```) la réponse à la question, ainsi que 3 autres entrées choisies aléatoirement qui feront office d'options. A chaque fois que l'utilisateur valide une réponse, une fenêtre de dialogue lui indique si la réponse qu'il a sélectionné était correcte ou non (auquel cas la bonne réponse lui est donnée). Une fois le quiz terminé, on affiche à l'utilisateur son score total.
