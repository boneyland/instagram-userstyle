# Changelog

## 2026.9.17.1

Compared against `2026.9.14.1`, kept as `Instagram-20260914-uploaded.user.css`.

Instagram capped the post page at its 935px site width, which pinned every no-token shape there and left the width settings working downwards only; the one rule added here lifts that cap, and it is the only change that moves pixels. Two labels widen to name shapes the rules always covered but no snapshot holds -- a square reel and a 4:5 carousel, each confirmed on the live site rather than in a capture. No existing rule is changed, no setting is added or removed, and no saved value is affected.

### Instagram's 935px cap on the post column, and the rule that lifts it

**Reported from the live site on 2026-09-17: widening a 1:1 single photo and a 16:9 carousel did nothing.** Both reproduce offline against captures taken the same day.

The post column is two nested `.xvc5jky` divs -- an outer `main > div.xvc5jky` wrapper and the inner `main > div > div.xvc5jky` that every width rule in the post block caps. The outer wrapper now carries `x1ykew4q`, and Instagram's own sheet says `.x1ykew4q{max-width:var(--polaris-site-width-wide)}`, which is 935px, its long-standing desktop content width. A `max-width` can only shrink a box, so the style's own cap could still narrow the column below 935 but could never widen it past that. That is the whole of the symptom: the settings appeared to work below 935 and to do nothing above it.

Measured on the 1:1 single photo at a 1638px window, sweeping `--u-post-photo-width`, before -> after: 700 -> column 700 either way, media 319x319; 935 -> 935 either way, 554x554; 1200 -> **935/554x554** before, 1200/819x819 after; 1600 -> **935/554x554** before, 1598/1217x1217 after. The 16:9 carousel's column moves identically, 935/935/935/935 becoming 700/935/1200/1598, while its slide media reads 599x337 at every value -- that is the derived slide width SingleFile freezes at save time, not a failure, and a post-page carousel's media can only be measured live.

**This is a change on Instagram's side, not a regression here.** The class splits the corpus cleanly by capture date: every snapshot taken between 2026-09-09 and 2026-09-14 contains neither `x1ykew4q` nor a `.x1ykew4q` rule at all, and every snapshot taken on 2026-09-17 carries it. When this rule was first measured that was 2 captures against 20; the folder was then re-captured through the day, and as it stands it holds 19 snapshots of which 10 carry the class -- the same split, further along. On the older markup the wrapper was unconstrained -- the square-carousel capture renders its children at 1598 with no stylesheet applied -- so `max-width: none` restores the geometry the rest of the block was measured against rather than inventing a new one.

The new rule is `main > div.xvc5jky:has(> div.xvc5jky)`, in the `regexp()` post block. Keyed on the nesting rather than on `x1ykew4q`, because Instagram's atomic class names are hashes of the declaration and churn whenever the sheet is rebuilt. The `:has(> div.xvc5jky)` guard is what keeps it off the post modal: there the bare `main > div.xvc5jky` matches **1** -- the profile page's own wrapper, 1212px wide, behind the dialog -- while the guarded form matches **0**. No `!important`: Instagram's `.x1ykew4q` is (0,1,0) and this selector is (0,2,3), so specificity settles it on the element itself.

`verify.py` passes, with the declaration census going 141 -> 142 for the one new line and the feed computationally identical. `scoped.py --diff` reported **2 of 22 snapshots changed** -- the two new-markup captures -- and `std = 0` on the other twenty, the modal and every older post shape included. That run was against the corpus as it stood before the day's re-captures, so it is a record rather than a figure reproducible against the folder today. Three of the current snapshots were then diffed individually: the `/p/` modal at **0 standard and 0 custom**, which is the guard holding; the square single photo at **628 standard properties over 1059 elements**; and the 16:9 carousel at **522 over 1959**. Both of the latter move `width`/`inline-size`, `height`/`block-size`, the two origins, `padding-bottom` and a few margins and insets -- geometry only, which is what lifting a `max-width` does. No `font-size`, `line-height` or `zoom` appears in any of the three.

**Both of the things this rule could not be checked against offline were then checked live on 2026-09-17.** The 16:9 carousel's media, which no capture can measure for the frozen-slide-width reason above, moves with the setting on the live site. And the portrait shapes were caught by the same ceiling and are freed by this rule: they size through `--x-maxWidth` on the inner column, which the wrapper clamps exactly as it clamps a `max-width`, and every post-page shape in the coverage matrix was reported responding correctly with this rule in place. Both are confirmed by response rather than by measurement, and no portrait post has been captured since the markup changed, so nothing offline exercises that path.

