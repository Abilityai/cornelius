#!/bin/bash
# Shared daemon freshness and URL encoding for the search wrappers.
# Callers set DAEMON_URL and FAISS_FILE before using daemon_fresh.

url_encode() {
    python3 -c "import urllib.parse,sys; print(urllib.parse.quote(sys.argv[1]))" "$1"
}

daemon_fresh() {
    local health build_id on_disk
    health=$(curl -s --max-time 0.2 "$DAEMON_URL/health" 2>/dev/null) || return 1
    [ -n "$health" ] || return 1
    build_id=$(printf '%s' "$health" | python3 -c "import sys,json; d=json.load(sys.stdin); v=d.get('build_id'); print(v if v is not None else '')" 2>/dev/null) || return 1
    [ -n "$build_id" ] || return 1
    [ -f "$FAISS_FILE" ] || return 1
    on_disk=$(python3 -c "import os,sys;print(int(os.path.getmtime(sys.argv[1])))" "$FAISS_FILE" 2>/dev/null) || return 1
    [ "$build_id" = "$on_disk" ]
}
