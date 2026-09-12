# Changelog

## 2026.9.12.4

Compared against `2026.9.12.1`, which was published to userstyles.world earlier the same day and is kept as `Instagram-20260912-uploaded.user.css` -- so this entry is the whole of what an installer receives. `2026.9.12.2` and `2026.9.12.3` were unpublished working steps and are covered here rather than kept as entries of their own. The `2026.9.12.1` entry below remains the cumulative comparison against `20260910` for anyone updating from further back.

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

A **duplicate `--x-maxWidth` rule** on the reel column, left behind when the new bounded version was written above it. Same selector, same specificity, both `!important`, so it lost only by coming first -- live code that did nothing and would have silently reverted the height cap if the block were ever reordered. `scoped.py --diff` confirms deleting it changes nothing on any snapshot.

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

A dark band under a small reel was reported with a screenshot, and the snapshot explained it exactly: the stage that holds the video carries Instagram's own `min-height: 450px` and centres the video in it, so a media box shorter than that leaves a band above and below. Measured at `u-reel-height: 400`: stage 225x450 against a 224x398 box, 26px each side. A one-property fix, `main > div > div.xvc5jky > div > div:has(video) { min-height: 0 !important }`, closed it to 0 on the snapshot and measured inert everywhere else.

**It is not in the style.** The live check found the band did not occur, so the rule would have been machinery against a snapshot artefact. Recorded here because the snapshot measurement is reproducible and convincing on its own -- anyone re-deriving it offline will reach the same rule -- and because the discrepancy is unexplained: the floor is real in the saved CSS and something live evidently overrides or avoids it. Do not add the rule on the strength of an offline measurement; reproduce the band on the live site first.

## 2026.9.12.1

Compared against `20260910`, the version currently published to userstyles.world -- so this entry is the whole of what an installer receives, not one step of it. Seven unpublished versions sit between the two, `2026.9.11.1` through `2026.9.11.7` and this one. Each keeps its own entry below, with the measurements and the reasoning; this entry is their sum and the place to start.

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

## 2026.9.11.7

Compared against `2026.9.11.6`, the entry below. None of these has been published, so an installer coming from `20260910` receives all seven.

### Fixed

- **"Feed: never let a reel get wider than" and "Feed: never let a photo or reel get taller than" now reach a landscape reel.** Reported from the live site. Neither setting had any effect on one: both feed reel rules were keyed on the literal `125%`, and a landscape reel's box carries its own ratio instead.

  **What was measured.** `Instagram_feed2.html`, captured 2026-09-11, is the first snapshot here to contain a landscape reel -- article 4, `padding-bottom:56.4263%`, a 16:9. At a 1638px window with everything default it rendered **687x387.7**: the full media column, against a width setting of 550. The 125% rules matched nothing on it, so the only thing reaching it was the two-column layout rule, which is keyed on the article rather than on the box.

  **The width setting.** One new rule caps the anchor -- the containing block the percentage resolves against, so the box shortens with it rather than being narrowed without being shortened. The arithmetic is simpler than in the 125% case and deliberately so: a 125% box may hold a source taller than 125%, so its width and height need separate terms, but a non-125% box carries the source's TRUE ratio, so capping the anchor at the setting gives a box exactly that wide by that times the ratio tall, with nothing for `object-fit: cover` to crop. Measured after: 550 gives 550x310.3, 400 gives 400x225.7, 300 gives 300x169.3, every one at ratio 0.5642 against the source's 0.5643. Both 125% reels in the same snapshot are unchanged at every setting swept.

  **The height setting needed a different mechanism, and this is the part to read before touching it.** A percentage-padding box's height is `ratio x containing block width`, and CSS cannot read that ratio -- it exists only as a substring of an inline style. For 125% the ratio is a constant and the cap is `H / 1.25`; for a landscape reel there is no divisor to write down. Confirmed that the obvious alternative does not exist: `max-height` on the box is inert with and without `box-sizing: border-box`, measured at 200px on the 56.4263% box, rendered height 387.7px both ways, because a border box cannot shrink below its own padding.

  So three rules stop using the padding box as the ratio carrier and use the video's own intrinsic size instead -- the same mechanism the feed photo rules already use for `img`. The box gets `padding-bottom: 0`, `height: auto` and `width: fit-content`; its one direct child, an `inset: 0` overlay, is made static so the box has something in flow to take its height from; the video gets `width: auto`, `height: auto`, `max-width: 100%` and `max-height` from the setting. With both dimensions auto the replaced-element min/max algorithm satisfies both caps and preserves the ratio by itself, so the style contains no arithmetic and the result is exact for any ratio rather than for an enumerated set of them.

  `width: fit-content` is load-bearing, not cosmetic. When the height cap binds the video is narrower than the column, and without it the box stays column-width with the video centred inside, leaving Instagram's own overlays -- the progress bar, the mute button -- positioned against the box's edges rather than the video's. Measured at 1200/300 on a 16:9 source: without it, box 687x300, video 532.9x300, mute button 38px clear of the video's right edge; with it, box 532.9x300 and both overlays exactly on the video.

  **Measured.** Article 4, 1638px window, box/video: 16:9 at 550/900 gives 550x309.6; at 550/200 gives 355.3x200; at 1200/300 gives 532.9x300; at 300/900 gives 300x168.9. A 1:1 source at 1200/300 gives 300x300, a 4:3 source 400x300. Every one holds its ratio to four decimals, and the 125% reels never move.

### Verification

`verify.py` passes all four checks at 42 rules and 142 declarations, against 39 and 125 before -- exactly the four new rules and their seventeen longhands, so Firefox dropped nothing.

  `scoped.py --diff` against `2026.9.11.6` reports **one of sixteen** snapshots changed, `Instagram_feed2.html`. `Instagram_feed1.html` holds only a 125% reel and is untouched, as are all fourteen post and modal pages -- which is the part of that run worth having, because it is what proves the four rules reach nothing they were not aimed at. The changed properties are exactly the ones these rules set (`max-width`, the two margin longhands, `padding-bottom`, `position`, `max-height`, `object-fit`) plus the heights they cascade into, and there is no `font-size`, `line-height` or `zoom` anywhere in the list.

  **What that run does NOT show is the rule working**, and the numbers make it look worse than it is. The saved page has no poster and no video source, so the landscape reel falls back to 300x150 and the feed shortens by 286.6px. That is the snapshot, not the rule -- see `Not proven` below.

`verify.py` also had to be repaired to run at all: `find_snapshot()` still looked for `Instagram (*).html`, which stopped existing when the feed captures were renamed to `Instagram_feed<n>.html`, so its three browser checks had been failing outright. It now takes the newest `Instagram_feed*.html`, which is also what puts the landscape reel in front of it.

### Confirmed live

**The height rule could not be tested offline at all, and was checked on the live site instead.** SingleFile strips video sources and replaces the poster with `data:,`, so `videoWidth` is 0 on every snapshot here and a rule keyed on intrinsic size has nothing to read: applied to `Instagram_feed2.html` as saved, the landscape reel renders 300x150, the CSS default object size for a replaced element with no intrinsic dimensions. The figures above come from the same snapshot with a synthetic poster of known pixel size patched onto every `<video>`, since a `<video>` takes its intrinsic dimensions from its poster frame when no video data has loaded. That exercises the real markup and the real cascade against a ratio we control, which proves the mechanism and nothing further.

Two things only the live site could settle: whether Instagram's poster and video agree with the `padding-bottom` it writes alongside them, and whether the poster arrives early enough that the reel is never briefly drawn at the 300x150 fallback while the feed scrolls. **Checked on the live feed on 2026-09-11: a 4:3 reel at `padding-bottom: 75%` and a 16:9 reel at `padding-bottom: 56.25%` both render correctly, and no 300x150 appeared.** Two distinct landscape ratios, neither of them the 56.4263% the snapshot holds -- 56.25% is the round 16:9 -- so this is confirmation against ratios the rule was never tuned to. A live reel shallower than 4:3, or between these two, is still unchecked; nothing in the rule distinguishes them, since it reads no ratio and does no arithmetic.

## 2026.9.11.6

Compared against `2026.9.11.5`, the entry below. None of these has been published, so an installer coming from `20260910` receives all six.

### Fixed

