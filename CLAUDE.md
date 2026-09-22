# Instagram Desktop site — UserCSS

A userstyle for the desktop web at `www.instagram.com`, published to [userstyles.world](https://userstyles.world/style/30052/instagram-desktop-site) under the user `boneyland` — **that page is the authority on which version is live.** Stylus is required; the browser is not restricted to Firefox. Despite being built on `@-moz-document`, the style was confirmed working under Stylus for Chromium on 2026-09-10 (ungoogled-chromium). The mechanism has not been verified here — presumably Stylus does the `@-moz-document` URL matching itself rather than handing the at-rule to the engine, but treat that as inference. Under git since 2026-09-11, with the remote intended to be public. `Instagram_snapshots/` is deliberately **untracked** — it captures a logged-in session — so a fresh clone cannot run either verification script until snapshots are captured locally. `.claude/` was added to `.gitignore` on 2026-09-18 and the `shipping-a-release` skill went untracked with it, so the release checklist is local to this machine and absent from a clone; the last tracked copy is `git show e88eb2e^:.claude/skills/shipping-a-release/SKILL.md`. `.gitignore` gives the reason for every exclusion.

## Files

| File | Role |
| --- | --- |
| `Instagram.user.css` | The style. This is the deliverable. |
| `Instagram-20260907-uploaded.user.css`, `Instagram-20260910-uploaded.user.css` | The two published versions that predate the repository. Neither blob ever existed as `Instagram.user.css` here, so no tag can carry them — these files are the only copy. Kept for history — **do not edit**. |
| `CHANGELOG.md` | Release notes per `@version`, current releases only — `2026.9.12.1` and later. The style file itself carries no changelog. |
| `docs/changelog-archive.md` | Releases before `2026.9.12.1`, verbatim. Not edited; look here for the history of an older entry. |
| `docs/removed.md` | **Why something is not in the style**, organized by subject rather than by release: every deletion and every deliberate omission, with the evidence. Read the entry before re-adding a rule of the same shape. |
| `USw-notes.md` | The whole Notes field on userstyles.world, ready to paste as-is: a summary of what the style changes, the requirements, and the user-facing changelog since the last *published* version — not every version. Keep it short and send the reader to GitHub for the rest. Mechanism and internals stay out of it. |
| `README.md` | The repository's public front page: what the style does, requirements, the settings table and the known limitations. Audience is a GitHub visitor, not a maintainer — keep internals out of it, and keep the settings table in step with the header. |
| `docs/token-overrides.md` | Why the five design-token overrides work, and how to measure a token's reach. Read before adding a sixth. |
| `docs/rule-notes.md` | Why each rule is written the way it is, and what was measured to get there — the style carries no comments, so this is the only explanation that exists. This file holds the index, the whole-file inline-style rule and the `:root` notes. **Read the note for a rule before loosening a guard or changing a number**; use the index rather than reading a whole file. |
| `docs/rule-notes-feed.md` | The notes for the `domain()` block — the feed and anything site-wide. |
| `docs/rule-notes-post.md` | The notes for the `regexp()` block — every post shape on `/p/`, `/<user>/p/` and `/<user>/reel/`. |
| `docs/open-questions.md` | Residual uncertainty, not pending work: the shapes that are untested or covered only by construction. The prohibitions these carry are duplicated into the Hard rules below. |
| `docs/snapshots.md` | Every SingleFile capture and what it is evidence for. Read it to pick the snapshot that exercises a rule. |
| `.claude/skills/shipping-a-release/` | The release checklist for userstyles.world. **Untracked since 2026-09-18** — local to this machine only. Nothing else in the repository carries the Stylus version comparator, the `@updateURL` trap or the record that mirroring is deliberately unused, so read it before shipping and recover it from history if it is missing. |
| `verify.py` | Verification harness (see below). Run before shipping. |
| `scoped.py` | The `@-moz-document` half of verification, which `verify.py` is blind to. See below. |
| `unwrap.py` | Joins hard-wrapped Markdown paragraphs into one line each, leaving fenced blocks, tables and headings verbatim. Checks that the result is equivalent — same text with all whitespace removed, same block structure — and refuses to write if it is not. `unwrap.py FILE` to check, `--write` to apply. |
| `Instagram_snapshots/` | Every SingleFile snapshot. Both scripts read this folder and nothing else — `verify.py` sets `SNAPSHOTS`, `scoped.py` imports it. |
| `node_modules/` | One package, `usercss-meta`. |

**Every published version from `2026.9.12.1` onward is an annotated git tag, `v<@version>`, and the tag is the baseline for diffing.** The newest is `git tag --sort=-v:refname | head -1`; retrieve a published file with `git show v2026.9.22.1:Instagram.user.css`, and diff the deliverable against the newest tag with `git diff $(git tag --sort=-v:refname | head -1) -- Instagram.user.css`. Each tag points at the earliest commit whose `Instagram.user.css` is byte-identical to what was uploaded, and its message records the check. Write each new `CHANGELOG.md` entry and the whole of `USw-notes.md` as a comparison with the newest tag. A tag records what was **committed**, not what was pasted into the website, so the release procedure is commit, then tag, then paste the tagged file — never edit the file between the tag and the upload. The tags still cannot settle which version is actually **live**: read that off [the style's page on USw](https://userstyles.world/style/30052/instagram-desktop-site) and match it to a tag here. Ask rather than inferring if the page is unreachable.

The snapshots themselves — **22 captures as of 2026-09-22**, and what each one is evidence *for* — are in `docs/snapshots.md`. The folder was re-captured that day, so counts written into older notes and changelog entries describe a corpus of 21-22 that no longer exists; that file dates the change and lists which captures carry Instagram's new `x1ykew4q` wrapper. Read it when you need the capture that exercises a rule you are about to change. Three earn a mention here: `Instagram_feed3.html` is the newest feed and therefore **the one `verify.py` now loads**, `Instagram_feed2.html` is the richest and holds the only mixed carousel and the only 9:16 single photo, and `Instagram-p-id-modal(single_photo).html` was long the only saved page with an `<article>` inside a `[role="dialog"]`. **There are now four modal captures** — three post modals and, since 2026-09-22, `Instagram_reel_modal_over_profile.html` at the bare `/reel/<id>/` — so a modal guard must be checked against all four rather than that one. It remains the strictest of them for the caption column: the only capture whose comment text is long enough to overflow a narrow column, which is what sets the setting's lower bound.

## Structure

**Two** `@-moz-document` blocks, and which one owns a page matters more than it looks:

| Block | Covers | Keyed on |
| --- | --- | --- |
| `domain("www.instagram.com")` | the feed, anything else site-wide, and **every modal** — post and reel alike | `article`, inline `min(470px`, and `[role="dialog"]` for the modal caption rule |
| `regexp(.../(p\|[^/]+/p\|[^/]+/reel)/...)` | **every post shape** on `/p/<id>/`, `/<user>/p/<id>/` and `/<user>/reel/<id>/` | a `video`, the carousel's `li[style*="translateX"]`, or a photo box with neither — and, throughout, whether the column carries an inline `--x-maxWidth` |

It was three blocks until 2026-09-12. The reel path was added to the post block because **every post shape is reachable at `/<user>/reel/<id>/`, not just reels** (the user's live observation), which left the two `regexp()` conditions identical character for character, and they were then merged. Nothing about the rules changed in the merge: they never overlapped by URL, only by selector. Three post shapes share three URL patterns, and **every rule stays in its lane by selector, not by URL** — do not reach for a new block to separate two shapes.

**The lever a post-page rule can use is decided by one thing: whether Instagram wrote an inline `--x-maxWidth` on the column.** Measured across the 21 snapshots present when the census was taken, it writes one only when the media is taller than square:

| Media | `padding-bottom` | inline `--x-maxWidth` |
| --- | --- | --- |
| 9:16 reel | 177.778% | yes, `min(100%,673px)` |
| 3:4 carousel, 3:4 single photo | 133.333% | yes, `min(100%,785px)` |
| 4:5 carousel — live check only, never captured | 125%, from the ratio | yes; the value was not read |
| square carousel, square photo | 100% | **no** |
| every landscape shape — reels at 88.8614/75/69.4981/56.2696%, carousels at 75%, photos at 75/56.4394% | below 100% | **no** |

So the token is present exactly where the media is portrait, and absent everywhere else — which is why the no-token rules are written `:not([style*="--x-maxWidth"])` on the element **itself** rather than as a test for squareness, and why they cover square and landscape alike. The 4:5 row is the one that came from a live check rather than a capture, and it is the reason the row above it no longer names a single ratio: on 2026-09-14 the user reported a **4:5 carousel on the post and reel pages responding to `--u-post-width`**, which only a column carrying the token can do, so 4:5 falls on the portrait side alongside 3:4 and `--u-post-width` is now labelled "portrait carousel". A 4:5 **single photo** is still unplaced, and nothing depends on placing it: both single-photo rules are token-agnostic, the cap being guarded by the leading digit of the `padding-bottom` percentage, which `125%` passes either way. No **9:16 carousel** has been seen at all. `.xvc5jky` in those selectors is load-bearing: without it the guards also match the "more posts" grid below the post.

Carousels are likewise handled by **two** rules, on the same principle. The caption column (`--u-reel-media-info`) is set for *every* carousel, on the `.xvc5jky` container rather than on `:root` — which is both why it reaches a square carousel and why it needs no `!important`. The width cap (`--u-post-photo-width`, the *single-photo* setting, so the two square shapes land on the same width) is applied to every carousel whose column carries **no** token, square and landscape alike, guarded by `:not([style*="--x-maxWidth"])` on the element **itself** — the token is an inline style on `.xvc5jky` directly, so a `:not(:has(...))` spelling matches nothing and would silently cap the portrait carousels too. **Neither carousel shape has a zoom rule**, as of 2026.9.11.4. One existed for the 3:4 shape and was removed once a live check showed it changed nothing: Instagram re-derives each slide's width from its container, so capping the container is the whole job. Do not add one back without a live measurement — see `docs/removed.md`.

Single photos are handled by **two** rules on the same pattern, and the split is the thing to understand before touching either. The caption column (`--u-reel-media-info`) is set for *every* shape. The width cap (`--u-post-photo-width`) is withheld from **landscape**, whose stock layout is already good — capping it made things worse, 1262×712 down to 670×378. The fourth guard on the capped rule reads the *leading digit* of the `padding-bottom` percentage: everything ≥100% starts with `1`, everything landscape starts 5–9, and Instagram accepts nothing ≥200%. The comma inside that `:has()` is a **list, not nesting**, which is what makes it legal.

Feed reels are handled by **two** families of rule, split on `[style*="125%"]` versus `:not([style*="125%"])`, and the split is total: Instagram flattens anything taller than 4:5 into a 125% box, and everything else keeps its true ratio. The 125% family caps the anchor with arithmetic against the known 1.25; the non-125% family cannot, because CSS cannot read a ratio that exists only inside an inline style, so it drops the padding box and sizes the video from its own intrinsic dimensions. That second family is the one thing here **no snapshot can check** — SingleFile strips video sources and the poster, so offline it renders at `<video>`'s 300×150 default and any measurement of it is meaningless. It was confirmed on the live feed instead. Read its note in `docs/rule-notes-feed.md` before touching it, and expect to need another live check rather than a passing script.

Reels on these pages are handled by **two** families of rule, split the same way everything else on the page is — on whether the column carries the token. A **9:16** reel has one, so the reel rules proper apply: `--media-info` from `:root`, and a column bounded three ways — `100%`, `--u-reel-width`, and `--u-reel-height` converted into the column width a 9:16 video needs to reach that height. Bounding the column is the whole mechanism: the `padding-bottom:177.778%` box then keeps its own ratio for free. A rule that collapsed that box to a fixed `min(95vh, 950px)` was removed on 2026-09-12 — it letterboxed at every setting, since the video is `object-fit: contain` — and **must not be written back**; `docs/rule-notes-post.md` keeps its measurements under a removed heading. Every **landscape** reel has no token, so it is caught instead by one rule shaped exactly like the square-carousel and square-photo caps — `.xvc5jky:not([style*="--x-maxWidth"]):has(video)`, setting a width cap and the caption column together. Since 2026-09-14 that width cap is **`--u-reel-landscape`, a setting of its own**; it read `--u-post-photo-width` until then, which left one setting driving six shapes through three rules. Its guard is "no token", which means square **or** landscape, so a 1:1 reel takes it too — confirmed live on 2026-09-17, which is why the setting reads "square/landscape reel"; still never captured, so nothing offline exercises it. A **portrait reel that is not 9:16** is handled but sized conservatively, and that is now measured rather than inferred: it takes the token, so it takes the column, but the height term converts through `9/16`, so a reel of ratio R reaches `H × 9/16 × R` -- exact at 9:16 and short of the budget everywhere else. Checked live on a 3:4 reel on 2026-09-14, 1638px viewport, height 1200 and width high enough not to bind: media 674×898.667, three quarters of the height asked for. Safe and never wrong-way, so **do not "fix" it by reintroducing a fixed height**. The box's own `padding-bottom` carries the true ratio on these pages, unlike the feed's clamped 125%, so an exact version is possible at one rule per known ratio -- not written, and not to be written without asking. No snapshot of a sub-9:16 portrait reel exists, so nothing offline exercises this path.

A mixed carousel (photo plus video slides) whose column has no token matches **two** rules — the slide-list cap and that `:has(video)` cap. They set the same property, and since the 2026-09-14 split they set **different** values, so precedence decides: the slide-list cap wins on specificity, (0,3,4) against (0,2,4), and a mixed carousel takes the carousel setting rather than the landscape-reel one. Source order is never consulted, so **do not reorder these two rules expecting it to matter** — and do not "fix" the overlap by adding a `:not(:has(video))` guard to the carousel rule without measuring, since the current precedence is already the wanted outcome. It is the one place in the block where two rules deliberately overlap; the overlap matches 0 on all twenty-one snapshots, so it is covered by construction only. See `docs/open-questions.md` and `docs/removed.md`.

A reel gets the same layout on all three of its URLs — proven against three 9:16 snapshots, two of them the same post and the third a different reel by a different user, and again across the four landscape ones, two on `/<user>/p/` and two on `/<user>/reel/` — which is why one block covers them and no post-page-specific reel setting exists.

Not every selector is safe outside its block. The post-page zoom selector matches a 470×3644 region on a **feed** page and would scale the feed's text with it — the URL scoping, not the selector, is what keeps it off. The post block's `:root` token rule has the same shape of hazard: its guard matches on the saved feed too, so unscoping it would push `--media-info` across the whole feed. So does the `177` rule, which matches a **photo** on the saved feed — `Instagram_feed2.html` article 10 is a sponsored single photo in a `padding-bottom:177.8%` box. Check before moving a rule between blocks.

Neither `regexp()` block matches `/reels/<id>/` or the `/reel/<id>/` floating dialog, deliberately: the saved `/reels/<id>/` is a modal with its own markup that shares no selector with the others. **But `/reel/<id>/` is no longer untouched** — since 2026-09-22 the modal caption rule in the `domain()` block reaches it, which is exactly why that rule lives there rather than in the post block. Widening the post block's pattern to cover `/reel/<id>/` was rejected and should stay rejected: its other rules resize a column and a full-height video box, and none was measured against a dialog. A modal is reached by selector — `[role="dialog"]` — not by URL.

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
python3 scoped.py --diff old.user.css Instagram.user.css --only reel177   # just one snapshot
```

`--urls` full-matches each block condition against a table of URL shapes: the ones a block must cover and the near misses it must keep out. Extend that table when a new page type is taken on. `--diff` is the one to run after changing a `regexp()` — it applies both files to **every** snapshot with only the blocks that page's real URL selects, and diffs every computed property of every element. It reads each snapshot's URL from the `url:` comment SingleFile writes at the top, so there is no table of URLs to fall out of date.

Read its output for `font-size`, `line-height` or `zoom`. Those usually mean a container holding text was resized by mistake, which is the failure mode the post-page zoom rule had to be walked outward to avoid.

Two traps it exists to encode. `regexp()` matches the **whole** URL, so test with `re.fullmatch`, not `search`. And the CSS source spells the pattern `\\.`, a CSS string escape for one backslash — hand that to a regex engine unconverted and every condition silently fails to match, which reads as "no block applies" rather than as an error.

**Both scripts are memory-guarded, and the guard is not optional.** Measuring a snapshot means headless Firefox over 20–105MB of SingleFile HTML — the largest capture holds 23,589 elements — so a probe that keeps a computed-style table per sheet costs gigabytes. On 2026-09-21 the unguarded `--diff` froze the machine outright, past the point of anything but a power cycle, because this laptop backs ~15GB of RAM with zram swap and has no earlyoom: there is no clean OOM kill to rescue it. Two defences now, and each is load-bearing. `PROBE_CORE` in `verify.py` holds **one separator-joined string per element** instead of a property table, split back apart only for elements that actually differ — do not "tidy" this back into an object per element. And every launch goes through `run_firefox_guarded()`, which polls `MemAvailable` and SIGKILLs the process group past `MEM_FLOOR_MB` (2200, override with `VERIFY_FLOOR_MB`). `scoped.py` imports both, runs one browser per snapshot **smallest file first** so a run that cannot finish still banks every other row, and reports a killed snapshot as a failed row rather than taking the session down. A `x FAIL … fell below the floor` line means retry that one snapshot alone with `--only`, not that the style is wrong. `systemd-run --user --scope -p MemoryMax=` is not an alternative here — it cannot reach the user dbus from the sandboxed shell.

The cost is dominated by Firefox, not by the scripts. `Instagram-p-id(carousel75).html` is the expensive one — 105MB and 23,589 elements — and measuring it draws about **8GB**, reaching the floor with roughly 2.4GB to spare on an otherwise idle machine; the page copy and the probe together are a rounding error beside that. So a `!` warning line on that snapshot is normal, and the way to give a run more room is to close other things rather than to lower the floor. Two smaller levers exist and are already applied: the page is streamed to disk in binary instead of being rebuilt as a Python string, and the decoded-image surface cache is capped (worth ~80MB — measured, not assumed). `VERIFY_WORKDIR` moves the scratch copy off `/tmp`, which is worth setting to a disk-backed path because Fedora's `/tmp` is tmpfs and the copy is as large as the snapshot.

## Hard rules

**Never write the literal `@var` outside the metadata block — comments included.** `usercss-meta` scans the whole file, reads it as a malformed variable declaration, and the style fails to install. Only `@var` behaves this way; `@name`, `@license` and `var()` are safe. Write "the variables declared in the header" instead. `verify.py` checks for this by name.

**Every rule in the `domain()` block keyed on `article` needs `:not([role="dialog"] *)`.** `article` is not a feed-only hook: a post opened as a floating modal — clicking a post in the feed, or a `/p/<id>/` URL reached from a profile grid — renders as an `<article>` inside a `[role="dialog"]`, and picks up every unguarded rule. That page is laid out by Instagram and sized by its own inline `max-height`/`max-width`/`aspect-ratio`, so feed rules landing on it resize a layout they were never measured against. The Media section was missing the guard until 2026.9.10.1, which let a *feed* setting cap the photo's height in the modal; `docs/changelog-archive.md` has the measurements. `Instagram-p-id-modal(single_photo).html` is the snapshot that catches this — the only saved page with an `<article>` inside a dialog. Adding a guard is cheap to check: compare `document.querySelectorAll(sel).length` with and without it across every snapshot.

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

**The `--u-media-px` slack constant is settled.** 12–13px was measured on a live page, and the reasoning behind picking 12 is recorded at the declaration itself. Do not reopen it.

**A setting's default is a picked compromise, not a derived number.** Do not write arithmetic justifying one, and do not treat a default as evidence of anything. The post-page column widths were each measured against a single aspect ratio — `docs/open-questions.md` says which.

**Before reaching for `zoom` on a carousel, check how the slide's width is written** — the feed and the post pages differ, and both were read live in DevTools on 2026-09-11. On the **feed** the div inside each `li` carries a static `width: calc(-2px + min(470px, 100vw))` that references nothing we touch, so the slide stays 468px and `zoom` scales it cleanly. On a **post page** that same div carries a literal `width:<n>px` which Instagram's JS derived from the container, so widening the container makes it recompute and the zoom cancels exactly — which is why that rule and `--u-post-media-scale` were removed in 2026.9.11.4 while the feed's `--u-carousel-scale-max` was kept. **Do not add a zoom or a derived-scale rule to a post-page carousel**, and treat an overflow reported against the saved square-carousel page as expected rather than as a bug: SingleFile freezes the derived width, so an offline measurement there will always disagree with the live page. `docs/removed.md` has both records.

**An inherited `:not(.xtcbf50)` was removed from the two-column post selector, and no offline test can validate that.** The class was absent everywhere checked, live and saved, so it excluded nothing — but if a post type ever lays out wrongly, restoring the exclusion is the first thing to try.

## Comment conventions

**Never hard-wrap a Markdown file in this repo.** One line per paragraph, as every `.md` file here is now written. They are read on GitHub and in the userstyles.world Notes field, both of which soft-wrap, so a hard-wrapped line re-wraps raggedly. `unwrap.py` joins wrapped paragraphs and refuses to write unless the result is provably equivalent; run it if a file ever drifts back. The cost is that these files have no controlled measure in a viewer that does not wrap.

**The style carries no comments outside the metadata block.** Every one was stripped on 2026-09-11 — see `docs/removed.md`, which records the equivalence proof. **Do not reintroduce them.** `docs/rule-notes.md` is now the only explanation of why a rule is shaped the way it is, so when you change a rule, the note there is not a duplicate to keep in sync — it is the record. Write it.

The metadata block is the exception, and it is not really a comment: Stylus parses it, the labels in it are the settings UI, and the whole style fails to install without it.

**If comments are ever restored, they are user-facing.** The file ships to userstyles.world, where anyone editing it in Stylus reads them. A comment there would say what a rule does and what would break if you changed it — nothing else. Specifically **never** write into the style: snapshot filenames, element or selector counts, pixel measurements, `verify.py` / `scoped.py` / `CHANGELOG.md` references, or the history of what a rule used to be. And do not hard-wrap: one line per paragraph, blank comment lines between paragraphs, because both consumer viewers soft-wrap and a hard-wrapped line re-wraps raggedly in a narrow pane.

**Do not state a mechanism you have not verified.** Several comments were wrong because earlier sessions wrote plausible-sounding explanations as fact — a guard described as excluding one child when it excludes two, an `aria-label` claimed to be un-localised on the basis of a single English page, a specificity hack attributed to a rule nobody had looked at. If a claim is inference, say so. Existing markers: `INHERITED, POSSIBLY STALE`, "has not been confirmed", "untested". These markers belong in `docs/rule-notes.md` and the files it indexes, along with the claim they qualify; a user-facing comment should not be making a claim that needs one.

**When you delete something, record why and what the evidence was**, so it does not get re-added — in `docs/removed.md`, not in the style. The file ships to userstyles.world, so it carries no changelogs and no notes about what used to be there. See the removed-nav and `:not(.xtcbf50)` entries there.

## What the snapshot can and cannot prove

SingleFile pruned unused CSS and flattened inline-style whitespace on save.

*Can* prove: DOM structure and class presence, and equivalence between two versions of the style (both see the same DOM, so the pruning cancels out).

*Cannot* prove: whether a selector matches live, what Instagram's own CSS does, inline-style spacing, or anything on a page that was not captured. The snapshot is a feed page — its only `<nav>` is the **footer**, so the left sidebar, settings, and reel pages are all absent. A class missing from it is not evidence the class is dead.

Live checks are the user's to run; ask rather than guessing.

The Playwright MCP browser cannot open `file://` URLs or reach localhost from this sandbox. Local headless Firefox is the only way to run these checks.

## Publishing to userstyles.world

Publishing is manual — uploaded, typed or pasted directly into the USw website. No hosted source and no mirroring: the git repository is for history, not distribution, and userstyles.world is fed by hand from the deliverable.

Use the `shipping-a-release` skill (`.claude/skills/shipping-a-release/`, untracked — see the Files table) for the pre-flight checks, the `@version` bump, the two notes files and the `@updateURL` trap.

**`@version` is CalVer plus a revision that starts at `.1`**: `YYYY.M.D.1`, then `.2` for a second release the same day, starting over at `.1` on a new day. Never write a bare `YYYY.M.D` and never write `.0` — Stylus compares a missing part as 0, so `2026.9.10` and `2026.9.10.0` compare *equal* to each other and no update is offered. Releases published before this scheme keep their plain `YYYY.M.D` and are not renamed. The skill has the comparator it was read from.

## Open questions

Residual uncertainty, not pending work, lives in `docs/open-questions.md` — eleven entries covering the Chromium floor, the shapes covered by construction rather than end to end, and the ratios nothing has been captured at. **Read the relevant entry before claiming a shape is handled.** The four prohibitions those entries carry are stated in the Hard rules above, because they fire mid-edit with no trigger phrase; the evidence behind each is in that file.
