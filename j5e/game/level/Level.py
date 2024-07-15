from j5e.game.level.Geometry import Ring, Coordinate, SegType, Line
from j5e.game.elements.Agent import Lemming, Generator


class Level:

    def __init__(self, grid_size):
        """
        :param int grid_size: nombre de ligne et colonnes de la grille (hypothèse : carrée) 
        """
        self.grid_size = grid_size
        self.rings = [[Ring(Coordinate(row,col,SegType.RING)) for col in range(grid_size)] for row in range(grid_size) ]
        self.rows = [[Line(Coordinate(row,col,SegType.ROW)) for col in range(grid_size-1)] for row in range(grid_size) ]
        self.cols = [[Line(Coordinate(row,col,SegType.COL)) for col in range(grid_size)] for row in range(grid_size-1) ]
        self.agents = {}
        self.elements = {}
        self.remaining_to_win = float("inf")
     
    def get_elements(self, coord):
        if coord not in self.elements.keys():
            return []
        else:
            return self.elements[coord]

    def add_agent(self, agent):
        if agent.coord not in self.agents:
            self.agents[agent.coord] = [] 
        self.agents[agent.coord].append(agent)

    def add_element(self, element):
        coord_elements = self.get_elements(element.coord)
        self.elements[element.coord] = coord_elements + [element]

    def rm_element(self, element):
        print(self.elements)
        print(element)
        self.elements[element.coord].remove(element)

    def delete_agent(self, agent):
        self.agents[agent.coord].remove(agent)

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
        return self.is_lost() or self.is_won() 

    def is_won(self):
        return self.remaining_to_win <= 0

    def is_lost(self):
        if self.remaining_to_win == float('inf'):
            return False

        nb_lemmings = 0        
        for agent_list in self.agents.values():
            for agent in agent_list:                
                if type(agent) is Lemming : nb_lemmings += 1
                elif type(agent) is Generator: nb_lemmings += agent.num_lemmings
        return nb_lemmings < self.remaining_to_win

    def copy(self):
        lvl = Level(self.grid_size)
        lvl.remaining_to_win = self.remaining_to_win
        for ring_row_idx, ring_row in enumerate(self.rings):
            for ring_col_idx, ring in enumerate(ring_row):
                for path_idx, path in enumerate(ring.paths):
                    if path is not None:
                        lvl.add_connection_to_ring(ring_row_idx, ring_col_idx, path_idx)
        for agent_list in self.agents.values():
            for agent in agent_list:
                a = agent.copy()
                lvl.add_agent(a)
        for element_list in self.elements.values():
            for el in element_list:
                lvl.add_element(el.copy())
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