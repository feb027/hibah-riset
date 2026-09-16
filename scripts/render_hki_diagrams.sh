#!/usr/bin/env bash
# Render the HKI mermaid diagrams to PNG at print scale.
#
# Mermaid CLI drives Chromium through puppeteer. On Ubuntu 23.10+ Chromium
# refuses to start without --no-sandbox, so this script writes a puppeteer
# config pointing at the playwright chromium build and passes it with -p.
# Override CHROME_PATH if your chromium lives elsewhere.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
OUT_DIR="$REPO_ROOT/docs/hki"
CHROME_PATH="${CHROME_PATH:-$HOME/.cache/ms-playwright/chromium-1228/chrome-linux64/chrome}"
PUPPETEER_CFG="$(mktemp /tmp/pptr-XXXX.json)"
trap 'rm -f "$PUPPETEER_CFG"' EXIT

if [ ! -x "$CHROME_PATH" ]; then
  echo "chromium not found at $CHROME_PATH — set CHROME_PATH" >&2
  exit 1
fi

python3 - "$CHROME_PATH" "$PUPPETEER_CFG" <<'PY'
import json, sys
chrome, out = sys.argv[1], sys.argv[2]
json.dump({"args": ["--no-sandbox", "--disable-setuid-sandbox"],
           "executablePath": chrome}, open(out, "w"))
PY

for name in diagram-arsitektur-sistem diagram-tahapan-penelitian; do
  echo "rendering $name"
  npx -y @mermaid-js/mermaid-cli@11 -p "$PUPPETEER_CFG" -b white -s 3 \
    -i "$OUT_DIR/$name.mmd" -o "$OUT_DIR/$name.png"
done

echo "done — PNG written to $OUT_DIR"
