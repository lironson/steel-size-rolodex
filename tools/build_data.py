"""Regenerate the embedded size table in index.html from data/Material_Database.xlsx.

Usage:  pip install openpyxl && python tools/build_data.py
"""
import json
import pathlib
import re

import openpyxl

ROOT = pathlib.Path(__file__).resolve().parent.parent
XLSX = ROOT / "data" / "Material_Database.xlsx"
HTML = ROOT / "index.html"


def num(v):
    if v is None:
        return None
    v = round(float(v), 2)
    return int(v) if v == int(v) else v


def main():
    ws = openpyxl.load_workbook(XLSX, data_only=True).active
    rows = []
    for t, metric, imperial, kgm, perim in ws.iter_rows(min_row=2, values_only=True):
        if not t or not metric:
            continue
        rows.append([str(t).strip(), str(metric).strip(), (imperial or "").strip(), num(kgm), num(perim)])

    blob = "/*DATA_START*/" + json.dumps(rows, separators=(",", ":")) + "/*DATA_END*/"
    html = HTML.read_text(encoding="utf-8")
    html, n = re.subn(r"/\*DATA_START\*/.*?/\*DATA_END\*/", lambda _: blob, html, flags=re.S)
    if n != 1:
        raise SystemExit("DATA markers not found in index.html")
    HTML.write_text(html, encoding="utf-8")
    print(f"Embedded {len(rows)} sizes into {HTML.name}")


if __name__ == "__main__":
    main()
