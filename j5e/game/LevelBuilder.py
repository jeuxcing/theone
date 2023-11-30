import json
from collections import namedtuple
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
        
        var_names = ["grid_size", "geometry", "lemmings", "exits", "teleporters"]
        data = json_to_named_tuple(var_names, json_level)            
        
        lvl = Level(data.grid_size)
        LevelBuilder.initialize_geomtry(lvl,data.geometry)
        LevelBuilder.initialize_lemmings(lvl,data.lemmings)
        LevelBuilder.initialize_exits(lvl,data.exits)
        LevelBuilder.initialize_teleporters(lvl,data.teleporters)
        return lvl

    def initialize_geomtry(lvl, geometry):
        var_names = ["fully_connected", "ring_connections", "ring_disconnections"]
        data = json_to_named_tuple(var_names, geometry)            

        if data.fully_connected:
            lvl.connect_all()        
            
        try:
            for connection in data.ring_connections:
                    lvl.add_connection_to_ring(*connection)
            for disconnection in data.ring_disconnections:
                lvl.rm_connection_to_ring(*disconnection)
        except KeyError as e:
            print("error : attribute not found in json config file ", e)
            return None


    def initialize_lemmings(lvl, lemmings):
        var_names = ["row_coord", "col_coord", "seg_type", "offset", "direction", "name"]
        for lemming in lemmings:
            data = json_to_named_tuple(var_names, lemming)            
            dir = Direction.__getitem__(data.direction)
            coord = copy_coord(lvl, data.row_coord, data.col_coord, data.seg_type, data.offset)
            
            lvl.add_lemming(Lemming(data.name, coord, dir))
            

    def initialize_exits(lvl, exits):
        var_names = ["row_coord", "col_coord", "seg_type", "offset", "required_lemmings"]
        for exit in exits:
            data = json_to_named_tuple(var_names, exit)

            coord = copy_coord(lvl, data.row_coord, data.col_coord, data.seg_type, data.offset)

            lvl.add_element(Exit(coord, data.required_lemmings))

        
    def initialize_teleporters(lvl, teleporters):
        var_names = ["row_coord", "col_coord", "seg_type", "offset", "dest_row_coord", "dest_col_coord", "dest_seg_type", "dest_offset"]

        for teleporter in teleporters:
            data = json_to_named_tuple(var_names, teleporter)
            
            coord_src = copy_coord(lvl, data.row_coord, data.col_coord, data.seg_type, data.offset)
            coord_dest = copy_coord(lvl, data.dest_row_coord, data.dest_col_coord, data.dest_seg_type, data.dest_offset)

            lvl.add_element(Teleporter(coord_src, coord_dest))

def copy_coord(lvl, row_coord, col_coord, seg_type, offset):
    seg = lvl.get_segment(Coordinate(row_coord, col_coord, SegType[seg_type]))
    return seg.coord.copy(offset)

def json_to_named_tuple(var_names, dico):
    JsonObject = namedtuple('JsonObject', var_names)
    values = []
    for var in var_names:
        if var not in dico:
            print("error : attribute not found in json config file ")
            return None
        values.append(dico[var])
    
    return JsonObject(*values)
