# Rule notes — the `domain()` block

The site-wide block: `@-moz-document domain("www.instagram.com")`. It owns the feed and anything else not on a post permalink, and it is keyed on `article` and the inline `min(470px` column.

Read `docs/rule-notes.md` first — it carries the whole-file inline-style rule and the `:root` notes that every rule here depends on, and the index of all three files. The post and reel pages are in `docs/rule-notes-post.md`.

**Every rule here keyed on `article` needs `:not([role="dialog"] *)`.** That is a Hard rule in `CLAUDE.md`, not a style preference — a post opened as a floating modal is an `<article>` inside a `[role="dialog"]` and picks up every unguarded rule.

Sections are in the order the rules appear in the style. A heading of *(section header)* is a block comment that introduces a group of rules rather than a single one.

---

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

The selector is the feed-column rule below lifted one level, to that column's parent. It has the same reach -- 1 match on each saved feed, 0 on all nineteen other snapshots -- so the reservation cannot leak onto a post, reel or modal page.

Reserving the space on the parent rather than on the feed column is what makes everything downstream fall out for free. The `width: calc(var(--u-feed-width) * 1%)` below is a percentage of this element's content box, so every feed-width value is now measured against the window minus the rail, and Instagram's own `justify-content: center` centres the result inside that same free area instead of inside the window.

`box-sizing: border-box` is load-bearing, and this was measured rather than assumed. The element carries Instagram's `xh8yej3`, which is `width: 100%`; under the default `content-box` the padding is added to that 100% instead of taken out of it, so the feed shifts right by 72px and overflows the right edge by the same amount. Measured at a 1638px window: parent 1710 wide against a 1638 viewport, feed column x=236 right=1710.

`justify-content: safe center` covers the one case the padding does not. When `--u-feed-min` exceeds the free width the column overflows, and a centred flex item overflows in BOTH directions: at a 900px window with the minimum at its 1600px maximum, the column's left edge lands at x=-350 -- back under the rail and off the screen entirely. `safe` falls back to flush-start whenever the item overflows, which puts it at x=72. It needs Firefox 63, well under this style's 126 floor, and Firefox keeps the declaration: the parse census goes from 119 declarations to 122, the three this rule adds.

Measured on the saved feed at a 1638px window, feed width 100 and media column 100 -- the settings that exposed the problem: the column ran x=0 to 1638 before, x=72 to 1638 after. At a feed width of 80 it is x=229 w=1253, against x=164 w=1310 before: narrower by the rail, centred in what is left. That 80 was the default when this was measured; **the default has been 90 since 2026-09-14**, so the numbers here describe a narrower feed than a fresh install now gets. The shape of the result is what matters and does not change with the setting.

72px is hard-coded rather than exposed as a setting, by choice. It appears twice -- here and in `--u-media-px` -- and both have to move together. RTL is not handled and was not checked; `padding-left` makes no claim about which side the rail takes there.


## `main > div > div[style*="630px"], main > div > div[style*="max-width"]`

The feed column. max-width is not a cap -- it exists solely to defeat the inline max-width Instagram sets on this element. The width above is what governs.


## `main [style*="--x-width"][style*="470px"], .xmnaoh6 + div > div`

Post column inside the feed column.


## `main div[style*="min(470px"]:not(li *):not(:has(ul))`

The media wrapper, present in EVERY post regardless of type, is what caps media at 468px. :not(li *) skips a carousel's slide frame, whose <li> takes its width from it, so 100% makes both resolve to zero. :not(:has(ul)) skips a carousel's outer wrapper, where widening only adds empty space around the media; the scale rule below handles carousels and relies on this wrapper staying 468px.

`min-width: min(468px, var(--u-media-px))` is a floor rather than a size, and it exists to stop this rule collapsing the column to zero. Reported live on 2026-09-21: after viewing stories from the feed and returning, carousels went blank and stayed blank. Scrolling them out of view and back was the only thing that restored them, and disabling the style stopped it happening at all.

The `width: 100%` above resolves against this wrapper's parent, which is a shrink-to-fit flex item. With the slide list unmounted the parent has nothing else sizing it, so the percentage is circular and both resolve to ZERO, taking the whole subtree below with them. This is the same failure `:not(li *)` already documents one level down -- "100% makes both resolve to zero" -- and `:not(:has(ul))` only holds it off for as long as Instagram keeps the `<ul>` mounted. Feed virtualization unmounts it when you navigate away to stories, which drops the wrapper into exactly the state the guard was never meant to cover.

Measured live in the blank state: the wrapper carries its inline `width: calc(-2px + min(470px, 100vw))`, so 468px, and computes `0px`, with the column at `775x2` and no img, video or ul inside it. Reproduced offline by deleting the `<ul>` from a saved carousel, which collapses the column to `769x2` with the wrapper at `0px` -- the same state, and a deterministic test case that needs no stories round trip.

Why it never recovers on its own is NOT established. The plausible reading is that a zero-height column never re-enters whatever threshold the virtualiser mounts on, so the collapse is self-sustaining -- but that is INFERENCE. What is measured is only that a scroll out and back, which forces a fresh mount, is what clears it.

The floor is built from `--u-media-px` rather than a flat 468px because a flat floor would overflow a narrow media column. `min()` means it can never exceed the column it sits in: at the default settings and a 1638px window it is 468px, which is the width this rule caps media to anyway, so it is inert; at the minimum `--u-media-column` of 20 it drops to about 270px at that same window, and to 68px at the minimum `--u-feed-min`. It tracks the column down wherever the column is narrow and does nothing wherever the column is already wide enough.

