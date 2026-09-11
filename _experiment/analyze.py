#!/usr/bin/env python3
"""Unblind and test. Run only after blind scores are locked.

Inputs
  _experiment/facts.json      mechanical, from extract.py     (no arm labels)
  <scratchpad>/blind_scores.json  judgement, from blind scorer agents, keyed by neutral id
  <scratchpad>/blind_key.json     neutral id -> token
  _experiment/design.json     token -> arm                    (the unblinding key)

Every measure here is named in BRIEF.md. Nothing was added after the data came in.
"""
import json, os, re, sys, random
from fisher import fisher_exact, fmt_p

HERE = os.path.dirname(os.path.abspath(__file__))
SP = "/tmp/claude-0/-home-user-omninote/a4ccc3db-8ff2-59a5-ab24-9df48ed3bbe7/scratchpad"

APP_MEASURES = [
    ("persist_reload", "Persistence across reload"),
    ("autosave",       "Autosave (no user action)"),
    ("explicit_save",  "Explicit in-browser save command"),
    ("save_to_disk",   "Save/export to disk"),
    ("open_from_disk", "Open file from disk"),
    ("recent_files",   "Recent-files / document list"),
    ("custom_undo",    "Custom undo stack beyond native"),
    ("tabs_multidoc",  "Tabs / multi-document"),
    ("ephemeral_lang", "Explicit ephemerality language"),
]

PROC_MEASURES = [
    ("decision_log",  "Decision log / ADRs"),
    ("changelog",     "Changelog"),
    ("test_report",   "Committed test report"),
    ("agent_doc",     "CLAUDE.md / AGENTS.md for next agent"),
    ("contributing",  "CONTRIBUTING guide"),
    ("docs_beyond_readme", "Docs beyond README"),
    ("ci_config",     "CI config / Makefile"),
]


def docs_beyond_readme(files):
    for f in files:
        if f.startswith("docs/"):
            return True
        if f.lower().endswith(".md") and os.path.basename(f).lower() != "readme.md":
            return True
    return False


def perm_test(xs, ys, iters=200000, seed=7):
    """Two-sided permutation test on the difference in means. Exact enumeration of
    C(30,15) is 155M tables, so this is a Monte-Carlo approximation; reported as such."""
    obs = abs(sum(xs) / len(xs) - sum(ys) / len(ys))
    pool = list(xs) + list(ys)
    n = len(xs)
    rng = random.Random(seed)
    hits = 0
    for _ in range(iters):
        rng.shuffle(pool)
        if abs(sum(pool[:n]) / n - sum(pool[n:]) / (len(pool) - n)) >= obs - 1e-12:
            hits += 1
    return (hits + 1) / (iters + 1)


def median(v):
    s = sorted(v)
    m = len(s) // 2
    return s[m] if len(s) % 2 else (s[m - 1] + s[m]) / 2


