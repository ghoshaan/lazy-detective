#!/usr/bin/env bash
set -euo pipefail
readarray -t ARGS < <(python3 scripts/build_args.py)
printf '→ Sources:\n'
printf '  %s\n' "${ARGS[@]}"
node scripts/build.mjs "${ARGS[@]}"
