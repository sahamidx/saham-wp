#!/usr/bin/env python3
"""
Upload HTML artikel saham ke WordPress sebagai draft atau update jika sudah ada.
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
        "status": "publish",
        "categories": [CATEGORY_ID],
        "content": html
    }

    auth_string = f"{WP_USER}:{WP_APP_PASSWORD}"
    token = base64.b64encode(auth_string.encode()).decode("utf-8")
    headers = {
        "Authorization": f"Basic {token}",
        "Content-Type": "application/json"
    }

    # Step 1: cek apakah slug sudah ada
    check_url = f"{WP_SITE}/wp-json/wp/v2/posts?slug={slug}"
    check_res = requests.get(check_url, headers=headers)
    posts = check_res.json()

    if posts:
        # Overwrite konten (pakai PUT)
        post_id = posts[0]["id"]
        update_url = f"{WP_SITE}/wp-json/wp/v2/posts/{post_id}"
        res = requests.put(update_url, headers=headers, json=payload)

        if res.status_code == 200:
            print(f"🔁 Overwrite sukses: {kode} → ID {post_id}")
        else:
            print(f"❌ Gagal update {kode} → {res.status_code}")
    else:
        # Buat post baru
        create_url = f"{WP_SITE}/wp-json/wp/v2/posts"
        res = requests.post(create_url, headers=headers, json=payload)

        if res.status_code == 201:
            print(f"✅ Upload sukses: {kode} → ID {res.json().get('id')}")
        else:
            print(f"❌ Gagal upload: {kode} → {res.status_code}")

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