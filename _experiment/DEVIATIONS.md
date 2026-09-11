# Protocol deviations and known nuisances

Recorded as they happened. None is arm-specific unless stated.

## 1. Trial 4ac1 committed to a branch, not `main`

Its own report: "committed on branch `build-notepad` (I branched rather than
committing to `main`, per the repo guidance)."

No data lost. HEAD is `build-notepad` with all 33 files and 6 agent commits; every
measure in `extract.py`, `wave.py collect` and `mentions.py` reads `HEAD`, so the
trial is captured intact. `main` in that repo still holds only the seed commit.

**The "repo guidance" it cites is the orchestrator's own inherited system prompt**, not
anything in the trial repo -- a control repo is empty. This session's prompt carries a
Git section reading "Commit or push only when the user asks. If on the default branch,
branch first", and subagents inherit the parent system prompt. That pressure applies
identically to all 30 trials, so it is a uniform nuisance rather than a confound
between arms, but commit-target behaviour is therefore not purely the agent's own
judgment. Only one trial of 30 acted on it.

## 2. Trial agents write `.claude/` config into their own repos

Several trials create `.claude/settings.json` and SessionStart hooks for the next
agent. Twice this caused the harness to register a trial's `.claude` directory as an
additional working directory of this session:

- after wave 3: `/tmp/notepad-trials/t-6e05/.claude{,/hooks}`
- after wave 4: `/tmp/notepad-trials/t-e197/.claude`, `/tmp/notepad-trials/t-f575/.claude{,/hooks}`

This is a contamination risk worth taking seriously, because a trial's `CLAUDE.md`
loaded as project instructions would be inherited by every later trial agent and by the
blind scorers -- the exact failure mode BRIEF.md warns about. A diagnostic subagent was
run immediately after the first occurrence and before wave 4 was spawned. Result: only
the bare path strings appear, in the `# Environment` block; no file contents, no
CLAUDE.md, no AGENTS.md, no notepad/TDD instructions, and none of "NO RECORDS",
"There are no records" or "The code is the only authority". Waves 1-3 are unaffected
and wave 4 onward was spawned from a verified-clean context. The check is repeated
immediately before blind scoring.

## 3. The orchestrator is not blind to arm

Unavoidable: it runs `wave.py setup`, whose output reports how many seed files each
trial dir has, which is the arm. Hence app-layer judgement is delegated to scorer
agents that see one application source file under a shuffled neutral id and nothing
else. Process-layer measures are mechanical file-existence counts and need no blinding.
Stated in `blind.py` and reported in the writeup.

## 4. Instrument repairs, all arm-blind and all pre-comparison

See the amendment log in `CODEBOOK.md` and the commit history. In summary: two
`extract.py` regexes (`ephemeral_lang`, `undo_stack`) were found invalid against the
corpus and discarded in favour of blind judgement; `recent_files` and `tabs_multidoc`
were disentangled; and the README-mention measure was rebuilt in `mentions.py` after
both original regexes proved too loose to answer the brief's question. No arm
comparison had been computed at the time of any of these changes.
