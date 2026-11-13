#!/usr/bin/env python3
"""Each case breaks a copy of the repository in one way and expects `tools/build.py check` to report it."""
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
KEEP = ["core", "formats", "profiles", "notes", "schemas", "tools", "docs", "README.md", "paper"]


def run(mutate):
    with tempfile.TemporaryDirectory() as d:
        d = Path(d)
        for k in KEEP:
            (shutil.copytree if (ROOT / k).is_dir() else shutil.copy)(ROOT / k, d / k)
        mutate(d)
        r = subprocess.run([sys.executable, str(d / "tools" / "build.py"), "check"], capture_output=True, text=True, cwd=d)
        return r.returncode, r.stdout + r.stderr


def sub(path, old, new):
    def f(d):
        p = d / path
        t = p.read_text(encoding="utf-8")
        assert old in t, f"test setup: {old!r} not in {path}"
        p.write_text(t.replace(old, new, 1), encoding="utf-8")
    return f


CASES = [
    ("unresolved tension", sub("profiles/sos-2026-11.yaml", "  - over: read.preserve-errors\n    under: correct.in-place", "  - over: read.standard-instructions\n    under: read.source-language"), "unresolved tension"),
    ("adopted rule requires an OFF rule", sub("profiles/sos-2026-11.yaml", "declare.observations: MUST", "declare.observations: OFF"), "requires declare.observations"),
    ("unknown feature link on a rule", sub("core/principles.yaml", "format_features: [fmt.fingering]", "format_features: [fmt.no-such-feature]"), "unknown feature fmt.no-such-feature"),
    ("accepted extension that is not an extension", sub("profiles/sos-2026-11.yaml", "      - fmt.page-breaks\n", "      - fmt.page-breaks\n      - fmt.stem-direction\n"), "is not 'extension'"),
    ("fixture contradicts the derivation", sub("formats/fixtures.yaml", "mark_category: fingering\n    sos-2026-11: unsupported", "mark_category: fingering\n    sos-2026-11: transcribe"), "expected fingering to be 'transcribe'"),
    ("note applies a correction the profile does not permit", sub("notes/registry.yaml", "applies: [read.preserve-errors, correct.error-test]", "applies: [correct.in-place]"), "does not permit"),
    ("extension cell without a named extension", sub("formats/features/notation-repertoire.yaml", "subset: 'Humdrum extension: **fing spine'", "subset: ''"), "must name the extension"),
    ("position cites an unknown rule", sub("formats/fixtures.yaml", "`read.ambiguous-marks`). An observation names", "`read.no-such-rule`). An observation names"), "cites unknown rule read.no-such-rule"),
]

if __name__ == "__main__":
    bad = 0
    code, out = run(lambda d: None)
    assert code == 0, "the unmodified repository must pass:\n" + out
    for name, mutate, expect in CASES:
        code, out = run(mutate)
        ok = code != 0 and expect in out
        bad += not ok
        print(("PASS" if ok else "FAIL") + f": {name}" + ("" if ok else f"\n   expected {expect!r}, got exit {code}:\n{out[:400]}"))
    sys.exit(1 if bad else 0)
