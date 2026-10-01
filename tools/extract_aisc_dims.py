"""Extract imperial section dimensions (inches) from the AISC Shapes Database v16
as bundled in the MIT-licensed `efficalc` package, into data/aisc_dimensions.json.

Usage:  pip install efficalc && python tools/extract_aisc_dims.py
"""
import importlib.util
import json
import pathlib
import sqlite3

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "aisc_dimensions.json"
# locate the bundled database without importing efficalc (avoids its runtime deps)
DB = pathlib.Path(importlib.util.find_spec("efficalc").submodule_search_locations[0]) / "sections" / "section_properties.db"

# family code -> (table, {output key: db column})
FAMILIES = {
    "I": ("aisc_wide_flange", {"d": "d", "bf": "bf", "tf": "tf", "tw": "tw", "k": "kdes", "k1": "k1"}),
    "C": ("aisc_channel", {"d": "d", "bf": "bf", "tf": "tf", "tw": "tw", "k": "kdes", "x": "x"}),
    "T": ("aisc_tee", {"d": "d", "bf": "bf", "tf": "tf", "tw": "tw", "k": "kdes", "y": "y"}),
    "L": ("aisc_angle", {"d": "d", "b": "b", "t": "t", "k": "kdes", "x": "x", "y": "y"}),
    "R": ("aisc_rectangular", {"h": "Ht", "b": "Bout", "t": "tdes", "tn": "tnom"}),
    "O": ("aisc_circular", {"od": "OD", "t": "tdes", "tn": "tnom"}),
}


def main():
    con = sqlite3.connect(DB)
    out = {}
    for fam, (table, cols) in FAMILIES.items():
        sql = f"select AISC_name, {', '.join(cols.values())} from {table}"
        for name, *vals in con.execute(sql):
            out[name.upper()] = {"f": fam, **{k: v for k, v in zip(cols, vals) if v is not None}}
    lines = [f"{json.dumps(k)}:{json.dumps(v, separators=(',', ':'))}" for k, v in sorted(out.items())]
    OUT.write_text("{\n" + ",\n".join(lines) + "\n}\n", encoding="utf-8")
    print(f"Wrote {len(out)} shapes to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
