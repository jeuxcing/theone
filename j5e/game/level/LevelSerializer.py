from j5e.game.elements.Element import Exit


class LevelSerializer:

    def __init__(self):
        pass

    def from_level(lvl):
        elements = []
        for coord, elem_list in lvl.elements.items():
            elements.extend([ LevelSerializer.from_element(coord, elem) for elem in elem_list if type(elem) is Exit])
        return '{elements: [' + ",".join(elements) + ']}'
    
    def from_element(coord, elem):
        if type(elem) is Exit:
            return "exit: {" + LevelSerializer.from_coord(coord) + "}"
        else:
            return ""
        
    def from_coord(coord):
        return "{row:" + str(coord.row) + ", col:" + str(coord.col) + ", type:" + str(coord.segment_type) + ", offset:" + str(coord.seg_offset) + "}"
