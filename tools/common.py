"""Shared loading, schema validation and derivations for the Scores of Scores build."""
import copy
import json
import re
from pathlib import Path

import yaml
from jsonschema import Draft202012Validator, FormatChecker

ROOT = Path(__file__).resolve().parent.parent
STATUS_OK = {"direct", "qualified"}


class _Loader(yaml.SafeLoader):
    """YAML where only true/false are booleans, so that the strength OFF is not read as false."""


_Loader.yaml_implicit_resolvers = {
    k: [(tag, rx) for tag, rx in v if tag != "tag:yaml.org,2002:bool"] for k, v in yaml.SafeLoader.yaml_implicit_resolvers.items()}
_Loader.add_implicit_resolver("tag:yaml.org,2002:bool", re.compile(r"^(?:true|false)$"), list("tf"))


def load(path):
    return yaml.load(Path(path).read_text(encoding="utf-8"), Loader=_Loader)


def schema_errors(instance, schema_file, def_name=None, label=None):
    schema = json.loads((ROOT / "schemas" / schema_file).read_text(encoding="utf-8"))
    if def_name:
        schema = {"$schema": schema["$schema"], "$ref": "#/$defs/" + def_name, "$defs": schema["$defs"]}
    v = Draft202012Validator(schema, format_checker=FormatChecker())
    where = label or schema_file
    return [f"{where}: {'/'.join(map(str, e.absolute_path)) or '(root)'}: {e.message}" for e in v.iter_errors(instance)]


def load_profiles():
    return {p["profile"]: p for p in (load(f) for f in sorted((ROOT / "profiles").glob("*.yaml")))}


def load_formats():
    """Assemble the formats layer from formats/*.yaml, in the shape the reader and checks use."""
    base = load(ROOT / "formats" / "formats.yaml")
    base["sources"] = load(ROOT / "formats" / "sources.yaml")
    base["cases"] = load(ROOT / "formats" / "cases.yaml")
    base["fixtures"] = load(ROOT / "formats" / "fixtures.yaml")
    feats, files = [], {}
    for c in base["categories"]:
        path = ROOT / "formats" / "features" / (c["id"] + ".yaml")
        items = load(path) if path.exists() else []
        files[c["id"]] = copy.deepcopy(items)  # raw copy, validated against the schema before derived fields exist
        for f in items:
            f["category"] = c["title"]
            feats.append(f)
    base["features"] = feats
    base["_feature_files"] = files
    return base


def link_formats(fdata, core):
    """Add derived fields: rules linked to each feature, the rule-linked tag, and computed `tested`."""
    inverse = {}
    for r in core["rules"]:
        for fid in r.get("format_features", []):
            inverse.setdefault(fid, []).append(r["id"])
    ran = {}  # (feature, format) -> True when a fixture has a result for it
    for fx in fdata["fixtures"]:
        for fmt, res in fx.get("results", {}).items():
            if res != "not_run":
                for fid in fx["features"]:
                    ran[(fid, fmt)] = True
    for f in fdata["features"]:
        f["rules"] = inverse.get(f["id"], [])
        if f["rules"] and "rule-linked" not in f["tags"]:
            f["tags"] = list(f["tags"]) + ["rule-linked"]
        for fmt, c in f["cells"].items():
            c["tested"] = bool(ran.get((f["id"], fmt)))
    return fdata


def feature_index(fdata):
    return {f["id"]: f for f in fdata["features"]}


def expressible(profile, feature_id, fidx):
    """(ok, status, note) for a feature in the profile's version-of-record format."""
    enc = profile["scope"]["encoding"]
    cell = fidx[feature_id]["cells"][enc["format"]]
    s = cell["status"]
    if s in STATUS_OK:
        return True, s, ""
    if s == "extension":
        if feature_id in enc["accept_extensions"]:
            return True, s, "extension accepted"
        return False, s, "extension not accepted"
    return False, s, ""


def mark_status(core, profile, fidx):
    """Effective treatment of each mark category in a profile, derived from the formats data."""
    over = profile.get("scope", {}).get("marks", {})
    out = []
    for k, c in core["mark_categories"].items():
        if "format_feature" in c:
            ok, status, note = expressible(profile, c["format_feature"], fidx)
            derived = "transcribe" if ok else "unsupported"
            fmt = profile["scope"]["encoding"]["format"]
            cell = fidx[c["format_feature"]]["cells"][fmt]
            reason = f"{c['format_feature']} in {fmt}: {status}" + (f" ({note})" if note else "") + f". {cell['summary']}."
        else:
            derived, reason = c["default_treatment"], c.get("rationale", "")
        o = over.get(k, {})
        t = o.get("treatment", derived)
        out.append({"id": k, "title": c["title"], "description": c["description"], "derived": derived,
                    "treatment": t, "reclassified": t != derived, "reason": o.get("reason") or reason})
    return out


RULE_REF = re.compile(r"`([a-z]+\.[a-z0-9]+(?:-[a-z0-9]+)*)`")
