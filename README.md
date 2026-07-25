# MagTile Circuits

Snap-together **magnetic circuit tiles** — every component (resistor, capacitor,
logic gate, LED) lives inside the smallest 1×1 magnetic square, and the magnets do
double duty: they hold the tiles together *and* carry the current. Dedicated
straight / elbow / T wire-tiles route the nets, so the circuit you snap together
keeps the same floorplan as the schematic on paper.

The guide builds up from a plain RC, to a Schmitt-trigger inverter, to a complete
**LED that blinks once per second** on a single 3 V CR2032 coin cell.

## 📖 Live build guide

**https://borenw.github.io/magtile-circuits/**

Part of [Bo's Engineering Curriculum](https://borenw.github.io/) — **Page 37**.

## The blinker

A single `74LVC1G14` Schmitt-trigger inverter wired as an astable RC oscillator:

- **R1 = 120 kΩ** feedback (output → input)
- **C1 = 10 µF** on the input node
- **R2 = 330 Ω** current-limits a red LED off the output
- **V = 3 V** (CR2032) → period `T ≈ τ·k ≈ 1.20 s × 0.83 ≈ 1.0 s` → ~1 Hz blink

## Layout

| Path              | Purpose                                            |
|-------------------|----------------------------------------------------|
| `docs/index.html` | The build guide (served by GitHub Pages)           |
| `README.md`       | This file                                          |

GitHub Pages is served from the `docs/` folder on the default branch.
