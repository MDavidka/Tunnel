FROM python:3.11-slim

# Alap függőségek
RUN apt-get update && apt-get install -y \
    curl unzip ca-certificates git procps \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Projekt másolása
COPY . /app

# Python csomagok telepítése
RUN pip install --no-cache-dir -r requirements.txt

# Cloudflared letöltése
RUN mkdir -p /app/Cloudflared \
    && curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
    -o /app/Cloudflared/cloudflared \
    && chmod +x /app/Cloudflared/cloudflared

# Entrypoint
ENTRYPOINT ["python3", "/app/Run_tunnel.py"]