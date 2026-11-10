#!/usr/bin/env python3
"""Write themes/kanagawa-<variant> from the shared palette.

Usage: scripts/generate.py [path/to/palette.json]   (default: ../.github/palette.json)
"""
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
VARIANTS = ["wave", "dragon", "lotus"]


def roles(variant):
    """Map each role to its hex color; a role missing from the palette raises KeyError later."""
    return {role: c["hex"] for c in variant["colors"].values() for role in c["usage"]}

# Variable -> palette role. The variables are named by role, so a bar block or
# other config can use them after the include.
VARS = {
    "kanagawa_bg": "ui.bg",
    "kanagawa_bg_dark": "ui.bg_m3",
    "kanagawa_bg_light": "ui.bg_p1",
    "kanagawa_bg_select": "ui.bg_p2",
    "kanagawa_fg": "ui.fg",
    "kanagawa_fg_dim": "ui.fg_dim",
    "kanagawa_accent": "syn.fun",
    "kanagawa_indicator": "syn.special1",
    "kanagawa_urgent": "diag.error",
    "kanagawa_warning": "diag.warning",
}
# client class -> border, background, text, indicator, child_border.
# focused_tab_title takes only the first three.
CLIENTS = {
    "focused": ["accent", "bg_select", "fg", "indicator", "accent"],
    "focused_inactive": ["bg_select", "bg_light", "fg_dim", "bg_select", "bg_select"],
    "focused_tab_title": ["bg_select", "bg_light", "fg"],
    "unfocused": ["bg_dark", "bg_dark", "fg_dim", "bg_dark", "bg_dark"],
    "urgent": ["urgent", "urgent", "bg", "urgent", "urgent"],
    "placeholder": ["bg", "bg", "fg", "bg", "bg"],
}


def theme(variant, colors):
    out = [f"# Kanagawa {variant.capitalize()}", "# https://github.com/kanagawa-community/sway", ""]
    out += [f"set ${k} {colors[r]}" for k, r in VARS.items()]
    out.append("")
    out += [f"client.{c:<17} " + " ".join(f"$kanagawa_{x}" for x in xs) for c, xs in CLIENTS.items()]
    out.append("client.background $kanagawa_bg")
    return "\n".join(out) + "\n"


def main():
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT.parent / ".github" / "palette.json"
    variants = json.loads(path.read_text())["variants"]
    for v in VARIANTS:
        out = ROOT / "themes" / f"kanagawa-{v}"
        out.parent.mkdir(exist_ok=True)
        out.write_text(theme(v, roles(variants[v])))
        print(out.relative_to(ROOT))


if __name__ == "__main__":
    main()