REMOVED CANDIDATE. An earlier attempt applied `width: 100%` in BOTH states instead, on the theory that removing the flip would remove the problem. Do not write this back: it makes every carousel hit the zero-width collapse the instant it loads, with no recovery at all. Tried live on 2026-09-21 and strictly worse than the bug it was meant to fix.

Verified on 2026-09-21 against all nineteen snapshots, each at its own URL, via `scoped.py`'s computed-property diff. Only the three feed captures change; every post, reel and modal capture is identical in every computed property, `Instagram-p-id-modal(single_photo).html` included. On the feeds the change is the declaration itself plus repair -- `Instagram_feed1.html` and `Instagram_feed2.html` show wrappers going `width: 0px -> 468px`, and `Instagram_feed3.html` gains 270px of height because that capture already contained an unmounted post whose column had collapsed. Nothing in the diff touches font-size, line-height or zoom.


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

At `--u-media-column` 55 and `--u-feed-width` 80: 1.60 at a 1729px viewport, 2.00 at 2155px, 2.38 at 2560px, 3.00 at 3218px, 3.58 at 3840px. Both were the defaults when this was measured; `--u-media-column` still is, but **`--u-feed-width` has defaulted to 90 since 2026-09-14**, which widens the feed and so reaches each of these ratios at a smaller viewport than the table says. Not re-measured.

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

One thing to know before moving a cap onto this element: max-width narrows the box without shortening it. The height is `padding-bottom: 125%`, and a percentage padding resolves against the CONTAINING BLOCK's width, not the element's own, so the height stays whatever the column gives it. Measured on the saved feed at a 1638px window, with the settings at the defaults of the day: 550 wide by 858.8 tall, in an anchor 687 wide. Both inputs have since moved: `--u-feed-reel-width` was 550 and is **600 since 2026-09-17**, and the 687 follows from `--u-feed-width` 80, **90 since 2026-09-14**. So a fresh install now gets a wider anchor and a wider, taller box than these numbers show. Not re-measured. (The 898 recorded here before 2026.9.11.5 was measured before the nav rail reservation narrowed the feed column.) Both caps below are on the anchor for exactly this reason -- the one that limits the box's height, and the one that stops it cropping the reel's sides.


## `article:has(a[href*="/reels/"]):not([role="dialog"] *) a:has(div[style*="padding-bottom"][style*="125%"])`

The height cap goes on the anchor, never on the box above. For the reason just given, neither max-height nor max-width on that box shortens it: measured with the setting forced to 400px, the box's computed max-height was 400px and its rendered height stayed 898px, unchanged. Forcing box-sizing: border-box does not rescue it either -- a border box cannot shrink below its own padding. The declaration that used to sit there had never done anything.

Capping the anchor works because the anchor IS the containing block the 125% resolves against, so height/1.25 is the width that produces it. Measured: the cap at 400px/1.25 gave a box of 320 by 400.

The second term of the min() is not a height cap at all. It is what keeps the box from cropping the reel LEFT AND RIGHT, and it is the reason the two settings cannot be read independently. Write F for "never let a reel get wider than" and A for the anchor's width: the box is `min(F, A)` wide and `1.25 x A` tall, and the video inside it is `object-fit: cover` filling the box (measured: computed object-fit cover, static position, filling the box's exact pixel size). Cover crops whichever axis the box is short on, so the sides go the moment the box is narrower in ratio than the source. A 9:16 reel needs the box to stay at or above 0.5625; lowering F alone narrows the box without shortening it, which is exactly how it falls through that floor.

Measured on the saved feed before this term existed, 1638px window, everything else default: F=550 gave 550x858.8, ratio 0.6405; F=470 gave 470x858.8, 0.5473; F=400 gave 400x858.8, 0.4658; F=300 gave 300x858.8, 0.3493. Everything from about 483px down was cutting the sides off a 9:16 reel.

Capping A at `F * 16 / 9 / 1.25` makes that impossible. Where A <= F the box is A wide and 1.25A tall, and 1.25 is already below 16/9; where A > F the box is F wide and the cap holds 1.25A at or under 1.7778F. The two constants are written unreduced because they are two separate facts: 16/9 is the tallest source a 125% box can hold, 1.25 is the box's own padding. The same measurements after: 550 unchanged at 0.6405, and 470, 400 and 300 giving 470x835.5, 400x711.1 and 300x533.3 -- all exactly 0.5625. Below the knee the reel is no longer cropped at all, on either axis.

The floor is 9:16 rather than 4:5 deliberately, and the difference is not measurable from the page. Per the note above, a 125% box holds a genuine 4:5 reel and a flattened 9:16 one indistinguishably, so the box cannot be made safe for both: a box taller than 4:5 reveals more of a 9:16 and side-crops a true 4:5, and only a true 125% box is safe for everything. The true-125% option was put to the user on 2026-09-11 with both trade-offs and declined -- it would cost the feature the style's own description leads with -- so a genuinely 4:5 reel is still side-cropped whenever the box is taller than 4:5, as it already was at the default. The floor is exact only while 9:16 is the tallest reel Instagram accepts; that comes from Instagram's upload limits and from every reel snapshot here being 177.778%, not from a capture of a taller one.

