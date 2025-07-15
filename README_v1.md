# 🚀 Cerita Perjalanan `saham-wp`: Dari Nol Hingga Produksi Otomatis

Ini adalah dokumentasi real tentang bagaimana sistem `saham-wp` dibangun dari nol hingga berhasil menghasilkan artikel saham yang:

✅ Valid,  
✅ Otomatis,  
✅ Diupload ke WordPress,  
✅ Dan dibackup ke GitHub tiap hari.

---

## 🛠 Awal Mula

> "Capek juga bro... file kosong, belum bisa validate..."

Proyek dimulai dari folder kosong. Banyak error awal:
- File tidak ditemukan (`FileNotFoundError`)
- Cron tidak jalan
- Upload ke WordPress gagal
- Duplikasi slug `-2` terus muncul
- GitHub tidak bisa push (`403`, `pathspec`, credential error)

Tapi semua ditangani satu per satu.

---

## 📦 Struktur Proyek Final

saham-wp/
├── data/
│ ├── static_info.csv
│ ├── fundamentals/
│ ├── validation/
├── output/
├── scripts/
│ ├── update_data.py
│ ├── validate_fundamentals.py
│ ├── generate_article.py
│ ├── upload_to_wp.py
│ ├── commit_push.py
│ └── run_all.py
├── templates/
│ └── template_emiten.html


---

## 🔁 Workflow Otomatis (`run_all.py`)

1. Ambil data yfinance (interval harian, stabil T–0)
2. Validasi fundamental & outlier
3. Generate artikel HTML per saham
4. Upload ke WordPress (overwrite jika slug sudah ada)
5. Push semua ke GitHub

---

## 🔐 Masalah yang Diselesaikan

| Masalah Awal                 | Solusi Implementasi                        |
|-----------------------------|---------------------------------------------|
| Cron tidak jalan             | Task Scheduler fix, bisa manual juga        |
| Upload duplikat `slug-2`     | `upload_to_wp.py` pakai `PUT` jika slug ada |
| `git commit` error (pathspec)| Fix tanda kutip di `commit_push.py`         |
| Repo GitHub salah akun       | Ubah remote, re-auth pakai token            |
| Artikel tidak overwrite      | Validasi via API → update by `post_id`      |

---

## 🎯 Status Final

- `run_all.py` jalan manual dan siap cron 17:00
- Artikel seperti `https://idxstock.com/unvr/` berhasil overwrite
- Push otomatis ke GitHub: [https://github.com/sahamidx/saham-wp](https://github.com/sahamidx/saham-wp)
- Sudah diterbitkan batch LQ45
- Template clean, tanpa gimmick promosi

---

## 🏁 Kata Terakhir

Sistem ini adalah hasil kerja keras, trial-error, dan pendekatan modular.  
Disusun secara **stabil, bisa diskalakan, dan siap jangka panjang**.

> "Capek sih... tapi sekarang tinggal nikmati batch harian."  
> — idxstock, Juli 2025

---

Terima kasih untuk semua error yang mendewasakan proyek ini 😉
