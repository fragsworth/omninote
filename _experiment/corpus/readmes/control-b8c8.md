# Notepad

A notepad that is one HTML file. Open `notepad.html` in a browser and it works —
no install, no build step, no server, no account, no network. Your notes are
saved in that browser's local storage and never leave the machine.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows
```

Or serve it, which is worth doing because some browsers deny local storage to
`file://` pages:

```
npm start                  # http://localhost:8080
```

## What it does

**Notes** — as many as you like, in a sidebar list. Create, rename, duplicate,
pin to the top, delete (with a confirmation), and search across every note's
title and body. Sort by last edited, date created, or title. Untitled notes take
their name from their first line, so you rarely have to name anything.

**Editing** — a plain-text editor with word wrap, adjustable text size, Tab and
Shift+Tab indentation, an insert-date-and-time key, and its own undo/redo
history that survives switching between notes.

**Find and replace** — in the current note, with match counts, next/previous,
match case, whole word, replace, and replace all as one undo step.

**Saving** — automatic, a moment after you stop typing, with a status in the
bottom-right. If the browser refuses to store anything (private browsing, say),
the app says so instead of losing your work quietly.

**Files** — download a note as `.txt`, open a `.txt` file as a new note (or drop
one on the window), back up every note to JSON, restore from that JSON, print,
and copy the whole note to the clipboard.

**The rest** — light/dark/system themes, a phone layout where the list becomes a
drawer, a live status bar (line and column, selection size, words, characters,
lines), and a keyboard shortcut sheet on `F1`.

### Keyboard shortcuts

| Keys | Action |
| --- | --- |
| `Ctrl+N` | New note |
| `Ctrl+S` | Download this note as `.txt` |
| `Ctrl+PageDown` / `Ctrl+PageUp` | Next / previous note |
| `Ctrl+Shift+F` | Search all notes |
| `Ctrl+Z` / `Ctrl+Y` | Undo / redo (also `Ctrl+Shift+Z`) |
| `Tab` / `Shift+Tab` | Indent / outdent |
| `Esc` then `Tab` | Move focus out of the text |
| `F5` | Insert date and time |
| `Ctrl+F` / `Ctrl+H` | Find / find and replace |
| `F3` / `Shift+F3` | Next / previous match |
| `Ctrl+=` / `Ctrl+-` / `Ctrl+0` | Bigger / smaller / reset text |
| `F1` or `Ctrl+/` | Shortcut sheet |
| `Esc` | Close find, dialogs, and search |

On macOS use `Cmd` wherever this says `Ctrl`.

## Where the notes live

In `localStorage` under the key `notepad.state.v1`, as JSON: every note, plus
which one was open and your display settings. Nothing is sent anywhere; there is
no server to send it to. Clearing site data deletes your notes, so use **Backup**
if they matter. A backup is a plain JSON file you can restore into any copy of
this app.

Unreadable or partly damaged storage never blocks startup: whatever can be read
is kept, the rest is skipped, and the app tells you what happened.

## Working on it

```
npm install     # jsdom, used only by the tests
npm test        # the whole suite, run against notepad.html itself
npm run lint    # syntax and house rules, no dependencies
npm run smoke   # optional: real Chromium, needs playwright installed globally
npm start       # serve the app on :8080
```

The tests load the real `notepad.html` into jsdom, so there is no second copy of
the code and nothing to keep in sync. Development is test-first — see
[CLAUDE.md](CLAUDE.md) for the working agreement and
[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how the file is put together.

## Browser support

Any current version of Chrome, Firefox, Safari, or Edge. The app uses no
frameworks and no build step; the newest CSS it relies on (`color-mix`, `dvh`)
degrades to a still-usable page in older engines.
