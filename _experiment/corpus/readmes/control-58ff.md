# Notepad

A plain-text notes app in **one HTML file**. Open `notepad.html` in a browser and it
works — no server, no build step, no dependencies, nothing loaded from the network.
Notes are stored in that browser's `localStorage`.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows
```

## What it does

| Area | Features |
| --- | --- |
| Notes | Multiple notes, create, rename, delete (with undo), pin to top, sort by recent / created / title |
| Editing | Autosave as you type, explicit save, `Ln`/`Col` and word / character / line / selection counts, `Tab` inserts a tab |
| Finding | Sidebar search across titles and bodies (all terms must match), find & replace in the open note with match-case and replace-all |
| Files | Import `.txt` / `.md` (button or drag-and-drop), export a note as `.txt`, export/restore every note as a JSON backup |
| View | Light / dark / follow-the-system theme, word wrap, sans or monospace, font size, print just the note |
| Keyboard | `Ctrl+Alt+N` new, `Ctrl+S` save, `Ctrl+K` search, `Ctrl+F` find, `F3` find again, `Esc` back to the text, `Alt+↑/↓` switch notes, `Alt+ +/-/0` text size, `F1` shortcuts — full list in the app |
| Care | Survives a blocked or full `localStorage`, repairs corrupt stored data, offers (never forces) changes made in another tab, one-step undo for destructive actions |

Notes never leave the browser. There is no account, no sync, and no network code in
the file — which also means clearing site data deletes them, so the **Backup** button
exists for a reason.

## Working on it

```bash
npm install        # once: jsdom, the only dev dependency
npm test           # the whole suite (123 cases, a few seconds)
npm run test:watch # re-run on change
```

Tests load the real `notepad.html` into [jsdom](https://github.com/jsdom/jsdom) and
drive it through clicks, typed text and keystrokes. There is no build and no separate
test bundle: the file the tests exercise is the file you ship.

**This project is test-driven.** Write the failing test first, watch it fail, then make
it pass. See [`CLAUDE.md`](CLAUDE.md) for the working agreement and
[`docs/`](docs/) for the details:

- [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) — how `notepad.html` is laid out, the data model, the DOM contract
- [`docs/TESTING.md`](docs/TESTING.md) — the harness, jsdom's gaps, how to write a test here
- [`docs/DECISIONS.md`](docs/DECISIONS.md) — why it is built this way
- [`docs/MANUAL-QA.md`](docs/MANUAL-QA.md) — the short list of things jsdom cannot check, for release day

## Layout

```
notepad.html                 the entire application (markup, CSS, JS)
tests/
  helpers/harness.mjs        loads the app into jsdom, user-level helpers
  core.test.mjs              pure helpers: model, stats, search, find, (de)serialisation
  notes.test.mjs             create / edit / switch / pin / delete / search / sort / persist
  find-replace.test.mjs      the find bar
  settings.test.mjs          theme, wrap, font, size
  shortcuts.test.mjs         keyboard, dialogs, focus
  import-export.test.mjs     .txt/.md import, note export, JSON backup & restore
  lifecycle.test.mjs         save-on-exit, cross-tab changes, print view
  robustness.test.mjs        injection, odd ids, huge notes, many notes, unicode
  journey.test.mjs           one long session that exercises the whole app
  storage.test.mjs           blocked and full localStorage
  app-contract.test.mjs      one file, no network, accessible names, public API
docs/                        architecture, testing, decisions, manual QA
```

## Browser support

Evergreen Chrome, Firefox, Safari and Edge. Nothing newer than ES2020 syntax is used,
every optional browser API is feature-detected (`matchMedia`, `execCommand`,
`URL.createObjectURL`, `Blob.text`), and the app degrades to an in-memory session if
storage is unavailable.
