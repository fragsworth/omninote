# Notepad

A complete, private notepad that lives in one HTML file. Open `index.html` in a
browser and it works — no install, no build step, no server, no dependencies,
no network access. Notes are stored in the browser, and nothing ever leaves it.

```
open index.html          # macOS
xdg-open index.html      # Linux
npm run serve            # or serve it over http://localhost (see "Storage")
```

## What it does

**Notes**
- As many notes as you like, in a searchable sidebar (search matches titles and
  body text, with the match highlighted in the preview)
- Titles are optional — a note is named after its first line until you rename it
- Pin notes to the top, duplicate them, delete them, sort by last edited, date
  created or title
- Everything saves itself as you type; the status bar says when it is saved

**Editing**
- Undo/redo that survives find-and-replace and text transforms, with typing
  coalesced into sensible steps
- Find and replace with match counts, highlighted matches, match case, whole
  word and regular expressions (including `$1` group references)
- Go to line, insert date and time, document statistics
- Line tools: sort, reverse, de-duplicate, remove blank lines, trim trailing
  spaces, collapse repeated spaces, move/duplicate/delete lines
- Case tools: UPPERCASE, lowercase, Title Case, Sentence case
- Tab/Shift+Tab indent (spaces or tabs, configurable width), auto-indent on
  Enter, optional line numbers, optional word wrap (one at a time: a gutter
  cannot line up with wrapped rows, so turning one on turns the other off)
- Live status bar: line and column, selection size, words, characters, lines,
  reading time

**Files**
- Import `.txt`, `.md` and other text files — or drag them onto the editor
- Export a note as `.txt` or `.md`, or every note as a `.json` backup
- Import a backup to restore notes on another browser or device (existing notes
  are never overwritten)
- Print a clean copy of the current note

**Comfort**
- Light and dark themes, or follow the system
- Monospace, sans or serif editor font, adjustable size (Ctrl+`+` / Ctrl+`-`)
- Full keyboard access; press **F1** for the shortcut list
- Works on a phone-sized screen
- Accessible: labelled controls, focus-trapped dialogs, live status messages,
  respects `prefers-reduced-motion`

## Keyboard shortcuts

| Keys | Action |
|---|---|
| `Ctrl+Alt+N` | New note |
| `Ctrl+S` | Save now |
| `Ctrl+Shift+S` | Export this note |
| `Ctrl+B` | Show/hide the note list |
| `Ctrl+F` / `Ctrl+H` | Find / find and replace |
| `Enter` / `Shift+Enter` | Next / previous match (in the find bar) |
| `Ctrl+G` | Go to line |
| `Ctrl+Z` / `Ctrl+Y` | Undo / redo |
| `Tab` / `Shift+Tab` | Indent / outdent |
| `Alt+↑` / `Alt+↓` | Move line up / down |
| `Shift+Alt+↓` | Duplicate line |
| `Ctrl+Shift+K` | Delete line |
| `Alt+Shift+D` | Insert date and time |
| `Ctrl+P` | Print |
| `Ctrl++` / `Ctrl+-` / `Ctrl+0` | Text size |
| `F1` or `Ctrl+/` | Keyboard shortcuts |
| `Esc` | Close the find bar, a menu or a dialog |

## Storage

Notes live in `localStorage` under the key `notepad.state.v1`, in this browser
profile only. They are not synced, uploaded or shared.

Opened straight from disk as a `file://` page, notes persist too — current
Chrome, Firefox and Safari all keep `localStorage` per file origin. Some
browsers and privacy settings block it; when that happens the app says so in a
banner and keeps working, it just cannot remember anything after the tab closes.
`npm run serve` (or any static web server) gives it a normal http origin, which
is also how you would host it for others.

Two tabs of Notepad stay in step: when one saves, an idle tab picks the change
up straight away, and a tab with unsaved edits keeps them and says the notes
also changed elsewhere rather than overwriting your work.

Stored data is treated as untrusted input: a corrupted, half-written, legacy or
newer-than-expected payload always loads into a working app, repairing what it
can and explaining what it could not in a banner.

## Development

Requires Node 22+ (for the built-in test runner and global `WebSocket`). There is
nothing to install.

```bash
npm test            # unit + contract + end-to-end tests
npm run test:unit   # fast: core logic only
npm run check       # project checks (this repo's dependency-free linter)
npm run verify      # check + all tests — run this before committing
npm run serve       # serve the app on a local http origin
```

End-to-end tests drive a real headless Chromium. They find a browser
automatically (including Playwright's download cache) and skip with a clear
message if there is none; set `CHROME_PATH` to point at a specific binary.

- **[CONTRIBUTING.md](CONTRIBUTING.md)** — how to work in this repository:
  test-first workflow, conventions, adding a feature end to end
- **[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** — how the app is put together
- **[docs/TESTING.md](docs/TESTING.md)** — the three test layers and how to use them
- **[docs/DECISIONS.md](docs/DECISIONS.md)** — why it is built this way

## Layout

```
index.html              the entire application (markup, styles, core, UI)
scripts/check.mjs       project checks: this repo's linter
scripts/serve.mjs       local development server
tests/unit/             core logic, one file per module, no browser
tests/contract/         structural promises index.html has to keep
tests/e2e/              the app driven in a real browser
tests/helpers/          harness: script extraction, CDP driver, static server
docs/                   architecture, testing, decisions
```

## Licence

MIT — see [LICENSE](LICENSE).
