from enum import Enum
from game.j5e.game.OutOfLedsError import OutOfLedsError
from game.j5e.game.Agents import Lemming, Trap
from threading import Thread
from multiprocessing import Event

class SegType(Enum):
    RING = 0
    ROW = 1
    COL = 2

    def nb_leds(self):
        if self == SegType.RING :
            return 12
        else: 
            return 18        


class Coordinate:
    """
    Les coordonnées sont définies dans le sens de lecture.
    La position est composée d'une ligne, d'une colonne, type de segment (SegType).
    Par exemple la Coordinate 2 1 RING 0 désigne la led à 0h05 (0) de l'anneau (RING) sur la 3ème ligne (2) et sur la 2ème colonne (1).
    La line est le segment qui commence à droite du ring.
    Le col est le segment qui commence en dessous du ring.

    """

    def __init__(self, row, col, type, offset):
        self.row = row
        self.col = col
        self.segment_type = type
        self.seg_offset = offset


    def copy(self, offset):
        return Coordinate(self.row, self.col, self.segment_type, offset)


    def __eq__(self, other):
        return self.row == other.row and self.col == other.col and self.segment_type == other.segment_type


    def get_next_coord(self, dir):
        #RING clockwise
        if (self.segment_type == SegType.RING):
            next_offset = self.seg_offset+1
            if (next_offset == self.segment_type.nb_leds()):
                next_offset = 0
            return self.copy(next_offset)
        
        #STRIPS
        if (self.seg_offset + dir.delta() <0 or self.seg_offset + dir.delta() > self.segment_type.nb_leds()):
            raise OutOfLedsError

        return self.copy(self.seg_offset + dir.delta())

    def __repr__(self):
        return f"{self.row} {self.col} {self.segment_type} {self.seg_offset}"    


class Direction(Enum):
    FORWARD = 1
    BACKWARD = -1
    RING_CLOCKWISE = 2
    RING_COUNTERCLOCKWISE = -2

    def delta(self):
        if (self == Direction.FORWARD or self == Direction.RING_CLOCKWISE):
            return 1
        else:
            return -1    


    def opposite(self):
        match(self):
            case Direction.FORWARD:
                return Direction.BACKWARD
            case Direction.BACKWARD:
                return Direction.FORWARD
            case Direction.RING_CLOCKWISE:
                return Direction.RING_COUNTERCLOCKWISE
            case Direction.RING_COUNTERCLOCKWISE:
                return Direction.RING_CLOCKWISE


class RingState(Enum):
    INACTIVE = 1
    CLOCKWISE = 2
    COUNTERCLOCKWISE = 3


class GameEngine(Thread):
    def __init__(self, grid_size):
        """
        :param int grid_size: nombre de ligne et colonnes de la grille (hypothèse : carrée) 
        """
        Thread.__init__(self)
        self.timer = Event()
        self.grid_size = grid_size
        self.elements=[]
        
    def add(self,el):
        self.elements.append(el)  
        
    def run(self):
        i=0
        # boucle d'action des éléments de jeu
        while not self.timer.wait(0.2):
            print(i,' : ')
            for element in self.elements:
                element.go()
                # suppression des lemmings non actifs
                if  isinstance(element,Lemming) and element.active==False:
                    self.elements.remove(element)
                    ## arrêt lorsque plus aucun lemming n'est actif
                    if True not in [isinstance(ele,Lemming) for ele in self.elements] :
                        self.timer.set()
            i+=1    

             
