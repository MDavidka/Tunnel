import subprocess
import os
import sys

# ---------- CONFIG ----------
# Cloudflared bináris helye (repo-ban)
CLOUDFLARED_BIN = "./Cloudflared/cloudflared"

# Tunnel ID (a Cloudflare által generált)
TUNNEL_ID = "69b2be84-7e1a-4f89-bf4e-ffa548c31d5a"

# Tunnel konfiguráció fájl (relatív útvonal a repo-hoz)
CONFIG_FILE = "./Cloudflared/config.yml"

# ---------- SCRIPT ----------
def run_tunnel():
    # Ellenőrzés: cloudflared létezik-e
    if not os.path.exists(CLOUDFLARED_BIN):
        print(f"Cloudflared nem található: {CLOUDFLARED_BIN}")
        sys.exit(1)

    # Ellenőrzés: config.yml létezik-e
    if not os.path.exists(CONFIG_FILE):
        print(f"Config fájl nem található: {CONFIG_FILE}")
        sys.exit(1)

    # Tunnel parancs
    cmd = [
        CLOUDFLARED_BIN,
        "tunnel",
        "run",
        TUNNEL_ID,
        "--config",
        CONFIG_FILE
    ]

    # Környezeti változók
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
    run_tunnel()