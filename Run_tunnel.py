import requests
import os

# ---------- CONFIG ----------
URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"
SAVE_PATH = "./Cloudflared/cloudflared"  # ide mentjük a binárist

# Létrehozzuk a mappát, ha nem létezik
os.makedirs(os.path.dirname(SAVE_PATH), exist_ok=True)

# Fájl letöltése
response = requests.get(URL, stream=True)
if response.status_code == 200:
    with open(SAVE_PATH, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)
    # Futtathatóvá tesszük a fájlt
    os.chmod(SAVE_PATH, 0o755)
    print(f"Cloudflared bináris sikeresen letöltve: {SAVE_PATH}")
else:
    print(f"Hiba a letöltéskor: {response.status_code}")