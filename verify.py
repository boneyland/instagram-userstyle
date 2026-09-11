#!/usr/bin/env python3
"""
Verify a userstyle, and optionally prove a refactor changed nothing.

    python3 verify.py Instagram.user.css
    python3 verify.py Instagram.user.css Instagram-nested.user.css

With one file it checks that file. With two it additionally proves the second
is computationally identical to the first, by applying each to the saved
Instagram snapshot and diffing every computed property of every element.

Checks
  1. metadata  - parsed by usercss-meta, the same library Stylus itself uses.
                 Skipped with a warning if node/node_modules are absent.
  2. parse     - Firefox is asked how many rules and declarations survived.
                 Anything Firefox cannot parse is dropped silently, so a
                 shortfall here is how a syntax error actually shows up.
  3. non-empty - the sheet must change something on the real snapshot.
                 Without this a stylesheet that silently became a no-op would
                 pass check 4 trivially.
  4. identical - (two files only) every computed property of every element
                 must match between the two.

Exit status is 0 only if every check passed.
"""

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
SNAPSHOTS = os.path.join(HERE, "Instagram_snapshots")
TAB = 4


# --------------------------------------------------------------------------
# Turning a .user.css into something a browser will apply
# --------------------------------------------------------------------------

def var_defaults(css):
    """The :root block Stylus builds from the @var lines and concatenates
    into every section of the style."""
    out = []
    for m in re.finditer(r'@var\s+(range|number|text|color)\s+([\w-]+)\s+'
                         r'"[^"]*"\s+(\[.*?\]|\S+)', css):
        name, raw = m.group(2), m.group(3).strip()
        if raw.startswith('['):
            parts = [p.strip() for p in raw[1:-1].split(',')]
            nums = [p for p in parts if not p.startswith('"')]
            units = [p.strip('"') for p in parts if p.startswith('"')]
            out.append(f"--{name}: {nums[0]}{units[0] if units else ''};")
        else:
            out.append(f"--{name}: {raw.strip(chr(34))};")
    return ":root{\n" + "\n".join(out) + "\n}\n"


def strip_wrappers(css):
    """Remove the metadata header and unwrap every @-moz-document block.

    Firefox does not honour @-moz-document in an author sheet, so the rules
    have to be lifted out of it to take effect at all. Both files get the
    same treatment, so a comparison between them stays valid.
    """
    css = re.sub(r'/\*\s*==UserStyle==.*?==/UserStyle==\s*\*/', '', css, flags=re.S)
    out, i = [], 0
    while True:
        m = re.search(r'@-moz-document[^{]*\{', css[i:])
        if not m:
            out.append(css[i:])
            break
        out.append(css[i:i + m.start()])
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
        out.append(css[j:k - 1])
        i = k
    return "".join(out)


def prepare(path):
    css = open(path, encoding="utf-8").read()
    return var_defaults(css) + strip_wrappers(css)


# --------------------------------------------------------------------------
# Check 1 - metadata, via Stylus's own parser
# --------------------------------------------------------------------------

NODE_SRC = r"""
const meta = require('usercss-meta');
const fs = require('fs');
const out = [];
for (const f of process.argv.slice(2)) {
  const src = fs.readFileSync(f, 'utf8');
  try {
    const { metadata } = meta.parse(src, { mandatoryKeys: ['name', 'namespace', 'version'] });
    out.push({ file: f, ok: true,
               name: metadata.name, version: metadata.version,
               namespace: metadata.namespace, license: metadata.license,
               preprocessor: metadata.preprocessor,
               vars: Object.keys(metadata.vars || {}) });
  } catch (e) {
    out.push({ file: f, ok: false, error: e.message,
               index: e.index === undefined ? null : e.index });
  }
}
console.log(JSON.stringify(out));
"""


