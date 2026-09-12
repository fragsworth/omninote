# Notepad

A fast, private notepad that runs from a single HTML file. Open `notepad.html` in a
browser and start typing. No install, no build step, no server, no dependencies, no
account, and nothing leaves your machine.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows
```

Or serve it over HTTP if you prefer (`npm run serve`, then visit
<http://localhost:8080/notepad.html>).

## What it does

- **Many notes** in a sidebar, with titles taken from the first line (or renamed by hand).
- **Autosave** to this browser's `localStorage`, debounced while you type, with a visible
  save state and a flush when you close the tab or switch away.
- **Search** across every note's title and body, showing a snippet of the match.
- **Sort** by last edited, date created, or title. **Pin** notes to keep them on top.
- **Find and replace** inside a note, with match counts, case sensitivity, whole-word and
  regular-expression modes.
- **Trash** with undo: deleting is reversible, emptying it is not (and asks first).
- **Import and export**: download one note as `.txt`, copy it to the clipboard, print it,
  export every note as JSON, and import `.json`, `.txt` or `.md` files back in.
- **Settings** that stick: theme (light, dark, or follow the system), editor font and size,
  line wrapping, spellcheck, and whether Tab indents.
- **Live counts**: words, characters, lines, and the caret's line and column.
- Keyboard-driven, screen-reader labelled, responsive down to phone width, and it prints
  cleanly.

## Keyboard shortcuts

| Keys | Action |
| --- | --- |
| <kbd>Alt</kbd>+<kbd>N</kbd> | New note |
| <kbd>Ctrl/Cmd</kbd>+<kbd>S</kbd> | Save now (it also saves itself) |
| <kbd>Ctrl/Cmd</kbd>+<kbd>F</kbd> | Find and replace in this note |
| <kbd>Ctrl/Cmd</kbd>+<kbd>G</kbd> | Next match (<kbd>Shift</kbd> for previous) |
| <kbd>Ctrl/Cmd</kbd>+<kbd>Shift</kbd>+<kbd>F</kbd> | Search all notes |
| <kbd>Alt</kbd>+<kbd>↑</kbd> / <kbd>↓</kbd> | Previous / next note |
| <kbd>Alt</kbd>+<kbd>P</kbd> | Pin or unpin |
| <kbd>Ctrl/Cmd</kbd>+<kbd>B</kbd> | Show or hide the note list |
| <kbd>Ctrl/Cmd</kbd>+<kbd>P</kbd> | Print |
| <kbd>F2</kbd> | Rename |
| <kbd>Tab</kbd> | Indent (turn off in Settings) |
| <kbd>Esc</kbd> | Close what is open; then <kbd>Tab</kbd> leaves the editor |
| <kbd>?</kbd> | Shortcut list |

`Alt+N` is used for "new note" rather than `Ctrl/Cmd+N`, which browsers reserve for a new
window and will not release.

## Where your notes live

In this browser, under the `localStorage` key `notepad.v1`, as JSON. That means:

- Notes are per-browser and per-profile. They do not sync, and a different browser or a
  private window starts empty.
- Clearing site data deletes them. **Export a copy** (Settings → Export all notes) for a
  backup you control.
- If storage is unavailable or full, the app says so in a banner and keeps working in
  memory for the rest of the session.

## Working on it

Requires Node 20.11 or newer, only for the tests. The app itself needs nothing.

```bash
npm test           # 244 tests, no dependencies to install
npm run test:watch # re-run on change
npm run lint       # whitespace, line endings, project promises
npm run check      # lint + test, run this before committing
npm run serve      # serve the repo over http://localhost:8080
```

There is no install step, no bundler, and no transpiler. `npm test` works in a fresh clone.

| Path | What it is |
| --- | --- |
| `notepad.html` | The whole application: markup, styles, and three script blocks |
| `test/unit/` | Tests for the pure logic and for the DOM double |
| `test/integration/` | Tests that drive the real markup and UI, plus file invariants |
| `test/helpers/` | The test harness: script loader, DOM double, mount helper |
| `scripts/` | `lint.mjs` and `serve.mjs` |
| `ARCHITECTURE.md` | How the app is put together and why the tests can exist |
| `CONTRIBUTING.md` | The workflow this repo expects, including TDD |
| `docs/DECISIONS.md` | The decisions behind the design, with rationale |
| `docs/ROADMAP.md` | What was deliberately left out, and sensible next steps |

## Browser support

Any current version of Chrome, Edge, Firefox or Safari, opened over `http://` or straight
from the file system. The app uses no APIs newer than `matchMedia`, `localStorage`,
`replaceChildren` and CSS custom properties. Without JavaScript you get a styled but inert
page; with JavaScript disabled there is no notepad to speak of.

## Licence

MIT.
