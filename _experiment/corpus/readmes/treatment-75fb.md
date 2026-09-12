# Notepad

A complete note editor in **one HTML file**, with no dependencies, no build step
and no server. Open `notepad.html` in a browser and it works. Notes live in that
browser's local storage; nothing is uploaded anywhere.

```sh
# the whole install procedure
open notepad.html            # macOS; xdg-open or start elsewhere

# or, recommended while developing, serve it over http
npm run serve                # http://127.0.0.1:8080
```

Some browsers refuse `localStorage` to pages loaded from `file://`. The app
detects that and says so rather than silently losing work, but if you plan to
keep real notes in it, serve it over http (`npm run serve`) or host the file on
any static host.

## What it does

**Notes.** Any number of them, in a searchable sidebar. The first line of a note
is its title - there is no separate title field to keep in sync. Notes autosave
as you type; anything structural (new note, delete, pin, import) is written
immediately.

**Finding things.** Search filters the list on every keystroke and matches all
whitespace-separated terms anywhere in a note. Sort by last edited, date created
or title; pinned notes stay on top. Inside a note, find and replace handles match
case, whole word, a match counter, step forward and back, replace one and replace
all.

**Not losing things.** Deleting moves a note to the trash, where it can be
restored or deleted for good; emptying the trash asks first. Export writes every
note (trash included) to a JSON file, and Import takes one back, either merged
alongside what you have or replacing it. A single note can be downloaded as
`.txt`, and a `.txt` file chosen through Import becomes a new note. If the saved
data in the browser is ever unreadable, the app keeps a copy under a separate key
instead of overwriting it.

**Comfort.** Light, dark or system theme; word wrap on or off; proportional or
monospace; text size from 12 to 28px. All of it is remembered. The status bar
shows the title, line and column, selection length, and word and character
counts, and `Ctrl+G` jumps to a line by number. Printing prints the note, not
the interface.

**Keyboard.**

| Keys | Action |
| --- | --- |
| `Ctrl/Cmd + N`, `Alt + N` | New note |
| `Ctrl/Cmd + K` | Search notes |
| `Ctrl/Cmd + F` | Find and replace |
| `F3` / `Shift + F3` | Next / previous match |
| `Ctrl/Cmd + S` | Save now |
| `Ctrl/Cmd + E` | Download this note as `.txt` |
| `Ctrl/Cmd + G` | Go to line |
| `Alt + ↑` / `Alt + ↓` | Previous / next note |
| `Alt + D` | Insert date and time |
| `?` | Shortcut list |
| `Esc` | Close whatever is open |

Everything is reachable without a mouse: real buttons, `aria` state, arrow-key
navigation in the list, focus handed back after the list re-renders, and no
`window.confirm` freezing the page.

## Repository layout

```
notepad.html          the application: styles, markup, core logic, DOM shell
tests/
  helpers/            harness that loads code out of notepad.html
  unit/               the pure core, tested without a DOM
  dom/                the real page, driven in jsdom
  structure/          promises about the file itself (single file, no network)
scripts/serve.mjs     dependency-free static server for local development
ARCHITECTURE.md       how the file is organised, and why
CONTRIBUTING.md       the TDD workflow and the conventions used here
AGENTS.md             orientation for an agent picking this up cold
```

## Tests

```sh
npm install        # jsdom, for the DOM tests - the app itself needs nothing
npm test           # everything
npm run test:unit  # pure logic only; works without jsdom installed
npm run test:dom   # the page in jsdom
npm run test:watch
```

The tests keep no copy of the application. The harness reads `notepad.html`,
pulls the `notepad-core` script out of it and evaluates that, so the unit tests
exercise exactly the code that ships; the DOM tests boot the same file in jsdom
and click it. See [ARCHITECTURE.md](ARCHITECTURE.md).

## Browser support

Any current version of Chrome, Edge, Firefox or Safari. The application is
written in conservative, ES5-era *syntax* (`var`, function expressions, no arrow
functions, no template literals, no optional chaining) so the single file needs
no transpiling; it does use built-ins every browser has had since about 2017
(`Promise`, `Object.assign`, `String.padStart`). Anything genuinely optional -
`matchMedia`, `execCommand`, `URL.createObjectURL`, `scrollIntoView`, `print`,
`localStorage` itself - is feature-detected or wrapped in a `try`, so a browser
that lacks it degrades instead of breaking.

## Licence

MIT.
