import os

DIGIT_COLOR = ["Black", "Brown", "Red", "Orange", "Yellow",
               "Green", "Blue", "Violet", "Grey", "White"]

E12 = [1.0, 1.2, 1.5, 1.8, 2.2, 2.7, 3.3, 3.9, 4.7, 5.6, 6.8, 8.2]

def display_value(ohms):
    if ohms < 1000:
        return f"{ohms:g} \u03a9"
    elif ohms < 1_000_000:
        return f"{ohms/1000:g} k\u03a9"
    else:
        return f"{ohms/1_000_000:g} M\u03a9"

def slugify(label):
    return label.replace("\u03a9", "ohm").lower().replace(" ", "-").replace(".", "-")

# --- Step 1: build the full list of rows first, so we can sort it
# and link each row to its neighbors before writing any files.
rows = []
for exp in range(0, 7):
    for base in E12:
        ohms = round(base * (10 ** exp), 6)
        sig2 = round(base * 10)
        d1, d2 = sig2 // 10, sig2 % 10
        mult_exp = exp - 1
        if 0 <= mult_exp <= 9:
            multiplier = DIGIT_COLOR[mult_exp]
        elif mult_exp == -1:
            multiplier = "Gold"
        else:
            multiplier = "Silver"

        label = display_value(ohms)
        rows.append({
            "ohms": ohms,
            "label": label,
            "slug": slugify(label),
            "decade_exp": exp,
            "band1": DIGIT_COLOR[d1],
            "band2": DIGIT_COLOR[d2],
            "multiplier": multiplier,
        })

# --- Step 2: sort numerically by resistance (this fixes the
# alphabetical-sorting problem from the hub page)
rows.sort(key=lambda r: r["ohms"])

# --- Step 3: now that rows are in true numeric order, each row's
# neighbors in the list ARE its prev/next resistor value
for i, r in enumerate(rows):
    r["prev_slug"] = rows[i - 1]["slug"] if i > 0 else ""
    r["prev_label"] = rows[i - 1]["label"] if i > 0 else ""
    r["next_slug"] = rows[i + 1]["slug"] if i < len(rows) - 1 else ""
    r["next_label"] = rows[i + 1]["label"] if i < len(rows) - 1 else ""

# --- Step 4: write the files
os.makedirs("content/resistors", exist_ok=True)
for r in rows:
    content = f"""---
title: "{r['label']} Resistor Color Code"
resistance_label: "{r['label']}"
resistance_ohms: {r['ohms']}
decade_exp: {r['decade_exp']}
band1: "{r['band1']}"
band2: "{r['band2']}"
multiplier: "{r['multiplier']}"
tolerance: "Gold"
tolerance_pct: "\u00b15%"
prev_slug: "{r['prev_slug']}"
prev_label: "{r['prev_label']}"
next_slug: "{r['next_slug']}"
next_label: "{r['next_label']}"
---
"""
    path = f"content/resistors/{r['slug']}.md"
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)

print(f"Wrote {len(rows)} resistor pages.")