- **A feed reel is no longer cropped left and right when "Feed: never let a reel get wider than" is set low.** Reported from the live site. The setting narrowed the box without shortening it, and past a point the box became narrower in ratio than the reel inside it, so `object-fit: cover` started cutting the sides instead of the top and bottom.

  **Why.** The box's height is `padding-bottom: 125%`, which resolves against the CONTAINING BLOCK's width -- the anchor -- not against the box's own. So the box is `min(setting, anchor)` wide and `1.25 x anchor` tall, and only the width followed the setting down. Measured on the saved feed at a 1638px window with everything else default: 550 gave 550x858.8, a ratio of 0.6405; 470 gave 470x858.8, 0.5473; 400 gave 400x858.8, 0.4658; 300 gave 300x858.8, 0.3493. A 9:16 reel needs 0.5625, so everything from about 483px down was losing its sides.

  **What changed.** One declaration. The anchor's `max-width` is now a `min()` of the height cap it already carried and a second term, `calc(var(--u-feed-reel-width) * 16 / 9 / 1.25)`. Shortening the anchor shortens the box, so the box's ratio cannot fall below 16:9 inverted: where the anchor is already narrower than the setting the box is a true 125% and the term is slack, and where it is wider the box is `setting` wide and the term holds its height at or under `setting x 16/9`. The two constants are left unreduced because they are two separate facts -- 16/9 is the tallest source a 125% box can hold, 1.25 is the box's own padding.

  **The effect on the settings.** Nothing moves at or above the default. At 550 on a 1638px window the new term is 782px against the old cap's 720px and the column's 687px, so the column still binds and the box renders 550x858.8 exactly as before. Below the knee the anchor now shortens with the setting: 470, 400 and 300 give 470x835.5, 400x711.1 and 300x533.3, all exactly 0.5625, where a 9:16 reel is not cropped on either axis. "Feed: never let a photo or reel get taller than" is unaffected and still composes -- measured with both moved at once, 550/400 gives 320x400, 300/400 gives 300x400, 1200/300 gives 240x300, 300/2000 gives 300x533.3.

  **The floor is 9:16, not 4:5, and that is a choice rather than a measurement.** Instagram flattens anything taller than 4:5 into the same 125% box, so a genuine 4:5 reel cannot be told from a 9:16 one here and no box is safe for both: one taller than 4:5 reveals more of a 9:16 and crops the sides off a true 4:5. Only a true 125% box is safe for everything, and it would cost the "less-cropped portrait reels" the style's description leads with. Put to the user with both trade-offs on 2026-09-11 and declined, so a genuinely 4:5 reel is still side-cropped whenever the box is taller than 4:5 -- unchanged from what the default already did. The floor is exact only while 9:16 is the tallest reel Instagram accepts, which comes from its upload limits and from every reel snapshot here being 177.778%, not from a capture of a taller one.

  **Verification.** `verify.py` passes all four checks with the declaration count unchanged at 122, so Firefox kept the nested `min(calc(), calc())` rather than dropping it. `scoped.py --diff` against `2026.9.11.5` reports **zero** properties moving on all fifteen snapshots, standard and custom alike -- which is the result to expect and not a sign the change did nothing: it runs every snapshot at the default settings, where the new term is slack by design. The change only renders below the knee, and both scripts are blind to that because neither varies a setting. What measured it was a one-off probe in the same headless Firefox: the saved feed, the style applied, `--u-feed-reel-width` forced to each value in turn and the box's rendered box read back. The before and after figures above are that probe's output.

  **Not done: 4:3 reels.** A 4:3 reel keeps Instagram's own 75% box, which no rule here touches, so it was never at risk of this and is not covered by the floor either.

## 2026.9.11.5

Compared against `2026.9.11.4`, the entry below. Neither has been published, so an installer coming from `20260910` receives both, along with `.1` to `.3`.

### Fixed

- **The feed no longer runs underneath the left nav rail.** Reported against "Feed: width of the feed" and "Feed: width of the photo" both at 100, where the feed filled the window, the rail covered the left edge of every post, and the like button could not be clicked at all: the rail expands on hover, so the pointer widened it before arriving. 72px is now reserved on the left of the feed area.

  **Why nothing reserved it already.** The rail is a fixed-positioned sibling of the whole content wrapper -- `position:fixed; top:0; height:100vh; width:fit-content; z-index:10` in the saved feed's own CSS -- so it takes no layout space and `main` starts at x=0. Instagram's own feed column is 630px and centred, so it never reaches the left 72px and the collision never shows on a stock page. Every width this style offers is measured from the same x=0, so the wider the feed, the further under the rail it goes.

  **What changed.** One new rule, on the feed column's parent: `box-sizing: border-box`, `padding-left: 72px`, `justify-content: safe center`. Its selector is the existing feed-width rule's selector lifted one level, so the reach is identical -- 1 match on the saved feed, 0 on all thirteen other snapshots. `--u-media-px` restates the feed width as `100vw - 72px` to match.

  **The effect on the settings.** "Feed: width of the feed" is now a percentage of the window minus the rail rather than of the whole window, and Instagram's own centring then centres the feed in that free area. At the default 80 on a 1638px window the feed column moves from x=164 w=1310 to x=229 w=1253 -- 57px narrower, sitting in the middle of the space the rail leaves. At 100 it runs x=72 to 1638 instead of x=0 to 1638. Existing installs see this without touching a setting.

  **Two details that had to be measured rather than assumed.** The parent carries Instagram's `xh8yej3`, which is `width: 100%`, so under the default `content-box` the padding is added to the 100% rather than taken out of it: the first attempt made the parent 1710px wide in a 1638px window and pushed the feed off the right edge instead of clear of the rail. `box-sizing: border-box` is what makes the reservation a reservation. And `justify-content: safe center` handles the case padding cannot: when "Feed: never let the feed get narrower than" exceeds the free width the column overflows, and a centred flex item overflows in both directions -- at a 900px window with that setting at its 1600px maximum the column's left edge landed at x=-350, further under the rail than before. `safe` makes an overflowing item flush-start instead, giving x=72.

  **Verification.** `verify.py` passes all four checks, and the parse census goes from 119 declarations to 122 -- the three this rule adds, so Firefox kept `safe center` rather than dropping it. `scoped.py --diff` against the previous file reports the feed snapshot moving 1469 standard properties and all thirteen other snapshots moving **zero**, custom-only, the single `--u-media-px` token set and inherited and never read there.

  **The feed's own diff includes `font-size` (81 elements) and `line-height` (79), which `scoped.py` flags as the signature of a container holding text being resized by mistake. Here it is not.** Those elements are exactly the 81 that also show `--u-carousel-scale` changing: they are the zoomed carousel subtree, and `zoom` scales every length inside it. The scale moved because the media column really is narrower now, and it moved by the right amount. At a 1638px window and the defaults, the column was 1310 x 0.55 - 12 = 708.5px, giving a ratio of 1.514 clamped to the 1.5 ceiling and media 702px wide. It is now 1252.8 x 0.55 - 12 = 677px, a ratio of 1.447 that no longer reaches the ceiling, and media 677px -- measured at 702 and 677 respectively, and 677 fits the 689px the column now leaves.

  **Not done: the post and reel pages.** They centre in the window and only reach the rail when their width setting exceeds the window minus 144px -- `--u-post-photo-width` at 2000 on a 1600px window, say. That is a different rule on different containers and no measurement of it exists, so nothing was written for it. The feed's reservation cannot help there: its selector matches 0 elements on all thirteen post, reel and modal snapshots, which is deliberate.

  **RTL is not handled.** `padding-left` is a deliberate no-claim; which side the rail takes under `dir="rtl"` was not checked, and no snapshot of it exists.

## 2026.9.11.4

Compared against `2026.9.11.3`, the entry below. None of these has been published, so an installer coming from `20260910` receives all four.

### Removed

- **The post-page carousel `zoom` rule and its setting, "Post page: enlarge a multi-photo post by" (`u-post-media-scale`, default 1.5).** Both are gone. The rule did nothing visible, and this was measured live on 2026-09-11 on a 3:4 carousel, on both `/p/<id>/` and `/<user>/p/<id>/`: moving the setting anywhere between 1 and 2 produces a brief flash and the media then settles at exactly the size it already was. Carousel sliding was unaffected throughout.

  **Why it never worked, and why the snapshots said otherwise.** Each carousel slide frame carries an inline literal `width:<n>px` that Instagram's JS derives from the container, with the slide offsets written as multiples of it. `zoom: 1.5` makes the container report 513 CSS px where it reported 770; Instagram fills 513; zoom scales the result back to 770 — the same rendered size as `zoom: 1`. The flash is the interval between the zoom applying to the old width and Instagram re-deriving the new one.

  SingleFile freezes that inline width, so on a saved page the slide cannot re-derive and `zoom` appears to enlarge it. **Every measurement that made this rule look effective came from that freeze** — the "673x898 media at the default scale", the claim that the column must hold `caption + natural media width x scale`, and the coupling between this setting and `--u-post-width`. `docs/rule-notes.md` now marks them as artifacts rather than repeating them.

  The same re-derivation is what makes the square-carousel cap added in `2026.9.11.3` correct with no zoom at all, and it was that change's live check which raised the question about this one.

  **What actually sizes a 3:4 carousel is unchanged**: `--u-post-width` caps the column, the caption column takes `--u-reel-media-info`, and Instagram fills the difference — measured at 785 -> 356, 950 -> 521, 1200 -> 771. Removing the zoom therefore changes nothing a user sees on a live page, beyond ending the flash and letting Instagram lay the media out at 770 CSS px one-to-one instead of at 513 upscaled.

  **Both verification scripts disagree with this on the saved pages, and are expected to.** `scoped.py --diff` reports the two 3:4 carousel snapshots moving 329 standard properties each, because their frozen 449px slides lose the 1.5 and render at 449 instead of 674; the square carousel is untouched at 0, and the remaining eleven snapshots show custom-only drift — 1668 to 16534 elements each losing the `--u-post-media-scale` declaration, with zero standard properties behind it. `verify.py`'s two-file mode fails for a second and separate reason: it flattens every `@-moz-document` block unconditionally, so the removed rule was reaching the feed snapshot, where `rule-notes.md` already recorded it matching a 470x3644 region. That accounts for its 2357 standard-property mismatches, all on the feed, a page the rule never touched in the shipped style. Neither result is a regression; they are the freeze and the flattening. The live behaviour is the measurement that counts here.

  A `zoom` rule must not be reintroduced on either carousel shape without a live measurement first.

  **The feed's `zoom` rule was checked on the same day and KEPT.** `--u-carousel-scale-max` does resize feed carousels, tapering off above roughly 1.6 because the scale is `min(setting, fit ratio)` and past that point the ratio is the smaller term -- the clamp working as designed, the setting being a ceiling. The difference is that the feed rule zooms the carousel wrapper without stretching it (the widening rule beside it is guarded `:not(:has(ul))`), so the container still measures 468px and Instagram still derives 468px slides. Resize the container as well, as the post-page rule did, and the re-derivation cancels the zoom. That is the test to apply to any future zoom.

