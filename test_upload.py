from upload_to_wp import upload_to_wordpress

# Ganti dengan post ID dummy atau post testing
POST_ID = 1234
USERNAME = "wp_user_anda"
APP_PASSWORD = "app_password_anda"

payload = {
    "title": "Tes Kutipan 'Single' dan \"Double\"",
    "content": "Ini konten <b>dengan kutipan</b>: 'satu' dan \"dua\".",
    "status": "publish"
}

upload_to_wordpress(POST_ID, payload, USERNAME, APP_PASSWORD)
