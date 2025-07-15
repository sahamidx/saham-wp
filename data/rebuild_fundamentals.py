import json
import os

# Path data input
BASE_DIR = os.path.dirname(__file__)
FUND_PATH = os.path.join(BASE_DIR, "fundamental.json")
STATIC_PATH = os.path.join(BASE_DIR, "static_info.json")
OUTPUT_DIR = os.path.join(BASE_DIR, "data", "fundamentals")

# Load data
with open(FUND_PATH, encoding="utf-8") as f:
    fundamentals = json.load(f)

with open(STATIC_PATH, encoding="utf-8") as f:
    static_info = json.load(f)

# Siapkan lookup berdasarkan kode
lookup = {item["kode"]: item for item in static_info}

# Pastikan output folder ada
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Patch dan tulis ulang
for emiten in fundamentals:
    kode = emiten["kode"].upper()
    static = lookup.get(kode, {})

    emiten["nama"] = static.get("nama", "Nama Perusahaan")
    emiten["sektor"] = static.get("sektor", "Sektor")
    emiten["subsektor"] = static.get("subsektor", "Subsektor")
    emiten["ipo_date"] = static.get("ipo_date", "2000-01-01")

    out_path = os.path.join(OUTPUT_DIR, f"{kode}.json")
    with open(out_path, "w", encoding="utf-8") as out_file:
        json.dump(emiten, out_file, indent=2, ensure_ascii=False)

print("✅ Semua file JSON sudah diperbarui.")
