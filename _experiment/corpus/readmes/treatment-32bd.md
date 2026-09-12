# Notepad

A notepad that is one file. Open `notepad.html` in a browser and start typing —
no install, no build, no server, no account, no network. Notes are kept in the
browser's local storage, so they are still there next time you open the file.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows
npm run serve              # or serve it at http://localhost:8080
```

## What it does

**Notes** — as many as you like, in a searchable sidebar. Each note takes its
title from an explicit title or from its first line. Notes can be pinned to the
top, duplicated, and deleted (with one-click undo). Sort by last edited, date
created, or title.

**Editing** — word/character/line counts and a live `Ln, Col` readout, selection
stats, per-note undo/redo grouped by word, `Tab`/`Shift+Tab` to indent and
outdent a selection, indentation carried onto new lines, and a date-time stamp
on `F5`.

**Find and replace** — live match counts, next/previous with wrapping, replace
one or all, and optional match-case, whole-word and regular-expression modes
(with `$1` capture groups in replacements). A bad pattern is reported in the bar
rather than thrown.

**Getting text in and out** — export a note as `.txt`, export every note as one
`.json` backup, import `.txt`/`.md`/`.json` files with the Import button or by
dropping them on the window, copy a note to the clipboard, or print it.

**Making it yours** — light/dark/system theme, monospace/sans/serif editor font,
font size, word wrap, spell check, and what `Tab` inserts. Settings are saved
alongside the notes.

**Everything is reachable** — `Ctrl+K` opens a command palette with every
action; `Ctrl+/` lists every shortcut. The app is keyboard navigable and
screen-reader labelled throughout, and it works down to phone width.

## Keyboard shortcuts

On macOS, use `⌘` wherever `Ctrl` is listed.

| Keys | Action |
| --- | --- |
| `Alt+N` or `Ctrl+N` | New note |
| `Alt+D` | Duplicate note |
| `Alt+P` | Pin or unpin note |
| `Alt+ArrowUp` / `Alt+ArrowDown` | Previous / next note |
| `Ctrl+Z` / `Ctrl+Shift+Z` or `Ctrl+Y` | Undo / redo |
| `Ctrl+F` / `Ctrl+H` | Find / find and replace |
| `F3` / `Shift+F3` | Find next / previous |
| `Ctrl+G` | Go to line |
| `F5` | Insert date and time |
| `Ctrl+S` | Save now |
| `Ctrl+Shift+S` | Export note as a text file |
| `Ctrl+P` | Print note |
| `Ctrl+K` | Command palette |
| `Ctrl+/` | Keyboard shortcuts |
| `Ctrl+,` | Settings |
| `Ctrl+Shift+F` | Search notes |
| `Alt+B` | Show or hide the notes list |
| `Alt+T` | Switch between light and dark |
| `Escape` | Close the find bar or a dialog |

Typing is saved automatically a moment after you stop. `Ctrl+S` only forces that
save to happen now — a web page cannot write to your disk on its own, so
`Ctrl+Shift+S` is how you get a real file. Browsers reserve a few of these
combinations for themselves (Chrome keeps `Ctrl+N`, for instance); the command
palette always works.

## Where your notes live

In this browser, under the local-storage key `notepad.v1`, on this origin. That
means:

- Notes do not follow you to another browser, another device, or a private
  window, and clearing site data deletes them.
- Opening the file from a different folder is a different origin to some
  browsers, which will look like an empty notepad. Keep the file where it is, or
  use `npm run serve`.
- If a browser blocks local storage entirely, the app says so in the status bar
  and still works for that session.

Export a `.json` backup from Settings to move notes anywhere; importing it brings
them back.

## Browser support

Any current Chrome, Firefox, Safari or Edge. Nothing newer than widely available
ES2017 is used, there are no external requests, and the only optional API is the
clipboard (the app tells you if it is refused).

## Working on it

```
npm install     # jsdom, the only dependency, and only for tests
npm test        # the whole suite
npm run serve   # http://localhost:8080/notepad.html
```

Tests load the real `notepad.html` in jsdom and drive it with clicks and
keystrokes. Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing anything — it
covers the layering, the test-first loop, and the traps in this setup.

```
notepad.html        the entire application
test/               the suite; test/helpers/harness.mjs boots the app
tools/serve.mjs     static file server for manual checks
CONTRIBUTING.md     how to work in this repository
CLAUDE.md           the short version, for agents
```
