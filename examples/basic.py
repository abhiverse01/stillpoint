import time
from stillpoint import stillpoint

for _ in stillpoint(range(40), label="processing"):
    time.sleep(0.03)
