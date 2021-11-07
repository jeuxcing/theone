from enum import Enum
import time


class Strip:
    def __init__(self, size):
        self.leds = [(0, 0, 0) for _ in range(size)]
        # valeurs dans [0,255]

    def set_color(self, pos, rgb):
        self.leds[pos] = rgb

    def get_color(self, pos):
        return self.leds[pos]

    def get_all_colors(self, pos):
        return self.leds

    def set_color_all(self, rgb):
        self.leds = [rgb for _ in range(len(self.leds))]

    def set_all_colors(self, rgb_colors):
        self.leds = rgb_colors


class Segment(Strip):
    NB_LEDS = 24

    def __init__(self, size=0):
        """
        size : taille du bandeau
        """
        super(Segment, self).__init__(size if size != 0 else Segment.NB_LEDS)


class Ring(Strip):
    NB_LEDS = 12

    def __init__(self, size=0):
        """
        size : taille de l'anneau
        """
        super(Ring, self).__init__(size if size != 0 else Ring.NB_LEDS)


class GridDims(Enum):
    ROW = ord('H') # H ascii
    COL = ord('V') # V ascii
    RING = ord('R') # R ascii


class Grid:
    SIZE = 5
    # NB_SEGMENTS = Grid.SIZE - 1

    def __init__(self, network, size=0):
        """
        size : taille de la grille
        """
        if size == 0:
            size = Grid.SIZE
        nb_segments = size - 1

        self.rows = [
            [Segment() for _ in range(nb_segments)] for _ in range(size)
        ]
        self.cols = [
            [Segment() for _ in range(nb_segments)] for _ in range(size)
        ]
        self.rings = [[Ring() for _ in range(size)] for _ in range(size)]

        self.segments = {
            GridDims.ROW : self.rows,
            GridDims.COL : self.cols,
            GridDims.RING : self.rings
        }

        self.network = network


    def set_color(self, dimension, line_idx, segment_idx, led_idx, rgb):
        self.network.wall.send_msg(
            bytes([ord('L'), dimension.value, line_idx, segment_idx, led_idx] + list(rgb))
        )
        self.segments[dimension][line_idx][segment_idx].set_color(led_idx, rgb)


    def set_segment(self, dimension, line_idx, segment_idx, led_start_idx, led_stop_idx, rgb):
        self.network.wall.send_msg(
            bytes([ord('S'), dimension.value, line_idx, segment_idx, led_start_idx, led_stop_idx] + list(rgb))
        )
        for led_idx in range(led_start_idx, led_stop_idx+1):
            self.segments[dimension][line_idx][segment_idx].set_color(led_idx, rgb)


    def get_color(self, dimension, line_idx, segment_idx, led_idx):
        return self.segments[dimension][line_idx][segment_idx].get_color(led_idx)


    def run_test(self):
        for line_idx in range(Grid.SIZE):
            for seg_idx in range(Grid.SIZE-1):
                for led_idx in range(24):
                    self.set_color(GridDims.ROW, line_idx, seg_idx, led_idx, (0, 40, 0))
                    self.set_color(GridDims.COL, line_idx, seg_idx, led_idx, (0, 40, 0))
                    self.set_color(GridDims.RING, line_idx, seg_idx, led_idx//2, (0, 40, 0))
                    time.sleep(0.1)
                    self.set_color(GridDims.ROW, line_idx, seg_idx, led_idx, (0, 0, 0))
                    self.set_color(GridDims.COL, line_idx, seg_idx, led_idx, (0, 0, 0))
                    self.set_color(GridDims.RING, line_idx, seg_idx, led_idx//2, (0, 0, 0))

    