**2026-09-14: the shape this actually costs is 3:4, not 4:5.** The user wrote the original limitation while taking 3:4 for 4:5, and has since seen a creator posting consistently in 3:4; no genuinely 4:5 video has ever been confirmed. It changes none of the reasoning above -- 3:4 is flattened into the same 125% box, so it is indistinguishable from 9:16 in exactly the same way -- but it makes the cost concrete rather than hypothetical. Past the knee the box is a true 9:16, so a 3:4 source loses `1 - 1.3333 / 1.7778` = 25% of its width; against the box measured above, 550x858.8, it scales to 644.1 wide to cover the box and loses 94.1px, about 15%. So the crop is present at the defaults and the setting decides its size. Per that note, the box was measured when `--u-feed-reel-width` defaulted to 550 and `--u-feed-width` to 80, against today's 600 and 90, so treat the 15% as the shape of the cost rather than its current size. `object-fit: contain` on the box's video would trade that crop for banding on both shapes without needing to tell them apart; it was put to the user with these numbers on 2026-09-14 and declined.

What the setting does, then, is change the box's shape and not just its size, in two stages: above the knee the box is F wide by whatever the column gives, and below it the box is F wide by a true 9:16. The height cap composes with it in either stage -- measured with both moved at once: F=550 H=400 gives 320x400 (a true 125%), F=300 H=400 gives 300x400, F=1200 H=300 gives 240x300, F=300 H=2000 gives 300x533.3. Whichever term binds, the ratio never goes below 0.5625.

This rule covers the 125% reels only. Everything else -- a landscape or square reel, whose box carries its true ratio -- is handled by the three rules below, which were added in 2026.9.11.6 after `Instagram_feed2.html` captured the first landscape reel. Until then neither setting reached one at all.

No !important: nothing sets max-width on this anchor -- Instagram computes max-width: none here, and the width: 100% rule below sets width only. Confirmed on the saved feed.


## `article:has(a[href*="/reels/"]):not([role="dialog"] *) a:has(div[style*="padding-bottom"]:not([style*="125%"]))` (removed 2026-09-14)

**The width cap for every feed reel that is NOT in a 125% box. Removed so that the width setting governs portrait reels only**, on the user's instruction: the setting was labelled "Feed: maximum width of reel" while reaching both families, and it was relabelled "Feed: maximum width of portrait reel" and narrowed to match rather than the label being widened. What it set was `max-width: var(--u-feed-reel-width)` plus `margin-inline: auto` on the anchor. The two rules below it are NOT removed -- a landscape reel still collapses its padding box and still sizes from the video's own intrinsic dimensions under the height cap.

What a landscape reel does now, with only those two rules: it takes `max-width: 100%` of the anchor, and the anchor is `width: 100%` from the ads-and-reels rule further down, so it fills the media column instead of stopping at the setting. Measured on `Instagram_feed2.html` at a 1638px window, defaults: the anchor goes 550 -> 687.017 wide, its `max-width` 550px -> none, and its auto margins 68.5 -> 0. Thirty-eight computed properties move in total, across the anchor and six descendants that were being constrained by it; no `font-size`, `line-height` or `zoom` is among them, and the 125% reels do not move. The media column percentage and the height setting are what bound a landscape reel from here.

**The measurements from when it existed are kept below, because they are what to re-measure against if it is ever written back.** It was added in 2026.9.11.6 after `Instagram_feed2.html` captured the first landscape reel; before it, article 4 -- a 16:9 reel at `padding-bottom:56.4263%` -- rendered 687x387.7 at a 1638px window and ignored the width setting entirely, because neither 125% rule matched it. That is the same 687.017 the reel returns to now, so the removal puts landscape reels back exactly where 2026.9.11.6 found them, with the height cap and the box collapse that release also added still in place.

The cap went on the anchor rather than the box for the reason given two sections up -- max-width narrows the box without shortening it -- but the arithmetic was simpler than in the 125% case, and that was the whole point of splitting them. A 125% box may hold a source taller than 125%, so its width and its height have to be capped by separate terms. A non-125% box carries the source's TRUE ratio, so capping the anchor at F gave a box exactly F wide by F x ratio tall, with nothing for `object-fit: cover` to crop on either axis. Measured while it existed, same reel: F=550 gave 550x310.3, F=400 gave 400x225.7, F=300 gave 300x169.3, all at ratio 0.5642 against the source's 0.5643.

`:not([style*="125%"])` rather than a positive match on the landscape ratios, because there is no list of those to match: 56.4263% is not even a round 16:9. The two spellings are exhaustive between them -- a reel box is either the flattened 125% one or its own ratio -- so the negation is what made the pair total. That negation still shapes the two rules below, which is why the reasoning stays here rather than going to `docs/removed.md` with the rest.

Both 125% reels in the same snapshot were unchanged by this rule at every setting swept: F of 550, 400, 300 and 1200 against H of 900 and 300, byte-identical before and after. That is the converse confirmation that the rule only ever touched the one landscape reel, and it is why removing it moves exactly one anchor.

## `article:has(a[href*="/reels/"]):not([role="dialog"] *) div[style*="padding-bottom"]:not([style*="125%"])` (and its `> div` and `video`)

The height cap for the same reels, and the one rule in this file that CANNOT be checked against a snapshot as saved.

Why it is built differently from everything around it. The height of a percentage-padding box is `ratio x containing block width`, and CSS cannot read that ratio: it exists only as a substring of an inline style. For the 125% boxes the ratio is a known constant and the cap is just `H / 1.25`. For a landscape reel it is whatever Instagram wrote, so there is no divisor to write down. Confirmed that the obvious alternative does not exist: `max-height` on the box is inert, with and without `box-sizing: border-box` -- measured at 200px on the 56.4263% box, rendered height stayed 387.7px both ways, because a border box cannot shrink below its own padding.

