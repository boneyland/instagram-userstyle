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
import signal
import subprocess
import sys
import tempfile
import threading
import time

HERE = os.path.dirname(os.path.abspath(__file__))
SNAPSHOTS = os.path.join(HERE, "Instagram_snapshots")
TAB = 4

# A run must never be able to take the machine down with it. The snapshots are
# 20-105MB of SingleFile HTML and the largest holds 23589 elements, so a probe
# that keeps a full computed-style table per sheet costs gigabytes. On a 15GB
# machine backed by zram -- where swap is compressed into the same RAM it is
# meant to relieve -- that wedges the desktop hard enough to need a power
# cycle, which is what happened on 2026-09-21 before this guard existed.
#
# Two defences, because either alone is not enough. The probes below keep one
# joined string per element rather than a table (see PROBE_CORE), and every
# Firefox launch goes through run_firefox_guarded, which kills the browser if
# free memory falls past a floor. Override the floor with VERIFY_FLOOR_MB.
MEM_FLOOR_MB = int(os.environ.get("VERIFY_FLOOR_MB", "2200"))


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
    for m in re.finditer(r'@var\s+select\s+([\w-]+)\s+"[^"]*"\s+(\{.*?\}|\[.*?\])',
                         css, flags=re.S):
        out.append(f"--{m.group(1)}: {select_default(m.group(2))};")
    return ":root{\n" + "\n".join(out) + "\n}\n"


def select_default(block):
    """The option a select variable starts on.

    Both spellings usercss-meta accepts are handled: a list of bare values,
    and a map of "key:Label" to value. The default is the entry marked with a
    trailing "*" on either side of the pair, and the first entry when none is.
    """
    quoted = re.findall(r'"((?:[^"\\]|\\.)*)"', block)
    if block.lstrip().startswith('{'):
        pairs = list(zip(quoted[::2], quoted[1::2]))
    else:
        pairs = [(v, v) for v in quoted]
    for key, value in pairs:
        if key.endswith('*') or value.endswith('*'):
            return value.rstrip('*')
    return pairs[0][1].rstrip('*') if pairs else ''


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
# Driving Firefox without putting the machine at risk
# --------------------------------------------------------------------------

def mem_available_mb():
    """MemAvailable, which is what actually predicts thrashing -- MemFree
    ignores reclaimable cache and reads far lower than the truth."""
    try:
        with open("/proc/meminfo") as f:
            for line in f:
                if line.startswith("MemAvailable:"):
                    return int(line.split()[1]) // 1024
    except OSError:
        pass
    return None          # unreadable: the watchdog then simply does not fire


FIREFOX_PREFS = (
    'user_pref("browser.dom.window.dump.enabled", true);\n'
    # One content process, so there is a single thing to watch and kill.
    'user_pref("dom.ipc.processCount", 1);\n'
    # Cap the JS heap. The probe is bounded by design, but this turns a
    # pathological page into a script error rather than a machine-wide OOM.
    'user_pref("javascript.options.mem.max", 3072);\n'
    'user_pref("browser.sessionstore.resume_from_crash", false);\n'
    # Decoded image surfaces dominate RSS on these captures -- they are
    # SingleFile pages with every image inlined as base64. Layout reads
    # intrinsic dimensions from the image headers, not from this cache, so
    # capping it cuts memory without moving anything the probe measures.
    'user_pref("image.mem.surfacecache.max_size_kb", 262144);\n'
    'user_pref("image.animation_mode", "none");\n')


def _find_last(path, needle, window=1 << 20):
    """Byte offset of the last `needle` in a file, without reading it all."""
    size = os.path.getsize(path)
    with open(path, "rb") as f:
        pos, overlap = size, len(needle)
        while pos > 0:
            start = max(0, pos - window)
            f.seek(start)
            buf = f.read(min(window + overlap, size - start))
            i = buf.rfind(needle)
            if i != -1:
                return start + i
            pos = start
    return -1


