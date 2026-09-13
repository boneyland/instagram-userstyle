---
name: shipping-a-release
description: Use when publishing a new version of this userstyle to userstyles.world — cutting a release, bumping @version, updating the live style, or writing release notes for installers.
---

# Shipping a release to userstyles.world

The style is published to [userstyles.world](https://userstyles.world/style/30052/instagram-desktop-site) (USw)
and that page is the authority on which version is live -- read the version off
it rather than inferring it from the uploaded copies in the repo.
under the user `boneyland`. Installers get auto-updates from USw once a new
version is live.

**Publishing is entirely manual.** Every release so far has been uploaded, typed
or pasted directly into the USw website. The project has been under git since
2026-09-11 and the repository is public, but git is for history, not
distribution: USw is fed by hand from the deliverable, with no mirroring — see
Mirroring below before suggesting otherwise.

## Before shipping

1. **Verify.** `python3 verify.py Instagram.user.css` — exits non-zero on
   failure.

   For a refactor that should change nothing, use the two-file form:
   `python3 verify.py old.user.css Instagram.user.css`. The current release is
   kept locally as `Instagram-20260910-uploaded.user.css`, so that check can be
   run against what is actually live. Keep the habit of copying the working file
   before a refactor anyway, for changes that sit on top of unreleased work.

2. **Bump `@version`.** CalVer plus a revision: `YYYY.M.D.R`. The revision
   starts at **1** and counts further releases on the same day —
   `2026.9.10.1`, `2026.9.10.2`. A new day starts over at `.1`.

   **Never write `.0`.** Stylus compares the dot-separated parts across the
   *longer* of the two versions and reads a missing part as 0 — `cmpver.js`,
   `Math.max(len1, len2)` with `parseInt(a, 10) || 0`, read from the Stylus
   source on 2026-09-10. So `2026.9.10.0` and `2026.9.10` compare **equal** and
   no update is offered. `2026.9.10.1` compares greater, and a later date still
   beats any revision of an earlier one: `2026.9.11.1` > `2026.9.10.5`.

   That same rule is what lets the two spellings coexist, so releases published
   before this scheme keep their plain `YYYY.M.D` and are not renamed.

   Bump it on every published change, so installers see an update. *(The
   comparator above is Stylus's, verified. That the USw update feed is what
   drives it has not been verified here.)*

3. **Check `@description`.** It describes what the style does and deliberately
   does **not** state the browser floor — do not add it there. The floor lives
   in `README.md` under Requirements and in `USw-notes.md`, and raising it means
   editing both. See `docs/open-questions.md` on the Chromium claim.

   Check the **settings** too: `README.md` carries the table of defaults and
   `USw-notes.md` names individual settings in its bullets, so a renamed or
   added setting has to be chased into both or installers read labels that are
   not in the pane.

4. **After uploading**, save the uploaded file alongside the previous ones as
   `Instagram-YYYYMMDD-uploaded.user.css`, or
   `Instagram-YYYYMMDD.R-uploaded.user.css` if the day already holds a
   published release — the filename mirrors `@version`, so a second release
   on one day forces the suffix onto both copies. Rename the existing one
   rather than leaving it ambiguous; earlier days keep their plain form.
   Then point the `CHANGELOG.md` convention at the new copy: the next entry
   is written as a comparison against the newest uploaded copy, not against
   the working file. Identify the newest by reading `@version` out of the
   candidates, not by sorting filenames.

5. **Write the notes.** Two files, two audiences:

   - `CHANGELOG.md` — release notes per `@version`. Mechanism and internals
     belong here. Anything **removed**, or deliberately **not done**, goes in
     `docs/removed.md` under a subject heading instead, with a one-line pointer
     left in the entry; that file is the record that outlives the release.
   - `USw-notes.md` — the user-facing version, for pasting into the Notes field
     on USw. Mechanism and internals stay out of it.

   The style file itself carries no changelog.

## Never add `@updateURL`

USw overwrites it, to avoid tracking and broken URLs. Installers get
auto-updates from USw automatically, so the field buys nothing and is replaced
regardless.

## Mirroring — not used here

USw can pull edits automatically instead of taking them by hand: host the raw
file, set it as the source, and tick **Mirror source code updates**. It then
polls every four hours at :04, and mirrors **only when `@version` differs** —
with an unchanged version it silently skips, with no error.

None of that is set up for this project, and nothing depends on it. Recorded so
the option is not mistaken for the current workflow, and so the silent-skip
behaviour is known if it is ever turned on.
