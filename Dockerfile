FROM debian:bullseye-slim

# Frissítések és függőségek
RUN apt-get update && apt-get install -y curl unzip && rm -rf /var/lib/apt/lists/*

# Cloudflared letöltése
RUN curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
    -o /usr/local/bin/cloudflared && \
    chmod +x /usr/local/bin/cloudflared

# Munkakönyvtár
WORKDIR /app

# Tunnel config és credential fájlok
COPY config.yml /app/config.yml
COPY credentials.json /app/credentials.json

# Futás
CMD ["cloudflared", "tunnel", "--config", "/app/config.yml", "run"]