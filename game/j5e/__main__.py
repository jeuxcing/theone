import signal, sys

from j5e.Hypervisor import Hypervisor
from j5e.hardware.led_strip import GridDims
import time




def signal_handler(sig, frame):
    print("\nGame closing")
    global hypervisor
    hypervisor.stop()
    sys.exit(0)



def test(grid):
    last_step = time.time()
    for i in range(1000):
        for seg_idx in range(4):
            for led_idx in range(12):
                # print(time.time() % 1., "light")
                grid.set_segment(GridDims.ROW, 0, seg_idx, led_idx, 23-led_idx, (30, 0, 0))
                delay = time.time() - last_step
                # print(delay)
                # waiting_time = .03
                waiting_time = .25
                time.sleep(waiting_time - min(delay, waiting_time))
                last_step = time.time()
                # print(time.time() % 1., "dark")
                grid.set_segment(GridDims.ROW, 0, seg_idx, led_idx, 23-led_idx, (0, 0, 0))


if __name__ == "__main__":
    global hypervisor
    signal.signal(signal.SIGINT, signal_handler)

    hypervisor = Hypervisor()
    hypervisor.start()
    print("Game started")
    test(hypervisor.grid)

    signal.pause()


hypervisor = None
