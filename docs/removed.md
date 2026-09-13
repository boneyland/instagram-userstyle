# Removed, and deliberately not done

Why something is **not** in `Instagram.user.css`, and what the evidence was — so it does not get added back.

The style ships to userstyles.world, so it carries no changelog and no notes about what used to be there. `CHANGELOG.md` records each release; this file is the subject-organized record of the deletions and the deliberate omissions, which are the entries most often needed long after the release that made them. Each heading gives the version it happened in.

**Read the entry before re-adding a rule of the same shape.** Several of these were measured live and several were rejected *because* an offline measurement was convincing and wrong — the snapshot freezes inline widths Instagram re-derives at runtime, so a saved page will agree with a rule that does nothing on the real site.

## Carousels

### The post-page carousel `zoom` rule and `--u-post-media-scale` — removed 2026.9.11.4

**The post-page carousel `zoom` rule and its setting, "Post page: enlarge a multi-photo post by" (`u-post-media-scale`, default 1.5).** Both are gone. The rule did nothing visible, and this was measured live on 2026-09-11 on a 3:4 carousel, on both `/p/<id>/` and `/<user>/p/<id>/`: moving the setting anywhere between 1 and 2 produces a brief flash and the media then settles at exactly the size it already was. Carousel sliding was unaffected throughout.

**Why it never worked, and why the snapshots said otherwise.** Each carousel slide frame carries an inline literal `width:<n>px` that Instagram's JS derives from the container, with the slide offsets written as multiples of it. `zoom: 1.5` makes the container report 513 CSS px where it reported 770; Instagram fills 513; zoom scales the result back to 770 — the same rendered size as `zoom: 1`. The flash is the interval between the zoom applying to the old width and Instagram re-deriving the new one.

SingleFile freezes that inline width, so on a saved page the slide cannot re-derive and `zoom` appears to enlarge it. **Every measurement that made this rule look effective came from that freeze** — the "673x898 media at the default scale", the claim that the column must hold `caption + natural media width x scale`, and the coupling between this setting and `--u-post-width`. `docs/rule-notes.md` now marks them as artifacts rather than repeating them.

The same re-derivation is what makes the square-carousel cap added in `2026.9.11.3` correct with no zoom at all, and it was that change's live check which raised the question about this one.

**What actually sizes a 3:4 carousel is unchanged**: `--u-post-width` caps the column, the caption column takes `--u-reel-media-info`, and Instagram fills the difference — measured at 785 -> 356, 950 -> 521, 1200 -> 771. Removing the zoom therefore changes nothing a user sees on a live page, beyond ending the flash and letting Instagram lay the media out at 770 CSS px one-to-one instead of at 513 upscaled.

**Both verification scripts disagree with this on the saved pages, and are expected to.** `scoped.py --diff` reports the two 3:4 carousel snapshots moving 329 standard properties each, because their frozen 449px slides lose the 1.5 and render at 449 instead of 674; the square carousel is untouched at 0, and the remaining eleven snapshots show custom-only drift — 1668 to 16534 elements each losing the `--u-post-media-scale` declaration, with zero standard properties behind it. `verify.py`'s two-file mode fails for a second and separate reason: it flattens every `@-moz-document` block unconditionally, so the removed rule was reaching the feed snapshot, where it matched a 470x3644 region -- the measurement is kept under Structure in `CLAUDE.md`. That accounts for its 2357 standard-property mismatches, all on the feed, a page the rule never touched in the shipped style. Neither result is a regression; they are the freeze and the flattening. The live behaviour is the measurement that counts here.

A `zoom` rule must not be reintroduced on either carousel shape without a live measurement first.

**The feed's `zoom` rule was checked on the same day and KEPT.** `--u-carousel-scale-max` does resize feed carousels, tapering off above roughly 1.6 because the scale is `min(setting, fit ratio)` and past that point the ratio is the smaller term -- the clamp working as designed, the setting being a ceiling. The difference is that the feed rule zooms the carousel wrapper without stretching it (the widening rule beside it is guarded `:not(:has(ul))`), so the container still measures 468px and Instagram still derives 468px slides. Resize the container as well, as the post-page rule did, and the re-derivation cancels the zoom. That is the test to apply to any future zoom.