def write_page(src, tag, dest, chunk=1 << 20):
    """Copy a snapshot to `dest` with `tag` injected before the LAST </body>.

    Streamed in binary on purpose. Read as one string and re-joined around the
    tag, a 105MB capture costs several hundred MB of Python heap before
    Firefox has even started -- and the snapshots are the reason this harness
    has a memory floor at all.

    The snapshot contains more than one "</body>"; only the last is the real
    end of the document. Injecting at the first lands inside markup that never
    runs, and the probe silently does nothing.
    """
    off = _find_last(src, b"</body>")
    if off == -1:
        off = os.path.getsize(src)       # no </body>: append, as before
    with open(src, "rb") as r, open(dest, "wb") as w:
        remaining = off
        while remaining > 0:
            buf = r.read(min(chunk, remaining))
            if not buf:
                break
            w.write(buf)
            remaining -= len(buf)
        w.write(tag.encode("utf-8"))
        shutil.copyfileobj(r, w, chunk)


def make_workdir(prefix):
    """Scratch space for the page copy and the browser profile.

    The page copy is as large as the snapshot. On a system where the system
    temp directory is tmpfs -- Fedora's /tmp is -- that copy is held in RAM,
    which is the one place this harness is trying not to spend. Set
    VERIFY_WORKDIR to a disk-backed directory to move it off RAM.
    """
    return tempfile.mkdtemp(prefix=prefix, dir=os.environ.get("VERIFY_WORKDIR"))


def write_profile(workdir):
    profile = os.path.join(workdir, "profile")
    os.makedirs(profile, exist_ok=True)
    open(os.path.join(profile, "user.js"), "w").write(FIREFOX_PREFS)
    return profile


def run_firefox_guarded(page, workdir, timeout=900, floor_mb=None):
    """Render `page` in headless Firefox and return (lines, error, low_mb).

    `lines` are the "@@ " lines the probe dumped, or None on failure, in which
    case `error` says why. `low_mb` is the lowest MemAvailable seen, which is
    worth printing even on success -- it is the only warning that a run came
    close to the floor.

    The watchdog polls MemAvailable and SIGKILLs the whole process group if it
    drops past the floor. Killing the browser costs one run; letting the
    kernel resolve it costs the session. start_new_session gives Firefox its
    own group so no child survives the kill.
    """
    floor = MEM_FLOOR_MB if floor_mb is None else floor_mb
    profile = write_profile(workdir)
    proc = subprocess.Popen(
        ["firefox", "--headless", "--profile", profile,
         "--screenshot", os.path.join(workdir, "shot.png"),
         "--window-size=1638,900", "file://" + page],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        start_new_session=True)

    state = {"killed": None, "low": mem_available_mb()}

    def watch():
        while proc.poll() is None:
            m = mem_available_mb()
            if m is None:
                return
            if state["low"] is None or m < state["low"]:
                state["low"] = m
            if m < floor:
                state["killed"] = f"MemAvailable {m}MB fell below the {floor}MB floor"
                try:
                    os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
                except OSError:
                    pass
                return
            time.sleep(0.4)

    threading.Thread(target=watch, daemon=True).start()
    try:
        out, err = proc.communicate(timeout=timeout)
    except subprocess.TimeoutExpired:
        state["killed"] = f"no result after {timeout}s"
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
        except OSError:
            pass
        out, err = proc.communicate()

    if state["killed"]:
        return None, state["killed"], state["low"]
    lines = [l[3:] for l in (out + err).splitlines() if l.startswith("@@ ")]
    if not lines or lines[-1] != "done":
        tail = "\n".join((out + err).splitlines()[-15:])
        return None, "browser run did not complete\n" + tail, state["low"]
    return lines, None, state["low"]


# --------------------------------------------------------------------------
# Checks 2-4 - drive a real Firefox over the saved snapshot
# --------------------------------------------------------------------------

# Shared by both probes here and in scoped.py. A row is every value in KEYS
# joined by one separator character, not an object of KEYS.length strings:
# same information, but one string per element instead of several hundred,
# which is the difference between a run that fits in memory and one that does
# not. Rows are split back apart one element at a time, only where they
# differ, so the expanded form never exists for more than one element at once.
PROBE_CORE = r"""
  var SEP = String.fromCharCode(1);

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
  function probeKeys(els, declared) {
    var k = {}, i, j;
    for (i = 0; i < els.length; i++) {
      var cs = getComputedStyle(els[i]);
      for (j = 0; j < cs.length; j++) k[cs[j]] = 1;
    }
    for (i = 0; i < declared.length; i++) k[declared[i]] = 1;
    return Object.keys(k);
  }

  function probeRows(css, els, KEYS) {
    var s = null;
    if (css) {
      s = document.createElement("style");
      s.textContent = css;
      document.head.appendChild(s);
    }
    var rows = new Array(els.length);
    for (var i = 0; i < els.length; i++) {
      var cs = getComputedStyle(els[i]), parts = new Array(KEYS.length);
      for (var j = 0; j < KEYS.length; j++) parts[j] = cs.getPropertyValue(KEYS[j]);
      rows[i] = parts.join(SEP);
    }
    if (s) s.remove();
    return rows;
  }

  function probeSplit(row) { return row.split(SEP); }
"""

