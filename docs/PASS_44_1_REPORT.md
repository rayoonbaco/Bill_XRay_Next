# Pass 44.1 - Public Language Clean Room

## Goal
Keep the Pass 44 public-product inversion intact while removing development-lab vocabulary from the public-facing articles.

## Changed
- `public/data.js`: public-facing TCJA, IRA, and ACA language cleaned.
- `tests/test_public_language_clean_room.py`: prevents backstage vocabulary from leaking upstairs.
- `SMOKE_TEST_PASS_44_1.py`: one-click validation and Ray human gate.
- `ONE_CLICK_PASS_44_1.bat`: root-level launcher.

## Intentionally unchanged
- `public/index.html`
- `public/styles.css`
- `public/app.js`
- Evidence drawer structure and receipt counts
- Three-bill chooser

## Doctrine
The citizen sees what happened, why it matters, and what remains uncertain. The build process stays invisible unless the reader explicitly asks for receipts.
