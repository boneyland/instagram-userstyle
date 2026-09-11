#!/usr/bin/env python3
"""
Reason about @-moz-document URL scoping, which verify.py cannot see.

    python3 scoped.py Instagram.user.css https://www.instagram.com/p/ABC/
    python3 scoped.py --urls Instagram.user.css
    python3 scoped.py --diff old.user.css Instagram.user.css

verify.py's prepare() unwraps every @-moz-document block unconditionally. That
is what makes its two-file mode a valid equivalence proof -- both sides get the
same treatment -- but it means a change to a block's CONDITION produces no diff
at all. verify.py also only ever loads the feed snapshot. So a passing run says
"the rules still parse and still do the same thing on the feed", never "this
change is correct".

This fills both gaps. It keeps only the blocks whose condition matches a given
URL, and it measures every snapshot at the URL that snapshot was really saved
from -- SingleFile records it in a comment at the top of the file, so there is
no table here to fall out of date.

Modes
  <style> <url>   which blocks apply to that URL, and the CSS they produce
  --urls <style>  full-match every block condition against a table of URL
                  shapes: the ones each block must cover, and the ones it must
                  keep excluding
  --diff  a b     apply a and b to every snapshot at its own URL and diff every
                  computed property of every element. This is the measurement
                  to run after changing a regexp()

Exit status is 0 unless a browser run or a file read fails. A diff is a result,
not a failure -- read the table.
"""

import json
import os
import re
import subprocess
import sys
import tempfile
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from verify import var_defaults, SNAPSHOTS  # the :root block Stylus builds from the header


# --------------------------------------------------------------------------
# Splitting a style into blocks, and deciding which apply to a URL
# --------------------------------------------------------------------------

def split_blocks(css):
    """Yield (condition, body) for each @-moz-document block, and
    (None, body) for the CSS between them."""
    css = re.sub(r'/\*\s*==UserStyle==.*?==/UserStyle==\s*\*/', '', css, flags=re.S)
    i = 0
    while True:
        m = re.search(r'@-moz-document([^{]*)\{', css[i:])
        if not m:
            yield None, css[i:]
            return
        yield None, css[i:i + m.start()]
        j = i + m.end()
        depth, k, in_str = 1, j, False
        while depth:
            c = css[k]
            if c == '"':
                in_str = not in_str
            elif not in_str and c == '{':
                depth += 1
            elif not in_str and c == '}':
                depth -= 1
            k += 1
        yield m.group(1).strip(), css[j:k - 1]
        i = k


def cond_matches(cond, url):
    """Does an @-moz-document condition list match this URL?

    A condition is a comma-separated list of functions and matches if ANY of
    them does. regexp() is matched against the WHOLE url, which is why this
    uses fullmatch rather than search.
    """
    for m in re.finditer(r'(domain|url-prefix|url|regexp)\(\s*"([^"]*)"\s*\)', cond):
        kind, val = m.group(1), m.group(2)
        if kind == "domain":
            host = re.sub(r'^https?://', '', url).split('/')[0]
            if host == val or host.endswith("." + val):
                return True
        elif kind == "url-prefix":
            if url.startswith(val):
                return True
        elif kind == "url":
            if url == val:
                return True
        elif kind == "regexp":
            # The captured text is raw CSS source, where a backslash is itself
            # escaped: the file's "\\." is a CSS string escape meaning ONE
            # backslash. Handing that to re unconverted makes every condition
            # fail silently -- it looks like "no block applies", not an error.
            if re.fullmatch(val.replace("\\\\", "\\"), url):
                return True
    return False


def blocks_for(css, url):
    return [c for c, _ in split_blocks(css) if c and cond_matches(c, url)]


def prepare_scoped(path, url):
    """The CSS this URL actually gets: the header's variable defaults, the
    top-level rules, and only those blocks whose condition matches."""
    css = open(path, encoding="utf-8").read()
    body = "".join(b for c, b in split_blocks(css)
                   if c is None or cond_matches(c, url))
    return var_defaults(css) + body


# --------------------------------------------------------------------------
# Snapshots, and the URL each was really saved from
# --------------------------------------------------------------------------

def snapshot_url(path):
    """SingleFile writes `url: https://...` in a comment at the top of the
    file. Read it rather than keeping a table here that can go stale."""
    with open(path, "rb") as f:
        head = f.read(3000).decode("utf-8", errors="replace")
    m = re.search(r'url:\s*(https?://\S+)', head)
    return m.group(1) if m else None


def find_snapshots():
    out = []
    for f in sorted(os.listdir(SNAPSHOTS)):
        if f.endswith(".html"):
            u = snapshot_url(os.path.join(SNAPSHOTS, f))
            if u:
                out.append((f, u))
    return out


# --------------------------------------------------------------------------
# Driving Firefox over one snapshot with two sheets
# --------------------------------------------------------------------------

