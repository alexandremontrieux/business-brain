#!/usr/bin/env python3
"""brain.py — deterministic tooling for the Business Brain vault.

Standard library only, so it runs on any machine and under any agent.

  python _scripts/brain.py validate          # schema, folders, links, tags  (exit 1 on errors)
  python _scripts/brain.py index             # rebuild 99_Meta/_index.md and _index.json
  python _scripts/brain.py stale [--days N]  # notes not reviewed for N days
  python _scripts/brain.py orphans           # typed notes with no links in or out
  python _scripts/brain.py thin-positions    # confidence not backed by evidence
  python _scripts/brain.py proposals         # pending proposals with age
  python _scripts/brain.py find "<term>"     # search titles, aliases, tags
"""
from __future__ import annotations

import json
import os
import re
import sys
from datetime import date, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
META = ROOT / "99_Meta"
SCHEMA = json.loads((META / "schema.json").read_text(encoding="utf-8"))
CONFIG = json.loads((ROOT / "brain.config.json").read_text(encoding="utf-8"))
_local = ROOT / "brain.config.local.json"
if _local.exists():
    CONFIG.update(json.loads(_local.read_text(encoding="utf-8")))

SKIP_DIRS = {".obsidian", ".git", "_scripts", "_attachments", "90_Templates", ".github"}
CODE = re.compile(r"```.*?```|`[^`\n]*`", re.S)
WIKILINK = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]*)?(?:\|[^\]]*)?\]\]")


# ---------- minimal YAML-ish frontmatter parser (subset used by this vault) ----------

def _scalar(v: str):
    v = v.strip()
    if v == "" or v == "~" or v == "null":
        return None
    if v.startswith("[") and v.endswith("]"):
        inner = v[1:-1].strip()
        if not inner:
            return []
        parts, cur, depth, quote = [], "", 0, None
        for ch in inner:
            if quote:
                cur += ch
                if ch == quote:
                    quote = None
                continue
            if ch in "\"'":
                quote = ch; cur += ch; continue
            if ch == "[": depth += 1
            if ch == "]": depth -= 1
            if ch == "," and depth == 0:
                parts.append(cur); cur = ""; continue
            cur += ch
        parts.append(cur)
        return [_scalar(p) for p in parts if p.strip() != ""]
    if (v.startswith('"') and v.endswith('"')) or (v.startswith("'") and v.endswith("'")):
        return v[1:-1]
    if v in ("true", "false"):
        return v == "true"
    return v


def _strip_comment(line: str) -> str:
    out, quote = "", None
    for ch in line:
        if quote:
            out += ch
            if ch == quote:
                quote = None
        elif ch in "\"'":
            quote = ch; out += ch
        elif ch == "#" and (not out or out[-1] == " "):
            break
        else:
            out += ch
    return out.rstrip()


def parse_frontmatter(text: str) -> dict | None:
    """Parse the YAML subset this vault uses: scalars, flow lists, block lists
    (indented or not), nested mappings, and block lists of mappings."""
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    lines = [l for l in text[3:end].strip("\n").splitlines()]
    pos = 0

    def indent_of(s):
        return len(s) - len(s.lstrip(" "))

    def parse_block(min_indent):
        """Parse a mapping or a list starting at current pos, items indented >= min_indent."""
        nonlocal pos
        # skip blanks/comments
        while pos < len(lines) and not _strip_comment(lines[pos]).strip():
            pos += 1
        if pos >= len(lines):
            return None
        first = _strip_comment(lines[pos])
        base = indent_of(first)
        if base < min_indent:
            return None
        if first.strip().startswith("- "):
            return parse_list(base)
        return parse_map(base)

    def parse_map(base):
        nonlocal pos
        data = {}
        while pos < len(lines):
            raw = _strip_comment(lines[pos])
            if not raw.strip():
                pos += 1; continue
            ind = indent_of(raw)
            if ind < base or (ind == base and raw.strip().startswith("- ")):
                break
            if ind > base:
                pos += 1; continue  # stray deeper line
            line = raw.strip()
            if ":" not in line:
                pos += 1; continue
            key, _, val = line.partition(":")
            key = key.strip(); val = val.strip()
            pos += 1
            if val:
                data[key] = _scalar(val)
            else:
                # block value: list may sit at the same indent as the key (valid YAML)
                look = pos
                while look < len(lines) and not _strip_comment(lines[look]).strip():
                    look += 1
                if look < len(lines):
                    nxt = _strip_comment(lines[look]); ni = indent_of(nxt)
                    if nxt.strip().startswith("- ") and ni >= base:
                        pos = look; data[key] = parse_list(ni); continue
                    if ni > base:
                        pos = look; data[key] = parse_map(ni); continue
                data[key] = None
        return data

    def parse_list(base):
        nonlocal pos
        items = []
        while pos < len(lines):
            raw = _strip_comment(lines[pos])
            if not raw.strip():
                pos += 1; continue
            ind = indent_of(raw)
            if ind != base or not raw.strip().startswith("- "):
                if ind > base:
                    pos += 1; continue
                break
            body = raw.strip()[2:]
            pos += 1
            if ":" in body and not body.startswith(("[", "\"", "'")) and not body.split(":")[0].strip().startswith("[["):
                # list item that is a mapping: "- key: val" (+ following deeper keys)
                key, _, val = body.partition(":")
                item = {key.strip(): _scalar(val)}
                sub_indent = base + 2
                while pos < len(lines):
                    nraw = _strip_comment(lines[pos])
                    if not nraw.strip():
                        pos += 1; continue
                    if indent_of(nraw) >= sub_indent and ":" in nraw and not nraw.strip().startswith("- "):
                        k, _, v = nraw.strip().partition(":")
                        item[k.strip()] = _scalar(v); pos += 1
                    else:
                        break
                items.append(item)
            else:
                items.append(_scalar(body))
        return items

    return parse_map(indent_of(_strip_comment(lines[0])) if lines else 0) if lines else {}