def check_stray_var(paths):
    """usercss-meta scans the whole file for @var, not just the metadata
    block, so the literal text "@var" inside an ordinary CSS comment is read
    as a malformed variable declaration and the style fails to install.
    Only @var behaves this way -- @name, @license and friends in comments are
    harmless -- so it is worth calling out by name."""
    ok = True
    for p in paths:
        s = open(p, encoding="utf-8").read()
        end = s.index("==/UserStyle==") if "==/UserStyle==" in s else 0
        for n, line in enumerate(s.split("\n"), 1):
            off = sum(len(x) + 1 for x in s.split("\n")[:n - 1])
            if "@var" in line and off > end:
                ok = False
                print(f"  x {os.path.basename(p)}:{n}  the text \"@var\" appears "
                      f"outside the metadata block")
                print(f"      {line.strip()}")
                print(f"      usercss-meta parses this as a variable declaration; "
                      f"reword it")
    if ok:
        print("  + no stray \"@var\" outside the metadata block")
    return ok


def check_metadata(paths):
    if not shutil.which("node") or not os.path.isdir(os.path.join(HERE, "node_modules")):
        print("  ~ SKIP  node or node_modules missing "
              "(npm install usercss-meta to enable)")
        return None
    src = os.path.join(tempfile.gettempdir(), "usercss_meta_check.js")
    open(src, "w").write(NODE_SRC)
    env = dict(os.environ, NODE_PATH=os.path.join(HERE, "node_modules"))
    r = subprocess.run(["node", src] + paths, cwd=HERE, env=env,
                       capture_output=True, text=True)
    if r.returncode != 0:
        print("  x FAIL  could not run usercss-meta:\n" + r.stderr.strip())
        return False
    ok = True
    for e in json.loads(r.stdout):
        base = os.path.basename(e["file"])
        if e["ok"]:
            print(f"  + {base}")
            print(f"      name={e['name']!r} version={e['version']} "
                  f"license={e['license']}")
            print(f"      namespace={e['namespace']}")
            print(f"      preprocessor={e['preprocessor']} "
                  f"@var x{len(e['vars'])}: {', '.join(e['vars'])}")
        else:
            ok = False
            print(f"  x {base}: {e['error']}"
                  + (f" (at char {e['index']})" if e["index"] is not None else ""))
    return ok


# --------------------------------------------------------------------------
# Checks 2-4 - drive a real Firefox over the saved snapshot
# --------------------------------------------------------------------------