PAGE_JS = r"""
(function () {
  function say(s) { dump("@@ " + s + "\n"); }
  var A = __A__, B = __B__;
  var els = Array.prototype.slice.call(document.querySelectorAll("*"));

  // Firefox's computed-style enumeration is not stable between snapshots: it
  // can list one custom property twice, displacing another. So fix the key
  // list up front and read it by name on both sides -- same reasoning, and
  // same fix, as verify.py.
  var KEYS = (function () {
    var k = {}, i, j;
    for (i = 0; i < els.length; i++) {
      var cs = getComputedStyle(els[i]);
      for (j = 0; j < cs.length; j++) k[cs[j]] = 1;
    }
    var d = __DECL__;
    for (i = 0; i < d.length; i++) k[d[i]] = 1;
    return Object.keys(k);
  })();

  function snap(css) {
    var s = null;
    if (css) {
      s = document.createElement("style");
      s.textContent = css;
      document.head.appendChild(s);
    }
    var rows = new Array(els.length);
    for (var i = 0; i < els.length; i++) {
      var cs = getComputedStyle(els[i]), o = {};
      for (var j = 0; j < KEYS.length; j++) o[KEYS[j]] = cs.getPropertyValue(KEYS[j]);
      rows[i] = o;
    }
    if (s) s.remove();
    return rows;
  }

  var a = snap(A), b = snap(B);
  var nStd = 0, nCus = 0, byProp = {}, shown = [];
  for (var i = 0; i < els.length; i++) {
    for (var p in a[i]) {
      // a key missing from one side is unobservable, not a difference
      if (a[i][p] === undefined || b[i][p] === undefined) continue;
      if (a[i][p] === b[i][p]) continue;
      if (p.indexOf("--") === 0) nCus++; else nStd++;
      byProp[p] = (byProp[p] || 0) + 1;
      if (p.indexOf("--") !== 0 && shown.length < 25) {
        var e = els[i];
        shown.push("<" + e.tagName.toLowerCase()
          + (e.className && typeof e.className === "string"
               ? "." + e.className.trim().split(/\s+/).slice(0, 3).join(".") : "")
          + ">  " + p + ": " + a[i][p] + " -> " + b[i][p]);
      }
    }
  }
  say("elements " + els.length);
  say("counts " + nStd + " " + nCus);
  var ks = Object.keys(byProp).sort(function (x, y) { return byProp[y] - byProp[x]; });
  for (var i = 0; i < ks.length; i++) say("prop " + byProp[ks[i]] + " " + ks[i]);
  for (var i = 0; i < shown.length; i++) say("el " + shown[i]);
  say("done");
})();
"""


def run_pair(snapshot, sheet_a, sheet_b):
    """Load one snapshot and diff every computed property under two sheets."""
    path = os.path.join(SNAPSHOTS, snapshot)
    html = open(path, encoding="utf-8", errors="replace").read()
    decl = sorted({m for s in (sheet_a, sheet_b)
                   for m in re.findall(r'(--[\w-]+)\s*:', s)})
    js = (PAGE_JS.replace("__A__", json.dumps(sheet_a))
                 .replace("__B__", json.dumps(sheet_b))
                 .replace("__DECL__", json.dumps(decl)))
    workdir = tempfile.mkdtemp(prefix="scoped-")
    try:
        # The snapshot contains more than one "</body>"; only the last is the
        # real end of the document. Injecting at the first lands inside markup
        # that never runs, and the script silently does nothing.
        i = html.rfind("</body>")
        tag = "<script>" + js + "</script>"
        html = (html[:i] + tag + html[i:]) if i != -1 else (html + tag)
        page = os.path.join(workdir, "page.html")
        open(page, "w", encoding="utf-8").write(html)

        profile = os.path.join(workdir, "profile")
        os.makedirs(profile, exist_ok=True)
        open(os.path.join(profile, "user.js"), "w").write(
            'user_pref("browser.dom.window.dump.enabled", true);\n')

        r = subprocess.run(
            ["firefox", "--headless", "--profile", profile,
             "--screenshot", os.path.join(workdir, "shot.png"),
             "--window-size=1638,900", "file://" + page],
            capture_output=True, text=True, timeout=900)
        lines = [l[3:] for l in (r.stdout + r.stderr).splitlines()
                 if l.startswith("@@ ")]
        if not lines or lines[-1] != "done":
            return None
        return lines
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


# --------------------------------------------------------------------------
# Modes
# --------------------------------------------------------------------------

# The URL shapes a change to a regexp() has to be checked against: the pages
# the style is meant to reach, and the near misses it must keep out. Extend
# this when a new page type is taken on.
URL_SHAPES = [
    ("feed",                        "https://www.instagram.com/"),
    ("profile",                     "https://www.instagram.com/someuser/"),
    ("explore",                     "https://www.instagram.com/explore/"),
    ("reel page",                   "https://www.instagram.com/someuser/reel/ABC123/"),
    ("post permalink",              "https://www.instagram.com/p/ABC123/"),
    ("post permalink, with user",   "https://www.instagram.com/someuser/p/ABC123/"),
    ("post permalink, with query",  "https://www.instagram.com/p/ABC123/?img_index=3"),
    ("reels, plural path",          "https://www.instagram.com/reels/ABC123/"),
    ("reel, floating dialog",       "https://www.instagram.com/reel/ABC123/"),
    ("reels grid on a profile",     "https://www.instagram.com/someuser/reels/"),
    ("reels audio page",            "https://www.instagram.com/reels/audio/12345/"),
    ("a subdomain",                 "https://help.instagram.com/"),
]