'''
    def get_nb_lines_segments_leds(self,segment_type):
        return (self.grid_size,self.grid_size,self.n_leds_ring) if segment_type=="ring" \
        else (self.grid_size,self.grid_size-1,self.n_leds_segment)
    
    def create_nodes(self,segment_type):
        nb_lines,nb_segments,n_leds = self.get_nb_lines_segments_leds(segment_type)
        for line_idx in range(nb_lines):
            for seg_idx in range(nb_segments):
                for led_idx in range(n_leds):
                    #n = Node()
                    #n.create('line', line_idx, seg_idx, led_idx)
                    #self.graph.add(n)
                    self.graph.add_node(self.node_index)
                    self.graph.nodes[self.node_index]['type'] = segment_type
                    self.graph.nodes[self.node_index]['alive'] = 1
                    self.node_index += 1

    def create_edges_within(self,segment_type):
        nb_lines,nb_segments,n_leds = self.get_nb_lines_segments_leds(segment_type)
        for line_idx in range(nb_lines):
            for seg_idx in range(nb_segments):
                for led_idx in range(1, n_leds):
                    i = self.to_graph_node_index(segment_type, line_idx, seg_idx, led_idx-1)
                    j = self.to_graph_node_index(segment_type, line_idx, seg_idx, led_idx)
                    #print("i = ", i, " ; j = ", j)
                    self.graph.add_edge(i, j)
                if (segment_type=="ring"):
                    led_end = self.to_graph_node_index('ring', line_idx, seg_idx, n_leds-1)
                    led_start = self.to_graph_node_index('ring', line_idx, seg_idx, 0)
                    self.graph.add_edge(led_end, led_start)
                        
                    
    # Assumes positions for start and end are valid
    def set_section_status(self, segment_type, segment_pos_x, segment_pos_y, led_start, led_end, status):
        graph_ind_start = self.to_graph_node_index(segment_type, segment_pos_x, segment_pos_y, led_start)
        graph_ind_end = self.to_graph_node_index(segment_type, segment_pos_x, segment_pos_y, led_end)
        for i in range(graph_ind_start, graph_ind_end+1):
            self.graph.nodes[i]['alive'] = status


    def change_direction_segment(self, segment_type, segment_pos_x, segment_pos_y):
        if segment_type == 'ring':
            # Reverse internal edges
            edges_to_remove = []
            edges_to_add = []
            for z in range(self.n_leds_ring):
                node_ind = self.to_graph_node_index(segment_type, segment_pos_x, segment_pos_y, z)
                succs = self.graph.successors(node_ind)
                for succ in succs:
                    if self.graph.nodes[succ]['type'] == segment_type:
                        edges_to_remove.append((node_ind, succ))
                        edges_to_add.append((succ, node_ind))
            for e in edges_to_remove:
                self.graph.remove_edge(e[0], e[1])
            for e in edges_to_add:
                self.graph.add_edge(e[0], e[1])
        
        
    def to_graph_node_index(self, segment_type, segment_pos_x, segment_pos_y, position_in_seg):
        print("Computing node_index from coords ", segment_pos_x, " / ", segment_pos_y, " / ", position_in_seg)
        n_leds_per_type = self.grid_size * (self.grid_size-1) * self.n_leds_segment
        type_offset = -1
        nb_segments,n_leds = self.get_nb_lines_segments_leds(segment_type)[1:]
        if segment_type == 'line':
            type_offset = 0
        elif segment_type == 'column':
            type_offset = 1
        elif segment_type == 'ring':
            type_offset = 2
        graph_node_index = type_offset*n_leds_per_type \
        + (segment_pos_x * nb_segments + segment_pos_y) * n_leds \
        + position_in_seg
        print("=> ", graph_node_index)
        return graph_node_index
        
        
    def to_tuple_position(self, graph_node_index):
        n_leds_per_type = self.grid_size * (self.grid_size-1) * self.n_leds_segment
        type_offset = graph_node_index // n_leds_per_type
        pos_in_type = graph_node_index % n_leds_per_type
        strip_type = ''
        if type_offset == 0:
            strip_type = 'line'
        elif type_offset == 1:
            strip_type = 'column'
        elif type_offset == 2:
            strip_type = 'ring'
        nb_segments,n_leds = self.get_nb_lines_segments_leds(strip_type)[1:]
        segment_pos_x = pos_in_type // (nb_segments * n_leds)
        pos_in_set = pos_in_type % (nb_segments * n_leds)
        segment_pos_y = pos_in_set // n_leds
        position_in_seg = pos_in_set % n_leds

        return (strip_type, segment_pos_x, segment_pos_y, position_in_seg)


    # Assumes that the next element of the ring is the first 'successor' neighbor
    # Exits the rings if possible ; if not, keep on turnin'
    def find_ring_exit(self, succs, preds, direction):
        for x in succs:
            if self.graph.nodes[x]["type"] != "ring":
                return {"position" : x, "direction" : Direction.FORWARD}
        for x in preds:
            if self.graph.nodes[x]["type"] != "ring":
                return {"position" : x, "direction" : Direction.BACKWARD}
        print("haha")
        return {"position" : succs[0], "direction" : direction}


    def filter_valid_nodes(self, nodes):
        new_nodes = []
        for n in nodes:
            if(self.graph.nodes[n]['alive'] == 1):
                new_nodes.append(n)
        return new_nodes


    def reverse_direction(self, direction):
        if direction == Direction.FORWARD:
            return Direction.BACKWARD
        elif direction == Direction.BACKWARD:
            return Direction.FORWARD
        return direction
        
    
    def compute_next_position_on_graph(self, g_position, direction):
        candidates = []
        # Specific behavior when in a ring
        if (self.graph.nodes[g_position]["type"] == "ring"):
            if direction == Direction.RING_CLOCKWISE:
                #print("ring")
                succs = list(self.graph.successors(g_position))
                preds = list(self.graph.predecessors(g_position))
                next = self.find_ring_exit(succs, preds, direction)
                return (next["position"], next["direction"])
            elif direction == Direction.RING_COUNTERCLOCKWISE:
                #print("ring")
                succs = list(self.graph.successors(g_position))
                preds = list(self.graph.predecessors(g_position))
                next = self.find_ring_exit(preds, succs, direction)
                return (next["position"], next["direction"])
            else:
                # Issue : what hapens when a ring is blocked / has no available successor ?
                candidates = list(self.graph.successors(g_position))
                new_g_position = candidates[0]
                new_direction = Direction.RING_CLOCKWISE
                if direction == Direction.BACKWARD:
                    new_direction = Direction.FORWARD
                return (new_g_position, new_direction)
        else:
            change_direction = False
            new_direction = direction
            if direction == Direction.FORWARD:
                candidates = self.filter_valid_nodes(list(self.graph.successors(g_position)))
                if(len(candidates) == 0):
                    change_direction = True
                    candidates = self.filter_valid_nodes(list(self.graph.predecessors(g_position)))
            elif direction == Direction.BACKWARD:
                candidates = self.filter_valid_nodes(list(self.graph.predecessors(g_position)))
                if(len(candidates) == 0):
                    change_direction = True
                    candidates = self.filter_valid_nodes(list(self.graph.successors(g_position)))
            if change_direction:
                new_direction = self.reverse_direction(direction)
            # TODO : solve cases where there are several candidates (or none)
            if(len(candidates) == 0):
                print("error : no successors and no predecessors for node ", g_position)
            new_g_position = candidates[0]
            return (new_g_position, new_direction)
    
    
    def get_next_position(self, position, direction):
        #position_orig = ()
        direction_orig = direction
        g_position_orig = self.to_graph_node_index(*position)

        print(g_position_orig)
        # pos -144

        new_g_pos_and_dir = self.compute_next_position_on_graph(g_position_orig, direction_orig)
        new_pos = self.to_tuple_position(new_g_pos_and_dir[0])
        new_pos_and_dir = (new_pos[0], new_pos[1], new_pos[2], new_pos[3], new_g_pos_and_dir[1])
        return new_pos_and_dir
'''