So these three rules stop using the padding box as the ratio carrier and use the video's own intrinsic size instead, which is the same mechanism the feed photo rules below already use for `img`. The box gets `padding-bottom: 0` and `height: auto`; its one direct child, an absolutely positioned `inset: 0` overlay, is made static so the box has something in flow to take its height from; and the video gets `width: auto`, `height: auto`, `max-width: 100%` and `max-height: var(--u-media-max-height)`. With both dimensions auto, the replaced-element min/max algorithm satisfies both caps and preserves the ratio on its own -- no arithmetic in the style at all, and it is exact for any ratio rather than for an enumerated set.

`width: fit-content` on the box is not cosmetic. When the height cap binds, the video is narrower than the column, and without it the box stays column-width while the video centres inside it. The overlays Instagram positions against that box -- the progress bar and the mute button -- would then sit against the box's edges instead of the video's. Measured at F=1200 H=300 with a 16:9 source: without fit-content the box was 687x300 with the video 532.9x300 and the mute button 38px clear of the video's right edge; with it the box is 532.9x300, and the overlay and the button land exactly on the video.

Measured, all on article 4 of `Instagram_feed2.html` at a 1638px window, written as `box`/`video`: a 16:9 source at F=550 H=900 gives 550x309.6 with both caps slack on the height; F=550 H=200 gives a box of 355.3x200; F=1200 H=300 gives 532.9x300; F=300 H=900 gives 300x168.9. A 1:1 source at F=1200 H=300 gives 300x300, a 4:3 source at the same settings 400x300. Every one holds the source ratio to four decimals. The 125% reels in the same snapshot do not move.

**How those numbers were obtained, and what they do not prove.** SingleFile strips video sources AND replaces the poster with `data:,`, so `videoWidth` is 0 on every snapshot here and a rule keyed on intrinsic size has nothing to read: applied to `Instagram_feed2.html` as saved, the landscape reel renders **300x150** -- the CSS default object size for a replaced element with no intrinsic dimensions, not a collapse to zero. That number is the signature to recognise; it is the snapshot's missing poster, not the rule misbehaving. What was measured instead is the snapshot with a synthetic poster of known pixel size patched onto every `<video>` -- a `<video>` takes its intrinsic dimensions from its poster frame when no video data has loaded, so this exercises the real markup and the real cascade with a ratio we control. That proves the MECHANISM, and nothing beyond it. Two things only the live site could settle: whether Instagram's poster and video agree with the `padding-bottom` it writes alongside them, and whether the poster is present early enough that the reel is never briefly drawn at the 300x150 fallback while the feed scrolls.

**Both were confirmed live on 2026-09-11.** The user checked the feed and reported a 4:3 reel at `padding-bottom: 75%` and a 16:9 reel at `padding-bottom: 56.25%` both rendering correctly, with no 300x150 anywhere. So Instagram's poster does carry the same ratio as the padding it writes, and it is in place early enough not to flash the fallback. Two distinct landscape ratios, and note that neither is the 56.4263% the snapshot holds -- 56.25% is the round 16:9 -- so the rule is confirmed against ratios it was never tuned to. What remains untested is a live reel shallower than 4:3 or between these two, which nothing suggests is any different: the rule reads no ratio and contains no arithmetic, so there is no boundary in it for such a reel to fall the wrong side of.

The 300x150 fallback still belongs in this note as the signature to recognise, because it is what an offline measurement of this rule will always report.

The 125% guard is what keeps all three off the portrait reels, which must keep their padding box -- the 125% cap depends on it. It is spelled `:not([style*="padding-bottom:125%"]):not([style*="padding-bottom: 125%"])` rather than the bare `:not([style*="125%"])` it was written as until 2026.9.12.1, and the two spellings are not equivalent: a bare substring test matches anywhere in the attribute, and `padding-bottom:68.125%` -- a value observed on a photo in `Instagram_feed2.html`, exactly `109/160` -- contains `125%`. A reel at that ratio was therefore classified portrait, capped by arithmetic against 1.25 and cropped by `object-fit: cover`, while being excluded from the rules here that would have sized it correctly.

Anchoring to the property name and the whole value fixes both halves at once, and the trailing `%` stops it swallowing `125.5%`. Matching the whole value is safe here, and is the deliberate exception to the standing rule against it, because `125%` is not a computed ratio: it is the constant Instagram clamps anything taller than 4:5 to. Across all twenty-one snapshots the round values occur only as the bare `75%`, `100%` and `125%`; every computed value carries decimals -- the 4:3 carousel added on 2026-09-12 carries `75%` and `74.9712%` side by side on the same page, which is the pattern in miniature, and one of the landscape reels captured the same day is a bare `75%` too. Verified on the landscape reel's box in `Instagram_feed2.html` by substituting values and reading back which selectors matched: `68.125%`, `56.2696%`, `75%`, `100%` and `125.5%` all classify landscape, `125%` in both spacings classifies portrait.


## Media (section header)

Images: Instagram reserves space with a `padding-bottom: <percent>` box and absolutely positions the image inside it with object-fit: cover. Collapsing the box and letting the image size itself removes both the crop and the letterboxing.

Video boxes are never collapsed. A <video preload="none"> has no intrinsic dimensions until its metadata loads, so a collapsed box gives it zero height, and with nothing rendered it never loads -- reels disappear entirely. They keep Instagram's box and are only re-fitted inside it.

