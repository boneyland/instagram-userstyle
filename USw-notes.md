Rebuilds Instagram's desktop layout around the media instead of a fixed 470px column: posts become two columns, photos are shown uncropped, and carousels and reels are enlarged to fill the space that gains.

**[Full documentation, the settings table and the complete changelog are on GitHub.](https://github.com/boneyland/instagram-userstyle)** The following is a summary.

## What it changes

- **Feed.** The feed widens to a share of the window, and each post becomes two columns — media on the left, caption and comments beside it — stacking again when the window is too narrow. Photos lose Instagram's crop-to-fill box and the blurred plate behind them, carousels are enlarged, and portrait reels get back more of their height. The right-hand sidebar is hidden, and a setting brings it back.
- **Post pages.** Carousels are enlarged by widening the column they sit in; the media takes whatever the caption column leaves it. Single photos, which Instagram lays out two different ways depending on their shape, are handled by capping that same column instead: the photo takes whatever width the caption column leaves it, and that comes out the same whether the photo is tall or square. Landscape photos get no width cap of their own, because Instagram's own layout for them is already good; they grow with the window instead.
- **Reel pages.** Reels are enlarged and the caption column widened. A portrait reel has both its width and its height adjustable — whichever you set tighter decides the size, and the video keeps its true proportions at every value. A square or landscape reel has a width setting of its own. All of it applies to reels reached through a post URL, and to any post opened at a `/reel/` URL.
- **Text.** Size and line spacing of usernames, captions and comments, everywhere above. Both start at Instagram's own values, so nothing changes until you move a setting.

Seventeen settings in all, adjustable from the Stylus settings pane. [The table of defaults is in the README.](https://github.com/boneyland/instagram-userstyle#settings)

## Requirements

[Stylus](https://add0n.com/stylus.html), and **Firefox 126 or newer** — `:has()` needs 121 and `zoom` needs 126. On an older build those declarations are dropped silently rather than erroring, so the style only partly applies and carousels stay at Instagram's size.

Chromium-based browsers are not restricted, and the style was confirmed working under Stylus for ungoogled-chromium. No version floor has been established there, so treat it as lightly tested.

## What's new

Since `2026.9.17.1`, the version published here before this one. [The full changelog, with the reasoning behind each change, is on GitHub.](https://github.com/boneyland/instagram-userstyle/blob/main/CHANGELOG.md)

One fix and one new setting. Your saved values carry over untouched, and the new setting starts switched off.

- **Feed carousels no longer go blank after you view a story.** Coming back to the feed from a story left carousels as empty boxes that never filled in again unless you scrolled them away and back. That was this style's doing: the rule that widens the media measured itself against a parent that had nothing to size it while Instagram had the slides unloaded, and the pair collapsed to nothing. It now has a floor it cannot fall below. Nothing else about the layout changes.
- **A carousel can show which slide you are on.** A new setting, **Carousels: a slide counter (3/7) over the media**, puts a small pill on carousels with the current slide and the total — in the feed, on post and reel pages, and on a post opened in a lightbox. It starts **hidden**, so switch it on if you want it. The dots stay exactly where they are and stay clickable; the counter sits above them on the feed and in the bottom corner of the media on a post page.

Not covered: carousels with more than 16 slides have not been checked. If you find one where the total reads low, that is why.
