# Notepad

A fast, private notepad that runs from a single HTML file. Open `index.html` in a
browser and start typing — no server, no build step, no dependencies, no account.
Notes are stored in the browser's `localStorage`, so they never leave the machine.

```
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
npm run serve            # or serve it at http://localhost:8080
```

## What it does

- **Many notes.** Create, rename, duplicate, pin, delete (with undo) and search
  them. Titles come from the first line automatically until you set your own.
- **Autosave.** Typing is written to `localStorage` shortly after you stop; every
  other action saves immediately. Edits made in another tab are picked up live.
- **Find and replace** within a note, with match counts, next/previous, match
  case, whole word and regular expressions.
- **A real status bar:** cursor line and column, word/character/line counts,
  selection size, reading time and when the note was last edited.
- **Files.** Download a note as `.txt`, back up every note as `.json`, restore a
  backup (merging by note, newest wins), or drop a text file onto the window.
- **Comfort.** Light/dark/auto theme, text size, word wrap, monospace font,
  spell-check toggle, a collapsible note list, printing, and full keyboard
  control. Works down to phone width.

### Keyboard shortcuts

Use `Cmd` instead of `Ctrl` on macOS. The in-app list lives under `Ctrl+/`.

| Shortcut | Action |
| --- | --- |
| `Ctrl+N` | New note |
| `Ctrl+S` | Save now (autosave already handles this) |
| `Ctrl+Shift+S` | Download the note as `.txt` |
| `Ctrl+F` / `Ctrl+H` | Find / find and replace |
| `Enter` / `Shift+Enter` | Next / previous match (in the find bar) |
| `Ctrl+K` | Search all notes |
| `Ctrl+B` | Show or hide the note list |
| `Alt+↑` / `Alt+↓` | Previous / next note |
| `Ctrl+Shift+D` | Duplicate note |
| `Ctrl+;` | Insert the date and time |
| `Tab` / `Shift+Tab` | Indent / outdent the selected lines |
| `Ctrl+Z` / `Ctrl+Y` | Undo / redo (the browser's own) |
| `Esc` | Close the find bar, a menu or a dialog |

Browsers reserve a few of these (`Ctrl+N` opens a window in some, `Ctrl+K` the
address bar); everything they intercept is also available from the `⋯` menu.

## Working on it

Requires Node 20.11+ for the test runner. The app itself needs nothing.

```
npm install         # jsdom, used only by the tests
npm test            # everything: unit, DOM and the single-file guardrails
npm run test:unit   # pure-logic tests only (no dependencies needed)
npm run test:dom    # browser-behaviour tests (needs jsdom)
npm run serve       # http://localhost:8080
```

Tests are the specification: they read `index.html` from disk and exercise the
real code, so there is no copy of the logic to keep in sync. Contributions are
expected to be test-driven — see [CLAUDE.md](CLAUDE.md) for the working
agreement and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how the file is
laid out and why.

## Privacy

Everything stays in the browser under the `notepad:state:v1` key of
`localStorage`. There are no network calls anywhere in the file — a test
enforces that. Clearing site data deletes your notes, so use
**Back up all notes** before you do.
