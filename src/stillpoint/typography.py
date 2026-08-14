"""Numbers set with the same care as the rest of the line — not f'{i}/{n}'."""

from __future__ import annotations

THIN_SPACE = "\u2009"
EN_DASH = "\u2013"


def aligned_count(current: int, total: int) -> str:
    """Right-aligned, fixed-width count so digits don't jitter the line as they grow."""
    width = len(str(total))
    return f"{current:>{width}}{THIN_SPACE}{EN_DASH}{THIN_SPACE}{total}"


def percent(current: int, total: int) -> str:
    if total <= 0:
        return "  0%"
    pct = round((current / total) * 100)
    return f"{pct:>3}%"


def elapsed(seconds: float) -> str:
    """Quiet, minute:second timestamp — no milliseconds screaming for attention."""
    m, s = divmod(int(seconds), 60)
    h, m = divmod(m, 60)
    if h:
        return f"{h}:{m:02}:{s:02}"
    return f"{m}:{s:02}"

def label_line(label: str, current: int, total: int, elapsed_s: float) -> str:
    parts = [label.strip(), aligned_count(current, total), percent(current, total), elapsed(elapsed_s)]
    return (THIN_SPACE * 2).join(p for p in parts if p)
