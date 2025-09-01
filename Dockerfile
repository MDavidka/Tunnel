FROM python:3.11-slim

# Függőségek
RUN apt-get update && apt-get install -y \
    curl unzip ca-certificates git procps \
    && rm -rf /var/lib/apt/lists/*

# Munkakönyvtár
WORKDIR /

# Projekt bemásolása
COPY . /

# Python csomagok telepítése
RUN pip install --no-cache-dir -r requirements.txt

# Cloudflared letöltése
RUN mkdir -p /app/Cloudflared \
    && curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
    -o /app/Cloudflared/cloudflared \
    && chmod +x /app/Cloudflared/cloudflared

# Config és credentials
COPY config.yml /config.yml
COPY credentials.json /credentials.json

# Entrypoint -> futtatja a Run_tunnel.py-t
ENTRYPOINT ["python3", "/app/Run_tunnel.py"]