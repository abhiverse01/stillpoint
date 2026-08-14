"""The actual drawing. Every frame is time-driven, not tick-driven —
so motion stays smooth regardless of how fast the underlying work runs."""

from __future__ import annotations
import sys
import time
from .color import Gradient, ease_in_out, RESET, DIM, DAWN
from .typography import label_line

FULL = "█"
SOFT_BLOCKS = " ▁▂▃▄▅▆▇█"  # sub-character resolution — the leading edge feels soft, not stepped
QUIET_GLYPHS = "◜◠◝◞◡◟"  # a single evolving glyph, for quiet mode
BREATH_FRAMES = "·∘○◯○∘"  # inhale / exhale


class _Writer:
    """Wraps stdout so the bar can redraw a single line in place."""

    def __init__(self, stream=None, min_interval: float = 1 / 30):
        self.stream = stream or sys.stdout
        self.min_interval = min_interval
        self._last_write = 0.0
        self._last_len = 0

    def write_line(self, text: str, force: bool = False) -> None:
        now = time.monotonic()
        if not force and (now - self._last_write) < self.min_interval:
            return
        self._last_write = now
        pad = max(0, self._last_len - len(_strip_ansi(text)))
        self.stream.write("\r" + text + (" " * pad))
        self.stream.flush()
        self._last_len = len(_strip_ansi(text))

    def finish(self) -> None:
        self.stream.write("\n")
        self.stream.flush()


def _strip_ansi(s: str) -> str:
    out, in_esc = [], False
    for ch in s:
        if ch == "\033":
            in_esc = True
            continue
        if in_esc:
            if ch.isalpha():
                in_esc = False
            continue
        out.append(ch)
    return "".join(out)


def render_bar(fraction: float, width: int, gradient: Gradient) -> str:
    """A gradient-filled bar with a soft (sub-character) leading edge."""
    fraction = max(0.0, min(1.0, fraction))
    filled_exact = fraction * width
    filled_full = int(filled_exact)
    remainder = filled_exact - filled_full

    chars = []
    for i in range(width):
        t = (i + 0.5) / max(width, 1)
        color = gradient.ansi_fg(t)
        if i < filled_full:
            chars.append(f"{color}{FULL}{RESET}")
        elif i == filled_full and remainder > 0:
            idx = max(1, round(remainder * (len(SOFT_BLOCKS) - 1)))
            chars.append(f"{color}{SOFT_BLOCKS[idx]}{RESET}")
        else:
            chars.append(f"{DIM}{SOFT_BLOCKS[1]}{RESET}")
    return "".join(chars)


def render_progress_line(current: int, total: int, label: str, start_time: float,
                          width: int, gradient: Gradient) -> str:
    fraction = current / total if total else 0.0
    bar = render_bar(fraction, width, gradient)
    text = label_line(label, current, total, time.monotonic() - start_time)
    return f"{bar}  {text}"


def breathing_frame(t: float, label: str, gradient: Gradient = DAWN) -> str:
    """t is any monotonically increasing value in seconds — breathing has no 'total'."""
    cycle = 4.0  # seconds per inhale+exhale
    phase = (t % cycle) / cycle
    eased = ease_in_out(phase if phase < 0.5 else 1 - phase)
    idx = min(len(BREATH_FRAMES) - 1, round(eased * (len(BREATH_FRAMES) - 1)) + (len(BREATH_FRAMES) // 2 if phase >= 0.5 else 0))
    idx = max(0, min(len(BREATH_FRAMES) - 1, idx))
    glyph = BREATH_FRAMES[idx]
    color = gradient.ansi_fg(eased)
    return f"{color}{glyph}{RESET}  {DIM}{label}{RESET}"


def quiet_frame(current: int, total: int, t: float, gradient: Gradient = DAWN) -> str:
    """A single evolving glyph — for people who find bars distracting."""
    fraction = current / total if total else 0.0
    idx = min(len(QUIET_GLYPHS) - 1, int(fraction * (len(QUIET_GLYPHS) - 1)))
    glyph = QUIET_GLYPHS[idx]
    color = gradient.ansi_fg(fraction)
    return f"{color}{glyph}{RESET}"