### Changed

- **Two feed setting ranges were widened. No default moved, so an existing install sees nothing change until a setting is touched.**

  **"Feed: width of the photo, as a % of the post"** (`u-media-column`) now reaches **100** rather than 90, so it can be taken to the full width of the feed when "Feed: width of the feed" is also at 100. Nothing new happens at 100: the caption already wrapped below the media at 90, because `--u-caption-min` (320px default) cannot fit in the remaining tenth, so this extends an existing single-column layout rather than introducing one. Measured on the saved feed at a 1729px viewport: at 55 the media is 761px with the caption beside it, at 90 it is 1245px with the caption wrapped below, at 100 it is 1383px with the caption wrapped below.

  **"Feed: never enlarge a multi-photo post by more than"** (`u-carousel-scale-max`) now reaches **6** rather than 3. The first change is what forced this one: the scale applied is `min(setting, fit ratio)`, and with `u-media-column` at 100 and `u-feed-width` at 100 the fit ratio is **3.67 at a 1729px viewport** and **5.44 at 2560px** — so the old ceiling of 3 began binding on an ordinary window, capping carousels below the width the feed had been widened to hold. 6 covers roughly a 2820px viewport at those maxima; 3840px reaches about 8.2 and is still capped.

- **A wrong claim was removed from `docs/rule-notes.md`: that the ceiling protects against upscaling.** It was justified there as guarding a "468px-wide slide source". 468px is the layout box the feed gives a slide, not the resolution of the image in it. A feed carousel slide inspected live in DevTools on 2026-09-11 held a **3277×4096** image in that 468px box, so a zoom well past 3 upscales nothing. The note now says what the ceiling is really for, which is user preference. The saved feed could not have answered this: SingleFile rewrites every srcset into a data URI and headless Firefox decodes none of them, so every `naturalWidth` reads 0.

- **The explanation of why the feed's `zoom` works and the post page's did not was corrected.** It had been recorded, marked as inference, as "the feed rule leaves the container's layout width alone, so Instagram still derives 468px slides". The conclusion was right and the mechanism was wrong: **nothing is derived on the feed at all.** Live DevTools shows the div inside each feed `li` carrying `width: calc(-2px + min(470px, 100vw))` — a static CSS expression referencing nothing the style touches — while the same div on a post page carries a literal `width:1262px` that Instagram's JS computed from the container. That is the whole difference, and it is now the test to apply before adding any zoom: read how the slide's width is written first.

- **`docs/rule-notes.md` no longer claims the two post-page carousel settings are coupled.** They never were; the coupling was inferred from the frozen snapshot. The note for the surviving column rule now states plainly that Instagram fills the media area the column leaves, and the note for the square-carousel cap points at it as the shared pattern rather than treating itself as the exception.

- **`README.md` and `USw-notes.md` drop the removed setting**, taking the count from fifteen to fourteen.

## 2026.9.11.3

Compared against `2026.9.11.2`, the entry below. Neither had been published, so an installer coming from `20260910` receives this with the rest.

### Added

- **Square carousels on a post page are handled.** A snapshot of one was captured on 2026-09-11, and it turned out the style reached the page with nothing but the two text rules from the `domain()` block -- the caption column width, the column cap and the media scale all missed it.

  The reason is the one already documented for single photos, and it applies to carousels identically: Instagram gives a 3:4 post the class `.xf68679` and an inline `--x-maxWidth:min(100%,785px)` on its column, and gives a square post **neither**. Every carousel rule in the post block was guarded on `--x-maxWidth`, so a square carousel matched none of them. Measured: `main div[style*="--x-maxWidth"]` counts **0** on the square carousel snapshot and 1 on each 3:4 one.

  So a square carousel is now capped the way a square single photo is -- `max-width` on the column, reading **`--u-post-photo-width`**, deliberately the same setting the square single photo uses so the two land on the same width. At the defaults, 1638px window: column 1598 -> 1150, caption 335 -> 380, media area 1263 -> 770, which is where the square single photo lands from the same settings.

  The guard is `:not([style*="--x-maxWidth"])` on the element **itself**, not `:not(:has(...))`. The token is an inline style on `.xvc5jky` directly, so the `:has()` spelling matches nothing and would have capped the 3:4 carousels too, putting `--u-post-photo-width` in a fight with `--u-post-width`.

### Changed

- **The carousel caption-column override moved from `:root` to the column container.** It was `:root:has(main div[style*="--x-maxWidth"] li[style*="translateX"]) { --media-info: ... !important }` and is now `main > div > div.xvc5jky:has(li[style*="translateX"]) { --media-info: ... }` -- the form `CLAUDE.md` asks for, and no longer `!important`.

  The `!important` is genuinely unnecessary rather than merely dropped. Instagram declares `--media-info` on `:root`, and `._aa4c`, its other declaring element, is not on the path between this container and `.x4h1yfo` (`width: var(--media-info)`) -- checked on all three carousel snapshots. A declaration on the container therefore beats the inherited one outright: importance only breaks ties within one element's cascade, and nothing else declares the token on that element.

  This is what lets the setting reach a square carousel, whose column has no `--x-maxWidth` for the old guard to find. It also removes a latent hazard: the old `:root` guard **also matched the saved feed**, where `main div[style*="--x-maxWidth"]` is present. Nothing reads `--media-info` there so it never rendered, but it was kept harmless only by the URL scoping -- the same shape of trap the reel block's `:root` rule still carries.

  `scoped.py --diff` over all fourteen snapshots: the two 3:4 carousels move **712 and 735 custom properties and zero standard ones** -- the token relocating with nothing rendering differently -- the square carousel moves 2711 standard properties, and the other **eleven snapshots do not change at all**, the modal and all four single photos included. No `font-size`, `line-height` or `zoom` among the moved properties.

### Not done

- **No zoom rule for the square carousel**, though one was asked for — and, as it turns out, none is needed.

  `zoom` is the only lever that resizes a carousel slide, which is why the 3:4 rule uses one: each slide frame carries an inline literal `width:<n>px` with the slide offsets written as multiples of it, and `zoom` scales both by the same factor so alignment survives. The setting that exists could not have supplied a usable value here anyway — `--u-post-media-scale` has a **minimum of 1**, so it can only enlarge, and a square carousel's slide already arrives at the full content width. Measured on the snapshot: the 1.5 default takes the slide from 1262 to 1893 inside a 770px viewport, strictly worse than leaving it alone.

  **Confirmed live on 2026-09-11**, which settled the question the snapshot could not: Instagram **re-derives** the slide width and the offsets from the container. With the style applied, the slides resize correctly at every value of `--u-post-photo-width` and each lands accurately in its frame — the same behaviour unstyled Instagram shows when the viewport is resized. Capping the container is therefore the entire job, and a zoom would only fight it.

  A `container-type: inline-size` + `tan(atan2())` derived-zoom version was built and measured before that check, and is deliberately not in the style: it hit a zoom/`cqw` feedback loop, computing 0.63 where 0.61 was wanted, and it reconstructed the very number SingleFile freezes, so no offline test could have validated it. Recorded so it is not attempted again.

  Related artifact, recorded so it is not mistaken for a bug: on the **saved** square-carousel page the cap narrows the container while the frozen slide stays 1262, so any measurement taken there reports the slide overflowing its 770px viewport by 493px. That is a property of the capture, not of the live page.


## 2026.9.11.2

Compared against `2026.9.11.1`, the entry below. Neither has been published, so an installer coming from `20260910` receives both.

### Added

- **The right-hand sidebar is a setting now rather than unconditional.** It had been hidden outright since before this changelog starts. The rule is unchanged in shape — one declaration on `.x6bx242` — but the value comes from a setting, **"Feed: the right-hand sidebar (your profile, the account switcher, suggestions)"**, defaulting to **Hidden**. An existing install therefore sees nothing change until the setting is moved.

  **The setting is a select, not a checkbox, and the two options are the two `display` values themselves — `none` and `block`.** A Stylus checkbox's value is `1` or `0`, and no CSS property takes a number for "hidden", so driving the rule from a checkbox would have meant `/*[[...]]*/` preprocessor substitution — a mechanism nothing else in this style uses, and one that leaves the raw file unparseable at that spot, which both `verify.py` and `scoped.py` read directly.

  **`block` is measured, not assumed.** `.x6bx242` is one of Instagram's atomic classes and carries exactly one declaration, `width: var(--feed-sidebar-width)`. The element wearing it is `<div class="x1dr59a3 x13vifvy x7vhb2i x6bx242">`, whose other three classes are `height:100vh`, `top:0` and `padding-inline-start:64px` — no `display` among them. With no stylesheet applied the element computes `display: block`. Headless Firefox at 1638×900, one match, 230 descendants: stock `block`, Hidden `none`, Shown `block`.

  The class is feed-only: two occurrences in the saved feed — Instagram's own CSS, and that element — and zero in the twelve other snapshots. It stays in the `domain()` block unscoped, and needs no `[role="dialog"]` guard because it is not keyed on `article`.

  At the default the change is inert. `verify.py` against the previous file reports **zero** standard-property differences across all 1668 elements; the only drift is `--u-feed-sidebar` itself, which is set on `:root`, inherited everywhere and read by one element. Flipped to Shown it moves 2913 standard properties — the rail and the reflow around it. The two harness failures that accompany a run like this are structural to adding any variable at all: one extra declaration in the `:root` block `var_defaults()` builds (119 → 120), and custom-property drift on every element.

