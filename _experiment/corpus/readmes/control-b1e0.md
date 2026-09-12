# Notepad

A fast, private notepad that is one HTML file. Open `notepad.html` in a browser
and start typing. No install, no build step, no server, no dependencies, no
network calls — notes live in that browser's `localStorage` and never leave the
machine.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows
```

Prefer a real origin (or want to reach it from your phone on the same network)?
`npm start` serves the folder at <http://127.0.0.1:8000/>.

## What it does

**Writing**

- A plain, fast `<textarea>` — no rich text, no surprises, native undo/redo intact.
- Titles derive themselves from the first line (`# Heading` and `- bullet` markers
  are stripped), or type your own in the toolbar.
- Live status bar: line and column, selection size, words, characters, lines and
  a reading estimate.
- Tab indents; with several lines selected, Tab and Shift+Tab shift the block.
- Insert the current date and time with F5, the way the original Notepad does.
- Word wrap toggle, three font families, adjustable text size, optional spell check.

**Notes**

- As many notes as you like, in a searchable sidebar; search matches titles and
  body text, every term must match.
- Sort by last edited, date created or title. Pin the ones you keep coming back to.
- Duplicate, rename, and delete. Deletes go to a trash that keeps the last 20,
  with a one-click undo in the toast and a restore list in the sidebar.
- Every change autosaves ~0.4s after you stop typing; the status bar says when it
  last saved, and tells you plainly if the browser refuses to store more.
- Open the same notes in two tabs and they keep each other up to date.

**Find and replace** (Ctrl+F / Ctrl+H)

- Live match count with the current match highlighted behind the text.
- Match case, whole word, and regular expressions with `$1`-style replacements.
- An invalid pattern says so instead of silently finding nothing.

**In and out**

- Download the current note as a dated `.txt` (`meeting-notes-2026-09-11.txt`).
- Export every note as a JSON backup, and import it again later — importing
  merges by note id and keeps whichever copy was edited more recently.
- Open or drag in `.txt` / `.md` files; drop a backup to restore it.
- Print (or "save as PDF") the current note through the browser's print dialog.

**The rest**

- Light and dark themes, following the system by default.
- Works down to phone width, where the note list becomes a drawer.
- Keyboard reachable throughout, with labelled controls, visible focus rings and
  live regions for status; honours `prefers-reduced-motion`.

## Keyboard shortcuts

| Action | Keys |
| --- | --- |
| New note | `Ctrl+Alt+N` |
| Next / previous note | `Ctrl+Alt+↓` / `Ctrl+Alt+↑` |
| Duplicate note | `Ctrl+Shift+D` |
| Search notes | `Ctrl+K` |
| Show or hide the note list | `Ctrl+B` |
| Find | `Ctrl+F` |
| Find and replace | `Ctrl+H` |
| Next / previous match | `F3` / `Shift+F3` |
| Go to line | `Ctrl+G` |
| Insert date and time | `F5` |
| Indent / outdent | `Tab` / `Shift+Tab` |
| Download note as .txt | `Ctrl+S` |
| Export backup of all notes | `Ctrl+Shift+S` |
| Open text file | `Ctrl+O` |
| Larger / smaller / reset text | `Ctrl+=` / `Ctrl+-` / `Ctrl+0` |
| Close find bar, menu or dialog | `Esc` |

On macOS use `Cmd` in place of `Ctrl`. New note is `Ctrl+Alt+N` rather than
`Ctrl+N` because browsers keep `Ctrl+N` for themselves and a page never sees it.

## Working on it

Requires Node 20.11+ **only for the tests** — the app itself needs nothing.

```bash
npm test              # everything: unit, integrity and real-browser tests
npm run test:unit     # pure logic, milliseconds, no browser
npm run test:watch    # re-run unit tests on save
npm start             # serve the folder for local development
```

There is nothing to install. `npm test` works on a fresh clone: unit tests run
the app's own logic through Node's test runner, and the browser tests drive a
headless Chrome over the DevTools protocol using only Node built-ins. If no
Chrome is installed the browser tests skip and say so; point `CHROME_PATH` at a
binary to run them.

```
notepad.html                 the entire application
test/
  unit/                      pure logic, extracted from the HTML and run in Node
  integrity/                 structural rules: one file, no network, no innerHTML
  browser/                   end-to-end in headless Chrome
  helpers/app.js             loads the app's core for unit tests
  helpers/browser.js         the dependency-free Chrome driver
tools/serve.mjs              static server for `npm start`
docs/ARCHITECTURE.md         how the app is put together, and how to extend it
CLAUDE.md                    conventions for anyone (or any agent) working here
```

Start with [CLAUDE.md](CLAUDE.md) for the working rules and
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for the design.

## Browser support

Current Chrome, Edge, Firefox and Safari. It uses `<dialog>`, `File.text()`,
CSS custom properties and `localStorage`.

## Privacy

Everything stays in your browser's local storage for the page you opened. There
are no accounts, no analytics, no requests of any kind — the integrity tests
fail the build if a network reference ever appears in the file. Clearing site
data (or browsing privately) clears the notes, so keep a JSON backup of anything
you care about.

## License

MIT.