# ---------- vault scan ----------

def iter_notes():
    for p in sorted(ROOT.rglob("*.md")):
        rel = p.relative_to(ROOT)
        if rel.parts[0] in SKIP_DIRS or len(rel.parts) == 1:  # root-level docs (README, AGENTS) are not notes
            continue
        if rel.as_posix() == "99_Meta/_index.md":  # generated; links to everything
            continue
        yield p


def load():
    notes = {}
    for p in iter_notes():
        text = p.read_text(encoding="utf-8", errors="replace")
        fm = parse_frontmatter(text) or {}
        body = text[text.find("\n---", 3) + 4:] if text.startswith("---") else text
        scan = CODE.sub("", text)  # ignore wikilinks quoted inside code spans / fences
        links = {m.group(1).strip() for m in WIKILINK.finditer(scan)}
        notes[str(p.relative_to(ROOT)).replace(os.sep, "/")] = {
            "path": str(p.relative_to(ROOT)).replace(os.sep, "/"),
            "folder": p.relative_to(ROOT).parts[0],
            "title": p.stem,
            "fm": fm,
            "links": sorted(l for l in links if not l.lower().endswith((".png", ".jpg", ".jpeg", ".pdf", ".svg"))),
            "words": len(body.split()),
        }
    return notes


def _as_list(v):
    if v is None:
        return []
    return v if isinstance(v, list) else [v]


def _link_targets(v):
    out = []
    for item in _as_list(v):
        if isinstance(item, str):
            m = WIKILINK.search(item)
            out.append(m.group(1).strip() if m else item.strip())
    return out


def _date(v):
    if isinstance(v, str):
        try:
            return datetime.strptime(v[:10], "%Y-%m-%d").date()
        except ValueError:
            return None
    return None


def _titles(notes):
    """Resolvable link targets: stems of real notes (proposals excluded) plus aliases."""
    titles, aliases = set(), {}
    for n in notes.values():
        if n["folder"] == "60_Proposals":
            continue
        titles.add(n["title"])
        for a in _as_list(n["fm"].get("aliases")):
            if isinstance(a, str):
                aliases[a] = n["title"]
    return titles, aliases


def _inbound(notes):
    counts = {n["title"]: 0 for n in notes.values() if n["folder"] != "60_Proposals"}
    for n in notes.values():
        if n["folder"] == "60_Proposals":
            continue
        for l in n["links"]:
            if l in counts:
                counts[l] += 1
    return counts


# ---------- commands ----------

