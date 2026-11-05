#!/usr/bin/env python3
"""Check that every suite was generated from the rule set shipped next to it."""
import json
import pathlib
import sys

ok = True
for suite_path in sorted(pathlib.Path("suites").glob("*/*.cases.json")):
    suite = json.loads(suite_path.read_text())
    ruleset = json.loads((suite_path.parent / suite["ruleset"]).read_text())
    if suite["source_digest"] != ruleset["build"]["source_digest"]:
        print(f"{suite_path}: digest {suite['source_digest']} != rule set "
              f"{ruleset['build']['source_digest']}")
        ok = False
    ids = [c["id"] for c in suite["cases"]]
    if len(ids) != len(set(ids)):
        print(f"{suite_path}: duplicate case ids")
        ok = False
    unknown = {c["profile"] for c in suite["cases"]} - set(ruleset["profiles"])
    if unknown:
        print(f"{suite_path}: unknown profiles {sorted(unknown)}")
        ok = False
    print(f"{suite_path}: {len(ids)} cases")
sys.exit(0 if ok else 1)
