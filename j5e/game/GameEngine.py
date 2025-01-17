from threading import Thread
from multiprocessing import Event
from os import path
from sys import stderr

from j5e.game.GameExceptions import OutOfLedsException, NextLedOnOtherSegmentException
from j5e.game.level.Level import Level
from j5e.game.level.LevelBuilder import LevelBuilder
from j5e.game.elements.Element import Actions
from j5e.game.elements.Agent import Agent, Lemming
from j5e.game.level.Geometry import Coordinate
from j5e.game.level.LevelJsonifier import LevelJsonifier


class GameEngine(Thread):

    def __init__(self):
        super().__init__()
        self.timer = Event()
        self.levels = []

        self.current_level = None
        self.current_level_idx = None
        self._pause = True
        self.stopped = False
        self.controller = None

    def stop_thread(self):
        self.stopped = True

    def set_ctrl(self, controller):
        self.controller = controller

    def load_levels(self, filepath):
        """ Charge les niveaux depuis une liste de chemin relatifs de json les décrivant                
        """
        with open(filepath) as fp:
            dirpath = path.dirname(path.abspath(filepath))
            # Charge les niveaux un à un
            for line in fp:
                line = line.strip()
                # Chemin relatif au fichier qui liste les niveaux
                lvlpath = path.join(dirpath, line) 
                self.levels.append(LevelBuilder.load_level_from_json(lvlpath))

            # Met en place le niveau après chargement
            if len(self.levels) > 0:
                self.current_level_idx = 0
        
    def run(self):
        while (not self.is_over()):
            self.current_level = self.levels[self.current_level_idx].copy()
            print('Level', self.current_level.name)
            if self.controller is not None:
                self.controller.notify(
                    LevelJsonifier.from_level(self.current_level)
                )
            else:
                print("ATTENTION: Pas de controleur == pas de mise à jour", file=stderr)
            self.pause()
            self.run_current_lvl()
            
            # Si thread stoppé
            if self.stopped:
                break

            if self.current_level.is_won():
                self.current_level_idx += 1
                print("Niveau complété :o\n")
                self.controller.notify('{"action":"level_completed"}')
            else:
                self.controller.notify('{"action":"level_failed"}')
                print("Gros Nul ! RECOMMENCE §§ \n")
        print("Game Over")
        
    
    def is_over(self):
        return self.current_level_idx >= len(self.levels)
    
    def set_current_lvl(self, idx: int) -> None:
        # Mettre en pause le jeu
        self.pause()
        # Mettre à jour le niveau courant
        self.current_level_idx = idx
        # Arreter le niveau courant
        self.suicide_agents()
        # Remettre en marche
        self.play()

    def run_current_lvl(self):
        i=0
        # boucle d'action des éléments de jeu
        is_over = False
        while (not is_over) and (not self.timer.wait(0.2)):
            # Si jamais le thread doit se stopper en cours de jeu
            if self.stopped:
                return
            # Boucle normale
            if (not self._pause):
                print(' Tour n°', i,' : ')
                self.trigger_agents()
                print(f"Remaining to win: {self.current_level.remaining_to_win}")
                i += 1

            if self.current_level.is_over():
                is_over = True

    def pause(self):
        self._pause = True

    def play(self):
        self._pause = False

    def suicide_agents(self):
        self.current_level.agents.clear()

    def trigger_agents(self):
        agent_lst = []
        for lst_agent in self.current_level.agents.values():
            agent_lst.extend(lst_agent)

        modified_coords = set()
        for agent in agent_lst:
            modified_coords.update(self.execute(agent, agent.play()))

        # Notifie le controleur avec chaque état de chaque coordonées
        list_coords_modif = [LevelJsonifier.from_coord_content(self.current_level, coord) for coord in modified_coords]

        self.controller.notify(list_coords_modif)
        

    def execute(self, agent, action) -> set[Coordinate]:
        """ Applique l'action de l'agent
        :returns: L'ensemble des coordonnées modifiées qu'il faut envoyer au controleur pour redessin
        """

        modified_coords = set()
        modified_coords.add(agent.coord)
        segment = self.current_level.get_segment(agent.coord)

        match(action):
            case Actions.MOVE:
                # update agent vector
                print(agent.coord)
                self.current_level.delete_agent(agent)
                agent.coord, agent.dir = segment.get_next_destination(agent.coord.seg_offset, agent.dir)
                self.current_level.add_agent(agent)
                elements = self.current_level.get_elements(agent.coord)
                print(agent.name," va en ", agent.coord)
                modified_coords.update(self.apply_elements(agent,elements))
                json_object = LevelJsonifier.from_agent(agent.coord, agent)
                json_object['action'] = 'move'
                self.controller.notify(json_object)
            case Actions.BIRTH:
                self.current_level.add_agent(Lemming(f"Lem_{agent.num_lemmings}_{agent.name}", agent.coord, agent.dir))
        
        modified_coords.add(agent.coord)
        return modified_coords

    def apply_elements(self, agent, elements):
        """ Applique l'effet des élements sur l'agent
        :returns: L'ensemble des coordonnées modifiées qu'il faut envoyer au controleur pour redessin
        """
        modified_coords = set()
        modified_coords.add(agent.coord)

        for el in elements:
            action = el.receive(agent)
            match(action):
                case Actions.EXIT:
                    self.current_level.delete_agent(agent)
                    self.current_level.remaining_to_win -= 1
                case Actions.TELEPORT:
                    self.current_level.rm_element(agent)
                    agent.coord = el.coord_dest
                    self.current_level.add_element(agent)
                    print(agent.name," téléporté en ", agent.coord)
                    new_elements = self.current_level.get_elements(agent.coord)
                    modified_coords.update(self.apply_elements(agent, new_elements))
    

        modified_coords.add(agent.coord)
        return modified_coords

    def change_ring_rotation(self, row, col):
        self.current_level.reverse_ring(row,col)