Carousels are excluded throughout: their slides sit in an absolutely positioned overlay on an empty aspect-ratio spacer, so collapsing anything in that chain makes the slides vanish. That exclusion is what the height setting's label names: until 2026-09-14 it read "Feed: maximum height of media", which the user reported as misleading because a carousel does not respond to it, and it now reads "Feed: maximum height of a single photo or reel". The reels half comes from the `a[href*="/reels/"]` guard on the rules above; the photo half from the `:not(li *)` here. Do not widen the label back to "media" -- the scope is deliberate, and feed carousels have their own size lever in the carousel scale setting.

Modals are excluded too, by the same :not([role="dialog"] *) the two-column and feed-reel rules above carry. This section had been missing it. A post opened as a floating dialog -- clicking a post in the feed, or a /p/<id>/ URL reached from a profile grid -- renders as an <article> inside a [role="dialog"], so all four rules below reached it: the box was collapsed and the image was then capped by a FEED setting, on a page laid out by Instagram and never measured against these rules. Instagram sizes that media itself, with an inline `max-height:925px;max-width:925px;aspect-ratio:1/1` on an ancestor of the `padding-bottom:100%` box, so the 900px default was quietly undercutting Instagram's own cap.

The guard's reach was measured across all ten snapshots: it changes exactly one page, the saved /p/<id>/ modal, where the last two rules go from 1 match to 0. Nowhere else does an <article> sit inside a dialog -- the feed has four articles and no dialog, and the /reels/<id>/ page has a dialog and no article -- so no other page moves.

All four are guarded, not just the one carrying the height cap. They are one pipeline: collapsing the box is what makes the cap meaningful, so exempting the cap alone would leave the modal with a collapsed box around an uncapped image, which is worse than either state.


## `article:not([role="dialog"] *) img[aria-hidden="true"]`

blurred/black plate drawn behind non-filling media


## `article:not([role="dialog"] *) a:has(div[style*="padding-bottom"])`

Ads and reels wrap their media in a shrink-to-fit anchor. Left as-is, the anchor sizes from its contents while the contents size from the anchor, and the pair resolves to 0x0. Matching on any padding-bottom box catches both without depending on a generated class name.



## The slide counter — `div:not([role="dialog"] *):has(> div > div > div > button[aria-current="step"])` and its three companions

The feed half of the carousel slide counter, added 2026-09-21. Four rules, and they only make sense read together:

```
host          counter-reset: u-slide u-cur
dot           counter-increment: u-slide u-cur
active ~ dot  counter-increment: u-slide
host::after   content: counter(u-cur) "/" counter(u-slide)
```

`u-slide` counts every dot. `u-cur` counts only up to the active one, because the third rule overrides the second for dots that FOLLOW the active dot and leaves `u-cur` out of their increment. So both numbers are readable at a single element, which is what allows one pill rather than two pieces that have to be seamed together. Counters resolve in tree order and `host::after` is the host's last child, so it has seen every increment below it.

`counter-reset` on the host, never on `:root` or the strip, is what keeps two carousels independent. **This was measured live, not assumed**: with two feed carousels on screen, clicking through one advanced its own index 0 to 6 while the other stayed at 1 throughout. A page-wide counter would have made the second read as a continuation of the first.

WHY THE DOTS ARE MATCHED STRUCTURALLY. The obvious hook is `button[aria-label^="Go to slide"]`, and it works -- on an English page. `aria-label` is prose and is localised, so a style keyed on it silently does nothing for everyone else. `aria-current="step"` is an ARIA token rather than prose, so it is safe, and it identifies the strip; the dots are then just that strip's `> button` children. Measured: every dot container's children are dots and nothing else, on both widgets, across every snapshot -- so `> button` needs no further qualification.

WHY THE HOST IS FOUR LEVELS UP. The chain is host > A > B > strip > buttons, hence `:has(> div > div > div > button[...])`. The nearer candidates do not work. The strip itself sits inside a 50px `overflow: hidden` window -- the thing that shrinks the outer dots on a long carousel -- so a badge anchored there is clipped. The host is the first ancestor outside that clip, and it is already `position: relative`, which makes it the badge's containing block with no change to Instagram's own layout.

**THE HOST IS A DIFFERENT ELEMENT ONCE THIS STYLE'S OWN TWO-COLUMN LAYOUT APPLIES, AND THAT IS THE WHOLE REASON THERE ARE TWO PLACEMENT RULES.** In Instagram's stock single-column layout the host's top edge IS the media's bottom edge, so `bottom: calc(100% + 12px)` lifts the badge 12px above the bottom of the media and overlays it. That is what the base rule does, and below 800px -- where the two-column block does not apply at all -- it is correct. At 800px and up this style moves the dot strip into the **caption column**, so the same host is now the column BESIDE the media rather than the strip below it, and the base rule lifts the badge above the caption column instead: the top-right corner of the whole post, nowhere near the media. **Reported from the live site on 2026-09-21 as exactly that.** The `@media screen and (min-width: 800px)` override re-anchors it.

This was missed because the placement was never actually looked at. The counter's rendered text was checked by screenshot, but the target was pinned with `position: fixed` first to bring it into view, which destroys the flex layout being judged. The number was right and the position was meaningless. Measure a badge against the media's own box, in the layout it will really be in.

HOW THE OVERRIDE FINDS THE MEDIA. Measured on `Instagram_feed3.html` at a 1638px window: the flex row's children are header (full width), media column, caption column; media column `769x869` and caption column `629x314`, so the host is the caption column and the media is two flex items away. It cannot be reached by an ancestor chain, because CSS counters resolve in document order and the dots come AFTER the media in the DOM -- an `::after` on the media column would read `0/0`. So the badge stays on the caption column and reaches the media by absolute positioning outward.