def short(cond, n=46):
    c = " ".join(cond.split())
    return c if len(c) <= n else c[:n - 1] + "…"


def mode_one(style, url):
    css = open(style, encoding="utf-8").read()
    conds = [c for c, _ in split_blocks(css) if c]
    print(f"\n{os.path.basename(style)}  at  {url}\n")
    for c in conds:
        hit = cond_matches(c, url)
        print(f"  {'APPLIES ' if hit else '    -   '}  {short(c, 70)}")
    out = prepare_scoped(style, url)
    print(f"\n  {len(out)} characters of CSS, "
          f"{sum(1 for c in conds if cond_matches(c, url))} of {len(conds)} blocks\n")
    return 0


def mode_urls(style):
    css = open(style, encoding="utf-8").read()
    conds = [c for c, _ in split_blocks(css) if c]
    w = max(len(l) for l, _ in URL_SHAPES) + 2
    print(f"\n{os.path.basename(style)} -- which block claims each URL shape")
    print("regexp() is matched against the whole URL, so these are full matches.\n")
    print(" " * w + "  " + "  ".join(f"[{i}]" for i in range(len(conds))))
    for label, u in URL_SHAPES:
        cells = "  ".join(f" {'X' if cond_matches(c, u) else '.'} " for c in conds)
        print(f"  {label:<{w}}{cells}   {u}")
    print()
    for i, c in enumerate(conds):
        print(f"  [{i}]  {short(c, 90)}")
    print()
    return 0


def mode_diff(a, b):
    snaps = find_snapshots()
    if not snaps:
        print("  x FAIL  no snapshots with a SingleFile url: comment found")
        return 1
    na, nb = (os.path.basename(p).replace(".user.css", "") for p in (a, b))
    print(f"\nComputed-property diff, every snapshot at its own URL")
    print(f"  {na}  ->  {nb}\n")

    rows, failed = [], False
    for snap, url in snaps:
        sa, sb = prepare_scoped(a, url), prepare_scoped(b, url)
        ba, bb = blocks_for(open(a, encoding='utf-8').read(), url), \
                 blocks_for(open(b, encoding='utf-8').read(), url)
        lines = run_pair(snap, sa, sb)
        if lines is None:
            print(f"  x FAIL  browser run did not complete on {snap}")
            failed = True
            continue
        info = {}
        props, els = [], []
        for l in lines:
            k, _, rest = l.partition(" ")
            if k == "prop":
                props.append(rest)
            elif k == "el":
                els.append(rest)
            else:
                info[k] = rest
        std, cus = info.get("counts", "0 0").split()
        rows.append((snap, url, info.get("elements", "?"), int(std), int(cus),
                     len(ba), len(bb), props, els))

    w = max(len(r[0]) for r in rows)
    print(f"  {'snapshot':<{w}}  {'els':>5}  {'std':>5}  {'custom':>7}  blocks")
    print(f"  {'-' * w}  {'-' * 5}  {'-' * 5}  {'-' * 7}  ------")
    for snap, url, n, std, cus, ba, bb, _, _ in rows:
        blocks = f"{ba}" if ba == bb else f"{ba} -> {bb}"
        mark = "   " if (std or cus) else " + "
        print(f"{mark}{snap:<{w}}  {n:>5}  {std:>5}  {cus:>7}  {blocks}")
    print()

    for snap, url, n, std, cus, ba, bb, props, els in rows:
        if not (std or cus):
            continue
        print(f"  {snap}   {url}")
        for p in props:
            cnt, _, name = p.partition(" ")
            print(f"      {cnt:>5}  {name}")
        if els:
            print(f"      first {len(els)} changed elements, standard properties only:")
            for e in els:
                print(f"        {e}")
        print()

    if all(r[3] == 0 and r[4] == 0 for r in rows):
        print("  + no snapshot renders differently\n")
    else:
        moved = [r[0] for r in rows if r[3] or r[4]]
        print(f"  ~ {len(moved)} of {len(rows)} snapshots changed: {', '.join(moved)}")
        print("    A custom-only change is a token that is set, inherited and never")
        print("    read -- it does not render. Check the property list above for")
        print("    font-size, line-height or zoom, which usually mean a container")
        print("    holding text was resized by mistake.\n")
    return 1 if failed else 0


def resolve(p):
    """Bare filenames mean files next to this script, as in verify.py, so the
    tool works the same from any directory."""
    p = p if os.path.isabs(p) else os.path.join(HERE, p)
    if not os.path.exists(p):
        sys.exit(f"no such file: {p}")
    return p


def main():
    av = sys.argv[1:]
    if not av:
        print(__doc__)
        return 2
    if av[0] == "--urls" and len(av) == 2:
        return mode_urls(resolve(av[1]))
    if av[0] == "--diff" and len(av) == 3:
        return mode_diff(resolve(av[1]), resolve(av[2]))
    if len(av) == 2 and not av[0].startswith("--"):
        return mode_one(resolve(av[0]), av[1])
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main())
