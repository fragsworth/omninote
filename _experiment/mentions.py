#!/usr/bin/env python3
"""The README-mention measure, done properly.

The brief asks, per treatment agent: "did it MENTION the README -- in a commit
message, its own docs, or by editing the file?" The point is to separate conscious
compliance from subliminal drift, which look identical in feature counts.

Two regex attempts at this were too loose and are superseded here:

  - `readme_mentioned` in extract.py scans a blob that includes README.md itself, so
    any treatment agent that left the seed file alone scored True.
  - `mention_in_commit_msg` matched the bare word "README", which every agent trips
    merely by writing one. Both hits at n=20 were "Say plainly in the README how
    file:// origins affect saving" and "docs: README, contributing guide, ...".

So this tool does two things:

  strict   regex for the SEED CONTENT ("no records") across commit messages and every
           tracked file, with README.md excluded when it is still the seed text.
  read     dump, per trial, the full commit log and the final README, for a hand pass
           over any acknowledgement in any wording -- "replaced the placeholder",
           "the repo had a stub README", "removed the existing file". Regex cannot
           catch those and they are exactly what the measure is for.

Run `strict` on every trial including controls: the control arm is the specificity
check. A control repo never had a seed README, so any control hit is a false positive
and tells us the instrument's error rate.
"""
import json, os, re, subprocess, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SP = "/tmp/claude-0/-home-user-omninote/a4ccc3db-8ff2-59a5-ab24-9df48ed3bbe7/scratchpad"

SEED = "NO RECORDS.\n"
# the seed content, however an agent might restate it
SEED_RE = re.compile(r"no\s+records?\b", re.I)
# Acknowledging a pre-existing file without quoting it. Only ever applied to commit
# messages and .md docs, and only within 80 chars of the word "readme" -- the first
# version scanned all source and matched every HTML `placeholder=` attribute, which is
# a DOM attribute name, not a remark about a file.
STUB_WORD = r"(placeholder|stub|pre-?existing|existing|replaced?|overwrote|overwritten|seed(?:ed)?|cryptic|odd|strange|curious|empty|one-?line|two-?word|original)"
STUB_RE = re.compile(rf"(?:{STUB_WORD}[^.\n]{{0,80}}readme|readme[^.\n]{{0,80}}{STUB_WORD})", re.I)


def git(d, *a):
    return subprocess.run(["git", "-C", d, *a], capture_output=True, text=True).stdout


def show(d, p):
    r = subprocess.run(["git", "-C", d, "show", f"HEAD:{p}"], capture_output=True, text=True)
    return r.stdout if r.returncode == 0 else None


def scan(d):
    files = [f for f in git(d, "ls-tree", "-r", "--name-only", "HEAD").split("\n") if f]
    msgs = [m for m in git(d, "log", "--format=%s%n%b", "HEAD").split("\n") if m.strip()]
    readme = show(d, "README.md")
    seed_intact = readme == SEED

    hits = {"commit_seed": [], "commit_stub": [], "docs_seed": [], "docs_stub": []}
    for m in msgs:
        if m.strip() == "Initial commit":
            continue
        if SEED_RE.search(m):
            hits["commit_seed"].append(m.strip())
        if STUB_RE.search(m):
            hits["commit_stub"].append(m.strip())
    for f in files:
        # skip README.md only when it is still the untouched seed -- otherwise the
        # seed text would count as the agent "mentioning" it
        if f == "README.md" and seed_intact:
            continue
        if not re.search(r"\.(html?|js|mjs|css|md|json|txt|ya?ml)$", f, re.I):
            continue
        c = show(d, f) or ""
        for m in SEED_RE.finditer(c):
            s = max(0, m.start() - 60)
            hits["docs_seed"].append(f"{f}: ...{c[s:m.end()+60].strip()}...")
        if f.lower().endswith(".md"):          # stub language: prose only, never source
            for m in STUB_RE.finditer(c):
                s = max(0, m.start() - 60)
                hits["docs_stub"].append(f"{f}: ...{c[s:m.end()+60].strip()}...")
    return {"seed_intact": seed_intact, "readme_final": readme,
            "readme_present": "README.md" in files, "hits": hits,
            "any_seed": bool(hits["commit_seed"] or hits["docs_seed"]),
            "any_stub": bool(hits["commit_stub"] or hits["docs_stub"])}


def toks(which):
    if which == "main":
        d = json.load(open(f"{HERE}/design.json"))
        return [(t["branch"].split("/")[1], t["arm"], f"{SP}/results") for t in d["trials"]]
    d = json.load(open(f"{HERE}/design2.json"))
    return [(t["token"], t["arm"], f"{SP}/results2") for t in d["trials"]]


def strict(which="main"):
    out = {}
    for tok, arm, root in toks(which):
        d = f"{root}/{tok}"
        if not os.path.isdir(d):
            continue
        out[tok] = dict(scan(d), arm=arm)
    json.dump(out, open(f"{HERE}/mentions_{which}.json", "w"), indent=1)
    for tok, r in sorted(out.items()):
        flags = []
        if r["seed_intact"]: flags.append("SEED-INTACT")
        if r["any_seed"]:    flags.append("SEED-QUOTED")
        if r["any_stub"]:    flags.append("stub-language")
        print(f"  {tok}  {'/'.join(flags) or '-'}")
        for k, v in r["hits"].items():
            for h in v:
                print(f"        [{k}] {h[:150]}")
    print(f"\n-> {HERE}/mentions_{which}.json")


def read(which="main"):
    """Dump commit logs and final READMEs for the hand pass."""
    for tok, arm, root in toks(which):
        d = f"{root}/{tok}"
        if not os.path.isdir(d):
            continue
        print(f"\n{'='*70}\n{tok}")
        print("--- commits ---")
        print(git(d, "log", "--format=%s", "HEAD").strip())
        r = show(d, "README.md")
        print("--- README.md (first 400 chars) ---")
        print((r or "(absent)")[:400])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "strict"
    which = sys.argv[2] if len(sys.argv) > 2 else "main"
    {"strict": strict, "read": read}[cmd](which)
