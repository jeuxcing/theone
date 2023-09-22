import json
from game.j5e.game.Geometry import *
from game.j5e.game.Agents import Lemming, Exit
from copy import deepcopy


class Level:

    def __init__(self, grid_size):
        """
        :param int grid_size: nombre de ligne et colonnes de la grille (hypothèse : carrée) 
        """
        self.grid_size = grid_size
        self.rings = [[Ring(Coordinate(row,col,SegType.RING)) for col in range(grid_size)] for row in range(grid_size) ]
        self.rows = [[Line(Coordinate(row,col,SegType.ROW)) for col in range(grid_size-1)] for row in range(grid_size) ]
        self.cols = [[Line(Coordinate(row,col,SegType.COL)) for col in range(grid_size)] for row in range(grid_size-1) ]
        self.lemmings = []
        self.agents = []
        self.exits = []
        self.elements = {}

    def get_elements(self, coord):
        if coord not in self.elements.keys():
            return []
        else:
            return self.elements[coord]


    def add_lemming(self,lemming):
        self.lemmings.append(lemming)
        self.agents.append(lemming)                

    def add_exit(self,exit):
        self.exits.append(exit)
        coord_elements = self.get_elements(exit.coord)
        self.elements[exit.coord] = coord_elements + [exit]

    def delete_agent(self, agent):
        self.agents.remove(agent)
        if agent in self.lemmings:
            self.lemmings.remove(agent)

    def connect_all(self) :
        for row_idx, row in enumerate(range(self.grid_size)):
            for col_idx, col in enumerate(range(self.grid_size)):
                if row_idx > 0 :
                    self.add_connection_to_ring(row_idx, col_idx, 12)
                if row_idx < (self.grid_size - 1):
                    self.add_connection_to_ring(row_idx, col_idx, 6)

                if col_idx > 0 :
                    self.add_connection_to_ring(row_idx, col_idx, 9)
                if col_idx < (self.grid_size - 1):
                    self.add_connection_to_ring(row_idx, col_idx, 3)


    def add_connection_to_ring(self, ring_row, ring_col, hour):
        match hour:
            case 3: 
                self.rings[ring_row][ring_col].set_3h(self.rows[ring_row][ring_col])
            case 6:
                self.rings[ring_row][ring_col].set_6h(self.cols[ring_row][ring_col])
            case 9:
                self.rings[ring_row][ring_col].set_9h(self.rows[ring_row][ring_col-1])
            case 12 | 0:
                self.rings[ring_row][ring_col].set_12h(self.cols[ring_row-1][ring_col])        


    def rm_connection_to_ring(self, ring_row, ring_col, hour):
        match hour:
            case 3: 
                self.rings[ring_row][ring_col].set_3h(None)
            case 6:
                self.rings[ring_row][ring_col].set_6h(None)
            case 9:
                self.rings[ring_row][ring_col].set_9h(None)
            case 12 | 0:
                self.rings[ring_row][ring_col].set_12h(None)


    def is_over(self):
        return len(self.lemmings) == 0


    def copy(self):
        lvl = Level(self.grid_size)
        for ring_row_idx, ring_row in enumerate(self.rings):
            for ring_col_idx, ring in enumerate(ring_row):
                for path_idx, path in enumerate(ring.paths):
                    if path is not None:
                        lvl.add_connection_to_ring(ring_row_idx, ring_col_idx, path_idx)
        for lemming in self.lemmings:
            l = lemming.copy()
            lvl.add_lemming(l)
        for exit in self.exits:
            e = exit.copy()
            lvl.add_exit(e)
            
        return lvl
    
    def getSegment(self, coord):
        match coord.segment_type:
            case SegType.RING:
                return self.rings[coord.row][coord.col]
            case SegType.ROW:
                return self.rows[coord.row][coord.col]
            case SegType.COL:
                return self.cols[coord.row][coord.col]
            case other:
                return None
        

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
        exits = None
        teleporters = None

       # Mandatory
        try:
            grid_size = json_level['grid_size']
            geometry = json_level['geometry']
            lemmings = json_level['lemmings']
            exits = json_level['exits']
            teleporters = json_level['teleporters']
            
        except KeyError as e:
            print("error : attribute not found in json config file ", e)
            return None

        lvl = Level(grid_size)
        LevelBuilder.initialize_geomtry(lvl,geometry)
        LevelBuilder.initialize_lemmings(lvl,lemmings)
        LevelBuilder.initialize_exits(lvl,exits)
        LevelBuilder.initialize_teleport(lvl,teleporters)
        return lvl

    def initialize_geomtry(lvl, geometry):
        try:
            fully_connected = geometry['fully_connected']
            ring_connections = geometry['ring_connections']
            ring_disconnections = geometry['ring_disconnections']
            
        except KeyError as e:
            print("error : attribute not found in json config file ", e)
            return None

        if fully_connected:
            lvl.connect_all()        
            
        for connection in ring_connections:
            try:
                lvl.add_connection_to_ring(*connection)
            except KeyError as e:
                print("error : attribute not found in json config file ", e)
                return None

        for disconnection in ring_disconnections:
            try:
                lvl.rm_connection_to_ring(*disconnection)
            except KeyError as e:
                print("error : attribute not found in json config file ", e)
                return None


    def initialize_lemmings(lvl, lemmings):
        for lemming in lemmings:
            try:
                name = lemming['name']
                row_coord = lemming['row_coord']
                col_coord = lemming['col_coord']
                seg_type = lemming['seg_type']
                offset = lemming['offset']
                direction = lemming['direction']
            except KeyError as e:
                print("error : attribute not found in json config file ", e)
                return None
            
            segment = None
            if seg_type == "ROW":
                segment = lvl.rows[row_coord][col_coord]
            elif seg_type == "COL":
                segment = lvl.cols[row_coord][col_coord]
            else:
                segment = lvl.rings[row_coord][col_coord]

            coord = segment.coord.copy(offset)

            dir = Direction.__getitem__(direction)
            
            l = Lemming(name, coord, dir)
            lvl.add_lemming(l)
            

    def initialize_exits(lvl, exits):
        for exit in exits:
            try:
                row_coord = exit['row_coord']
                col_coord = exit['col_coord']
                seg_type = exit['seg_type']
                offset = exit['offset']
                required_lemmings = exit['required_lemmings']
            except KeyError as e:
                print("error : attribute not found in json config file ", e)
                return None
            
            segment = None
            if seg_type == "ROW":
                segment = lvl.rows[row_coord][col_coord]
            elif seg_type == "COL":
                segment = lvl.cols[row_coord][col_coord]
            else:
                segment = lvl.rings[row_coord][col_coord]
            
            coord = segment.coord.copy(offset)

            exit = Exit(coord, required_lemmings)
            lvl.add_exit(exit)
            
    def initialize_teleporters(lvl, teleporters):
        for teleporter in teleporters:
            try:
                row_coord = teleporter['row_coord']
                col_coord = teleporter['col_coord']
                seg_type = teleporter['seg_type']
                offset = teleporter['offset']
                dest_row_coord = teleporter['dest_row_coord']
                dest_col_coord = teleporter['dest_col_coord']
                dest_seg_type = teleporter['dest_seg_type']
                dest_offset = teleporter['dest_offset']
            except KeyError as e:
                print("error : attribute not found in json config file ", e)
                return None
            
            segment = None
            if seg_type == "ROW":
                segment = lvl.rows[row_coord][col_coord]
            elif seg_type == "COL":
                segment = lvl.cols[row_coord][col_coord]
            else:
                segment = lvl.rings[row_coord][col_coord]
            
            coord = segment.coord.copy(offset)

            teleporter = Teleporter(coord, required_lemmings)
            lvl.add_exit(teleporter)






