# Rule notes

Why each rule in `Instagram.user.css` is written the way it is, and what was measured to get there.

**This file exists because the style itself ships.** `Instagram.user.css` is uploaded to userstyles.world, where its comments are read by installers and by anyone editing the style in Stylus, so it carries only short explanations of what a rule does. Snapshot filenames, element counts, pixel measurements, references to `verify.py` / `scoped.py` / `CHANGELOG.md`, and the history of what a rule used to be are all project-internal — they belong here.

The text below is the reasoning as it stood in the style file before that split, preserved verbatim. Treat it as the evidence record for each rule: **read the note here before loosening a guard or changing a number.** Where a claim is inference rather than measurement it says so, and those markers are load-bearing — see the comment conventions in `CLAUDE.md`.

Sections are in the order the rules appear in the style. A heading of *(section header)* is a block comment that introduces a group of rules rather than a single one.

---


## Inline-style matching (whole-file rule)

Inline styles: never match a whole value. Instagram writes the same declaration with and without a space after the colon (server-rendered markup vs a CSSOM re-render), and one ratio appears under several spellings (3:4 as 133.333%, 133.33333333333331%, 133.31719128329297%). Match a distinctive prefix, or split into two conditions.


## `:root`

Stylus turns each knob in the header into a custom property on :root and concatenates that rule into every section, so the reel-page block at the bottom sees them too. Only computed values live here. Every property this style declares is prefixed --u- so it cannot collide with one of Instagram's own tokens; the exceptions are deliberate overrides, marked as such where they appear.


## `--u-media-px` (declared on `:root`)

Width available to the media column, as a real length -- the carousel scale below is a unitless ratio, and CSS can only build one out of two lengths. Restating the feed width against the viewport is exact, not approximate: the nav rail is fixed-positioned and takes no layout space, so the feed column's containing block is the full viewport. The 12px is the scrollbar, which Firefox counts in vw but cannot lay out in; it is a constant because a percentage inside atan2() would not resolve.


## `article, main, [role="dialog"]`

--system-14-font-size and --system-14-line-height are Instagram's own tokens, so these keep Instagram's names instead of taking the --u- prefix. The defaults are Instagram's own values, 14px and 18px, so the style changes nothing here until the setting is moved.

Scope comes from which ancestor the token is declared on, not from the cascade. article and main carry the value by sitting closer to the text than anything of Instagram's.

:root is deliberately not among them. Instagram declares the same two tokens on ._aa4c -- a class on <html>, so a same-specificity rival to :root -- from a <style> in the BODY, which is later in document order and therefore wins; a :root selector here would do nothing at all. It would also be a trap: if Instagram ever dropped that declaration or moved the <style> into the head, :root would silently start winning and the setting would jump from about 130 elements to the whole UI, with nothing changed on this side. Naming the containers pins the scope here instead of to Instagram's build output. Forcing :root with !important has the same site-wide reach, since ._ar45 sets body's font-size from these tokens and most text inherits from there.

main is what reaches the reel pages, neither of which has an <article>. Measured on the three saved pages with the size raised, elements whose computed size changes: feed 108 -> 131, /<user>/reel/<id>/ 0 -> 544, /reels/<id>/ 0 -> 143. !important on :root would instead give 1334 / 2498 / 2436, i.e. the entire UI including buttons and textareas.

[role="dialog"] is the third carrier because the comments panel on /reels/<id>/ renders outside main, as a sibling of it rather than a descendant. It was previously recorded here as unreachable, on the grounds that the React mount above it carries only a generated id; that is true of the mount, but the panel itself is a [role="dialog"], which is a stable hook. Measured on the saved /reels/<id>/ page: adding it takes font-size from 143 to 241 elements and brings the panel's 11 comments in.

/reels/<id>/ is the only saved page carrying a dialog, so the reach on modals elsewhere was checked live instead (2026-09-10): the floating /reel/<id>/ and /p/<id>/ modals both follow the two text settings, and both do so consistently with the size setting's own reach -- no subtree took one setting without the other. Modals outside those two paths (settings, share sheets) were not part of that check.


## `main .xvs91rp, [role="dialog"] .xvs91rp`

