# Notepad

A complete notepad that lives in one HTML file. Open `notepad.html` in a
browser and start typing — no install, no build step, no server, no
dependencies, and nothing leaves the machine it runs on.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows
npm run serve              # or serve it at http://localhost:8080
```

## What it does

**Notes** — a sidebar of notes with search, sorting (edited / created / title),
pinning, duplication, renaming, and delete with an undo. Titles come from the
first line unless you set one.

**Editing** — autosave, undo/redo, word wrap, optional line numbers, smart Tab
indentation, list continuation on Enter, duplicate/delete/move/sort lines,
case conversion, markdown bold/italic/code wrappers, insert date and time.

**Find and replace** — literal, whole-word, case-sensitive and regular
expression search, match counts, next/previous, replace one or all, with `$1`
group references in regex mode.

**Markdown preview** — a side-by-side rendering of the note. Note text is always
escaped, so a note can never inject markup into the page.

**Files** — save a note as `.txt`/`.md`, print it, copy it, import text files by
dropping them onto the window, and export or restore every note as a JSON
backup.

**Everything else** — light/dark/system themes, three typefaces, adjustable text
size, a command palette (`Ctrl`/`Cmd` + `K`) that lists every command with its
shortcut, a keyboard shortcut reference (`Ctrl`/`Cmd` + `/`), document
statistics, and a layout that works down to phone width.

Notes are stored in `localStorage`. If a browser blocks storage (private
windows, blocked cookies), the app keeps working in memory and says so in the
status bar rather than failing.

## Working on it

```
npm test          # unit tests for the app's logic (215) — no dependencies needed
npm run check     # structural checks on notepad.html (9)
npm run test:e2e  # Playwright tests that drive the real UI (47)
npm run verify    # all three, in that order
```

`npm test` and `npm run check` run anywhere Node 20+ is installed. The browser
tests need Playwright; without it they print a skip notice and pass. To run
them:

```
npm i -D playwright && npx playwright install chromium
```

## Layout

```
notepad.html          the entire application
test/unit/            unit tests for the logic layer (node:test)
test/e2e/             browser tests for the UI (Playwright)
test/helpers/         loads the logic layer straight out of notepad.html
scripts/              check-app.mjs (structural checks), serve.mjs (dev server)
docs/                 architecture, testing and decision notes
```

Start with [`AGENTS.md`](AGENTS.md) for the conventions,
[`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for how the file is put together,
and [`docs/DECISIONS.md`](docs/DECISIONS.md) for why it is that way.

## Browser support

Current Chrome, Edge, Firefox and Safari. The app uses `<dialog>`, CSS custom
properties, `color-mix()` and `:has()`; older browsers will render a usable but
plainer page.
