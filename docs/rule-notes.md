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

Width available to the media column, as a real length -- the carousel scale below is a unitless ratio, and CSS can only build one out of two lengths. The feed width has to be restated against the viewport because a percentage inside atan2() would not resolve, which is also why the 12px scrollbar allowance is a constant.

`100vw - 72px`, not `100vw`, since the nav-rail reservation below. The rail is fixed-positioned and takes no layout space, so nothing subtracts it automatically: the reservation takes it out of the feed's containing block by hand, and this restatement has to take it out by hand to match. Leave it at `100vw` and the estimate over-states the media column by up to 72px, scaling feed carousels larger than the space they have.


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

Hiding it is now a setting rather than unconditional, and the setting is a select whose two options are the two `display` values themselves -- `none` and `block` -- rather than a checkbox. A checkbox's value is `1` or `0`, and no property takes a number for "hidden", so a checkbox would have needed `/*[[...]]*/` preprocessor substitution, which nothing else in this style uses and which would leave the raw file unparseable at that spot for both verification scripts.

`block` is the measured stock value, not a guess. `.x6bx242` is one of Instagram's atomic classes, and it carries a single declaration: `width: var(--feed-sidebar-width)`. The element wearing it in the saved feed is `<div class="x1dr59a3 x13vifvy x7vhb2i x6bx242">`, and those three siblings are `height:100vh`, `top:0` and `padding-inline-start:64px` -- no `display` among them. With no stylesheet applied at all the element computes `display: block` (a `div`, and a flex item of its parent besides, so blockified either way). Measured in headless Firefox at 1638x900: stock `block`, Hidden `none`, Shown `block`, one match with 230 descendants.

The class is feed-only. It occurs twice in the saved feed -- once in Instagram's own CSS, once on that element -- and in none of the twelve other snapshots, which is why the rule sits in the `domain()` block with no URL scoping and needs no dialog guard: it is not keyed on `article`.

Because the rule is a single declaration on a named container, the two states cost nothing to compare. At the default, Hidden, the style is byte-for-byte equivalent in effect to the unconditional `display: none` it replaced: `verify.py` reports zero standard-property differences, and the only drift is `--u-feed-sidebar` itself, set and inherited on all 1668 elements and read by one. Flipped to Shown it moves 2913 standard properties, which is the rail and the reflow around it.


## `main > div:has(> div[style*="630px"]), main > div:has(> div[style*="max-width"])`

Reserves the left nav rail's 72px. The rail is a fixed-positioned sibling of the entire content wrapper -- `position:fixed; top:0; height:100vh; width:fit-content; z-index:10`, read out of the saved feed's own CSS -- so it takes no layout space at all and `main` begins at x=0. Instagram gets away with that because its own feed column is 630px and centred, and so never reaches the left 72px. Widen the feed and it slides underneath. The result is worse than cosmetic: the rail expands on hover, so a like button underneath it cannot be reached at all, because the pointer expands the rail before it arrives.

The selector is the feed-column rule below lifted one level, to that column's parent. It has the same reach -- 1 match on the saved feed, 0 on all thirteen other snapshots -- so the reservation cannot leak onto a post, reel or modal page.

Reserving the space on the parent rather than on the feed column is what makes everything downstream fall out for free. The `width: calc(var(--u-feed-width) * 1%)` below is a percentage of this element's content box, so every feed-width value is now measured against the window minus the rail, and Instagram's own `justify-content: center` centres the result inside that same free area instead of inside the window.

`box-sizing: border-box` is load-bearing, and this was measured rather than assumed. The element carries Instagram's `xh8yej3`, which is `width: 100%`; under the default `content-box` the padding is added to that 100% instead of taken out of it, so the feed shifts right by 72px and overflows the right edge by the same amount. Measured at a 1638px window: parent 1710 wide against a 1638 viewport, feed column x=236 right=1710.

