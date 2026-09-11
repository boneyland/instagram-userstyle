# Custom-property overrides: why the exceptions work

`CLAUDE.md` (Hard rules) names the five of Instagram's own design tokens this style overrides, and the condition attached to them: each needs `!important` to win the collision **unless** the override is declared on an element closer to the target than Instagram's own declaration.

This file explains that exception, and how to measure how far a token reaches. Read it before adding a sixth override.

## Why a `:root` override is inert

Instagram declares tokens on `:root` **and** on `._aa4c`, a class it puts on `<html>` — the same element, the same (0,1,0) specificity — from a `<style>` in the **body**, so it is later in document order and beats an unprefixed `:root` override every time. A `:root` override without `!important` is therefore inert.

`--system-14-*` is what relies on the exception. It is declared on `article, main, [role="dialog"]` instead, containers that sit nearer the text than anything of Instagram's; pages with none of those get nothing.

`[role="dialog"]` is there because the comments panel on `/reels/<id>/` renders as a **sibling** of `main`, not a descendant, so neither of the other two carriers reaches it. Its React mount carries only a generated id, but the panel itself is a `[role="dialog"]`. `/reels/<id>/` is the only saved page that has one, so this carrier's reach on modals elsewhere was checked live rather than offline (2026-09-10): the floating `/reel/<id>/` and `/p/<id>/` modals both take the text settings, consistently with the size setting's own reach. Modals on other paths were not checked.

Naming a container is not always enough on its own. A carrier only works if some rule **below** it reads the token; declaring one on a descendant cannot change a value an ancestor already computed. `.xvs91rp` is the case that caught this out: it reads `--system-14-font-size` and nothing else, so on `/reels/<id>/`, where it is the only token reader under `main`, the line-height token was inherited by 1826 elements and read by none — the text kept a computed `18px` inherited from `body._ar45`. Such a class needs the missing property paired onto it by hand; see the rule beside the carriers in the style.

## Why naming containers beats `!important` on `:root`

Not only for scope — `!important` on `:root` reaches every button, textarea and label, because `._ar45` sets `body`'s font-size from these tokens and the rest inherits — but because a `:root` selector's inertness depends on where Instagram puts a `<style>` tag. If that ever moves into the head, the selector starts winning and the feature silently goes site-wide. Naming containers pins the scope to this file.

## Measuring reach

How far a token reaches is decided by which of Instagram's components read it *and* by where you declare it. Both are answerable only against a real page.

Measure by counting elements whose computed value changes, not by listing the classes you think read the token — a hand-written class list missed `.xvs91rp`, the reel caption, and produced a table that pointed the wrong way.