### `u-reel-landscape` now says "square/landscape"

The label read **"Reel/post pages: total width of a landscape reel and caption"** and now reads **"Reel/post pages: total width of a square/landscape reel and caption"**.

The rule behind it is untouched. `main > div > div.xvc5jky:not([style*="--x-maxWidth"]):has(video)` caps the column of any reel whose column carries **no** inline `--x-maxWidth`, and per the boundary the post block turns on, that means square **or** landscape. It reads no ratio at all; the ratio only ever entered through the label, which named the shapes that had been measured -- four reels at `56.2696%`, `69.4981%`, `75%` and `88.8614%`, with no reel at `100%` anywhere in the census.

What changed is the measurement. On 2026-09-17 the user found a **square reel on the live site** and reported it responding to this setting, which retires an open question that had stood since the setting was introduced: a 1:1 reel was known by construction to take it, and the label was the honest name for every shape actually captured. It is still not captured, so nothing offline exercises the path.

**The variable is still named `u-reel-landscape`.** Stylus keys a saved value by the variable name, so renaming it would silently reset every installed user's value to the 1500px default. Only the label moved. `verify.py` in two-file mode confirms all sixteen variables parse and the two versions are computationally identical.

### `u-post-width` now says "portrait carousel"

The label read **"Reel/post pages: total width of a 3:4 carousel post and caption"** and now reads **"Reel/post pages: total width of a portrait carousel and caption"**.

The rule behind it is untouched. `main div[style*="--x-maxWidth"]:has(li[style*="translateX"])` caps the column of any carousel whose column carries Instagram's inline `--x-maxWidth`, and it reads no ratio at all -- the ratio only ever entered through the label, which named the one shape that had been measured.

What changed is the measurement. Both captured carousels on the token side are 3:4, so 3:4 was all the label could honestly claim. On 2026-09-14 the user checked a **4:5 carousel live on `/p/<id>/`, `/<user>/p/<id>/` and `/<user>/reel/<id>/`** and reported it responding to this setting. Only a column carrying the token can do that, so a 4:5 carousel sits on the portrait side alongside 3:4 and the old label under-claimed by one shape.

"Portrait" stops there rather than running to 9:16: **no 9:16 carousel has been found anywhere**, live or captured, so the name covers two confirmed ratios rather than a range checked end to end. The rule would size a taller one identically if Instagram ever served one, since it reads no ratio. `docs/open-questions.md` carries both that gap and the fact that the 4:5 case was confirmed by response rather than by numbers -- no snapshot of one exists, and the inline value Instagram writes for a 4:5 column was not read.

### Settings

Still sixteen.

| | |
| --- | --- |
| Relabelled | `u-reel-landscape` -- "total width of a landscape reel and caption" -> "total width of a square/landscape reel and caption". |
| Relabelled | `u-post-width` -- "total width of a 3:4 carousel post and caption" -> "total width of a portrait carousel and caption". |

## 2026.9.14.1

Compared against `2026.9.12.4`, kept as `Instagram-20260912.4-uploaded.user.css` -- so this entry is the whole of what an installer receives.

A release about **labels that claimed more than they governed**, and the one setting that genuinely governed too much. Three labels were reported as misleading, each in the same way: the label named a category and the rule behind it covered a subset. In two cases the label was narrowed to the rule; in the third the rule was split so a label could be true of each half. No shape lost its sizing, and one gained a setting of its own.

### A setting that drove six shapes now drives four

`u-post-photo-width` -- "total width of photo/video and caption" -- reached three separate rules. A census across all twenty-one snapshots measured exactly what it moved: 1:1 (`100%`) and 4:3 (`74.9712%`) carousels, 1:1 (`100%`) and 3:4 (`133.333%`) single photos, and four landscape reels (`56.2696%`, `69.4981%`, `75%`, `88.8614%`). So a user tuning a photo could not leave reels alone, which is what was reported.

The landscape-reel rule, `main > div > div.xvc5jky:not([style*="--x-maxWidth"]):has(video)`, now reads a **new setting of its own**, `u-reel-landscape`, "Reel/post pages: total width of a landscape reel and caption". `u-post-photo-width` keeps the carousel and single-photo rules and is relabelled "total width of photo/carousel and caption" -- the "video" half of its old label having left it.

