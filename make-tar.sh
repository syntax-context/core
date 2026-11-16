#!/usr/bin/env bash
# Builds syntax.tar for CapRover: build the site, then pack the Dockerfile and site/.
# Deploy: caprover deploy -n myplaceholder -a syntax -t syntax.tar
set -euo pipefail
cd "$(dirname "$0")"
# build.py needs Python 3.12 or later (nested f-strings); on 16 November 2026 a run from jaisa's reader met 3.9 here, cause not found
python3 -c 'import sys; sys.exit(sys.version_info < (3, 12))' || { echo "make-tar.sh: build.py needs Python 3.12 or later; python3 here is $(command -v python3), $(python3 --version 2>&1); PATH=$PATH" >&2; exit 1; }
python3 build.py
COPYFILE_DISABLE=1 tar --exclude='._*' --exclude='.DS_Store' -cf syntax.tar captain-definition Dockerfile nginx.conf site
echo "syntax.tar: $(du -h syntax.tar | cut -f1)"
