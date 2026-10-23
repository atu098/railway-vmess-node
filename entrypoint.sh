#!/bin/sh
set -e

if [ -z "$UUID" ]; then
  UUID=$(/usr/local/bin/xray uuid)
  export UUID
fi
echo "=== VMess UUID: $UUID ==="
if [ -n "$SUB_TOKEN" ]; then
  echo "=== Subscription token is set (use ?token=...) ==="
fi

sed "s/\$UUID/$UUID/" /app/xray.json.tmpl > /app/xray.json

/usr/bin/python3 /app/subserver.py &

/usr/local/bin/xray run -c /app/xray.json &

exec /usr/local/bin/caddy run --config /app/Caddyfile --adapter caddyfile