`justify-content: safe center` covers the one case the padding does not. When `--u-feed-min` exceeds the free width the column overflows, and a centred flex item overflows in BOTH directions: at a 900px window with the minimum at its 1600px maximum, the column's left edge lands at x=-350 -- back under the rail and off the screen entirely. `safe` falls back to flush-start whenever the item overflows, which puts it at x=72. It needs Firefox 63, well under this style's 126 floor, and Firefox keeps the declaration: the parse census goes from 119 declarations to 122, the three this rule adds.

Measured on the saved feed at a 1638px window, feed width 100 and media column 100 -- the settings that exposed the problem: the column ran x=0 to 1638 before, x=72 to 1638 after. At the default 80 it is x=229 w=1253, against x=164 w=1310 before: narrower by the rail, centred in what is left.

72px is hard-coded rather than exposed as a setting, by choice. It appears twice -- here and in `--u-media-px` -- and both have to move together. RTL is not handled and was not checked; `padding-left` makes no claim about which side the rail takes there.


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

**Confirmed working live on 2026-09-11**, and worth recording because the post-page zoom rule removed on the same day was confirmed NOT to work. Moving the setting resizes feed carousels; above roughly 1.6 it stops doing anything, and between 1.5 and 1.6 the effect tapers. That is the clamp, not a fault: the scale is min(setting, fit ratio), so once the setting passes the ratio the ratio is what applies. The setting is a ceiling, which is what its label says.

WHY THIS ONE WORKS AND THE POST-PAGE ONE DID NOT. The two pages size a slide by completely different means, seen directly in live DevTools on 2026-09-11. On the FEED, the div inside each `li` carries `width: calc(-2px + min(470px, 100vw))` -- a static CSS expression, not a number anyone computed. It does not reference the container this rule zooms, so there is nothing for Instagram to re-derive: the slide is 468px whatever happens around it, and `zoom` simply scales the result. The offsets are literal px written by JS, `translateX(2339px)` and so on, but they are multiples of that same fixed 468, so they stay in step.

On a POST PAGE the same div carries `width:1262px` or `width:449px` -- a literal px that Instagram's JS derived FROM THE CONTAINER. The post-page rule widened that container via `--x-maxWidth`, so the slide was re-derived to fill it and the zoom cancelled out exactly.

An earlier version of this note explained the difference as "the feed rule leaves the container's layout width alone, so Instagram still derives 468px slides". The conclusion was right and the mechanism was wrong -- nothing is derived on the feed at all. It was marked as inference at the time; the DevTools capture replaced it.

WHY THE CEILING'S RANGE IS 1-6, AND MUST NOT BE NARROWED. The setting only binds when it is BELOW the fit ratio, and that ratio scales with the viewport and with --u-media-column and --u-feed-width. Measured on the saved feed with the ceiling lifted out of the way, so min() resolves to the fit ratio alone:

At the default --u-media-column 55 and --u-feed-width 80: 1.60 at a 1729px viewport, 2.00 at 2155px, 2.38 at 2560px, 3.00 at 3218px, 3.58 at 3840px.

With --u-media-column 90 and --u-feed-width 100: 3.05 at 1600px, 3.67 at 1920px, 4.90 at 2560px.

With both at 100: 3.67 at 1729px, 5.44 at 2560px.

So a ceiling of 2 would become the binding constraint past about 2155px at stock settings -- an ordinary 2560x1440 monitor is well past it -- and the former ceiling of 3 bound at 1729px once --u-media-column reached 100. It was raised to 6 on 2026-09-11 in the same pass that took --u-media-column's own maximum from 90 to 100, because that change is what put the ratio above 3 on an ordinary window. 6 covers roughly a 2820px viewport at those maxima; a 3840px one reaches about 8.2 and is still capped.

DO NOT justify the ceiling as protection against upscaling. An earlier version of this note did, on the reasoning that "the slide source is 468px wide" -- that was wrong, and is the kind of claim this file exists to stop. 468px is the LAYOUT BOX the feed gives a slide, not the resolution of the image in it. Instagram serves originals far larger, ON THE FEED: a carousel slide inspected live in DevTools on 2026-09-11 held a 3277x4096 image, in a 468px box. So a zoom well past 3 upscales nothing there. The saved feed cannot show this -- SingleFile rewrites every srcset into a data URI and headless Firefox decodes none of them, so every naturalWidth reads 0 -- which is why it took a live check.