Vertically that is exact and needs no arithmetic: both columns are flex items of the same row with `align-items: flex-start`, so the caption column's top edge and the media column's top edge are the same line -- measured 10391 against 10392, and 12279 against 12280. `top: 12px` therefore lands 11px below the top of the media whatever the header above it is doing, which matters because the header is one line or two depending on whether the post carries a location.

Horizontally it needs the media column's width, which is not a length this element can see. It is recovered from the setting: the media column is `--u-media-column`% of the row and the caption column takes the rest, so the media column is the host's own width times `c / (100 - c)`. Half of that, added to `right: 100%`, puts the badge's right edge on the media column's centre line, and `translateX(50%)` centres the badge on it. **Centre, not a corner, is deliberate**: the media inside that column is `468px` times the carousel zoom and is centred with auto margins, so the gutter between media and column edge is not a constant -- at the default scale of 1.5 it is about 33px a side, and it shrinks as `--u-carousel-scale-max` rises. Any fixed offset from the column's edge would sometimes land in the gutter; the centre line is shared by the column and the media whatever the zoom is.

Measured against the media's real box at four settings, `--u-media-column` 20, 35, 55 and 70: the badge's centre is **exactly** on the media's centre in every case, 0px of error, and its top is 11px below the media's top in every case.

`max(1, 100 - var(--u-media-column))` guards the denominator. `--u-media-column` goes to 100, and dividing by zero there does not fail cleanly -- Firefox was observed producing a position of about -17,894,000px rather than dropping the declaration.

KNOWN GAP: the stacked state, and it is a decision rather than a loose end. When the caption column cannot hold `--u-caption-min` it wraps onto its own line at full width, and then its top edge is the media's BOTTOM rather than its top, while the media column becomes its own left `--u-media-column`% instead of lying to its left. Both facts invert at once, so the override's anchors are wrong in both axes: measured at c=90 on a 1638px window, the right-offset computes to about 6666px and the badge lands near x=-6161. **It is therefore absent rather than misplaced**, which is the one thing that makes leaving it defensible -- nothing appears in the wrong place. Reported live on 2026-09-21 by a user running about c=90, and left as is by their decision. The band is NOT narrow, and an earlier version of this note saying so was wrong: any `--u-media-column` high enough to squeeze the caption below its minimum stacks the post at every window size, so a user who likes a wide media column never sees the counter at all. Each state has an exact one-line rule of its own -- stacked wants `bottom: calc(100% + 12px)` with `left: calc(var(--u-media-column) * 1% / 2)` and `translateX(-50%)` -- but the desired centre is `host.left - M/2` unwrapped against `host.left + host.width * c/200` stacked, and those agree only at c=0. CSS cannot ask whether a flex line wrapped, so one rule cannot serve both. What DOES hold in both is centring over the media COLUMN rather than the media: the media is `468px` times the carousel zoom and centred with auto margins, so at c=90 its column is 1259 wide against a 702 media and the gutter is 278px a side -- measured column centre 779 against media centre 779. Anchor to the column's edge and the badge sits 278px off the photo.

`position: relative` is restated on the host even though every host measured already had it. It costs nothing where it is already true and it keeps the rule self-contained: the badge's containing block is then guaranteed by this file rather than by an Instagram declaration that could move.

The dots are not touched at all -- no size, `overflow` or `transform` change -- so they stay clickable. `counter-increment` has no layout effect, so with the setting hidden the only trace of all this is two inert properties.

THE COUNTER IS ONLY CORRECT WHILE INSTAGRAM RENDERS ONE DOT PER SLIDE, and that relationship is now verified across the whole range rather than assumed. It held at 3, 5, 6, 7, 9, 10, 11 and 16 slides across the captures, and the user confirmed live on 2026-09-21 at 17 to 19 slides and again at **20, which is Instagram's own maximum**, with every number correct. The feed shrinks the outer dots of a long carousel to 2px rather than dropping them -- that is what the 50px clipped strip exists for -- so length does not cost the counter anything. This was an open question until that last check and is not one now; if it ever does break, the failure is silent, because the badge still shows a plausible number.

Match counts across the twenty-one snapshots: 4 on `Instagram_feed3.html`, 4 on `Instagram_feed2.html`, 2 on `Instagram_feed1.html`, 4 on `Instagram_post_modal_over_feed.html` (the feed BEHIND the modal), and **0 on every other capture** -- every reel, every single photo, every post page, and the single-photo modal. Rendered proof: `2/6` on the first feed3 carousel, whose strip shows six dots with the second active.

The `:not([role="dialog"] *)` guard is defensive rather than load-bearing. A modal carousel uses the OTHER widget entirely -- see the post-page note -- so this selector cannot reach one. The guard is there because that is not obvious from the selector, and because the rule is keyed on a dot strip rather than on `article`, which is what the hard rule in `CLAUDE.md` is written around.


## `div[role="dialog"] article div[style*="--x-maxWidth"] > div + div`

The caption and comment column of a post or reel opened as a MODAL, pinned to `--u-modal-caption` at both bounds and through Instagram's own `--media-info` token. Added 2026-09-22 in the `regexp()` post block and **moved here the same day**, for the reason the next paragraph gives. Added 2026-09-22. It is the only rule in either block that targets the modal's geometry, and the only one that deliberately scopes ITSELF to `[role="dialog"]` rather than out of it.

