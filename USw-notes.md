Rebuilds Instagram's desktop layout around the media instead of a fixed 470px column: posts become two columns, photos are shown uncropped, and carousels and reels are enlarged to fill the space that gains.

**[Full documentation, the settings table and the complete changelog are on GitHub.](https://github.com/boneyland/instagram-userstyle)** The following is a summary.

## What it changes

- **Feed.** The feed widens to a share of the window, and each post becomes two columns — media on the left, caption and comments beside it — stacking again when the window is too narrow. Photos lose Instagram's crop-to-fill box and the blurred plate behind them, carousels are enlarged, and portrait reels get back more of their height. The right-hand sidebar is hidden, and a setting brings it back.
- **Post pages.** Carousels are enlarged by widening the column they sit in; the media takes whatever the caption column leaves it. Single photos, which Instagram lays out two different ways depending on their shape, are handled by capping that same column instead: the photo takes whatever width the caption column leaves it, and that comes out the same whether the photo is tall or square. Landscape photos get no width cap of their own, because Instagram's own layout for them is already good; they grow with the window instead.
- **Reel pages.** Reels are enlarged and the caption column widened. A portrait reel has both its width and its height adjustable — whichever you set tighter decides the size, and the video keeps its true proportions at every value. A square or landscape reel has a width setting of its own. All of it applies to reels reached through a post URL, and to any post opened at a `/reel/` URL.
- **Post modal.** A post or reel opened in a floating panel — by clicking it in the feed, or reaching it from a profile grid — is laid out by Instagram rather than by the settings above, so its caption and comment column has a setting of its own. Narrowing it hands the space to the media.
- **Text.** Size and line spacing of usernames, captions and comments, everywhere above. Both start at Instagram's own values, so nothing changes until you move a setting.

Eighteen settings in all, adjustable from the Stylus settings pane. [The table of defaults is in the README.](https://github.com/boneyland/instagram-userstyle#settings)

## Requirements

[Stylus](https://add0n.com/stylus.html), and **Firefox 126 or newer** — `:has()` needs 121 and `zoom` needs 126. On an older build those declarations are dropped silently rather than erroring, so the style only partly applies and carousels stay at Instagram's size.

Chromium-based browsers are not restricted, and the style was confirmed working under Stylus for ungoogled-chromium. No version floor has been established there, so treat it as lightly tested.

## What's new

Since `2026.9.21.1`, the version published here before this one. [The full changelog, with the reasoning behind each change, is on GitHub.](https://github.com/boneyland/instagram-userstyle/blob/main/CHANGELOG.md)

One new setting and a retune of some defaults. Nothing outside a post modal changes, and settings you have already adjusted are kept as they are.

- **The caption column of a post or reel modal is adjustable.** A new setting, **Post modal: width of the caption and comment column**, default 400px. Instagram lets that column drift between 405px and 500px depending on the space available, which in a narrow window leaves more than half the screen to comments. The setting pins it to one width instead, and the media beside it grows into whatever the column gives up. It reaches every modal — a post opened from the feed or from a profile grid, and a reel opened at a `/reel/` URL — and nothing else on the page moves. Mostly useful for narrowing the column, which is what makes a modal usable in a narrow window such as a phone browser in desktop mode.
- **The carousel slide counter is now shown by default.** It arrived switched off in the previous version. A fresh install now sees it; if you already have the style, your own choice is kept and nothing changes.
- **Finer sliders.** Most pixel settings now step in 5px rather than 10, and the reel/post caption column in 5px rather than 1. `Reel/post pages: width of the caption column` is relabelled "caption and comment column" to match the new modal setting — same setting, same value, new name.
