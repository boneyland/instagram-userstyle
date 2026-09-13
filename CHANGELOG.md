# Changelog

## 2026.9.12.4

Compared against `2026.9.12.1`, which was published to userstyles.world earlier the same day and is kept as `Instagram-20260912.1-uploaded.user.css` -- so this entry is the whole of what an installer receives. `2026.9.12.2` and `2026.9.12.3` were unpublished working steps and are covered here rather than kept as entries of their own. The `2026.9.12.1` entry below remains the cumulative comparison against `20260910` for anyone updating from further back.

### Reels on the post and reel pages now respond to both settings, at every shape

Three separate defects, one arc of work, all of it reported from the live site and then measured against snapshots captured for it.

**Landscape reels took nothing at all.** Reels at `56.2696%`, `88.8614%`, `75%` and `69.4981%` responded to no setting except the text ones. Four snapshots were captured -- two on `/<user>/p/<id>/`, two on `/<user>/reel/<id>/` -- and the cause measured: a landscape reel's column carries **no inline `--x-maxWidth`**, and all three reel rules were keyed on that token, so none of them matched. They are now caught by `main > div > div.xvc5jky:not([style*="--x-maxWidth"]):has(video)`, which sets the width cap and the caption column together. Measured at the defaults, 1638px window, stock -> styled: 1598x712 -> 1150x452 with the video 1262x710 -> 769x433; 1598x1123 -> 1150x685; 1598x949 -> 1150x579; 1598x879 -> 1150x536. Caption 335 -> 380 on all four.

That measurement also produced the general rule the whole block now turns on, checked across all twenty-one snapshots: **Instagram writes the inline `--x-maxWidth` only when the media is taller than square.** 177.778% and 133.333% carry one; 100% and every landscape ratio carry none. So the block splits on the token rather than on media type, and the no-token rules cover square and landscape alike.

**The 9:16 reel had a hard-coded height.** `padding-bottom: 0; height: min(95vh, 950px)` replaced the ratio box with a fixed height, which nothing could adjust and which fought the width setting: because the video is `object-fit: contain`, the box drifted away from 9:16 at every setting and letterboxed. Measured before: at a 950px column the box was 569x855 holding a video visible at 481x855 -- an 88px dead band on each side -- and raising the width setting past that changed nothing but the size of the bands.

The rule is **removed**. Instead the column itself is bounded, so the `padding-bottom:177.778%` box keeps its own ratio for free:

```
--x-maxWidth: min(100%, var(--u-reel-width),
   calc(var(--u-reel-height) * 9 / 16 + var(--u-reel-media-info)))
```

Measured after, at a 1638x900 window, as column / box: 950/950 -> 914 / 533x948; 950/600 -> 718 / 337x598; 950/400 -> 605 / 224x398; 950/1400 -> 950 / 569x1012; 2000/400 -> 605 / 224x398. Every one reads h/w 1.778 exactly. Both settings bind, whichever is tighter, and the visible video at today's defaults is unchanged -- all that goes away is the dead space.

Two consequences to know. The `95vh` term is gone with the rule, so the height setting is authoritative and a reel can exceed the window: at 950 on a 900px-tall window the box is 948 tall and scrolls. And with both settings at 950 the height term binds first, so the effective default column is **914px**, not the 950 the width slider reads.

The `9/16` is written for 9:16 and is conservative for anything shallower -- the same trade the feed's `16/9/1.25` term makes. It replaces the style's only literal ratio match on a post page.

### The post and reel blocks became one

The reel URL was added to the post block, because **every post shape is reachable at `/<user>/reel/<id>/`, not only reels** -- reported live. That left the two `regexp()` conditions identical character for character, so they were merged. Three blocks become two. Nothing about the rules changed: they never overlapped by URL, only by selector, and `scoped.py --diff` measured 0 standard and 0 custom property changes across every snapshot, with the reel-permalink snapshot moving from 2 applicable blocks to 3.

### Removed

A **duplicate `--x-maxWidth` rule** on the reel column, left behind when the new bounded version was written above it — live code that did nothing and would have silently reverted the height cap if the block were ever reordered. See `docs/removed.md`.

