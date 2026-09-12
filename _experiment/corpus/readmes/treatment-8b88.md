# Notepad

A plain-text notepad in **one HTML file**. No dependencies, no build step, no server, no
account. Open `notepad.html` in a browser and start writing; every note is stored in that
browser's local storage on that device, and nothing is ever sent anywhere.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows
```

Or serve it over http (handy on browsers that restrict storage on `file://` pages):

```
npm run serve              # http://127.0.0.1:8080/notepad.html
```

## What it does

**Notes**
- Many notes with a searchable, sortable list; search matches titles and body text
- A note is named by its first line until you type a title of your own
- Pin notes to the top, duplicate them, delete with an **Undo** that puts the note back
  where it was
- Sort by last edited, date created, or title (A–Z, with natural number ordering)

**Writing**
- Autosave while you type (debounced), a save-state indicator, and `Ctrl+S` to flush now
- Find and replace with match counts, match case, whole word, wrap-around, replace all
- Go to line, insert date and time, word wrap on/off, spell check on/off
- Status bar: line and column, words, characters, lines, reading time, last save
- Native undo/redo (`Ctrl+Z` / `Ctrl+Y`) inside the editor

**Your data**
- Save a note as `.txt`, back up everything as `.json`, restore a backup (importing the
  same backup twice adds nothing), drag and drop text files in to add them as notes
- Print the open note
- Edits in one tab appear in the others, and two tabs editing at once merge rather
  than overwrite each other
- If storage is unavailable, full, or damaged, the app says so plainly and keeps working
  instead of losing your text

**Comfort**
- Light and dark themes (following the OS by default), adjustable text size, monospace
  option, collapsible note list, phone-friendly layout
- Keyboard-first: menus with arrow-key navigation, labelled controls, visible focus,
  reduced-motion support

## Keyboard shortcuts

| Action | Shortcut |
| --- | --- |
| New note | `Ctrl+Alt+N` |
| Delete note (undoable) | `Ctrl+Alt+Backspace` |
| Pin or unpin note | `Ctrl+Alt+P` |
| Search all notes | `Ctrl+K` |
| Previous / next note | `Alt+↑` / `Alt+↓` |
| Save now | `Ctrl+S` |
| Find and replace | `Ctrl+F` |
| Find next / previous | `F3` / `Shift+F3` |
| Go to line | `Ctrl+G` |
| Insert date and time | `Ctrl+Alt+D` |
| Word wrap on or off | `Ctrl+Alt+W` |
| Larger / smaller text | `Ctrl++` / `Ctrl+-` |
| Close find bar or dialog | `Esc` |
| Shortcut reference | `F1` |

`Ctrl+N`, `Ctrl+T` and friends are reserved by browsers and cannot be intercepted, which
is why note commands use `Ctrl+Alt`. On macOS, `Cmd` works wherever `Ctrl` is listed.

## Where notes live

In `localStorage` under the key `notepad:state:v1`, as a single JSON document (schema in
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)). Consequences worth knowing:

- Notes are per-browser and per-device. They do not sync.
- Clearing site data or browsing history for this page erases them.
- Private windows usually discard them when the window closes.
- **File → Back up all notes** writes a `.json` file you own; **Restore backup** reads it
  back, in any browser.

## Repository layout

```
notepad.html            the whole application — the only file that ships
package.json            test scripts only; there are no dependencies
scripts/serve.mjs       zero-dependency static server (npm run serve, and the e2e tests)
tests/
  helpers/              test-side plumbing: app loader, fakes, browser harness
  unit/                 the core, run in Node with no browser
  integrity/            guards on the single-file promise
  e2e/                  real Chromium driving the real file
docs/
  ARCHITECTURE.md       how the file is organised, data model, invariants
  DECISIONS.md          why it is built this way
CONTRIBUTING.md         the working agreement for changes
CLAUDE.md               short brief for AI agents working here
.github/workflows/ci.yml  unit tests on Node 20/22/24, browser tests on Chromium
```

## Tests

```
npm test          # everything: unit + integrity + browser
npm run test:unit # unit + integrity only — no browser needed, fast
npm run test:e2e  # browser tests only
npm run test:watch
```

Requires Node 20.10 or newer. Nothing to install: the suite uses `node:test` only.

The unit tests read `notepad.html`, extract its inline `<script>` and evaluate it with no
DOM, so they exercise **the code that actually ships** rather than a copy. The browser
tests drive the real file in Chromium through Playwright if a copy is already installed on
the machine; if not, they report themselves as skipped with the command that enables them
(`npm i -D playwright && npx playwright install chromium`) and the rest of the suite still
runs and still passes.

New work here is test-first — see [CONTRIBUTING.md](CONTRIBUTING.md).

## Browser support

The browser suite runs on Chromium, which is what is verified on every change. The app is
written for current Chrome, Edge, Firefox and Safari — it uses `<dialog>`, `File.text()`,
`Intl.Collator`, CSS custom properties and regular-expression lookbehind, all of which
those browsers have shipped for years — with no polyfills and no transpilation.

To check another engine, install it and run the same suite against it:

```
npx playwright install firefox
NOTEPAD_E2E_BROWSER=firefox npm run test:e2e
```
