# Notepad

A complete notepad that is **one HTML file**. No dependencies, no build step, no
server, no account, no network. Open `notepad.html` in a browser and it works —
including from a USB stick or an email attachment.

Your notes live in that browser's `localStorage` and go nowhere else.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows

npm start                  # or serve it at http://localhost:8017/notepad.html
```

## What it does

**Notes.** As many as you like, in a searchable sidebar. Create, rename,
duplicate, pin, delete, sort by last edited / created / title. Titles are taken
from the first line until you set one yourself. Everything autosaves.

**Editing.** Plain text, the way a notepad should be. Undo/redo with sensible
grouping, tab and shift-tab indentation, auto-indent, word wrap, three font
families, adjustable text size, and a status bar with line, column, selection
and counts.

**Find and replace.** Whole word, match case, regular expressions with `$1`
group references in the replacement, a match counter, wrap-around, and
replace-all as a single undo step.

**Tools.** Go to line, document statistics, upper/lower/title/sentence case,
sort lines, reverse lines, remove duplicate lines, trim trailing spaces, and
insert the date and time.

**Files.** Open a `.txt` or `.md` file (or drop one on the editor), save the
current note as `.txt` or `.md`, export every note as JSON, import it back, and
print.

**The rest.** Light/dark/system themes, a keyboard-driven menu bar, a shortcut
sheet on `F1`, full keyboard operation with ARIA roles throughout, and a layout
that works on a phone.

Press `F1` in the app for the full shortcut list, or read
[docs/FEATURES.md](docs/FEATURES.md).

## Working on it

```
npm install         # one dev dependency: jsdom, used only by the tests
npm run check       # the gate: full test suite + a report on the shipped file
npm test            # just the tests
npm run test:watch  # re-run on save
npm start           # serve it for a real browser
```

Requires Node 22 or newer (the tests use the built-in `node:test` runner).

**This project is test-driven.** Write the failing test first, in the layer
where the behaviour belongs, then make it pass. See
[CONTRIBUTING.md](CONTRIBUTING.md) for the workflow and
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how the pieces fit together.

## How it is put together

`notepad.html` contains exactly two scripts, and the split is the whole design:

| Block | What lives there | Tested by |
| --- | --- | --- |
| `<script id="notepad-core">` | Pure logic: text measurement, find/replace, undo timeline, note model, command table. No DOM, no storage, no clock. | `test/core/` — fast unit tests |
| `<script id="notepad-app">` | Everything that touches the page: rendering, events, storage, dialogs. Makes no decisions of its own. | `test/ui/` — jsdom behaviour tests |

`test/contract/` guards the promises that neither layer owns on its own: that
the file stays self-contained, that the core stays pure, that every declared
command is implemented and reachable, and that the markup and CSS agree with the
code.

## Public API

The app exposes a deliberately small surface on `window.NotepadApp`, used by the
tests and available to an embedding page:

| Member | Purpose |
| --- | --- |
| `version` | The app version string. |
| `run(commandId)` | Execute any command from the command table. Returns `false` for an unknown id. |
| `getState()` | A JSON snapshot of the notes and settings. |
| `flush()` | Write pending changes to storage now, instead of after the debounce. |
| `setFileSaver(fn)` | Replace how downloads are handed to the browser: `fn({name, mime, text})`. |
| `openText(name, text)` | Create a note from a file's name and contents. |
| `importJson(text)` | Merge notes from an exported JSON payload. Returns `{ok, imported, error}`. |
| `notify(message)` | Show a transient status message. |

`window.NotepadCore` is global too, and is pure — handy for poking at the logic
from the browser console.

## Known limits

- Notes are per-browser and per-profile. There is no sync; use
  **File → Export all notes** for a backup.
- `localStorage` holds roughly 5 MB per origin. If a save is refused, the status
  bar says so rather than failing silently.
- Two tabs open on the same origin overwrite each other's saves; the last writer
  wins.
- The editor is plain text on purpose. There is no rich text and no Markdown
  preview.
