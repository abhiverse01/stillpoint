from __future__ import annotations
import sys
import time
from contextlib import contextmanager
from typing import Iterable, Iterator, TypeVar, Optional

from .color import Gradient, DAWN
from .render import _Writer, render_progress_line, breathing_frame, quiet_frame

T = TypeVar("T")


class Bar:
    """A running progress indicator. Created via stillpoint() or StillPoint.track()."""

    def __init__(self, total: Optional[int], label: str = "", width: int = 28,
                 gradient: Gradient = DAWN, mode: str = "full", stream=None):
        self.total = total
        self.label = label
        self.width = width
        self.gradient = gradient
        self.mode = mode
        self.current = 0
        self.start_time = time.monotonic()
        self._writer = _Writer(stream)
        self._closed = False

    def _draw(self, force: bool = False) -> None:
        if self.total is None:
            line = breathing_frame(time.monotonic() - self.start_time, self.label, self.gradient)
        elif self.mode == "quiet":
            line = quiet_frame(self.current, self.total, time.monotonic() - self.start_time, self.gradient)
        else:
            line = render_progress_line(self.current, self.total, self.label,
                                         self.start_time, self.width, self.gradient)
        self._writer.write_line(line, force=force)

    def advance(self, n: int = 1) -> None:
        self.current += n
        self._draw()

    def set(self, current: int) -> None:
        self.current = current
        self._draw()

    def close(self) -> None:
        if not self._closed:
            self._draw(force=True)
            self._writer.finish()
            self._closed = True

    def __enter__(self) -> "Bar":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


class StillPoint:
    """Namespace for the library's entry points: track() and breathe()."""

    @staticmethod
    def track(total: Optional[int] = None, label: str = "", width: int = 28,
              gradient: Gradient = DAWN, mode: str = "full", stream=None) -> Bar:
        return Bar(total=total, label=label, width=width, gradient=gradient, mode=mode, stream=stream)

    @staticmethod
    @contextmanager
    def breathe(label: str = "waiting", gradient: Gradient = DAWN, stream=None) -> Iterator[Bar]:
        """For indeterminate waits — retries, network calls, anything with no known total."""
        bar = Bar(total=None, label=label, gradient=gradient, stream=stream)
        try:
            yield bar
        finally:
            bar.close()


def stillpoint(iterable: Iterable[T], label: str = "", width: int = 28,
               gradient: Gradient = DAWN, mode: str = "full", stream=None) -> Iterator[T]:
    """Wrap any iterable. Total is inferred via len() when available."""
    try:
        total = len(iterable)  # type: ignore
    except TypeError:
        total = None
    bar = Bar(total=total, label=label, width=width, gradient=gradient, mode=mode, stream=stream)
    try:
        for item in iterable:
            yield item
            bar.advance()
    finally:
        bar.close()


stillpoint.track = StillPoint.track  # type: ignore[attr-defined]
stillpoint.breathe = StillPoint.breathe  # type: ignore[attr-defined]
