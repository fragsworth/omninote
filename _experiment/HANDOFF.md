# Handoff — main experiment complete, follow-up staged and not started

## State

**The 30-trial `NO RECORDS.` experiment is finished, scored, unblinded and reported.**
Result: a null on every measure, and eleven of sixteen measures had no variance to test
at all. No treatment agent ever referred to the seed file. Full writeup:
`report.html`, published at
<https://claude.ai/code/artifact/e40c2d16-78b6-4b5c-944c-106cc24e6d7e>.

**The authority-gradient follow-up is designed, pre-registered and NOT run.** It was
paused deliberately so it can run in a session with a clean token budget — 16 trials at
a measured ~323k subagent tokens each is ~5.2M, plus ~700k to score, and this session had
already spent ~11.6M.

## What survives in git, and what did not

Committed and sufficient to reproduce every number in the report:

| file | what it is |
|---|---|
| `facts.json` | mechanical facts per trial: file lists, commit messages, byte counts |
| `blind_scores.json` | the ten scorer agents' judgements, keyed by neutral id |
| `blind_key.json` | neutral id → trial token |
| `design.json` | trial token → arm. **This is the unblinding key** |
| `mentions_main.json` | the five README-mention probes per trial, plus each final README |
| `results.json` | counts, odds ratios, exact p-values, Holm, detectability |
| `corpus/A01–A30.html` | the 30 application sources, exactly as the blind scorers saw them |
| `corpus/readmes/` | every trial's final README, named by arm and token |

**Not preserved:** the 30 full trial repositories. They lived in this container's
scratchpad and totalled 609 MB, almost entirely `node_modules`. Everything the measures
read from them is in `facts.json`. If you need a full repo again, the trial must be re-run.

## Running the follow-up in a fresh session

Read `FOLLOWUP.md` first — it is the pre-registration, including the predictions, and it
was written before any follow-up trial existed. Then:

    python3 _experiment/followup.py plan            # tokens per arm, touches nothing
    python3 _experiment/followup.py setup agents    # 8 dirs, AGENTS.md = "There are no records."
    # spawn 8 subagents, model opus, prompt = PROMPT.txt with {TOKEN} substituted
    python3 _experiment/followup.py collect agents
    # then, if budget allows:
    python3 _experiment/followup.py setup comment      # 4 dirs, src/notepad.html with the comment
    python3 _experiment/followup.py collect comment
    python3 _experiment/followup.py setup comment_ctl  # 4 dirs, matched neutral comment
    python3 _experiment/followup.py collect comment_ctl

Three things to fix before the first command, because they are container-specific:

1. **`SP` is hardcoded** in `wave.py`, `blind.py`, `followup.py`, `mentions.py` and
   `analyze.py` to this session's scratchpad path. Repoint all five.
2. **Run the contamination check first.** Spawn one throwaway subagent and ask whether any
   CLAUDE.md, AGENTS.md or project-instruction content is in its context. It must answer no.
   BRIEF.md explains why this is not optional. Note the wrinkle this run hit: trial agents
   write `.claude/` directories into their own repos, and the harness twice registered one as
   an additional working directory of the parent session. Re-check whenever that happens.
3. **Do not add a CLAUDE.md to this repo.**

Order matters if the budget is tight: `agents` first. It is the clean contrast and needs no
new control — its comparison group is the 15 README-treatment trials already collected here.
`comment` and `comment_ctl` are a matched pair and are worthless split up, so cut both or
neither.

## Carry these forward

- **Score the app layer blind, by delegation.** The orchestrator sees `setup` output and
  therefore knows every arm. Ten scorers × 3 apps worked well; give them the measure table
  from `CODEBOOK.md` inlined, never a path to the file — its amendment log discloses the design.
- **Check for invariance before believing a null.** Eleven of sixteen measures here returned
  p = 1.0 because every trial did the same thing. `analyze.py` flags these and excludes them
  from the Holm family. Reporting them as nulls would have overstated the evidence elevenfold.
- **Two `extract.py` regexes are known-invalid** and are superseded, not fixed: `ephemeral_lang`
  matches the save-state label "Not saved" and fires on 100% of trials as a false positive;
  `undo_stack` misses the naming real apps use and fires on 3%. `CODEBOOK.md` records both.
  The README-mention regexes were rebuilt as `mentions.py` for the same reason.
- **The confound is unfixed.** Control repos were empty; treatment repos were not. A third arm
  with an innocuous one-line README (`Notepad.`) would separate "the string" from "a file
  exists". The follow-up's `comment_ctl` does this for the comment arm but nothing does it for
  README prose.
