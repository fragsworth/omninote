# Notepad

A complete notepad that is one HTML file. Open `index.html` in a browser and it
works — no install, no build step, no server, no account, no network. Notes are
stored in the browser that opened the file.

```
git clone <this repo>
open index.html          # macOS ("start index.html" on Windows, "xdg-open" on Linux)
```

For local work over `http://` instead of `file://` (handy for trying it on a
phone on the same network):

```
npm run serve            # http://localhost:8080
```

## What it does

**Notes.** Create, rename, duplicate, pin and search notes. The list sorts by
last edited, date created or title, and pinned notes stay on top. A note's name
is its own title if you give it one, otherwise its first line.

**Editing.** Autosave with a save indicator, per-note undo/redo with sensible
grouping, Tab/Shift+Tab to indent, go to line, and a status bar with word,
character and line counts, reading time, selection size and cursor position.

**Find and replace.** Live match count, next/previous with wrapping, match case,
whole word, regular expressions, replace one or replace all (a single undo
step). Every match is highlighted in the text and the current one is ringed.

**Trash.** Deleting moves a note to the trash, where it can be restored or
deleted for good. Anything left there is cleared after 30 days.

**Files.** Save a note as `.txt`, import `.txt`/`.md` files (or drag them onto
the editor), export every note as one JSON backup, and import that backup back
— merging rather than overwriting, so nothing is lost. Printing prints the note,
not the interface.

**Settings.** Light, dark or system theme; monospace, sans or serif; text size
(also Ctrl +/−/0); word wrap; spell check. All remembered.

**Keyboard.** Ctrl+N new, Ctrl+S save as text, Ctrl+F find, Ctrl+H replace,
Ctrl+G go to line, Ctrl+Z / Ctrl+Shift+Z undo/redo, Ctrl+B toggle the list,
Ctrl+/ for the full list. ⌘ on a Mac. Browsers reserve a few combinations for
themselves (Ctrl+N often opens a window) — every shortcut also has a button.

It is usable with a keyboard alone, announces itself to screen readers, keeps
7:1 text contrast in both themes, and reflows to phone width.

## What it deliberately does not do

No accounts, no sync, no cloud, no analytics, no telemetry, no fonts or scripts
from a CDN. Notes never leave the browser they were typed in — which also means
**clearing site data deletes them**, so the JSON backup is the safety net.

Rich text, markdown preview and tags are out of scope: this is a notepad.

## Testing

```
npm install              # dev-only: Playwright, used by the browser tests
npm test                 # unit + guardrail tests (fast, no browser)
npm run test:e2e         # drives real Chromium against index.html
npm run test:all         # everything
```

`npm test` needs nothing but Node ≥ 20.11. The browser suite also needs
Chromium: `npx playwright install chromium` once. If it is missing, that suite
reports itself as skipped rather than failing.

See [docs/TESTING.md](docs/TESTING.md) for how the suites are laid out and
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how the app is built.
Conventions for anyone — human or agent — changing this repository are in
[CLAUDE.md](CLAUDE.md).

## Layout

```
index.html               the entire application
scripts/serve.mjs        optional static server for local development
tests/unit/              pure logic, run in Node (no browser)
tests/guard/             invariants: one file, no dependencies, no build step
tests/e2e/               real-browser behaviour via Playwright
tests/helpers/           test plumbing shared by the suites
docs/                    architecture and testing notes
```

## Browser support

Current Chrome, Edge, Firefox and Safari. It uses `<dialog>`, `:focus-visible`,
`100dvh` and CSS custom properties, so roughly 2022 onwards. Nothing is
transpiled or polyfilled.

## Licence

MIT — see [LICENSE](LICENSE).
