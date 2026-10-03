#!/usr/bin/env python3
"""Enforce the runbook template and catch broken relative links."""
import pathlib, re, sys

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED = ["Symptoms", "Impact", "Diagnose", "Mitigate", "Verify", "Escalate", "Do not"]
LINK = re.compile(r"\[[^\]]*\]\(([^)#\s]+)(?:#[^)]*)?\)")
errors = []

files = sorted((ROOT / "runbooks").glob("*.md"))
if not files:
    errors.append("no runbooks found")

for f in files:
    text = f.read_text()
    rel = f.relative_to(ROOT)
    if not text.startswith("# Runbook:"):
        errors.append(f"{rel}: first line must start with '# Runbook:'")
    if "Last verified:" not in text:
        errors.append(f"{rel}: missing 'Last verified:' line")
    headings = set(re.findall(r"^## (.+?)\s*$", text, flags=re.M))
    for section in REQUIRED:
        if section not in headings:
            errors.append(f"{rel}: missing section '## {section}'")

for f in list(ROOT.rglob("*.md")):
    if ".git" in f.parts:
        continue
    for target in LINK.findall(f.read_text()):
        if re.match(r"^[a-z]+://|^mailto:", target):
            continue
        if not (f.parent / target).resolve().exists():
            errors.append(f"{f.relative_to(ROOT)}: broken link to {target}")

if errors:
    print("runbook check FAILED")
    for e in errors:
        print(" -", e)
    sys.exit(1)
print(f"runbook check passed ({len(files)} runbooks)")
