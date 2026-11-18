# Build and verification notes

Playing needs only index.html in a modern browser. The following is for maintaining the project.

The release reads data/cards.json as its catalog. src/engine.js is the only rules engine; the browser, the automated tests, simulations and example use it. The XLSX and PDF faces read the same JSON. To change balance, edit both the applicable engine primitive and the card data where necessary, then repeat the affected checks.

tools/build_catalog.py and tools/art_scenes.py are the catalog's original authoring source. Re-running build_catalog.py regenerates cards.json, the Markdown catalog, and art_briefs.json. Keep direct JSON edits in those sources as well if you plan to regenerate later.

## Runtime checks

- node tests/engine.test.cjs
- node tools/simulate.cjs 100
- node tools/example.cjs
- node --check src/app.js

The simulation argument is games per player count; 100 produces 500 games across 2, 3, 4, 5 and 6 players. Styles and seats rotate. This is heuristic-bot evidence, not human playtesting.

## Release builders

Python requires reportlab, pypdf, jsonschema and installed Open Sans fonts. tools/build_release.py builds the offline HTML, the field manual, print files and the six-card style proof. The script currently reads Open Sans from /usr/share/fonts/truetype/open-sans; adjust FONT when using another OS.

The workbook builder uses @oai/artifact-tool in the Codex primary runtime. Run tools/build_catalog_xlsx.mjs with an absolute project root argument. It writes to outputs/great-escalation and copies the catalog workbook into data. Its workbook totals are formulas, and a temporary artwork-status change is checked and restored before export. The builder is specific to that authoring environment; the exported XLSX does not need it.

Then run python3 tests/artifact_checks.py. It validates the final embedded JavaScript, current catalog embedding, all PDF card IDs, trim boxes, bleed boxes and actual illustration completion states.

## Browser walkthrough still required

tests/browser.test.cjs uses Playwright. It can resolve an installed playwright package or the Codex primary runtime package. TGE_CHROMIUM optionally supplies an executable path. TGE_NO_SANDBOX is an explicit optional development-environment setting; normal runs leave it unset.

The included walkthrough covers collection filters, modal target selection, prebuilt openings, card play, Undo, bots returning control, autosave reload, save export/import, pass-and-play hand privacy, manual content, mobile width, and console/network errors. It was not executed because the available browser runners could not open this local prototype. Do not substitute its existence for a passing result.

## Production next steps

All 110 art assets are complete. New art should follow docs/ART_DIRECTION.md and data/art_briefs.json. tools/ingest_art.py prepares print masters and lightweight web copies from individual generated originals. Run tools/build_art_atlas.py after build_release.py to rebuild the full art atlas. Run human matches with each player count and make a physical duplex proof. Final color profiles, stock, printer tolerances and commercial packaging are not specified by this playtest build.
