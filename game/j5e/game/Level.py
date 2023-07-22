from game.j5e.game.Geometry import *
from game.j5e.game.Agents import Lemming


class Level:

    def __init__(self, grid_size):
        """
        :param int grid_size: nombre de ligne et colonnes de la grille (hypothèse : carrée) 
        """
        self.grid_size = grid_size
        self.rings = [[Ring(Coordinate(row,col,SegType.RING)) for col in range(grid_size)] for row in range(grid_size) ]
        self.rows = [[Segment(Coordinate(row,col,SegType.ROW)) for col in range(grid_size-1)] for row in range(grid_size) ]
        self.cols = [[Segment(Coordinate(row,col,SegType.COL)) for col in range(grid_size)] for row in range(grid_size-1) ]

        start_lemmi = Coordinate(0, 0, SegType.ROW, 0)
        start_octo = Coordinate(0, 0, SegType.RING, 0)
        goal = Coordinate(1, 0, SegType.ROW, 0)
        self.lemmings = [Lemming(1, "Lemmiwings", start_lemmi, Direction.FORWARD, goal),
                        Lemming(2, "Octodon", start_octo, Direction.RING_CLOCKWISE, goal)]

    def is_over(self):
        return len(self.lemmings) == 0

'''
    gameEngine.add(Trap(3, "une porte",4))




                for element in self.elements:
                element.go()
                # suppression des lemmings non actifs
                if  isinstance(element,Lemming) and element.active==False:
                    self.elements.remove(element)
                    ## arrêt lorsque plus aucun lemming n'est actif
                    if True not in [isinstance(ele,Lemming) for ele in self.elements] :
                        self.timer.set()





    def set_config_from_json(self, json_file_path):
        self.config.load_config_from_json(json_file_path)
        self.translate_config_to_gamespace()
        self.setup_agents()

    # Create GameSpace graph matching the config
    def translate_config_to_gamespace(self):
        print("init graph with params", self.config.grid_size, self.config.n_leds_segment, self.config.n_leds_ring)
        self.gamespace.init_graph(self.config.grid_size, self.config.n_leds_segment, self.config.n_leds_ring)
        print("adding", len(self.config.walls), "walls")
        for w in self.config.walls:
            self.gamespace.set_section_status(w[0].segment_type, w[0].seg_pos_x, w[0].seg_pos_y, w[0].pos_in_seg, w[1].pos_in_seg, 0)
        print("reversing direction on", len(self.config.walls), "rings")
        for rr in self.config.reverse_rings:
            self.gamespace.change_direction_segment(rr.segment_type, rr.seg_pos_x, rr.seg_pos_y)

    def setup_agents(self):
        self.agent=Lemming(1, "Lemmiwings",self.config.start_point.getCoord(), Direction.FORWARD, self.config.end_point.getCoord(), self.gamespace)
        # TODO : setup from agents in config, only one for the moment
        
'''       







class Config:

    def __init__(self, grid_s = 3):
        self.grid_size = grid_s
        self.n_leds_segment = n_leds_s
        self.n_leds_ring = n_leds_r
        self.walls = []
        self.reverse_rings = []
        self.n_lemmings = 1
        self.time_between_spawns_lemmings = 5
        self._n_lemmings_to_win = 1

    # Parser
    def load_config_from_json(self, json_file_path):
        json_contents = json.loads(open(json_file_path).read())
        # Level layout
        json_level = json_contents['level']
        # Mandatory
        try:
            json_start_point = json_level['start_point']
            json_end_point = json_level['end_point']
            self.start_point = Position(json_start_point['segment_type'], json_start_point['seg_pos_x'], json_start_point['seg_pos_y'], json_start_point['pos_in_seg'])
            self.end_point = Position(json_end_point['segment_type'], json_end_point['seg_pos_x'], json_end_point['seg_pos_y'], json_end_point['pos_in_seg'])
        except AttributeError:
            print("error : no valid start or end point found in json config file ", json_file_path)
        # Optional
        keyz = json_level.keys()
        for key in keyz:
            #print(key)
            if key == 'dimensions':
                #print("found dimensions")
                json_dimensions = json_level['dimensions']
                if hasattr(json_dimensions, 'grid_size'):
                    self.grid_size = json_dimensions['grid_size']
            elif key == 'hazards':
                #print("found hazards")
                json_hazards = json_level['hazards']
                keyz_hazards = json_hazards.keys()
                for key_hazard in keyz_hazards:
                    if key_hazard == 'walls':
                        json_walls = json_hazards['walls']
                        for w in json_walls:
                            self.walls.append((Position(w['segment_type'], w['seg_pos_x'], w['seg_pos_y'], w['pos_in_seg_start']), Position(w['segment_type'], w['seg_pos_x'], w['seg_pos_y'], w['pos_in_seg_end'])))
                    elif key_hazard == 'reverse_rings':
                        json_reverse_rings = json_hazards['reverse_rings']
                        for rr in json_reverse_rings:
                            self.reverse_rings.append(Position('ring', rr['seg_pos_x'], rr['seg_pos_y'], 0))
        # Agents
        json_agents = json_contents['agents']
        keyz_agents = json_agents.keys()
        for key in keyz_agents:
            if key == 'lemmings':
                self.n_lemmings = json_agents['lemmings']['number_spawns']
                self.time_between_spawns_lemmings = json_agents['lemmings']['time_between_spawns']
                self.n_lemmings_to_win = json_agents['lemmings']['number_to_win']