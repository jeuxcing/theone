import json
from j5e.game.Geometry import *
from j5e.game.Element import Exit, Teleporter
from j5e.game.Agent import Lemming
from j5e.game.Actions import Actions
from j5e.game.Level import Level

class LevelBuilder:

    def __init__(self):
        pass

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
        LevelBuilder.initialize_teleporters(lvl,teleporters)
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
            
            dir = Direction.__getitem__(direction)
            seg = lvl.get_segment(Coordinate(row_coord, col_coord, SegType[seg_type]))
            coord = seg.coord.copy(offset)
            
            lvl.add_lemming(Lemming(name, coord, dir))
            

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
            
            seg = lvl.get_segment(Coordinate(row_coord, col_coord, SegType[seg_type]))
            coord = seg.coord.copy(offset)

            exit = Exit(coord, required_lemmings)
            lvl.add_element(exit)
            
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
            
            seg_src = lvl.get_segment(Coordinate(row_coord, col_coord, SegType[seg_type]))
            coord_src = seg_src.coord.copy(offset)

            seg_dest = lvl.get_segment(Coordinate(dest_row_coord, dest_col_coord, SegType[dest_seg_type]))
            coord_dest = seg_dest.coord.copy(dest_offset)

            teleporter = Teleporter(coord_src, coord_dest)
            lvl.add_element(teleporter)