**It lives in the `domain()` block because the selector, not a URL, is what keeps it in its lane -- and because no URL condition could cover its pages anyway.** A reel opened as a modal is served at the bare `/reel/<id>/`, which the `regexp()` post block deliberately does not match: that pattern needs a `p` segment or a `<segment>/reel` pair, and the floating dialog has neither. Widening it was rejected -- the post block's other rules resize a column and a full-height video box, and `CLAUDE.md` excludes the dialog from them on purpose, so taking the URL on would drag all of them onto a layout none was measured against. Site-wide scoping costs nothing here because the selector is already exact: measured across all twenty-two snapshots it matches **1 on each of the four modal captures and 0 on the other eighteen**, the three feeds and `Instagram-reels-id.html` included. `scoped.py --diff` over the move itself changed exactly one snapshot, the reel modal, and left the three post modals and every other page byte-identical.

This is the second rule in this block to carry NO `:not([role="dialog"] *)` guard, and for the same reason as the slide counter: the modal is exactly where it is wanted. The hard rule in `CLAUDE.md` exists because feed rules landing on a modal resize a layout they were never measured against -- this rule was measured against nothing else.

Motivated by a use the style was never designed for: Instagram opened in Firefox for Android with desktop mode on, where the style works well enough to be worth adjusting. Nothing about the rule is mobile-specific -- the column is simply too wide for a narrow window, and the setting is the same one on every screen.

**Gated behind `@media screen and (min-width: 736px)` since 2026-09-24 -- Instagram's own breakpoint for the modal, not this block's 800px.** Shipped without a media query, and the user then reported from the live site that in a narrow viewport the rule wrecks Instagram's default modal -- seen in a narrow window on a desktop computer, and on a phone sending a desktop user agent with desktop mode OFF, so with the phone's real narrow viewport. **Below 736px the modal is a different layout:** the user found live that at `max-width:735px` it turns single-column with no comments shown, so there is no caption column beside the media for the rule to size, and pinning one forces a width onto a layout that has none. Both numbers are in Instagram's CSS in every modal capture -- `@media (max-width:735px)` and `@media (min-width:736px)` -- but none of the rules that survived in the captures touches the modal, so the threshold rests on the live observation, not on a selector traced offline.

**It was briefly gated at 800px, the breakpoint the rest of this block uses, and moved the same day.** That was confirmed live to work -- below 800 both modal types kept the stock column, and a phone in desktop mode still took the setting -- but it withheld the setting from 736-799px, where the modal is still Instagram's two-column layout and the setting is as safe as above 800. Instagram's other nearby breakpoints were checked live by the user and are not the modal's: 767/768px swaps the left sidebar for a bottom bar and changes the header, 1310/1311px and 767/768px both change `/reels/<id>/`, and 875/876px showed no visible difference. At 736px the stock column's own floor is 405px, so the default of 400 leaves the media no narrower than stock does. **Confirmed live at the 736px gate on 2026-09-24:** from 736 to 799px both modal types take the setting, and below 736 they keep Instagram's single-column layout.

**Confirmed live on 2026-09-24, at the 800px gate:** on the phone with desktop mode ON the setting drives the column, so the case that motivated the rule sits above either gate.

**The column is a flex item bounded at both ends, and `min-width` is the end that was hurting.** Instagram gives it `flex-grow:1; flex-shrink:2` with `min-width:405px` and `max-width:500px`, as two of its stylex atoms. The sibling that holds the media is `._aatk._aatl._aatm` with inline `max-height:925px;max-width:925px;aspect-ratio:1/1;flex-basis:925px`, where `._aatk` contributes `flex-grow:1; min-height:450px` and `._aatl` contributes `flex-shrink:1`. So in a narrow window the two shrink together, weighted, until the caption hits 405px and stops -- and 405px of a phone-width viewport is more than half the window given to comments. `max-width:500px` is never reached there and was never the problem.

