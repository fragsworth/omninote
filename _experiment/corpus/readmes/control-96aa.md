# Notepad

A notepad that lives in one HTML file. Open `index.html` in a browser and write.
No install, no build step, no server, no account, no network calls — your notes
are stored in that browser and never leave it.

```
git clone <this repo>
open index.html          # macOS ("start index.html" on Windows, "xdg-open" on Linux)
```

It works from `file://`, off a USB stick, or from any static host. The whole
application is ~115 KB of hand-written HTML, CSS and JavaScript.

## What it does

**Writing**

- Multiple notes with autosave — there is no save button to forget
- The first line becomes the note's title, or set one explicitly
- Word, character and line counts, reading time, and live line/column
- Undo and redo that cover programmatic edits too, not just typing
- Tab indents (Escape first if you want Tab to move focus instead)
- Enter continues `-`, `*`, `1.`, `>` and `- [ ]` lists, and ends them on a
  blank item
- Find and replace within a note, with match counting and optional case
  sensitivity
- Insert the current date and time (`Ctrl`/`⌘` + `Shift` + `D`)

**Organising**

- Search across titles and bodies, with matches highlighted in the list
- `#tags` written anywhere in a note become one-click filters
- Pin notes to the top; sort by last edited, date created or title
- A quick switcher (`Ctrl`/`⌘` + `P`) that fuzzy-matches and can create a note
  from whatever you typed
- Trash with restore, "delete forever" and "empty trash" — deleting is always
  undoable

**Keeping your notes**

- Download a note as `.txt` or `.md`, or every note as a dated `.json` backup
- Import backups (merged by note, newest edit wins) and plain text/markdown
  files, from the menu or by dropping files onto the window
- Print a note
- Copy a note to the clipboard

**Comfort**

- Light and dark, following the system or pinned either way
- Sans, serif or monospace editor font, adjustable size, optional line wrap
- Focus mode, collapsible note list, and a layout that works on a phone
- Keyboard shortcuts throughout (`Ctrl`/`⌘` + `/` lists them)
- Screen-reader labels, live announcements, visible focus, and respect for
  `prefers-reduced-motion`

## Where notes are stored

In `localStorage`, under `notepad.notes.v1`, in the browser and profile you used.
That means:

- Notes do not sync between browsers, devices or profiles.
- Clearing site data deletes them. **Take backups** (export menu → *Back up all
  notes*).
- Private/incognito windows may refuse storage entirely; the app says so in a
  banner and keeps working for the session.
- If the stored data is ever unreadable, the app keeps the original bytes under
  `notepad.notes.backup.v1` rather than overwriting them.
- Two tabs open at once stay in sync, and the tab you are typing in never loses
  what you have written.

## Development

```
npm install     # jsdom, for the tests only — the app itself has no dependencies
npm run check   # lint + the full suite (~320 tests, a few seconds)
npm test        # tests only
npm run lint    # repo-specific checks (dangling element ids, leftovers, whitespace)
```

Tests drive the real `index.html` inside jsdom, so they exercise the file a user
opens rather than a copy of its source.

Read [CONTRIBUTING.md](CONTRIBUTING.md) before changing anything — it covers the
architecture, the test-first workflow, and the constraints that keep this a
single dependency-free file.

## Licence

MIT. See [LICENSE](LICENSE).
