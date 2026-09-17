Rebuilds Instagram's desktop layout around the media instead of a fixed 470px column: posts become two columns, photos are shown uncropped, and carousels and reels are enlarged to fill the space that gains.

**[Full documentation, the settings table and the complete changelog are on GitHub.](https://github.com/boneyland/instagram-userstyle)** The following is a summary.

## What it changes

- **Feed.** The feed widens to a share of the window, and each post becomes two columns — media on the left, caption and comments beside it — stacking again when the window is too narrow. Photos lose Instagram's crop-to-fill box and the blurred plate behind them, carousels are enlarged, and portrait reels get back more of their height. The right-hand sidebar is hidden, and a setting brings it back.
- **Post pages.** Carousels are enlarged by widening the column they sit in; the media takes whatever the caption column leaves it. Single photos, which Instagram lays out two different ways depending on their shape, are handled by capping that same column instead: the photo takes whatever width the caption column leaves it, and that comes out the same whether the photo is tall or square. Landscape photos get no width cap of their own, because Instagram's own layout for them is already good; they grow with the window instead.
- **Reel pages.** Reels are enlarged and the caption column widened. A portrait reel has both its width and its height adjustable — whichever you set tighter decides the size, and the video keeps its true proportions at every value. A square or landscape reel has a width setting of its own. All of it applies to reels reached through a post URL, and to any post opened at a `/reel/` URL.
- **Text.** Size and line spacing of usernames, captions and comments, everywhere above. Both start at Instagram's own values, so nothing changes until you move a setting.

Sixteen settings in all, adjustable from the Stylus settings pane. [The table of defaults is in the README.](https://github.com/boneyland/instagram-userstyle#settings)

## Requirements

[Stylus](https://add0n.com/stylus.html), and **Firefox 126 or newer** — `:has()` needs 121 and `zoom` needs 126. On an older build those declarations are dropped silently rather than erroring, so the style only partly applies and carousels stay at Instagram's size.

Chromium-based browsers are not restricted, and the style was confirmed working under Stylus for ungoogled-chromium. No version floor has been established there, so treat it as lightly tested.

## What's new

Since `2026.9.14.1`, the version published here before this one. [The full changelog, with the reasoning behind each change, is on GitHub.](https://github.com/boneyland/instagram-userstyle/blob/main/CHANGELOG.md)

One fix and two labels. No setting is added or removed, and your saved values carry over untouched.

- **The post and reel page width settings work at every value again.** Instagram started capping the post column at its own 935px content width, so widening a photo, carousel or reel past that point did nothing — the settings appeared to work up to a point and then stop. That ceiling is lifted, and the media grows with the window again. The "More posts from" grid below the post widens with it, the way it did before Instagram's change.
- **Two labels now name every shape they reach.** "Total width of a landscape reel and caption" reads **square/landscape reel**, and "total width of a 3:4 carousel post and caption" reads **portrait carousel**. The rules behind them always covered those shapes; only the labels were behind.