PAGE_JS = r"""
(function () {
  function say(s) { dump("@@ " + s + "\n"); }
  var SHEETS = __SHEETS__;
  var els = Array.prototype.slice.call(document.querySelectorAll("*"));

  function census(css) {
    var s = document.createElement("style");
    s.textContent = css;
    document.head.appendChild(s);
    var rules = 0, decls = 0;
    (function walk(list) {
      for (var i = 0; i < list.length; i++) {
        var r = list[i];
        if (r.style) { rules++; decls += r.style.length; }
        if (r.cssRules) walk(r.cssRules);
      }
    })(s.sheet.cssRules);
    s.remove();
    return { rules: rules, decls: decls };
  }

  // Firefox's computed-style enumeration is not stable between snapshots:
  // it can list one custom property twice, which displaces another from
  // that snapshot's list even though the total count is unchanged. Keying
  // the comparison off each snapshot's own enumeration therefore either
  // skips real properties or invents differences against undefined.
  // So the key list is fixed up front -- every name enumerated anywhere
  // with no stylesheet applied, plus every custom property the sheets
  // themselves declare -- and each snapshot reads that same list by name.
  // getPropertyValue works regardless of enumeration, and a property that
  // does not apply reads as "" consistently on both sides.
  var KEYS = (function () {
    var k = {}, i, j;
    for (i = 0; i < els.length; i++) {
      var cs = getComputedStyle(els[i]);
      for (j = 0; j < cs.length; j++) k[cs[j]] = 1;
    }
    var declared = __DECLARED__;
    for (i = 0; i < declared.length; i++) k[declared[i]] = 1;
    return Object.keys(k);
  })();
  say("keys " + KEYS.length);

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

  say("elements " + els.length);

  var names = Object.keys(SHEETS);
  var snaps = {}, counts = {};
  for (var n = 0; n < names.length; n++) {
    counts[names[n]] = census(SHEETS[names[n]]);
    say("census " + names[n] + " " + counts[names[n]].rules
        + " " + counts[names[n]].decls);
  }

  var base = snap("");
  for (var n = 0; n < names.length; n++) snaps[names[n]] = snap(SHEETS[names[n]]);

  // Firefox's computed-style enumeration sometimes lists one custom
  // property twice, which displaces another from that snapshot's key list
  // even though the total count is unchanged. Iterating only the left
  // side would silently skip the displaced property; iterating the union
  // instead compares a real value against undefined and invents a
  // difference. So: walk the union, but treat a key missing from either
  // side as unobservable rather than as a mismatch, and count how often
  // that happens so it never hides silently.
  function union(x, y) {
    var k = {}, p;
    for (p in x) k[p] = 1;
    for (p in y) k[p] = 1;
    return k;
  }
  var nSkipped = 0;
  function differs(x, y, p) {
    if (x[p] === undefined || y[p] === undefined) { nSkipped++; return false; }
    return x[p] !== y[p];
  }

  // check 3: each sheet must actually change the page
  for (var n = 0; n < names.length; n++) {
    var changed = 0, cur = snaps[names[n]];
    for (var i = 0; i < els.length; i++) {
      var ks = union(cur[i], base[i]);
      for (var p in ks) if (differs(cur[i], base[i], p)) changed++;
    }
    say("changed " + names[n] + " " + changed);
  }

  // check 4: sheets must agree with each other
  if (names.length > 1) {
    var a = snaps[names[0]], b = snaps[names[1]], diffs = [];
    var nCustom = 0, nStandard = 0;
    for (var i = 0; i < els.length; i++) {
      var ks = union(a[i], b[i]);
      for (var p in ks) {
        if (differs(a[i], b[i], p)) {
          var e = els[i];
          if (p.indexOf("--") === 0) nCustom++; else nStandard++;
          diffs.push("<" + e.tagName.toLowerCase()
            + (e.id ? " id=" + e.id : "")
            + (e.className && e.className.baseVal === undefined
                 ? ' class="' + String(e.className).slice(0, 60) + '"' : "")
            + ">  " + p + ": " + names[0] + "=" + a[i][p]
            + "  " + names[1] + "=" + b[i][p]);
        }
      }
    }
    say("diffcount " + diffs.length);
    say("diffkind " + nCustom + " " + nStandard);
    say("skipped " + nSkipped);
    for (var d = 0; d < Math.min(diffs.length, 40); d++) say("diff " + diffs[d]);
  }
  say("done");
})();
"""


def find_snapshot():
    for f in sorted(os.listdir(SNAPSHOTS)):
        if f.startswith("Instagram (") and f.endswith(".html"):
            return os.path.join(SNAPSHOTS, f)
    return None


def run_browser(sheets, workdir):
    snap = find_snapshot()
    if not snap:
        print(f"  x FAIL  no 'Instagram (*).html' snapshot found in {SNAPSHOTS}")
        return None
    html = open(snap, encoding="utf-8", errors="replace").read()
    declared = sorted({m for s in sheets.values()
                       for m in re.findall(r'(--[\w-]+)\s*:', s)})
    js = (PAGE_JS.replace("__SHEETS__", json.dumps(sheets))
                 .replace("__DECLARED__", json.dumps(declared)))
    tag = "<script>" + js + "</script>"
    # The snapshot contains more than one "</body>"; only the last one is the
    # real end of the document. Injecting at the first lands inside markup
    # that never runs, and the script silently does nothing.
    i = html.rfind("</body>")
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
        capture_output=True, text=True, timeout=300)
    lines = [l[3:] for l in (r.stdout + r.stderr).splitlines() if l.startswith("@@ ")]
    if not lines or lines[-1] != "done":
        print("  x FAIL  browser run did not complete")
        print("\n".join((r.stdout + r.stderr).splitlines()[-15:]))
        return None
    return lines


