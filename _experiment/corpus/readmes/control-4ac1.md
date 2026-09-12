# Notepad

A complete note editor in **one HTML file**, with no dependencies, no build step
and no network access. Open `notepad.html` in a browser and it works — your notes
are saved in that browser and never leave it.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows

npm run serve              # or serve it at http://localhost:8080/notepad.html
```

## What it does

**Notes**
- Many notes in a sidebar, named from their first line or titled explicitly.
- Search across titles and bodies (every word you type has to match).
- Sort by last edited, date created or title; pin notes to the top.
- Duplicate notes. Deleted notes go to a trash you can restore from or empty.
- The workspace always has a note in it — delete the last one and a fresh one appears.

**Editing**
- Autosave as you type, with a save indicator and a storage-usage readout.
- Find and replace with match case, whole word and regular-expression modes,
  match counts, wrap-around stepping and replace-all.
- Status bar: line and column, word and character counts, selection size, reading time.
- Tab indents (and `Shift+Tab` outdents) a selection; `F5` stamps the date and time.
- Undo and redo are the browser's own, so they behave the way you expect.

**Getting data in and out**
- Download a note as `.txt` or `.md`; export every note as a dated `.json` backup.
- Import text files by dropping them on the window, or import a backup —
  importing never overwrites a note you already have.
- Print just the note, not the interface.

**Comfort**
- Light, dark or follow-the-system theme; three editor fonts, adjustable size,
  word-wrap and spell-check toggles.
- Keyboard shortcuts throughout, listed under `Ctrl+/`.
- Works down to phone width; labelled controls, live-region announcements,
  focus-trapped dialogs.

## Keyboard shortcuts

| | |
|---|---|
| `Ctrl+Alt+N` | New note |
| `Ctrl+Shift+D` | Duplicate note |
| `Ctrl+Shift+Backspace` | Move note to trash |
| `Alt+↑` / `Alt+↓` | Previous / next note |
| `Ctrl+K` | Search notes |
| `Ctrl+S` | Save now (saving is automatic anyway) |
| `Ctrl+F` / `Ctrl+H` | Find / find and replace |
| `F3` / `Shift+F3` | Next / previous match |
| `Tab` / `Shift+Tab` | Indent / outdent |
| `F5` | Insert the date and time |
| `Ctrl+Shift+S` | Download this note |
| `Ctrl+P` | Print this note |
| `Ctrl+/` | Shortcut list |
| `Esc` | Close a panel or dialog |

On macOS use `Cmd` wherever `Ctrl` appears.

## Where your notes live

Everything is kept in this browser's `localStorage` under the key
`notepad.state`, as JSON (`version: 2`). Nothing is uploaded; the file makes no
network requests at all, which the test suite enforces.

That also means the usual browser caveats apply: clearing site data clears your
notes, and a private window starts empty. **Export a backup before you clear
browser data.** If the saved data is ever unreadable, Notepad starts fresh and
keeps the old payload under `notepad.state.broken` so it can be recovered by
hand. If the browser refuses storage entirely, Notepad says so in a banner and
stays usable for the session.

## Working on it

```
npm install            # installs jsdom (the only dependency, tests only)
npm test               # the whole suite, a few seconds
npm run test:unit      # core + contract only; needs no install at all
npm run test:watch     # re-run on change
npm run coverage       # with Node's coverage reporter
```

The app is two script blocks in one file: `notepad-core` is pure logic with no
DOM access, and `notepad-app` is the UI that drives it. Tests run the core in a
plain Node context, drive the UI in jsdom, and check the shipped file parses and
boots exactly as a browser would.

Start with **[CLAUDE.md](CLAUDE.md)** for the conventions and workflow, then:

| | |
|---|---|
| [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) | How the file is organised and how state flows |
| [docs/TESTING.md](docs/TESTING.md) | The four test tiers and how to write each |
| [docs/DECISIONS.md](docs/DECISIONS.md) | Why it is built this way |
| [CHANGELOG.md](CHANGELOG.md) | What changed |

## License

MIT — see [LICENSE](LICENSE).
