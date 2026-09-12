# Notepad

A notepad that is one HTML file. Open `notepad.html` in a browser and start
typing: no install, no build step, no accounts, no network. Notes are kept in
that browser's local storage and never leave the machine.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows

npm run serve              # or http://localhost:8080/notepad.html
```

## What it does

- **Many notes.** Create, rename, duplicate, pin and delete; the sidebar lists
  them with a preview and when they changed. Deleting can be undone from the
  toast that appears.
- **Autosave.** Every edit is written to local storage shortly after you stop
  typing, and again when the tab closes. The status bar says where things stand
  (`Saving...`, `Saved`, or `Could not save` if storage is full or blocked).
- **Search.** Filter the note list by title or body; the count in the sidebar
  footer shows how many matched.
- **Find and replace** inside the open note, with match counts, next/previous,
  match case and whole word. Replace all is a single undo step.
- **Undo and redo** per note, with typing bursts collapsed into one step and
  pastes kept separate.
- **Titles that look after themselves.** A note's title follows its first line
  until you type your own; clearing the title hands it back to the first line.
- **Reading comfort.** Light, dark or system theme; sans, serif or monospace
  editor font; text size 12-28px; word wrap and spell check toggles.
- **Go to line**, insert date and time, indent and outdent with Tab.
- **Text in, text out.** Download the open note as `.txt`, print it properly
  (the whole note, not just the visible box), export every note as one JSON
  backup, import a backup, or drop a `.txt`/`.md` file in to open it as a note.
- **Keyboard first.** Everything has a shortcut, focus is managed, dialogs trap
  and restore focus, and the app is usable end to end without a mouse.
- **Two tabs at once.** Notes saved in one tab appear in the other.

## Keyboard shortcuts

| Action | Shortcut |
| --- | --- |
| New note | `Ctrl+N` |
| Download this note | `Ctrl+S` |
| Find and replace | `Ctrl+F` |
| Search all notes | `Ctrl+Shift+F` |
| Go to line | `Ctrl+G` |
| Undo / redo | `Ctrl+Z` / `Ctrl+Shift+Z` (or `Ctrl+Y`) |
| Insert date and time | `Ctrl+Shift+D` |
| Show or hide the note list | `Ctrl+B` |
| Print | `Ctrl+P` |
| Settings | `Ctrl+,` |
| Indent / outdent | `Tab` / `Shift+Tab` |
| Leave the editor | `Esc` then `Tab` |
| Close a panel or dialog | `Esc` |

On a Mac the app shows and uses `Cmd`. The in-app list lives behind the `?`
button in the toolbar.

## Where the notes live

Everything is one entry in the browser's local storage under the key
`notepad.v1`, holding the notes, the active note and the settings. Consequences
worth knowing:

- Notes are per browser and per profile. A different browser, a different
  machine or a cleared "site data" means different (or no) notes.
- Private windows usually forget everything when they close.
- Local storage is small (a few MB). Settings shows how much the notes use.
- Use **Export backup** in settings for anything you would be upset to lose.
- If the saved data is ever unreadable, the app starts a fresh note and keeps
  the unreadable copy under `notepad.v1.broken` rather than throwing it away.

## Browser support

Any current browser: Chrome, Edge, Firefox and Safari, desktop or mobile. The
app uses `localStorage`, `textarea` selection APIs and CSS custom properties,
and degrades gracefully when `matchMedia`, `Blob` URLs or `FileReader` are
missing. JavaScript is required.

## Working on it

```bash
npm install      # one dev dependency: jsdom, for the UI tests
npm test         # 213 tests, about 10 seconds
npm run serve    # serve the repo, then open /notepad.html
```

The app runs in any browser; the tests need Node 22.22 or newer, because that
is what jsdom requires. The core suite (`npm run test:core`) runs on anything
from Node 20 and needs nothing installed.

| Path | What it is |
| --- | --- |
| `notepad.html` | The whole application: styles, markup, core logic, UI |
| `tests/core/` | Unit tests for the DOM-free core (no jsdom needed) |
| `tests/ui/` | jsdom tests that boot the real file and drive it |
| `tests/invariants.test.mjs` | The rules the file must keep (see below) |
| `tests/helpers/app.mjs` | Test harness: `loadCore()` and `launch()` |
| `docs/ARCHITECTURE.md` | How the app is put together and why |
| `CLAUDE.md` | Conventions for whoever works here next |
| `scripts/serve.mjs` | Dependency-free static server |

The tests enforce the promises this project makes, so they fail if a change
breaks one of them: a single self-contained HTML file, no runtime dependencies,
no network calls, no HTML built from strings, and a core that never touches the
DOM. `npm test` also runs without `npm install` - the core suite still runs and
the UI suite skips itself with an explanation.

Development is test-first; `CLAUDE.md` describes the loop and the house style.

## Licence

No licence has been chosen yet. Pick one before publishing this anywhere.
