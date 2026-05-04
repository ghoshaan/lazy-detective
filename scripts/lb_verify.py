#!/usr/bin/env python3
"""Quick Labelbox API key verification — no export, no data written.

Connects to Labelbox and confirms the key can reach each project.
Run this before setting up secrets to prove the key works.

Usage:
  pip install labelbox
  LABELBOX_API_KEY=<key> python3 scripts/lb_verify.py
"""
import os, sys

try:
    import labelbox as lb
except ImportError:
    print("Install the SDK first:  pip install labelbox")
    sys.exit(1)

PROJECTS = {
    "cmoboff2o0mnk07zwg0thgem7": "NeutralKoala",
    "cmoboldal08eg0738ayr2gdcy": "CoastalLatency",
    "cmokdpcr706v5070x7kt0b3ph": "LuckyTulip",
}

api_key = os.environ.get("LABELBOX_API_KEY") or (sys.argv[1] if len(sys.argv) > 1 else "")
if not api_key:
    print("Usage: LABELBOX_API_KEY=<key> python3 scripts/lb_verify.py")
    sys.exit(1)

print("→ Connecting to Labelbox...")
try:
    client = lb.Client(api_key=api_key)
    user = client.get_user()
    print(f"✓ Connected — {user.email}  (org: {user.organization.name})\n")
except Exception as e:
    print(f"✗ Connection failed: {e}")
    sys.exit(1)

all_ok = True
for project_id, batch in PROJECTS.items():
    try:
        project = client.get_project(project_id)
        print(f"  ✓ {batch:16s}  '{project.name}'")
    except Exception as e:
        print(f"  ✗ {batch:16s}  {e}")
        all_ok = False

print()
if all_ok:
    ids = ",".join(f"{pid}:{name}" for pid, name in PROJECTS.items())
    print("All projects reachable. Set these two secrets to activate automated exports:\n")
    print(f"  LABELBOX_API_KEY  = <your key>")
    print(f"  LABELBOX_PROJECTS = {ids}")
    print()
    print("GitHub:  repo → Settings → Secrets and variables → Actions → New repository secret")
    print("Vercel:  project → Settings → Environment Variables")
else:
    print("One or more projects failed. Check that the key has access to all three projects.")
    sys.exit(1)
