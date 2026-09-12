# Notepad

A plain-text notepad that lives in one HTML file. Open `notepad.html` in a
browser and start typing — no install, no build step, no server, no account.
Notes are saved in that browser as you type.

```
open notepad.html          # or: npm run open, or double-click the file
```

## What it does

**Writing**

- Autosaves to the browser while you type, with a save indicator in the status bar
- Per-note undo and redo (`Ctrl+Z` / `Ctrl+Shift+Z`) that survive switching notes
- `Tab` inserts a tab character; `Esc` gets you back out of the editor
- Insert the date and time at the caret (`Alt+D`)
- Live count of lines, words, characters and the current `Ln, Col`

**Notes**

- As many notes as you like, listed with a title, preview and last-edited time
- Titles come from the first line, or set your own in the title field
- Search across every note (accent- and case-insensitive, all terms must match)
- Sort by recently edited, date created or title; pin notes to the top
- Duplicate and delete, with a confirmation step

**Find and replace** (`Ctrl+F`, `Ctrl+H`)

- Match case, whole word and regular expressions, with a live match count
- `F3` / `Shift+F3` walk the matches and wrap around
- Replace one or replace all; `$1` and `$&` work in regex mode
- One undo step reverses a Replace all

**Files**

- Open `.txt` or `.md` files as new notes, or drop them onto the window
- Download the current note as `.txt` or `.md`
- Export every note to JSON and import it back on another machine
- Print the current note (`Ctrl+P`)

**Appearance**

- Light, dark or follow-the-system theme
- Word wrap on or off, three editor fonts, twelve text sizes
- Works down to phone width, where the note list becomes a drawer
- Keyboard accessible throughout, with visible focus and screen-reader announcements

Press `F1` in the app for the full list of shortcuts.

## Where the notes live

In `localStorage`, under the key `notepad.state.v1`, in the browser profile you
opened the file with. That means:

- Notes are not synced anywhere and never leave the machine.
- A different browser, a private window, or clearing site data gives you a
  different (or empty) notepad.
- Use **More → Export notes as JSON** for a backup you can keep or move.

If the saved data is ever unreadable, the app keeps the raw copy under
`notepad.backup.<timestamp>` instead of discarding it, and starts fresh.

## Developing

Requires Node 20.10+ for the test runner. The app itself has no dependencies.

```
npm install        # only test tooling: Playwright
npm test           # unit + static + end-to-end
npm run test:fast  # skip the browser tests
npm run test:watch # re-run unit and static tests on save
```

The end-to-end suite drives the real file in Chromium. If it complains about a
missing browser, run `npx playwright install chromium`.

Start with [CONTRIBUTING.md](CONTRIBUTING.md) for how to work in this repository,
and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for how `notepad.html` is put
together.

## Browser support

Any current version of Chrome, Edge, Firefox or Safari. The app uses no
dependencies and no build step, so what you read in `notepad.html` is exactly
what runs.
