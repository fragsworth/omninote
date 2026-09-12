# Notepad

A plain-text notepad that lives in **one HTML file**. Open `notepad.html` in a
browser and it works: no install, no build step, no dependencies, no network, no
account. Notes are stored in the browser's local storage on the device you use.

```
open notepad.html          # macOS
xdg-open notepad.html      # Linux
start notepad.html         # Windows
npm run serve              # or serve it at http://127.0.0.1:8080/notepad.html
```

## What it does

**Notes** - as many as you like, in a searchable sidebar. The first line becomes
the title until you type one yourself. Notes can be pinned, duplicated, sorted by
last edited / created / title, and deleted into a trash that can be restored or
emptied. Everything autosaves a third of a second after you stop typing; the
status bar says when it last saved.

**Editing** - word and character counts, line and column, reading time, tab and
shift-tab indenting, move-line-up/down, duplicate line, and a find & replace bar
with match counting, case / whole-word / regular-expression modes and capture
groups. Line transforms (upper, lower, sort, dedupe, trim trailing spaces,
collapse blank lines) apply to the selection, or to the whole note when nothing
is selected. `F5` stamps the date and time, as Notepad always has.

**Files** - open `.txt` / `.md` files (or drag them onto the page), save the
current note as `.txt` or `.md`, print, export every note as one `.json` bundle
and import it back on another machine.

**Comfort** - light / dark / follow-the-system themes, three editor fonts, text
size controls, word wrap and spell-check toggles, a distraction-free focus mode,
a full keyboard-shortcut reference (`Ctrl+/`), a responsive layout that turns the
sidebar into a drawer on a phone, and screen-reader labels throughout.

### Keyboard shortcuts

| Action                        | Keys                                          |
| ----------------------------- | --------------------------------------------- |
| New note                      | `Alt+N`                                       |
| Duplicate note                | `Ctrl+D`                                      |
| Rename note                   | `F2`                                          |
| Pin / unpin                   | `Ctrl+Shift+P`                                |
| Move note to trash            | `Ctrl+Shift+Backspace`                        |
| Search notes                  | `Ctrl+K`                                      |
| Find & replace                | `Ctrl+F` (`Ctrl+H` starts in the replace box) |
| Next / previous match         | `Enter` / `Shift+Enter`                       |
| Go to line                    | `Ctrl+G`                                      |
| Indent / outdent              | `Tab` / `Shift+Tab`                           |
| Move line up / down           | `Alt+Up` / `Alt+Down`                         |
| Duplicate line                | `Ctrl+Shift+D`                                |
| Insert date & time            | `F5`                                          |
| Save as .txt                  | `Ctrl+S`                                      |
| Print                         | `Ctrl+P`                                      |
| Bigger / smaller / reset text | `Ctrl+=` / `Ctrl+-` / `Ctrl+0`                |
| Focus mode                    | `Ctrl+.`                                      |
| Shortcut list                 | `Ctrl+/` or `F1`                              |
| Close panel or dialog         | `Esc`                                         |

On macOS use `Cmd` instead of `Ctrl`. Browsers reserve a few combinations
(`Ctrl+N` most notably), which is why the new-note shortcut is `Alt+N`.

## Working on it

```
npm install          # Playwright, the only dev dependency
npm test             # everything (unit + browser)
npm run test:unit    # fast, zero dependencies, no browser
npm run test:browser # real Chromium against the real file
npm run test:watch   # unit tests on save
npm run serve        # static server for manual poking
```

The unit tier lifts the pure logic out of `notepad.html` and exercises it in
plain Node; the browser tier drives the actual page in Chromium. If Playwright
cannot be installed, the browser suites skip themselves with a message and the
unit tier still runs.

Before changing anything, read **[AGENTS.md](AGENTS.md)** - it covers the rules
this repository keeps (test first, one file, no dependencies) - and
**[docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)** for how the file is laid out and
how the stored data is versioned.

## Layout

```
notepad.html              the entire application
tests/unit/               node:test suites, no browser, no dependencies
tests/browser/            Playwright suites driving the real page
tests/helpers/            loads the app for each tier
tools/serve.mjs           dependency-free static server
docs/                     architecture and decision log
```

## Limits worth knowing

- Notes live in one browser profile on one device. Export a `.json` bundle to
  move them; there is no sync and nothing is sent anywhere.
- Local storage caps out around 5 MB per origin. The sidebar footer shows how
  much of that the notes take, and a failed save is reported rather than hidden.
- Opening the file over `file://` works, but some browsers give `file://` pages
  no local storage. `npm run serve` avoids that.