.xvs91rp is Instagram's `font-size: var(--system-14-font-size)` class, and it sets font-size ALONE -- unlike ._aaco, which sets both. Text carrying it therefore took the size setting while its spacing stayed at whatever it inherited, so the two settings drifted apart wherever this class is the one in play.

That is the whole of the bug on /reels/<id>/, where the effect is total rather than partial: the page has no <article>, .xvs91rp is the ONLY token reader under main (104 of them), and the classes that do read the line-height token are all out of reach -- ._aaco sits in the comments panel, and .x17ydfre, .x1d6elog and the `body textarea` rule match zero elements. So the spacing setting was inherited as a computed 18px from body._ar45, which resolves the token at its :root value before main ever redeclares it, and a declaration on a descendant cannot reach back up to change it. Measured before this rule: the setting was inherited by 1826 elements and read by none.

Pairing the two properties on this class closes the gap on every saved page, not just that one. Elements whose computed line-height moves, before -> after: feed 84 -> 129, /reels/<id>/ 0 -> 241, /<user>/reel/<id>/ 67 -> 524, both post pages 43 -> 267. Against the font-size reach on the same pages (115 / 241 / 542 / 293) the two settings now cover comparable ground.

Both carriers are named. Scoping this to main alone left the comments panel's own 32 .xvs91rp taking the size setting without the spacing one, which is the same defect in a new place.


## `article ._aacl._aaco._aacu._aacx._aad7._aade, article ._acan, article .x1f6kntn`

Captions sit in a narrow column once the two-column layout below kicks in, so long unbroken words and URLs need somewhere to break.


## `.x6bx242`

The right-hand rail. Despite the name this is not only "Suggested for you" -- the same container holds your own profile block and the account switcher, so hiding it removes those too. That is intended; reach the switcher through the nav instead.


## `main > div > div[style*="630px"], main > div > div[style*="max-width"]`

The feed column. max-width is not a cap -- it exists solely to defeat the inline max-width Instagram sets on this element. The width above is what governs.


## `main [style*="--x-width"][style*="470px"], .xmnaoh6 + div > div`

Post column inside the feed column.


## `main div[style*="min(470px"]:not(li *):not(:has(ul))`

The media wrapper, present in EVERY post regardless of type, is what caps media at 468px. :not(li *) skips a carousel's slide frame, whose <li> takes its width from it, so 100% makes both resolve to zero. :not(:has(ul)) skips a carousel's outer wrapper, where widening only adds empty space around the media; the scale rule below handles carousels and relies on this wrapper staying 468px.


## `main div[style*="min(470px"]:not([style*="--x-width"]):has(ul)`

Carousels are enlarged whole, which takes the inline translateX(n × 468px) slide offsets with them, so alignment is preserved without touching the offsets.

zoom, not transform: scale(). zoom reflows, so the wrapper genuinely occupies its new size and Instagram's own centering flex column centres it. scale() does not, and the extra height would have to be reserved by hand -- which cannot be done correctly, because a percentage margin resolves against WIDTH and so needs the aspect ratio, which is unknowable here (see the note at the top). zoom needs Firefox 126+; older builds drop the declaration and carousels stay at stock size.

The scale is a ratio of two lengths. CSS cannot divide by a length, so tan(atan2(a, b)) is used to get a/b unitless. (100% / 468px is rejected by Firefox.)

:not([style*="--x-width"]) excludes the post column, whose inline style also contains min(470px, 100vw) and which also :has(ul); without it the carousel would be enlarged twice.


## `main > div > div > .xw7yly9 > div`

Stories tray spans the full width.


## `article:not([role="dialog"] *) > .xdt5ytf:has(> div:nth-child(3))`

Two-column post: header full width, then media beside caption.

:has(> div:nth-child(3)) is the guard. A photo post has three children here (header, media, caption); a reel has two, because its header is overlaid on the video rather than given a row. Failing the guard is what keeps the nth-last-child rules off reels, which would otherwise count from the wrong end; reels are handled separately below. Nesting states the guard once so it cannot drift between rules.

