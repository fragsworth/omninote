# Notepad

A notepad that lives in one HTML file. Open `notepad.html` in a browser and start
typing — no server, no build step, no dependencies, no account. Notes are saved in
that browser's `localStorage` as you type.

```
┌───────────────────────────────────────────────────────────────┐
│ =  Notepad          Saved             [+ New]  [find]  [...]  │
├──────────────────────┬────────────────────────────────────────┤
│ Search notes...      │  Apple pie                             │
│──────────────────────│  butter, flour, a cold morning         │
│ > Apple pie      pin │                                        │
│   Banana bread       │                                        │
│   Cherry jam         │                                        │
│                      │                                        │
│ 3 notes              │  Ln 2, Col 31 · 6 words · 42 chars     │
└──────────────────────┴────────────────────────────────────────┘
```

## Run it

```sh
open notepad.html        # macOS
xdg-open notepad.html    # Linux
```

Or double-click the file. It works from a `file://` URL with no network access.

## Run the tests

```sh
npm install   # jsdom, for the tests only — the app itself has no dependencies
npm test
```

`npm run test:watch` re-runs on save. See [docs/TESTING.md](docs/TESTING.md).

## What it does

- **Many notes** in a sidebar, most recently edited first, with pinning.
- **Autosave** to `localStorage`, debounced, with a save indicator and `Ctrl+S` to flush.
- **Titles come from the text** — the first non-empty line names the note.
- **Search** across every note (all terms must match) and **find/replace** inside one.
- **Delete with undo** — no confirmation dialogs; a toast offers the note back.
- **Export** one note as `.txt`/`.md` or everything as `.json`; **import** merges a
  `.json` export back in, the newest version of each note winning.
- **Preferences that stick**: theme (system/light/dark), word wrap, editor font,
  text size, sort order, sidebar visibility.
- **Status bar** with cursor position, word and character counts, and last-edited time.
- **Small conveniences**: insert the date and time at the cursor, copy a note to the
  clipboard, duplicate a note, `Tab` indents instead of escaping the note.
- **Keyboard first** (`Ctrl+/` lists every shortcut), **screen-reader labelled**,
  **responsive** down to phone width, and it prints just the note.

## Keyboard shortcuts

| Keys | Action |
|---|---|
| `Ctrl+N` / `Alt+N` | New note |
| `Ctrl+S` | Save now |
| `Ctrl+K` | Search all notes |
| `Ctrl+F` | Find in note |
| `Ctrl+H` | Find and replace |
| `Enter` / `Shift+Enter` | Next / previous match (from the find bar) |
| `Alt+Down` / `Alt+Up` | Next / previous note |
| `Alt+P` | Pin or unpin |
| `Alt+D` | Duplicate |
| `Alt+;` | Insert date and time |
| `Alt+Delete` / `Ctrl+Shift+D` | Delete note |
| `Alt+W` | Word wrap |
| `Alt+T` | Cycle theme |
| `Alt+S` | Show or hide the note list |
| `Ctrl+/` or `?` | Shortcut list |
| `Esc` | Close the top-most bar, menu or dialog |

On macOS use `Cmd` instead of `Ctrl`. A few browsers keep `Ctrl+N` for themselves;
`Alt+N` always reaches Notepad.

## Where things live

```
notepad.html          the whole application (markup, styles, logic)
tests/                node:test + jsdom suite that drives the real file
  helpers/harness.js  boots notepad.html in jsdom; every test goes through it
docs/ARCHITECTURE.md  how the file is organised, the data model, the test seam
docs/TESTING.md       how to write tests here
docs/DECISIONS.md     why it is built this way
CLAUDE.md             conventions for whoever works on this next
```

## Known limitations

- **One browser, one device.** Notes live in `localStorage`; they do not sync, and
  clearing site data deletes them. Export regularly if they matter.
- **No live sync between tabs.** Two tabs open on the same profile will overwrite
  each other's most recent changes. See [docs/DECISIONS.md](docs/DECISIONS.md).
- **`Ctrl+Z` after find-and-replace** can undo more than the replacement, because a
  programmatic edit resets the textarea's native undo stack.
- **No rich text.** Plain text only, by design.
