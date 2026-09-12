Rebuilds Instagram's desktop layout around the media instead of a fixed 470px column: posts become two columns, photos are shown uncropped, and carousels and reels are enlarged to fill the space that gains.

**[Full documentation, the settings table and the complete changelog are on GitHub.](https://github.com/boneyland/instagram-userstyle)** The following is a summary.

## What it changes

- **Feed.** The feed widens to a share of the window, and each post becomes two columns — media on the left, caption and comments beside it — stacking again when the window is too narrow. Photos lose Instagram's crop-to-fill box and the blurred plate behind them, carousels are enlarged, and portrait reels get back more of their height. The right-hand sidebar is hidden, and a setting brings it back.
- **Post pages.** Carousels are enlarged by widening the column they sit in; the media takes whatever the caption column leaves it. Single photos, which Instagram lays out two different ways depending on their shape, are handled by capping that same column instead: the photo takes whatever width the caption column leaves it, and that comes out the same whether the photo is tall or square. Landscape photos are left alone, because Instagram's own layout for them is already good.
- **Reel pages.** Reels are enlarged and the caption column widened. A 9:16 reel has both its width and its height adjustable — whichever you set tighter decides the size, and the video keeps its true proportions at every value. A landscape reel is enlarged too. All of it applies to reels reached through a post URL, and to any post opened at a `/reel/` URL.
- **Text.** Size and line spacing of usernames, captions and comments, everywhere above. Both start at Instagram's own values, so nothing changes until you move a setting.

Fifteen settings in all, adjustable from the Stylus settings pane. [The table of defaults is in the README.](https://github.com/boneyland/instagram-userstyle#settings)

## Requirements

[Stylus](https://add0n.com/stylus.html), and **Firefox 126 or newer** — `:has()` needs 121 and `zoom` needs 126. On an older build those declarations are dropped silently rather than erroring, so the style only partly applies and carousels stay at Instagram's size.

Chromium-based browsers are not restricted, and the style was confirmed working under Stylus for ungoogled-chromium. No version floor has been established there, so treat it as lightly tested.

## What's new

Since `2026.9.12.1`, the version published here earlier today. [The full changelog, with the reasoning behind each change, is on GitHub.](https://github.com/boneyland/instagram-userstyle/blob/main/CHANGELOG.md)

- **Reels on post and reel pages now respond to the settings whatever their shape.** A landscape reel — anything wider than it is tall — ignored every setting except the text ones and filled the window at Instagram's own size. It is now sized like a photo post, by the same setting.
- **The size of a 9:16 reel is now yours to set, in both directions.** Its height was fixed before: no setting touched it, and widening the reel only added empty space on either side of the video rather than making it bigger. There is now a new setting, **Reel/post pages: maximum height of a 9:16 reel**, working alongside the width one — whichever you set tighter decides the size, and the reel keeps its proportions at every value. Two things worth knowing: the height no longer stops at the window's height, so a tall value will scroll; and with both at their 950px default it is the height that decides, so the reel is a little narrower than the width slider reads.
- **Any post opened at a `/reel/` address gets the full treatment.** Photos and multi-photo posts turn up at those addresses too, not only reels, and they were being left at Instagram's layout there.
- **Every setting has been renamed** — each one now names what it governs rather than describing it, so the pane reads as a list rather than a paragraph. Saved values carry over untouched.
- **Two defaults moved**, both post-page widths, from 1150px to 1350px. Every default is only a starting point: set them to whatever suits your screen.