What the ceiling is actually for is user preference: it is a "never enlarge by more than" guard, INERT by design whenever the fit ratio is the smaller term, which is why it can look like it does nothing on a narrower screen. That is not a fault to fix.

So the principle, for any zoom added here later: **check how the slide's width is written before reaching for zoom.** If it is a CSS expression, as on the feed, zoom scales it and nothing fights back. If it is a literal px derived from the container, as on a post page, then resizing that container makes Instagram recompute the slide and the zoom buys nothing. Both halves were measured live on 2026-09-11, the feed half by reading the attribute in DevTools.


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

One thing to know before moving a cap onto this element: max-width narrows the box without shortening it. The height is `padding-bottom: 125%`, and a percentage padding resolves against the CONTAINING BLOCK's width, not the element's own, so the height stays whatever the column gives it. Measured on the saved feed at a 1638px window, default settings: 550 wide by 858.8 tall, in an anchor 687 wide. (The 898 recorded here before 2026.9.11.5 was measured before the nav rail reservation narrowed the feed column.) Both caps below are on the anchor for exactly this reason -- the one that limits the box's height, and the one that stops it cropping the reel's sides.


## `article:has(a[href*="/reels/"]):not([role="dialog"] *) a:has(div[style*="padding-bottom"][style*="125%"])`

The height cap goes on the anchor, never on the box above. For the reason just given, neither max-height nor max-width on that box shortens it: measured with the setting forced to 400px, the box's computed max-height was 400px and its rendered height stayed 898px, unchanged. Forcing box-sizing: border-box does not rescue it either -- a border box cannot shrink below its own padding. The declaration that used to sit there had never done anything.

Capping the anchor works because the anchor IS the containing block the 125% resolves against, so height/1.25 is the width that produces it. Measured: the cap at 400px/1.25 gave a box of 320 by 400.

The second term of the min() is not a height cap at all. It is what keeps the box from cropping the reel LEFT AND RIGHT, and it is the reason the two settings cannot be read independently. Write F for "never let a reel get wider than" and A for the anchor's width: the box is `min(F, A)` wide and `1.25 x A` tall, and the video inside it is `object-fit: cover` filling the box (measured: computed object-fit cover, static position, filling the box's exact pixel size). Cover crops whichever axis the box is short on, so the sides go the moment the box is narrower in ratio than the source. A 9:16 reel needs the box to stay at or above 0.5625; lowering F alone narrows the box without shortening it, which is exactly how it falls through that floor.

Measured on the saved feed before this term existed, 1638px window, everything else default: F=550 gave 550x858.8, ratio 0.6405; F=470 gave 470x858.8, 0.5473; F=400 gave 400x858.8, 0.4658; F=300 gave 300x858.8, 0.3493. Everything from about 483px down was cutting the sides off a 9:16 reel.

Capping A at `F * 16 / 9 / 1.25` makes that impossible. Where A <= F the box is A wide and 1.25A tall, and 1.25 is already below 16/9; where A > F the box is F wide and the cap holds 1.25A at or under 1.7778F. The two constants are written unreduced because they are two separate facts: 16/9 is the tallest source a 125% box can hold, 1.25 is the box's own padding. The same measurements after: 550 unchanged at 0.6405, and 470, 400 and 300 giving 470x835.5, 400x711.1 and 300x533.3 -- all exactly 0.5625. Below the knee the reel is no longer cropped at all, on either axis.

