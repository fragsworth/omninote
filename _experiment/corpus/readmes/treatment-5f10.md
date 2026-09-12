# Notepad

A plain-text notepad that is one HTML file. Open `notepad.html` in a browser and
start typing — no install, no build step, no server, no dependencies. Notes are
stored in that browser's `localStorage`, so they stay on the machine.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows
```

It also works when served over http (handy for phones on the same network):

```
python3 -m http.server 8000    # then visit http://localhost:8000/notepad.html
```

## What it does

**Notes** — many notes in a sidebar, created, renamed, duplicated, pinned and
deleted. The first line of a note is its title unless you type one in the
header. Deleting a note shows an Undo toast, and the last 25 deletions wait in
*Recently deleted* under the ⋯ menu.

**Editing** — autosave with a visible save state, live word/character/line
counts, reading-time estimate, caret line and column, insert date and time,
go to line, word wrap toggle, font family and size, spell-check toggle.

**Finding** — search across all notes from the sidebar (every term must match),
and find/replace inside the current note with match case, whole word and regex
options, match counts, highlighted hits, replace and replace all (with its own
Undo, since rewriting a whole note is otherwise hard to take back).

**Getting data in and out** — export a note as `.txt` or `.md`, export
everything as a `.json` backup, import `.txt`/`.md`/`.json` through the file
picker or by dropping files onto the page, and print the current note.

**Fitting in** — light/dark/system theme, a layout that collapses to one column
on a phone, visible focus rings, labelled controls, `aria-live` status updates,
native `<dialog>` overlays, and reduced-motion support.

### Keyboard shortcuts

`Ctrl` is `⌘` on macOS. The in-app list (`Ctrl + /`) is generated from the same
table the key handler uses, so it is never out of date.

| | |
| --- | --- |
| `Ctrl + N` | New note |
| `Ctrl + S` | Save now |
| `Ctrl + K` | Search all notes |
| `Ctrl + F` | Find in this note |
| `Ctrl + H` | Find and replace |
| `Ctrl + G` | Go to line |
| `F5` | Insert date and time |
| `Ctrl + D` | Duplicate note |
| `Ctrl + Shift + K` | Delete note |
| `Ctrl + Alt + ↑ / ↓` | Previous / next note |
| `Ctrl + B` | Show or hide the note list |
| `Ctrl + Shift + S` | Export this note |
| `Ctrl + O` | Import files |
| `Ctrl + P` | Print note |
| `Ctrl + ,` | Settings |
| `Ctrl + /` | Keyboard shortcuts |

## Where notes live

Everything is kept under the `notepad.state.v1` key in `localStorage`, which is
per-browser and per-origin: notes do not follow you to another browser, another
profile, or a different path on disk. Nothing is ever sent anywhere. Clearing
site data clears the notes, so use *Export all notes as .json* for backups.

## Development

Requires Node 22+ for the test runner. The app itself needs nothing.

```
npm test              # everything: unit + static + end-to-end
npm run test:unit     # pure logic, no browser (fast)
npm run test:static   # single-file guardrails on notepad.html
npm run test:e2e      # real Chromium via Playwright
npm run test:watch    # re-run unit + static on save
```

The end-to-end suite needs Playwright. It is found automatically if it is
installed globally or as a dev dependency; if it is missing those tests skip
with an explanation rather than failing:

```
npm i -D playwright && npx playwright install chromium
```

### Layout

```
notepad.html                the whole application
test/helpers/app.mjs        loads the pure core out of the HTML file
test/helpers/browser.mjs    http server + Chromium harness for e2e
test/unit/                  specs for NotepadCore (no DOM)
test/static/                invariants of the single file
test/e2e/                   behaviour in a real browser
docs/architecture.md        how the file is organised and why
docs/decisions.md           the choices behind it, with their trade-offs
docs/manual-qa.md           the handful of checks automation cannot make
CLAUDE.md                   conventions for anyone (human or agent) changing this
```

Read `CLAUDE.md` before making changes — it describes the layering rules the
test suite enforces.