Keep every declaration ABOVE the nested rules in each block. One placed after a nested rule needs CSSNestedDeclarations, Firefox 132+, past this style's floor of 126.


## `> div:nth-last-child(3)`

header row


## `> div:nth-last-child(2)`

media


## `> div:last-child`

caption


## `article:has(a[href*="/reels/"]):not([role="dialog"] *) > .xdt5ytf`

Reels have no header row -- it is overlaid on the video -- so the media/caption split is first-child / last-child instead.


## `article:has(a[href*="/reels/"]):not([role="dialog"] *) div[style*="padding-bottom"][style*="125%"]`

Feed reels: Instagram flattens anything taller than 4:5 into a 125% box and crops it with object-fit: cover (3:4 sources render at 125%, not their natural 133.33%), so 9:16 cannot be told from a genuine 4:5 here. Shallower ratios pass through at their true value -- 4:3 reels are 75% -- so capping the 125% boxes crops 9:16 a little further and leaves 4:3 untouched. The a[href*="/reels/"] guard on the article is what keeps this off same-ratio photo posts; the media element itself is not inspected.

One thing to know before moving a cap onto this element: max-width narrows the box without shortening it. The height is `padding-bottom: 125%`, and a percentage padding resolves against the CONTAINING BLOCK's width, not the element's own, so the height stays whatever the column gives it. Measured on the saved feed at a 1638px window, default settings: 550 wide by 898 tall. The height cap below is on the anchor for exactly this reason.


## `article:has(a[href*="/reels/"]):not([role="dialog"] *) a:has(div[style*="padding-bottom"][style*="125%"])`

The height cap goes on the anchor, never on the box above. For the reason just given, neither max-height nor max-width on that box shortens it: measured with the setting forced to 400px, the box's computed max-height was 400px and its rendered height stayed 898px, unchanged. Forcing box-sizing: border-box does not rescue it either -- a border box cannot shrink below its own padding. The declaration that used to sit there had never done anything.

Capping the anchor works because the anchor IS the containing block the 125% resolves against, so height/1.25 is the width that produces it. Measured: the cap at 400px/1.25 gave a box of 320 by 400.

Lowering this setting therefore changes the box's shape, not just its size: below about 690px the anchor becomes the binding constraint and the box returns to a true 125%, where above that it is 550 wide by whatever the column gives (898 at the default). How much of a flattened source that reveals or hides cannot be worked out from here -- per the note above, the box does not tell you the source's real ratio. At the 900px default the cap starts binding around a 1640px window, which is where the box first passes 900px tall anyway.

Only the 125% reels are capped. A 4:3 reel keeps its own 75% box, which needs a media column near 1200px before it reaches even the 900px default, and no snapshot of one exists to test a second divisor against. The :has() guard is what scopes this to the 125% case; an anchor wrapping any other ratio is left alone.

No !important: nothing sets max-width on this anchor -- Instagram computes max-width: none here, and the width: 100% rule below sets width only. Confirmed on the saved feed.


## Media (section header)

Images: Instagram reserves space with a `padding-bottom: <percent>` box and absolutely positions the image inside it with object-fit: cover. Collapsing the box and letting the image size itself removes both the crop and the letterboxing.

Video boxes are never collapsed. A <video preload="none"> has no intrinsic dimensions until its metadata loads, so a collapsed box gives it zero height, and with nothing rendered it never loads -- reels disappear entirely. They keep Instagram's box and are only re-fitted inside it.

Carousels are excluded throughout: their slides sit in an absolutely positioned overlay on an empty aspect-ratio spacer, so collapsing anything in that chain makes the slides vanish.

Modals are excluded too, by the same :not([role="dialog"] *) the two-column and feed-reel rules above carry. This section had been missing it. A post opened as a floating dialog -- clicking a post in the feed, or a /p/<id>/ URL reached from a profile grid -- renders as an <article> inside a [role="dialog"], so all four rules below reached it: the box was collapsed and the image was then capped by a FEED setting, on a page laid out by Instagram and never measured against these rules. Instagram sizes that media itself, with an inline `max-height:925px;max-width:925px;aspect-ratio:1/1` on an ancestor of the `padding-bottom:100%` box, so the 900px default was quietly undercutting Instagram's own cap.

