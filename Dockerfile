FROM alpine:3.18

# Install dependencies
RUN apk add --no-cache curl bash

# Download cloudflared
RUN curl -L https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 \
    -o /usr/local/bin/cloudflared && \
    chmod +x /usr/local/bin/cloudflared

# Copy tunnel config & creds
WORKDIR /app
COPY config.yml /app/config.yml
COPY credentials.json /app/credentials.json

# Run cloudflared
CMD ["cloudflared", "tunnel", "--config", "/app/config.yml", "run"]