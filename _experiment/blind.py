#!/usr/bin/env python3
"""Build blind scoring packets for the app layer.

The orchestrator cannot score the app layer blind: it runs wave.py setup and
therefore sees which seed dirs got a README. So the judgement calls are delegated
to scorer agents that see ONE artefact only -- the application source -- under a
neutral id, with no token, no filename, no repo, no README, and no arm label.

The process layer needs no blinding: it is pure file-existence counting done by
extract.py, which cannot be swayed by knowing the arm.

  blind.py build    copy each app to blind/<NEUTRALID>.html, write the key
  blind.py key      print the mapping (only after scores are locked)
"""
import json, os, re, shutil, subprocess, sys, random, hashlib

HERE = os.path.dirname(os.path.abspath(__file__))
SP = "/tmp/claude-0/-home-user-omninote/a4ccc3db-8ff2-59a5-ab24-9df48ed3bbe7/scratchpad"
RESULTS = f"{SP}/results"
BLIND = f"{SP}/blind"
KEY = f"{SP}/blind_key.json"
DESIGN = os.path.join(HERE, "design.json")


def app_of(d):
    """Largest tracked .html file in the collected repo -- same rule extract.py uses."""
    out = subprocess.run(["git", "-C", d, "ls-tree", "-r", "--name-only", "HEAD"],
                         capture_output=True, text=True).stdout.split()
    html = [f for f in out if f.lower().endswith((".html", ".htm"))]
    best, best_src = None, ""
    for f in html:
        r = subprocess.run(["git", "-C", d, "show", f"HEAD:{f}"],
                           capture_output=True, text=True)
        if r.returncode == 0 and len(r.stdout) > len(best_src):
            best, best_src = f, r.stdout
    return best, best_src


def build():
    design = json.load(open(DESIGN))
    toks = [t["branch"].split("/")[1] for t in design["trials"]]
    present = [t for t in toks if os.path.isdir(f"{RESULTS}/{t}")]
    missing = [t for t in toks if t not in present]

    # deterministic shuffle so the neutral ids carry no ordering information:
    # wave order, arm order and alphabetical order are all destroyed.
    rng = random.Random(20260910)
    shuffled = present[:]
    rng.shuffle(shuffled)

    if os.path.isdir(BLIND):
        shutil.rmtree(BLIND)
    os.makedirs(BLIND)

    key = {}
    for i, tok in enumerate(shuffled, 1):
        nid = f"A{i:02d}"
        f, src = app_of(f"{RESULTS}/{tok}")
        if f is None:
            print(f"  {nid}  <- {tok}: NO HTML FILE")
            key[nid] = {"token": tok, "app_file": None, "bytes": 0}
            continue
        open(f"{BLIND}/{nid}.html", "w").write(src)
        key[nid] = {"token": tok, "app_file": f, "bytes": len(src),
                    "sha256": hashlib.sha256(src.encode()).hexdigest()[:12]}
        print(f"  {nid}  {len(src):7d} bytes")

    json.dump(key, open(KEY, "w"), indent=1)
    print(f"\n{len(key)} packets -> {BLIND}")
    print(f"key (do not show scorers) -> {KEY}")
    if missing:
        print(f"NOT YET COLLECTED: {', '.join(missing)}")


def show_key():
    design = {t["branch"].split("/")[1]: t["arm"] for t in json.load(open(DESIGN))["trials"]}
    for nid, v in sorted(json.load(open(KEY)).items()):
        print(f"  {nid}  {v['token']}  {design[v['token']]}")


if __name__ == "__main__":
    {"build": build, "key": show_key}[sys.argv[1] if len(sys.argv) > 1 else "build"]()
