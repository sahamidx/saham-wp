#!/usr/bin/env python3
"""
Validasi data fundamental saham dari folder data/fundamentals/
Hasil disimpan di folder data/validation/
"""

import os, json

FUNDAMENTAL_DIR = "../data/fundamentals"
VALIDATION_DIR = "../data/validation"

# Batas validasi kasar
def is_outlier(data):
    def safe_gt(val, limit):   # safe "greater than"
        return val is not None and val > limit

    def safe_lt(val, limit):   # safe "less than"
        return val is not None and val < limit

    return {
        "per": safe_gt(data.get("per"), 100),
        "pbv": safe_gt(data.get("pbv"), 20),
        "eps": safe_lt(data.get("eps"), -1000) or safe_gt(data.get("eps"), 10000),
        "dividen_yield": safe_gt(data.get("dividen_yield"), 25),
        "market_cap": safe_lt(data.get("market_cap"), 1e12) or safe_gt(data.get("market_cap"), 5e15),
    }

def validate_file(filepath):
    with open(filepath, "r") as f:
        data = json.load(f)
    
    kode = data.get("kode", "UNKNOWN")
    outliers = is_outlier(data)

    result = {
        "kode": kode,
        "outliers": outliers
    }

    # Simpan hasil validasi
    os.makedirs(VALIDATION_DIR, exist_ok=True)
    out_path = os.path.join(VALIDATION_DIR, f"{kode}_validation.json")
    with open(out_path, "w") as f:
        json.dump(result, f, indent=2)

    print(f"Validated {kode} → {out_path}")

def main():
    if not os.path.exists(FUNDAMENTAL_DIR):
        print("Folder data/fundamentals/ tidak ditemukan.")
        return

    files = [f for f in os.listdir(FUNDAMENTAL_DIR) if f.endswith(".json")]

    if not files:
        print("Tidak ada file JSON di folder fundamental.")
        return

    for fname in files:
        fpath = os.path.join(FUNDAMENTAL_DIR, fname)
        validate_file(fpath)

    print("✅ Semua data telah divalidasi.")

if __name__ == "__main__":
    main()
