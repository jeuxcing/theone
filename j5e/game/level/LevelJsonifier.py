from j5e.game.elements.Agent import Generator, Lemming
from j5e.game.elements.Element import Exit, Teleporter


class LevelJsonifier:

    def __init__(self):
        pass


    def from_level(lvl):
        elements = []
        for coord, elem_list in lvl.elements.items():
            for elem in elem_list:
                elements.append(LevelJsonifier.from_element(coord, elem))

        agents = []
        for coord, ag_list in lvl.agents.items():
            for agent in ag_list:
                agents.append(LevelJsonifier.from_agent(coord, agent))

        return {'elements': elements, 'agents': agents}
    
    def from_element(coord, elem, with_coord=True):
        res = {}
        if isinstance(elem, Exit):
            res = {'type': 'Exit', 'remaining_lemmings': elem.remaining_lemmings}
        elif isinstance(elem, Teleporter):
            res = {'type': 'Teleporter', 'coord_dest': LevelJsonifier.from_coord(elem.coord_dest)}

        if with_coord:
            res['coords'] = LevelJsonifier.from_coord(coord)

        return res
    
    def from_agent(coord, agent, with_coord=True):
        res = {}
        
        if isinstance(agent, Lemming):
            res = {'type': 'Lemming'}
        elif isinstance(agent, Generator):
            res = {'type': 'Generator'}

        # Ajouter l'id de l'agent
        res['id'] = agent.id

        if with_coord:
            res['coords'] = LevelJsonifier.from_coord(coord)

        return res
    
    def from_coord(coord):
        return {
            'row': coord.row,
            'col': coord.col,
            'segtype': coord.segment_type.name,
            'offset': coord.seg_offset
        }
    
    def from_coord_content(lvl, coord):
        elements = [LevelJsonifier.from_element(coord, elem, False) for elem in lvl.get_elements(coord)]
        agents = [LevelJsonifier.from_agent(coord, agent, False) for agent in lvl.get_agents(coord)]
        return {
            'row': coord.row,
            'col': coord.col,
            'segtype': coord.segment_type.name,
            'offset': coord.seg_offset,
            'content': elements + agents
        }
