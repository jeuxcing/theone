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
                elements.append(LevelSerializer.from_element(coord, elem))

        agents = []
        for coord, ag_list in lvl.agents.items():
            for agent in ag_list:
                agents.append(LevelSerializer.from_agent(coord, agent))

        return json.dumps({'elements': elements, 'agents': agents}, separators=(',', ':'))
    
    def from_element(coord, elem, with_coord=True):
        res = {}
        if with_coord:
            res.update(LevelSerializer.from_coord(coord))
        if isinstance(elem, Exit):
            res.update({'type': 'Exit', 'remaining_lemmings': elem.remaining_lemmings})
        elif isinstance(elem, Teleporter):
            res.update({'type': 'Teleporter', 'coord_dest': LevelSerializer.from_coord(elem.coord_dest)})
        return res
    
    def from_agent(coord, agent, with_coord=True):
        res = {}
        if with_coord:
            res.update(LevelSerializer.from_coord(coord))
        if isinstance(agent, Lemming):
            res.update({'type': 'Lemming'})
        elif isinstance(agent, Generator):
            res.update({'type': 'Generator'})
        return res
    
    def from_coord(coord):
        return {
            'row': coord.row,
            'col': coord.col,
            'segtype': coord.segment_type.name,
            'offset': coord.seg_offset
        }
    
    def from_coord_content(lvl, coord):
        elements = [LevelSerializer.from_element(coord, elem, False) for elem in lvl.get_elements(coord)]
        agents = [LevelSerializer.from_agent(coord, agent, False) for agent in lvl.get_agents(coord)]
        return json.dumps({
            'row': coord.row,
            'col': coord.col,
            'segtype': coord.segment_type.name,
            'offset': coord.seg_offset,
            'content': elements + agents
        }, separators=(',', ':'))
