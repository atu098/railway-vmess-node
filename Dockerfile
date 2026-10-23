FROM alpine:3.21

RUN apk add --no-cache ca-certificates python3 curl unzip && \
    curl -L -o /tmp/xray.zip https://github.com/XTLS/Xray-core/releases/latest/download/Xray-linux-64.zip && \
    unzip -o /tmp/xray.zip -d /usr/local/bin/ xray && \
    chmod +x /usr/local/bin/xray && \
    rm /tmp/xray.zip && \
    curl -L -o /tmp/caddy.tar.gz "https://caddyserver.com/api/download?os=linux&arch=amd64" && \
    tar -xzf /tmp/caddy.tar.gz -C /usr/local/bin/ caddy && \
    chmod +x /usr/local/bin/caddy && \
    rm /tmp/caddy.tar.gz && \
    mkdir -p /srv/www/sub

WORKDIR /app
COPY entrypoint.sh xray.json.tmpl Caddyfile subserver.py surge.tmpl ./
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
