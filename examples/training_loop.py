import time
from stillpoint import stillpoint, DUSK

# A determinate run, styled with the dusk gradient.
with stillpoint.track(total=200, label="epoch 1/5", gradient=DUSK) as bar:
    for step in range(200):
        time.sleep(0.01)
        bar.advance()

# An indeterminate wait — no total, so it breathes instead of faking progress.
with stillpoint.breathe(label="waiting for checkpoint upload"):
    time.sleep(2)