### Removed

- **`@description` no longer states the browser requirement.** It ended `Requires Firefox 126+ (:has() and zoom).`; it now ends at the layout summary. The requirement itself is unchanged — the floor is still Firefox 126, `:has()` needing 121 and `zoom` needing 126 — and it is stated where a reader looks for it rather than in a one-line blurb: `README.md` gives it a "Requirements" heading of its own, alongside Stylus and the Chromium caveat. Do not re-add it to `@description`.

  `USw-notes.md` was rewritten in the same pass and now carries a Requirements heading of its own, so the statement a userstyles.world visitor sees is no longer buried in an old changelog entry.

### Changed

- **`verify.py` resolves `select` defaults.** `var_defaults()` knew `range`, `number`, `text` and `color` only, so a `select` variable would have gone undeclared and every `var()` reading it would have been invalid at computed-value time — the check would have passed while testing nothing. It now reads both spellings `usercss-meta` accepts (a list of bare values, and a map of `"key:Label"` to value), takes the entry marked with a trailing `*` as the default, and falls back to the first entry when none is marked.

## 2026.9.11.1

Compared against `2026.9.10.1`, the entry below. Neither has been published, so an installer coming from `20260910` receives both.

### Added

- **Single photos on `/p/<id>/` and `/<user>/p/<id>/` are now sized consistently.** 2026.9.10.1 recorded that "a single-photo post permalink is currently left entirely stock", on the evidence of two snapshots that scored zero on every selector in the style. That was accurate and is now superseded: the reason those two scored zero is itself the finding.

  **Instagram lays single photos out in two different ways, and which one you get depends on the media's shape.** That, not any single size, is what made them inconsistent with each other:

  | shape | column | media | why |
  | --- | --- | --- | --- |
  | 3:4 portrait | `--x-maxWidth:min(100%,785px)` | 449×599 | column carries Instagram's `.xf68679` |
  | 1:1 square | none at all | 1262×1262 | that class is **absent** |
  | 16:9 landscape | none at all | 1262×712 | same as the square — see below |

  `.xf68679` is Instagram's `max-width: var(--x-maxWidth)` class. The square post's column does not carry it and has no inline token either, so nothing caps the column and it fills the content area — 1262px at a 1638px window, and wider on a wider screen. The 3:4 post starts from 449×599, the same numbers a carousel starts from. One shape was unbounded and the other was smaller than everything else on the page.

  That is also why the earlier pair scored zero on `main div[style*="--x-maxWidth"]`: both were the **square** post. They are the same post at both permalink paths, and the two paths agree to the pixel, as they do for carousels and reels — so on their own they could only prove the two paths agree, never that one aspect ratio behaves like another. The new `Instagram-user-p-id(single_photo133).html` is what made the split visible.

  **`--x-maxWidth` is therefore not the lever here**, however well it works for carousels and reels one block up. Setting it on the square page changes nothing at all: measured at 900px and at 1300px, the column's computed `max-width` stayed `none`, because the element that would read the token is missing the class that reads it. A plain `max-width` on the column works on both shapes, and has the side benefit of adding no sixth design-token override — see `docs/token-overrides.md`.

  **No `zoom`, unlike the carousel rule beside it.** A single photo's `padding-bottom` box takes its width from the column, so the media is the column minus the caption, linearly: measured at 900/1102/1150/1300 with the caption at 429, the media came out 470/672/721/964 wide. Nothing has to be scaled and no aspect ratio is matched, so unlike the carousel settings this is not calibrated against one ratio.

  One new setting, **"Post page: total width of a tall or square single photo and caption"**, which shipped at **1100px** and now stands at 1150. The default is a picked compromise rather than a derived number, and the setting is the user's to move. One constraint on any value chosen, because it is a trap rather than a preference: a range setting's default must be a whole number of steps above its minimum, and `usercss-meta` rejects the style outright rather than clamping. `verify.py` catches it.

  Result at the defaults, against the carousel for reference:

  | | before | after |
  | --- | --- | --- |
  | square photo | 1262×1262 | **670×670** |
  | 3:4 photo | 449×599 | **670×893** |
  | 16:9 photo | 1262×712 | **1168×659** |
  | carousel (3:4) | 674×898 | 674×898 |

  The two capped shapes land four to five pixels from a carousel on both axes and identical to each other in width — which was the point. The landscape photo is deliberately outside that comparison and keeps Instagram's own column; see the landscape entry below. No horizontal overflow, text unchanged at 14/18, nothing zoomed.

  **Three guards, each load-bearing.** `:has(div[style*="padding-bottom"] > img)` requires a photo box in this column; `:not(:has(li[style*="translateX"]))` excludes a carousel; `:not(:has(video))` excludes a reel, which this block's URL pattern also selects. Counted across all ten snapshots the three together match 1 on each of the three single-photo pages and **0 on every other page** — the feed, both carousels, both reels, `/reels/<id>/`, and the `/p/<id>/` modal. That last zero is the one that matters: this block's URL pattern does select the modal, and every other rule in the block is kept off it only by a guard the modal happens to fail.

  `scoped.py --diff` against the pre-change file agrees: standard-property changes on the three single-photo snapshots only (405, 405, 257), and **0 on the other eight**. The only custom-property drift anywhere is the new setting itself, inherited from `:root` and never read outside its own rule — the "set, inherited, never read" signature the tool documents. No `font-size`, `line-height` or `zoom` moved on any page.

  **`.xvc5jky` is in the selector on purpose and must stay.** It is the post column's own class, carried by all three post shapes — 1 on every post page, 0 on the feed, the modal and `/reels/<id>/`. Without it the three guards also match the **"more posts" grid** below the post, and on a reel page that shrank a grid cell from 532×709 to 382×510. Its failure mode is the safe direction: if Instagram churns the class the rule stops applying and single photos return to stock.

  **Two traps worth recording.** `:has()` does not nest, so `:root:has(X)` where `X` itself contains `:has()` is invalid and Firefox drops the whole rule **silently** — the first attempt at the `--media-info` override looked like it had simply had no effect. It does not need `:root` anyway: the column sits closer to the caption than Instagram's own declaration, which is on `:root`, and on every post snapshot each element under the column inherits a single value with nothing redeclaring it in between. `!important` is kept as insurance rather than necessity — the rule measured identical without it on all three pages, but the snapshot's CSS is pruned and the live sheet may carry a declaration the snapshot dropped.

