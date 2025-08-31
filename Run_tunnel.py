import os
import sys
import requests
import subprocess

# ---------- CONFIG ----------
CLOUDFLARED_DIR = "./Cloudflared"
CLOUDFLARED_BIN = os.path.join(CLOUDFLARED_DIR, "cloudflared")
TUNNEL_ID = "69b2be84-7e1a-4f89-bf4e-ffa548c31d5a"
CONFIG_FILE = os.path.join(CLOUDFLARED_DIR, "config.yml")
CLOUDFLARED_URL = "https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64"

# ---------- FUNKCIÓK ----------
def download_cloudflared():
    os.makedirs(CLOUDFLARED_DIR, exist_ok=True)
    if os.path.exists(CLOUDFLARED_BIN):
        print("Cloudflared már létezik, kihagyjuk a letöltést.")
        return

    print("Cloudflared letöltése...")
    response = requests.get(CLOUDFLARED_URL, stream=True)
    if response.status_code != 200:
        print(f"Hiba a letöltéskor: {response.status_code}")
        sys.exit(1)

    with open(CLOUDFLARED_BIN, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    os.chmod(CLOUDFLARED_BIN, 0o755)
    print(f"Cloudflared bináris sikeresen letöltve: {CLOUDFLARED_BIN}")

def run_tunnel():
    if not os.path.exists(CLOUDFLARED_BIN):
        print("Cloudflared bináris nem található!")
        sys.exit(1)
    if not os.path.exists(CONFIG_FILE):
        print(f"Config fájl nem található: {CONFIG_FILE}")
        sys.exit(1)

    cmd = [CLOUDFLARED_BIN, "tunnel", "run", TUNNEL_ID, "--config", CONFIG_FILE]
    env = os.environ.copy()

    try:
        print("Cloudflared tunnel indítása...")
        process = subprocess.Popen(cmd, env=env)
        process.wait()
    except KeyboardInterrupt:
        print("Tunnel leállítva")
    except Exception as e:
        print(f"Hiba a tunnel futtatásakor: {e}")

# ---------- MAIN ----------
if __name__ == "__main__":
    download_cloudflared()
    run_tunnel()