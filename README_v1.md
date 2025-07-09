# IDXSTOCK SAHAM-WP v1.0 – SISTEM GENERATE ARTIKEL SAHAM OTOMATIS

## 🧠 Tujuan Sistem
Sistem ini bertugas mengambil data saham dari sumber valid, melakukan validasi, merender artikel berbasis template, dan mengunggahnya ke WordPress (idxstock.com) secara otomatis.

## 🧱 Struktur Folder

```
saham-wp/
├── data/
│   ├── static_info.csv        ← Daftar kode saham
│   ├── fundamentals/          ← Output data JSON per emiten
│   ├── validation/            ← Outlier JSON per emiten
│   └── prices/                ← Data harga harian
├── templates/
│   └── template_emiten.html   ← Template artikel HTML (final)
├── output/
│   └── *.html                 ← Artikel final siap upload
├── scripts/
│   ├── update_data.py
│   ├── validate_fundamentals.py
│   ├── generate_article.py
│   └── upload_to_wp.py
```

## ⚙️ Alur Eksekusi

1. **Update data saham**
   ```bash
   python scripts/update_data.py --codes-file data/static_info.csv --output-dir data
   ```

2. **Validasi data fundamental**
   ```bash
   python scripts/validate_fundamentals.py
   ```

3. **Generate artikel HTML**
   ```bash
   python scripts/generate_article.py
   ```

4. **Upload ke WordPress (draft)**
   ```bash
   python scripts/upload_to_wp.py
   ```

## 📝 Format `static_info.csv`

```csv
kode
BBRI
BBCA
UNVR
```

## ✍️ Tentang Template

- Template dipakai: `templates/template_emiten.html`
- Gaya: formal populer (semi-blog)
- Sudah mengandung paragraf antar heading
- Tidak menampilkan data ekstrem/outlier
- Memakai `{{ kode }}`, `{{ nama }}`, `{{ sektor }}`, dll dari JSON

## 🔐 Catatan Validasi

Outlier yang ditandai (tapi tidak ditampilkan di artikel):

| Field           | Outlier Jika                          |
|----------------|----------------------------------------|
| PER             | > 100                                  |
| PBV             | > 20                                   |
| EPS             | < -1000 atau > 10.000                 |
| Dividen Yield   | > 25%                                  |
| Market Cap      | < 1T atau > 5.000T                     |

## 🔑 Akses WordPress API

| Item              | Value                              |
|-------------------|------------------------------------|
| Situs             | https://idxstock.com               |
| Email user        | kendalreload@gmail.com             |
| Application Pass  | fEZA 2JYS 4i2j LBQq slaN 5oqv       |
| Kategori ID       | 5 (kategori "saham")               |

## 🔁 Rencana Selanjutnya

Jika sistem v1.0 ini berjalan stabil…

- [ ] Integrasi cron scheduler
- [ ] Optimasi internal linking
- [ ] Auto schema (FAQ, HowTo)
- [ ] Tagging otomatis berdasarkan sektor
- [ ] Generate halaman indeks (IDX30, LQ45)
- [ ] Integrasi foreign flow, volume distribusi

## 🏁 Status
✅ Sistem artikel saham v1.0 stabil dan produksi-ready.  
Siap upload ratusan artikel secara batch dan konsisten.