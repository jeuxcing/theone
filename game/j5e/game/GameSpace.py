import time
import networkx as nx
from j5e.hardware.led_strip import Grid, GridDims as gd

# Not used
class Node:
    def __init__(self):
        self.status = 0
        
    def create(self, segment_type, segment_pos_x, segment_pos_y, position_in_seg):
        self.seg_type = segment_type
        self.seg_pos_x = segment_pos_x
        self.seg_pos_y = segment_pos_y
        self.pos_in_seg = position_in_seg



class GameSpace:

    def __init__(self):
        self.graph = nx.DiGraph()
        
    #def init_graph(self, grid, n_leds_segment, n_leds_ring):
        #self.grid = grid
    def init_graph(self, grid_size, n_leds_segment, n_leds_ring):
        self.grid_size = grid_size
        self.n_leds_segment = n_leds_segment
        self.n_leds_ring = n_leds_ring
        print("Initializing graph...")
        # Create nodes
        node_index = 0;
        # Lines
        for line_idx in range(grid_size):
            for seg_idx in range(grid_size-1):
                for led_idx in range(n_leds_segment):
                    #n = Node()
                    #n.create('line', line_idx, seg_idx, led_idx)
                    #self.graph.add(n)
                    self.graph.add_node(node_index)
                    node_index += 1
        # Columns
        for line_idx in range(grid_size):
            for seg_idx in range(grid_size-1):
                for led_idx in range(n_leds_segment):
                    self.graph.add_node(node_index)
                    node_index += 1
        # Rings
        for line_idx in range(grid_size):
            for seg_idx in range(grid_size):
                for led_idx in range(n_leds_ring):
                    self.graph.add_node(node_index)
                    node_index += 1
        # Create edges
        # Within lines segments
        for line_idx in range(grid_size):
            for seg_idx in range(grid_size-1):
                for led_idx in range(1, n_leds_segment):
                    i = self.to_graph_node_index('line', line_idx, seg_idx, led_idx-1)
                    j = self.to_graph_node_index('line', line_idx, seg_idx, led_idx)
                    #print("i = ", i, " ; j = ", j)
                    self.graph.add_edge(i, j)
        # Within columns segments
        for line_idx in range(grid_size):
            for seg_idx in range(grid_size-1):
                for led_idx in range(1, n_leds_segment):
                    i = self.to_graph_node_index('column', line_idx, seg_idx, led_idx-1)
                    j = self.to_graph_node_index('column', line_idx, seg_idx, led_idx)
                    self.graph.add_edge(i, j)
        # Within rings segments
        for line_idx in range(grid_size):
            for seg_idx in range(grid_size):
                for led_idx in range(1, n_leds_ring):
                    i = self.to_graph_node_index('ring', line_idx, seg_idx, led_idx-1)
                    j = self.to_graph_node_index('ring', line_idx, seg_idx, led_idx)
                    self.graph.add_edge(i, j)
             
        # Lines and rings
        for line_idx in range(grid_size):
            for seg_idx in range(grid_size-1):
                led_ring_start = self.to_graph_node_index('ring', line_idx, seg_idx, 2)
                led_strip_start = self.to_graph_node_index('line', line_idx, seg_idx, 0)
                self.graph.add_edge(led_ring_start, led_strip_start)
                led_strip_end = self.to_graph_node_index('line', line_idx, seg_idx, n_leds_segment-1)
                led_ring_end = self.to_graph_node_index('ring', line_idx, seg_idx+1, 8)
                self.graph.add_edge(led_strip_end, led_ring_end)
        # Columns and rings
        for line_idx in range(grid_size):
            for seg_idx in range(grid_size-1):
                led_ring_start = self.to_graph_node_index('ring', line_idx, seg_idx, 5)
                led_strip_start = self.to_graph_node_index('column', line_idx, seg_idx, 0)
                self.graph.add_edge(led_ring_start, led_strip_start)
                led_strip_end = self.to_graph_node_index('column', line_idx, seg_idx, n_leds_segment-1)
                led_ring_end = self.to_graph_node_index('ring', line_idx, seg_idx+1, 11)
                self.graph.add_edge(led_strip_end, led_ring_end)
             
        #print("Printing nodes and edges")
        #print(list(self.graph.nodes))
        #print(list(self.graph.edges))
        print("Neighbors of node 290 = ", list(self.graph.neighbors(290)))
        print("Neighbors of node 22 = ", list(self.graph.neighbors(22)))
        print("Neighbors of node 22 = ", list(self.graph.neighbors(23)))
        
        
    def to_graph_node_index(self, segment_type, segment_pos_x, segment_pos_y, position_in_seg):
        #print("Computing node_index from coords ", segment_pos_x, " / ", segment_pos_y, " / ", position_in_seg)
        n_leds_per_type = self.grid_size * (self.grid_size-1) * self.n_leds_segment
        type_offset = -1
        graph_node_index = -1
        if segment_type == 'line':
            type_offset = 0
            graph_node_index = type_offset*n_leds_per_type \
            + (segment_pos_x * (self.grid_size-1) + segment_pos_y) * self.n_leds_segment \
            + position_in_seg
        elif segment_type == 'column':
            type_offset = 1
            graph_node_index = type_offset*n_leds_per_type \
            + (segment_pos_x * (self.grid_size-1) + segment_pos_y) * self.n_leds_segment \
            + position_in_seg
        elif segment_type == 'ring':
            type_offset = 2
            graph_node_index = type_offset*n_leds_per_type \
            + (segment_pos_x * self.grid_size + segment_pos_y) * self.n_leds_ring \
            + position_in_seg
        #print("=> ", graph_node_index)
        return graph_node_index
        
        
    def to_tuple_position(self, graph_node_index):
        n_leds_per_type = self.grid_size * (self.grid_size-1) * self.n_leds_segment
        type_offset = graph_node_index // n_leds_per_type
        pos_in_type = graph_node_index % n_leds_per_type
        strip_type = ''
        segment_pos_x = segment_pos_y = position_in_seg = -1
        if type_offset == 0:
            strip_type = 'line'
            segment_pos_x = pos_in_type // ((self.grid_size-1) * self.n_leds_segment)
            pos_in_set = pos_in_type % ((self.grid_size-1) * self.n_leds_segment)
            segment_pos_y = pos_in_set // self.n_leds_segment
            position_in_seg = pos_in_set % self.n_leds_segment
        elif type_offset == 1:
            strip_type = 'column'
            segment_pos_x = pos_in_type // ((self.grid_size-1) * self.n_leds_segment)
            pos_in_set = pos_in_type % ((self.grid_size-1) * self.n_leds_segment)
            segment_pos_y = pos_in_set // self.n_leds_segment
            position_in_seg = pos_in_set % self.n_leds_segment
        elif type_offset == 2:
            strip_type = 'ring'
            segment_pos_x = pos_in_type // ((self.grid_size) * self.n_leds_ring)
            pos_in_set = pos_in_type % ((self.grid_size) * self.n_leds_ring)
            segment_pos_y = pos_in_set // self.n_leds_ring
            position_in_seg = pos_in_set % self.n_leds_ring
        return (strip_type, segment_pos_x, segment_pos_y, position_in_seg)
        
    
    def compute_next_position_on_graph(self, g_position, direction):
        candidates = []
        change_direction = False
        new_direction = direction
        if direction == 1:
            candidates = list(self.graph.successors(g_position))
            if(len(candidates) == 0):
                change_direction = True
                candidates = list(self.graph.predecessors(g_position))
        elif direction == -1:
            candidates = list(self.graph.predecessors(g_position))
            if(len(candidates) == 0):
                change_direction = True
                candidates = list(self.graph.successors(g_position))
        if change_direction:
            new_direction = -direction
        # TODO : solve cases where there are several candidates (or none)
        new_g_position = candidates[0]
        return (new_g_position, new_direction)
    
    
    def get_next_position(self, position_and_direction):
        #position_orig = ()
        direction_orig = position_and_direction[4]
        g_position_orig = self.to_graph_node_index(position_and_direction[0], position_and_direction[1], position_and_direction[2], position_and_direction[3])
        new_g_pos_and_dir = self.compute_next_position_on_graph(g_position_orig, direction_orig)
        new_pos = self.to_tuple_position(new_g_pos_and_dir[0])
        new_pos_and_dir = (new_pos[0], new_pos[1], new_pos[2], new_pos[3], new_g_pos_and_dir[1])
        return new_pos_and_dir


#gr = Grid()
#gs = GameSpace(gr, 24, 12)
gs = GameSpace()
gs.init_graph(3, 24, 12)
pos = ('line', 0, 0, 22, 1)
print(gs.get_next_position(pos))