**Both bounds are set to the same value, so the column is pinned rather than floored.** That is a choice, not a derivation: the user asked for one setting, and pinning makes it behave like `--u-reel-media-info`, the caption-column setting for post pages proper -- a width you set is a width you get. The cost is that the column stops being elastic on a wide window, where Instagram would have let it drift between 405 and 500. Floor-only (`min-width` alone, leaving Instagram's 500) and floor-with-following-ceiling (`max-width: max(500px, ...)`) were both considered and rejected for being harder to explain for no behaviour anyone asked for.

**The hashed classes are deliberately NOT used as the hook, and this is the reason.** The obvious spelling is `.x65f84u.x1vq45kp`, and it measures identically -- but those are stylex names hashed FROM THE DECLARATION: `.x65f84u` is `max-width:500px` and `.x1vq45kp` is `min-width:405px`. If Instagram ever retunes either number the class name changes with it, and a rule keyed on the old name stops matching with no error and no visible breakage beyond the setting quietly doing nothing. The structural hook survives a value change. This is a different judgement from `.xvc5jky` and `._acnb` elsewhere in this file, which are keyed on classes because no structural hook was available; here one is.

**`[role="dialog"]` is load-bearing and was measured, not assumed.** Dropping it leaves `div[style*="--x-maxWidth"] > div + div`, which matches 1 element on each of the three feed captures and 2 on `Instagram_post_modal_over_feed.html` -- the feed page behind the modal contributes its own. With the guard the selector matches **1 on each of the three modal captures and 0 on the other eighteen**, the 105MB carousel page included.

**All four modal captures are structurally identical at this point, which is what makes one selector enough:** the column is the second of exactly two children of a div carrying inline `--x-maxWidth`, inside `<article role="presentation">`, inside `[role="dialog"]` six levels up. The reel modal, `Instagram_reel_modal_over_profile.html` captured 2026-09-22 at `https://www.instagram.com/reel/DdjAuBjTwiu/`, matches on every one of those hooks and carries the same stock `--media-info:335px` and the same `.x1q2y9iw` floor -- so it needed no new selector, only a block that reaches its URL.

**No `!important`, and none is needed.** The selector is (0,2,5) against Instagram's (0,1,0) for a single-atom class rule, so it wins on specificity alone. That is the form `CLAUDE.md` prefers, and it is available here only because the override is written on the element itself rather than on `:root`.

**The media DOES take the freed space, and how Instagram sizes it is now MEASURED rather than inferred.** Offline none of this is visible: the media column is sized by JS-written inline styles that SingleFile froze at capture, the same trap `docs/removed.md` records for post-page carousels, and all three captures carry the identical `flex-basis:925px`, so the corpus cannot show the figure responding to anything. It was read off the live site instead, on 2026-09-22, by logging the column's inline style on every resize across two controlled sweeps -- height varied with width fixed, then the reverse -- over a 4:5 photo, a 9:16 reel, a square photo and a 16:9 landscape, with the style both off and on. **38 rows, and three relations hold exactly on every one of them:**

```
max-height  =  vh - 48
max-width   =  flex-basis  =  max-height * min(AR, 1)
rendered    =  min(max-width, (vw - 128) - caption width)
```

So `925px` was never a constant -- it is one viewport's value for a square post. **The media's width is governed by the HEIGHT budget, never by its own width**, and the `min(AR, 1)` is the square box: for a portrait or square post the box takes the media's true ratio -- the inline `aspect-ratio` reads `720 / 1280`, `1 / 1` -- but for EVERY landscape row the box is forced to `1 / 1` and the media letterboxes inside it, measured at `852x580` inside an `852x852` column. A landscape post therefore gets exactly the width a square one would.

The third relation is the one this rule depends on. The flex row is given `vw - 128`, the caption takes its cut first, and the media gets the rest up to its own cap -- which is why narrowing the caption hands the space straight to the media, and also why it eventually stops paying: once `(vw - 128) - setting` exceeds `max-width` the media is already at its cap and further narrowing gains nothing. On a tall narrow window it never binds, which is the case the setting was added for; on a short wide one it binds early, at roughly 620 for a square post at 1600x900.

**The style does not perturb the derivation.** `max-height` and `max-width` came out identical in the style-off and style-on sweeps, depending only on `vh` and the media's ratio -- never on `vw`, and never on the caption width. So there is no feedback loop between this rule and the number it is competing with. UNVERIFIED: what the constants 48 and 128 are made of -- both are exact across every row sampled, but nothing was measured to attribute them to particular padding, and neither was tested outside vw 800-1600 or vh 600-1600.

**The same live check found the failure that shaped the setting's range, and it is worth understanding before widening it again.** Below about 340 the caption column's contents stopped fitting inside it and spilled over the media to the right -- the comment list, the action bar and the composer all escaping the column they belong to.

The cause is one Instagram declaration: **`.x1q2y9iw { min-width: var(--media-info) }`**, on the wrapper directly inside the caption column. `--media-info` is Instagram's own caption-column token, and on a modal it arrives as an inline style on an ancestor at its stock **335px** -- the same stock value the reel pages carry. So pinning the column below 335 left its inner wrapper still demanding 335, and everything inside the wrapper overflowed. `max-width` and `min-width` on the column alone could never have fixed this, because the constraint was never on the column.

**So the rule sets the token too, and that is what the `--media-info` declaration is for.** Declared on the column itself, it inherits down to `.x1q2y9iw`, whose `min-width` then follows the setting instead of the stock value. No `!important`: the token arrives from an ancestor's inline style, and an inline style only wins at the element it is written on, so a declaration on the column beats it for the column's whole subtree. This is the exception `CLAUDE.md` describes -- an override that needs no `!important` because it is declared closer to the target than Instagram's own.

Measured offline, escaping elements at each setting, on `Instagram-p-id-modal(single_photo).html`. Without the token: clean at 335, **8 at 330**, 46 at 320, 75 at 300, 85 at 250, 100 at 200. With it: clean at 335, 320, 300, 250 and 210, and **4 at 200**. Identical thresholds at 882x1757 and at 1638x900, and the carousel modal agrees, so the floor is neither viewport- nor shape-dependent.

**The residual floor is content, not layout, which is why the range stops at 220 rather than at 200.** The four escapes left at 200 are a single un-wrappable link about 142px wide overflowing by roughly nine -- one element, not the whole column -- and the carousel modal has none at all at the same setting. A longer username would reach further, so no fixed minimum can be proven safe for every post; 220 is where both captures are clean with margin. UNVERIFIED: what the widest realistic username does at 220.

`scoped.py --diff` at the default 400 across all twenty-one snapshots: standard-property changes on exactly the three modal captures -- 204, 164 and 164 -- and 0 on the other eighteen. `min-width` changes on **two** elements per modal, the column and that wrapper; `max-width` on one; `--media-info` on 192, 192 and 303 as it inherits through the subtree. No `font-size`, no `line-height`, no `zoom` anywhere. UNVERIFIED: that Instagram recomputes the media width on resize and the media therefore grows. The rule's own job -- making the caption column narrower -- does not depend on it.

**The reel modal is clean across the whole range**, 350 down to 200, with no escaping elements at any setting -- so the 220 floor is still set by the single-photo post modal alone. It also shows the media cap binding in practice: its column grows as the caption narrows and then stops, because `max-width:520.313px` is `925 * 0.5625` and the media has reached it. Below that point narrowing the caption buys nothing on that post.

