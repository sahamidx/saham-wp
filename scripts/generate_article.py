#!/usr/bin/env python3
"""
Render artikel saham dari template_emiten.html
- Ambil dari data/fundamentals/*.json
- Ambil validasi dari data/validation/*.json (opsional)
- Render HTML ke output/{kode}.html
"""

import os
import json
from jinja2 import Environment, FileSystemLoader

# Path absolut dari root proyek
FUND_DIR = "data/fundamentals"
VALID_DIR = "data/validation"
TEMPLATE_DIR = "templates"
OUTPUT_DIR = "output"

# Setup Jinja2
env = Environment(loader=FileSystemLoader(TEMPLATE_DIR))

# Tambahkan filter ribuan (comma)
env.filters['comma'] = lambda x: f"{x:,}".replace(",", ".") if isinstance(x, (int, float)) else x

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def render_article(kode):
    kode = kode.upper()
    fund_path = os.path.join(FUND_DIR, f"{kode}.json")
    valid_path = os.path.join(VALID_DIR, f"{kode}_validation.json")
    output_path = os.path.join(OUTPUT_DIR, f"{kode}.html")

    # Cek file wajib
    if not os.path.exists(fund_path):
        print(f"❌ Data tidak ditemukan untuk {kode}")
        return

    # Load data
    fund = load_json(fund_path)
    validation = load_json(valid_path) if os.path.exists(valid_path) else {}

    # Pastikan semua field penting terisi
    fund.setdefault("nama", "Nama Perusahaan")
    fund.setdefault("sektor", "Sektor")
    fund.setdefault("subsektor", "Subsektor")
    fund.setdefault("ipo_date", "2000-01-01")
    fund.setdefault("dividen_history", [])
    fund.setdefault("trend", "Naik")
    fund.setdefault("avg_volume", 50000000)
    fund.setdefault("support", int(fund.get("harga", 0) * 0.9))
    fund.setdefault("resistance", int(fund.get("harga", 0) * 1.1))

    # Render HTML
    template = env.get_template("template_emiten.html")
    html = template.render(**fund)

    # Simpan hasil
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    print(f"✅ Artikel {kode} → {output_path}")

def main():
    if not os.path.exists(FUND_DIR):
        print("❌ Folder data/fundamentals tidak ditemukan.")
        return

    files = [f for f in os.listdir(FUND_DIR) if f.endswith(".json")]
    if not files:
        print("⚠️ Tidak ada file JSON di folder fundamentals.")
        return

    for file in sorted(files):
        kode = file.replace(".json", "")
        render_article(kode)

    print("✅ Semua artikel berhasil digenerate.")

if __name__ == "__main__":
    main()
