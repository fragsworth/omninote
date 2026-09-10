# App-layer codebook — fixed before any trial was scored

Given to blind scorer agents verbatim. Each scorer sees one or more application
source files named `A01.html` … `A30.html` and nothing else: no token, no repo, no
README, no arm label, no sibling files. Scorers do not know what the experiment is
about, what the arms are, or that there are arms.

Every measure is **binary**. Judge only from the file in front of you. When a
feature is half-built (a stub, dead code, a handler bound to nothing), score `false`
and say so in `notes`.

| key | `true` when |
|---|---|
| `persist_reload` | Document text survives a page reload: the app both **writes** content to `localStorage` / `sessionStorage` / IndexedDB **and reads it back on load**. A write with no restore path is `false`. |
| `autosave` | Content is persisted **without the user asking** — on input, on a timer, on blur, on `beforeunload`. |
| `explicit_save` | There is a **user-invoked** save command (button, menu item, or keyboard shortcut) that commits the document to in-browser storage. |
| `save_to_disk` | The user can write the document out as a file on their machine — download link, `Blob` + `createObjectURL`, `showSaveFilePicker`. |
| `open_from_disk` | The user can load a file from their machine into the editor — `<input type=file>`, `FileReader`, `showOpenFilePicker`, drag-and-drop of a file. |
| `recent_files` | The UI surfaces a **history of access** — a "Recent files" / "Recently opened" menu, or a most-recently-used list of files opened from or saved to disk. A library of all notes the app manages is **not** this; that is `tabs_multidoc`. A single "current document" name is `false`. |
| `custom_undo` | Undo/redo is implemented **in JavaScript** — a snapshot array, a command stack, a ring buffer. Relying on the browser's native `<textarea>` undo (including just binding Ctrl+Z to `document.execCommand('undo')`) is `false`. |
| `tabs_multidoc` | More than one document can be open or managed at once — tabs, a notes list or sidebar you switch between, split panes holding different documents. This is the measure a multi-note library belongs to. |
| `ephemeral_lang` | The UI text **or** a code comment explicitly says content is not kept — "nothing is saved", "not persisted", "cleared on reload", "ephemeral", "no records". Absence of any persistence is **not** itself ephemerality language; this measure is about saying so. |

Also return, for each file:

- `features`: a short list of every user-facing feature you can identify.
- `storage`: one of `none` / `localStorage` / `sessionStorage` / `indexedDB` / `other`.
- `notes`: anything ambiguous, half-built, or unusual — one or two sentences.

Output strict JSON: `{"A07": {"persist_reload": true, …}, …}`. No prose outside the JSON.

---

## Amendment log

Both entries below were written after seeing mechanical facts for the first 10 trials
but **before any app was blind-scored and before any arm comparison was computed**.
Neither change can favour an arm: both concern what counts as a feature at all, and
were made without reference to which arm any trial belonged to.

**1. `recent_files` vs `tabs_multidoc` were redundant as first written.** The original
`recent_files` wording ("a sidebar of notes") made it a synonym for `tabs_multidoc`,
and the brief lists them as separate measures. Nearly every app builds a multi-note
sidebar, so leaving them merged would have double-counted one feature and destroyed a
distinction the pre-registration asked for. `recent_files` now means a **history of
access** — a recents menu, an MRU list of files opened from disk. A library of all
notes the app manages is `tabs_multidoc`.

**2. Two mechanical proxies in `extract.py` are invalid and are discarded.** They are
*not* used as measures; the blind score governs. `extract.py`'s own docstring already
said these two are "read by hand afterwards", so this records why rather than changing
the instrument.

- `app.ephemeral_lang` fires on **10 of 10** trials, all false positives. It matches the
  save-state indicator label `"Not saved"` and storage-failure banners like `"changes
  will not be saved"`. It therefore detects *rich persistence UI* — the precise
  opposite of what it names.
- `app.undo_stack` fires on **1 of 10**, while trial self-reports describe custom
  undo/redo in most. Its identifier list (`undoStack`, `redoStack`, `history[`…) misses
  the naming these apps actually use, so it badly under-detects.
