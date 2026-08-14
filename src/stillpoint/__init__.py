"""stillpoint — a calm, typographically considered progress indicator.

    from stillpoint import stillpoint

    for item in stillpoint(range(100), label="training"):
        ...

    with stillpoint.track(total=100, label="download") as bar:
        for chunk in chunks:
            download(chunk)
            bar.advance()

    with stillpoint.breathe(label="waiting for response"):
        slow_network_call()
"""

from .core import stillpoint, StillPoint, Bar
from .color import Gradient, DAWN, DUSK, MOSS

__version__ = "0.1.0"
__all__ = ["stillpoint", "StillPoint", "Bar", "Gradient", "DAWN", "DUSK", "MOSS"]
