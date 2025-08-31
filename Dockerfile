FROM python:3.11-slim

# Telepítéshez kellő eszközök
RUN apt-get update && apt-get install -y curl unzip

# Projekt bemásolása
WORKDIR /app
COPY . /app

# Python csomagok
RUN pip install --no-cache-dir -r requirements.txt

# Cloudflared letöltése (Linux AMD64 build)
RUN mkdir -p /app/Cloudflared \
    && curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -o /app/Cloudflared/cloudflared \
    && chmod +x /app/Cloudflared/cloudflared

# Entrypoint: Python script indítja a tunnel-t
ENTRYPOINT ["python3", "/app/all_in_one_runner.py"]
