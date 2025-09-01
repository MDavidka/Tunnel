FROM python:3.11-slim

# Alap függőségek
RUN apt-get update && apt-get install -y \
    curl unzip ca-certificates git procps \
    && rm -rf /var/lib/apt/lists/*

# Munkakönyvtár
WORKDIR /app

# Projekt bemásolása
COPY . /app

# Python csomagok
RUN pip install --no-cache-dir -r requirements.txt

# Cloudflared letöltése
RUN mkdir -p /app/Cloudflared \
    && curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
    -o /app/Cloudflared/cloudflared \
    && chmod +x /app/Cloudflared/cloudflared

# Config és credentials
COPY config.yml /app/config.yml
COPY credentials.json /app/credentials.json

# Entrypoint -> a GitHubból bemásolt Run_tunnel.py
ENTRYPOINT ["python3", "/app/Run_tunnel.py"]