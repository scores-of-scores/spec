#!/usr/bin/env python3
"""Validate every layer and the links between them, then generate documents, data and pages.

Usage:
  python3 tools/build.py           validate, then generate everything
  python3 tools/build.py check     validate only

Layers:    core/principles.yaml, formats/, profiles/*.yaml, notes/registry.yaml
Generated: docs/principles-rules.md, docs/format-support.md, docs/glossary.md, docs/notes-for-transcribers.md,
           README.md and docs/overview.md (document map), paper/paper.md (tables), build/*, site/*
Exit status is non-zero if anything is inconsistent.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from check import check_all  # noqa: E402
from common import ROOT, load, load_formats, load_profiles, link_formats, schema_errors  # noqa: E402


def main(argv):
    cmd = argv[1] if len(argv) > 1 else "all"
    core = load(ROOT / "core" / "principles.yaml")
    profiles = load_profiles()
    notes = load(ROOT / "notes" / "registry.yaml")
    fdata = link_formats(load_formats(), core)
    errs = schema_errors(load(ROOT / "core" / "glossary.yaml"), "glossary.schema.json", label="core/glossary.yaml")
    errs += check_all(core, profiles, notes, fdata, notes["profile"])
    if errs:
        print("FAILED:")
        for e in errs:
            print("  -", e)
        return 1
    if cmd == "check":
        print(f"OK: {len(core['rules'])} rules, {len(profiles)} profiles, {len(notes['notes'])} notes, {len(fdata['features'])} format features")
        return 0
    import gen_docs
    import gen_formats
    import gen_paper
    n = gen_docs.gen_principles(core, profiles, fdata)
    m = gen_docs.gen_notes(notes, core, profiles[notes["profile"]])
    rows = gen_docs.gen_format_support(core, profiles, fdata)
    g = gen_docs.gen_glossary()
    k = gen_formats.gen_formats(fdata)
    gen_docs.gen_docmap()
    gen_paper.gen_paper(core, profiles, fdata, notes)
    unconfirmed = [(p, len(set(v["strengths"]) - set(v.get("basis", {})))) for p, v in profiles.items() if v["status"] == "draft"]
    print(f"OK: {n} rules, {m} notes, {k} format features ({rows} rule-feature links), {g} glossary terms, profiles: {', '.join(profiles)}")
    for p, c in unconfirmed:
        print(f"note: profile {p} is a draft; {c} strengths are unconfirmed core defaults")
    import build_site
    build_site.main()
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
