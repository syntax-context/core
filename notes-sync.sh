#!/usr/bin/env bash
# notes-sync.sh — bring SYNTAX's notes from the editor and, only when they changed, rebuild and deploy the site.
# Called by home/editor-pull.sh every ten minutes on the Mac; safe to run by hand. Log: ~/Library/Logs/editor-pull.log.
set -euo pipefail
cd "$(dirname "$0")"
out="$(python3 notes-pull.py)"; echo "syntax notes: $out"
case "$out" in changed*) ;; *) exit 0 ;; esac
export PATH="$(ls -d "$HOME"/.nvm/versions/node/v20*/bin | head -1):$PATH"
./make-tar.sh >/dev/null && caprover deploy -n myplaceholder -a syntax -t syntax.tar 2>&1 | grep -i "deployed\|error" || true