The guard's reach was measured across all ten snapshots: it changes exactly one page, the saved /p/<id>/ modal, where the last two rules go from 1 match to 0. Nowhere else does an <article> sit inside a dialog -- the feed has four articles and no dialog, and the /reels/<id>/ page has a dialog and no article -- so no other page moves.

All four are guarded, not just the one carrying the height cap. They are one pipeline: collapsing the box is what makes the cap meaningful, so exempting the cap alone would leave the modal with a collapsed box around an uncapped image, which is worse than either state.


## `article:not([role="dialog"] *) img[aria-hidden="true"]`

blurred/black plate drawn behind non-filling media


## `article:not([role="dialog"] *) a:has(div[style*="padding-bottom"])`

Ads and reels wrap their media in a shrink-to-fit anchor. Left as-is, the anchor sizes from its contents while the contents size from the anchor, and the pair resolves to 0x0. Matching on any padding-bottom box catches both without depending on a generated class name.


## `@-moz-document regexp("https://www\\.instagram\\.com/(p|[^/]+/p|[^/]+/reel)/.*")`

Reels, on each of the three URLs where one gets a page of its own:

https://www.instagram.com/<user>/reel/<id>/ https://www.instagram.com/p/<id>/ https://www.instagram.com/<user>/p/<id>/

Those three render ONE layout, so the rules below are written once and reach all of them. Measured across three snapshots -- the same reel reached by both post-permalink paths, plus a different reel by a different user on /<user>/reel/<id>/ -- every selector count and every box agrees: no <article> and no [role="dialog"], one --x-maxWidth column at Instagram's stock min(100%, 673px), a 337x599.1 video in a `padding-bottom:177.778%` box, --media-info at its stock 335px, and zero carousel slides.

Scoped by URL, not by selector, for two separate reasons. The padding-bottom rule at the bottom would otherwise hit portrait reels in the feed. And the :root rule at the top would misfire there too: on the saved feed `main div[style*="--x-maxWidth"] video` matches 1, so an unscoped version would push --media-info across the whole feed -- which is the bug that moved this token out of the domain() block in the first place.

The pattern still excludes /reels/<id>/ (standalone, plural path) and /reel/<id>/ (the floating dialog opened from a /<user>/reels/ grid). Neither carries a `p` segment, and neither offers a <segment>/reel pair: /reel/<id>/ has nothing before `reel`, and /reels/<id>/ has no `reel` segment at all. Both get the feed rules above and nothing from here. That is deliberate -- the dialog is a modal with its own layout, which these rules, resizing a column and a full-height video box, would not transfer to unchanged, and the feed rules already exclude modals via :not([role="dialog"] *).

Carousels on the two /p/ paths belong to the post-permalink block BELOW, and the two blocks stay apart by their guards: everything here needs a <video> in the --x-maxWidth column, everything there needs the carousel's slide list. The one shape that could satisfy both is a MIXED carousel -- photo plus video slides -- on a /p/ URL. No snapshot of one exists, so nothing was written against it; what can be measured says it is harmless, and CHANGELOG.md records the reasoning.


## `:root:has(main div[style*="--x-maxWidth"] video)`

--media-info is Instagram's own token, so this is an override and !important is what wins the collision. Declared here rather than in the domain() block so that it reaches the three paths above and nothing else -- Instagram uses this token elsewhere, including post modals.

The :has() guard pairs this with the media column rule below, which fires only when the page holds a video. Widening the caption column is only safe when something widens the media to match: a carousel post reached through a /<user>/reel/<id>/ URL has no video, so the column rule missed while this one still took its 429px, leaving the carousel smaller than with the style switched off. Reported from the live site; all four post-page snapshots agree that the video guard scores zero on a carousel and one on a reel.

The guard is deliberately looser than the column rule's -- a descendant combinator rather than that rule's exact child chain -- because it only has to answer "is there a video in the media column", not "which element is the column".


## `main div[style*="--x-maxWidth"]:has(> div > div > div video)`

