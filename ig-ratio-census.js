/* Instagram media-ratio census -- paste into Firefox's console on instagram.com.
   Reads each media element's INTRINSIC dimensions, so it reports the true
   aspect ratio even where Instagram's inline padding-bottom box is clamped.
   IGR.help() lists the commands. */
(() => {
  const KNOWN = [
    ['1.91:1', 1.91], ['16:9', 16/9], ['3:2', 3/2], ['4:3', 4/3], ['5:4', 5/4],
    ['1:1', 1], ['4:5', 4/5], ['3:4', 3/4], ['2:3', 2/3], ['9:16', 9/16],
  ];
  const NEAR = 0.03;   // widest gap between neighbours is 6.7%, so 3% is unambiguous
  const EXACT = 0.005; // inside this, call it the ratio; outside, mark it "~"

  const label = (r) => {
    let best = '?', err = Infinity;
    for (const [n, v] of KNOWN) {
      const e = Math.abs(r - v) / v;
      if (e < err) { err = e; best = n; }
    }
    if (err <= EXACT) return best;
    if (err <= NEAR) return '~' + best;
    return 'other ' + r.toFixed(4);
  };

  const store = window.__IGR || (window.__IGR = new Map());

  // Grid and "more posts" thumbnails sit inside a link to their own post.
  // Feed media sits inside an <article>; post-page media inside neither.
  const surface = (el) => {
    if (el.closest('article')) return 'feed';
    return el.closest('a[href*="/p/"], a[href*="/reel/"], a[href*="/reels/"]') ? 'thumb' : 'post';
  };

  const postOf = (el) => {
    const a = el.closest('a[href*="/p/"], a[href*="/reel/"], a[href*="/reels/"]');
    const scope = el.closest('article');
    const href = (a && a.getAttribute('href'))
      || (scope && (scope.querySelector('a[href*="/p/"], a[href*="/reel/"], a[href*="/reels/"]') || {}).getAttribute
          && scope.querySelector('a[href*="/p/"], a[href*="/reel/"], a[href*="/reels/"]').getAttribute('href'))
      || location.pathname;
    return (href.match(/\/(?:p|reel|reels)\/[^/?]+/) || [href])[0];
  };

  // The inline padding-bottom box Instagram writes, and the --x-maxWidth token
  // the post-page rules key on.
  const boxOf = (el) => {
    let n = el.parentElement, pad = null, depth = 0, token = false;
    for (let i = 1; n && i <= 12; i++, n = n.parentElement) {
      const s = n.getAttribute && n.getAttribute('style');
      if (!s) continue;
      if (pad === null) {
        const m = s.match(/padding-bottom:\s*([\d.]+%)/);
        if (m) { pad = m[1]; depth = i; }
      }
      if (s.includes('--x-maxWidth')) token = true;
    }
    return { pad, depth, token };
  };

  // Elements found before their dimensions were available. A <video> reports
  // 0x0 until metadata arrives, so dropping those silently would under-count
  // reels. They are watched instead, and counted so the shortfall is visible.
  const pending = window.__IGRW || (window.__IGRW = new Set());

  // Instagram serves post media from scontent*.cdninstagram.com / fbcdn.net;
  // UI sprites come from the same hosts under /rsrc.php/. A GIF data: URI is a
  // placeholder (SingleFile writes those when it cannot inline an image).
  const isMedia = (src) => {
    if (!src) return true;                                  // srcless <video>: judge by dimensions
    if (src.startsWith('blob:')) return true;
    if (src.includes('/rsrc.php/')) return false;
    if (src.startsWith('data:')) return /^data:image\/(jpeg|jpg|png|webp|avif)/.test(src);
    return /(?:cdninstagram\.com|fbcdn\.net)/.test(src);
  };

  function consider(el) {
    const isVideo = el.tagName === 'VIDEO';
    const w = isVideo ? el.videoWidth : el.naturalWidth;
    const h = isVideo ? el.videoHeight : el.naturalHeight;

    if (!w || !h) {
      if (!el.__igrWatched) {
        el.__igrWatched = true;
        pending.add(el);
        const done = () => { pending.delete(el); consider(el); };
        el.addEventListener(isVideo ? 'loadedmetadata' : 'load', done, { once: true });
        el.addEventListener('error', () => pending.delete(el), { once: true });
      }
      return 'pending';
    }
    pending.delete(el);

    const src = (el.currentSrc || el.src || '').split('?')[0];
    const skip = (why) => { el.__igrSkip = why; return 'skip'; };
    if (/profile picture|user avatar/i.test(el.alt || '')) return skip('avatar');
    if (w === h && w <= 320) return skip('avatar');
    if (w < 150 || h < 150) return skip('too small');
    if (!isMedia(src)) return skip('not post media');
    delete el.__igrSkip;
    const post = postOf(el);
    const key = isVideo ? `v|${post}|${w}x${h}` : `i|${src || post + w + h}`;
    if (store.has(key)) return 'dup';

    const b = boxOf(el);
    store.set(key, {
      ratio: label(w / h), exact: +(w / h).toFixed(4), px: `${w}x${h}`,
      kind: isVideo ? 'video' : 'photo', on: surface(el),
      boxPad: b.pad || '', boxDepth: b.depth || '',
      // Does the box describe THIS media, or just the container it sits in?
      // A grid/tray cell crops with object-fit, and the feed clamps portrait
      // video to 125%, so a mismatch is normal and worth seeing.
      boxFits: b.pad ? (Math.abs(parseFloat(b.pad) - 100 * h / w) / (100 * h / w) <= 0.03) : null,
      token: b.token,
      dialog: !!el.closest('[role="dialog"]'), post,
    });
    return 'added';
  }

  function scan() {
    let added = 0;
    for (const el of document.querySelectorAll('img, video')) {
      if (consider(el) === 'added') added++;
    }
    return added;
  }

  const skipNote = () => {
    const tally = {};
    for (const el of document.querySelectorAll('img, video')) {
      if (el.__igrSkip) tally[el.__igrSkip] = (tally[el.__igrSkip] || 0) + 1;
    }
    const parts = Object.entries(tally).map(([k, v]) => `${v} ${k}`);
    return parts.length ? parts.join(', ') : '';
  };

  const pendingNote = () => {
    const live = [...pending].filter(el => el.isConnected);
    const v = live.filter(el => el.tagName === 'VIDEO').length;
    return live.length
      ? `${live.length} element(s) still without dimensions (${v} video, ${live.length - v} image)`
      : '';
  };

  function report() {
    const rows = [...store.values()];
    if (!rows.length) {
      const p0 = pendingNote();
      console.log('nothing collected yet -- run IGR.auto()'
                  + (p0 ? `; ${p0}. A <video> reports 0x0 until its metadata loads -- `
                        + `scroll it into view so it autoplays, then IGR.scan() again.` : ''));
      return { total: 0, posts: 0, twoThirds: [], near: [], pending: p0, excluded: skipNote() };
    }

    const groups = new Map();
    for (const r of rows) {
      const k = r.ratio.replace(/^~/, '');
      const g = groups.get(k) || { ratio: k, n: 0, exact: 0, approx: 0, photos: 0, videos: 0,
                                   main: 0, thumbs: 0, boxes: new Set(), boxMismatch: 0, example: '' };
      g.n++;
      r.ratio[0] === '~' ? g.approx++ : g.exact++;
      r.kind === 'video' ? g.videos++ : g.photos++;
      r.on === 'thumb' ? g.thumbs++ : g.main++;
      if (r.boxPad) { g.boxes.add(r.boxPad); if (r.boxFits === false) g.boxMismatch++; }
      if (!g.example) g.example = `${r.px} ${r.post}`;
      groups.set(k, g);
    }

    console.table([...groups.values()].sort((a, b) => b.n - a.n).map(g => ({
      ratio: g.ratio, count: g.n, 'exact': g.exact, 'approx': g.approx,
      photos: g.photos, videos: g.videos, 'main media': g.main, thumbnails: g.thumbs,
      'inline padding-bottom': [...g.boxes].sort().join(' ') || '(none)',
      "box != media": g.boxMismatch,
      example: g.example,
    })));

    const hit = rows.filter(r => r.ratio.replace(/^~/, '') === '2:3');
    const posts = new Set(rows.map(r => r.post)).size;
    console.log(
      `%c2:3 media: ${hit.length ? 'FOUND -- ' + hit.length + ' item(s)' : 'none'}` +
      `   [${rows.length} media across ${posts} posts]`,
      `font-weight:bold;font-size:13px;color:${hit.length ? '#e1306c' : '#777'}`);
    if (hit.length) console.table(hit);

    const near = rows.filter(r => r.ratio.replace(/^~/, '') !== '2:3'
                                  && Math.abs(r.exact - 2/3) / (2/3) <= 0.06);
    if (near.length) { console.log('within 6% of 2:3 but classed elsewhere:'); console.table(near); }
    const sk = skipNote();
    if (sk) console.log(`excluded on this page: ${sk}`);
    const p = pendingNote();
    if (p) console.log(`%cwaiting: ${p}. A <video> reports 0x0 until its metadata loads -- `
                     + `scroll it into view so it autoplays, then IGR.scan() again.`,
                       'color:#c47f00');
    console.log('note: a thumbnail is the grid/"more posts" image. Instagram usually serves those '
              + 'uncropped, so their ratio is real -- but a square-cropped thumbnail reads as 1:1, '
              + 'so trust "main media" counts over "thumbnails" for negative results.');
    return { total: rows.length, posts, twoThirds: hit, near, pending: pendingNote(), excluded: skipNote() };
  }

  let timer = null;
  function auto(rounds = 40, waitMs = 1200) {
    if (timer) clearInterval(timer);
    let quiet = 0, i = 0;
    console.log(`scrolling + scanning: up to ${rounds} rounds, stopping after 5 quiet ones`);
    timer = setInterval(() => {
      const n = scan();
      quiet = n ? 0 : quiet + 1;
      if (n) console.log(`round ${i}: +${n} (total ${store.size})`);
      scrollBy(0, innerHeight * 0.9);
      if (++i >= rounds || quiet >= 5) { clearInterval(timer); timer = null; report(); }
    }, waitMs);
    return 'running -- IGR.stop() aborts';
  }

  window.IGR = {
    scan: () => { const n = scan(); const p = pendingNote();
                  console.log(`+${n} new (total ${store.size})` + (p ? ` -- ${p}` : ''));
                  return n; },
    report, auto,
    rows: () => [...store.values()],
    boxes: (ratio) => {
      const want = String(ratio || '').replace(/^~/, '');
      const rows = [...store.values()]
        .filter(r => !want || r.ratio.replace(/^~/, '') === want)
        .map(r => ({ ratio: r.ratio, px: r.px, kind: r.kind, on: r.on,
                     box: r.boxPad || '(none)', depth: r.boxDepth,
                     'box describes media': r.boxFits, post: r.post }))
        .sort((a, b) => String(a.box).localeCompare(String(b.box)));
      console.table(rows);
      return rows;
    },
    csv: () => { const r = [...store.values()]; const k = Object.keys(r[0] || {});
                 return [k.join(','), ...r.map(o => k.map(x => o[x]).join(','))].join('\n'); },
    reset: () => { store.clear(); return 'cleared'; },
    stop: () => { if (timer) clearInterval(timer); timer = null; return 'stopped'; },
    help: () => console.log([
      'IGR.auto()    scroll, scan as it goes, then report   <- start here',
      'IGR.scan()    scan what is rendered right now',
      'IGR.report()  ratio table + the 2:3 verdict',
      'IGR.boxes("9:16")  per-item boxes for one ratio -- the grouped column',
      '                   is a UNION over the group, so use this to see which',
      '                   item contributed which padding-bottom',
      'IGR.rows()    raw records        IGR.csv()   same as CSV',
      'IGR.reset()   forget everything  IGR.stop()  abort auto()',
      'the store survives IGR being re-pasted, so you can keep adding pages',
    ].join('\n')),
  };

  scan();
  IGR.help();
  console.log(`%cready -- ${store.size} media already visible. Run IGR.auto()`, 'font-weight:bold');
})();
