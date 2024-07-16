import json
from j5e.game.elements.Agent import Generator, Lemming
from j5e.game.elements.Element import Exit, Teleporter


class LevelSerializer:

    def __init__(self):
        pass

    def from_level(lvl):
        elements = []
        for coord, elem_list in lvl.elements.items():
            for elem in elem_list:
                elements.extend([ LevelSerializer.from_element(coord, elem)])

        agents = []
        for coord, ag_list in lvl.agents.items():
            for agent in ag_list:
                agents.extend([ LevelSerializer.from_agent(coord, agent)])

        return '{elements: [' + ",".join(elements) + ']}' + '\n' + '{agents: [' + ",".join(agents) + ']}' #+ '\n' + json.dumps(lvl)
    
    def from_element(coord, elem):
        res = LevelSerializer.from_coord(coord)
        if type(elem) is Exit:
            res = 'exit: {' + res + ',' + str(elem.remaining_lemmings) + '}' 
        elif type(elem) is Teleporter:
            res = 'teleporter {' + res + LevelSerializer.from_coord(elem.coord_dest) + '}'
        return res
    
    def from_agent(coord, agent):
        res = LevelSerializer.from_coord(coord)
        if type(agent) is Lemming:
            res = 'lemming: {' + res + '}' 
        elif type(agent) is Generator:
            res = 'generator {' + res + '}'
        return res
    
    def from_coord(coord):
        return "{row:" + str(coord.row) + ", col:" + str(coord.col) + ", type:" + str(coord.segment_type.name) + ", offset:" + str(coord.seg_offset) + "}"
