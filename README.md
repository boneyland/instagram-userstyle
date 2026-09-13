# Instagram Desktop Site

A Stylus userstyle that rebuilds Instagram's desktop layout around the media: two-column feed, larger photos, carousels and reels. Layout widths, media size caps, the caption column, font size and line spacing are all adjustable.

![A feed post laid out in two columns, with the photo on the left and the caption, likes and comments beside it on the right.](Preview_1246.png)

## What it changes

**Feed.** The feed column widens to a share of the window rather than sitting at Instagram's fixed width. Each post becomes two columns — media on the left, caption and comments beside it — falling back to stacked when the window is too narrow to give the caption its minimum. Photos drop Instagram's crop-to-fill box and are sized to their own proportions, so nothing is cut off and no blurred plate is drawn behind them. Carousels are enlarged to fit the wider column. Portrait reels, which Instagram flattens into a 4:5 box and crops, are given back more of their height. A landscape reel is sized to its own proportions instead, and follows the same width and height caps. The right-hand rail is hidden by default, and can be brought back from a setting.

**Post pages** (`/p/<id>/` and `/<user>/p/<id>/`). Carousels are enlarged and the column widened to hold them beside a caption. Single photos get the more useful fix: Instagram lays them out two different ways depending on shape, so a tall photo comes out smaller than a carousel in the same place while a square one grows without limit. Neither is sized directly — what the settings govern is the column holding photo and caption, and the width of the caption column within it. The photo takes what is left, which is the same width whatever its shape. Landscape photos are deliberately left alone — Instagram's own layout for them is already good.

**Reel pages** (`/<user>/reel/<id>/`, and reels reached through either `/p/` path). A 9:16 reel is enlarged, with its width and its height each adjustable — whichever is tighter decides the size, and the video keeps its true proportions at every value. A landscape reel is enlarged too, sharing the setting that sizes a photo post. Every post shape is reachable at a `/reel/` URL, not only reels, so all of the above applies there as well.

**Text.** Size and line spacing for usernames, captions and comments, on all of the above. Both start at Instagram's own values, so nothing changes until you move a setting.

## Requirements