### No zoom rule for the square carousel — not done, 2026.9.11.3

**No zoom rule for the square carousel**, though one was asked for — and, as it turns out, none is needed.

`zoom` is the only lever that resizes a carousel slide, which is why the 3:4 rule uses one: each slide frame carries an inline literal `width:<n>px` with the slide offsets written as multiples of it, and `zoom` scales both by the same factor so alignment survives. The setting that exists could not have supplied a usable value here anyway — `--u-post-media-scale` has a **minimum of 1**, so it can only enlarge, and a square carousel's slide already arrives at the full content width. Measured on the snapshot: the 1.5 default takes the slide from 1262 to 1893 inside a 770px viewport, strictly worse than leaving it alone.

**Confirmed live on 2026-09-11**, which settled the question the snapshot could not: Instagram **re-derives** the slide width and the offsets from the container. With the style applied, the slides resize correctly at every value of `--u-post-photo-width` and each lands accurately in its frame — the same behaviour unstyled Instagram shows when the viewport is resized. Capping the container is therefore the entire job, and a zoom would only fight it.

A `container-type: inline-size` + `tan(atan2())` derived-zoom version was built and measured before that check, and is deliberately not in the style: it hit a zoom/`cqw` feedback loop, computing 0.63 where 0.61 was wanted, and it reconstructed the very number SingleFile freezes, so no offline test could have validated it. Recorded so it is not attempted again.

Related artifact, recorded so it is not mistaken for a bug: on the **saved** square-carousel page the cap narrows the container while the frozen slide stays 1262, so any measurement taken there reports the slide overflowing its 770px viewport by 493px. That is a property of the capture, not of the live page.

### No guard against a mixed carousel — not done, 2026.9.10.1

**No guard was written against a *mixed* carousel** — photo plus video slides — on a `/p/` URL. It is the one page shape that could satisfy the reel block's loose `:root` video guard and the post block's carousel guard at the same time, now that both blocks match these URLs.

Everything measurable says it is harmless. Both blocks set `--media-info` to the same 429px, so that collision has no outcome. The reel block's column rule needs the exact child chain `:has(> div > div > div video)`, which scores **0** on both carousel snapshots. And the reel block precedes the post block in the file, so at equal specificity a carousel's own `--x-maxWidth` wins any collision that did occur. Carousel slides also use an `aspect-ratio` spacer rather than a `padding-bottom` box, which is what the `177` rule keys on.

It was left unguarded because no snapshot of a mixed carousel exists to test a guard against, and an untested selector is the thing this file's conventions exist to avoid. If one ever lays out wrongly, adding `:not(:has(li[style*="translateX"]))` to the reel block's `:root` and column rules is the first thing to try — but measure it against a real capture first, because on a flattened feed that exclusion *does* change the outcome.

### No carousel height cap — not done, 2026.9.10.1

**Carousels are still uncapped, deliberately.** A carousel's height is `468px × ratio × zoom`, and the same padding-percentage reason applies to its spacer: `max-height` there changed nothing (936px before and after). `max-height` on the zoomed wrapper does bite, but only as a crop with `overflow: hidden`, and the value has to be divided back out by the scale because it is inside the zoom — measured, `calc(400px / var(--u-carousel-scale))` plus `overflow: hidden` gave exactly 400px on screen with the bottom of the photo cut off. Fitting rather than cropping means lowering the scale, which needs the media's aspect ratio. That is readable from the inline `padding-bottom` prefix the way `125%` and `177` already are, so a per-ratio bucket using `tan(atan2())` is possible — it was not written because it costs one rule per known ratio and was out of scope here.

## Reels

