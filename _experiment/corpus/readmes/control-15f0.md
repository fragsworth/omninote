# Notepad

A notepad that opens instantly, works offline, and keeps your notes to itself.

The whole application is one file: [`notepad.html`](notepad.html). No build step, no
dependencies, no server, no account. Open it in a browser and start typing. Notes live in
that browser's `localStorage`; nothing is ever sent anywhere.

```sh
# just open it
xdg-open notepad.html      # Linux
open notepad.html          # macOS
start notepad.html         # Windows

# or serve it, if you prefer a real origin
npm run serve              # http://localhost:8080
```

## What it does

**Notes** — as many as you like, in a searchable sidebar. The first line of a note becomes
its title until you rename it. Notes can be pinned to the top, duplicated, sorted by last
edited / created / title, and deleted with an undo.

**Editing** — autosave (nothing to remember), per-note undo/redo that survives switching
notes, word and character counts, caret line/column, reading time, go to line, indent and outdent with
Tab, and `F5` to stamp in the date and time like the original Notepad.

**Find and replace** — inside the current note, with match counting, wrap-around, match
case, whole word, and regular expressions (with `$1` capture groups in replacements).

**Your files** — download a note as `.txt`, back up everything as `.json`, and open `.txt`
or `.json` files by picking them or dropping them on the editor. A backup restores
alongside your existing notes rather than replacing them.

**Comfort** — light/dark/system theme, three editor typefaces, adjustable text size, word
wrap toggle, a collapsible sidebar, a phone-friendly layout, print support, and a shortcut
sheet on `?`.

**Care with your data** — every note is stored under a single `localStorage` key
(`notepad.state.v1`). Corrupt or unreadable storage never produces a blank screen, and if
the browser refuses to store anything (private mode, full disk) the app says so instead of
pretending to save. Notes saved in another tab are picked up automatically unless you have
unsaved edits in this one.

### Keyboard shortcuts

| | |
|---|---|
| New note | `Ctrl+N` |
| Search all notes | `Ctrl+K` |
| Previous / next note | `Alt+Up` / `Alt+Down` |
| Delete note | `Ctrl+Shift+Del` |
| Undo / redo | `Ctrl+Z` / `Ctrl+Shift+Z` |
| Find | `Ctrl+F` |
| Find and replace | `Ctrl+H` |
| Find next / previous | `F3` / `Shift+F3` |
| Go to line | `Ctrl+G` |
| Indent / outdent | `Tab` / `Shift+Tab` |
| Insert date and time | `F5` |
| Download note as `.txt` | `Ctrl+S` |
| Back up all notes | `Ctrl+Shift+S` |
| Open files | `Ctrl+O` |
| Print | `Ctrl+P` |
| Show / hide note list | `Ctrl+B` |
| Shortcut sheet | `?` |

On a Mac, `Cmd` works wherever `Ctrl` is listed.

## Working on it

```sh
npm install        # optional: installs jsdom, which the DOM tests use
npm test           # the whole suite (node:test); DOM suites skip without jsdom
npm run lint       # single-file rules: self-contained, no eval, ids resolve
npm run check      # lint + test, what CI runs
npm run test:watch # re-run on save
```

Requires Node 20 or newer for the built-in test runner. Nothing is needed to *run* the app
— only to test it.

| Path | What it is |
|---|---|
| `notepad.html` | The application. Two tagged scripts: pure logic, then the DOM layer. |
| `test/unit/` | Tests for the pure core plus static checks on the file itself. |
| `test/dom/` | jsdom tests that drive the real UI: clicks, typing, keystrokes. |
| `test/helpers/app.mjs` | Loads the core and boots the page for tests. |
| `scripts/lint.mjs` | Dependency-free linter for the rules a single file needs. |
| `scripts/serve.mjs` | Static server for hands-on checks. |
| `docs/` | Architecture, testing guide, and the reasoning behind the decisions. |

Start with [`CLAUDE.md`](CLAUDE.md) for the conventions this repository follows, and
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for how the file is put together.

## Browser support

Any current version of Chrome, Edge, Firefox, or Safari. The app uses no APIs newer than
2020 and degrades gracefully when something is missing: no clipboard API, no
`URL.createObjectURL`, and no `localStorage` all have fallbacks.