**The split itself renders nothing differently.** Measured against a baseline identical but for the split, with both settings at the old shared 1350: `verify.py` reports 0 standard-property differences across 2810 elements, and `scoped.py --diff` reports `std = 0` on **all twenty-one snapshots** at their own URLs, the four landscape reels included. The only property that moves anywhere is the new token being declared and inherited, and the declaration census goes 140 -> 141, which is the single `:root` line Stylus builds from the new setting. The default was then set to **1500**, so landscape reels do start wider than before; that is a chosen default, not a consequence of the split.

**One overlap changed character and is worth knowing.** A mixed carousel -- photo plus video slides -- whose column carries no token matches both the slide-list cap and the `:has(video)` cap. While both read `u-post-photo-width` they set the same value and it did not matter; they now set different ones, so precedence decides. Measured in Firefox on a synthetic mixed carousel with the carousel rule first in source order: the element matched both and computed the **carousel** rule's value, so the specificity settles it, (0,3,4) against (0,2,4), and source order is never consulted. A mixed carousel therefore takes the carousel setting, which is the wanted outcome. It stays covered by construction only -- the overlap matches 0 on every snapshot, and none has been captured on a `/p/` URL.

### Three labels narrowed to what they actually govern

**"Feed: maximum height of media" is now "Feed: maximum height of a single photo or reel".** It never reached carousels: the feed photo rules exclude them with `:not(li *)` and the feed reel rules with the `a[href*="/reels/"]` guard. That exclusion is deliberate and load-bearing -- a carousel's slides sit in an absolutely positioned overlay on an empty aspect-ratio spacer, so collapsing anything in that chain makes them vanish -- and feed carousels have their own lever in the carousel scale setting. Label only; nothing renders differently.

**"Feed: maximum width of reel" is now "Feed: maximum width of portrait reel"**, and the rule was narrowed to match rather than the label widened. It fed both reel families: the two rules on the flattened `125%` box, and one on every other box. The landscape rule is **removed**, so the setting now reaches only the `125%` portrait boxes its label names. See `docs/removed.md`.

This is the one change in the release that moves pixels. A landscape feed reel is not left unbounded -- the other two rules stay, so it still collapses its padding box and sizes the video from its own intrinsic dimensions under `max-width: 100%` and the height setting -- but it no longer takes a dedicated width cap and instead fills the media column. Measured on `Instagram_feed2.html` at a 1638px window: the anchor's `max-width` 550px -> none, width 550 -> 687.017, auto margins 68.5 -> 0. Thirty-eight standard properties move, across that anchor and six descendants it was constraining; no `font-size`, `line-height` or `zoom` is among them. `scoped.py --diff` reports **1 of 21 snapshots changed**, the only one holding a landscape reel, with every post shape and the modal byte-identical.

**The post-page pair now says "portrait reel" rather than "9:16 reel"**, which is the honest reach: those rules are keyed on the inline `--x-maxWidth` token, which Instagram writes whenever the media is taller than square, not only at 9:16. The `9 / 16` in the height arithmetic is unchanged and still exact only at that ratio, sizing anything shallower conservatively -- `docs/open-questions.md` carries that one.

### Settings

Fifteen become **sixteen**.

| | |
| --- | --- |
| Added | `u-reel-landscape`, "Reel/post pages: total width of a landscape reel and caption", default 1500px. |
| Relabelled | `u-media-max-height`, `u-feed-reel-width`, `u-post-photo-width`, `u-reel-width` and `u-reel-height` -- each narrowed to the shapes it governs. |
| Prefix | The five post-page labels read "Reel/post pages:" throughout; two of them said "Reel/Post page:". The plural is the accurate form -- the block covers `/p/`, `/<user>/p/` and `/<user>/reel/`. |
| Default | `u-feed-width` 80 -> **90**. |
| Control | `u-carousel-scale-max` is a `range` rather than a `number`, so it draws as a slider like every other numeric setting. Its default, bounds and step are unchanged. |

Saved values carry over: every rename keeps its variable name, and only the labels moved.

### Removed

The landscape feed reel's width cap, recorded in `docs/removed.md` with its measurements and the note that it should come back with a setting of its own rather than by re-attaching `u-feed-reel-width`.

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