### The landscape feed reel's width cap — removed 2026.9.14.1

**`article:has(a[href*="/reels/"]):not([role="dialog"] *) a:has(div[style*="padding-bottom"]:not([style*="125%"]):not([style*="padding-bottom: 125%"]))`, setting `max-width: var(--u-feed-reel-width)` and `margin-inline: auto` on the anchor.** Removed so that `u-feed-reel-width` governs the 125% portrait boxes only, which is what its label now says: it was relabelled from "Feed: maximum width of reel" to "Feed: maximum width of portrait reel" in the same change. This was the user's instruction, and the choice was deliberate -- the label named more than the setting should govern, and the setting was narrowed to the label rather than the label widened to the setting.

**Only this rule went.** The two rules below it in the block are untouched, so a landscape reel still collapses its `padding-bottom` box to `height: auto; width: fit-content` and still sizes its video from the video's own intrinsic dimensions under `max-width: 100%` and `max-height: var(--u-media-max-height)`. What it lost is a dedicated width setting, not a width bound.

**Measured, `Instagram_feed2.html` article 4 -- a 16:9 reel at `padding-bottom:56.4263%` -- at a 1638px window, defaults.** The anchor's `max-width` goes 550px -> none, its width 550 -> 687.017, and its auto margins 68.5 -> 0. `verify.py`'s two-file mode reports 38 standard-property mismatches and 0 custom, spread over the anchor and six descendants that were constrained by it; the properties that move are width/inline-size, transform-origin/perspective-origin and the four margin longhands, with **no `font-size`, `line-height` or `zoom`** among them -- the signature that would mean a text container had been resized by mistake. The declaration census drops 143 -> 140, which is exactly this rule: `max-width` plus `margin-inline` expanded to its two longhands, since `verify.py` counts CSSOM `style.length`. Rule count drops 42 -> 41. Single-file mode passes, so nothing was silently dropped. `scoped.py --diff`, which applies each file to every snapshot with only the blocks that page's real URL selects, reports **1 of 21 snapshots changed -- `Instagram_feed2.html`**, the only capture holding a landscape reel. The twenty others, every post shape and the modal among them, are byte-identical, which is the confirmation that this rule reached nothing outside the feed.

**Where this leaves a landscape reel, and why that is not a regression to before 2026.9.11.6.** It fills the media column: the anchor is `width: 100%` from the ads-and-reels rule, so 687.017 at the defaults. That is the same number the note in `docs/rule-notes-feed.md` records for the state *before* 2026.9.11.6 added this rule -- but that release added three rules, and the other two stay. The box collapse and the intrinsic-size video cap are still there, so the reel is bounded by the media-column percentage and by the height setting, whose label was widened to "Feed: maximum height of a single photo or reel" in the same session. Only the dedicated width term is gone.

**Offline verification cannot show what this looks like.** SingleFile strips video sources and replaces the poster with `data:,`, so every `<video>` in every snapshot here renders at the 300x150 replaced-element default. The computed-property measurements above are real -- they are about the anchor, which has no dependence on intrinsic video size -- but the reel's rendered size is not checkable offline. Confirming the result is a live check.

