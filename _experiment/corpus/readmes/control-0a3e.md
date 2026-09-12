# Notepad

A plain-text notepad that lives in **one HTML file**. Open `index.html` in a
browser and start typing — no server, no build step, no dependencies, no
accounts, nothing uploaded anywhere. Notes are saved in the browser as you type.

```
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
npm run open             # any of the above, from this repo
```

## What it does

**Notes**

- Many notes with a searchable, sortable sidebar (last edited / created / title)
- Titles derive from the first line automatically, or rename a note yourself
- Pin notes to keep them at the top
- Delete moves to a trash that holds the last 25 notes; restore or purge them
- Undo toast right after a delete
- Autosave with an explicit "Saved 14:03" indicator, plus `Ctrl+S` to flush now

**Editing**

- Find and replace: case sensitivity, whole word, regular expressions with `$1`
  capture groups, match counter, next/previous, replace one or all
- Go to line, select all, insert date and time
- Tab indents, `Shift+Tab` outdents, across a multi-line selection
- Live status bar: line and column, words, characters, lines, reading time,
  selection size, storage used

**Files**

- Download the current note as `.txt` or `.md`, or export every note as one
  markdown file
- Open text files with `Ctrl+O` or by dropping them onto the window
- Print with a clean, chrome-free print stylesheet

**Appearance**

- Light / dark / follow-the-system themes
- Monospace, sans or serif editor font; zoom from 10px to 32px
- Word wrap, spell check, status bar and sidebar toggles, focus mode
- Works down to phone width, where the note list becomes a drawer
- Keyboard accessible throughout: menus, note list, dialogs, live regions

## Keyboard shortcuts

| Keys | Action |
| --- | --- |
| `Ctrl+N` / `Ctrl+Alt+N` | New note |
| `Ctrl+D` | Duplicate note |
| `Ctrl+O` | Open a text file |
| `Ctrl+S` | Save to this browser now |
| `Ctrl+Shift+S` | Download as `.txt` |
| `Ctrl+P` | Print |
| `Ctrl+F` / `Ctrl+H` | Find / find and replace |
| `F3` / `Shift+F3` | Find next / previous |
| `Ctrl+G` | Go to line |
| `Ctrl+Shift+D` or `F5` | Insert date and time |
| `Ctrl+Shift+C` | Copy the whole note |
| `Ctrl+B` | Show or hide the note list |
| `Ctrl+Shift+W` | Toggle word wrap |
| `Ctrl+Shift+F` | Focus mode |
| `Ctrl+Plus` / `Ctrl+Minus` / `Ctrl+0` | Zoom in / out / reset |
| `Ctrl+Shift+Backspace` | Move note to trash |
| `Ctrl+/` | Show every shortcut |

On macOS use `⌘` instead of `Ctrl`. The in-app list (`Ctrl+/`) is generated from
the keymap, so it can never drift. Chrome and Firefox reserve `Ctrl+N` for a new
window; `Ctrl+Alt+N` always reaches the app.

## Where notes live

Everything is kept in `localStorage` under the key `notepad.state.v2`, as a
single JSON blob: notes, trash, the selected note and your preferences. It never
leaves the device, and different browsers or profiles do not share it.

Clearing site data deletes your notes, so export anything you want to keep
(**File → Export all notes**). Data written by an older version is migrated on
load; unreadable data falls back to a fresh notepad rather than an error. If a
browser blocks storage entirely the app still runs, and says so in the status
bar.

## Repository layout

```
index.html                    the entire application (core logic + view)
tests/
  helpers/load-core.mjs       loads the pure core out of index.html for Node
  helpers/browser.mjs         Playwright harness for the browser tests
  unit/*.test.mjs             pure logic + static contract tests (no browser)
  e2e/app.test.mjs            the real file driven in Chromium
docs/ARCHITECTURE.md          how the app is put together
docs/TESTING.md               how the test setup works and how to extend it
docs/DECISIONS.md             why it is built this way
CLAUDE.md                     working agreements for anyone changing this repo
scripts/open.mjs              opens index.html in your browser
```

## Development

```
npm test           # unit + contract tests, ~150 of them, no dependencies
npm run test:watch # the same, re-run on change
npm run test:e2e   # Chromium tests (needs Playwright; skips politely if absent)
npm run test:all   # both
```

The unit suite runs on Node 20+ with **no `npm install`** — it uses the built-in
test runner and reads `index.html` directly. The browser suite needs Playwright:

```
npm i -D playwright && npx playwright install chromium
```

Work test-first: `docs/TESTING.md` explains the three tiers and
[CLAUDE.md](CLAUDE.md) has step-by-step recipes for adding a command, a
shortcut, a setting or a storage migration.

## Browser support

Any current Chrome, Edge, Firefox or Safari. Uses `<dialog>`, `structuredClone`-
free plain objects, CSS custom properties and `localStorage`; no polyfills.

## License

MIT — see [LICENSE](LICENSE).
