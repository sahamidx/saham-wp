from datetime import datetime

def log(msg):
    waktu = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(f"[{waktu}] {msg}")
