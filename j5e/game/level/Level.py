from j5e.game.level.Geometry import Ring, Coordinate, SegType, Line


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
        self.elements = {}

    def get_elements(self, coord):
        if coord not in self.elements.keys():
            return []
        else:
            return self.elements[coord]


    def add_lemming(self,lemming):
        self.lemmings.append(lemming)
        self.agents.append(lemming)                

    def add_element(self,element):
        coord_elements = self.get_elements(element.coord)
        self.elements[element.coord] = coord_elements + [element]

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
        for coord in self.elements:
            lvl.elements[coord.copy()] = [el.copy() for el in self.elements[coord]]
        return lvl

    def reverse_ring(self, row, col):
        self.get_segment(Coordinate(row, col, SegType.RING)).reverse_ring()

    def get_segment(self, coord):
        match coord.segment_type:
            case SegType.RING:
                return self.rings[coord.row][coord.col]
            case SegType.ROW:
                return self.rows[coord.row][coord.col]
            case SegType.COL:
                return self.cols[coord.row][coord.col]
            case other:
                return None