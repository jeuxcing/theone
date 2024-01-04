# INPROGRESS
Pour lancer : 
python3 -m j5e.game


# TODO

- Terminal interactif (play / pause)
- Simuler les entrées de commande
    - Fausse interaction réseau
        - Centre de commande qui modifie l'état du jeu
        - Classe timée qui envoie les commandes
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

- aller plus loin dans le chargement des data json en objets pythons de nos classes..?
https://pynative.com/python-convert-json-data-into-custom-python-object/


# DONE

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