The floor is 9:16 rather than 4:5 deliberately, and the difference is not measurable from the page. Per the note above, a 125% box holds a genuine 4:5 reel and a flattened 9:16 one indistinguishably, so the box cannot be made safe for both: a box taller than 4:5 reveals more of a 9:16 and side-crops a true 4:5, and only a true 125% box is safe for everything. The true-125% option was put to the user on 2026-09-11 with both trade-offs and declined -- it would cost the feature the style's own description leads with -- so a genuinely 4:5 reel is still side-cropped whenever the box is taller than 4:5, as it already was at the default. The floor is exact only while 9:16 is the tallest reel Instagram accepts; that comes from Instagram's upload limits and from every reel snapshot here being 177.778%, not from a capture of a taller one.

What the setting does, then, is change the box's shape and not just its size, in two stages: above the knee the box is F wide by whatever the column gives, and below it the box is F wide by a true 9:16. The height cap composes with it in either stage -- measured with both moved at once: F=550 H=400 gives 320x400 (a true 125%), F=300 H=400 gives 300x400, F=1200 H=300 gives 240x300, F=300 H=2000 gives 300x533.3. Whichever term binds, the ratio never goes below 0.5625.

This rule covers the 125% reels only. Everything else -- a landscape or square reel, whose box carries its true ratio -- is handled by the three rules below, which were added in 2026.9.11.6 after `Instagram_feed2.html` captured the first landscape reel. Until then neither setting reached one at all.

No !important: nothing sets max-width on this anchor -- Instagram computes max-width: none here, and the width: 100% rule below sets width only. Confirmed on the saved feed.


## `article:has(a[href*="/reels/"]):not([role="dialog"] *) a:has(div[style*="padding-bottom"]:not([style*="125%"]))`

The width cap for every feed reel that is NOT in a 125% box. Measured in `Instagram_feed2.html`, article 4 is a 16:9 reel at `padding-bottom:56.4263%`; with only the 125% rules in place it rendered 687x387.7 at a 1638px window, ignoring "never let a reel get wider than" entirely because neither of those rules matched it.

The cap goes on the anchor rather than the box for the reason given two sections up -- max-width narrows the box without shortening it -- but the arithmetic here is simpler than in the 125% case, and that is the whole point of splitting them. A 125% box may hold a source taller than 125%, so its width and its height have to be capped by separate terms. A non-125% box carries the source's TRUE ratio, so capping the anchor at F gives a box exactly F wide by F x ratio tall, with nothing for `object-fit: cover` to crop on either axis. Measured after, same reel: F=550 gives 550x310.3, F=400 gives 400x225.7, F=300 gives 300x169.3, all at ratio 0.5642 against the source's 0.5643.

`:not([style*="125%"])` rather than a positive match on the landscape ratios, because there is no list of those to match: 56.4263% is not even a round 16:9. The two spellings are exhaustive between them -- a reel box is either the flattened 125% one or its own ratio -- so the negation is what makes the pair total.

Both 125% reels in the same snapshot are unchanged by this rule at every setting swept: F of 550, 400, 300 and 1200 against H of 900 and 300, byte-identical before and after.


## `article:has(a[href*="/reels/"]):not([role="dialog"] *) div[style*="padding-bottom"]:not([style*="125%"])` (and its `> div` and `video`)

The height cap for the same reels, and the one rule in this file that CANNOT be checked against a snapshot as saved.

Why it is built differently from everything around it. The height of a percentage-padding box is `ratio x containing block width`, and CSS cannot read that ratio: it exists only as a substring of an inline style. For the 125% boxes the ratio is a known constant and the cap is just `H / 1.25`. For a landscape reel it is whatever Instagram wrote, so there is no divisor to write down. Confirmed that the obvious alternative does not exist: `max-height` on the box is inert, with and without `box-sizing: border-box` -- measured at 200px on the 56.4263% box, rendered height stayed 387.7px both ways, because a border box cannot shrink below its own padding.

So these three rules stop using the padding box as the ratio carrier and use the video's own intrinsic size instead, which is the same mechanism the feed photo rules below already use for `img`. The box gets `padding-bottom: 0` and `height: auto`; its one direct child, an absolutely positioned `inset: 0` overlay, is made static so the box has something in flow to take its height from; and the video gets `width: auto`, `height: auto`, `max-width: 100%` and `max-height: var(--u-media-max-height)`. With both dimensions auto, the replaced-element min/max algorithm satisfies both caps and preserves the ratio on its own -- no arithmetic in the style at all, and it is exact for any ratio rather than for an enumerated set.