**If it is written back**, the measurements from when it existed are kept in `docs/rule-notes-feed.md` under the removed heading, including what the cap produced at each setting (F=550 gave 550x310.3, F=400 gave 400x225.7, F=300 gave 300x169.3, all holding the source's 0.5643 ratio) and why the cap belongs on the anchor rather than the box. It should come back with a setting of its own rather than by re-attaching `u-feed-reel-width`, which would put the label back in the state this change fixed.

### The duplicate `--x-maxWidth` rule on the reel column — removed 2026.9.12.4

A **duplicate `--x-maxWidth` rule** on the reel column, left behind when the new bounded version was written above it. Same selector, same specificity, both `!important`, so it lost only by coming first -- live code that did nothing and would have silently reverted the height cap if the block were ever reordered. `scoped.py --diff` confirms deleting it changes nothing on any snapshot.

### The reel stage's `min-height` — not done, 2026.9.12.4

A dark band under a small reel was reported with a screenshot, and the snapshot explained it exactly: the stage that holds the video carries Instagram's own `min-height: 450px` and centres the video in it, so a media box shorter than that leaves a band above and below. Measured at `u-reel-height: 400`: stage 225x450 against a 224x398 box, 26px each side. A one-property fix, `main > div > div.xvc5jky > div > div:has(video) { min-height: 0 !important }`, closed it to 0 on the snapshot and measured inert everywhere else.

**It is not in the style.** The live check found the band did not occur, so the rule would have been machinery against a snapshot artefact. Recorded here because the snapshot measurement is reproducible and convincing on its own -- anyone re-deriving it offline will reach the same rule -- and because the discrepancy is unexplained: the floor is real in the saved CSS and something live evidently overrides or avoids it. Do not add the rule on the strength of an offline measurement; reproduce the band on the live site first.

## Single photos

### No height cap — not done, 2026.9.11.1

**No height cap.** The tallest photo Instagram appears to accept is the 133.333% of the new snapshot, which at the default lands at 893px tall — within 5px of the carousel's 898px, so there is nothing for a cap to do yet. A cap could not be built the obvious way in any case: `max-height` on a `padding-bottom` box does nothing, for the reason recorded at length under the feed reel-height entry in 2026.9.10.1.

## The left nav and its dependents — all removed 2026.9.10

### The collapsing left nav

**The collapsing left nav** — the rules that set `--nav-narrow-width`, `--nav-medium-width`, and `--nav-wide-width` to 72px and restored 244px/335px on hover. Instagram still declares those three tokens, which is where the hover values came from, but nothing reads them any more: no `var()` consumer appears in a saved page, and setting them has no visible effect on a live one. Rebuilding the feature means finding whatever governs nav width now; the old token names are a dead end.

### The settings-page padding rules

**The settings-page padding rules** on `.x17snn68` / `.xw2csxc`. They existed to compensate for the collapsed nav and do nothing without it.

### `svg[aria-label="Instagram"]`

**`svg[aria-label="Instagram"] { width: min(103px, 100%) }`**, a third nav leftover. In 20260907 it sat immediately after the nav block, which is where its two branches make sense: `100%` stopped the logo overflowing the rail the style had narrowed to 72px, and 103px capped it once hover expanded the rail. With the nav rules gone nothing narrows the rail any more. The selector still matches, but what it matches on all five snapshots is a 24×24 `viewBox="0 0 24 24"` glyph in the rail's home link, not a 103px wordmark — so its containing block is 24px, `100%` resolves to 24px, and `min(103px, 24px)` returns the size the glyph already had. Measured under the `verify.py` harness on the feed snapshot: computed width 24px with and without the rule, and a full two-file diff of the style against itself minus this rule is computationally identical across all 1668 elements. The rail is present in that snapshot but its fixed container computes to width 0, so the offline evidence covers only the collapsed state; the user confirmed on a live page that it changes nothing whatever the rail is doing. This also retires the open item about the `aria-label` being confirmed only on an `en` page — a rule that does nothing cannot silently do nothing in other locales.

## Selectors and overrides

### `:not(.xtcbf50)` — removed 2026.9.10

**`:not(.xtcbf50)`** from the two-column post selector. The class was inherited from an earlier version with no recorded purpose and was not found anywhere — live feed, reel pages, `/reels/audio/`, or the saved snapshot — so it excluded nothing. This is the one change here that no offline check can validate, precisely because the class is absent everywhere we can look: if some post type ever lays out wrongly, restoring this exclusion is the first thing to try.

### The `:root` half of the `--system-14-*` override — removed 2026.9.10

**The `:root` half of the `--system-14-*` override.** 20260907 declared these on `:root, article`. The `:root` selector never did anything — see the entry under Changed — so it was dropped rather than left looking load-bearing.

## Metadata and comments

### Every comment outside the metadata block — removed 2026.9.11.1

**Every comment outside the metadata block.** The style went from 367 lines to 232. Nothing else changed: no selector, declaration or block condition was touched, and the metadata header is byte-for-byte identical.

This reverses the standing convention that the style's comments are user-facing, and it was a deliberate call, not drift. The cost is that a reader in the Stylus editor or the userstyles.world code view now gets no explanation of why a guard is shaped the way it is. That is survivable only because `docs/rule-notes.md` already holds every one of those explanations keyed by selector, and is the canonical copy — the comments were the abbreviated duplicate, not the record. **Before loosening a guard or changing a number, read the note there.** Nothing in the style will warn you any more.

Proven inert rather than assumed so. `verify.py` against the pre-strip file: both keep the same 37 rules and 119 declarations, both change the same 31697 computed properties across 1668 elements, and the two are reported computationally identical. `scoped.py --diff` across all 13 snapshots, each at its own URL: zero standard and zero custom property differences, with every snapshot selecting the same block count as before.

### `@description` no longer states the browser requirement — removed 2026.9.11.2

**`@description` no longer states the browser requirement.** It ended `Requires Firefox 126+ (:has() and zoom).`; it now ends at the layout summary. The requirement itself is unchanged — the floor is still Firefox 126, `:has()` needing 121 and `zoom` needing 126 — and it is stated where a reader looks for it rather than in a one-line blurb: `README.md` gives it a "Requirements" heading of its own, alongside Stylus and the Chromium caveat. Do not re-add it to `@description`.

`USw-notes.md` was rewritten in the same pass and now carries a Requirements heading of its own, so the statement a userstyles.world visitor sees is no longer buried in an old changelog entry.

## Investigated, not changed

### High memory use on some Instagram pages — 2026.9.10

A report of high memory use on some Instagram pages, seen in both Firefox and Chromium. **No root cause was found and nothing was changed.** The symptom did not reproduce on demand when looked for. Three hypotheses were tested and all three came back negative; do not re-open them without a reproduction.

**Zero-height posts driving an infinite-scroll runaway.** The theory was that the media-box collapse (`height: auto` plus `position: static` on the image) yields a zero-height post whenever the image has no intrinsic size, leaving the feed short enough that the scroll sentinel never leaves the viewport and Instagram appends pages forever. Rejected by observation: on a live affected page, article count, image count and `scrollHeight` all stayed flat over a minute of sitting still.

The collapse itself is real but was only reproduced against the snapshot, where it is an artifact. Applying the style there drops one article from 1135px to 419px and zeroes its `_aagu`/`_aagv` wrappers — but every `<img>` in the snapshot has `src="data:,"` (SingleFile stripped the bitmaps) and so reports `naturalWidth` 0. The snapshot cannot show whether a live, not-yet-loaded image behaves the same way. Worth knowing that the trap the style already documents for `<video>` has the same shape for images.

**`zoom` raster cost.** Measured, and too small to matter: rasterised media area over one 1638×900 screenful goes from 378,581px² to 595,878px², about +57%, on the order of 1.5MB → 2.4MB. Bounded per screen, so it cannot produce unbounded growth.

**The shipped and local versions both enabled at once compounding `zoom`.** Plausible on its face, since `zoom` multiplies down the ancestor chain and the `:not([style*="--x-width"])` guard exists to stop exactly that. Rejected by measurement: with both sheets applied in either order, maximum effective zoom stays 1.500 across 81 zoomed nodes and media area is unchanged to within 9px². 20260907 declares no `zoom` at all, and where both versions match they match the same element, so the cascade picks one winner rather than nesting.

The leading explanation is now the null one — Instagram's own retention on infinite-scroll pages, several tabs at a time, independent of the style. That both engines behave alike supports it. To beat it, the measurement needed is the same page at the same scroll depth in two windows, style on versus off, compared in `about:performance` or Chromium's task manager.

