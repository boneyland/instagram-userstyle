Rebuilds Instagram's desktop layout around the media instead of a fixed 470px column: posts become two columns, photos are shown uncropped, and carousels and reels are enlarged to fill the space that gains.

**[Full documentation, the settings table and the complete changelog are on GitHub.](https://github.com/boneyland/instagram-userstyle)** The following is a summary.

## What it changes

- **Feed.** The feed widens to a share of the window, and each post becomes two columns — media on the left, caption and comments beside it — stacking again when the window is too narrow. Photos lose Instagram's crop-to-fill box and the blurred plate behind them, carousels are enlarged, and portrait reels get back more of their height. The right-hand sidebar is hidden, and a setting brings it back.
- **Post pages.** Carousels are enlarged by widening the column they sit in; the media takes whatever the caption column leaves it. Single photos, which Instagram lays out two different ways depending on their shape, are handled by capping that same column instead: the photo takes whatever width the caption column leaves it, and that comes out the same whether the photo is tall or square. Landscape photos are left alone, because Instagram's own layout for them is already good.
- **Reel pages.** Reels are enlarged and the caption column widened. A portrait reel has both its width and its height adjustable — whichever you set tighter decides the size, and the video keeps its true proportions at every value. A landscape reel has a width setting of its own. All of it applies to reels reached through a post URL, and to any post opened at a `/reel/` URL.
- **Text.** Size and line spacing of usernames, captions and comments, everywhere above. Both start at Instagram's own values, so nothing changes until you move a setting.

Sixteen settings in all, adjustable from the Stylus settings pane. [The table of defaults is in the README.](https://github.com/boneyland/instagram-userstyle#settings)

## Requirements

[Stylus](https://add0n.com/stylus.html), and **Firefox 126 or newer** — `:has()` needs 121 and `zoom` needs 126. On an older build those declarations are dropped silently rather than erroring, so the style only partly applies and carousels stay at Instagram's size.

Chromium-based browsers are not restricted, and the style was confirmed working under Stylus for ungoogled-chromium. No version floor has been established there, so treat it as lightly tested.

## What's new

Since `2026.9.12.4`, the version published here before this one. [The full changelog, with the reasoning behind each change, is on GitHub.](https://github.com/boneyland/instagram-userstyle/blob/main/CHANGELOG.md)

Mostly a tidy-up of the settings pane: several labels promised more than the setting behind them did, and one setting was doing the work of two. Your saved values carry over untouched — only the labels changed, never the settings themselves.

- **Landscape reels get their own width setting.** One setting used to size landscape reels, single photos and carousels together, so you could not widen a photo without widening reels with it. There is now **Reel/post pages: total width of a landscape reel and caption**, starting at 1500px, and the old setting keeps the photos and carousels. Landscape reels start a little wider than before as a result; both are yours to set.
- **Three labels now say what they actually do.** "Feed: maximum height of media" never affected carousels, and is now **maximum height of a single photo or reel**. "Feed: maximum width of reel" reached both upright and landscape reels, and is now **maximum width of portrait reel**. The post-page one that read "photo/video" no longer covers video, and reads **photo/carousel**.
- **A landscape reel in the feed now fills the media column** rather than stopping at the reel width setting, which no longer applies to it. Its height setting still does, as does the media column width.
- **The two post-page reel settings say "portrait reel"** instead of "9:16 reel". They always covered every upright reel, not just that one shape.
- **The carousel scale setting is a slider now** rather than a number box, matching the rest of the pane. Same default, same range.
- **The feed now starts at 90% of the window** rather than 80%. As always, every default is only a starting point.