def cmd_validate(notes) -> int:
    errors, warnings = [], []
    titles, aliases = _titles(notes)
    types = SCHEMA["types"]
    for n in notes.values():
        fm, path, folder = n["fm"], n["path"], n["folder"]
        untyped_ok = folder in SCHEMA["folders_untyped"]
        t = fm.get("type")
        if not fm:
            (warnings if untyped_ok else errors).append(f"{path}: no frontmatter")
            continue
        if t is None:
            if folder == "60_Proposals":
                errors.append(f"{path}: proposal has no type")
            elif not untyped_ok:
                errors.append(f"{path}: missing type")
            continue
        if t not in types:
            errors.append(f"{path}: unknown type '{t}'"); continue
        is_proposal = folder == "60_Proposals"
        if is_proposal:
            prop = fm.get("proposal")
            if not isinstance(prop, dict):
                errors.append(f"{path}: proposal without 'proposal' block")
            else:
                if prop.get("action") not in SCHEMA["values"]["proposal_action"]:
                    errors.append(f"{path}: proposal.action '{prop.get('action')}' not allowed")
                if prop.get("action") in ("update", "merge", "retire") and not prop.get("target"):
                    errors.append(f"{path}: proposal.action '{prop.get('action')}' needs a target")
        elif folder != types[t]["folder"]:
            errors.append(f"{path}: type '{t}' belongs in {types[t]['folder']}/")
        for f in SCHEMA["required_fields"]:
            if f not in fm:
                if f == "status" and t == "meta":
                    continue
                if is_proposal and f == "reviewed":
                    continue
                errors.append(f"{path}: missing field '{f}'")
        for f in SCHEMA["type_fields"].get(t, []):
            if f not in fm:
                errors.append(f"{path}: {t} needs field '{f}'")
        st = fm.get("status")
        if types[t]["status"] and st not in types[t]["status"] and not (is_proposal and st is None):
            errors.append(f"{path}: status '{st}' not valid for {t}")
        for key in ("origin", "maturity", "confidence", "kind"):
            if key in fm and fm[key] is not None and fm[key] not in SCHEMA["values"][key]:
                errors.append(f"{path}: {key} '{fm[key]}' not allowed")
        for key in ("created", "reviewed"):
            if fm.get(key) is not None and _date(fm[key]) is None:
                errors.append(f"{path}: {key} is not a YYYY-MM-DD date")
        for tag in _as_list(fm.get("tags")):
            if tag not in SCHEMA["tags"]:
                warnings.append(f"{path}: unregistered tag '{tag}'")
        for target in n["links"] + _link_targets(fm.get("related")) + _link_targets(fm.get("evidence")) + _link_targets(fm.get("concepts")):
            base = target.split("/")[-1]
            if base not in titles and base not in aliases:
                errors.append(f"{path}: link to missing note [[{target}]]")
        if t == "position":
            need = SCHEMA["evidence_minimum"].get(fm.get("confidence"), 0)
            if len(_as_list(fm.get("evidence"))) < need:
                warnings.append(f"{path}: confidence '{fm.get('confidence')}' with {len(_as_list(fm.get('evidence')))} evidence links (needs {need})")
    for e in errors:
        print("ERROR  ", e)
    for w in warnings:
        print("WARN   ", w)
    print(f"\n{len(notes)} notes, {len(errors)} errors, {len(warnings)} warnings")
    return 1 if errors else 0


def cmd_index(notes) -> int:
    rows = []
    inbound = _inbound(notes)
    for n in notes.values():
        fm = n["fm"]
        rows.append({
            "title": n["title"], "path": n["path"], "type": fm.get("type"), "status": fm.get("status"),
            "tags": _as_list(fm.get("tags")), "aliases": _as_list(fm.get("aliases")),
            "created": fm.get("created"), "reviewed": fm.get("reviewed"), "origin": fm.get("origin"),
            "confidence": fm.get("confidence"), "kind": fm.get("kind"),
            "links_out": n["links"], "links_in": inbound.get(n["title"], 0), "words": n["words"],
            "proposal": fm.get("proposal") if n["folder"] == "60_Proposals" else None,
        })
    (META / "_index.json").write_text(json.dumps({"generated": date.today().isoformat(), "notes": rows}, indent=1, ensure_ascii=False), encoding="utf-8")
    lines = ["---", "type: meta", "tags: [meta/moc]", "status:", f"created: 2026-10-13", f"reviewed: {date.today().isoformat()}", "origin: agent", "related: []", "---", "",
             "# Index", "", f"Generated by `brain.py index` on {date.today().isoformat()}. Do not edit by hand.", ""]
    for t in SCHEMA["types"]:
        group = [r for r in rows if r["type"] == t and not r["proposal"]]
        if not group:
            continue
        lines += [f"## {t} ({len(group)})", ""]
        for r in sorted(group, key=lambda r: r["title"].lower()):
            extra = f" · {r['confidence']}" if r["confidence"] else (f" · {r['kind']}" if r["kind"] else "")
            lines.append(f"- [[{r['title']}]] — {r['status']}{extra} · {', '.join(r['tags'])} · in {r['links_in']} / out {len(r['links_out'])} · reviewed {r['reviewed']}")
        lines.append("")
    pend = [r for r in rows if r["proposal"]]
    if pend:
        lines += [f"## proposals ({len(pend)})", ""] + [f"- [[{r['title']}]] — {r['proposal'].get('action')} · {r['proposal'].get('proposed_on')}" for r in pend] + [""]
    (META / "_index.md").write_text("\n".join(lines), encoding="utf-8")
    print(f"indexed {len(rows)} notes → 99_Meta/_index.md, _index.json")
    return 0


