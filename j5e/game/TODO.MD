# NOTICE
Pour lancer : 
le jeu :
python3 -m j5e.game
le controleur :
python3 -m j5e.game.panelAdmin
le serveur web :
python3 -m http.server 8080

Commandes réseau d'interaction avec le jeu : j5e/game/PROTOCOL.md

Pour quitter proprement, play après le Game Over

Pour gagner un niveau, il faut que le nombre de lemmings requis total soit atteint

# INPROGRESS



# TODO

- appel du redessin à partir des actions de jeu  ("coups", par ex : déplacement, téléportation, victoire, défaite, etc.) 
    - modélisation des actions de jeu

    
- voir si on peut retirer teleporters si vide

- Classe timée qui envoie les commandes
- capturer le control C pour quitter proprement (pb de port sinon)
- Plug on/off

- ajouter des items de gameplay
    - aiguillage
    - lave leminningicide roundupisante
    - déplaceur d'objet
    - tapis roulant (fixe à une case)
    - case active / inactive

- faire le controleur
    - déplacement d'élément par
        - l'activation du potentiomètre linéaire 
        - l'activation du rotary encoder

- créer une structure du jeu complet

- interface de création de niveau en js

- aller plus loin dans le chargement des data json en objets pythons de nos classes..?
https://pynative.com/python-convert-json-data-into-custom-python-object/

ngs da
ns level
    - récupération des éléments modifiés
        - gestion des éléments sur un level (Map <coordonnée, element>)
            - appels de add element lors des ajouts de lemmings dans level
            - méthode de suppression des éléments dans level
- méthode de suppression des éléments dans level# DONE

- sockets non bloquants
- commande reset de niveau
- gagner le niveau
- générateur de lemmings
- Simuler les entrées de commande
    - Fausse interaction réseau
        - Centre de commande qui modifie l'état du jeu
- niveau 3 carré rotation 0 1 victorieuse
- commande rotation row col
- noter dans un fichier le protocole
- commande play : lancer niveau côté controller
- Supprimer résidu RingState
- Terminal interactif (play / pause)
- segment actif / inactif
- lemmings bougent correctement
- lemmings disparaissent une fois la sortie passée
- téléporteur
- nettoyage du GameEngine
- séparation Level / LevelBuilder
- 1er refacto LevelBuilder
- refacto Agent/Element
- transformer en package python
- plusieurs chemins de levels dans un fichier
- plusieurs levels dans le jeu
- alléger try parsing json dans LevelBuilder
- Thread de contrôle via socket
- Stop
- Play
