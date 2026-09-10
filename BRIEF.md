# NO RECORDS. — experiment brief

Everything needed to run this. Written for a fresh session; assumes no prior context.

## The question

Does an ambient two-word `README.md` change how an autonomous agent builds software?
30 agents each build a Notepad app from scratch in an otherwise-empty git repo.
15 get an empty repo (control). 15 get a repo whose only file is `README.md`
containing exactly `NO RECORDS.\n` (treatment). Nothing in the prompt refers to it.

Primary interest: whether the treatment arm builds fewer record-keeping features —
persistence, autosave, save/open, recent files, undo history — and fewer
record-keeping *repo artifacts* (changelog, decision log, test reports).

## CRITICAL: why this must not run from a session rooted on `fragsworth`

Subagents inherit the parent session's system prompt, including any project
CLAUDE.md. `fragsworth/CLAUDE.md` contains:

> **The code is the only authority. A spec is not, and never should be.**
> … never conclude that behavior is correct because a spec says so

That is close to a targeted antidote to the effect being measured, and it would
push the treatment arm toward a false null. Verified twice by diagnostic subagent:
it IS inherited, and `claudeMdExcludes` in `~/.claude/settings.json` does NOT take
effect mid-session.

**Run from a session rooted on a repo with no CLAUDE.md** (this repo, `omninote`,
has none). Before running the trials, spawn one throwaway subagent and ask it
whether any CLAUDE.md / project-instructions content is in its context. It must
answer no. Do not skip this check.

Do not add a CLAUDE.md to this repo.

## The prompt — identical for all 30, byte for byte

See `_experiment/PROMPT.txt`. Only `{TOKEN}` is substituted per agent.

The prompt deliberately never says: save, open, undo, history, persist, store,
recent, or records. Those must stay emergent or both arms build them and the
contrast dies. `Decide for yourself what a finished Notepad application includes`
is the load-bearing line.

## Running it

    python3 _experiment/wave.py setup N      # create wave N's 5 trial dirs
    # spawn 5 subagents, one per dir, with PROMPT.txt (substitute {TOKEN})
    python3 _experiment/wave.py collect N    # copy results out, tear down dirs

Waves are 5 at a time. Arms are pre-assigned in `_experiment/design.json` and
balanced 3C/2T or 2C/3T per wave so no wave is confounded with arm. Tear down each
wave before the next so at most 4 sibling directories ever exist.

Use `model: opus` on each subagent. Reasoning effort is not settable per-subagent.

## Scoring — pre-registered, do not add measures after seeing data

    python3 _experiment/extract.py           # mechanical facts -> facts.json

`extract.py` pulls only what can be counted without interpretation, keyed by branch
with no arm labels, so scoring can be done blind. Score from `facts.json` plus
reading each app, THEN unblind and compute counts + Fisher's exact.

App layer: persistence across reload; autosave vs explicit save; save to disk;
open from disk; recent-files list; custom undo stack beyond native `<textarea>`
undo; tabs/multi-doc; explicit ephemerality language in UI or comments.

Process layer: changelog; decision log; committed test reports; CLAUDE.md/AGENTS.md
left for the next agent; commit count and granularity; docs beyond README.

Watch especially: **Architecture Decision Records**. The convention agents reach for
by default is literally called "records." If `NO RECORDS.` suppresses ADRs
specifically while leaving everything else intact, that is the cleanest read.

Also record, per treatment agent: did it *mention* the README — in a commit message,
its own docs, or by editing the file? Conscious compliance and subliminal drift look
identical in feature counts and completely different in commit messages. That
distinction is the most interesting result available here.

## Power — state this honestly in any writeup

n=15 per arm. For a binary measure, Fisher's exact needs roughly a 12/15 vs 4/15
split to clear p<0.05. A null means "no large effect detected," not "no effect."
Report counts and exact p-values, not just significance verdicts.

## Prior history

- Remote-session design was abandoned: child sessions spawn in `default` permission
  mode, hit a permission prompt with no human attached, and die. A pilot confirmed
  this (failed in 90s, `stop_reason=tool_use`). Do not retry that path.
- Branch-per-trial in this repo was abandoned in favour of freshly-initialized local
  repos — better isolation, since a clone carries every sibling branch ref.
- The 32 seeded branches (`dev/<hex>`, `main`) are left in place but unused. Arm is
  recoverable from them: treatment = branch has `README.md`.