The reel column. Instagram writes --x-maxWidth inline as a value computed from the viewport, so the number differs between screens and zoom levels. Matching the property name with the descendant video as the guard survives that; matching the number would not.


## `main div[style*="padding-bottom"][style*="177"]`

9:16 reels, observed live on a reel page as `padding-bottom: 177.778%` -- note both the rounded value and the space after the colon, which is why only the leading digits are matched. The saved pages spell the same ratio without the space, which is the other half of why. "177" is deliberately loose; `main` is the guard that keeps it off unrelated elements whose style attribute happens to contain those digits.

It stays loose safely because the only 177 box on any of these pages is the reel itself: on all three snapshots `main [style*="177"]` matches exactly 1, and the "more posts" grid below the reel uses 133.333% boxes that this cannot touch. On the two carousel post pages it matches 0.


## `@-moz-document regexp("https://www\\.instagram\\.com/(p|[^/]+/p)/.*")`

Post permalink pages with URL https://www.instagram.com/p/<id>/ and https://www.instagram.com/<user>/p/<id>/

Both paths render the same layout. Two carousel snapshots, one of each path, agree on every selector count and on the whole height chain down to identical computed values, so one block covers both. A later pair of reel snapshots, again one of each path, agrees the same way -- see the reel block above, which is where a reel on these URLs is handled.

Nothing in the feed section reaches these pages: they carry no `min(470px` anywhere. The column is Instagram's own --x-maxWidth (stock `min(100%, 785px)`, the same token name the reel block above uses) and each slide frame carries an inline literal width, with the slide offsets written as multiples of it.

Widening the column does not enlarge anything by itself. Forcing --x-maxWidth larger widens the column and leaves the media at its original size, because the inline slide width is what governs; the extra space is empty. Overriding that slide width with a percentage instead collapses the media to zero, the same hazard the feed's `:not(li *)` guard exists for. zoom is the one lever that changes the media's size, and it carries the inline translateX offsets with it, so slide alignment survives.

So the column width below is not there to enlarge the media. It is there to make room for it: the media area is the column width minus the caption column, and once the caption is widened to match a reel page the stock 785px no longer fits a zoomed carousel.

Carousels and single photos, which are two different shapes handled by two separate groups of rules below. A reel on one of these URLs is not left stock either -- it is handled by the reel block above, whose URL pattern covers these two paths as well, because a reel here renders the same layout as /<user>/reel/<id>/ down to the pixel.

Three post shapes, then, sharing two URL patterns, and every rule in both blocks is kept in its own lane by a SELECTOR guard rather than by the URL: a carousel by its slide list, a reel by its video, a single photo by a photo box with neither of those present. Do not loosen one by guesswork; the whole point is that each boundary was measured against every snapshot.


## `:root:has(main div[style*="--x-maxWidth"] li[style*="translateX"])`

These pages lay out like a reel page: media and caption side by side inside one column. Stock, that column is 785px and splits 449 media + 335 caption.

Every rule in this block carries the same carousel guard, `:has(li[style*="translateX"])` -- the slide list only a carousel has. That is what keeps the pair together: widening the caption column is only safe when something widens the media to match, and the zoom rule below cannot match a single-media post. Without the guard, a reel on one of these URLs would take the wider caption column from HERE while the reel block above widened its media as well, and a single-media photo post would take it with nothing widening the media at all -- the second is exactly the bug fixed on reel pages above.


## `main div[style*="--x-maxWidth"]:has(li[style*="translateX"])`

The column has to hold the caption at its new width plus the zoomed media, so it needs its own setting rather than the reel page's --u-reel-width: at that variable's 950px default the media overflows its box by 152.5px, measured at the default scale. The media area comes out as the column width minus the caption width exactly -- 785 gives 356, 950 gives 521, 1200 gives 771 -- so the column needs at least caption + natural media width x scale. With the defaults that is 429 + 449 x 1.5 = 1102.5, and 1150 leaves a little slack.

Overshooting is not free either: the media stays the size zoom makes it, so surplus column width becomes empty space around the media, and because an aspect-ratio spacer sizes the container, surplus width becomes surplus HEIGHT too. At 1400 the container is 971x1293 around a 673x898 media.


