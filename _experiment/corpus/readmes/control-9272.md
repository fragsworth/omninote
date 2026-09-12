# Notepad

A complete notepad that is one HTML file. Open `index.html` in a browser and
write. No install, no build, no server, no account, no network calls — your
notes live in that browser's local storage and nowhere else.

```
git clone <this repo>
open index.html          # macOS  (or: xdg-open index.html / double-click it)
```

Some browsers refuse `localStorage` on `file://` URLs, which silently turns off
saving. The app detects that, tells you, and keeps working in memory for the
session. To get persistence in those browsers, serve the folder instead:

```
npm start                # http://localhost:8080
```

## What it does

**Notes.** As many as you like, in a searchable sidebar. Sort by recently
edited, date created or title; pin the ones you keep coming back to. The title
is the first line of the note, or type your own in the toolbar.

**Editing.** Autosave as you type, word wrap, adjustable font size and family,
spellcheck toggle, and a status bar with line/column, selection size, word,
character and line counts. Lists keep themselves going when you press Enter;
Tab indents the selected lines; lines can be duplicated, deleted and moved.

**Find and replace.** Match case, whole word, and regular expressions (with
`$1` backreferences in the replacement). `F3` and `Shift+F3` walk the matches.

**Files.** Open `.txt`/`.md` files (or drag them onto the editor), save the
current note as a text file, print it, export every note as a JSON backup, and
import one back.

**Comfort.** Light and dark themes that follow the system by default, full
keyboard control, screen-reader labels, and a layout that works down to phone
width.

## Keyboard shortcuts

On macOS use ⌘ wherever this says Ctrl. Press `F1` in the app for the same list.

| | |
| --- | --- |
| New note | `Ctrl+Alt+N` |
| Next / previous note | `Ctrl+PgDn` / `Ctrl+PgUp` |
| Open text file | `Ctrl+O` |
| Save note to file | `Ctrl+S` |
| Save a dated copy | `Ctrl+Shift+S` |
| Print | `Ctrl+P` |
| Find | `Ctrl+F` |
| Find and replace | `Ctrl+H` |
| Next / previous match | `F3` / `Shift+F3` |
| Go to line | `Ctrl+G` |
| Insert date and time | `Ctrl+;` |
| Indent / outdent | `Tab` / `Shift+Tab` |
| Duplicate / delete line | `Ctrl+Shift+D` / `Ctrl+Shift+K` |
| Move line up / down | `Alt+↑` / `Alt+↓` |
| Show or hide the note list | `Ctrl+B` |
| Word wrap | `Alt+Z` |
| Text size | `Ctrl+=` / `Ctrl+-` / `Ctrl+0` |
| Keyboard shortcuts | `F1` |

Undo and redo are the browser's own (`Ctrl+Z` / `Ctrl+Y`) — even the scripted
edits like "move line up" go through the native undo stack.

`Ctrl+N`, `Ctrl+T` and `Ctrl+W` are deliberately left alone: browsers keep those
for themselves and a page cannot intercept them.

## Working on it

The app ships as `index.html` with no dependencies. The tooling around it is
Node 20+ and, for the DOM tests, jsdom.

```
npm install        # jsdom, for the integration tests
npm test           # the whole suite, about two seconds
npm run test:unit  # pure logic + single-file constraints (no jsdom needed)
npm run test:dom   # jsdom integration tests
npm run lint       # whitespace, syntax, script structure
npm run check      # lint + test, what CI runs
npm start          # static server on :8080
npm run smoke      # optional: real Chromium pass, writes artifacts/*.png
```

Tests come first here — see [docs/TESTING.md](docs/TESTING.md) for the loop and
the harness, and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how one file
stays testable. [CLAUDE.md](CLAUDE.md) is the short version for anyone (human or
agent) picking the repo up cold.

## Privacy

Everything stays in the browser under the `notepad:state` key in `localStorage`.
There is no telemetry, no fonts or scripts fetched from anywhere, and nothing
leaves the machine. Clearing site data clears the notes, so keep a backup with
**Export all** if they matter.

MIT licensed.