`width: fit-content` on the box is not cosmetic. When the height cap binds, the video is narrower than the column, and without it the box stays column-width while the video centres inside it. The overlays Instagram positions against that box -- the progress bar and the mute button -- would then sit against the box's edges instead of the video's. Measured at F=1200 H=300 with a 16:9 source: without fit-content the box was 687x300 with the video 532.9x300 and the mute button 38px clear of the video's right edge; with it the box is 532.9x300, and the overlay and the button land exactly on the video.

Measured, all on article 4 of `Instagram_feed2.html` at a 1638px window, written as `box`/`video`: a 16:9 source at F=550 H=900 gives 550x309.6 with both caps slack on the height; F=550 H=200 gives a box of 355.3x200; F=1200 H=300 gives 532.9x300; F=300 H=900 gives 300x168.9. A 1:1 source at F=1200 H=300 gives 300x300, a 4:3 source at the same settings 400x300. Every one holds the source ratio to four decimals. The 125% reels in the same snapshot do not move.

**How those numbers were obtained, and what they do not prove.** SingleFile strips video sources, so `videoWidth` is 0 on every snapshot here and a rule keyed on intrinsic size measures nothing: applied to the snapshot as saved, the box collapses to 0x0. What was measured instead is the snapshot with a synthetic poster of known pixel size patched onto every `<video>` -- a `<video>` takes its intrinsic dimensions from its poster frame when no video data has loaded, so this exercises the real markup and the real cascade with a ratio we control. That proves the MECHANISM. It does not prove the two things only the live site can: that Instagram's poster and video agree with the `padding-bottom` it wrote alongside them, and that the poster is present early enough that the box is never briefly zero-height while the feed is scrolling. Both were flagged to the user for a live check on 2026-09-11; until that comes back, treat this rule as untested against Instagram rather than as measured.

The `:not([style*="125%"])` guard is what keeps all three off the portrait reels, which must keep their padding box -- the 125% cap depends on it.


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

Carousels and single photos, which are two different shapes handled by two separate groups of rules below. Each of those two shapes comes in turn in TWO layouts, and the split is the same one both times: Instagram gives a 3:4 post the class `.xf68679` and an inline `--x-maxWidth:min(100%,785px)` on its column, and gives a square post neither. So a square carousel is built like a square single photo, not like a 3:4 carousel, and the token every other rule in this block is guarded on is simply absent from it. A reel on one of these URLs is not left stock either -- it is handled by the reel block above, whose URL pattern covers these two paths as well, because a reel here renders the same layout as /<user>/reel/<id>/ down to the pixel.

Three post shapes, then, sharing two URL patterns, and every rule in both blocks is kept in its own lane by a SELECTOR guard rather than by the URL: a carousel by its slide list, a reel by its video, a single photo by a photo box with neither of those present. Do not loosen one by guesswork; the whole point is that each boundary was measured against every snapshot.


## `main > div > div.xvc5jky:has(li[style*="translateX"])`

The caption column, for EVERY carousel shape. These pages lay out like a reel page: media and caption side by side inside one column. Stock, a 3:4 column is 785px and splits 449 media + 335 caption; a square column is the whole content area and splits 1262 media + the same 335 caption.

The reader is one Instagram declaration, `.x4h1yfo { width: var(--media-info) }`, one match per post page. Instagram declares `--media-info` on `:root`, and `._aa4c`, its other declaring element, is not on the path between this container and `.x4h1yfo` -- measured on all three carousel snapshots. So a declaration HERE beats the inherited one on its own and needs no `!important`: importance only breaks ties within one element's cascade, and nothing else declares the token on this element. That is the form CLAUDE.md asks for, and it replaced a `:root:has(...) { ... !important }` rule that did the same job.

