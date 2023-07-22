from enum import Enum
from abc import abstractmethod
from game.j5e.game.GameExceptions import OutOfLedsException


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

    def __init__(self, row, col, type, offset = None):
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
            raise OutOfLedsException

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