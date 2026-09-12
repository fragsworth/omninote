# Notepad

A notepad that lives in one HTML file. Open `index.html` in a browser and it
works — no server, no build step, no dependencies, no account. Notes are kept in
that browser's `localStorage` and never leave the machine.

```
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
```

Or, if you would rather have it on `http://`:

```
npm run serve            # http://localhost:8080
```

## What it does

- **Many notes.** A sidebar lists them, newest first, with pinned notes on top.
  Sort by last edited, date created or title.
- **Titles that write themselves.** Leave the title blank and the first line of
  the note becomes its heading.
- **Search** across titles and bodies, several terms at once, `"quoted phrases"`
  included, with matches highlighted in the list.
- **Autosave**, with an honest status line — `Saving…`, `Saved`, or a warning if
  the browser refuses to store anything.
- **Trash.** Deleting is undoable: notes go to the trash, can be previewed and
  restored there, and are cleared out automatically after 30 days.
- **Find and replace** inside a note, with match counts, case and whole-word
  options, and replace-one or replace-all.
- **Import and export.** One note as `.txt` or `.md`, everything as a `.json`
  bundle; drag files onto the window to bring them back in. Re-importing the
  same bundle twice does not duplicate anything.
- **It adapts.** Light and dark themes (following the system by default), three
  typefaces, adjustable text size, optional line wrapping and spellcheck, a
  collapsible sidebar, and a drawer layout on phones.
- **Keyboard first.** `Ctrl`/`Cmd` + `N`, `S`, `K`, `F`, `G`, `D`, `B`, `P`,
  `Backspace`, `Alt`+arrows to move between notes, `Tab` to indent, `?` for the
  full list.
- **Printing** produces the note, not the interface.

## Working on it

```
npm install     # jsdom, for the tests only
npm test        # the whole suite
npm run test:watch
npm run test:unit / test:dom / test:contract
```

Everything that ships is `index.html`. `tests/`, `tools/` and `docs/` support it
and are never loaded by the app.

Tests are [`node:test`](https://nodejs.org/api/test.html) over
[jsdom](https://github.com/jsdom/jsdom), and they load the real `index.html` —
there is no second copy of the source to fall out of step.

| Directory | What lives there |
| --- | --- |
| `tests/unit/` | Pure helpers and store transitions, against injected fakes |
| `tests/dom/` | A booted app, driven by clicks and keystrokes |
| `tests/contract/` | The single-file, no-dependency constraints themselves |
| `tests/helpers/app.mjs` | The only thing that knows how to load the app |

New here? Read [`docs/ARCHITECTURE.md`](docs/ARCHITECTURE.md) for how the file is
laid out and where to add things, and [`CLAUDE.md`](CLAUDE.md) for the working
agreements. [`docs/DECISIONS.md`](docs/DECISIONS.md) records why the awkward
choices are the way they are.

## Browser support

Anything current: Chrome, Edge, Firefox and Safari from 2023 onwards. The app
uses `:has()`, `dvh` units and `Intl.DateTimeFormat`, and degrades quietly
without `localStorage` (it says so, and keeps working for the session).
