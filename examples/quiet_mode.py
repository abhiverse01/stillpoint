import time
from stillpoint import stillpoint

for _ in stillpoint(range(40), label="processing", mode="quiet"):
    time.sleep(0.03)
