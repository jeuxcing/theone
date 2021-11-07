from j5e.hardware.led_strip import Grid, GridDims
from threading import Thread

class Game(Thread):
    def __init__(self, grid):
        super().__init__()
        self.grid = grid
        self.ended = False


    def run(self):
        while not self.ended:
            for line_idx in range(Grid.SIZE):
                for seg_idx in range(Grid.SIZE-1):
                    for led_idx in range(24):
                        if self.ended:
                            break
                        self.grid.set_color(GridDims.ROW, line_idx, seg_idx, led_idx, (0, 40, 0))
                        self.grid.set_color(GridDims.COL, line_idx, seg_idx, led_idx, (0, 40, 0))
                        self.grid.set_color(GridDims.RING, line_idx, seg_idx, led_idx//2, (0, 40, 0))
                        time.sleep(0.3)
                        self.grid.set_color(GridDims.ROW, line_idx, seg_idx, led_idx, (0, 0, 0))
                        self.grid.set_color(GridDims.COL, line_idx, seg_idx, led_idx, (0, 0, 0))
                        self.grid.set_color(GridDims.RING, line_idx, seg_idx, led_idx//2, (0, 0, 0))


    def stop(self):
        self.ended = True