The replacement was measured rather than assumed: `scoped.py --diff` reports the two 3:4 carousels moving 712 and 735 CUSTOM properties and ZERO standard ones -- the token relocating from `:root` to the container with nothing rendering differently -- and zero changes of either kind on the other eleven snapshots.

Reselecting it this way fixed two things beyond the move. The old `:root` guard also matched the saved FEED, where `main div[style*="--x-maxWidth"]` is present; nothing reads `--media-info` there so it never rendered, but it was kept harmless only by the URL scoping, the same latent hazard the reel block's `:root` rule still has. And the old guard required `--x-maxWidth`, which a SQUARE carousel does not have, so the setting simply never reached one.

The guard is `:has(li[style*="translateX"])`, the slide list only a carousel has. Counted across all fourteen snapshots it matches 1 on each of the three carousel pages and 0 on every other -- the feed, both reels, all four single photos, /reels/<id>/, and the /p/<id>/ modal. That last zero matters for the same reason it does further down: this block's URL pattern does select the modal.

Why the guard has to stay: widening the caption column is only safe when the media is widened or scaled to match. Without it, a reel on one of these URLs would take the wider caption from HERE while the reel block above also widened its media, and a single-media photo post would take it with nothing compensating -- the second is exactly the bug fixed on reel pages above.


## `main > div > div.xvc5jky:not([style*="--x-maxWidth"]):has(li[style*="translateX"])`

The width cap, for SQUARE carousels only, and the counterpart of the single-photo cap at the bottom of this file. A square carousel's column carries no `--x-maxWidth`, so the token every other carousel rule in this block uses is not a lever here; `max-width` on the column is, exactly as it is for a square single photo. It reads `--u-post-photo-width` rather than `--u-post-width` for the same reason: the shape it is bringing into line is the square single photo, and the two should land on the same width.

The guard `:not([style*="--x-maxWidth"])` is on the element ITSELF, not `:not(:has(...))`. The token is an inline style on `.xvc5jky` directly -- the same element -- so a `:has()` spelling matches nothing and would silently cap the 3:4 carousels too, putting `--u-post-photo-width` in a fight with `--u-post-width`. Measured: the attribute form matches 1 on the square carousel and 0 on both 3:4 carousels.

Measured at the defaults on the square carousel snapshot, 1638px window: column 1598 -> 1150, caption 335 -> 380, media area 1263 -> 770. The square single photo lands at 770 from the same settings, which is the point.

KNOWN ARTIFACT, and do not try to "fix" it against a snapshot. Each slide frame carries an inline literal `width:<n>px` that Instagram's JS computed from the container AT LOAD, with the slide offsets written as multiples of it -- 1262 on this snapshot, against a stock media area of 1263. SingleFile freezes both. So on the saved page the cap narrows the container while the frozen slide stays 1262, and any measurement taken there reports the slide overflowing its 770px viewport by 493px. That number is an artifact of the capture, not a prediction. **Confirmed live on 2026-09-11**: with the style applied, the slides resize correctly at every value of `--u-post-photo-width` and each lands accurately in the frame. Instagram re-derives the slide width and the offsets from the container, exactly as it does for an unstyled page when the viewport is resized. So the cap alone is correct and complete here, and any offline measurement of this snapshot that reports an overflow is measuring the freeze, not the rule. Do not add machinery to "fix" it.

No zoom rule accompanies this cap, and none is needed: because Instagram re-derives the slide from the container, capping the container is the whole job. The 3:4 carousel had such a rule until 2026.9.11.4 and it turned out to do nothing live, so it was removed along with its setting -- this cap is now the pattern both carousel shapes follow. A `container-type: inline-size` + `tan(atan2())` version was built and measured before the live check and is NOT in the style: it hit a zoom/`cqw` feedback loop (0.63 computed where 0.61 was wanted) and, being a reconstruction of the very number the snapshot freezes, could not be validated by any offline test. It is recorded here so it is not attempted again.


## `main div[style*="--x-maxWidth"]:has(li[style*="translateX"])`

