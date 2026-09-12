# Notepad

A complete note-taking app in **one HTML file**. No build step, no bundler, no
runtime dependencies, no network calls. Open `notepad.html` in a browser and it
works; notes live in that browser's `localStorage` and never leave the machine.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows
```

Or serve it over http, which some browsers require before they will hand out
`localStorage` on a `file://` page:

```
npm run serve              # http://localhost:8080/notepad.html
```

## What it does

**Notes**
- Many notes in a sidebar, with live search across titles and bodies (matches
  are highlighted in the list)
- Titles come from the first line automatically, or set one explicitly with
  *Rename*
- Pin notes to the top, duplicate them, sort by last edited / date created /
  title
- `#hashtags` written in a note become filter chips in the sidebar
- Trash with undo: deleting is reversible, trashed notes can be read before
  they are restored, and they are removed for good after 30 days

**Editing**
- Autosave (400 ms after you stop typing) with a live saved / editing indicator
- Find and replace with match case, whole word, next/previous, replace all
- `Tab` indents, `Shift+Tab` outdents, and both keep the browser's native undo
- Live word, character, line, caret-position, selection and reading-time counts
- Word wrap, font family, and font size settings; light / dark / system theme

**Getting notes in and out**
- Download the open note as `.txt` or `.md`, or export every note as JSON
- Import a JSON export back (newer copies win, nothing is silently overwritten)
- Drop `.txt`, `.md` or `.json` files onto the window to add them
- Print the open note (printing is wired to a mirror element, so the whole note
  prints, not just the visible part of the textarea)

**Everything else**
- Keyboard-first: press <kbd>?</kbd> in the app for the full list
- Works offline, on phones, and in two tabs at once (changes in one tab appear
  in the other without clobbering unsaved edits)
- Degrades gracefully: if the browser refuses storage the app says so and stays
  usable; unreadable saved data is backed up rather than thrown away

## Working on it

```
npm install      # jsdom, the only dev dependency
npm test         # the whole suite
npm run test:core   # pure logic only (fast)
npm run test:ui     # the app running in jsdom
npm run test:watch  # re-run on change
```

Tests boot the real `notepad.html` inside jsdom, so they exercise the file that
ships rather than a copy of its logic.

## Layout

```
notepad.html              the entire application
tests/
  helpers/harness.mjs     boots notepad.html in jsdom, plus query/click/type helpers
  core.*.test.mjs         pure logic: notes, text, search, state and storage
  ui.*.test.mjs           the app running: editing, list, find, preferences
  constraints.test.mjs    guards the "single dependency-free file" promise
scripts/serve.mjs         zero-dependency static server
docs/ARCHITECTURE.md      how notepad.html is put together, and why
CONTRIBUTING.md           how to work in this repository
```

Start with [CONTRIBUTING.md](CONTRIBUTING.md) before changing anything, and
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) when you need the internals.
