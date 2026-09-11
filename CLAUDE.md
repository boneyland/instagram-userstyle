# Instagram Desktop site — UserCSS

A userstyle for the desktop web at `www.instagram.com`, published to [userstyles.world](https://userstyles.world/) under the user `boneyland`. Stylus is required; the browser is not restricted to Firefox. Despite being built on `@-moz-document`, the style was confirmed working under Stylus for Chromium on 2026-09-10 (ungoogled-chromium). The mechanism has not been verified here — presumably Stylus does the `@-moz-document` URL matching itself rather than handing the at-rule to the engine, but treat that as inference. Under git since 2026-09-11, with the remote intended to be public. `Instagram_snapshots/` and `Preview_1246.png` are deliberately **untracked** — both capture a logged-in session — so a fresh clone cannot run either verification script until snapshots are captured locally. `.gitignore` gives the reason for every exclusion.

## Files

| File | Role |
| --- | --- |
| `Instagram.user.css` | The style. This is the deliverable. |
| `Instagram-20260910-uploaded.user.css` | The currently published version. Diff the deliverable against this one, and write each new `CHANGELOG.md` entry as a comparison with it — **do not edit**. |
| `Instagram-20260907-uploaded.user.css` | The version published before that. Kept for history — **do not edit**. |
| `CHANGELOG.md` | Release notes per `@version`, and the record of what was removed and why. The style file itself carries no changelog. |
| `USw-notes.md` | The whole Notes field on userstyles.world, ready to paste as-is: a summary of what the style changes, the requirements, and the user-facing changelog since the last *published* version — not every version. Keep it short and send the reader to GitHub for the rest. Mechanism and internals stay out of it. |
| `README.md` | The repository's public front page: what the style does, requirements, the settings table and the known limitations. Audience is a GitHub visitor, not a maintainer — keep internals out of it, and keep the settings table in step with the header. |
| `docs/token-overrides.md` | Why the five design-token overrides work, and how to measure a token's reach. Read before adding a sixth. |
| `docs/rule-notes.md` | Why each rule is written the way it is, and what was measured to get there. The style carries no comments, so this is the only explanation that exists. **Read the note for a rule before loosening a guard or changing a number.** |
| `.claude/skills/shipping-a-release/` | The release checklist for userstyles.world. |
| `verify.py` | Verification harness (see below). Run before shipping. |
| `scoped.py` | The `@-moz-document` half of verification, which `verify.py` is blind to. See below. |
| `unwrap.py` | Joins hard-wrapped Markdown paragraphs into one line each, leaving fenced blocks, tables and headings verbatim. Checks that the result is equivalent — same text with all whitespace removed, same block structure — and refuses to write if it is not. `unwrap.py FILE` to check, `--write` to apply. |
| `Instagram_snapshots/` | Every SingleFile snapshot. Both scripts read this folder and nothing else — `verify.py` sets `SNAPSHOTS`, `scoped.py` imports it. |
| `node_modules/` | One package, `usercss-meta`. |

Snapshots, all inside `Instagram_snapshots/`:

| File | Role |
| --- | --- |
| `Instagram_feed1.html` | Snapshot of a logged-in feed. 23MB, mostly base64 images; only ~1668 elements. Its one reel is a 125% portrait. |
| `Instagram_feed2.html` | A second, richer feed — 11 articles, three of them reels, and the **only snapshot with a landscape reel** (article 4, `padding-bottom:56.4263%`). `verify.py` uses this one: `find_snapshot()` takes the newest `Instagram_feed*.html`, so a fresh capture is picked up without editing it. |
| `Instagram-user-reel-id.html` | Snapshot of `/<user>/reel/<id>/`. |
| `Instagram-reels-id.html` | Snapshot of `/reels/<id>/`, captured as the floating dialog (it has a `[role="dialog"]`). Matches no selector in the style. |
| `Instagram-p-id(carousel133).html`, `Instagram-user-p-id(carousel133).html` | A **3:4 carousel** on the two post-permalink paths. Structurally identical to each other; no feed selector reaches either. Their column carries `.xf68679` and an inline `--x-maxWidth:min(100%,785px)`. |
| `Instagram-p-id(carousel100).html` | A **square (1:1) carousel**, and the snapshot that proves carousels have *two* layouts, exactly as single photos do. Its column carries **no `--x-maxWidth` at all**, so until 2026-09-11 every carousel rule missed it and only the two text rules from the `domain()` block reached the page. Media 1262×1262 at a 1638px window. |
| `Instagram-p-id(reel).html`, `Instagram-user-p-id(reel).html` | A **reel** on the same two paths — the same post captured twice. Identical to each other *and* to `Instagram-user-reel-id.html`, which is a different reel by a different user: a reel gets one layout wherever it is reached from. |
| `Instagram-p-id(single_photo100).html`, `Instagram-user-p-id(single_photo100).html` | A **square (1:1) single photo** on the same two paths, again the same post twice. Its column carries **no `--x-maxWidth` at all** — Instagram omits the `.xf68679` class that reads it — so nothing caps the column and the media fills the content area: 1262×1262 at a 1638px window, and wider on a wider screen. |
| `Instagram-user-p-id(single_photo133).html` | A **3:4 portrait single photo**, and the snapshot that proves single photos have *two* layouts. This one's column does carry `.xf68679` and an inline `--x-maxWidth:min(100%,785px)`, giving 449×599 — the same numbers a carousel starts from. |
| `Instagram-p-id(single_photo56).html`, `Instagram-user-p-id(single_photo56).html` | A **16:9 landscape single photo** on the same two paths, the same post twice. Its column is built like the square one — no `.xf68679`, no inline `--x-maxWidth` — but stock it renders 1262×712 in a 1598px column, which is already good, so it is the one single-photo shape the width cap is deliberately **withheld** from. It gets the caption-column setting and nothing else. These two are also by far the largest DOMs of any snapshot, ~16.5k elements against ~1–3k elsewhere. |
| `Instagram-p-id-modal(single_photo).html` | The **same post as those two**, captured as the floating modal opened over a profile grid. Its URL is the plain `/p/<id>/` permalink, so both `regexp()` blocks select it — but every rule in both is guarded on `main div[style*="--x-maxWidth"]`, which matches 0 here, so only the `domain()` block reaches it. It is the one saved page with an `<article>` **inside** a `[role="dialog"]`, which makes it the test for the modal guards. |

## Structure

Three `@-moz-document` blocks, and which one owns a page matters more than it looks:

| Block | Covers | Keyed on |
| --- | --- | --- |
| `domain("www.instagram.com")` | the feed, and anything else site-wide | `article`, and inline `min(470px` |
| `regexp(.../(p\|[^/]+/p\|[^/]+/reel)/...)` | **reels** on `/<user>/reel/<id>/`, `/p/<id>/` and `/<user>/p/<id>/` | a `video` in the `--x-maxWidth` column |
| `regexp(.../(p\|[^/]+/p)/...)` | **carousels and single photos** on `/p/<id>/` and `/<user>/p/<id>/` | the carousel's `li[style*="translateX"]`; for a single photo, a photo box with neither that nor a `video` |

The last two blocks both match the two `/p/` paths, and it is their *selector* guards — video versus slide list versus bare photo box — that decide which owns a given post, not their URL patterns. Three post shapes share two URL patterns; every rule stays in its lane by selector.

**Square** media is the shape whose lever is **not** `--x-maxWidth`, and this is true of a square carousel and a square single photo alike. Instagram omits the class that reads that token on square and landscape photos — both measured, no longer inference — so the rule sets `max-width` on the column directly, which works on every single-photo layout. `.xvc5jky` in that selector is load-bearing: without it the guards also match the "more posts" grid below the post.

Carousels are likewise handled by **two** rules, on the same principle. The caption column (`--u-reel-media-info`) is set for *every* carousel, on the `.xvc5jky` container rather than on `:root` — which is both why it reaches a square carousel and why it needs no `!important`. The width cap (`--u-post-photo-width`, the *single-photo* setting, so the two square shapes land on the same width) is applied **only** to a square carousel, guarded by `:not([style*="--x-maxWidth"])` on the element **itself** — the token is an inline style on `.xvc5jky` directly, so a `:not(:has(...))` spelling matches nothing and would silently cap the 3:4 carousels too. **Neither carousel shape has a zoom rule**, as of 2026.9.11.4. One existed for the 3:4 shape and was removed once a live check showed it changed nothing: Instagram re-derives each slide's width from its container, so capping the container is the whole job. Do not add one back without a live measurement — see the removal record under 2026.9.11.4 in `CHANGELOG.md`.

Single photos are handled by **two** rules on the same pattern, and the split is the thing to understand before touching either. The caption column (`--u-reel-media-info`) is set for *every* shape. The width cap (`--u-post-photo-width`) is withheld from **landscape**, whose stock layout is already good — capping it made things worse, 1262×712 down to 670×378. The fourth guard on the capped rule reads the *leading digit* of the `padding-bottom` percentage: everything ≥100% starts with `1`, everything landscape starts 5–9, and Instagram accepts nothing ≥200%. The comma inside that `:has()` is a **list, not nesting**, which is what makes it legal.

Feed reels are handled by **two** families of rule, split on `[style*="125%"]` versus `:not([style*="125%"])`, and the split is total: Instagram flattens anything taller than 4:5 into a 125% box, and everything else keeps its true ratio. The 125% family caps the anchor with arithmetic against the known 1.25; the non-125% family cannot, because CSS cannot read a ratio that exists only inside an inline style, so it drops the padding box and sizes the video from its own intrinsic dimensions. That second family is the one thing here **no snapshot can check** — SingleFile strips video sources — so read its note in `docs/rule-notes.md` before touching it.

Keep every rule in each block carrying its guard. The one shape that could satisfy both `regexp()` blocks is a mixed carousel (photo plus video slides); nothing is written against it and nothing can be until a snapshot of one exists. See the `Not done` entry under 2026.9.10.1 in `CHANGELOG.md`.

A reel gets the same layout on all three of its URLs — proven against three snapshots, two of them the same post and the third a different reel by a different user — which is why one block covers them and no post-page-specific reel setting exists.

Not every selector is safe outside its block. The post-page zoom selector matches a 470×3644 region on a **feed** page and would scale the feed's text with it — the URL scoping, not the selector, is what keeps it off. The reel block's `:root` token rule has the same shape of hazard: its guard matches on the saved feed too, so unscoping it would push `--media-info` across the whole feed. Check before moving a rule between blocks.

`/reels/<id>/` and the `/reel/<id>/` floating dialog are matched by none of them, deliberately: the saved `/reels/<id>/` is a modal with its own markup that shares no selector with the others.

## Verifying

```
python3 verify.py Instagram.user.css                      # check one file
python3 verify.py old.user.css Instagram.user.css         # prove a refactor changed nothing
```

Exits non-zero on failure. Four checks: metadata via `usercss-meta` (the parser Stylus itself uses), a Firefox rule/declaration census that catches silently dropped syntax, a non-empty check so equivalence cannot pass vacuously, and — with two files — a full computed-property diff over every element.

The two-file mode reports mismatches split into **standard** and **custom** properties. Custom-only drift means nothing renders differently; it is the signature of a declaration that is set, inherited, and never read.

Run it after any change. It has caught real breakage more than once.

**It is blind to URL scoping, and to two other things.** `prepare()` flattens every `@-moz-document` block unconditionally — which is exactly what makes the two-file mode a valid equivalence proof — so a change to a block's *condition* produces no diff at all. It also only ever loads one feed snapshot (`find_snapshot()` takes the newest `Instagram_feed*.html` inside `Instagram_snapshots/`), so nothing it says covers the other feed, the reel, post or modal pages. A passing run therefore means "the rules still parse and still do the same thing on the feed", never "this change is correct".

`scoped.py` covers that gap:

```
python3 scoped.py Instagram.user.css https://www.instagram.com/p/ABC/   # which blocks apply
python3 scoped.py --urls Instagram.user.css                            # every block vs every URL shape
python3 scoped.py --diff old.user.css Instagram.user.css               # every snapshot, at its own URL
```

`--urls` full-matches each block condition against a table of URL shapes: the ones a block must cover and the near misses it must keep out. Extend that table when a new page type is taken on. `--diff` is the one to run after changing a `regexp()` — it applies both files to **every** snapshot with only the blocks that page's real URL selects, and diffs every computed property of every element. It reads each snapshot's URL from the `url:` comment SingleFile writes at the top, so there is no table of URLs to fall out of date.

Read its output for `font-size`, `line-height` or `zoom`. Those usually mean a container holding text was resized by mistake, which is the failure mode the post-page zoom rule had to be walked outward to avoid.

Two traps it exists to encode. `regexp()` matches the **whole** URL, so test with `re.fullmatch`, not `search`. And the CSS source spells the pattern `\\.`, a CSS string escape for one backslash — hand that to a regex engine unconverted and every condition silently fails to match, which reads as "no block applies" rather than as an error.

## Hard rules

**Never write the literal `@var` outside the metadata block — comments included.** `usercss-meta` scans the whole file, reads it as a malformed variable declaration, and the style fails to install. Only `@var` behaves this way; `@name`, `@license` and `var()` are safe. Write "the variables declared in the header" instead. `verify.py` checks for this by name.

**Every rule in the `domain()` block keyed on `article` needs `:not([role="dialog"] *)`.** `article` is not a feed-only hook: a post opened as a floating modal — clicking a post in the feed, or a `/p/<id>/` URL reached from a profile grid — renders as an `<article>` inside a `[role="dialog"]`, and picks up every unguarded rule. That page is laid out by Instagram and sized by its own inline `max-height`/`max-width`/`aspect-ratio`, so feed rules landing on it resize a layout they were never measured against. The Media section was missing the guard until 2026.9.10.1, which let a *feed* setting cap the photo's height in the modal; `CHANGELOG.md` has the measurements. `Instagram-p-id-modal(single_photo).html` is the snapshot that catches this — the only saved page with an `<article>` inside a dialog. Adding a guard is cheap to check: compare `document.querySelectorAll(sel).length` with and without it across every snapshot.

**Never match a whole percentage in an attribute selector.** One ratio reaches the DOM under several spellings — a single saved feed carried 3:4 as `133.333%`, `133.33333333333331%` and `133.31719128329297%`. Round values also occur (`125%`, `100%`, and a live reel page gave `177.778%`), so the hazard is not "always computed", it is "not always the same". Match a distinctive prefix.

**Inline-style whitespace is unstable.** Server-rendered markup keeps a raw attribute string (`padding-bottom:125%`); a React re-render rewrites it through the CSSOM and inserts a space (`padding-bottom: 125%`). The same element switches after navigating away and back. Match a prefix that stops before the ambiguity (`[style*="min(470px"]`) or split into two conditions (`[style*="padding-bottom"][style*="125%"]`).

**Prefix every custom property `--u-`.** The only exceptions are deliberate overrides of Instagram's own design tokens, which must keep Instagram's names: currently `--media-info` (caption column — reel-page **and** post-page blocks), `--x-width` (feed post column), `--x-maxWidth` (the whole media-plus-caption column — again both the reel-page and post-page blocks) and the `--system-14-*` pair (post text). All of them need `!important` to win the collision **unless** the override is declared on an element closer to the target than Instagram's own declaration.

**Prefer naming containers over `!important` on `:root`.** `!important` on `:root` reaches every button, textarea and label, and a `:root` selector's inertness depends on where Instagram puts a `<style>` tag. Naming containers pins the scope to this file.

`docs/token-overrides.md` explains why the `!important` exception above works, why a `:root` override is otherwise inert, and how to measure a token's reach against a real page. Read it before adding a sixth override.

A quick audit: everything declared should be `--u-*` plus those five.

```
grep -oE '^\s*--[a-zA-Z][A-Za-z0-9-]*\s*:' Instagram.user.css | sed 's/^\s*//' | sort -u
```

**`:has()` does not nest.** `:root:has(X)` where `X` itself contains `:has()` is invalid, and Firefox drops the **whole rule** with no error — it reads as "the override had no effect", not as a mistake. This bit the single-photo `--media-info` override, whose guard needs `:has()` of its own. Declare such an override on a named container instead, which is the preferred form anyway.

**With CSS nesting, all declarations go above the nested rules.** A declaration after a nested rule needs `CSSNestedDeclarations` (Firefox 132), above this style's floor.

**Browser floor is Firefox 126** — `:has()` needs 121, `zoom` needs 126. `@description` deliberately does **not** state it; do not add it back there. Raising the floor means updating `README.md`, which gives it a Requirements heading, and `USw-notes.md`, which repeats it for installers.

## Comment conventions

**Never hard-wrap a Markdown file in this repo.** One line per paragraph, as every `.md` file here is now written. They are read on GitHub and in the userstyles.world Notes field, both of which soft-wrap, so a hard-wrapped line re-wraps raggedly. `unwrap.py` joins wrapped paragraphs and refuses to write unless the result is provably equivalent; run it if a file ever drifts back. The cost is that these files have no controlled measure in a viewer that does not wrap.

**The style carries no comments outside the metadata block.** Every one was stripped on 2026-09-11 — see the `Removed` entry under 2026.9.11.1 in `CHANGELOG.md`, which records the equivalence proof. **Do not reintroduce them.** `docs/rule-notes.md` is now the only explanation of why a rule is shaped the way it is, so when you change a rule, the note there is not a duplicate to keep in sync — it is the record. Write it.

The metadata block is the exception, and it is not really a comment: Stylus parses it, the labels in it are the settings UI, and the whole style fails to install without it.

**If comments are ever restored, they are user-facing.** The file ships to userstyles.world, where anyone editing it in Stylus reads them. A comment there would say what a rule does and what would break if you changed it — nothing else. Specifically **never** write into the style: snapshot filenames, element or selector counts, pixel measurements, `verify.py` / `scoped.py` / `CHANGELOG.md` references, or the history of what a rule used to be. And do not hard-wrap: one line per paragraph, blank comment lines between paragraphs, because both consumer viewers soft-wrap and a hard-wrapped line re-wraps raggedly in a narrow pane.

**Do not state a mechanism you have not verified.** Several comments were wrong because earlier sessions wrote plausible-sounding explanations as fact — a guard described as excluding one child when it excludes two, an `aria-label` claimed to be un-localised on the basis of a single English page, a specificity hack attributed to a rule nobody had looked at. If a claim is inference, say so. Existing markers: `INHERITED, POSSIBLY STALE`, "has not been confirmed", "untested". These markers belong in `rule-notes.md` along with the claim they qualify; a user-facing comment should not be making a claim that needs one.

**When you delete something, record why and what the evidence was**, so it does not get re-added — in `CHANGELOG.md`, not in the style. The file ships to userstyles.world, so it carries no changelogs and no notes about what used to be there. See the removed-nav and `:not(.xtcbf50)` entries under 2026.9.10.

## What the snapshot can and cannot prove

SingleFile pruned unused CSS and flattened inline-style whitespace on save.

*Can* prove: DOM structure and class presence, and equivalence between two versions of the style (both see the same DOM, so the pruning cancels out).

*Cannot* prove: whether a selector matches live, what Instagram's own CSS does, inline-style spacing, or anything on a page that was not captured. The snapshot is a feed page — its only `<nav>` is the **footer**, so the left sidebar, settings, and reel pages are all absent. A class missing from it is not evidence the class is dead.

Live checks are the user's to run; ask rather than guessing.

The Playwright MCP browser cannot open `file://` URLs or reach localhost from this sandbox. Local headless Firefox is the only way to run these checks.

## Publishing to userstyles.world

Publishing is manual — uploaded, typed or pasted directly into the USw website. No hosted source and no mirroring: the git repository is for history, not distribution, and userstyles.world is fed by hand from the deliverable.

Use the `shipping-a-release` skill (`.claude/skills/shipping-a-release/`) for the pre-flight checks, the `@version` bump, the two notes files and the `@updateURL` trap.

**`@version` is CalVer plus a revision that starts at `.1`**: `YYYY.M.D.1`, then `.2` for a second release the same day, starting over at `.1` on a new day. Never write a bare `YYYY.M.D` and never write `.0` — Stylus compares a missing part as 0, so `2026.9.10` and `2026.9.10.0` compare *equal* to each other and no update is offered. Releases published before this scheme keep their plain `YYYY.M.D` and are not renamed. The skill has the comparator it was read from.

## Open items

Residual uncertainty, not pending work. The `--u-media-px` slack constant is **not** on this list: 12–13px was measured on a live page, and the reasoning behind picking 12 is recorded at the declaration itself. Do not reopen it.

- **No Chromium floor has been established.** Firefox 126 is the only floor stated anywhere. The style is known to work in one ungoogled-chromium build (2026-09-10) and nothing narrower has been checked. `README.md` and `USw-notes.md` both now say as much — not restricted, confirmed once, no floor, treat as lightly tested — so a Chromium user is no longer left with nothing. What is still open is whether to claim support properly, which needs a version actually tested.
- An inherited `:not(.xtcbf50)` was removed from the two-column selector. The class was absent everywhere checked, live and saved, so no offline test can validate the removal — restore it first if a post type ever lays out wrongly.
- The post-page **column widths** were measured against one aspect ratio each. Both 3:4 carousel snapshots hold media 449px wide, so that is the only shape `--u-post-width` has been checked against — and, since 2026-09-11, the only shape it still *reaches*: a square carousel has no `--x-maxWidth` and is capped by `--u-post-photo-width` instead. A landscape carousel is untested and no snapshot of one exists. The defaults are picked compromises, not derived numbers: do not write arithmetic justifying one, and do not treat a default as evidence of anything.
- **On the POST and REEL pages, reels are only handled at 9:16.** Every reel snapshot of those pages is `padding-bottom:177.778%`, and the rule that collapses that box matches the literal `177`. A reel of any other ratio keeps Instagram's box on all three reel URLs. Same limitation the reel pages always had; it is not new to the post-permalink paths. The **feed** is no longer in this position — since 2026.9.11.7 a non-125% feed reel is sized from the video's intrinsic dimensions instead, which needs no ratio matching at all. See the note in `docs/rule-notes.md`, including what that mechanism has *not* been proven against.
- **Only one landscape ratio has been measured.** Both landscape snapshots are the same 16:9 post at 56.4394%. The guard that exempts landscape from the width cap reads the leading digit, so it covers the whole 52.36–99.99% range by construction rather than by measurement — but no 3:2 or 1.91:1 capture exists to confirm Instagram builds those columns the same way.
- **Instagram re-derives a carousel slide's width from its container — confirmed live on 2026-09-11, and the reason a snapshot will always disagree.** Each slide frame carries an inline literal `width:<n>px` written by Instagram's JS, with the slide offsets as multiples of it; SingleFile freezes both. So on the saved square-carousel page the cap narrows the container while the slide stays 1262, and any offline measurement reports a 493px overflow. That is the capture, not the page: live, the slides resize correctly at every `--u-post-photo-width` value and each lands accurately in the frame, the same way they do on unstyled Instagram when the viewport is resized. Treat an overflow reported against this snapshot as expected, and do not add a zoom or a derived-scale rule to correct it.

- **Before reaching for `zoom` on a carousel, check how the slide's width is written** — the feed and the post pages differ, and both were read live in DevTools on 2026-09-11. On the **feed** the div inside each `li` carries `width: calc(-2px + min(470px, 100vw))`, a static CSS expression that references nothing we touch, so the slide stays 468px and `zoom` scales it cleanly; the `translateX` offsets are JS-written px but are multiples of that same fixed width. On a **post page** the same div carries a literal `width:1262px` that Instagram's JS derived from the container, so widening the container made it recompute and the zoom cancelled exactly — which is why that rule and `--u-post-media-scale` were removed in 2026.9.11.4 while the feed's `--u-carousel-scale-max` was kept. Feed media is served at full resolution (a slide measured 3277×4096 in a 468px box), so scaling it up is not upscaling.

- A **mixed carousel** (photo plus video slides) on a `/p/` URL is the one page shape both `regexp()` blocks could claim at once. Everything measurable says it is harmless and nothing was written against it, because no snapshot of one exists. See the `Not done` entry under 2026.9.10.1 in `CHANGELOG.md` for the measurements and for what to try first if one lays out wrongly.