def cmd_stale(notes, days: int) -> int:
    today = date.today()
    out = []
    for n in notes.values():
        fm = n["fm"]
        if not fm.get("type") or fm.get("type") == "meta" or fm.get("status") == "retired" or n["folder"] == "60_Proposals":
            continue
        d = _date(fm.get("reviewed"))
        age = (today - d).days if d else None
        if age is None or age > days:
            out.append((age if age is not None else 10**6, n["path"]))
    for age, p in sorted(out, reverse=True):
        print(f"{'never' if age >= 10**6 else str(age)+'d':>6}  {p}")
    print(f"\n{len(out)} notes not reviewed in {days} days")
    return 0


def cmd_orphans(notes) -> int:
    inbound = _inbound(notes)
    out = [n["path"] for n in notes.values() if n["folder"] != "60_Proposals" and n["fm"].get("type") not in (None, "meta") and not n["links"] and inbound.get(n["title"], 0) == 0]
    for p in out:
        print(p)
    print(f"\n{len(out)} orphans")
    return 0


def cmd_thin(notes) -> int:
    out = []
    for n in notes.values():
        fm = n["fm"]
        if fm.get("type") != "position" or fm.get("status") == "retired":
            continue
        need = SCHEMA["evidence_minimum"].get(fm.get("confidence"), 0)
        have = len(_as_list(fm.get("evidence")))
        if have < need:
            out.append(f"{n['path']}: {fm.get('confidence')} confidence, {have} evidence (needs {need})")
    print("\n".join(out) or "no thin positions")
    return 0


def cmd_proposals(notes) -> int:
    today = date.today()
    rows = []
    for n in notes.values():
        if n["folder"] != "60_Proposals":
            continue
        prop = n["fm"].get("proposal") or {}
        d = _date(prop.get("proposed_on"))
        rows.append(((today - d).days if d else -1, prop.get("action"), prop.get("proposed_by"), n["path"]))
    for age, action, by, p in sorted(rows, reverse=True):
        print(f"{age:>4}d  {action or '?':<8} {by or '?':<10} {p}")
    print(f"\n{len(rows)} pending proposals")
    return 0


def cmd_find(notes, term: str) -> int:
    t = term.lower()
    hits = []
    for n in notes.values():
        fm = n["fm"]
        hay = [n["title"]] + [a for a in _as_list(fm.get("aliases")) if isinstance(a, str)] + [x for x in _as_list(fm.get("tags")) if isinstance(x, str)]
        if any(t in h.lower() for h in hay):
            hits.append(f"{n['path']}  ({fm.get('type')}, {fm.get('status')})")
    print("\n".join(hits) or "no matches")
    return 0


def main(argv):
    if len(argv) < 2 or argv[1] in ("-h", "--help"):
        print(__doc__); return 0
    cmd = argv[1]
    notes = load()
    if cmd == "validate":
        return cmd_validate(notes)
    if cmd == "index":
        return cmd_index(notes)
    if cmd == "stale":
        days = int(CONFIG.get("stale_days", 90))
        if "--days" in argv:
            try:
                days = int(argv[argv.index("--days") + 1])
            except (IndexError, ValueError):
                print("usage: stale --days N"); return 2
        return cmd_stale(notes, days)
    if cmd == "orphans":
        return cmd_orphans(notes)
    if cmd == "thin-positions":
        return cmd_thin(notes)
    if cmd == "proposals":
        return cmd_proposals(notes)
    if cmd == "find":
        return cmd_find(notes, " ".join(argv[2:]))
    print(f"unknown command {cmd}"); print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv))
