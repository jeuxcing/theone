from enum import Enum
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

