#!/bin/bash
set -e

BENCH_DIR="/home/frappe/frappe-bench"

mkdir -p "$BENCH_DIR/sites" "$BENCH_DIR/apps" "$BENCH_DIR/logs" "$BENCH_DIR/config"

if [ ! -f "$BENCH_DIR/sites/common_site_config.json" ]; then
    echo "=== Initializing Frappe Bench Environment ==="
    
    if [ ! -d "$BENCH_DIR/env" ]; then
        python3 -m venv "$BENCH_DIR/env"
        "$BENCH_DIR/env/bin/pip" install --upgrade pip setuptools wheel
        "$BENCH_DIR/env/bin/pip" install frappe-bench
    fi

    cat <<EOF > "$BENCH_DIR/sites/common_site_config.json"
{
 "db_host": "mariadb",
 "db_port": 3306,
 "redis_cache": "redis://redis-cache:6379",
 "redis_queue": "redis://redis-queue:6379",
 "redis_socketio": "redis://redis-queue:6379",
 "reorder_models": 1
}
EOF

    cat <<EOF > "$BENCH_DIR/sites/apps.txt"
frappe
erpnext
sms_aftersales
EOF

    cd "$BENCH_DIR"
    if [ ! -d "$BENCH_DIR/apps/frappe" ]; then
        git clone --depth 1 --branch version-15 https://github.com/frappe/frappe "$BENCH_DIR/apps/frappe"
        "$BENCH_DIR/env/bin/pip" install -e "$BENCH_DIR/apps/frappe"
    fi

    if [ ! -d "$BENCH_DIR/apps/erpnext" ]; then
        git clone --depth 1 --branch version-15 https://github.com/frappe/erpnext "$BENCH_DIR/apps/erpnext"
        "$BENCH_DIR/env/bin/pip" install -e "$BENCH_DIR/apps/erpnext"
    fi

    if [ -d "$BENCH_DIR/apps/sms_aftersales" ]; then
        "$BENCH_DIR/env/bin/pip" install -e "$BENCH_DIR/apps/sms_aftersales" || true
    fi

    echo "=== Frappe Bench Environment Initialized Successfully ==="
fi

chown -R frappe:frappe /home/frappe
exec "$@"
