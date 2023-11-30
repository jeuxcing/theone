# INPROGRESS


# TODO
python3 -m game.j5e.game
-> transformer en package python

- alléger try parsing json dans LevelBuilder ?    

- Fausse interaction réseau
    - Centre de commande qui modifie l'état du jeu
    - Classe timée qui envoie les commandes
        - Play
        - Stop
        - Plug on/off

- ajouter des items de gameplay
    - aiguillage
    - générateur de lemmings
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

- TODO plusieurs chemins de levels dans un fichier


# DONE

- segment actif / inactif
- lemmings bougent correctement
- lemmings disparaissent une fois la sortie passée
- téléporteur
- nettoyage du GameEngine
- séparation Level / LevelBuilder
- 1er refacto LevelBuilder
- refacto Agent/Element