## `main div[style*="--x-maxWidth"] > div > div:has(li[style*="translateX"])`

The media column holds the caption and the comments as well as the carousel, so zooming the column itself would scale the text and fight the text settings above -- a username box measured 18px before and 23.4px after. This selects the outermost element holding the media and nothing else: walking outward from the carousel's <ul>, every ancestor up to this one contains zero text characters, and its parent jumps to 2283.

`translateX` is matched rather than `transform:` because it sits after the colon, out of reach of the inline-style whitespace problem described at the top of this file.

The scale is a plain setting, not a computed fit. The feed's tan(atan2()) formula does not transfer: that one divides by a constant 468px because the feed wrapper is 468px wide whatever the media ratio, whereas here the slide width varies with the ratio, and CSS cannot read an element's own width to divide by it.

The two settings are coupled: raising this one needs the column width above raised with it, by the natural media width times the increase. The natural width varies with the post's aspect ratio -- 449px on the 3:4 post both snapshots contain -- so the pairing cannot be made automatic, and a squarer or landscape post, which starts wider, will want a wider column at the same scale. That is untested; no snapshot of one exists.

This selector must stay inside this URL block. It is not self-guarding: on a feed page it matches a 470x3644 region spanning many posts, and zooming that scales the feed's text with it -- measured at a username box of 18px going to 27px. The URL scoping, not the selector, is what keeps it off the feed.


## `main > div > div.xvc5jky:has(div[style*="padding-bottom"] > img):not(:has(li[style*="translateX"])):not(:has(video))`

Single photos, which Instagram lays out in TWO different ways depending on the media's shape. That, not any one size, is what makes them inconsistent with each other.

A portrait photo's column carries Instagram's .xf68679, whose `max-width: var(--x-maxWidth)` caps it: the 3:4 snapshot writes `--x-maxWidth:min(100%,785px)` inline and renders 449x599, the same numbers a carousel starts from. A square photo's column does not carry that class and has no inline token at all, so nothing caps it and it fills the content area -- 1262x1262 at a 1638px window, and wider on a wider screen. A landscape photo's column behaves like the square one: the 16:9 snapshot carries neither the class nor the token and renders 1262x712 in a 1598px column. All three shapes were measured on both paths, and as with carousels and reels the two paths agree to the pixel.

Landscape is the shape that wants NO correction. Uncapped is the right answer for it -- the media is already large and already the full width of the content area, and the height its own ratio gives it is modest. Only the two shapes that Instagram gets wrong are capped below: the portrait one because it comes out smaller than everything else on the page, the square one because it is unbounded. What the three had in common was the caption column, so that is what the rule above sets for all of them.

So --x-maxWidth is NOT the lever here, however well it works one block up. Setting it on the square page changes nothing at all: measured at 900px and at 1300px, the column's computed max-width stayed `none`, because the element that would read the token is missing the class that reads it. A plain max-width works on both capped shapes, and has the side benefit of adding no sixth design-token override.

No zoom either, unlike the carousel rule above. A single photo's `padding-bottom` box takes its width from the column, so the media is the column minus the caption, linearly -- measured at 900/1102/1150/1300 with the caption at 429, the media came out 470/672/721/964 wide. Nothing needs scaling and no aspect ratio is matched, so unlike the carousel settings the WIDTH is not calibrated against one ratio; the ratio is read only to decide whether the cap applies at all.

The default comes from 429 + 673 -- the caption column plus the width a carousel's media reaches at the default scale -- rounded down to 1100 because a range setting's default has to be a whole number of steps above its minimum, and 1102 is not one. Measured with the whole style applied at the defaults: square 670x670, 3:4 670x893, against the carousel's 674x898 and the reel's 520x855. Four to five pixels from a carousel on both axes, and identical to each other in width, which is the point. Landscape is deliberately outside that comparison at 1168x659, Instagram's own width less the widened caption.

