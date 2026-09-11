## Changelog

### 2026.9.11

#### Added

- **Single photos on `instagram.com/p/…` and `instagram.com/<user>/p/…` are now sized consistently.** Instagram sizes them two different ways depending on the photo's shape: a tall photo came out small — smaller than a carousel on the same page — while a square one filled the whole window and kept growing on a wider screen. Both now come out the same width, and within a few pixels of a carousel.
- One new setting, **Post page: total width of a single photo and caption**, default 1100px. Lower it for a smaller photo, raise it for a bigger one. Unlike the multi-photo settings it needs no second setting to go with it, and it works the same whatever shape the photo is.
- Popups are unaffected, as are carousels, reels, and the feed.

#### Changed

- **"Post page: total width of photo and caption together" is now "Post page: total width of a multi-photo post and caption."** With a single-photo setting beside it the old name was ambiguous. Only the name changed; your saved value carries over.

### 2026.9.10.1

#### Fixed

- **Post popups are left alone again.** Opening a post as a popup — clicking one in the feed, or from a profile grid — put the photo through the feed's sizing, so the maximum height setting was shortening it even though it is a feed setting. Popups now keep Instagram's own layout. Posts opened as a full page are unaffected, as before.
- **The maximum height setting now works on reels**, not just photos. It had never had any effect on a reel, whatever you set it to. It is now called **Feed: never let a photo or reel get taller than**, and your saved value carries over.
- At the default of 900px nothing changes unless your window is wider than about 1640px. Below roughly 690px the reel also starts getting narrower as it gets shorter, since the two are tied together by the reel's shape.
- Carousels are not limited by this setting. Only single photos and reels are.
- **Line spacing now works everywhere the text size setting works.** On `instagram.com/reels/<id>/` it had no effect at all, and elsewhere it reached less of the text than the size setting did — usernames, timestamps and other short labels changed size but kept Instagram's spacing. Both settings now move together.
- **The comments panel on `instagram.com/reels/<id>/` now follows the text settings too.** This was listed as a known gap in the previous release; it is closed.

### 2026.9.10

#### Added

- Carousels are now enlarged along with everything else in the feed. Previously only single images grew and carousels stayed at Instagram's default size.
- Every setting is now adjustable from Stylus' own options screen — feed width, how the row splits between media and caption, text size and line height, maximum media height, how much carousels scale, and the reel page's widths. No more editing the CSS by hand.
- Carousels are now enlarged on individual post pages too, both `instagram.com/p/…` and `instagram.com/<user>/p/…`. These pages now use the same caption column width as reel pages, and there are two new settings: **Post page: enlarge a multi-photo post by**, and **Post page: total width of photo and caption together**. Captions and comments keep their own text size. Reels on those pages are not affected yet.
- Those two settings work together: if you raise how much the post is enlarged, raise the total width with it, or the photo will outgrow the space beside the caption. Wide posts need more total width than tall ones at the same setting.
- Every setting has been renamed to say plainly what it does, so you no longer have to read the stylesheet to tell them apart.

#### Changed

- Now requires **Firefox 126 or newer**.
- Text size and line height now start at Instagram's own 14px and 18px, instead of being forced to 16px with tighter line spacing. Raise them in the settings if you preferred the larger text. They affect usernames, captions and comments in the feed, on individual post pages, and on reel pages. One known gap: the comments panel on `instagram.com/reels/<id>/` keeps Instagram's own size.

#### Fixed

- Widening now applies reliably. Depending on how Instagram rendered a page, some posts and reels could keep their original size.
- The reel page's caption column width no longer affects post popups.
- Carousels opened at a reel URL are no longer made *smaller* than without the style. The widened caption column was taking space that nothing gave back.

#### Removed

- The collapsing left sidebar. Instagram stopped using the variables it worked through, so it had no effect any more.
