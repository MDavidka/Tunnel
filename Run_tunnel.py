import os
import sys
import requests
import subprocess
import time

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
        print("[INFO] Cloudflared már létezik, kihagyjuk a letöltést.")
        return

    print("[INFO] Cloudflare letöltése...")
    try:
        response = requests.get(CLOUDFLARED_URL, stream=True)
        response.raise_for_status()
    except Exception as e:
        print(f"[ERROR] Hiba a letöltéskor: {e}")
        sys.exit(1)

    with open(CLOUDFLARED_BIN, "wb") as f:
        for chunk in response.iter_content(1024):
            f.write(chunk)

    os.chmod(CLOUDFLARED_BIN, 0o755)
    print(f"[SUCCESS] Cloudflared bináris sikeresen letöltve: {CLOUDFLARED_BIN}")

def run_tunnel():
    if not os.path.exists(CLOUDFLARED_BIN):
        print("[ERROR] Cloudflared bináris nem található!")
        sys.exit(1)
    if not os.path.exists(CONFIG_FILE):
        print(f"[ERROR] Config fájl nem található: {CONFIG_FILE}")
        sys.exit(1)

    cmd = [CLOUDFLARED_BIN, "tunnel", "--config", CONFIG_FILE, "run", TUNNEL_ID]
    env = os.environ.copy()

    try:
        print("[INFO] Cloudflared tunnel indítása...")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=env)

        # Figyeljük a logokat
        while True:
            output = process.stdout.readline()
            if output:
                line = output.decode().strip()
                print(f"[LOG] {line}")
                if "Tunnel is ready" in line or "started" in line.lower():
                    print("[SUCCESS] Tunnel elindult sikeresen!")
            elif process.poll() is not None:
                break

        stderr = process.stderr.read().decode().strip()
        if stderr:
            print(f"[ERROR] {stderr}")

        exit_code = process.wait()
        if exit_code != 0:
            print(f"[FAILED] Tunnel leállt, exit code: {exit_code}")
        else:
            print("[INFO] Tunnel futása befejeződött rendben.")

    except KeyboardInterrupt:
        print("[INFO] Tunnel leállítva Ctrl+C-vel")
        process.terminate()
    except Exception as e:
        print(f"[ERROR] Hiba a tunnel futtatásakor: {e}")

# ---------- MAIN ----------
if __name__ == "__main__":
    download_cloudflared()
    while True:
        run_tunnel()
        print("[INFO] Tunnel leállt, újraindítás 10mp múlva...")
        time.sleep(10)