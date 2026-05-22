#!/bin/bash
# Build and deploy script for top10.lk
# Usage: ./deploy.sh [dev|prod]

set -e

export PATH=/opt/data/bin:$PATH
SITE_DIR=/opt/data/top10.lk

echo "🔨 Building Hugo site..."
cd "$SITE_DIR"
/opt/data/bin/hugo --gc -d public
echo "✅ Build complete"

if [ "$1" = "prod" ]; then
    echo "🌐 Starting production server (ports 80/443)..."
    CONFIG=Caddyfile.prod
    KILL_CMD="pkill -f 'caddy.*Caddyfile' || true"
else
    echo "🧪 Starting dev server (port 8080)..."
    CONFIG=Caddyfile
    KILL_CMD="pkill -f 'caddy.*Caddyfile' || true"
fi

# Kill existing Caddy instance
eval "$KILL_CMD"
sleep 1

# Start new Caddy instance
cd "$SITE_DIR"
nohup env XDG_DATA_HOME=/opt/data/.caddy /opt/data/bin/caddy run --config "$CONFIG" > /opt/data/top10.lk/caddy.log 2>&1 &
echo "✅ Caddy started with $CONFIG"
echo "📋 Logs: /opt/data/top10.lk/caddy.log"
