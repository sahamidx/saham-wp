import os

print("📡 Update data...")
os.system("python scripts/update_data.py --codes-file data/static_info.csv --output-dir data")

print("🔎 Validasi...")
os.system("python scripts/validate_fundamentals.py")

print("📝 Generate artikel...")
os.system("python scripts/generate_article.py")

print("🌐 Upload ke WordPress...")
os.system("python scripts/upload_to_wp.py")

print("✅ Semua proses selesai.")

print("🛡 Push ke GitHub...")
os.system("python scripts/commit_push.py")

