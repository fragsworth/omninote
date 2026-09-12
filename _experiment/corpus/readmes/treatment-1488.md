# Notepad

A notepad that is one HTML file. Open `index.html` in a browser and write. No
install, no build step, no dependencies, no account, no network — notes are
saved in that browser's local storage, on that device, and nowhere else.

```
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
```

Some browsers treat `file://` as an opaque origin and refuse local storage. If
the status bar says the browser blocked storage, serve it instead:

```
npm start                # http://localhost:8080
```

## What it does

- **Many notes.** Create, rename, duplicate, pin, delete (with undo). A note's
  name is the first line of its text unless you type one in the title field.
- **Search everything.** Filter the list as you type; matches are highlighted
  in the results.
- **Find and replace** inside the current note, with match case, whole word and
  regular expressions (capture groups work in replacements).
- **Autosave**, with a status line that tells you the truth: *Saving…*, *Saved*,
  or *Not saved* when the browser blocks storage. `Ctrl+S` saves right now.
- **Import and export.** Every note as a dated `.json` backup, one note as
  `.txt`, or copy to the clipboard. Import `.json` backups and `.txt` files, or
  drop text files onto the editor.
- **Reading comfort.** Light, dark or system theme; sans, serif or monospace;
  text size; word wrap; spell check. All remembered.
- **Keyboard first.** Everything is reachable without a mouse; `Ctrl+/` lists
  the shortcuts.
- **Two tabs stay in sync**, and the whole thing works offline.

### Keyboard shortcuts

| | |
|---|---|
| New note | `Ctrl+N` |
| Save now | `Ctrl+S` |
| Find / find and replace | `Ctrl+F` / `Ctrl+H` |
| Next / previous match | `Enter` / `Shift+Enter` |
| Search all notes | `Ctrl+K` |
| Previous / next note | `Ctrl+Alt+↑` / `Ctrl+Alt+↓` |
| Duplicate note | `Ctrl+D` |
| Pin or unpin note | `Ctrl+Shift+P` |
| Show or hide the note list | `Ctrl+B` |
| Shortcuts | `Ctrl+/` |
| Close find, menus and dialogs | `Esc` |

On a Mac, `Cmd` works wherever this says `Ctrl`.

## Working on it

The app has no dependencies. The *tests* need one (jsdom) and Node 22+.

```
npm install
npm test               # 220+ tests in jsdom, a few seconds
npm run check          # static checks on index.html
npm run verify         # both — what CI runs
npm run test:watch     # while you work
node tools/smoke.mjs   # optional: drives the real file in a real browser
```

Development is test-first. `CLAUDE.md` has the conventions,
`docs/ARCHITECTURE.md` explains how the single file is laid out, and
`docs/TESTING.md` covers the harness and the class of bugs jsdom cannot see —
read it before writing a test.

## Where your notes live

In `localStorage` under the key `notepad.state.v1`, as JSON: the notes, which
one is open, and your settings. Clearing site data deletes them; nothing else
can read them. Use **Export all** for a backup you control.

## Licence

MIT.
