#!/usr/bin/env python3
import json
import re
from pathlib import Path
from shutil import copy2
import difflib

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / 'shim_removal_preview.json'
OUT_LIMIT = 10

import sys


def load_preview_text():
    with PREVIEW.open('r', encoding='utf-8', errors='ignore') as f:
        return f.read()

def extract_all_candidates_from_text(text):
    pairs = []
    seen = set()
    for fm in re.finditer(r'"file"\s*:\s*"([^"]+\.css)"', text):
        filev = fm.group(1)
        if filev in seen:
            continue
        seen.add(filev)
        css_path = ROOT / 'css' / filev
        if not css_path.exists():
            css_path = ROOT / filev
        shim_id = None
        if css_path.exists():
            ctext = css_path.read_text(encoding='utf-8', errors='ignore')
            m1 = re.search(r'#pu(\d+)', ctext)
            if m1:
                shim_id = 'u' + m1.group(1)
            else:
                m2 = re.search(r'#u(\d+)', ctext)
                if m2:
                    shim_id = 'u' + m2.group(1)
        html = filev.replace('.css', '.html')
        pairs.append((shim_id, html))
    return pairs

def bump_css_versions(text):
    # increment numeric ?v=N params
    def inc(m):
        num = m.group(1)
        try:
            n = int(num) + 1
        except Exception:
            n = 1
        return f'?v={n}'
    # replace ?v=number
    text = re.sub(r"\?v=(\d+)", lambda m: inc(m), text)
    # append ?v=1 to css links without a query
    text = re.sub(r'(href\s*=\s*"[^"]+\.css)(")', lambda m: m.group(1)+m.group(2) if '?v=' in m.group(1) else m.group(1)+'?v=1'+m.group(2), text)
    return text

def insert_shim_hide(text, shim_id):
    style = '\n<!-- shim-hide inserted by script -->\n<style>#{id}, #{id}-bw {{display:none !important; height:0 !important; margin:0 !important; padding:0 !important;}}</style>\n'.format(id=shim_id)
    if re.search(r'</head>', text, flags=re.I):
        return re.sub(r'(</head>)', style + r'\1', text, count=1, flags=re.I)
    else:
        # fall back to prepending
        return style + text

def process(candidate):
    shim_id, html_rel = candidate
    html_path = ROOT / html_rel
    if not html_path.exists():
        print(f"SKIP (missing): {html_rel}")
        return False
    bak = html_path.with_suffix(html_path.suffix + '.bak')
    if not bak.exists():
        copy2(html_path, bak)
    orig = html_path.read_text(encoding='utf-8', errors='ignore')
    # if shim_id is None, try to detect from the HTML or CSS in the page
    if not shim_id:
        m = re.search(r'id\s*=\s*"(u\d+)"', orig)
        if m:
            shim_id = m.group(1)
        else:
            m2 = re.search(r'id\s*=\s*"(pu\d+)"', orig)
            if m2:
                shim_id = m2.group(1).lstrip('p')
    if not shim_id:
        print(f"SKIP (no shim id found): {html_rel}")
        return False
    mod = bump_css_versions(orig)
    mod = insert_shim_hide(mod, shim_id)
    if orig == mod:
        print(f"NOCHANGE: {html_rel}")
        return True
    # write modified
    html_path.write_text(mod, encoding='utf-8')
    # print unified diff
    diff = difflib.unified_diff(orig.splitlines(), mod.splitlines(), fromfile=str(bak.name), tofile=str(html_path.name), lineterm='')
    print('\n'.join(list(diff)))
    return True

def main():
    if not PREVIEW.exists():
        print('shim_removal_preview.json not found')
        return
    # parse optional arguments
    start = 0
    do_all = False
    for i,arg in enumerate(sys.argv[1:], start=1):
        if arg.startswith('--start='):
            try:
                start = int(arg.split('=',1)[1])
            except Exception:
                start = 0
        if arg == '--all':
            do_all = True
    text = load_preview_text()
    all_cands = extract_all_candidates_from_text(text)
    if do_all:
        candidates = all_cands
        print(f"Processing all {len(candidates)} candidates")
    else:
        candidates = all_cands[start:start+OUT_LIMIT]
        print(f"Processing {len(candidates)} candidates (start={start})")
    for c in candidates:
        process(c)

if __name__ == '__main__':
    main()
