#!/usr/bin/env python3
"""
Upload HTML artikel saham ke WordPress sebagai draft via REST API
"""

import os
import requests
import base64
import json

WP_USER = "kendalreload@gmail.com"
WP_APP_PASSWORD = "fEZA 2JYS 4i2j LBQq slaN 5oqv"
WP_SITE = "https://idxstock.com"
CATEGORY_ID = 5  # ID kategori 'saham'

OUTPUT_DIR = "output"
FUNDAMENTAL_DIR = "data/fundamentals"

def upload_post(kode):
    kode = kode.upper()
    slug = kode.lower()

    html_path = os.path.join(OUTPUT_DIR, f"{kode}.html")
    fund_path = os.path.join(FUNDAMENTAL_DIR, f"{kode}.json")

    if not os.path.exists(html_path) or not os.path.exists(fund_path):
        print(f"❌ Lewati {kode}, file tidak lengkap")
        return

    with open(html_path, "r", encoding="utf-8") as f:
        html = f.read()

    with open(fund_path, "r", encoding="utf-8") as f:
        fund = json.load(f)

    title = f"Profil Saham {kode}"

    payload = {
        "title": title,
        "slug": slug,
        "status": "draft",
        "categories": [CATEGORY_ID],
        "content": html
    }

    auth_string = f"{WP_USER}:{WP_APP_PASSWORD}"
    token = base64.b64encode(auth_string.encode()).decode("utf-8")
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }

    url = f"{WP_SITE}/wp-json/wp/v2/posts"
    res = requests.post(url, headers=headers, json=payload)

    if res.status_code == 201:
        print(f"✅ Upload sukses: {kode} → ID {res.json().get('id')}")
    else:
        print(f"❌ Upload gagal: {kode} → {res.status_code}")
        print(res.text)

def main():
    files = [f for f in os.listdir(OUTPUT_DIR) if f.endswith(".html")]
    if not files:
        print("⚠️ Tidak ada file HTML untuk di-upload.")
        return

    for file in sorted(files):
        kode = file.replace(".html", "")
        upload_post(kode)

    print("✅ Semua upload selesai.")

if __name__ == "__main__":
    main()
