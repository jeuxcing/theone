import json
from collections import namedtuple
from j5e.game.level.Geometry import Direction, Coordinate, SegType
from j5e.game.elements.Element import Exit, Teleporter
from j5e.game.elements.Agent import Lemming, Generator
from j5e.game.Actions import Actions
from j5e.game.level.Level import Level

class LevelBuilder:

    def __init__(self):
        pass

    def load_level_from_json(json_file_path):
        json_level = json.loads(open(json_file_path).read())
        
        var_names = ["grid_size", "geometry", "lemmings", "exits", "teleporters", "required_to_win"]
        data = json_to_named_tuple(var_names, json_level)
        
        lvl = Level(data.grid_size)
        LevelBuilder.initialize_geomtry(lvl,data.geometry)
        LevelBuilder.initialize_lemmings(lvl,data.lemmings)
        lvl.remaining_to_win = data.required_to_win
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
        var_names = ["row_coord", "col_coord", "seg_type", "offset"] 
        # optional : "required_lemmings"
        for exit in exits:
            data = json_to_named_tuple(var_names, exit)

            coord = copy_coord(lvl, data.row_coord, data.col_coord, data.seg_type, data.offset)

            if data.required_lemmings is not None:
                lvl.add_element(Exit(coord, data.required_lemmings))
            else:
                lvl.add_element(Exit(coord))

        
    def initialize_teleporters(lvl, teleporters):
        var_names = ["row_coord", "col_coord", "seg_type", "offset", "dest_row_coord", "dest_col_coord", "dest_seg_type", "dest_offset"]

        for teleporter in teleporters:
            data = json_to_named_tuple(var_names, teleporter)
            
            coord_src = copy_coord(lvl, data.row_coord, data.col_coord, data.seg_type, data.offset)
            coord_dest = copy_coord(lvl, data.dest_row_coord, data.dest_col_coord, data.dest_seg_type, data.dest_offset)

            lvl.add_element(Teleporter(coord_src, coord_dest))

    def initialize_generators(lvl, generators):
        var_names = ["row_coord", "col_coord", "seg_type", "offset", "lemming_number"]

        for generator in generators:
            data = json_to_named_tuple(var_names, generator)
            dir = Direction.__getitem__(data.direction)            
            coord = copy_coord(lvl, data.row_coord, data.col_coord, data.seg_type, data.offset)
            num_lemmings = data.num_lemmings

            lvl.add_generator(Generator(coord, num_lemmings, dir))

def copy_coord(lvl, row_coord, col_coord, seg_type, offset):
    seg = lvl.get_segment(Coordinate(row_coord, col_coord, SegType[seg_type]))
    return seg.coord.copy(offset)

# def json_to_named_tuple(var_names, dico):
#     JsonObject = namedtuple('JsonObject', var_names)
#     values = []
#     for var in var_names:
#         if var not in dico:
#             print("error : attribute not found in json config file ")
#             return None
#         values.append(dico[var])
    
#     return JsonObject(*values)

def json_to_named_tuple(mandatory_names, dico):
    # Vérifie la présence des clés obligatoires
    for name in mandatory_names:
        if name not in dico:
            print("error : attribute not found in json config file ")
            return None

    # Remplis les valeurs associées aux clés
    keys = [x for x in dico.keys()]
    JsonObject = namedtuple('JsonObject', keys)

    values = []
    for key in keys:
        values.append(dico[key])
    
    return JsonObject(*values)
