import subprocess
import os
import sys

CLOUDFLARED_BIN = "./Cloudflared"  # ide másoljuk fel a binárist
TUNNEL_ID = "69b2be84-7e1a-4f89-bf4e-ffa548c31d5a"

def run_tunnel():
    if not os.path.exists(CLOUDFLARED_BIN):
        print("Cloudflared nem található!")
        sys.exit(1)

    cmd = [
        CLOUDFLARED_BIN,
        "tunnel",
        "run",
        TUNNEL_ID
    ]

    env = os.environ.copy()
    process = subprocess.Popen(cmd, env=env)
    process.wait()

if __name__ == "__main__":
    run_tunnel()
