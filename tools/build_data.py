"""Regenerate the embedded size table in index.html from data/Material_Database.xlsx,
joined with imperial dimensions from data/aisc_dimensions.json (see extract_aisc_dims.py).

Usage:  pip install openpyxl && python tools/build_data.py
"""
import json
import pathlib
import re

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parent.parent
XLSX = ROOT / "data" / "Material_Database.xlsx"
HTML = ROOT / "index.html"
DIMS = ROOT / "data" / "aisc_dimensions.json"
TYPES = ["PIPE", "HSS", "WT", "MC", "HP", "W", "M", "S", "C", "L"]


def num(v):
    if v is None:
        return None
    v = round(float(v), 2)
    return int(v) if v == int(v) else v


def to_num(s):
    """'12.7', '3/4', '1-3/8' -> float"""
    whole, _, frac = s.rpartition("-") if "/" in s else ("", "", s)
    if "/" in frac:
        n, d = frac.split("/")
        return (float(whole) if whole else 0) + float(n) / float(d)
    return float(frac)


def key(label):
    """Label -> comparable key, so 'HSS20.000X1/2' and 'HSS20.000X0.500' match."""
    s = label.upper().replace(" ", "")
    t = next((t for t in TYPES if s.startswith(t)), "")
    if t == "PIPE":
        return s
    try:
        return (t,) + tuple(round(to_num(n), 2) for n in s[len(t):].split("X") if n)
    except ValueError:
        return s


def main():
    dims = {key(k): v for k, v in json.loads(DIMS.read_text(encoding="utf-8")).items()}
    ws = openpyxl.load_workbook(XLSX, data_only=True).active
    rows = []
    for t, metric, imperial, kgm, perim in ws.iter_rows(min_row=2, values_only=True):
        if not t or not metric:
            continue
        imperial = (imperial or "").strip()
        rows.append([str(t).strip(), str(metric).strip(), imperial, num(kgm), num(perim),
                     dims.get(key(imperial)) if imperial else None])

    blob = "/*DATA_START*/" + json.dumps(rows, separators=(",", ":")) + "/*DATA_END*/"
    html = HTML.read_text(encoding="utf-8")
    html, n = re.subn(r"/\*DATA_START\*/.*?/\*DATA_END\*/", lambda _: blob, html, flags=re.S)
    if n != 1:
        raise SystemExit("DATA markers not found in index.html")
    HTML.write_text(html, encoding="utf-8")
    missing = [r[2] or r[1] for r in rows if not r[5]]
    print(f"Embedded {len(rows)} sizes into {HTML.name} ({len(rows) - len(missing)} with dimensions)")
    if missing:
        print("  no dimensions:", ", ".join(missing))


if __name__ == "__main__":
    main()
