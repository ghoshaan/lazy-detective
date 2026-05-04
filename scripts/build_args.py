#!/usr/bin/env python3
"""Collect NDJSON snapshots from ndjson/ and print build args for build.mjs.

Two sources are merged:
  1. ndjson/batch-{BATCH}-{DATE}.ndjson  — automated Labelbox exports
  2. ndjson/manifest.json                — manually uploaded files
       Format: { "exact-filename.ndjson": "NicknameBatch", ... }
       Date is extracted automatically from any ISO timestamp in the
       filename (e.g. 20260427T204919Z → 2026-04-27-20).
"""
import glob, json, os, re, sys

DIR = 'ndjson'
args = []
seen = set()

# --- automated exports: batch-{BATCH}-{DATE}.ndjson ---
for path in sorted(glob.glob(os.path.join(DIR, 'batch-*.ndjson'))):
    name  = os.path.basename(path).removesuffix('.ndjson')
    rest  = name.removeprefix('batch-')
    m     = re.search(r'\d{4}-\d{2}-\d{2}(?:-\d{2})?$', rest)
    date  = m.group(0) if m else None
    batch = rest[:-(len(date) + 1)] if date else rest
    args.append(f"{path}:{batch}:{date}" if date else f"{path}:{batch}")
    seen.add(os.path.basename(path))

# --- manually uploaded files listed in manifest.json ---
manifest_path = os.path.join(DIR, 'manifest.json')
if os.path.exists(manifest_path):
    with open(manifest_path, encoding='utf-8') as f:
        manifest = json.load(f)
    for filename, batch in manifest.items():
        if filename in seen:
            continue
        path = os.path.join(DIR, filename)
        if not os.path.exists(path):
            print(f"✗ manifest: '{filename}' not found in {DIR}/", file=sys.stderr)
            sys.exit(1)
        # Parse ISO compact timestamp: 20260427T204919Z → 2026-04-27-20
        m = re.search(r'(\d{4})(\d{2})(\d{2})T(\d{2})\d{4}Z', filename)
        date = f"{m.group(1)}-{m.group(2)}-{m.group(3)}-{m.group(4)}" if m else None
        args.append(f"{path}:{batch}:{date}" if date else f"{path}:{batch}")
        seen.add(filename)

if not args:
    print(f"✗ No NDJSON files found in {DIR}/ — add files or check manifest.json", file=sys.stderr)
    sys.exit(1)

print(' '.join(args))
