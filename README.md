# Steel Size Rolodex

A single-page lookup for structural steel sections with metric and imperial designations side by side.

Type a size and press **Enter**. The list snaps to the closest match, so near-miss numbers from different suppliers still land in the right place. For example, `W310x29` snaps to **W310X28 = W12X19**. Scroll the wheel to see nearby sizes.

- Accepts metric or imperial input: `W310x28`, `W12x19`, `HSS4x4x1/4`, `L102x102x12.7`, `Pipe 4 STD`
- Spaces, `x`, `×` and `*` all work as separators, and case doesn't matter
- **↑ / ↓** in the search box step one size at a time; clicking a row snaps to it
- Shows mass (kg/m and lb/ft) and perimeter (mm and in) for the selected size
- Types covered: W, M, S, HP, C, MC, L, WT, HSS, Pipe (1,411 sizes)

## Use it

Open `index.html` in any browser. It's one self-contained file with no build step or server.

To host it on **GitHub Pages**, push this repo, then go to *Settings → Pages* and set the source to the `main` branch, root folder.

## Updating the size table

The data is embedded in `index.html` and generated from `data/Material_Database.xlsx`
(columns: Type, Label (Metric), Label (Imperial), W (kg/m), Perimeter (mm)).

```bash
pip install openpyxl
python tools/build_data.py
```

## How matching works

The input is split into section type and dimensions (fractions like `1-3/8` are understood), then compared against both the metric and imperial label of every size of that type. The first dimension (nominal depth or size) carries the most weight, and the size with the smallest relative difference wins.
