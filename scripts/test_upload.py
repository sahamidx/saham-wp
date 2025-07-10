from upload_to_wp import upload_to_wordpress

POST_ID = 2173  # Ganti dengan post yang benar-benar ada
USERNAME = "kendalreload@gmail.com"
APP_PASSWORD = "fEZA 2JYS 4i2j LBQq slaN 5oqv"

payload = {
    "title": "Tes Kutipan 'dan' \"Double\" Berjalan",
    "content": "Ini <b>konten uji</b> upload dengan PUT, kutipan dan markup aman.",
    "status": "publish"
}

upload_to_wordpress(POST_ID, payload, USERNAME, APP_PASSWORD)