- **Landscape single photos keep Instagram's own width, and gain the adjustable caption column.** The entry above was written with no landscape snapshot and listed that as its main open question. Two now exist — `Instagram-p-id(single_photo56).html` and `Instagram-user-p-id(single_photo56).html`, the same 16:9 post (`DdGxCmDz9r5`) reached by both permalink paths, which agree to the pixel as every other pair has.

  **The inference recorded there was half right.** A landscape column does lack `.xf68679` and does lack an inline `--x-maxWidth`, exactly as predicted, so the rule matched it on the strength of its photo box alone. The prediction that this "already covers it" is the half that was wrong. Stock, the photo is **1262×712** in a 1598px column — already the full width of the content area and, being short, in no danger of running away with the window the way the square one does. Capping that column to the 1100px default took it to **670×378**: under half the area, and short enough to sit in a letterboxed band beside a taller caption. The cap was correcting a problem landscape does not have.

  So the single rule is now **two**. The caption column (`--u-reel-media-info`) is still set for every single-photo shape — that part was always right, and it is what the three shapes genuinely have in common. The width cap (`--u-post-photo-width`) is now withheld from landscape. No new setting: landscape reuses the caption-column variable the reel and post pages already share.

  | | before | after |
  | --- | --- | --- |
  | 16:9 photo | 670×378 | **1168×659** |
  | column | 1100 (capped) | 1598 (Instagram's) |
  | caption | 429 | 429 |

  1168 rather than the stock 1262 because the widened caption takes the difference — 1598 − 429 — which is the trade the setting exists to let you make.

  **The fourth guard reads the leading digit of the ratio**, not the ratio: `:has(div[style*="padding-bottom:1"] > img, div[style*="padding-bottom: 1"] > img)`. That digit separates the two cases: landscape is below 100% and always starts 5–9; square, portrait and reel ratios are at or above 100% and all start with 1. Nothing Instagram accepts is tall enough to reach a leading 2, which is the only thing that would break the correspondence.

  Post media measured across the snapshots — excluding the 133.333% boxes that appear on every post page, which are the "more posts" grid rather than the post: landscape 56.4394%, square 100%, portrait 125% and 133.317/133.333%, reel 177.778%. An earlier draft of this entry gave the portrait ceiling as 4:5 (125%), which `single_photo133` contradicts. The 1.91:1 (52.36%) floor and the 200% claim are **inference from Instagram's documented upload limits, not measurement** — 56.4394% is the widest ratio ever captured here. The guard needs neither bound to be exact, only the 100% boundary.

  Matching one digit rather than a whole percentage is the rule `CLAUDE.md` states, for the reason it states: a single saved feed carried 3:4 as `133.333%`, `133.33333333333331%` and `133.31719128329297%`. Both spellings of the colon are listed because inline-style whitespace is unstable — the server writes `padding-bottom:56.4394%` and a React re-render rewrites it with a space, on the same element, after navigating away and back. **A comma inside one `:has()` is a list, not nesting**, so this is valid where `:root:has(…)` of the same guards would have been dropped silently.

  Failure mode is the safe direction, as `.xvc5jky`'s is: if the guard stops matching, a square photo returns to Instagram's stock layout rather than breaking.

  **Measured.** Guard counts across all thirteen snapshots: the caption-column selector matches 1 on each of the five single-photo pages and 0 everywhere else, the modal included; the capped selector matches 1 on the three square and portrait pages, **0 on the two landscape ones**, 0 everywhere else. `scoped.py --diff` against the pre-change file changes **exactly the two landscape snapshots** (156 standard properties each, the two paths agreeing) and **0 on the other eleven**, with no custom-property drift anywhere and no `font-size`, `line-height` or `zoom` on any page. `verify.py` two-file mode reports the feed computationally identical, 36 rules → 37 from the split with the same 119 declarations surviving on both sides — so nothing was dropped and nothing leaked out of the post block.

  Final sizes at the defaults: landscape 1168×659 in an uncapped 1598px column, square 670×670, 3:4 670×893, caption 429 throughout, both paths agreeing.

### Changed

- **"Post page: total width of photo and caption together" is now "Post page: total width of a multi-photo post and caption."** With a single-photo setting beside it the old label was ambiguous — both would have read as "total width of … photo and caption". Only the label changed; the variable name is untouched, so no saved value is lost. The new wording matches the vocabulary the other two carousel settings already use ("multi-photo post").

- **"Post page: total width of a single photo and caption" is now "Post page: total width of a tall or square single photo and caption."** The setting no longer reaches a landscape photo, so the old label promised more than it delivers. Only the label changed; the variable name is untouched, so no saved value is lost.

- **`@description` no longer claims single photos come out "at a consistent size whatever their shape."** That stopped being true the moment landscape was exempted from the cap. It now says square and portrait are brought to a consistent size and landscape is left at Instagram's own.

- **The two square single-photo snapshots were renamed** from `Instagram-p-id(single_photo).html` and `Instagram-user-p-id(single_photo).html` to `…(single_photo100).html`, and `Instagram-user-p-id(single_photo133).html` was added. The 2026.9.10.1 entry below refers to them under their old names. The two landscape captures, `…(single_photo56).html`, were added later in the same version.

### Removed

- **Every comment outside the metadata block.** The style went from 367 lines to 232. Nothing else changed: no selector, declaration or block condition was touched, and the metadata header is byte-for-byte identical.

  This reverses the standing convention that the style's comments are user-facing, and it was a deliberate call, not drift. The cost is that a reader in the Stylus editor or the userstyles.world code view now gets no explanation of why a guard is shaped the way it is. That is survivable only because `docs/rule-notes.md` already holds every one of those explanations keyed by selector, and is the canonical copy — the comments were the abbreviated duplicate, not the record. **Before loosening a guard or changing a number, read the note there.** Nothing in the style will warn you any more.

  Proven inert rather than assumed so. `verify.py` against the pre-strip file: both keep the same 37 rules and 119 declarations, both change the same 31697 computed properties across 1668 elements, and the two are reported computationally identical. `scoped.py --diff` across all 13 snapshots, each at its own URL: zero standard and zero custom property differences, with every snapshot selecting the same block count as before.

### Not done

- **No height cap.** The tallest photo Instagram appears to accept is the 133.333% of the new snapshot, which at the default lands at 893px tall — within 5px of the carousel's 898px, so there is nothing for a cap to do yet. A cap could not be built the obvious way in any case: `max-height` on a `padding-bottom` box does nothing, for the reason recorded at length under the feed reel-height entry in 2026.9.10.1.

## 2026.9.10.1

Compared against `20260910`, the version published before it.

First release under `YYYY.M.D.R`. The revision suffix exists because `2026.9.10` shipped earlier the same day and plain CalVer had no second slot for it. It starts at `.1`, never `.0`: Stylus compares versions across the longer of the two and reads a missing part as 0, so `2026.9.10.0` would compare *equal* to `2026.9.10` and never be offered as an update. Earlier releases keep their plain `YYYY.M.D` — the same comparison rule is what lets both spellings coexist. See the `shipping-a-release` skill.

### Added

- **Reels on `/p/<id>/` and `/<user>/p/<id>/` are now enlarged.** 2026.9.10 listed this as deliberately unattempted for want of a snapshot; two now exist — `Instagram-p-id(reel).html` and `Instagram-user-p-id(reel).html`, the same reel (`DRcBUtuja8_`) reached by both paths.

  **A reel on a post-permalink URL is not merely similar to a reel page, it is the same layout.** Measured across three snapshots — the two above plus `Instagram-user-reel-id.html`, which is a *different* reel by a different user — every selector count and every box agrees: no `<article>` and no `[role="dialog"]`, one `--x-maxWidth` column at Instagram's stock `min(100%, 673px)`, a 337×599.1 video inside a `padding-bottom:177.778%` box, `--media-info` at its stock 335px, and zero `li[style*="translateX"]`. The third snapshot is what makes this evidence rather than coincidence: the two post-permalink captures are the same post, so on their own they could only prove the two *paths* agree.

  Note the stock column is **673px** here, not the 785px the carousel post pages carry. Instagram sizes it to the media, so the two post-page shapes start from different numbers.

  Because it is the same layout, **no new rule and no new setting were written.** The reel block's URL pattern was widened to cover the two post-permalink paths, and its three rules — every one of them already guarded on a `<video>` in the `--x-maxWidth` column — reach them unchanged:

  ```
  regexp("https://www\\.instagram\\.com/[^/]+/reel/.*")
  →
  regexp("https://www\\.instagram\\.com/(p|[^/]+/p|[^/]+/reel)/.*")
  ```

  Result on both new snapshots, identically: video 337×599.1 → **520×855**, column 673 → 950, caption 335 → 429, page height 2205.9 → 2461.8, no horizontal overflow, text unchanged at 14px, nothing zoomed. Those are the same numbers `/<user>/reel/<id>/` already produced, which is the whole point.

  The pattern was checked against eleven URL shapes as a full match, which is how `regexp()` is evaluated. It gains `/p/<id>/`, `/<user>/p/<id>/` and a `?img_index=` query form; it keeps `/<user>/reel/<id>/`; and it still excludes `/reels/<id>/`, the `/reel/<id>/` floating dialog, `/<user>/reels/`, `/reels/audio/<id>/`, the feed and a profile. The two exclusions that matter hold for a stateable reason: neither carries a `p` segment, and neither offers a `<segment>/reel` pair — `/reel/<id>/` has nothing before `reel`, and `/reels/<id>/` has no `reel` segment at all.

  The video is `object-fit: contain` in a 521px-wide box, so a 9:16 source letterboxes by about 40px either side rather than cropping. That is not new and not specific to these pages — it is what reel pages have always done at these settings.

### Changed

- **"Reel page: total width of reel and caption together" is now "Reel and post pages: …"**, since that setting governs the two post-permalink paths as well now. Only the label changed; the variable name is untouched, so no saved value is lost. `u-reel-media-info` was already labelled for both.

  A reel on a post page therefore shares `u-reel-width` with reel pages rather than taking `u-post-width`. That is deliberate and follows from the measurement above: the layouts are the same, so one number serves both. `u-post-width` continues to govern carousels on those URLs, and the two labels stay apart by reading "reel and caption" against "photo and caption".

### Fixed

- **The feed's media rules no longer reach a post opened as a floating modal.** Reported against the new `Instagram-p-id-modal(single_photo).html`: the photo's height was being governed by "Feed: never let a photo or reel get taller than", a *feed* setting, on a post page.

  The four rules in the Media section of the `domain()` block were keyed on `article` alone. Every other feed rule in that block — both two-column rules, the feed-reel width cap, the feed-reel height cap — carries `:not([role="dialog"] *)`; this section had simply never been given it. A `/p/<id>/` post opened as a modal (clicking a post in the feed, or reaching the URL from a profile grid) renders as an `<article>` **inside** a `[role="dialog"]`, so it collected the whole feed media treatment.

  Measured on that snapshot before the fix: `article div[style*="padding-bottom"]:has(> img):not(li *)` matched 1, the box was collapsed from `padding-bottom: 925px` to 0, and the image picked up `max-height: none → 900px`. Instagram sizes this media itself — an ancestor of the `padding-bottom:100%` box carries an inline `max-height:925px;max-width:925px;aspect-ratio:1/1` — so the 900px default was undercutting Instagram's own cap by 25px, and any lower setting by more.

  **All four rules were guarded, not only the one carrying the height cap.** They are one pipeline: collapsing the reserved box is what makes the cap meaningful, so exempting the cap alone would have left the modal with a collapsed box around an uncapped image — worse than either state.

  The guard's reach was measured across all ten snapshots. It changes exactly one page. On the feed, all four selectors match the same elements with and without it (four `<article>`s, no dialog); `/reels/<id>/` has a dialog but no `<article>`; no other page has either. `verify.py` on the feed reports the two versions computationally identical at the same 116 declarations, and `scoped.py --diff` reports 0 standard and 0 custom differences on nine of ten snapshots. On the modal it reports 36 standard differences, all of them the page returning to stock: the box regains `padding-bottom: 925px`, six elements in the media chain regain their 925px height, and the image returns to Instagram's `position: absolute` / `height: 100%` / `object-fit` with `max-height` gone. No `font-size`, `line-height` or `zoom` moved.

  Two things this did **not** turn out to be. The two non-modal single-photo snapshots — `Instagram-p-id(single_photo).html` and `Instagram-user-p-id(single_photo).html`, the same post at both permalink paths — score **zero** on every selector in the style: no `<article>`, no `min(470px`, and no `main div[style*="--x-maxWidth"]` either. A single-photo post permalink is currently left entirely stock, and is untouched by this change. And the modal is not reached by either `regexp()` block despite its `/p/<id>/` URL selecting both: every rule in those two blocks is guarded on `main div[style*="--x-maxWidth"]`, which matches 0 there. The `domain()` block was the only one reaching this page.

  Note that the 2026.9.10 entry below, on the text-token carriers, records that "the feed rules are unaffected either way: their `:not([role="dialog"] *)` guards are on layout selectors keyed on `article`". That was true of the rules it was comparing against, but it read as though every `article` rule in the block carried the guard. Four did not.

- **"Feed: never let a photo get taller than" now limits reels too**, which is what the label had always implied. It never had: the declaration that was supposed to do it sat on the reel's `padding-bottom: 125%` box, whose height is entirely padding, so `max-height` had nothing to clamp — it constrains the content box, which is zero here. Measured on the saved feed at a 1638px window with the setting forced to 400px: computed `max-height: 400px`, rendered height 898px, unchanged. Forcing `box-sizing: border-box` did not rescue it either (still 898px); a border box cannot shrink below its own padding. The declaration had never done anything, in either box-sizing mode, and was removed.

  The working form caps the **anchor** that wraps the box. A percentage padding resolves against the containing block's width, and the anchor is that containing block, so `max-width: calc(height / 1.25)` is the width that produces the wanted height. Measured across the setting's range at the same window: 900 (default) and above do not bind here and the reel stays 550×898; 800 → 550×800; 600 → 480×600; 400 → 320×400; 300 → 240×300. Carousels are unaffected at every value (702×936 throughout).

  Scoped to 125% reels by a `:has(div[style*="padding-bottom"][style*="125%"])` guard on the anchor, matching the box rule beside it. A 4:3 reel keeps its own 75% box: it needs a media column near 1200px to reach even the 900px default, and no snapshot of one exists to test a second divisor against.

  No `!important`. Instagram computes `max-width: none` on this anchor and the style's own rule below it sets `width` only, so there is no collision to win.

- **The label now reads "Feed: never let a photo or reel get taller than."** Only the label changed; the variable name is untouched, so no saved value is lost.

- **"Text: spacing between lines of that text" now reaches the text that "Text: size of usernames, captions and comments" already reached.** The two settings had drifted apart on every page, and on `/reels/<id>/` the spacing setting did nothing whatsoever.

  Root cause is one Instagram class. `.xvs91rp` is declared `font-size: var(--system-14-font-size)` and sets font-size **alone**, unlike `._aaco`, which sets both. Wherever that class is the one styling the text, it took the size setting and left the spacing at whatever it inherited.

  On `/reels/<id>/` the effect was total rather than partial, because there `.xvs91rp` is the *only* token reader under `main`: the page has no `<article>`, so `main` is the sole carrier, and the classes that do read the line-height token are all out of reach — `._aaco` sits in the comments panel outside `main`, while `.x17ydfre`, `.x1d6elog` and the `body textarea` rule match zero elements on that page. The reel text's spacing was therefore an inherited computed `18px` from `body._ar45`, which resolves the token at its `:root` value *before* `main` redeclares it — and a declaration on a descendant cannot reach back up to change an ancestor's computed value. Measured on the saved page: the setting was inherited by 1826 elements and read by **none**.

  The fix pairs `line-height` onto that class beside the font-size it already reads. Elements whose computed line-height moves with the setting raised, before → after: feed 84 → 129, `/reels/<id>/` **0 → 241**, `/<user>/reel/<id>/` 67 → 524, both post pages 43 → 267. Against the font-size reach on the same pages (115 / 241 / 542 / 293) the two settings now cover comparable ground. Verified by applying the shipped `20260910` file and this one to all five snapshots and counting computed changes at 1638×900.

  The feed change is deliberate and not confined to reel pages: the extra 45 elements there are the `.xvs91rp` timestamps (`•`, `5m`), which already followed the size setting and now follow the spacing one too.

- **The comments panel on `/reels/<id>/` now takes both text settings.** It was recorded as a known gap on the grounds that the panel renders outside `main`, in a sibling subtree whose React mount carries only a generated id. That is true of the mount, but the panel itself is a `[role="dialog"]`, which is a stable hook, so `[role="dialog"]` was added as a third token carrier beside `article` and `main`. Measured on the saved page: font-size reach 143 → 241, bringing the panel's 11 comments in.

  The pairing above names both carriers. Scoping it to `main` alone left the panel's own 32 `.xvs91rp` taking the size setting without the spacing one — landing 154 line-height changes instead of 241, i.e. the same defect reproduced in the newly reached subtree.

  `/reels/<id>/` is the only saved page carrying a `[role="dialog"]`, so the reach on modals elsewhere could not be measured offline and was **checked live instead** (2026-09-10). Both floating modals — `/reel/<id>/` and `/p/<id>/` — follow the two text settings, and follow them consistently with the size setting's own reach: no subtree took one setting without the other. That is the outcome the carrier was added for. Modals outside those two paths (settings, share sheets) were not part of the check.

  The feed rules are unaffected either way: their `:not([role="dialog"] *)` guards are on layout selectors keyed on `article`, not on the token carriers.

### Notes

- The feed-reel comment gained a paragraph recording that `max-width` on the 125% box narrows it without shortening it — the height is percentage padding and resolves against the containing block, so at default settings the box is 550×898, not 550×687.5. That is the measurement the anchor cap exists to work around, and it is written down so the cap does not get "simplified" back onto the box. The existing sentence about cropping is unchanged: it describes Instagram flattening 133%/177% sources into a 125% box, which crops top and bottom, and is not a claim about the width cap.

  One open question left at the rule rather than settled: below about 690px the anchor becomes the binding constraint and the box returns to a true 125%, where above that it stays 550 wide. How much of a flattened source that reveals or hides is not calculable from the DOM, because the box does not carry the source's real ratio.

- The `svg[aria-label="Instagram"]` removal is written up under 2026.9.10's **Removed**, but it did not make it into the uploaded `20260910` — that file still carries the rule, so the removal lands in this release instead. Nothing changed here; only the version it ships in did. The evidence stands as recorded: computed width 24px with and without, and a full two-file diff identical across all 1668 elements.

- **`verify.py` cannot see the reel-page change, by construction.** Its `prepare()` flattens every `@-moz-document` block unconditionally — which is what makes its two-file mode a valid equivalence proof — so a change to a block's URL *condition* is invisible to it. Run against this release it reports 35 rules / 116 declarations and passes, and a two-file diff against the file as it stood before the widening is computationally identical across all 1668 elements of the feed snapshot. That is the correct result and not evidence of anything: strip the comments from both and the rules are byte-identical, because only the condition and one label moved.

  The URL scoping was therefore checked two other ways. The pattern itself was full-matched against eleven URL shapes (listed under **Added**). And every snapshot was re-measured through a scoping-aware harness that includes only the blocks whose condition matches that page's real URL, diffing every computed property of every element before and against after:

  | snapshot | URL used | standard | custom |
  | --- | --- | --- | --- |
  | `Instagram-p-id(reel).html` | `/p/DRcBUtuja8_/` | 553 | 1118 |
  | `Instagram-user-p-id(reel).html` | `/lijiao9/p/DRcBUtuja8_/` | 553 | 1106 |
  | `Instagram-p-id(carousel).html` | `/p/Da-Ak53DEHh/` | **0** | **0** |
  | `Instagram-user-p-id(carousel).html` | `/bibihamers/p/Da-Ak53DEHh/` | **0** | **0** |
  | `Instagram-user-reel-id.html` | `/fitdodoo/reel/DdEdvCFSyTN/` | **0** | **0** |
  | `Instagram (…).html` (feed) | `/` | **0** | **0** |
  | `Instagram-reels-id.html` | `/reels/Dc-NB7sge4u/` | **0** | **0** |

  Only the two intended pages move, and they move by the same 553 standard properties. The custom-property figure is `--media-info` inheriting to every element from a `:root` declaration — the "set, inherited, never read" drift `verify.py` already documents, not something that renders.

  What moved on those two pages is geometry and nothing else: `width`, `height`, their logical aliases, `transform-origin`/`perspective-origin` as a consequence, and singletons for the column's `max-width` and the reel box's `padding-bottom`. **No `font-size`, no `line-height`, no `zoom`, no `color`** appears in the diff — which is the check that matters here, since scaling a container that holds the caption is the failure mode the post block's own zoom rule had to be walked outward to avoid.

### Not done

- **No guard was written against a *mixed* carousel** — photo plus video slides — on a `/p/` URL. It is the one page shape that could satisfy the reel block's loose `:root` video guard and the post block's carousel guard at the same time, now that both blocks match these URLs.

  Everything measurable says it is harmless. Both blocks set `--media-info` to the same 429px, so that collision has no outcome. The reel block's column rule needs the exact child chain `:has(> div > div > div video)`, which scores **0** on both carousel snapshots. And the reel block precedes the post block in the file, so at equal specificity a carousel's own `--x-maxWidth` wins any collision that did occur. Carousel slides also use an `aspect-ratio` spacer rather than a `padding-bottom` box, which is what the `177` rule keys on.

  It was left unguarded because no snapshot of a mixed carousel exists to test a guard against, and an untested selector is the thing this file's conventions exist to avoid. If one ever lays out wrongly, adding `:not(:has(li[style*="translateX"]))` to the reel block's `:root` and column rules is the first thing to try — but measure it against a real capture first, because on a flattened feed that exclusion *does* change the outcome.

- **Carousels are still uncapped, deliberately.** A carousel's height is `468px × ratio × zoom`, and the same padding-percentage reason applies to its spacer: `max-height` there changed nothing (936px before and after). `max-height` on the zoomed wrapper does bite, but only as a crop with `overflow: hidden`, and the value has to be divided back out by the scale because it is inside the zoom — measured, `calc(400px / var(--u-carousel-scale))` plus `overflow: hidden` gave exactly 400px on screen with the bottom of the photo cut off. Fitting rather than cropping means lowering the scale, which needs the media's aspect ratio. That is readable from the inline `padding-bottom` prefix the way `125%` and `177` already are, so a per-ratio bucket using `tan(atan2())` is possible — it was not written because it costs one rule per known ratio and was out of scope here.

## 2026.9.10

Compared against `20260907`, the version published before it.

### Added

- **Carousels are enlarged.** Previously they were left at Instagram's stock 468px while single images were widened. The whole carousel wrapper is now scaled with `zoom`, which takes the inline `translateX(n × 468px)` slide offsets with it, so slide alignment is preserved. `zoom` reflows (unlike `transform: scale()`), so the wrapper really occupies its new size and Instagram's own flex column centres it. The scale factor is derived from the media column width via `tan(atan2(a, b))`, because CSS cannot divide by a length.
- **Every setting is now a Stylus UserCSS variable**, editable from the Stylus options UI instead of by hand-editing `:root`. Thirteen knobs: feed width and its minimum, media column share, caption wrap threshold, media maximum height, feed-reel maximum width, carousel maximum scale, text size and line height, the two post-page settings added below, reel-page total width, and the caption column width shared by reel and post pages.
- **Every setting is labelled in plain language**, so the Stylus options screen can be used without reading the stylesheet — "Feed: never let a reel get wider than" rather than "Feed reels: maximum width". Only the labels changed; the variable names are untouched, so no saved value is lost. Two labels were also wrong rather than merely terse: `u-reel-width` is the whole media-plus-caption column, not the reel, and `u-reel-media-info` now governs post pages as well as reel pages. The post-page labels say "Post page:", not "Single post page:" — "single" sits in the same label as "multi-photo" and reads as a post with one photo, the opposite of what the setting acts on, and the "Feed:" prefix already separates a post in the feed from the page for one post.
- `@preprocessor default`, `@homepageURL`, and a real `@license` (MIT, was "No License"). `@namespace` now carries the account name.

### Changed

- **Requires Firefox 126+**, stated in `@description`. `:has()` needs 121 and the new `zoom` rule needs 126.
- **Post text now defaults to Instagram's own size.** 20260907 hard-coded `--system-14-font-size: 16px` and `--system-14-line-height: 1.2` for everyone. The defaults are now 14px and 18px, Instagram's own values, so the style changes nothing there until the setting is moved. Confirmed on the saved snapshot: at defaults, not one standard property computes differently.
- **The text settings reach reel pages, which 20260907 did not.** The override is declared on `article, main` — no `:root`, which would be inert: Instagram declares the same two tokens on `._aa4c`, a class it puts on `<html>`, from a `<style>` in the body, so it wins on document order at equal specificity. 20260907's `:root, article` therefore only ever worked through `article`, and neither `/<user>/reel/<id>/` nor `/reels/<id>/` contains an `<article>` at all. Naming the containers also pins the scope on our side: a `:root` selector would silently start winning, and go site-wide, if Instagram ever moved that `<style>` into the head. Measured on the three saved pages with the size raised, elements whose computed size changes: feed 108 → 131, `/<user>/reel/<id>/` 0 → 544, `/reels/<id>/` 0 → 143; removing `:root` changed none of those three numbers, which is what "inert" means here. `!important` on `:root` would instead give 1334 / 2498 / 2436 — every button, textarea and label on the site — so it was not done. Known gap: the comments panel on `/reels/<id>/` renders outside `main`, in a sibling subtree of the React mount, so its comments keep Instagram's size. The mount has only a generated id, which is not safe to match.
- **Domain scope tightened** from `instagram.com` to `www.instagram.com`, so the style no longer loads on subdomains it was never written for.
- **Inline-style matching hardened.** Instagram emits the same declaration with and without a space after the colon depending on whether the markup was server-rendered or re-rendered through the CSSOM, and the same element can switch after navigating away and back. Three selectors matched whole values and so matched only some of the time:
  - `min(470px, 100vw)` → prefix `min(470px`
  - `padding-bottom: 125%` → `[style*="padding-bottom"][style*="125%"]`
  - `padding-bottom: 177` → `[style*="padding-bottom"][style*="177"]`
- **`--media-info` is now scoped to reel pages.** It was declared in the `domain()` block, where it also overrode Instagram's token of that name on post modals and anywhere else the site reads it. It now lives in the reel-page `regexp()` block.
- **All custom properties are prefixed `--u-`.** The old `--feed-width` silently collided with Instagram's own `--feed-width` token (470px, declared on `:root`), making the style an override of theirs rather than a private variable. The only unprefixed properties left are the deliberate overrides of Instagram tokens: `--media-info`, `--x-width`, `--x-maxWidth` and the `--system-14-*` pair.
- **Feed column maximum width removed** (`--feed-max: 90%`). The declaration is now `max-width: none`; it existed only to defeat Instagram's inline `max-width`, and the width setting is what governs.
- **Two-column post rules rewritten with CSS nesting.** The guard `:has(> div:nth-child(3))` was repeated across six selectors and can now drift only in one place.
- Comments trimmed throughout, and several corrected. The feed-reel rule was documented as being kept off photo posts by `:has(video)`, which it does not contain — the `a[href*="/reels/"]` guard on the article does that.

### Removed

- **The collapsing left nav** — the rules that set `--nav-narrow-width`, `--nav-medium-width`, and `--nav-wide-width` to 72px and restored 244px/335px on hover. Instagram still declares those three tokens, which is where the hover values came from, but nothing reads them any more: no `var()` consumer appears in a saved page, and setting them has no visible effect on a live one. Rebuilding the feature means finding whatever governs nav width now; the old token names are a dead end.
- **The `:root` half of the `--system-14-*` override.** 20260907 declared these on `:root, article`. The `:root` selector never did anything — see the entry under Changed — so it was dropped rather than left looking load-bearing.
- **The settings-page padding rules** on `.x17snn68` / `.xw2csxc`. They existed to compensate for the collapsed nav and do nothing without it.
- **`svg[aria-label="Instagram"] { width: min(103px, 100%) }`**, a third nav leftover. In 20260907 it sat immediately after the nav block, which is where its two branches make sense: `100%` stopped the logo overflowing the rail the style had narrowed to 72px, and 103px capped it once hover expanded the rail. With the nav rules gone nothing narrows the rail any more. The selector still matches, but what it matches on all five snapshots is a 24×24 `viewBox="0 0 24 24"` glyph in the rail's home link, not a 103px wordmark — so its containing block is 24px, `100%` resolves to 24px, and `min(103px, 24px)` returns the size the glyph already had. Measured under the `verify.py` harness on the feed snapshot: computed width 24px with and without the rule, and a full two-file diff of the style against itself minus this rule is computationally identical across all 1668 elements. The rail is present in that snapshot but its fixed container computes to width 0, so the offline evidence covers only the collapsed state; the user confirmed on a live page that it changes nothing whatever the rail is doing. This also retires the open item about the `aria-label` being confirmed only on an `en` page — a rule that does nothing cannot silently do nothing in other locales.
- **`:not(.xtcbf50)`** from the two-column post selector. The class was inherited from an earlier version with no recorded purpose and was not found anywhere — live feed, reel pages, `/reels/audio/`, or the saved snapshot — so it excluded nothing. This is the one change here that no offline check can validate, precisely because the class is absent everywhere we can look: if some post type ever lays out wrongly, restoring this exclusion is the first thing to try.

### Notes

`verify.py` passes on the shipped file. The comment-trimming and unwrapping passes were each proved computationally identical over 1668 elements before being kept, so neither changed rendering.

Coverage figures above come from loading all three saved pages in headless Firefox with the text size raised, and counting elements whose computed font-size or line-height changes. The saved pages are a feed, a `/<user>/reel/<id>/` and a `/reels/<id>/`.

The style runs under Stylus for Chromium, confirmed in ungoogled-chromium on 2026-09-10. `@-moz-document` had been assumed to make this Firefox-only. No Chromium version floor has been established, and both `@description` and `USw-notes.md` still name Firefox 126+ only.

### Investigated, not changed

A report of high memory use on some Instagram pages, seen in both Firefox and Chromium. **No root cause was found and nothing was changed.** The symptom did not reproduce on demand when looked for. Three hypotheses were tested and all three came back negative; do not re-open them without a reproduction.

- **Zero-height posts driving an infinite-scroll runaway.** The theory was that the media-box collapse (`height: auto` plus `position: static` on the image) yields a zero-height post whenever the image has no intrinsic size, leaving the feed short enough that the scroll sentinel never leaves the viewport and Instagram appends pages forever. Rejected by observation: on a live affected page, article count, image count and `scrollHeight` all stayed flat over a minute of sitting still.

  The collapse itself is real but was only reproduced against the snapshot, where it is an artifact. Applying the style there drops one article from 1135px to 419px and zeroes its `_aagu`/`_aagv` wrappers — but every `<img>` in the snapshot has `src="data:,"` (SingleFile stripped the bitmaps) and so reports `naturalWidth` 0. The snapshot cannot show whether a live, not-yet-loaded image behaves the same way. Worth knowing that the trap the style already documents for `<video>` has the same shape for images.

- **`zoom` raster cost.** Measured, and too small to matter: rasterised media area over one 1638×900 screenful goes from 378,581px² to 595,878px², about +57%, on the order of 1.5MB → 2.4MB. Bounded per screen, so it cannot produce unbounded growth.

- **The shipped and local versions both enabled at once compounding `zoom`.** Plausible on its face, since `zoom` multiplies down the ancestor chain and the `:not([style*="--x-width"])` guard exists to stop exactly that. Rejected by measurement: with both sheets applied in either order, maximum effective zoom stays 1.500 across 81 zoomed nodes and media area is unchanged to within 9px². 20260907 declares no `zoom` at all, and where both versions match they match the same element, so the cascade picks one winner rather than nesting.

The leading explanation is now the null one — Instagram's own retention on infinite-scroll pages, several tabs at a time, independent of the style. That both engines behave alike supports it. To beat it, the measurement needed is the same page at the same scroll depth in two windows, style on versus off, compared in `about:performance` or Chromium's task manager.

### Added — post pages enlarge carousels

Post permalink pages (`/p/<id>/` and `/<user>/p/<id>/`) previously got nothing from this style. Carousels there are now scaled by a new setting, **Post page: enlarge a multi-photo post by** (`u-post-media-scale`, default 1.5). Measured against two new snapshots, `Instagram-p-id.html` and `Instagram-user-p-id.html`.

With the defaults, media goes from 449×598.7 to 673.5×898.0 on both snapshots, the caption column widens from 335 to 429 to match reel pages, the column widens from 785 to 1150 to hold both, the username box stays 70.8×18.0 and the page does not overflow.

**Reels on these URLs are not covered.** The selector keys on the carousel's slide list, so it cannot match a single-media post, and no snapshot of a reel on a post URL exists to write one against. Left deliberately unattempted rather than guessed at.

**The setting is separate from Carousels: maximum scale on purpose.** That one is a *maximum* applied to a computed fit; this one is the scale itself, since no fit can be computed here (see below).

**The rule is not self-guarding.** It must stay inside its `@-moz-document` block: on a feed page the same selector matches a 470×3644 region spanning many posts, and zooming it scales the feed's text — a username box measured 18px going to 27px. URL scoping, not the selector, is what keeps it off the feed. This is recorded at the rule itself too.

**The two paths are one layout.** Every selector census and the whole height chain agree between the two snapshots, down to identical computed values. One rule will cover both.

**No feed selector reaches them.** All four score zero: the `min(470px` wrapper, the carousel `zoom` selector, the `--x-width` post column and the 630px feed column. The page carries no `min(470px` anywhere. Its column token is `--x-maxWidth` (Instagram's own value `min(100%, 785px)`), the same name the reel-page block uses, and the slide frames carry an inline literal `width: 449px` with slide offsets written as multiples of 449.

**Widening the column does nothing.** Forcing `--x-maxWidth` to `min(100%, 1200px)` widens the column to 1200px and leaves the media at 449×598.7 — measured, not inferred. The media is sized by that inline 449px and an `aspect-ratio: 0.75 / 1` spacer that derives height from width (449 / 0.75 = 598.667). Where the 449 comes from is Instagram's JS and is not visible in a static snapshot.

**Overriding the slide width collapses the media to zero.** `li > div { width: 100% }` gives 0×0 — the same hazard the feed rule documents for `:not(li *)`. Do not retry it.

**`zoom` works, and the media-only container has been found.** Zooming enlarges the carousel and preserves slide alignment (offsets stay evenly spaced at the new width), so the mechanism transfers from the feed. The first containers tried also held the caption — the username box scaled from 18px to 23.4px at `zoom: 1.3` — but walking outward from the `<ul>` and counting text characters at each level locates the boundary exactly: every ancestor up to and including the one at 450×598.7 has zero text characters, and its parent jumps to 2283 characters and 26 images.

That container is two levels inside the column, and this selects it:

```
main div[style*="--x-maxWidth"] > div > div:has(li[style*="translateX"])
```

`translateX` is matched rather than `transform:` because it sits after the colon and so is immune to the inline-style whitespace problem.

Measured on both snapshots, identically: `zoom: 1.6` takes the media from 449×598.7 to 718×957.8 with slide offsets evenly spaced, no horizontal overflow, and the username and caption boxes unchanged at 70.8×18.0/14px and 251×396.

Settled by decision, not by measurement:

- **The scale is a separate setting**, not a reuse of `--u-carousel-scale-max`. That one is a maximum clamping a computed fit; this is the scale itself.
- **The column cap is raised.** An earlier revision of this entry recorded the opposite — that the stock 785px cap would stay — on the grounds that raising it only adds empty space. That reasoning was right in isolation and wrong in context: it was measured before the caption column was widened. See below.

No fit can be computed here, which is why the scale is a plain factor. The feed's `tan(atan2())` formula divides by a constant 468px because the feed wrapper is that wide whatever the media ratio; here the slide width varies with the ratio, and CSS cannot read an element's own width to divide by it.

#### Caption column and column width

These pages lay out like a reel page — media and caption side by side in one column, stock 785px splitting 449 media + 335 caption. The caption is now widened to match reel pages, from the same `--u-reel-media-info` setting.

That is what forces the column wider. The media area comes out as column width minus caption width exactly (785 → 356, 950 → 521, 1200 → 771), so once the caption takes 429px the stock column leaves only 356px for a media that zoom has made 673.5px wide — it overflows its box by 317.5px. The reel page's own `--u-reel-width` is no better: at its 950px default the overflow is still 152.5px. Hence a separate **Post page: total width of photo and caption together** (`u-post-width`, default 1150). The requirement is caption + natural media width × scale, which at the defaults is 429 + 449 × 1.5 = 1102.5; 1150 leaves slack.

Overshooting is not free. The media stays whatever size zoom made it, so surplus column width becomes empty space around it — and because an aspect-ratio spacer sizes the container, surplus width becomes surplus *height* too: at 1400 the container is 971×1293 around a 673×898 media.

The two settings are therefore coupled, and cannot be coupled automatically, because the natural media width varies with the post's aspect ratio (449px on the 3:4 post both snapshots contain) and CSS cannot read it.

Verified end to end with the real style file, identically on both snapshots: media 449×598.7 → 673.5×898.0, container 721 so the media fits, caption 335 → 429, column 785 → 1150, username unchanged at 70.8×18.0, no page overflow.

**Every rule in the block carries the same carousel guard**, `:has(li[style*="translateX"])`. Widening the caption is only safe when something widens the media to match, and the zoom rule cannot match a single-media post — so without the guard a reel on one of these URLs would hit exactly the bug fixed on reel pages above.

Note the feed's scale formula does not transfer as-is either. It divides by a constant 468px because the feed wrapper is always 468px wide whatever the media ratio; here the slide width varies with the ratio, so there is no constant to divide by.

### Fixed — reel pages made carousels smaller than stock

On `/<user>/reel/<id>/`, the `--media-info` override applied to every page the URL matched, but the rule that widens the media column to compensate is gated on a video:

```
main div[style*="--x-maxWidth"]:has(> div > div > div video)
```

A carousel post has no `<video>`, so the caption column took its 429px and nothing gave the media the space back — the result was smaller than with the style disabled. Reported from the live site.

Fixed by giving the token the same condition, so the pair travels together:

```
:root:has(main div[style*="--x-maxWidth"] video)
```

The guard is looser than the column rule's — a descendant combinator rather than that rule's exact child chain — because it only has to answer "is there a video in the media column", not "which element is the column".

Verified across snapshots: the guard matches on the video reel page (1) and on neither post page (0). `verify.py` is unchanged at 31 rules / 109 declarations / 25,243 computed properties, because on the feed snapshot the guard is true and the token applies exactly as it did before.

Note for anyone reaching for `[style*="--x-maxWidth"]` as a page-type test: it is **not** one. Feed, reel page and post pages each carry exactly one such element. Only the video inside it distinguishes them.
