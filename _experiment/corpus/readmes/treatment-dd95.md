# Notepad

A complete, private notepad that is **one HTML file with no dependencies**. Download
`index.html`, double-click it, and write. No build step, no server, no account, no network
access — your notes live in your own browser.

```
open index.html          # macOS
xdg-open index.html      # Linux
start index.html         # Windows
npm start                # or serve it at http://localhost:8137
```

---

## What it does

**Notes**

- Many notes in one file, listed in a sidebar with a title, a preview and "last edited"
- Titles derive themselves from the first line (`# Heading` and `- bullets` are stripped) or
  can be set by hand
- Search across every note's title and body, pin notes to the top, sort by last edited, date
  created or title, duplicate and delete

**Editing**

- Plain text, word wrap, optional line numbers that stay correct across wrapped lines
- Real undo/redo per note, with typing coalesced into sensible steps and programmatic edits
  (like Replace all) as single steps
- Tab indents, Shift+Tab outdents, block indent for multi-line selections
- Continue `-`, `*`, `1.` and `- [ ]` lists on Enter; an empty item ends the list
- Duplicate, move and delete whole lines; insert the date and time (F5, as in the original)
- Live status bar: line and column, selection size, words, characters, lines and note size

**Find and replace**

- Every match highlighted in place, with the current one picked out
- Match case, whole word, and full regular expressions with `$1` backreferences
- Find next/previous with wrap-around, replace one, replace all (a single undo step)

**Files and safety**

- Everything autosaves to this browser, including which note was open and where the caret was
- Open `.txt` / `.md` files (button, Ctrl+O, or drag and drop)
- Save the current note as `.txt`; back up **all** notes to `.json` and restore them later,
  merging or replacing
- Damaged saved data is recovered rather than discarded; blocked storage (private windows) is
  reported instead of failing silently
- Print a clean copy of the note, not a screenshot of the editor

**Comfort**

- Light, dark and system themes; monospace, sans or serif; adjustable text size
- Works down to phone width, respects `prefers-reduced-motion`
- Full keyboard control with a shortcut sheet on F1

## Keyboard shortcuts

| | |
|---|---|
| New note / duplicate note | `Ctrl N` / `Ctrl Shift D` |
| Search notes / toggle the note list | `Ctrl K` / `Ctrl B` |
| Open file / save as .txt / back up all | `Ctrl O` / `Ctrl S` / `Ctrl Shift S` |
| Undo / redo | `Ctrl Z` / `Ctrl Y` |
| Find / find next / previous / replace | `Ctrl F` / `F3` / `Shift F3` / `Ctrl H` |
| Go to line | `Ctrl G` |
| Insert date and time | `F5` |
| Indent / outdent | `Tab` / `Shift Tab` |
| Move focus out of the editor | `Esc` then `Tab` |
| Duplicate line / move line / delete line | `Ctrl D` / `Alt ↑↓` / `Ctrl Shift K` |
| Word wrap / text size | `Alt Z` / `Ctrl Alt +` `Ctrl Alt -` |
| Shortcut sheet | `F1` |

On macOS use `Cmd` in place of `Ctrl`.

## Where your notes are kept

In `localStorage` under the key `notepad:v2`, on this device, in this browser, for this origin.
That means:

- Clearing site data, or "clear cookies and site data on exit", deletes them.
- A file opened from disk (`file://`) has a different origin from `http://localhost` — the two
  do not share notes.
- Private windows usually block storage entirely; Notepad detects that, says so, and keeps
  working for the session.

Use **File ▸ Back up all notes** for anything you care about.

## Development

Requires Node 22+. The application itself has no dependencies; `jsdom` is a dev dependency used
only to drive the UI in tests.

```bash
npm install        # jsdom, for the UI test suite
npm test           # core + UI tests
npm run test:core  # core only - runs with nothing installed
npm run check      # guardrails: single file, no dependencies, no DOM in the core
npm run verify     # check + test + real-browser layout checks
npm start          # serve on http://localhost:8137
```

| Path | What it is |
|---|---|
| `index.html` | The whole application: styles, markup, core layer, UI layer |
| `test/core/` | Unit tests for the DOM-free core, extracted straight out of `index.html` |
| `test/ui/` | jsdom integration tests that click, type and press keys |
| `test/support/` | Test harness (core loader, app loader, fake clock/timers/storage) |
| `tools/check.mjs` | Static guardrails, also asserted by `test/guardrails.test.js` |
| `tools/visual-check.mjs` | Optional real-browser layout checks (needs playwright) |
| `tools/serve.mjs` | Zero-dependency static server |
| `docs/ARCHITECTURE.md` | How the file is laid out and why |
| `docs/DECISIONS.md` | The decisions behind it, with their trade-offs |
| `CONTRIBUTING.md` | Working agreement: test first, and the invariants to keep |

Before changing anything, read `CONTRIBUTING.md` — this repository is test-driven, and the
"one dependency-free file" property is enforced mechanically.
