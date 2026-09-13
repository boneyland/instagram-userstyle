# Rule notes

Why each rule in `Instagram.user.css` is written the way it is, and what was measured to get there.

**This file exists because the style itself ships.** `Instagram.user.css` is uploaded to userstyles.world, where its comments are read by installers and by anyone editing the style in Stylus, so it carries only short explanations of what a rule does. Snapshot filenames, element counts, pixel measurements, references to `verify.py` / `scoped.py` / `CHANGELOG.md`, and the history of what a rule used to be are all project-internal — they belong here.

The notes are the reasoning as it stood in the style file before that split, preserved verbatim. Treat them as the evidence record for each rule: **read the note for a rule before loosening a guard or changing a number.** Where a claim is inference rather than measurement it says so, and those markers are load-bearing — see the comment conventions in `CLAUDE.md`.

## How this is split

The notes are in three files, on the same boundary the style itself uses — which block owns the rule:

| File | Covers |
| --- | --- |
| **this file** | The whole-file inline-style rule and the `:root` notes. These apply everywhere: Stylus concatenates the `:root` rule into every section, so both blocks see them. |
| `docs/rule-notes-feed.md` | The `domain()` block — the feed and anything else site-wide. |
| `docs/rule-notes-post.md` | The `regexp()` block — every post shape on `/p/`, `/<user>/p/` and `/<user>/reel/`. |

Within each file, sections are in the order the rules appear in the style. A heading of *(section header)* is a block comment that introduces a group of rules rather than a single one.

**Use the index below rather than reading a whole file.** The style carries no comments, so these notes are the only explanation that exists — a note that goes unread is the failure mode this index exists to prevent.

## Index

### The `domain()` block — `docs/rule-notes-feed.md`

- `article, main, [role="dialog"]`
- `main .xvs91rp, [role="dialog"] .xvs91rp`
- `article ._aacl._aaco._aacu._aacx._aad7._aade, article ._acan, article .x1f6kntn`
- `.x6bx242`
- `main > div:has(> div[style*="630px"]), main > div:has(> div[style*="max-width"])`
- `main > div > div[style*="630px"], main > div > div[style*="max-width"]`
- `main [style*="--x-width"][style*="470px"], .xmnaoh6 + div > div`
- `main div[style*="min(470px"]:not(li *):not(:has(ul))`
- `main div[style*="min(470px"]:not([style*="--x-width"]):has(ul)`
- `main > div > div > .xw7yly9 > div`
- `article:not([role="dialog"] *) > .xdt5ytf:has(> div:nth-child(3))`
- `> div:nth-last-child(3)`
- `> div:nth-last-child(2)`
- `> div:last-child`
- `article:has(a[href*="/reels/"]):not([role="dialog"] *) > .xdt5ytf`
- `article:has(a[href*="/reels/"]):not([role="dialog"] *) div[style*="padding-bottom"][style*="125%"]`
- `article:has(a[href*="/reels/"]):not([role="dialog"] *) a:has(div[style*="padding-bottom"][style*="125%"])`
- `article:has(a[href*="/reels/"]):not([role="dialog"] *) a:has(div[style*="padding-bottom"]:not([style*="125%"]))` (removed 2026-09-14)
- `article:has(a[href*="/reels/"]):not([role="dialog"] *) div[style*="padding-bottom"]:not([style*="125%"])` (and its `> div` and `video`)
- Media (section header)
- `article:not([role="dialog"] *) img[aria-hidden="true"]`
- `article:not([role="dialog"] *) a:has(div[style*="padding-bottom"])`

### The `regexp()` post and reel block — `docs/rule-notes-post.md`

- `@-moz-document regexp("https://www\\.instagram\\.com/(p|[^/]+/p|[^/]+/reel)/.*")`
- `:root:has(main div[style*="--x-maxWidth"] video)`
- `main div[style*="--x-maxWidth"]:has(> div > div > div video)`
- The reel stage's `min-height` (measured, NOT in the style)
- `main div[style*="padding-bottom"][style*="177"]` (removed 2026-09-12)
- The carousel and single-photo rules (same block)
- `main > div > div.xvc5jky:has(li[style*="translateX"])`
- `main > div > div.xvc5jky:not([style*="--x-maxWidth"]):has(li[style*="translateX"])`
- `main > div > div.xvc5jky:not([style*="--x-maxWidth"]):has(video)`
- `main div[style*="--x-maxWidth"]:has(li[style*="translateX"])`
- `main > div > div.xvc5jky:has(div[style*="padding-bottom"] > img):not(:has(li[style*="translateX"])):not(:has(video))`
- `main > div > div.xvc5jky:has(div[style*="padding-bottom"] > img):not(:has(li[style*="translateX"])):not(:has(video)):has(div[style*="padding-bottom:1"] > img, div[style*="padding-bottom: 1"] > img)`

---

## Inline-style matching (whole-file rule)

Inline styles: never match a whole value. Instagram writes the same declaration with and without a space after the colon (server-rendered markup vs a CSSOM re-render), and one ratio appears under several spellings (3:4 as 133.333%, 133.33333333333331%, 133.31719128329297%). Match a distinctive prefix, or split into two conditions.


## `:root`

Stylus turns each knob in the header into a custom property on :root and concatenates that rule into every section, so the reel-page block at the bottom sees them too. Only computed values live here. Every property this style declares is prefixed --u- so it cannot collide with one of Instagram's own tokens; the exceptions are deliberate overrides, marked as such where they appear.


## `--u-media-px` (declared on `:root`)

Width available to the media column, as a real length -- the carousel scale below is a unitless ratio, and CSS can only build one out of two lengths. The feed width has to be restated against the viewport because a percentage inside atan2() would not resolve, which is also why the 12px scrollbar allowance is a constant.

`100vw - 72px`, not `100vw`, since the nav-rail reservation below. The rail is fixed-positioned and takes no layout space, so nothing subtracts it automatically: the reservation takes it out of the feed's containing block by hand, and this restatement has to take it out by hand to match. Leave it at `100vw` and the estimate over-states the media column by up to 72px, scaling feed carousels larger than the space they have.