The column, and since 2026-09-11 the ONLY thing that sizes a 3:4 carousel's media. Instagram fills whatever media area the column leaves it, so the media comes out as the column width minus the caption column, exactly: measured at 785 -> 356, 950 -> 521, 1200 -> 771.

It needs its own setting rather than the reel page's --u-reel-width, whose 950px default leaves a 3:4 carousel narrower than intended. The 1150px default here is a picked compromise, not a derived number, and is the user's to set.

A `zoom` rule used to sit below this one, driven by a `--u-post-media-scale` setting, on the belief that widening the column alone left the media at its original size. That was an artifact of the saved page, where each slide's inline `width:<n>px` is frozen. Live, Instagram re-derives it, and the zoom changed nothing at all -- see the removal record under 2026.9.11.4 in CHANGELOG.md. Do not reintroduce one without a live measurement.

This rule and the caption rule above reach 3:4 carousels ONLY. A square carousel is built with no `--x-maxWidth` on its column at all, and is capped by `max-width` instead, one rule up. The two shapes are now handled the same way: cap the column, let Instagram fill what is left. A landscape carousel is untested and no snapshot of one exists.


## `main > div > div.xvc5jky:has(div[style*="padding-bottom"] > img):not(:has(li[style*="translateX"])):not(:has(video))`

Single photos, which Instagram lays out in TWO different ways depending on the media's shape. That, not any one size, is what makes them inconsistent with each other.

A portrait photo's column carries Instagram's .xf68679, whose `max-width: var(--x-maxWidth)` caps it: the 3:4 snapshot writes `--x-maxWidth:min(100%,785px)` inline and renders 449x599, the same numbers a carousel starts from. A square photo's column does not carry that class and has no inline token at all, so nothing caps it and it fills the content area -- 1262x1262 at a 1638px window, and wider on a wider screen. A landscape photo's column behaves like the square one: the 16:9 snapshot carries neither the class nor the token and renders 1262x712 in a 1598px column. All three shapes were measured on both paths, and as with carousels and reels the two paths agree to the pixel.

Landscape is the shape that wants NO correction. Uncapped is the right answer for it -- the media is already large and already the full width of the content area, and the height its own ratio gives it is modest. Only the two shapes that Instagram gets wrong are capped below: the portrait one because it comes out smaller than everything else on the page, the square one because it is unbounded. What the three had in common was the caption column, so that is what the rule above sets for all of them.

So --x-maxWidth is NOT the lever here, however well it works one block up. Setting it on the square page changes nothing at all: measured at 900px and at 1300px, the column's computed max-width stayed `none`, because the element that would read the token is missing the class that reads it. A plain max-width works on both capped shapes, and has the side benefit of adding no sixth design-token override.

No zoom either, unlike the carousel rule above. A single photo's `padding-bottom` box takes its width from the column, so the media is the column minus the caption, linearly -- measured at 900/1102/1150/1300 with the caption at 429, the media came out 470/672/721/964 wide. Nothing needs scaling and no aspect ratio is matched, so unlike the carousel settings the WIDTH is not calibrated against one ratio; the ratio is read only to decide whether the cap applies at all.

What the cap is for is bringing the two shapes to the same width; the default is a picked compromise, not a derived number, and any value is the user's to set. Measured with the whole style applied and this setting at 1100, the default at the time: square 670x670, 3:4 670x893, against the carousel's 674x898 and the reel's 520x855. Four to five pixels from a carousel on both axes, and identical to each other in width, which is the point. Landscape is deliberately outside that comparison at 1168x659, Instagram's own width less the widened caption.

Three guards, each load-bearing. `:has(div[style*="padding-bottom"] > img)` requires a photo box in this column. `:not(:has(li[style*="translateX"]))` excludes a carousel. `:not(:has(video))` excludes a reel, which this block's URL pattern also selects. Counted across all thirteen snapshots the three together match 1 on each of the five single-photo pages and 0 on every other page -- the feed, both carousels, both reels, /reels/<id>/, and the /p/<id>/ modal. That last zero is the one that matters: this block's URL pattern does select the modal, and every other rule here is kept off it only by a guard the modal happens to fail.

