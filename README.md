# Steel Size Rolodex

A single-page lookup for structural steel sections with metric and imperial designations side by side.

Type a size and press **Enter**. The list snaps to the closest match, so near-miss numbers from different suppliers still land in the right place. For example, `W310x29` snaps to **W310X28 = W12X19**. Scroll the wheel to see nearby sizes.

- Accepts metric or imperial input: `W310x28`, `W12x19`, `HSS4x4x1/4`, `L102x102x12.7`, `Pipe 4 STD`
- Spaces, `x`, `×` and `*` all work as separators, and case doesn't matter
- **↑ / ↓** in the search box step one size at a time; clicking a row snaps to it
- Shows weight and perimeter under the section dimensions
- **Imperial / Metric** switch on the diagram swaps every dimension, weight and perimeter between inches (lb/ft) and millimetres (kg/m); metric dimensions are converted from the AISC inch values
- Draws the selected section to scale with imperial dimensions (d, bf, tf, tw, k, k1 for beams; legs and thickness for angles; size and wall for HSS and pipe)
- **Banana for scale**: a switch at the bottom of the page adds a 7" banana beside the section, drawn at the same scale (remembered in your browser)
- Types covered: W, M, S, HP, C, MC, L, WT, HSS, Pipe (1,411 sizes)

## Updating the size table

The data is embedded in `index.html` and generated from two files:

- `data/Material_Database.xlsx`: the size list (columns: Type, Label (Metric), Label (Imperial), W (kg/m), Perimeter (mm))
- `data/aisc_dimensions.json`: section dimensions in inches, keyed by AISC name

```bash
pip install openpyxl
python tools/build_data.py
```

The dimensions come from the AISC Shapes Database v16, as bundled in the MIT-licensed
[efficalc](https://pypi.org/project/efficalc/) package. To regenerate them:

```bash
pip install efficalc
python tools/extract_aisc_dims.py
```

## How matching works

The input is split into section type and dimensions (fractions like `1-3/8` are understood), then compared against both the metric and imperial label of every size of that type. The first dimension (nominal depth or size) carries the most weight, and the size with the smallest relative difference wins.
