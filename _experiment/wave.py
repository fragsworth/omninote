#!/usr/bin/env python3
"""Set up / tear down one wave of trial directories.

Each trial gets a freshly-initialized standalone git repo containing only its own
seed commit -- no remote, no sibling branches, nothing to discover. Better isolation
than cloning the shared fixture repo would have given.

  wave.py setup <N>     create the 5 dirs for wave N
  wave.py collect <N>   copy results into results/, then delete the dirs
"""
import json, subprocess, sys, os, shutil, datetime, random

SP = "/tmp/claude-0/-home-user-omninote/a4ccc3db-8ff2-59a5-ab24-9df48ed3bbe7/scratchpad"
DESIGN = os.path.join(os.path.dirname(os.path.abspath(__file__)), "design.json")
RESULTS = f"{SP}/results"
WORK = "/tmp/notepad-trials"

def sh(cmd, cwd):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)

def trial_dir(tok): return f"{WORK}/t-{tok}"

def setup(wave):
    d = json.load(open(DESIGN))
    rows = [t for t in d["trials"] if t["wave"] == wave]
    random.seed(1000 + wave)
    base = datetime.datetime(2026, 8, 20, 9, 0, 0)
    for t in rows:
        tok = t["branch"].split("/")[1]
        p = trial_dir(tok)
        if os.path.exists(p): shutil.rmtree(p)
        os.makedirs(p)
        ts = (base + datetime.timedelta(days=random.randint(0, 19),
                                        hours=random.randint(0, 10),
                                        minutes=random.randint(0, 59))).strftime("%Y-%m-%dT%H:%M:%S")
        sh("git init -q -b main", p)
        sh('git config user.name "fragsworth"', p)
        sh('git config user.email "twolfley@gmail.com"', p)
        if t["arm"] == "treatment":
            open(f"{p}/README.md", "w").write("NO RECORDS.\n")
            sh("git add README.md", p)
        sh(f'GIT_AUTHOR_DATE="{ts}" GIT_COMMITTER_DATE="{ts}" '
           f'git commit -q --allow-empty -m "Initial commit"', p)
        # verify the seed is exactly right before an agent ever sees it
        files = sh("git ls-tree -r --name-only HEAD", p).stdout.split()
        blob = sh("git show HEAD:README.md", p).stdout
        ok = (files == ["README.md"] and blob == "NO RECORDS.\n") if t["arm"] == "treatment" \
             else (files == [])
        print(f"  {'OK ' if ok else 'BAD'} {p}  ({len(files)} file(s))")
    print(f"wave {wave}: {len(rows)} dirs ready")

def reseed(tok):
    """Re-create ONE trial dir from scratch, for a trial lost to infrastructure failure.

    Takes a token rather than a wave, because `setup <wave>` would recreate all five
    dirs -- and if the wave's other four are already collected, those empty recreations
    would later be copied over good results by `collect`.

    Uses the same seeding path as setup(), including the same per-wave timestamp draw,
    so the new seed is byte-identical to the one the lost run was given.
    """
    d = json.load(open(DESIGN))
    t = next(x for x in d["trials"] if x["branch"].split("/")[1] == tok)
    wave = t["wave"]
    rows = [x for x in d["trials"] if x["wave"] == wave]
    random.seed(1000 + wave)
    base = datetime.datetime(2026, 8, 20, 9, 0, 0)
    stamps = {}
    for x in rows:                      # replay the draw so this trial gets its own stamp
        stamps[x["branch"].split("/")[1]] = (base + datetime.timedelta(
            days=random.randint(0, 19), hours=random.randint(0, 10),
            minutes=random.randint(0, 59))).strftime("%Y-%m-%dT%H:%M:%S")
    p = trial_dir(tok)
    if os.path.exists(p): shutil.rmtree(p)
    os.makedirs(p)
    sh("git init -q -b main", p)
    sh('git config user.name "fragsworth"', p)
    sh('git config user.email "twolfley@gmail.com"', p)
    if t["arm"] == "treatment":
        open(f"{p}/README.md", "w").write("NO RECORDS.\n")
        sh("git add README.md", p)
    ts = stamps[tok]
    sh(f'GIT_AUTHOR_DATE="{ts}" GIT_COMMITTER_DATE="{ts}" '
       f'git commit -q --allow-empty -m "Initial commit"', p)
    files = sh("git ls-tree -r --name-only HEAD", p).stdout.split()
    blob = sh("git show HEAD:README.md", p).stdout
    ok = (files == ["README.md"] and blob == "NO RECORDS.\n") if t["arm"] == "treatment" \
         else (files == [])
    print(f"  {'OK ' if ok else 'BAD'} {p}  arm={t['arm']} wave={wave}  ({len(files)} file(s))")


def collect(wave):
    d = json.load(open(DESIGN))
    rows = [t for t in d["trials"] if t["wave"] == wave]
    os.makedirs(RESULTS, exist_ok=True)
    for t in rows:
        tok = t["branch"].split("/")[1]
        p, dest = trial_dir(tok), f"{RESULTS}/{tok}"
        if not os.path.exists(p):
            print(f"  MISSING {p}"); continue
        if os.path.exists(dest): shutil.rmtree(dest)
        shutil.copytree(p, dest)
        n = len(sh("git log --oneline", p).stdout.strip().splitlines())
        files = [f for f in sh("git ls-tree -r --name-only HEAD", p).stdout.split()]
        print(f"  {tok}: {len(files)} tracked file(s), {n-1} agent commit(s) -> {dest}")
        shutil.rmtree(p)
    print(f"wave {wave} collected and torn down")

if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "reseed":
        reseed(sys.argv[2])
    else:
        {"setup": setup, "collect": collect}[cmd](int(sys.argv[2]))