[Stylus](https://add0n.com/stylus.html) — this is a UserCSS style, not a stylesheet you can drop into a browser on its own.

**Firefox 126 or newer.** `:has()` needs 121 and `zoom` needs 126. On an older build the declarations are dropped rather than erroring, so the style partly applies and carousels stay at stock size.

Chromium is not restricted, and the style was confirmed working under Stylus for ungoogled-chromium on 2026-09-10. No Chromium version floor has been established, so treat anything older than that as untested.

## Install

Published to [userstyles.world](https://userstyles.world/style/30052/instagram-desktop-site) under the name `Instagram Desktop Site`. Install from there and Stylus will offer updates as new versions are published.

To install this copy instead, open `Instagram.user.css` raw and Stylus will intercept it. Note that a manual install carries no update URL.

## Coverage matrix — page × media shape (WIP)

| Page / modal   | URL shape    | Single photo     | Carousel       | Reel                  |
| -------------- | ------------ | ---------------- | -------------- | --------------------- |
| **Feed**            | `/`           | ✅any ratio — verified 1:1, 4:5, 3:4, 4:3, 3:2, 9:16 (ad) | ✅ any ratio — verified 4:5, 3:4, 4:3, incl. mixed photo+video | ✅ 125% box, 4:3, 16:9 |
| **Post permalink**         | `/p/<id>/`<br>`/<user>/p/<id>/` | ✅ 1:1, 3:4  <br>⭕ 16:9, 4:3             | ✅ 1:1, 3:4, 4:3                           | ✅ 9:16, 16:9, 4:3 |
| **Reel permalink**                | `/<user>/reel/<id>/`       | ✅ 1:1, 3:4  <br>⭕ 16:9, 4:3               | ✅ 1:1, 3:4, 4:3                        | ✅ 9:16, 16:9, 4:3 |
| **Reels, plural path**        | `/reels/<id>/`       | —              | —                  | ❌                     |
| **Reel floating dialog**       | `/reel/<id>/`                   | —                       | —                         | ❌                     |
| **Post modal over profile grid**               | `/p/<id>/`            | ❌                 | ❌            | ❌                     |
| **Post modal over feed**                 | `/p/<id>/`            | ❌                     | ❌              | ❌                     |
| **Grid pages** (profile, explore, hashtag, saved, tagged) | various          | — thumbnails only              | —                           | —                     |
| **Stories**                             | `/stories/...`            | —                   | —                          | —                     |

✅ styled  ·  ❌  nothing except font size and line spacing works here  ·  ⭕ caption column widened, media left at Instagram's own width  ·  — shape cannot reach that URL

## Settings

Fifteen, all exposed through the Stylus settings pane.

| Setting | Default |
| --- | --- |
| Feed: the right-hand sidebar (your profile, the account switcher, suggestions) | Hidden |
| Feed: feed width, as a % of the window | 80% |
| Feed: minimum feed width in pixels | 780px |
| Feed: media width, as a % of feed width | 55% |
| Feed: minimum width of caption column before it moves underneath | 320px |
| Feed: maximum height of a single photo or reel | 900px |
| Feed: maximum width of reel | 550px |
| Feed: scale carousels by a maximum of (1 = off) | 1.5 |
| Text: font size of usernames, captions and comments | 14px |
| Text: spacing between lines of that text | 18px |
| Reel/Post page: total width of photo/video and caption | 1350px |
| Reel/Post page: total width of a 3:4 carousel post and caption | 1350px |
| Reel/post pages: total width of 9:16 reel and caption | 950px |
| Reel/post pages: maximum height of a 9:16 reel | 950px |
| Reel/post pages: width of the caption column | 380px |

Nothing is sized directly. Every width setting caps the column that holds the media and its caption, and the media takes whatever the caption column leaves it — which is why the caption width belongs in the same group rather than being a separate concern.

The two 9:16 reel settings bound the same thing from different directions, and whichever is tighter wins: the width setting caps the column, and the height setting caps it by the width a 9:16 video would need to reach that height. Set either low and the reel simply gets smaller, keeping its proportions.

## Known limitations

- **A portrait reel that is not 9:16 is sized conservatively.** The height setting works out the column a 9:16 video would need, so a shallower portrait reel comes out under its height budget rather than filling it. Landscape reels and 9:16 reels are both exact. No capture of a portrait reel at any other shape exists, so this is reasoning from the arithmetic rather than a measurement.
- **A reel whose own frame is not 9:16 sits on a dark backing.** Instagram puts it in a 9:16 box and the video is letterboxed inside it. Nothing in a stylesheet can recover those pixels — filling the box would mean cropping the video's sides.
- **A reel that is genuinely 4:5 is cropped left and right in the feed.** Instagram flattens anything taller into the same 4:5 box, so a 9:16 reel cannot be told apart from a true one, and giving a tall reel back its height is the same thing as taking the sides off a short one. Lowering "Feed: maximum width of reel" stops at 9:16, so a tall reel is never cropped on its sides at any setting.
- **`/reels/<id>/` and the floating reel dialog are deliberately untouched.** Both are modals with their own markup, which these rules would not transfer to unchanged.

## Repository layout

| Path | Role |
| --- | --- |
| `Instagram.user.css` | The style. The deliverable. |
| `Instagram-2026*-uploaded.user.css` | Previously published versions, kept for diffing. |
| `CHANGELOG.md` | Release notes per version. Earlier releases in `docs/changelog-archive.md`. |
| `docs/removed.md` | Why something is **not** in the style, by subject, with the evidence. |
| `USw-notes.md` | The user-facing changelog, for the Notes field on userstyles.world. |
| `docs/rule-notes*.md` | Why each rule is written the way it is, and what was measured to get there. The index is in `docs/rule-notes.md`; the notes are split by `@-moz-document` block. |
| `docs/token-overrides.md` | Why the design-token overrides work, and how to measure a token's reach. |
| `verify.py`, `scoped.py` | Verification harness. |

The style itself carries no comments beyond its metadata header — the reasoning lives in `docs/rule-notes.md` and the two files it indexes, keyed by selector. Read the note for a rule before loosening a guard or changing a number.

## Verifying a change

```
python3 verify.py Instagram.user.css                   # check one file
python3 verify.py old.user.css Instagram.user.css      # prove a change altered nothing
python3 scoped.py --urls Instagram.user.css            # every block vs every URL shape
python3 scoped.py --diff old.user.css new.user.css     # every snapshot, at its own URL
```

`verify.py` checks the metadata with `usercss-meta` — the parser Stylus itself uses — then runs a rule and declaration census in headless Firefox to catch silently dropped syntax, and with two files diffs every computed property of every element. It is blind to URL scoping, which is what `scoped.py` covers.

**Neither script runs from a fresh clone.** Both read `Instagram_snapshots/`, which is not tracked — the snapshots are captured logged-in sessions of Instagram. Capture your own with [SingleFile](https://github.com/gildas-lormeau/SingleFile) before verifying.

## License

MIT.
