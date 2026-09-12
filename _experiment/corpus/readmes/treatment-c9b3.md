# Notepad

A plain-text notepad that is one HTML file. Open `index.html` in a browser and
it works — no server, no build step, no dependencies, no network. Notes live in
the browser's `localStorage`; nothing is ever sent anywhere.

```
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
```

## What it does

- **Many notes** in a sidebar, with search, sorting (last updated / date
  created / title) and pinning.
- **Autosave** as you type, with a save indicator and `Ctrl+S` to flush now.
- **Titles** that follow the first line of the note until you rename it by hand.
- **Find and replace** inside a note (`Ctrl+F`), with match case, next/previous,
  replace and replace all.
- **Status bar**: caret line/column, selection size, word, character and line
  counts.
- **Delete with undo** — a toast offers the note back for a few seconds.
- **Import and export**: download a note as `.txt`, back every note up as one
  JSON file, add notes back from `.txt`/`.md`/`.json` files.
- **Print** just the note, without the app chrome.
- **View settings**: light / dark / system theme, three text sizes, monospace
  toggle, word wrap toggle, and whether <kbd>Tab</kbd> inserts a tab character.
- **Keyboard first**: every action has a shortcut; `Ctrl+/` lists them.
- **Degrades gracefully**: private-mode browsers with storage blocked still let
  you write and export; corrupt or older saved data is repaired on load.

## Keyboard shortcuts

| Action | Keys |
| --- | --- |
| New note | <kbd>Alt</kbd> <kbd>N</kbd> |
| Search notes | <kbd>Alt</kbd> <kbd>F</kbd> |
| Next / previous note | <kbd>Alt</kbd> <kbd>↓</kbd> / <kbd>Alt</kbd> <kbd>↑</kbd> |
| Show or hide the notes list | <kbd>Alt</kbd> <kbd>B</kbd> |
| Save now | <kbd>Ctrl</kbd> <kbd>S</kbd> |
| Find and replace | <kbd>Ctrl</kbd> <kbd>F</kbd> |
| Print | <kbd>Ctrl</kbd> <kbd>P</kbd> |
| Shortcut list | <kbd>Ctrl</kbd> <kbd>/</kbd> |
| Close a panel, or leave the text area | <kbd>Esc</kbd> |

On a Mac, <kbd>Cmd</kbd> works wherever <kbd>Ctrl</kbd> is listed.

## Development

The app has no dependencies. The *tests* need Node 22+ and jsdom.

```bash
npm install        # jsdom, for the test suite only
npm test           # the whole suite
npm run test:watch # re-run on change
npm run test:only test/editor.test.mjs   # one file
```

Tests load the real `index.html` into jsdom and drive it the way a person
would: typing, clicking, pressing keys. There is nothing to build, so what the
tests exercise is exactly what ships.

jsdom has no layout engine, so it cannot see clipped menus, overflowing
toolbars or unreadable hover states. For those there is an opt-in check against
real Chromium:

```bash
npm install --no-save playwright-core
npx playwright install chromium     # or set CHROME_PATH
npm run browser-check               # also writes tmp/screenshots/
```

## Repository layout

```
index.html                 the entire application (markup, CSS, JS)
test/                      node:test + jsdom suite
  helpers/dom.mjs          harness: loads the app, selectors, DOM helpers
  core.test.mjs            pure helpers (counts, titles, find, slugs, dates)
  store.test.mjs           note store and persisted-state migration
  boot.test.mjs            first run, restore, corrupt data, no storage
  editor.test.mjs          typing, autosave, titles, status bar, settings
  notes-list.test.mjs      sidebar: create, switch, search, sort, pin, delete
  find-replace.test.mjs    the find bar
  io.test.mjs              download, backup, import, print
  a11y.test.mjs            names, roles, live regions, focus handling
  source-contract.test.mjs the "one file, no network, no build" promises
scripts/browser-check.mjs  optional Chromium layout check
docs/ARCHITECTURE.md       how index.html is organised, data model, storage
docs/DECISIONS.md          why the notable choices were made
CONTRIBUTING.md            working agreements for contributors
CLAUDE.md                  the same, condensed, for coding agents
```

## Browser support

Anything current: Chrome, Edge, Firefox, Safari. The app uses no modules, no
build output, and no APIs newer than `localStorage`, `Blob` and
`crypto.randomUUID` — each feature-detected before use.

## Privacy

Everything stays in the browser profile that opened the file. There is no
account, no sync and no telemetry; the app makes no network requests at all,
which the test suite enforces.
