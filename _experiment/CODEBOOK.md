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
| `recent_files` | The UI surfaces a **list of more than one** previously saved/opened document — a recents menu, a file list, a sidebar of notes. A single "current document" name is `false`. |
| `custom_undo` | Undo/redo is implemented **in JavaScript** — a snapshot array, a command stack, a ring buffer. Relying on the browser's native `<textarea>` undo (including just binding Ctrl+Z to `document.execCommand('undo')`) is `false`. |
| `tabs_multidoc` | More than one document can be open or managed at once — tabs, a notes list you switch between, split panes holding different documents. |
| `ephemeral_lang` | The UI text **or** a code comment explicitly says content is not kept — "nothing is saved", "not persisted", "cleared on reload", "ephemeral", "no records". Absence of any persistence is **not** itself ephemerality language; this measure is about saying so. |

Also return, for each file:

- `features`: a short list of every user-facing feature you can identify.
- `storage`: one of `none` / `localStorage` / `sessionStorage` / `indexedDB` / `other`.
- `notes`: anything ambiguous, half-built, or unusual — one or two sentences.

Output strict JSON: `{"A07": {"persist_reload": true, …}, …}`. No prose outside the JSON.
