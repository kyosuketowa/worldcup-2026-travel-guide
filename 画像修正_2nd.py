"""media-list APIから画像候補を取得し、サムネイルっぽい写真を優先して保存。"""
import urllib.request, os, json, time, io
from PIL import Image

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {
    'User-Agent': 'MorishitaTravelGuide/1.0 (contact: beat.kyosuke.0226@gmail.com)',
    'Accept': 'application/json,image/*',
}

# (Wikipedia英語記事名, 保存ファイル名, 避けたい名前パターン)
JOBS = [
    ('Griffith_Observatory', 'griffith.jpg', ['logo', 'seal', 'icon', 'svg']),
    ('Roller_coaster',       'roller-coaster.jpg', ['logo', 'svg', 'map']),
    ('Palm_tree',            'la-palms.jpg', ['logo', 'svg', 'map', 'diagram']),
]

def fetch_json(url):
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode('utf-8'))

def fetch_binary(url):
    req = urllib.request.Request(url, headers=HDRS)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read(), r.headers.get('Content-Type', '')

def is_jpeg(data):
    return len(data) >= 3 and data[:3] == b'\xff\xd8\xff'

def is_png(data):
    return len(data) >= 8 and data[:8].startswith(b'\x89PNG')

for title, outname, blacklist in JOBS:
    try:
        ml = fetch_json(f'https://en.wikipedia.org/api/rest_v1/page/media-list/{title}')
        picked = None
        for item in ml.get('items', []):
            if item.get('type') != 'image':
                continue
            name = item.get('title', '').lower()
            if any(b in name for b in blacklist):
                continue
            # Prefer srcset largest
            srcs = item.get('srcset') or []
            if srcs:
                picked = ('https:' + srcs[-1]['src']) if srcs[-1]['src'].startswith('//') else srcs[-1]['src']
                print(f'  picked for {title}: {name} -> {picked[:80]}')
                break
        if not picked:
            print(f'  !! {title}: no suitable image in media-list')
            continue
        data, ct = fetch_binary(picked)
        if not (is_jpeg(data) or is_png(data)):
            print(f'  !! {outname}: non-image ct={ct}')
            continue
        # Convert & resize through PIL to enforce JPEG 1600px Q85
        with Image.open(io.BytesIO(data)) as im:
            im = im.convert('RGB')
            w, h = im.size
            if w > 1600:
                nh = int(h * 1600 / w)
                im = im.resize((1600, nh), Image.LANCZOS)
            out = io.BytesIO()
            im.save(out, format='JPEG', quality=85, optimize=True, progressive=True)
            final = out.getvalue()
        fp = os.path.join(BASE, outname)
        with open(fp, 'wb') as f:
            f.write(final)
        print(f'  OK {outname}: {len(final):,}B')
        time.sleep(1.5)
    except Exception as e:
        print(f'  !! {title}: {e}')
        time.sleep(1.5)