### Settings

Fourteen become **fifteen**.

| | Setting |
| --- | --- |
| Added | `u-reel-height`, "Reel/post pages: maximum height of a 9:16 reel", default 950px. |
| Relabelled | Every setting. The labels were rewritten to name what they govern rather than describe it -- "Feed: maximum height of media" rather than "Feed: never let a photo or reel get taller than" -- and the post-page pair now reads "Reel/Post page:", since both reach the reel URL. |
| Default moved | `u-post-photo-width` and `u-post-width`, 1150px -> 1350px. |

`u-reel-height`'s label shipped for one working version as a copy of `u-reel-width`'s, which would have read as a duplicate slider in the settings pane. Corrected here.

### Verification

`verify.py` passes. `scoped.py --diff` across all twenty-one snapshots isolates each change to the pages it is meant to reach: the landscape-reel rule to the four landscape reels, and nothing at all on any feed, carousel, single photo, modal or `/reels/<id>/` page. Every change in this release was also checked on the live site.

### Not done: the reel stage's `min-height`

A dark band under a small reel was reported, and the snapshot explained it exactly — Instagram's own `min-height: 450px` on the reel stage. A one-property fix measured clean offline. **It is not in the style**: the live check found the band did not occur. Do not add it on the strength of an offline measurement; reproduce the band live first. Measurements in `docs/removed.md`.

## 2026.9.12.1

Compared against `20260910`, the version published before it -- so this entry is the whole of what an installer receives, not one step of it. Seven unpublished versions sit between the two, `2026.9.11.1` through `2026.9.11.7` and this one. Each keeps its own entry in `docs/changelog-archive.md`, with the measurements and the reasoning; this entry is their sum and the place to start.

### Settings

Thirteen settings become fourteen -- two added and one removed, net plus one. (2026.9.11.4 records the count as going from fifteen to fourteen; that was against the unpublished `2026.9.11.3`, which had briefly carried two more.) Saved values carry over, and no default moves except the one noted, so an existing install renders the same until a setting is touched.

| | Setting |
| --- | --- |
| Removed | `u-post-media-scale`, "Post page: enlarge a multi-photo post by". It did nothing -- Instagram re-derives a carousel slide's width from its container, so scaling the container up and the slides down cancelled exactly. See 2026.9.11.4. |
| Added | `u-feed-sidebar`, "Feed: the right-hand sidebar". It had been hidden unconditionally since before this changelog started. See 2026.9.11.2. |
| Added | `u-post-photo-width`, "Post page: total width of a square post or a tall single photo, and caption". See 2026.9.11.1 and 2026.9.11.3. |
| Relabelled | `u-media-max-height`, `u-post-width` and `u-reel-width` -- each now names the pages or the media it actually governs. |
| Range widened | `u-media-column` 90 to 100 and `u-carousel-scale-max` 3 to 6 (2026.9.11.4); `u-feed-reel-width` 1200 to 2000. |
| Default moved | `u-reel-media-info`, the caption column, 429px to 380px. |

### What an installer receives

**Feed.**

- The feed no longer runs underneath the left nav rail, which had made the like button under it unclickable. `Feed: width of the feed` is now a share of the window *beside* the rail. (2026.9.11.5)
- The right-hand sidebar can be brought back. (2026.9.11.2)
- Feed media rules no longer reach a post opened as a floating modal, where a feed setting had been capping the photo's height. (2026.9.11.1)
- `Feed: never let a photo or reel get taller than` limits reels, which its old label had always implied and which it had never done. (2026.9.11.1)
- A reel is no longer cropped left and right when `Feed: never let a reel get wider than` is set low. (2026.9.11.6)
- Both reel settings now reach a **landscape** reel, which had ignored them entirely. (2026.9.11.7)
- A reel whose box ratio ends in `125` is no longer misclassified as a flattened portrait one. (this version, below)
- `Text: spacing between lines` now reaches everything `Text: size` reaches. (2026.9.11.1)

**Post pages.**