def main():
    paths = sys.argv[1:] or ["Instagram.user.css"]
    paths = [p if os.path.isabs(p) else os.path.join(HERE, p) for p in paths]
    for p in paths:
        if not os.path.exists(p):
            sys.exit(f"no such file: {p}")
    names = [os.path.basename(p).replace(".user.css", "") for p in paths]

    results = {}

    print("\n[1] metadata (usercss-meta, the parser Stylus uses)")
    results["stray-@var"] = check_stray_var(paths)
    results["metadata"] = check_metadata(paths)

    sheets = {n: prepare(p) for n, p in zip(names, paths)}
    workdir = tempfile.mkdtemp(prefix="userstyle-verify-")
    try:
        print("\n[2] parse + [3] effect + [4] equivalence (headless Firefox, real snapshot)")
        lines = run_browser(sheets, workdir)
        if lines is None:
            results["browser"] = False
        else:
            info = {}
            diffs = []
            for l in lines:
                k, _, rest = l.partition(" ")
                if k == "diff":
                    diffs.append(rest)
                elif k in ("census", "changed"):
                    who, _, v = rest.partition(" ")
                    info.setdefault(k, {})[who] = v
                else:
                    info[k] = rest

            print(f"  elements compared: {info.get('elements')}")

            ok_parse = True
            for n in names:
                rules, decls = info["census"][n].split()
                print(f"  {n}: {rules} rules, {decls} declarations survived parsing")
                if int(decls) == 0:
                    ok_parse = False
            if len(names) > 1:
                d = [int(info["census"][n].split()[1]) for n in names]
                if d[0] != d[1]:
                    print(f"  x FAIL  declaration counts differ: {d[0]} vs {d[1]} "
                          f"-- Firefox dropped something")
                    ok_parse = False
                else:
                    print(f"  + both files kept the same {d[0]} declarations")
            results["parse"] = ok_parse

            ok_effect = True
            for n in names:
                c = int(info["changed"][n])
                print(f"  {n}: changes {c} computed properties vs no stylesheet")
                if c == 0:
                    print(f"  x FAIL  {n} is a no-op -- later checks would pass vacuously")
                    ok_effect = False
            results["effect"] = ok_effect

            if len(names) > 1:
                n_diff = int(info.get("diffcount", "0"))
                if n_diff == 0:
                    print(f"  + {names[0]} and {names[1]} are computationally identical")
                    results["equivalence"] = True
                else:
                    custom, standard = (info.get("diffkind", "0 0").split() + ["0"])[:2]
                    print(f"  x FAIL  {n_diff} property mismatches "
                          f"({standard} on standard properties, "
                          f"{custom} on custom properties)")
                    if standard == "0":
                        print("          no standard property differs, so nothing renders "
                              "differently.\n"
                              "          Custom-property-only drift usually means the "
                              "declarations involved\n"
                              "          are dead: set, inherited, and never read.")
                    for d in diffs:
                        print("      " + d)
                    results["equivalence"] = False
                sk = int(info.get("skipped", "0"))
                if sk:
                    print(f"  ~ {sk} property reads were unobservable on one side "
                          f"(Firefox enumeration quirk) and were not compared")
    finally:
        shutil.rmtree(workdir, ignore_errors=True)

    print("\n" + "-" * 62)
    failed = [k for k, v in results.items() if v is False]
    skipped = [k for k, v in results.items() if v is None]
    for k, v in results.items():
        print(f"  {'PASS' if v else 'SKIP' if v is None else 'FAIL'}  {k}")
    if failed:
        print(f"\nFAILED: {', '.join(failed)}")
        return 1
    print("\nAll checks passed." + (f" (skipped: {', '.join(skipped)})" if skipped else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
