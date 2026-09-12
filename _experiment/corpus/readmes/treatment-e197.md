# Notepad

A plain-text notepad that is one HTML file. Open `index.html` in a browser and
write. No install, no build, no server, no network, no accounts. Notes are kept
in the browser's local storage and can be downloaded or exported at any time.

```
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
```

## What it does

**Writing**

- Multiple notes, with autosave (nothing to press, ever).
- Titles are optional: a note is named after its first line until you name it.
- Undo and redo that group typing sensibly - one undo removes a word, not a
  letter, and a paste or a Replace All is a single step.
- Tab and Shift+Tab indent and outdent, including whole selected blocks.
- Live status bar: line and column, words, characters, lines, reading time.
- Jump to a line number, and stamp the date and time into a note.

**Finding**

- Find and replace inside the open note: literal, whole word, or regular
  expression with `$1`-style capture groups in the replacement.
- Match counter (`3 of 12`), wrap-around, Replace and Replace All.
- Search across all notes from the sidebar, with the matching text highlighted.

**Keeping**

- Notes are saved locally and restored when you come back.
- Delete is undoable, and deleted notes stay recoverable after a reload.
- Download the open note as `.txt`, export everything as JSON, import `.txt`,
  `.md` or a previously exported bundle (dragging files onto the editor works).
- If another tab changes your notes, this one offers to load them instead of
  quietly overwriting.
- If the browser refuses to store anything (private mode, full quota), the app
  says so plainly and keeps working in memory.

**Reading**

- Light, dark, or follow the system.
- Serif, sans or monospace; adjustable text size; word wrap on or off.
- Responsive: on a phone the note list becomes a drawer.
- Keyboard-driven throughout; press <kbd>?</kbd> for the full list.
- Printing prints the note, not the interface.

| Shortcut | Action |
| --- | --- |
| <kbd>Ctrl</kbd>+<kbd>N</kbd> | New note |
| <kbd>Ctrl</kbd>+<kbd>S</kbd> | Download the note |
| <kbd>Ctrl</kbd>+<kbd>F</kbd> / <kbd>Ctrl</kbd>+<kbd>H</kbd> | Find / find and replace |
| <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>F</kbd> | Search all notes |
| <kbd>Ctrl</kbd>+<kbd>G</kbd> | Go to line |
| <kbd>F5</kbd> | Insert the date and time |
| <kbd>Ctrl</kbd>+<kbd>Z</kbd> / <kbd>Ctrl</kbd>+<kbd>Shift</kbd>+<kbd>Z</kbd> | Undo / redo |
| <kbd>Alt</kbd>+<kbd>↑</kbd> / <kbd>Alt</kbd>+<kbd>↓</kbd> | Previous / next note |
| <kbd>Ctrl</kbd>+<kbd>B</kbd> | Show or hide the note list |
| <kbd>Esc</kbd> | Close whatever is open |

On macOS, <kbd>⌘</kbd> works wherever <kbd>Ctrl</kbd> is listed.

## Working on it

```bash
npm install        # one dev dependency: jsdom
npm test           # the full suite: contract, core and jsdom UI tests
npm run check      # lint + tests + browser tests: the gate before committing
npm run serve      # optional: serve the folder over http
```

This project is developed test-first: write the failing test, then the code.
`CONTRIBUTING.md` describes the workflow, and `docs/ARCHITECTURE.md` explains
how the app is put together and where to add things.

## Layout

```
index.html              the entire application: markup, styles, two scripts
  <script id="notepad-core">   pure logic - no DOM, no storage, no timers
  <script id="notepad-ui">     everything that touches the browser
test/contract/          the rules that keep the project honest
test/core/              unit tests for the pure logic (no DOM)
test/ui/                the real index.html driven through jsdom
test/browser/           layout and paint in Chromium (skipped when absent)
scripts/lint.mjs        dependency-free lint pass
scripts/serve.mjs       optional static file server
docs/ARCHITECTURE.md    design, data model, extension points
```

## Constraints

These are enforced by `test/contract`, not merely written down:

1. The application is a single HTML file that runs from `file://`.
2. It loads nothing over the network - no CDN, no fonts, no frameworks.
3. There is no build step. What you edit is what ships.
4. The core logic block never touches the DOM, storage or timers.

Browser support: any current browser (Chrome, Edge, Firefox, Safari). The app
feature-detects everything optional, so it still works where `matchMedia`, blob
URLs or local storage are unavailable.