- Single photos on `/p/<id>/` and `/<user>/p/<id>/` are sized consistently instead of coming out at wildly different widths depending on shape, and landscape ones keep Instagram's own layout while gaining the caption column. (2026.9.11.1)
- Square carousels are handled; they had reached no carousel rule at all. (2026.9.11.3)
- Reels reached through either `/p/` path are enlarged. This widened the middle `@-moz-document` condition from `[^/]+/reel/` to `(p|[^/]+/p|[^/]+/reel)/`. (2026.9.11.1)
- The post-page carousel `zoom` rule is gone, with its setting. (2026.9.11.4)

**Reel pages.**

- The comments panel on `/reels/<id>/` takes both text settings -- the known gap recorded in 20260910. (2026.9.11.1)

**Internal, with no rendering change.**

- Every comment outside the metadata block was stripped; `docs/rule-notes.md` is now the only record of why a rule is shaped as it is. (2026.9.11.1)
- `@description` no longer states the browser floor, which lives in `README.md` and `USw-notes.md`. (2026.9.11.2)
- `verify.py` resolves `select` defaults, and its snapshot lookup was repaired after the feed captures were renamed. (2026.9.11.2, 2026.9.11.7)
- Several wrong claims were removed from `docs/rule-notes.md`. (2026.9.11.4)

### This version's own change

- **A feed reel whose box ratio happens to end in `125` was treated as a portrait reel and cropped.** Found while answering a question about where Instagram's percentages come from; the bug is older than the landscape work and was inherited by it.

  **What was wrong.** Both 125% rules were keyed on `[style*="padding-bottom"][style*="125%"]`, and `[style*="125%"]` is a substring test over the WHOLE style attribute. `padding-bottom:68.125%` contains the substring `125%`. So a reel at that ratio matched the portrait selector, was capped by arithmetic derived from 1.25, and had `object-fit: cover` crop it to a shape it never had. The landscape rules added in 2026.9.11.7 use the negation of the same test, so such a reel was excluded from the rules that would have sized it correctly -- one misclassification, both halves wrong.

  **This is not hypothetical.** `68.125%` is an observed value: it is on a photo in `Instagram_feed2.html`. It is exactly `109/160`, so it is the kind of number Instagram's own arithmetic produces, and nothing about a reel prevents it. Confirmed against the real markup by setting that value on the landscape reel's box and asking Firefox which selectors matched: the portrait selector matched, the landscape selector did not.

  **What changed.** Every one of the six guards now anchors the match to the property name and the whole value, in both spellings inline styles occur in: `:is([style*="padding-bottom:125%"], [style*="padding-bottom: 125%"])`, and the negation as two chained `:not()`s. A trailing `%` terminates the match, so `padding-bottom:125.5%` no longer matches either. Verified after, on the landscape reel's box in `Instagram_feed2.html`: `68.125%`, `56.2696%`, `75%`, `100%` and `125.5%` all classify as landscape; `125%` and `125%` with the re-rendered space both classify as portrait.

  **Why matching the whole value is right here**, when the standing rule in `CLAUDE.md` is never to match a whole percentage. That rule exists because one ratio reaches the DOM under several spellings -- 3:4 arrives as `133.333%`, `133.33333333333331%` and `133.31719128329297%`. It does not apply to `125%`, which is not a computed ratio at all: it is the constant Instagram clamps anything taller than 4:5 to. Across all sixteen snapshots the only spellings of the round values are the bare `75%`, `100%` and `125%`, with every computed value carrying decimals. Exactness is what the split needs, and a prefix is what would break it.

### Verification

`verify.py` two-file mode reports the rewrite **computationally identical** to `2026.9.11.7` on the feed snapshot, at 142 declarations on both sides -- so Firefox parsed the `:is()` spelling rather than dropping it. `scoped.py --diff` reports **no snapshot renders differently**, all sixteen, standard and custom alike. Both are the expected result: no box in any snapshot is both a reel and a ratio ending in `125`, so this is a pure refactor there, and the defect it fixes is one no saved page happens to contain.
