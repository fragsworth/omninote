# Notepad

A notepad that is one file. `index.html` contains the markup, the styles and all
of the JavaScript: no build step, no bundler, no runtime dependencies, no server.
Open it in a browser and it works, from a hard drive, a USB stick or any static
host.

Notes are stored in the browser's `localStorage`, so they stay on the machine
that wrote them.

## Run it

```sh
open index.html          # macOS ("xdg-open index.html" on Linux)
npm run serve            # or serve it at http://localhost:8000
```

## What it does

- **Many notes.** A searchable, sortable list; pin the ones you keep coming back
  to. Titles come from the first line of the note, or rename a note to fix its
  title in place.
- **Saves itself.** Every edit is autosaved (debounced) with an honest indicator
  in the status bar: `Unsaved changes`, `Saved 14:32`, or a warning if the
  browser is out of space or refusing to store anything.
- **Find & replace.** Match case, whole word, and regular expressions with `$1`
  backreferences. Replace-all is a single undo step.
- **Go to line**, live line/column, and counts for lines, words, characters and
  reading time.
- **Undo/redo** that keeps working after programmatic edits, with a separate
  history per note. Quick keystrokes collapse into one undo step; a pause, or a
  newline, starts a new one.
- **Trash, not deletion.** Deleting offers an immediate Undo, and the note waits
  in the trash (30 days) where it can be restored or deleted for good.
- **Import and export.** Download the open note as `.txt`, drag `.txt`/`.md`
  files onto the editor to import them, or export every note as a JSON backup
  and import it again elsewhere.
- **Print** the open note (the print stylesheet prints the text, not the app).
- **Comfortable to look at.** Light, dark or system theme; monospace, sans or
  serif editor font; adjustable size; word wrap and spellcheck toggles. Works on
  a phone, where the note list becomes a drawer.
- **Keyboard first**, with an in-app shortcut reference (<kbd>Ctrl</kbd>+<kbd>/</kbd>).

### Shortcuts

| Action | Keys |
| --- | --- |
| New note | <kbd>Ctrl</kbd>+<kbd>N</kbd> |
| Search notes | <kbd>Ctrl</kbd>+<kbd>K</kbd> |
| Find & replace | <kbd>Ctrl</kbd>+<kbd>F</kbd> / <kbd>Ctrl</kbd>+<kbd>H</kbd> |
| Next / previous match | <kbd>Enter</kbd> / <kbd>Shift</kbd>+<kbd>Enter</kbd> |
| Go to line | <kbd>Ctrl</kbd>+<kbd>G</kbd> |
| Download as `.txt` | <kbd>Ctrl</kbd>+<kbd>S</kbd> |
| Print | <kbd>Ctrl</kbd>+<kbd>P</kbd> |
| Undo / redo | <kbd>Ctrl</kbd>+<kbd>Z</kbd> / <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Z</kbd> |
| Insert date & time | <kbd>F5</kbd> or <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>D</kbd> |
| Show/hide note list | <kbd>Ctrl</kbd>+<kbd>B</kbd> |
| Shortcut reference | <kbd>Ctrl</kbd>+<kbd>/</kbd> |
| Close a panel | <kbd>Esc</kbd> |

On macOS, <kbd>Cmd</kbd> works wherever <kbd>Ctrl</kbd> is listed.

## Where the notes live

Everything is kept under the `localStorage` key `notepad.state` of the origin
serving the page, as a single JSON document with a schema version. Nothing is
sent anywhere. Clearing site data deletes the notes, so use **Settings → Export
all notes** for a backup you can keep.

Opened straight from disk (a `file://` URL), each folder is its own origin, and a
browser configured to block storage for local files will not let the app save. It
still runs, and the status bar says so rather than pretending — serving the folder
(`npm run serve`) or hosting it anywhere static gives you a stable origin.

## Development

```sh
npm install        # only dependency: jsdom, only used by the tests
npm test           # everything: core, browser and structure tests
npm run test:core  # logic only, no dependencies needed
npm run test:dom   # the real index.html driven through jsdom
npm run test:watch # re-run on save
```

```
index.html                the entire application
  <script data-module="core">   pure logic, no DOM, unit tested in Node
  <script data-module="view">   the only code that touches the DOM
tests/core/*.test.mjs     unit tests for the core module
tests/dom/*.test.mjs      browser-level tests through jsdom
tests/structure.test.mjs  the rules the app file must keep obeying
tests/helpers/            the two test harnesses
tools/serve.mjs           dependency-free static server for npm run serve
docs/ARCHITECTURE.md      state, storage schema, DOM contract, test strategy
docs/DECISIONS.md         why things are the way they are
CLAUDE.md                 working agreement for anyone (human or agent) editing this
```

This project is written test-first. Before changing behaviour, read
[CLAUDE.md](CLAUDE.md) — it is short, and it explains the loop, the invariants
and the traps in the test harness.

## Browser support

Any current Chrome, Firefox, Safari or Edge. The app uses `localStorage`,
`Blob`, object URLs and optional chaining; there is no transpilation and no
polyfill. It degrades honestly: if storage is unavailable the app still runs and
says so in the status bar.
