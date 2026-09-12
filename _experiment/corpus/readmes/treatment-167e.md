# Notepad

A notepad that is one HTML file. Open `notepad.html` in a browser and write.
No install, no build, no server, no account, no network — notes are saved in
that browser's local storage and never leave the machine.

```
git clone <this repo>
open notepad.html          # macOS      (or: xdg-open notepad.html, or double-click it)
```

That is the whole product. Everything else in this repository exists to keep it
honest: tests, tooling, and notes for whoever works on it next.

## What it does

**Writing**
- Autosaves as you type, with a visible “Saving… / Saved at 14:03” state.
- The first line of a note becomes its title, until you rename it — then your
  name sticks.
- Live word, character and line counts, plus cursor position and selection size.
- Tab and Shift+Tab indent and outdent the selected lines.
- Text size, monospace and line wrapping are yours to set, and they persist.

**Organising**
- Many notes in a sidebar, sorted by last edited, date created or title.
- Pin the ones you keep coming back to.
- Search every note as you type, with matches highlighted in the previews.
- Find and replace inside a note, with match counts, case and whole-word options.
- Deleting moves a note to the trash (with a one-click Undo); the trash holds it
  until you empty it, and notes there open read-only with Restore / Delete forever.
- Duplicate a note, copy it to the clipboard, print it.

**Owning your data**
- Download a note as `.txt` or `.md`.
- Export everything as one JSON bundle; import bundles or plain `.txt`/`.md`
  files back in. Imports merge by note id and never clobber a newer copy.
- Two tabs open at once stay in sync, and an unsaved edit is never thrown away
  by the other tab's changes.

**Comfort**
- Light and dark, following the system by default, switchable and remembered.
- Keyboard-first: `Ctrl/Cmd+N`, `K`, `F`, `S`, `/`, `Alt+↑/↓`, `F3`, `Esc`.
  Press `Ctrl/Cmd+/` in the app for the full list.
- Screen-reader labels, visible focus rings, a print stylesheet, reduced-motion
  support, and a layout that works down to a phone.
- If the browser refuses to save (private mode, full quota), the app says so
  instead of quietly losing your work.

## Working on it

```
npm install         # jsdom, for the DOM tests. The app itself has no dependencies.
npm test            # unit + jsdom UI + file-integrity suites (fast, hermetic)
npm run test:e2e    # real Chromium against file://notepad.html (needs playwright)
npm run test:watch  # re-run on save
npm run screenshots # render the app to ./screenshots for a visual check
npm run serve       # serve the folder over http, if you prefer that to file://
```

Development here is test-first — see [CONTRIBUTING.md](CONTRIBUTING.md) for the
loop and the house rules, and [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) for
how the single file is put together and what the tests hold you to.

## Browser support

Anything current: Chrome, Edge, Firefox, Safari, and their mobile versions.
The app avoids APIs that need a secure context and degrades politely when one is
missing — no clipboard, no downloads, no storage — saying so rather than failing
silently.
