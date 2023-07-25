import json
from game.j5e.game.Geometry import *
from game.j5e.game.Agents import Lemming


class Level:

    def __init__(self, grid_size):
        """
        :param int grid_size: nombre de ligne et colonnes de la grille (hypothèse : carrée) 
        """
        self.grid_size = grid_size
        self.rings = [[Ring(Coordinate(row,col,SegType.RING)) for col in range(grid_size)] for row in range(grid_size) ]
        self.rows = [[Line(Coordinate(row,col,SegType.ROW)) for col in range(grid_size-1)] for row in range(grid_size) ]
        self.cols = [[Line(Coordinate(row,col,SegType.COL)) for col in range(grid_size)] for row in range(grid_size-1) ]

        self.lemmings = [Lemming(1, "Lemmiwings", self.rows[0][0], 0, Direction.FORWARD)
                        ]#,Lemming(2, "Octodon", self.rings[0][0], 0 , Direction.RING_CLOCKWISE)]
        self.agents = [l for l in self.lemmings]

    def add_connection_to_ring(self, ring_row, ring_col, hour):
        match hour:
            case 3: 
                self.rings[ring_row][ring_col].set_3h(self.rows[ring_row][ring_col])
            case 6:
                self.rings[ring_row][ring_col].set_6h(self.cols[ring_row][ring_col])
            case 9:
                self.rings[ring_row][ring_col].set_9h(self.rows[ring_row-1][ring_col])
            case 12:
                self.rings[ring_row][ring_col].set_12h(self.cols[ring_row][ring_col-1])        

    def is_over(self):
        return len(self.lemmings) == 0

    def copy(self):
        lvl = Level(self.grid_size)
        for ring_row_idx, ring_row in enumerate(self.rings):
            for ring_col_idx, ring in enumerate(ring_row):
                for path_idx, path in enumerate(ring.paths):
                    if path is not None:
                        lvl.add_connection_to_ring(ring_row_idx, ring_col_idx, path_idx)
        return lvl

class LevelBuilder:

    def __init__(self):
        pass

    def load_level_list_from_json(json_file_path):
        #TODO plusieurs chemins de levels dans un fichier
        return [LevelBuilder.load_level_from_json(json_file_path)]

    def load_level_from_json(json_file_path):
        json_level = json.loads(open(json_file_path).read())
        grid_size = None
        geometry = None
        lemmings = None
        objects = None

       # Mandatory
        try:
            grid_size = json_level['grid_size']
            geometry = json_level['geometry']
            lemmings = json_level['lemmings']
            
        except KeyError as e:
            print("error : attribute not found in json config file ", e)
            return None

        lvl = Level(grid_size)
        LevelBuilder.initialize_geomtry(lvl,geometry)
        LevelBuilder.initialize_lemmings(lvl,lemmings)
        return lvl

    def initialize_geomtry(lvl, geometry):
        try:
            fully_connected = geometry['fully_connected']
            ring_connections = geometry['ring_connections']
            
        except KeyError as e:
            print("error : attribute not found in json config file ", e)
            return None

        #todo fully
        for connection in ring_connections:
            try:
                lvl.add_connection_to_ring(
                    connection['row_coord'], connection['col_coord'], connection['hour_coord'])
            except KeyError as e:
                print("error : attribute not found in json config file ", e)
                return None



    def initialize_lemmings(lvl, lemmings):
        pass
'''

        # Optional
        keyz = json_level.keys()
        for key in keyz:
            #print(key)
            if key == 'dimensions':
                #print("found dimensions")
                grid_size = json_level['dimensions']
                if hasattr(grid_size, 'grid_size'):
                    self.grid_size = grid_size['grid_size']
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

'''

'''
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
