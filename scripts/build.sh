#!/usr/bin/env bash
set -euo pipefail

# Ensure LFS objects are present (Vercel clones shallow; pull real files)
if [ -d .git ]; then
  echo "→ Pulling Git LFS objects"
  git lfs pull
fi

# Diagnostic: show NDJSON file sizes so logs reveal if LFS files are real
echo "→ NDJSON file sizes:"
ls -lh ndjson/*.ndjson 2>/dev/null || echo "  (none found)"

readarray -t ARGS < <(python3 scripts/build_args.py | tr -d '\r')
printf '→ Sources:\n'
printf '  %s\n' "${ARGS[@]}"
node scripts/build.mjs "${ARGS[@]}"
