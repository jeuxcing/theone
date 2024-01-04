from enum import Enum
from abc import abstractmethod
from j5e.game.GameExceptions import OutOfLedsException


class SegType(Enum):
    RING = 0
    ROW = 1
    COL = 2

    def nb_leds(self):
        if self == SegType.RING :
            return 12
        else: 
            return 24    


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


    def copy(self, offset = None):
        if offset is None:
            offset = self.seg_offset
        return Coordinate(self.row, self.col, self.segment_type, offset)
    

    def __eq__(self, other):
        # /!\ offset à None pour les coord de segments
        return self.row == other.row and self.col == other.col and self.seg_offset == other.seg_offset and self.segment_type == other.segment_type

    def __hash__(self) -> int:
        off_val = 25 if self.seg_offset is None else self.seg_offset
        return self.row + self.col * 5 + self.segment_type.value * 5 * 5 + off_val * 5 * 5 * 3

    def get_next_coord(self, dir):
        #RING clockwise
        if (self.segment_type == SegType.RING):
            next_offset = self.seg_offset+1
            if (next_offset == self.segment_type.nb_leds()):
                next_offset = 0
            return self.copy(next_offset)
        
        #STRIPS
        if (self.seg_offset + dir.delta() <0 or self.seg_offset + dir.delta() >= self.segment_type.nb_leds()):
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

    def __init__(self, coord = None):
        self.coord = coord
        if coord is not None: 
            self.coord.seg_offset = None

    @abstractmethod
    def get_next_destination(self, offset, dir):
        """
        Retourne un triplet (segment, offset, direction) à partir de la coordonnée actuelle et de la direction de l'agent
        """
        pass

    def __repr__(self) -> str:
        return str(self.coord)

class Line(Segment):

    def __init__(self, coord, entrance = None, exit = None):
        super().__init__(coord)
        self.entrance = entrance
        self.exit = exit

    def get_next_destination(self, offset, dir):

        try:
            dest_coord = self.coord.copy(offset).get_next_coord(dir)
            return self.coord.copy(dest_coord.seg_offset), dir
        except OutOfLedsException:
            print("exception",dir,self.entrance,self.exit)
            if dir==Direction.BACKWARD and (self.entrance is not None):
                print("1er if")
                ring_offset_delta = 1 if self.entrance.clockwise else 0
                ring_offset_entrance = 2 if self.coord.segment_type==SegType.ROW else 5
                # exit the row in 0, enter the ring in 2 ( O<-- )
                # exit the col in 0, enter the ring in 5
                dest_offset = ring_offset_entrance+ring_offset_delta
                dest_dir = Direction.RING_CLOCKWISE if self.entrance.clockwise else Direction.RING_COUNTERCLOCKWISE
                return self.entrance.coord.copy(dest_offset), dest_dir


            elif dir==Direction.FORWARD and (self.exit is not None):
                print("passe")
                ring_offset_delta = 1 if self.exit.clockwise else 0
                ring_offset_entrance = 8 if self.coord.segment_type==SegType.ROW else 11
                delta_row = 0 if self.coord.segment_type==SegType.ROW else 1
                delta_col = 1 if self.coord.segment_type==SegType.ROW else 0  
                # exit the row in 23, enter the ring in 8 ( -->O )
                # exit the col in 23, enter the ring in 11
                dest_offset = ring_offset_entrance+ring_offset_delta
                dest_dir = Direction.RING_CLOCKWISE if self.exit.clockwise else Direction.RING_COUNTERCLOCKWISE
                return self.exit.coord.copy(dest_offset), dest_dir

            else:
                dest_dir = dir.opposite()
                dest_offset = offset+dest_dir.delta()
                return self.coord.copy(dest_offset), dest_dir 

    def __repr__(self) -> str:
        return "< Line " + super().__repr__() + " >"

class Ring(Segment):

    def __init__(self, coord, clockwise=True, path3h=None, path6h=None, path9h=None, path12h=None):
        super().__init__(coord)
        self.clockwise = clockwise
        self.paths = [None] * 12
        self.paths[3] = path3h
        self.paths[6] = path6h
        self.paths[9] = path9h
        self.paths[0] = path12h

    def get_next_destination(self, offset, dir):
        next_offset = (offset + 1) % 12
        new_segment_offset = 0 if 1 < offset < 8 else 23
        new_segment_dir = Direction.FORWARD if 1 < offset < 8 else Direction.BACKWARD

        if self.clockwise and (self.paths[next_offset] is not None):
            return self.paths[next_offset].coord.copy(new_segment_offset), new_segment_dir 
        elif (not self.clockwise) and (self.paths[offset] is not None) :
            return self.paths[offset].coord.copy(new_segment_offset), new_segment_dir
        else:
            return self.coord.copy((offset+dir.delta()) % 12), dir

    def set_h(self, line, hour):
        hour %= 12
        if line is None:
            if self.paths[hour] is not None:
                if 3 <= hour <= 6:
                    self.paths[hour].entrance = None
                else:
                    self.paths[hour].exit = None            
        else:
            if 3 <= hour <= 6:
                line.entrance = self
            else:
                line.exit = self

        self.paths[hour] = line


    def set_12h(self, line):
        self.set_h(line,0)


    def set_3h(self, line):
        self.set_h(line,3)


    def set_6h(self, line):
        self.set_h(line,6)


    def set_9h(self, line):
        self.set_h(line,9)

    def __repr__(self) -> str:
        return "< Ring " + super().__repr__() + " >"