PAGE_JS = r"""
(function () {
  function say(s) { dump("@@ " + s + "\n"); }
__CORE__
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

  var KEYS = probeKeys(els, __DECLARED__);
  say("keys " + KEYS.length);

  function snap(css) { return probeRows(css, els, KEYS); }

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

  // Both sides read the same fixed KEYS list by name, so a row always has
  // exactly KEYS.length fields and the two sides always line up by index --
  // the enumeration instability the key list exists to defeat cannot reach
  // this far. The undefined guard is kept anyway, and counted, so that if
  // that assumption ever stops holding it surfaces instead of hiding.
  var nSkipped = 0;

  // check 3: each sheet must actually change the page
  for (var n = 0; n < names.length; n++) {
    var changed = 0, cur = snaps[names[n]];
    for (var i = 0; i < els.length; i++) {
      if (cur[i] === base[i]) continue;      // identical row: nothing to split
      var x = probeSplit(cur[i]), y = probeSplit(base[i]);
      for (var j = 0; j < KEYS.length; j++) {
        if (x[j] === undefined || y[j] === undefined) { nSkipped++; continue; }
        if (x[j] !== y[j]) changed++;
      }
    }
    say("changed " + names[n] + " " + changed);
  }

  // check 4: sheets must agree with each other
  if (names.length > 1) {
    var a = snaps[names[0]], b = snaps[names[1]], diffs = [];
    var nCustom = 0, nStandard = 0;
    for (var i = 0; i < els.length; i++) {
      if (a[i] === b[i]) continue;
      var x = probeSplit(a[i]), y = probeSplit(b[i]);
      for (var j = 0; j < KEYS.length; j++) {
        if (x[j] === undefined || y[j] === undefined) { nSkipped++; continue; }
        if (x[j] === y[j]) continue;
        var p = KEYS[j], e = els[i];
        if (p.indexOf("--") === 0) nCustom++; else nStandard++;
        diffs.push("<" + e.tagName.toLowerCase()
          + (e.id ? " id=" + e.id : "")
          + (e.className && e.className.baseVal === undefined
               ? ' class="' + String(e.className).slice(0, 60) + '"' : "")
          + ">  " + p + ": " + names[0] + "=" + x[j]
          + "  " + names[1] + "=" + y[j]);
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
    """The feed snapshot to render against -- the newest by name, so a freshly
    captured Instagram_feed<n>.html is picked up without editing this."""
    feeds = [f for f in sorted(os.listdir(SNAPSHOTS))
             if f.endswith(".html")
             and (f.startswith("Instagram_feed") or f.startswith("Instagram ("))]
    return os.path.join(SNAPSHOTS, feeds[-1]) if feeds else None


def run_browser(sheets, workdir):
    snap = find_snapshot()
    if not snap:
        print(f"  x FAIL  no 'Instagram_feed*.html' snapshot found in {SNAPSHOTS}")
        return None
    declared = sorted({m for s in sheets.values()
                       for m in re.findall(r'(--[\w-]+)\s*:', s)})
    js = (PAGE_JS.replace("__CORE__", PROBE_CORE)
                 .replace("__SHEETS__", json.dumps(sheets))
                 .replace("__DECLARED__", json.dumps(declared)))
    page = os.path.join(workdir, "page.html")
    write_page(snap, "<script>" + js + "</script>", page)

    lines, err, low = run_firefox_guarded(page, workdir, timeout=300)
    if err:
        print(f"  x FAIL  {err}")
        return None
    if low is not None and low < MEM_FLOOR_MB * 2:
        print(f"  ! only {low}MB of memory to spare at the worst point "
              f"(floor is {MEM_FLOOR_MB}MB)")
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
    workdir = make_workdir("userstyle-verify-")
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
