#!/usr/bin/env python3
"""Join hard-wrapped markdown paragraphs into one line each.

Left verbatim: fenced code blocks, table rows, headings, blank lines.
Joined: paragraph runs and list items (with their continuation lines).
"""
import re
import sys

FENCE = re.compile(r'^\s*(```|~~~)')
HEAD = re.compile(r'^#{1,6} ')
TABLE = re.compile(r'^\s*\|')
BULLET = re.compile(r'^(\s*)[-*+] ')


def _starts_block(line):
    return bool(FENCE.match(line) or HEAD.match(line)
                or TABLE.match(line) or BULLET.match(line))


def unwrap(text):
    lines = text.split('\n')
    out = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]

        if FENCE.match(line):
            out.append(line)
            i += 1
            while i < n:                      # copy through the closing fence
                out.append(lines[i])
                closed = FENCE.match(lines[i])
                i += 1
                if closed:
                    break
            continue

        if not line.strip() or HEAD.match(line) or TABLE.match(line):
            out.append(line)
            i += 1
            continue

        buf = [line.rstrip()]                 # paragraph or list item
        i += 1
        while i < n:
            nxt = lines[i]
            if not nxt.strip() or _starts_block(nxt):
                break
            buf.append(nxt.strip())
            i += 1
        out.append(' '.join(buf))

    return '\n'.join(out)


def blocks(text):
    """Canonical block structure, for comparing before against after."""
    lines = text.split('\n')
    out = []
    i, n = 0, len(lines)
    while i < n:
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        if FENCE.match(line):
            buf = [line.strip()]
            i += 1
            while i < n:
                buf.append(lines[i].strip())
                closed = FENCE.match(lines[i])
                i += 1
                if closed:
                    break
            out.append(('fence', 0, '\n'.join(buf)))
            continue

        indent = len(line) - len(line.lstrip())
        if HEAD.match(line):
            out.append(('head', indent, ' '.join(line.split())))
            i += 1
            continue
        if TABLE.match(line):
            out.append(('table', indent, ' '.join(line.split())))
            i += 1
            continue

        kind = 'bullet' if BULLET.match(line) else 'para'
        buf = [line.strip()]
        i += 1
        while i < n:
            nxt = lines[i]
            if not nxt.strip() or _starts_block(nxt):
                break
            buf.append(nxt.strip())
            i += 1
        out.append((kind, indent, ' '.join(buf)))
    return out


if __name__ == '__main__':
    path = sys.argv[1]
    write = '--write' in sys.argv

    original = open(path, encoding='utf-8').read()
    result = unwrap(original)

    ok = True

    stripped_before = re.sub(r'\s+', '', original)
    stripped_after = re.sub(r'\s+', '', result)
    if stripped_before == stripped_after:
        print('  + content identical with all whitespace removed '
              f'({len(stripped_before)} chars)')
    else:
        ok = False
        print('  ! CONTENT CHANGED')
        for a, b in zip(stripped_before, stripped_after):
            if a != b:
                at = stripped_before.index(a)
                print(f'      first difference near: {stripped_before[at-60:at+60]!r}')
                break

    before, after = blocks(original), blocks(result)
    if before == after:
        print(f'  + block structure identical ({len(before)} blocks)')
    else:
        ok = False
        print(f'  ! STRUCTURE CHANGED: {len(before)} blocks -> {len(after)}')
        for x, y in zip(before, after):
            if x != y:
                print(f'      before: {x}\n      after:  {y}')
                break

    kinds = {}
    for k, _, _ in before:
        kinds[k] = kinds.get(k, 0) + 1
    print(f'  . blocks by kind: {kinds}')

    wrapped = [ln for ln in result.split('\n')
               if len(ln) > 100 and not TABLE.match(ln)]
    print(f'  . lines over 100 chars (expected, these are the joined ones): '
          f'{len(wrapped)}')
    print(f'  . {len(original.splitlines())} lines -> {len(result.splitlines())}')

    if write and ok:
        open(path, 'w', encoding='utf-8').write(result)
        print(f'  + wrote {path}')
    elif write:
        print('  ! refusing to write, checks failed')
        sys.exit(1)
    sys.exit(0 if ok else 1)
