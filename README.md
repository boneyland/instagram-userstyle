# Instagram Desktop Site

A userstyle that rebuilds the desktop web layout of `www.instagram.com` around the media instead of around a fixed 470px column: posts become two columns, photos are shown uncropped and unletterboxed, and carousels and reels are enlarged to fill the space that gains.

![A feed post laid out in two columns, with the photo on the left and the caption, likes and comments beside it on the right.](Preview_1246.png)

## What it changes

**Feed.** The feed column widens to a share of the window rather than sitting at Instagram's fixed width. Each post becomes two columns — media on the left, caption and comments beside it — falling back to stacked when the window is too narrow to give the caption its minimum. Photos drop Instagram's crop-to-fill box and are sized to their own proportions, so nothing is cut off and no blurred plate is drawn behind them. Carousels are enlarged to fit the wider column. Portrait reels, which Instagram flattens into a 4:5 box and crops, are given back more of their height. The right-hand rail is hidden.

**Post pages** (`/p/<id>/` and `/<user>/p/<id>/`). Carousels are enlarged and the column widened to hold them beside a caption. Single photos get the more useful fix: Instagram lays them out two different ways depending on shape, so a tall photo comes out smaller than a carousel in the same place while a square one grows without limit. Both are brought to a consistent width. Landscape photos are deliberately left alone — Instagram's own layout for them is already good.

**Reel pages** (`/<user>/reel/<id>/`, and reels reached through either `/p/` path). The 9:16 box is collapsed to the video's real height and the caption column is widened.

**Text.** Size and line spacing for usernames, captions and comments, on all of the above. Both start at Instagram's own values, so nothing changes until you move a setting.

## Requirements

[Stylus](https://add0n.com/stylus.html) — this is a UserCSS style, not a stylesheet you can drop into a browser on its own.

**Firefox 126 or newer.** `:has()` needs 121 and `zoom` needs 126. On an older build the declarations are dropped rather than erroring, so the style partly applies and carousels stay at stock size.

Chromium is not restricted, and the style was confirmed working under Stylus for ungoogled-chromium on 2026-09-10. No Chromium version floor has been established, so treat anything older than that as untested.

## Install

Published to [userstyles.world](https://userstyles.world/user/boneyland) under the user `boneyland`. Install from there and Stylus will offer updates as new versions are published.

To install this copy instead, open `Instagram.user.css` raw and Stylus will intercept it. Note that a manual install carries no update URL.

## Settings

Fourteen, all exposed through the Stylus settings pane.

| Setting | Default |
| --- | --- |
| Feed: width of the feed, as a % of the window | 80% |
| Feed: never let the feed get narrower than | 780px |
| Feed: width of the photo, as a % of the post | 55% |
| Feed: width the caption needs beside the photo, or it moves underneath | 320px |
| Feed: never let a photo or reel get taller than | 900px |
| Feed: never let a reel get wider than | 550px |
| Feed: never enlarge a multi-photo post by more than (1 = off) | 1.5 |
| Text: size of usernames, captions and comments | 14px |
| Text: spacing between lines of that text | 18px |
| Post page: enlarge a multi-photo post by (1 = off) | 1.5 |
| Post page: total width of a multi-photo post and caption | 1150px |
| Post page: total width of a tall or square single photo and caption | 1150px |
| Reel and post pages: total width of reel and caption together | 950px |
| Reel and post pages: width of the caption column | 380px |

The two post-page settings are coupled: enlarging a carousel needs the column width raised with it, by the media's natural width times the increase. That natural width varies with the post's shape, so the pairing cannot be automatic.

## Known limitations

- **Reels are handled at 9:16 only.** A reel of any other shape keeps Instagram's box on all three reel URLs.
- **Post-page defaults are calibrated against one aspect ratio**, a 3:4 carousel. A squarer or wider post starts wider and will want a wider column at the same scale.
- **`/reels/<id>/` and the floating reel dialog are deliberately untouched.** Both are modals with their own markup, which these rules would not transfer to unchanged.
- **A mixed carousel** — photo and video slides in one post — is the one page shape nothing has been written against, for want of a capture of one.

## Repository layout

| Path | Role |
| --- | --- |
| `Instagram.user.css` | The style. The deliverable. |
| `Instagram-2026*-uploaded.user.css` | Previously published versions, kept for diffing. |
| `CHANGELOG.md` | Release notes per version, and the record of what was removed and why. |
| `USw-notes.md` | The user-facing changelog, for the Notes field on userstyles.world. |
| `docs/rule-notes.md` | Why each rule is written the way it is, and what was measured to get there. |
| `docs/token-overrides.md` | Why the design-token overrides work, and how to measure a token's reach. |
| `verify.py`, `scoped.py` | Verification harness. |

The style itself carries no comments beyond its metadata header — the reasoning lives in `docs/rule-notes.md`, keyed by selector. Read the note for a rule before loosening a guard or changing a number.

## Verifying a change

```
python3 verify.py Instagram.user.css                   # check one file
python3 verify.py old.user.css Instagram.user.css      # prove a change altered nothing
python3 scoped.py --urls Instagram.user.css            # every block vs every URL shape
python3 scoped.py --diff old.user.css new.user.css     # every snapshot, at its own URL
```

`verify.py` checks the metadata with `usercss-meta` — the parser Stylus itself uses — then runs a rule and declaration census in headless Firefox to catch silently dropped syntax, and with two files diffs every computed property of every element. It is blind to URL scoping, which is what `scoped.py` covers.

**Neither script runs from a fresh clone.** Both read `Instagram_snapshots/`, which is not tracked — the snapshots are 273MB of captured pages, and they capture a logged-in session. Capture your own with [SingleFile](https://github.com/gildas-lormeau/SingleFile) before verifying.

## License

MIT.
