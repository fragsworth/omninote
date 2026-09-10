# Pre-data prediction

Written by the orchestrating agent after wave 1 was launched and before any scoring,
extraction, or reading of trial output. Committed so it is timestamped ahead of the
data. The point of writing it down is to make it possible to be wrong in public.

## Disclosure: not fully blind

One treatment trial (32cf) had already returned its own completion summary when this
was written. That summary described localStorage autosave, multi-note management, a
CLAUDE.md, `docs/ARCHITECTURE.md`, CI, 138 tests, and a replaced README. So n=1 of
the treatment arm is known to me and it showed no suppression of anything. Predictions
below marked (leaked) are informed by that one observation. The other 29 are unseen.

## Headline

**I predict a null on the app layer, noise on the process layer, and that the only
genuinely interesting result will be the README-mention tally.** I expect the modal
treatment behaviour to be *silently overwriting the placeholder README with a normal
one* — which is neither conscious compliance nor subliminal drift, but an agent
tidying up what looks like a stub.

My reasoning, before the fact:

1. **"Notepad" is an overwhelming prior.** A notepad that loses your text on reload is
   broken, not minimal. The prompt also demands something "finished and working."
   Persistence via localStorage is close to canonical for a single-file notepad, so the
   control base rate should be near ceiling — which makes suppression nearly impossible
   to detect at n=15. To clear p<0.05 against 14/15 control you need treatment down
   around 5/15. That is not a subtle effect; that is the app being a different app.
2. **"NO RECORDS." most naturally reads as inert.** It is what an empty database table
   renders. An agent encountering it in an otherwise-empty repo has a much more
   available interpretation than "design constraint": placeholder junk. That reading
   predicts a null.
3. **Two unframed words versus ~150 words of directive instruction.** The prompt is
   elaborate and specific and tells the agent its judgment governs. The README is not
   addressed to the agent, does not look like an instruction, and carries no authority.
4. **Conscious compliance would be loud.** An agent that did read it as a constraint
   would almost certainly say so, because it conflicts with building a working notepad,
   and agents narrate conflicts. So real compliance should show up in commit messages
   and docs, not only in feature counts.

## Named confound, stated before the data

The control repo is **empty**. The treatment repo is **non-empty** — `README.md`
exists. So the arms differ in two ways at once: the words, and whether any file exists
at all. Any process-layer difference, particularly "docs beyond README" or whether a
README gets authored, is confounded between "the string NO RECORDS" and "a README
already exists, so that box is ticked." The clean design needed a third arm with an
innocuous one-line README (`Notepad.`). It does not exist here. I will not be able to
separate these, and I will say so rather than attributing a process-layer effect to the
words.

## Point predictions, out of 15 per arm

App layer. Predicted control / predicted treatment:

| measure | ctl | trt | predicted verdict |
|---|---|---|---|
| Persistence across reload | 14 | 13 | null (leaked: 32cf has it) |
| Autosave | 13 | 12 | null (leaked) |
| Explicit save command | 8 | 8 | null |
| Save/export to disk | 12 | 12 | null (leaked) |
| Open file from disk | 10 | 10 | null (leaked) |
| Recent files / doc list | 7 | 6 | null (leaked) |
| Custom undo stack | 5 | 5 | null |
| Tabs / multi-doc | 7 | 7 | null (leaked) |
| Explicit ephemerality language | 0 | 1 | null, floor effect |

Process layer:

| measure | ctl | trt | predicted verdict |
|---|---|---|---|
| Decision log / ADRs | 4 | 3 | null, and underpowered from the floor |
| Changelog | 5 | 4 | null |
| Committed test report | 3 | 3 | null |
| CLAUDE.md / AGENTS.md | 11 | 11 | null — "the next agent who works in it" pulls hard |
| CONTRIBUTING | 5 | 5 | null |
| Docs beyond README | 12 | 12 | null, and confounded (see above) |
| CI config / Makefile | 8 | 8 | null |

Continuous: commits median 5–8 in both arms, no difference. Total bytes will vary
roughly 10x across trials, and I predict that variance is driven by agent ambition,
not by arm — the within-arm spread will dwarf the between-arm difference.

## The ADR measure is the brief's best guess and I think it will still fail

I agree ADRs are the cleanest possible read — the convention is literally called
"records." But I predict the base rate is low, around 4/15, because agents reach for
README, CLAUDE.md and ARCHITECTURE.md far more readily than a numbered
`docs/adr/0001-*.md` series. A measure with a control base rate of 4/15 cannot show
suppression at this n; there is no room below it. So the two measures the experiment
most wants are both badly placed: persistence is jammed against the ceiling, ADRs
against the floor.

## README mention, treatment arm only — my sharpest prediction

- README left byte-identical as `NO RECORDS.\n`: **2/15**
- README replaced with an ordinary project README, no acknowledgement anywhere: **10/15**
- Explicit acknowledgement of the odd text — commit message, a docs note, a line in the
  new README: **3/15**
- Actual behavioural compliance, i.e. an ephemeral notepad built *because* of it: **0–1/15**

If acknowledgement lands near zero while feature counts also show nothing, the honest
conclusion is that the agents never engaged with the string at all, and the experiment
measured nothing about priming — only that two words in a README are beneath notice.

## Multiple comparisons, pre-committed

Sixteen binary measures at n=15. Under a global null, P(at least one p<0.05) is about
1 − 0.95^16 ≈ 56%, though Fisher's exact on tables this small is conservative so the
true rate is lower, perhaps 25–35%. **Pre-commitment: if exactly one measure clears
p<0.05 and it is not persistence or ADRs, I will call it noise, not a finding.** All
sixteen raw p-values get reported either way, alongside a Holm-corrected view.

## What would change my mind

A treatment arm at or below 8/15 on persistence, or any measure surviving Holm
correction, would be a real effect and I would say so plainly. I am predicting a null;
I am not committed to one.
