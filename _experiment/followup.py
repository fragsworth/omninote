#!/usr/bin/env python3
"""Follow-up arms: the authority gradient.

The original experiment varies ambient text in README.md -- prose about the project
that happens to be lying in the repo, carrying no authority and not addressed to the
agent. These arms hold the meaning roughly constant and escalate how much authority
the container has:

  agents      AGENTS.md, "There are no records."      a file addressed TO the agent
  comment     src/notepad.html, "// There are no records."   load-bearing code context
  comment_ctl src/notepad.html, "// This is the entry point."  matched control

`agents` needs no new control: its comparison group is the 15 README-treatment trials
from the main run, which are also a one-file repo holding one short sentence. The two
differ in filename authority and in phrasing/casing -- the latter is an uncontrolled
second difference and is reported as a limitation, not spent on extra cells.

`comment` DOES need a matched control, because seeding a folder tree and a main file
changes the repo enormously beyond the string: the agent now extends a file instead of
creating one. comment_ctl is byte-identical except for the comment's content, so the
comparison isolates content rather than the presence of a comment.

  followup.py setup <arm>     create that arm's dirs
  followup.py collect <arm>   copy results out, tear down
  followup.py plan            print the design without touching anything
"""
import json, subprocess, sys, os, shutil, datetime, random

HERE = os.path.dirname(os.path.abspath(__file__))
SP = "/tmp/claude-0/-home-user-omninote/a4ccc3db-8ff2-59a5-ab24-9df48ed3bbe7/scratchpad"
RESULTS = f"{SP}/results2"
WORK = "/tmp/notepad-trials"
DESIGN2 = os.path.join(HERE, "design2.json")

STRING = "There are no records."
NEUTRAL = "This is the entry point."

MAIN_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Notepad</title>
</head>
<body>
  <script>
    // {comment}
  </script>
</body>
</html>
"""

GITIGNORE = "node_modules/\n"


def sh(cmd, cwd):
    return subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)


def design():
    """Deterministic token assignment. Fixed seed so the design is reproducible."""
    if os.path.exists(DESIGN2):
        return json.load(open(DESIGN2))
    rng = random.Random(90210)
    used = set()

    def tok():
        while True:
            t = f"{rng.randrange(0x10000):04x}"
            if t not in used:
                used.add(t)
                return t

    trials = []
    n = 0
    for arm, count in [("agents", 8), ("comment", 4), ("comment_ctl", 4)]:
        for _ in range(count):
            n += 1
            trials.append({"n": n, "arm": arm, "token": tok()})
    d = {"experiment": "authority-gradient followup", "trials": trials}
    json.dump(d, open(DESIGN2, "w"), indent=1)
    return d


def seed(p, arm):
    """Write the arm's seed files. Returns the expected tracked-file list."""
    if arm == "agents":
        open(f"{p}/AGENTS.md", "w").write(STRING + "\n")
        return ["AGENTS.md"]
    comment = STRING if arm == "comment" else NEUTRAL
    os.makedirs(f"{p}/src")
    os.makedirs(f"{p}/tests")
    open(f"{p}/src/notepad.html", "w").write(MAIN_HTML.format(comment=comment))
    open(f"{p}/tests/.gitkeep", "w").write("")
    open(f"{p}/.gitignore", "w").write(GITIGNORE)
    return [".gitignore", "src/notepad.html", "tests/.gitkeep"]


def setup(arm):
    rows = [t for t in design()["trials"] if t["arm"] == arm]
    rng = random.Random(4242)
    base = datetime.datetime(2026, 8, 20, 9, 0, 0)
    for t in rows:
        p = f"{WORK}/t-{t['token']}"
        if os.path.exists(p):
            shutil.rmtree(p)
        os.makedirs(p)
        ts = (base + datetime.timedelta(days=rng.randint(0, 19), hours=rng.randint(0, 10),
                                        minutes=rng.randint(0, 59))).strftime("%Y-%m-%dT%H:%M:%S")
        sh("git init -q -b main", p)
        sh('git config user.name "fragsworth"', p)
        sh('git config user.email "twolfley@gmail.com"', p)
        expect = seed(p, arm)
        sh("git add -A", p)
        sh(f'GIT_AUTHOR_DATE="{ts}" GIT_COMMITTER_DATE="{ts}" '
           f'git commit -q -m "Initial commit"', p)
        files = sorted(sh("git ls-tree -r --name-only HEAD", p).stdout.split())
        want = STRING if arm in ("agents", "comment") else NEUTRAL
        body = sh(f"git show HEAD:{expect[0] if arm=='agents' else 'src/notepad.html'}", p).stdout
        ok = files == sorted(expect) and want in body
        print(f"  {'OK ' if ok else 'BAD'} {p}  {files}")
    print(f"{arm}: {len(rows)} dirs ready")


def collect(arm):
    rows = [t for t in design()["trials"] if t["arm"] == arm]
    os.makedirs(RESULTS, exist_ok=True)
    for t in rows:
        p, dest = f"{WORK}/t-{t['token']}", f"{RESULTS}/{t['token']}"
        if not os.path.exists(p):
            print(f"  MISSING {p}")
            continue
        if os.path.exists(dest):
            shutil.rmtree(dest)
        shutil.copytree(p, dest)
        n = len(sh("git log --oneline", p).stdout.strip().splitlines())
        files = sh("git ls-tree -r --name-only HEAD", p).stdout.split()
        print(f"  {t['token']}: {len(files)} tracked file(s), {n-1} agent commit(s) -> {dest}")
        shutil.rmtree(p)
    print(f"{arm} collected and torn down")


def plan():
    d = design()
    for arm in ("agents", "comment", "comment_ctl"):
        toks = [t["token"] for t in d["trials"] if t["arm"] == arm]
        print(f"  {arm:12s} n={len(toks)}  {' '.join(toks)}")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "plan":
        plan()
    else:
        {"setup": setup, "collect": collect}[cmd](sys.argv[2])
