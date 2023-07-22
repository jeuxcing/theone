from enum import Enum
from abc import abstractmethod
from threading import Thread
from multiprocessing import Event

from game.j5e.game.Geometry import Coordinate, SegType
from game.j5e.game.GameExceptions import OutOfLedsException, NextLedOnOtherSegmentException
from game.j5e.game.Agents import Lemming, Trap


# TODO methods and defaults values

class Segment:

    def __init__(self, active=True, coord = None):
        self.active = active
        self.coord = coord
        if coord is not None: 
            self.coord.seg_offset = None

    @abstractmethod
    def get_next_coord(self, coord, dir):
        pass

class Line(Segment):

    def __init__(self, active=True, entrance = None, exit = None):
        super().__init__(active)
        self.entrance = entrance
        self.exit = exit

    # TODO ? coord -> offset
    def get_next_coord(self, coord, dir):
        try:
            return coord.get_next_coord(dir)
        except OutOfLedsException:
            if dir==Direction.BACKWARD and (self.entrance is not None):
                ring_offset_delta = 1 if self.entrance.clockwise else 0
                ring_offset_entrance = 2 if coord.segment_type==SegType.ROW else 5
                # exit the row in 0, enter the ring in 2 ( O<-- )
                # exit the col in 0, enter the ring in 5
                return Coordinate(coord.row, coord.col, SegType.RING, ring_offset_entrance+ring_offset_delta)


            elif dir==Direction.FORWARD and (self.exit is not None):
                ring_offset_delta = 1 if self.exit.clockwise else 0
                ring_offset_entrance = 8 if coord.segment_type==SegType.ROW else 11
                delta_row = 0 if coord.segment_type==SegType.ROW else 1
                delta_col = 1 if coord.segment_type==SegType.ROW else 0  
                # exit the row in 23, enter the ring in 8 ( -->O )
                # exit the col in 23, enter the ring in 11
                return Coordinate(coord.row+delta_row, coord.col+delta_col, SegType.RING, ring_offset_entrance+ring_offset_delta)

            else:
                raise OutOfLedsException


class Ring(Segment):

    def __init__(self, clockwise=True, path3h=None, path6h=None, path9h=None, path12h=None):
        super().__init__()
        self.clockwise = clockwise
        self.paths = [None] * 12
        self.paths[3] = path3h
        self.paths[6] = path6h
        self.paths[9] = path9h
        self.paths[0] = path12h

    def get_next_coord(self, coord, dir):
        previous_offset = (coord.seg_offset + 11) % 12
        offset = 0 if 1 < coord.seg_offset < 8 else 23
        if self.clockwise and (self.paths[previous_offset] is not None):
            return self.paths[previous_offset].coord.copy(offset)
        elif (not self.clockwise) and (self.paths[coord.seg_offset] is not None) :
            return self.paths[coord.seg_offset].coord.copy(offset)


class GameEngine(Thread):

    def __init__(self, grid_size):
        """
        :param int grid_size: nombre de ligne et colonnes de la grille (hypothèse : carrée) 
        """
        Thread.__init__(self)
        self.timer = Event()
        self.grid_size = grid_size
        self.rings = [[Ring(Coordinate(row,col,SegType.RING)) for col in range(grid_size)] for row in range(grid_size) ]
        self.rows = [[Segment(Coordinate(row,col,SegType.ROW)) for col in range(grid_size-1)] for row in range(grid_size) ]
        self.cols = [[Segment(Coordinate(row,col,SegType.COL)) for col in range(grid_size)] for row in range(grid_size-1) ]
        self.elements=[]


    def add(self,el):
        self.elements.append(el)

    def get_next_coord(self, coord, dir):

        #Select the current segment
        current_segment = None
        if (coord.segment_type == SegType.RING):
            current_segment = self.rings[coord.row][coord.col]
        elif (coord.segment_type == SegType.ROW):
            current_segment = self.rows[coord.row][coord.col]
        else:
            current_segment = self.cols[coord.row][coord.col]

        #Get the next coord
        try:
            return current_segment.get_next_coord(coord, dir)
        except OutOfLedsException:
            raise OutOfLedsException            
        except NextLedOnOtherSegmentException:
            #TODO calcul coordonné en sortie de segment
            if dir==Direction.FORWARD:
                +1
            else :
                -1
            return Coordinate()

        
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

