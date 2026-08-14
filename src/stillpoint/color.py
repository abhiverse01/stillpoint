"""Soft, continuous color — the opposite of a hard-edged '#' block."""

from __future__ import annotations
import math


def _hex_to_rgb(h: str) -> tuple[int, int, int]:
    h = h.lstrip("#")
    return tuple(int(h[i : i + 2], 16) for i in (0, 2, 4))  # type: ignore


def _lerp(a: float, b: float, t: float) -> float:
    return a + (b - a) * t


def ease_in_out(t: float) -> float:
    """Cosine easing — no linear, mechanical motion."""
    return 0.5 - 0.5 * math.cos(math.pi * max(0.0, min(1.0, t)))


class Gradient:
    """A smooth multi-stop gradient, sampled at any point t in [0, 1]."""

    def __init__(self, stops: list[str]):
        self.stops = [_hex_to_rgb(s) for s in stops]

    def sample(self, t: float) -> tuple[int, int, int]:
        t = max(0.0, min(1.0, t))
        n = len(self.stops) - 1
        if n <= 0:
            return self.stops[0]
        segment = min(int(t * n), n - 1)
        local_t = (t * n) - segment
        c0, c1 = self.stops[segment], self.stops[segment + 1]
        return tuple(round(_lerp(c0[i], c1[i], local_t)) for i in range(3))  # type: ignore

    def ansi_fg(self, t: float) -> str:
        r, g, b = self.sample(t)
        return f"\033[38;2;{r};{g};{b}m"


RESET = "\033[0m"
DIM = "\033[2m"
HIDE_CURSOR = "\033[?25l"
SHOW_CURSOR = "\033[?25h"

# Default palettes — quiet, low-saturation, dusk-toned.
DAWN = Gradient(["#3A4A5C", "#8FA6A0", "#D8C7A1"])
DUSK = Gradient(["#2B2540", "#7A5C7E", "#C98F8F"])
MOSS = Gradient(["#2E3B32", "#5E7C63", "#B7C9A8"])