.xvc5jky is the post column's own class, carried by all three post shapes -- 1 on every post page, 0 on the feed, the modal and /reels/<id>/. Dropping it is not safe. Without it the guards also match the "more posts" grid below the post, and on a reel page that shrank a grid cell from 532x709 to 382x510. Its failure mode is the safe direction: if Instagram churns the class the rule stops applying and single photos return to stock.

--media-info is declared on the column rather than on :root for two separate reasons. The first is that `:root:has(...)` cannot express this guard at all -- :has() does not nest, so a :root selector wrapping these guards is invalid and Firefox drops the whole rule with no error. The second is that it does not need to: the column sits closer to the caption than Instagram's own declaration, which is on :root, and on every post snapshot each element under the column inherits a single value with nothing redeclaring it in between. !important is therefore insurance, not necessity -- the rule measured identical without it on the three single-photo pages that existed when it was written, but the snapshot's CSS is pruned and the live sheet may carry a declaration the snapshot dropped.

The caption column is set for every shape, landscape included; only the width cap below is withheld from landscape.


## `main > div > div.xvc5jky:has(div[style*="padding-bottom"] > img):not(:has(li[style*="translateX"])):not(:has(video)):has(div[style*="padding-bottom:1"] > img, div[style*="padding-bottom: 1"] > img)`

The width cap, for SQUARE AND PORTRAIT photos only.

A landscape photo gets no cap: Instagram's own layout for one is already good, and capping the column to a width chosen for a portrait post is what made it worse. The 16:9 snapshot measures 1262x712 stock in a 1598px column; capping the column to 1100px took it to 670x378 -- well under half the area, and short enough to leave the media sitting in a letterboxed band beside a taller caption. Square and portrait have the opposite problem and still need the cap: uncapped, the square post fills the content area at 1262x1262 and keeps growing with the window.

So the fourth guard selects "ratio at or above 100%". It reads the leading digit of the padding-bottom percentage, which separates the two cases: landscape is below 100% and always starts 5-9, while square, portrait and reel ratios are at or above 100% and all start with 1. Nothing Instagram accepts is tall enough to reach a leading 2, which is the only thing that would break the correspondence.

Measured across the snapshots, post media only -- the 133.333% boxes that appear on every post page are the "more posts" grid, not the post: landscape 56.4394%, square 100%, portrait 125% and 133.317/133.333%, reel 177.778%. So portrait goes at least to 3:4, not the 4:5 (125%) this note previously claimed as the ceiling. INFERENCE, NOT MEASURED: that landscape bottoms out at 1.91:1 (52.36%) and that nothing reaches 200% both come from Instagram's documented upload limits, not from any capture -- the widest thing ever measured here is 56.4394%. The guard does not depend on either bound being exact, only on the 100% boundary and on no accepted ratio reaching 200%.

Matching one digit rather than a whole percentage is the rule the top of this file states, and for the reason it states: a single saved feed carried 3:4 as 133.333%, 133.33333333333331% and 133.31719128329297%. Both spellings of the colon are listed because inline-style whitespace is unstable -- server-rendered markup writes `padding-bottom:56.4394%` and a React re-render rewrites it as `padding-bottom: 56.4394%`, on the same element, after navigating away and back. A comma inside one :has() is a list, not nesting, so this is valid where :root:has(...) of these guards would not be.

Measured across all thirteen snapshots: 1 on each of the three square and portrait post pages, 0 on the two landscape ones, 0 everywhere else. At the defaults, landscape 1168x659 in an uncapped 1598px column, square 670x670, 3:4 670x893 -- so the two shapes that were inconsistent with each other still come out identical in width, and landscape keeps Instagram's.

Failure mode is the safe direction, the same as .xvc5jky's: if the guard stops matching, a square photo returns to Instagram's stock layout rather than breaking.
