# NOTICE
Pour lancer : 
le jeu :
python3 -m j5e.game
le controleur :
python3 -m j5e.game.panelAdmin

un serveur web simple :
python3 -m http.server 8080

Commandes réseau d'interaction avec le jeu : j5e/game/PROTOCOL.md

Pour quitter proprement, play après le Game Over

Pour gagner un niveau, il faut que le nombre de lemmings requis total soit atteint

# INPROGRESS

- Mise à jour de l'état des lemmings lors du play. Objectif : voir les déplacements.

# TODO
- refacto from_coord_content / from_coord (DRY)
- modéliser les événements (état d'un élément du jeu / actions qui démarrent ou s'arrêtent)
-> le contrôleur (ESP) préempte l'évolution de l'état de sa vue associée mais c'est le moteur de jeu qui reste chef d'orchestre et resynchronise au besoin
- en pause, tout est synchronisé
- play -> on décentralise mouvements et collisions

- ajouter la possibilité de lancer un niveau choisi (bouton charger niveau + field numéro)

- faire le js de la rotation
- sérialization des éléments du level

- modélisation des actions de jeu

- Classe timée qui envoie les commandes
- Plug on/off

- intégrer l'envoi du niveau sérialisé à chaque début de niveau, msg = load_lvl ???

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



# DONE 

- AdminFlask SSE : mettre en place une Queue par client (sinon un seul reçoit)

- capturer le control C pour quitter proprement (pb de port sinon)

- suppression des teleporters et lemmings dans json si vide

- dans Level, tout mettre dans agents en se passant de lemings et generators

- sérialisation des exits

ngs dans level
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
