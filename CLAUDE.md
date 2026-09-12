# Instagram Desktop site — UserCSS

A userstyle for the desktop web at `www.instagram.com`, published to [userstyles.world](https://userstyles.world/) under the user `boneyland`. Stylus is required; the browser is not restricted to Firefox. Despite being built on `@-moz-document`, the style was confirmed working under Stylus for Chromium on 2026-09-10 (ungoogled-chromium). The mechanism has not been verified here — presumably Stylus does the `@-moz-document` URL matching itself rather than handing the at-rule to the engine, but treat that as inference. Under git since 2026-09-11, with the remote intended to be public. `Instagram_snapshots/` and `Preview_1246.png` are deliberately **untracked** — both capture a logged-in session — so a fresh clone cannot run either verification script until snapshots are captured locally. `.gitignore` gives the reason for every exclusion.

## Files

| File | Role |
| --- | --- |
| `Instagram.user.css` | The style. This is the deliverable. |
| `Instagram-20260912-uploaded.user.css` | The currently published version, `2026.9.12.1`. Diff the deliverable against this one, and write each new `CHANGELOG.md` entry and the whole of `USw-notes.md` as a comparison with it — **do not edit**. There is one uploaded copy per publication, so the newest by date is always the baseline; check before assuming. |
| `Instagram-20260910-uploaded.user.css`, `Instagram-20260907-uploaded.user.css` | Previously published versions. Kept for history — **do not edit**. |
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
| `Instagram_feed2.html` | A second, richer feed — 11 articles, three of them reels, and the only **feed** snapshot with a landscape reel (article 4, `padding-bottom:56.4263%`). Also the only snapshot holding a **mixed carousel** (article 7: three slides, two with `video`, one with `img`, all in 125% boxes) and a **9:16 single photo** (article 10, a sponsored post in a `padding-bottom:177.8%` box with no video in the article). `verify.py` uses this one: `find_snapshot()` takes the newest `Instagram_feed*.html`, so a fresh capture is picked up without editing it. |
| `Instagram-user-reel-id(reel177).html` | Snapshot of `/<user>/reel/<id>/`. |
| `Instagram-reels-id.html` | Snapshot of `/reels/<id>/`, captured as the floating dialog (it has a `[role="dialog"]`). Matches no selector in the style. |
| `Instagram-p-id(carousel133).html`, `Instagram-user-p-id(carousel133).html` | A **3:4 carousel** on the two post-permalink paths. Structurally identical to each other; no feed selector reaches either. Their column carries `.xf68679` and an inline `--x-maxWidth:min(100%,785px)`. |
| `Instagram-p-id(carousel100).html` | A **square (1:1) carousel**, and the snapshot that proves carousels have *two* layouts, exactly as single photos do. Its column carries **no `--x-maxWidth` at all**, so until 2026-09-11 every carousel rule missed it and only the two text rules from the `domain()` block reached the page. Media 1262×1262 at a 1638px window. |
| `Instagram-p-id(carousel75).html` | A **4:3 landscape carousel**, and the snapshot that retires "a landscape carousel is untested". Its column carries **no `--x-maxWidth`**, exactly like the square one, so the same no-token rule caps it with `--u-post-photo-width`: 1598 → 1150 at a 1638px window, caption 335 → 380. Its slide boxes are `75%` and `74.9712%`, so the set is continuous here too. |
| `Instagram-p-id(single_photo75).html` | A **4:3 landscape single photo**. Treated identically to the 16:9 one — the width cap's leading-digit guard rejects `75%` and `56.4394%` alike, so both keep Instagram's 1598px column and receive only the caption-column setting. Any difference between the two is appearance, not coverage. |
| `Instagram-p-id(reel177).html`, `Instagram-user-p-id(reel177).html` | A **9:16 reel** on the same two paths — the same post captured twice. Identical to each other *and* to `Instagram-user-reel-id(reel177).html`, which is a different reel by a different user: a reel gets one layout wherever it is reached from. Every one of the three carries the inline `--x-maxWidth:min(100%,673px)` that the reel rules are keyed on. |
| `Instagram-user-p-id(reel56).html`, `Instagram-user-p-id(reel75).html`, `Instagram-user-reel-id(reel69).html`, `Instagram-user-reel-id(reel88).html` | **Landscape reels**, captured 2026-09-12 at `56.2696%`, `75%`, `69.4981%` and `88.8614%`, two on each of the two URL shapes. They are what proved a landscape reel's column carries **no `--x-maxWidth`**, which is why every reel rule missed them and only the text settings reached the page. Now handled by `.xvc5jky:not([style*="--x-maxWidth"]):has(video)`. Measured at the defaults, 1638px window, stock → styled: `reel56` 1598×712 → 1150×452 with the video 1262×710 → 769×433, `reel88` 1598×1123 → 1150×685, `reel75` 1598×949 → 1150×579, `reel69` 1598×879 → 1150×536; caption 335 → 380 on all four. |
| `Instagram-p-id(single_photo100).html`, `Instagram-user-p-id(single_photo100).html` | A **square (1:1) single photo** on the same two paths, again the same post twice. Its column carries **no `--x-maxWidth` at all** — Instagram omits the `.xf68679` class that reads it — so nothing caps the column and the media fills the content area: 1262×1262 at a 1638px window, and wider on a wider screen. |
| `Instagram-user-p-id(single_photo133).html` | A **3:4 portrait single photo**, and the snapshot that proves single photos have *two* layouts. This one's column does carry `.xf68679` and an inline `--x-maxWidth:min(100%,785px)`, giving 449×599 — the same numbers a carousel starts from. |
| `Instagram-p-id(single_photo56).html`, `Instagram-user-p-id(single_photo56).html` | A **16:9 landscape single photo** on the same two paths, the same post twice. Its column is built like the square one — no `.xf68679`, no inline `--x-maxWidth` — but stock it renders 1262×712 in a 1598px column, which is already good, so it is the one single-photo shape the width cap is deliberately **withheld** from. It gets the caption-column setting and nothing else. These two are also by far the largest DOMs of any snapshot, ~16.5k elements against ~1–3k elsewhere. |
| `Instagram-p-id-modal(single_photo).html` | The **same post as those two**, captured as the floating modal opened over a profile grid. Its URL is the plain `/p/<id>/` permalink, so both `regexp()` blocks select it — but no rule in either reaches it, so only the `domain()` block does. Two separate guards do that work, and both were measured here: `main div[style*="--x-maxWidth"]` matches 0 (the page's one `--x-maxWidth` element is inside the dialog, not under `main`, and carries `inherit` rather than a width), and `main > div > div.xvc5jky` matches 0 — **`.xvc5jky` itself matches 5**, all inside the dialog, so it is the `main > div > div` child chain and not the class that keeps the carousel and single-photo rules off. Loosen that chain to a descendant combinator and every one of them fires on the modal. It is the one saved page with an `<article>` **inside** a `[role="dialog"]`, which makes it the test for the modal guards. |

## Structure

**Two** `@-moz-document` blocks, and which one owns a page matters more than it looks:

| Block | Covers | Keyed on |
| --- | --- | --- |
| `domain("www.instagram.com")` | the feed, and anything else site-wide | `article`, and inline `min(470px` |
| `regexp(.../(p\|[^/]+/p\|[^/]+/reel)/...)` | **every post shape** on `/p/<id>/`, `/<user>/p/<id>/` and `/<user>/reel/<id>/` | a `video`, the carousel's `li[style*="translateX"]`, or a photo box with neither — and, throughout, whether the column carries an inline `--x-maxWidth` |

It was three blocks until 2026-09-12. The reel path was added to the post block because **every post shape is reachable at `/<user>/reel/<id>/`, not just reels** (the user's live observation), which left the two `regexp()` conditions identical character for character, and they were then merged. Nothing about the rules changed in the merge: they never overlapped by URL, only by selector. Three post shapes share three URL patterns, and **every rule stays in its lane by selector, not by URL** — do not reach for a new block to separate two shapes.

**The lever a post-page rule can use is decided by one thing: whether Instagram wrote an inline `--x-maxWidth` on the column.** Measured across all twenty-one snapshots, it writes one only when the media is taller than square:

| Media | `padding-bottom` | inline `--x-maxWidth` |
| --- | --- | --- |
| 9:16 reel | 177.778% | yes, `min(100%,673px)` |
| 3:4 carousel, 3:4 single photo | 133.333% | yes, `min(100%,785px)` |
| square carousel, square photo | 100% | **no** |
| every landscape shape — reels at 88.8614/75/69.4981/56.2696%, carousels at 75%, photos at 75/56.4394% | below 100% | **no** |

So the token is present exactly where the media is portrait, and absent everywhere else — which is why the no-token rules are written `:not([style*="--x-maxWidth"])` on the element **itself** rather than as a test for squareness, and why they cover square and landscape alike. A 4:5 (125%) post is the one gap in the table: it exists only on the feed, so which side of the boundary it falls on has never been measured. `.xvc5jky` in those selectors is load-bearing: without it the guards also match the "more posts" grid below the post.

Carousels are likewise handled by **two** rules, on the same principle. The caption column (`--u-reel-media-info`) is set for *every* carousel, on the `.xvc5jky` container rather than on `:root` — which is both why it reaches a square carousel and why it needs no `!important`. The width cap (`--u-post-photo-width`, the *single-photo* setting, so the two square shapes land on the same width) is applied to every carousel whose column carries **no** token, square and landscape alike, guarded by `:not([style*="--x-maxWidth"])` on the element **itself** — the token is an inline style on `.xvc5jky` directly, so a `:not(:has(...))` spelling matches nothing and would silently cap the 3:4 carousels too. **Neither carousel shape has a zoom rule**, as of 2026.9.11.4. One existed for the 3:4 shape and was removed once a live check showed it changed nothing: Instagram re-derives each slide's width from its container, so capping the container is the whole job. Do not add one back without a live measurement — see the removal record under 2026.9.11.4 in `CHANGELOG.md`.

Single photos are handled by **two** rules on the same pattern, and the split is the thing to understand before touching either. The caption column (`--u-reel-media-info`) is set for *every* shape. The width cap (`--u-post-photo-width`) is withheld from **landscape**, whose stock layout is already good — capping it made things worse, 1262×712 down to 670×378. The fourth guard on the capped rule reads the *leading digit* of the `padding-bottom` percentage: everything ≥100% starts with `1`, everything landscape starts 5–9, and Instagram accepts nothing ≥200%. The comma inside that `:has()` is a **list, not nesting**, which is what makes it legal.

Feed reels are handled by **two** families of rule, split on `[style*="125%"]` versus `:not([style*="125%"])`, and the split is total: Instagram flattens anything taller than 4:5 into a 125% box, and everything else keeps its true ratio. The 125% family caps the anchor with arithmetic against the known 1.25; the non-125% family cannot, because CSS cannot read a ratio that exists only inside an inline style, so it drops the padding box and sizes the video from its own intrinsic dimensions. That second family is the one thing here **no snapshot can check** — SingleFile strips video sources and the poster, so offline it renders at `<video>`'s 300×150 default and any measurement of it is meaningless. It was confirmed on the live feed instead. Read its note in `docs/rule-notes.md` before touching it, and expect to need another live check rather than a passing script.

Reels on these pages are handled by **two** families of rule, split the same way everything else on the page is — on whether the column carries the token. A **9:16** reel has one, so the reel rules proper apply: `--media-info` from `:root`, and a column bounded three ways — `100%`, `--u-reel-width`, and `--u-reel-height` converted into the column width a 9:16 video needs to reach that height. Bounding the column is the whole mechanism: the `padding-bottom:177.778%` box then keeps its own ratio for free. A rule that collapsed that box to a fixed `min(95vh, 950px)` was removed on 2026-09-12 — it letterboxed at every setting, since the video is `object-fit: contain` — and **must not be written back**; `docs/rule-notes.md` keeps its measurements under a removed heading. Every **landscape** reel has no token, so it is caught instead by one rule shaped exactly like the square-carousel and square-photo caps — `.xvc5jky:not([style*="--x-maxWidth"]):has(video)`, setting `--u-post-photo-width` and the caption column together. The shape still unhandled is a **portrait reel that is not 9:16**: it takes the token, so it takes the column, but the `9/16` arithmetic sizes it conservatively. No snapshot of one exists.

A mixed carousel (photo plus video slides) whose column has no token now matches **two** rules — the slide-list cap and that new `:has(video)` cap. They set the same property to the same value, so it is harmless; it is the one place in the block where two rules deliberately overlap. See the `Not done` entry under 2026.9.10.1 in `CHANGELOG.md`.

A reel gets the same layout on all three of its URLs — proven against three 9:16 snapshots, two of them the same post and the third a different reel by a different user, and again across the four landscape ones, two on `/<user>/p/` and two on `/<user>/reel/` — which is why one block covers them and no post-page-specific reel setting exists.

Not every selector is safe outside its block. The post-page zoom selector matches a 470×3644 region on a **feed** page and would scale the feed's text with it — the URL scoping, not the selector, is what keeps it off. The post block's `:root` token rule has the same shape of hazard: its guard matches on the saved feed too, so unscoping it would push `--media-info` across the whole feed. So does the `177` rule, which matches a **photo** on the saved feed — `Instagram_feed2.html` article 10 is a sponsored single photo in a `padding-bottom:177.8%` box. Check before moving a rule between blocks.

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

**Never match a whole percentage in an attribute selector — and never match a bare one either.** One ratio reaches the DOM under several spellings: a single saved feed carried 3:4 as `133.333%`, `133.33333333333331%` and `133.31719128329297%`, and 16:9 has now been seen as `56.25%`, `56.2696%`, `56.4263%` and `56.4394%` across saved and live pages. The percentages are computed from the media's real pixel dimensions — `68.125%` is exactly `109/160` — so treat the set as continuous. Match a distinctive prefix.

**The mirror-image trap: a bare `[style*="125%"]` is a substring test over the whole attribute, and `padding-bottom:68.125%` contains `125%`.** That misclassified a landscape reel as a flattened portrait one until 2026.9.12.1. Anchor the match to the property name and the whole value, in both spellings: `:is([style*="padding-bottom:125%"], [style*="padding-bottom: 125%"])`, negated as two chained `:not()`s. The trailing `%` is what stops it swallowing `125.5%`.

Matching `125%` whole is the deliberate exception to the paragraph above, because it is **not a computed ratio**: it is the constant Instagram clamps anything taller than 4:5 to. Across all twenty-one snapshots the round values occur only as the bare `75%`, `100%` and `125%`, while every computed value carries decimals. Exactness is what the reel split needs; a prefix is what would break it.

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
- The post-page **column widths** were measured against one aspect ratio each. Both 3:4 carousel snapshots hold media 449px wide, so that is the only shape `--u-post-width` has been checked against — and, since 2026-09-11, the only shape it still *reaches*: every other carousel measured has no `--x-maxWidth` and is capped by `--u-post-photo-width` instead. The defaults are picked compromises, not derived numbers: do not write arithmetic justifying one, and do not treat a default as evidence of anything.
- **On the POST and REEL pages, a portrait reel that is not 9:16 is the one reel shape still sized by guesswork.** Landscape reels were the gap until 2026-09-12: four ratios — `56.2696%`, `75%`, `69.4981%`, `88.8614%` — were reported live as responding to nothing but the text settings, then captured, and the cause measured. Their column carries **no inline `--x-maxWidth`**, and every reel rule was keyed on that token. They are now caught by `.xvc5jky:not([style*="--x-maxWidth"]):has(video)` and all four measure correctly. What remains is the other side of the boundary: a portrait reel between 100% and 177% carries the token, so it takes the bounded column, but the height term converts `--u-reel-height` through `9 / 16`, which is right only at 9:16 — anything shallower comes out under its height budget rather than filling it. Safe, never wrong-way, but not exact. A census of every inline `padding-bottom` box across all twenty-one snapshots found no `video` in any 133% box on any page, so a 3:4 reel has never been captured anywhere; on the feed it could not be, since Instagram flattens anything taller than 4:5 to 125%. The **feed** has no equivalent gap — since 2026.9.11.7 a non-125% feed reel is sized from the video's intrinsic dimensions, which needs no ratio matching at all. See the note in `docs/rule-notes.md` before touching that one: it cannot be measured offline.
- **A 9:16 single photo is handled on the feed and untested on a post page.** `Instagram_feed2.html` article 10 is a sponsored photo post in a `padding-bottom:177.8%` box with no `video` anywhere in the article — so Instagram does accept a photo at that ratio, and the feed's shape-agnostic photo rules size it like any other. On a post page the width cap's leading-digit guard would cap it, since `177` starts with `1`, but no post-page snapshot of one exists. That same box is also why the reel block stays URL-scoped: `main div[style*="padding-bottom"][style*="177"]` matches it on the saved feed.
- **The landscape range is now measured at seven points, all of them below 100%.** Photos at `56.4394%` and `75%`, a carousel at `75%`/`74.9712%`, and reels at `56.2696%`, `69.4981%`, `75%` and `88.8614%`. Every one of them has no inline `--x-maxWidth`, which is what the leading-digit guard and the `:not([style*="--x-maxWidth"])` guards both depend on. The 52.36–99.99% range is still covered by construction rather than end to end, and the closest capture to the 100% boundary is 88.8614%; nothing at 1.91:1 exists.
- **Instagram re-derives a carousel slide's width from its container — confirmed live on 2026-09-11, and the reason a snapshot will always disagree.** Each slide frame carries an inline literal `width:<n>px` written by Instagram's JS, with the slide offsets as multiples of it; SingleFile freezes both. So on the saved square-carousel page the cap narrows the container while the slide stays 1262, and any offline measurement reports a 493px overflow. That is the capture, not the page: live, the slides resize correctly at every `--u-post-photo-width` value and each lands accurately in the frame, the same way they do on unstyled Instagram when the viewport is resized. Treat an overflow reported against this snapshot as expected, and do not add a zoom or a derived-scale rule to correct it.

- **Before reaching for `zoom` on a carousel, check how the slide's width is written** — the feed and the post pages differ, and both were read live in DevTools on 2026-09-11. On the **feed** the div inside each `li` carries `width: calc(-2px + min(470px, 100vw))`, a static CSS expression that references nothing we touch, so the slide stays 468px and `zoom` scales it cleanly; the `translateX` offsets are JS-written px but are multiples of that same fixed width. On a **post page** the same div carries a literal `width:1262px` that Instagram's JS derived from the container, so widening the container made it recompute and the zoom cancelled exactly — which is why that rule and `--u-post-media-scale` were removed in 2026.9.11.4 while the feed's `--u-carousel-scale-max` was kept. Feed media is served at full resolution (a slide measured 3277×4096 in a 468px box), so scaling it up is not upscaling.

- A **mixed carousel** (photo plus video slides) on a `/p/` URL remains uncaptured, but one now exists on the **feed** — `Instagram_feed2.html` article 7, three slides, two with `video` and one with `img`, all in 125% boxes inside `li`. The feed reel rules miss it on the `a[href*="/reels/"]` guard and the feed photo rules on `:not(li *)`, so it is handled by the carousel zoom alone. On a post page such a carousel with no token would match two rules at once, the slide-list cap and the `:has(video)` cap, which set the same property to the same value. See the `Not done` entry under 2026.9.10.1 in `CHANGELOG.md` for what to try first if one lays out wrongly.
