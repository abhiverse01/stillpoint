# stillpoint

A progress indicator built for calm, not urgency.

Every terminal progress library — `tqdm`, `rich`, `alive-progress` — is built
to grab attention: hard `#` blocks, frantic refresh rates, spinners that
never stop moving. `stillpoint` is the opposite bet: a gradient-filled bar
with a soft leading edge, motion paced by an easing curve instead of your
CPU's refresh rate, and typography set with the same care you'd give a
printed page.

```
▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▓▒░  training   34 – 40   88%   0:04
```

## Install

```bash
pip install stillpoint-bar
```

## Use

```python
from stillpoint import stillpoint

for item in stillpoint(range(100), label="training"):
    train_step(item)
```

Context-manager form, when you need to advance manually:

```python
with stillpoint.track(total=100, label="download") as bar:
    for chunk in chunks:
        download(chunk)
        bar.advance()
```

Indeterminate waits get a breathing glyph instead of a fake percentage:

```python
with stillpoint.breathe(label="waiting for response"):
    slow_network_call()
```

Quiet mode, for people who find bars distracting — a single evolving glyph:

```python
for item in stillpoint(data, mode="quiet"):
    ...
```

## Palettes

Three built-in gradients — `DAWN` (default), `DUSK`, `MOSS` — or pass your
own via `stillpoint.Gradient(["#hex1", "#hex2", ...])`.

## Design notes

- No dependencies beyond the standard library.
- Frames are time-driven, not tick-driven, so a tight loop doesn't flood
  your terminal — updates are capped to ~30fps regardless of iteration speed.
- Numbers are right-aligned and spaced so the line doesn't jitter as digit
  counts change.

## License

MIT — see `LICENSE`.