Three guards, each load-bearing. `:has(div[style*="padding-bottom"] > img)` requires a photo box in this column. `:not(:has(li[style*="translateX"]))` excludes a carousel. `:not(:has(video))` excludes a reel, which this block's URL pattern also selects. Counted across all thirteen snapshots the three together match 1 on each of the five single-photo pages and 0 on every other page -- the feed, both carousels, both reels, /reels/<id>/, and the /p/<id>/ modal. That last zero is the one that matters: this block's URL pattern does select the modal, and every other rule here is kept off it only by a guard the modal happens to fail.

.xvc5jky is the post column's own class, carried by all three post shapes -- 1 on every post page, 0 on the feed, the modal and /reels/<id>/. Dropping it is not safe. Without it the guards also match the "more posts" grid below the post, and on a reel page that shrank a grid cell from 532x709 to 382x510. Its failure mode is the safe direction: if Instagram churns the class the rule stops applying and single photos return to stock.

--media-info is declared on the column rather than on :root for two separate reasons. The first is that `:root:has(...)` cannot express this guard at all -- :has() does not nest, so a :root selector wrapping these guards is invalid and Firefox drops the whole rule with no error. The second is that it does not need to: the column sits closer to the caption than Instagram's own declaration, which is on :root, and on every post snapshot each element under the column inherits a single value with nothing redeclaring it in between. !important is therefore insurance, not necessity -- the rule measured identical without it on the three single-photo pages that existed when it was written, but the snapshot's CSS is pruned and the live sheet may carry a declaration the snapshot dropped.

The caption column is set for every shape, landscape included; only the width cap below is withheld from landscape.


## `main > div > div.xvc5jky:has(div[style*="padding-bottom"] > img):not(:has(li[style*="translateX"])):not(:has(video)):has(div[style*="padding-bottom:1"] > img, div[style*="padding-bottom: 1"] > img)`

The width cap, for SQUARE AND PORTRAIT photos only.

A landscape photo gets no cap: Instagram's own layout for one is already good, and capping the column to a width chosen for a portrait post is what made it worse. The 16:9 snapshot measures 1262x712 stock in a 1598px column; capping the column to the 1100px default took it to 670x378 -- well under half the area, and short enough to leave the media sitting in a letterboxed band beside a taller caption. Square and portrait have the opposite problem and still need the cap: uncapped, the square post fills the content area at 1262x1262 and keeps growing with the window.

So the fourth guard selects "ratio at or above 100%". It reads the leading digit of the padding-bottom percentage, which separates the two cases: landscape is below 100% and always starts 5-9, while square, portrait and reel ratios are at or above 100% and all start with 1. Nothing Instagram accepts is tall enough to reach a leading 2, which is the only thing that would break the correspondence.

Measured across the snapshots, post media only -- the 133.333% boxes that appear on every post page are the "more posts" grid, not the post: landscape 56.4394%, square 100%, portrait 125% and 133.317/133.333%, reel 177.778%. So portrait goes at least to 3:4, not the 4:5 (125%) this note previously claimed as the ceiling. INFERENCE, NOT MEASURED: that landscape bottoms out at 1.91:1 (52.36%) and that nothing reaches 200% both come from Instagram's documented upload limits, not from any capture -- the widest thing ever measured here is 56.4394%. The guard does not depend on either bound being exact, only on the 100% boundary and on no accepted ratio reaching 200%.

Matching one digit rather than a whole percentage is the rule the top of this file states, and for the reason it states: a single saved feed carried 3:4 as 133.333%, 133.33333333333331% and 133.31719128329297%. Both spellings of the colon are listed because inline-style whitespace is unstable -- server-rendered markup writes `padding-bottom:56.4394%` and a React re-render rewrites it as `padding-bottom: 56.4394%`, on the same element, after navigating away and back. A comma inside one :has() is a list, not nesting, so this is valid where :root:has(...) of these guards would not be.

Measured across all thirteen snapshots: 1 on each of the three square and portrait post pages, 0 on the two landscape ones, 0 everywhere else. At the defaults, landscape 1168x659 in an uncapped 1598px column, square 670x670, 3:4 670x893 -- so the two shapes that were inconsistent with each other still come out identical in width, and landscape keeps Instagram's.

Failure mode is the safe direction, the same as .xvc5jky's: if the guard stops matching, a square photo returns to Instagram's stock layout rather than breaking.
