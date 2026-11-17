# The Great Escalation — verified project handoff
Last checked: 2026-11-17
Project: The Great Escalation, illustrated 110-card alpha v0.1.0 (art revision 1).

## Definitive input packages
Two archives were uploaded to the ChatGPT conversation, **not yet to this repository**:
- `The_Great_Escalation_110_Card_Alpha_0_1_0(3).zip` — 279,056,962 bytes; SHA-256 `bb8d390d42148c9c4fbd21cebc5d70980e58db2eef98414bc7d9895daea6697e`
- `The_Great_Escalation_110_Original_Illustrations(4).zip` — 491,728,923 bytes; SHA-256 `7556babe1085527941b13db998a51047917fe9eb3de965ccabf819731bdbacf3`

Uploaded archive names include download-copy suffixes; they do not indicate a new product edition.

## Verified against the actual archives
- Both ZIPs pass ZIP CRC checks.
- Alpha package has 272 entries (one project root folder); all **271 files** listed in `MANIFEST.json` match both byte size and SHA-256 digest.
- `data/cards.json` has exactly **110 cards**: Media 25, Infrastructure 20, Political/Corporate 20, Conspiracy 15, IT 15, Wildcard 15.
- Alpha has **110 master JPEGs** in `art/`, **110 lightweight JPEGs** in `art/web/`, an embedded, self-contained `index.html`, source, tests, workbook and print PDFs.
- The second archive has **110 PNG originals**, all 110 IDs match the JPEG card IDs, and all 110 have different SHA-256 digests.
- Re-ran `node tests/engine.test.cjs`: **25/25 passed**.
- Re-ran `python tests/artifact_checks.py`: **572/572 passed**.
- Browser end-to-end walkthrough is **not verified**. Chromium launched in the review environment but both `file://` and localhost pages were blocked by administrator policy. Automated artifact results do not prove that interactive browser flows work.
- Human playtesting and production-grade physical print proof are not complete.

## GitHub publication status
As of this check, `main` contains the project README and `.github/workflows/publish-alpha.yml`, **not the full source/game/assets**, and no GitHub Releases are published.

The existing workflow is **not runnable as-is**: it references `requirements-checks.txt`, `tools/package_release.py` and `docs/RELEASE_NOTES.md`, which are absent from the current repository and the alpha ZIP. Do not dispatch it until updated.

## Resume here
1. Import the contents of the alpha ZIP's `The_Great_Escalation/` folder into repository root, preserving the existing `.github/` workflow only after correcting it. The original PNG ZIP should be archived as a Release asset rather than checking nearly 500 MB of originals into Git history.
2. Create a GitHub Release (suggested tag `v0.1.0-illustrated.1`) attaching **both** original uploaded ZIPs, with the two hashes above. Keep printable PDF proofs available via the release.
3. Repair CI/release workflow to use the **actual** source layout. Run both test suites again on the imported tree. No publication claim until the Release and assets are visible.
4. Run the included `tests/browser.test.cjs` in an unrestricted Playwright/Chromium environment; then conduct human playtesting and a physical print proof.

This handoff records verification and remaining work; it is **not** evidence that the binary archives were pushed or published.