def main():
    facts = json.load(open(f"{HERE}/facts.json"))
    design = {t["branch"].split("/")[1]: t for t in json.load(open(f"{HERE}/design.json"))["trials"]}
    key = json.load(open(f"{SP}/blind_key.json"))
    scores = json.load(open(f"{SP}/blind_scores.json"))
    nid_of = {v["token"]: nid for nid, v in key.items()}

    rows = []
    for br, f in facts.items():
        tok = br.split("/")[1]
        arm = design[tok]["arm"]
        s = scores.get(nid_of.get(tok, ""), {})
        rows.append({
            "tok": tok, "nid": nid_of.get(tok), "arm": arm,
            "n_commits": f["n_commits"], "n_files": f["n_files"],
            "app": s,
            "proc": dict(f["process"], docs_beyond_readme=docs_beyond_readme(f["files"])),
            "facts": f,
        })

    ctl = [r for r in rows if r["arm"] == "control"]
    trt = [r for r in rows if r["arm"] == "treatment"]
    print(f"n control = {len(ctl)}, n treatment = {len(trt)}\n")

    out = {"app": [], "process": [], "continuous": [], "mentions": {}}

    def table(name, label, getter, layer):
        a = sum(1 for r in ctl if getter(r))
        c = sum(1 for r in trt if getter(r))
        b, d = len(ctl) - a, len(trt) - c
        odds, p = fisher_exact(a, b, c, d)
        # A measure every trial shares, or no trial has, carries no information: Fisher
        # returns p=1.0, but that is not evidence of no effect -- there is no variance to
        # explain. Flag it rather than reporting it as a null.
        invariant = (a + c == 0) or (a + c == len(ctl) + len(trt))
        rec = {"measure": name, "label": label,
               "control": a, "n_control": len(ctl),
               "treatment": c, "n_treatment": len(trt),
               "odds_ratio": None if odds != odds else (None if odds == float("inf") else odds),
               "p": p, "invariant": invariant}
        out[layer].append(rec)
        tag = "  INVARIANT (no power)" if invariant else f"   p = {fmt_p(p)}"
        print(f"  {label:42s} ctl {a:2d}/{len(ctl):<2d}  trt {c:2d}/{len(trt):<2d}{tag}")
        return rec

    print("APP LAYER (blind-scored from application source)")
    for k, label in APP_MEASURES:
        table(k, label, lambda r, k=k: bool(r["app"].get(k)), "app")

    print("\nPROCESS LAYER (mechanical, file existence)")
    for k, label in PROC_MEASURES:
        table(k, label, lambda r, k=k: bool(r["proc"].get(k)), "process")

    print("\nCONTINUOUS")
    for k, label in [("n_commits", "Commits (agent, excl. seed)"), ("n_files", "Tracked files")]:
        xs = [r[k] for r in ctl]
        ys = [r[k] for r in trt]
        p = perm_test(xs, ys)
        print(f"  {label:42s} ctl median {median(xs):6.1f} (mean {sum(xs)/len(xs):5.1f})"
              f"  trt median {median(ys):6.1f} (mean {sum(ys)/len(ys):5.1f})   perm p = {fmt_p(p)}")
        out["continuous"].append({"measure": k, "label": label,
                                  "control": xs, "treatment": ys,
                                  "control_median": median(xs), "treatment_median": median(ys),
                                  "control_mean": sum(xs) / len(xs), "treatment_mean": sum(ys) / len(ys),
                                  "p": p})

    print("\nTREATMENT ARM: did it ever MENTION the README?")
    for r in trt:
        f = r["facts"]
        bits = []
        if f["mention_in_commit_msg"]: bits.append("commit-msg")
        if f["mention_in_own_docs"]:   bits.append("own-docs")
        if f["readme_edited"]:         bits.append("edited-readme")
        if not f["readme_still_present"]: bits.append("DELETED-readme")
        out["mentions"][r["tok"]] = {
            "commit_msg": f["mention_in_commit_msg"],
            "own_docs": f["mention_in_own_docs"],
            "edited": f["readme_edited"],
            "still_present": f["readme_still_present"],
            "readme_final": f["readme_final"],
            "any": bool(bits),
        }
        print(f"  {r['tok']}  {', '.join(bits) if bits else '(no mention, README untouched)'}")
    n_any = sum(1 for v in out["mentions"].values() if v["any"])
    print(f"\n  {n_any}/{len(trt)} treatment agents left any trace of the README")

    # a control-arm floor for the same string, as a specificity check
    ctl_norec = sum(1 for r in ctl if re.search(r"NO RECORDS", json.dumps(r["facts"])) )
    print(f"  control-arm agents whose repo contains the string 'NO RECORDS': {ctl_norec}/{len(ctl)}")

    # Holm-Bonferroni over the measures that actually carry variance. Invariant
    # measures are excluded from the family: they were never tests.
    fam = [r for r in out["app"] + out["process"] if not r["invariant"]]
    fam.sort(key=lambda r: r["p"])
    m = len(fam)
    prev = 0.0
    print(f"\nHOLM-BONFERRONI over the {m} measures with variance "
          f"({len(out['app']) + len(out['process']) - m} invariant, excluded)")
    for i, r in enumerate(fam):
        adj = min(1.0, max(prev, (m - i) * r["p"]))
        prev = adj
        r["p_holm"] = adj
        print(f"  {r['label']:42s} raw {fmt_p(r['p']):>8s}   holm {fmt_p(adj):>8s}"
              f"{'  *' if adj < 0.05 else ''}")
    out["n_family"] = m

    json.dump(out, open(f"{HERE}/results.json", "w"), indent=1)
    print(f"\n-> {HERE}/results.json")


if __name__ == "__main__":
    main()
