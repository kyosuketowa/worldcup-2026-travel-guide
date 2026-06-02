"""Logo化した3枚を別ソース（Pexels + Wikipedia media-list）で差し替え。"""
import sys, io, urllib.request, os, json, time
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {
    'User-Agent': 'MorishitaTravelGuide/1.0 (contact: beat.kyosuke.0226@gmail.com)',
    'Accept': 'application/json,image/*',
}

def fetch(url):
    r = urllib.request.urlopen(urllib.request.Request(url, headers=HDRS), timeout=30)
    return r.read(), r.headers.get('Content-Type','')

def is_img(data):
    if len(data) < 12: return False
    if data[:3] == b'\xff\xd8\xff': return True
    if data[:8].startswith(b'\x89PNG'): return True
    if data[:4] == b'RIFF' and data[8:12] == b'WEBP': return True
    return False

def resize_save(data, out_path, max_w=1600):
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.size[0] > max_w:
        h = int(im.size[1] * max_w / im.size[0])
        im = im.resize((max_w, h), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=85, optimize=True, progressive=True)
    with open(out_path, 'wb') as f:
        f.write(buf.getvalue())
    return len(buf.getvalue())

# Pexels 直リンク（商用可）
PEXELS = {
    'in-n-out.jpg':    'https://images.pexels.com/photos/1251208/pexels-photo-1251208.jpeg?auto=compress&cs=tinysrgb&w=1600',
    'walk-of-fame.jpg':'https://images.pexels.com/photos/2166817/pexels-photo-2166817.jpeg?auto=compress&cs=tinysrgb&w=1600',
}

print('--- Pexels で置換 ---')
for name, url in PEXELS.items():
    fp = os.path.join(BASE, name)
    try:
        data, ct = fetch(url)
        if not is_img(data):
            print(f'  !! {name}: non-image')
            continue
        sz = resize_save(data, fp)
        print(f'  OK {name:<24} {sz:>7,}B')
        time.sleep(0.6)
    except Exception as e:
        print(f'  !! {name}: {e}')

# Wikipedia media-list から Old St Patrick's 取得
print('\n--- media-list で Old St Patrick\'s + Strawberry Fields ---')
def media_list_pick(title, blacklist=None):
    blacklist = blacklist or ['logo','svg','icon','seal','map','diagram']
    ml = json.loads(fetch(f'https://en.wikipedia.org/api/rest_v1/page/media-list/{title}')[0].decode('utf-8'))
    for item in ml.get('items', []):
        if item.get('type') != 'image': continue
        n = item.get('title','').lower()
        if any(b in n for b in blacklist): continue
        srcs = item.get('srcset') or []
        if srcs:
            u = srcs[-1]['src']
            return ('https:' + u) if u.startswith('//') else u
    return None

for title, outname in [
    ("Old_St._Patrick's_Cathedral", 'old-st-patricks.jpg'),
    ('Strawberry_Fields_(memorial)', 'strawberry-fields.jpg'),  # IMAGINE モザイクを狙う
]:
    fp = os.path.join(BASE, outname)
    try:
        # 特に Strawberry Fields は "Imagine" を含むファイルを優先
        ml = json.loads(fetch(f'https://en.wikipedia.org/api/rest_v1/page/media-list/{title}')[0].decode('utf-8'))
        picked = None
        # IMAGINE 優先
        for item in ml.get('items', []):
            if item.get('type') != 'image': continue
            n = item.get('title','').lower()
            if 'imagine' in n or 'mosaic' in n:
                srcs = item.get('srcset') or []
                if srcs:
                    u = srcs[-1]['src']
                    picked = ('https:' + u) if u.startswith('//') else u
                    break
        if not picked:
            picked = media_list_pick(title)

        if not picked:
            print(f'  !! {outname}: no image')
            continue
        data, ct = fetch(picked)
        if not is_img(data):
            print(f'  !! {outname}: non-image')
            continue
        sz = resize_save(data, fp)
        print(f'  OK {outname:<24} {sz:>7,}B  <- {picked[-50:]}')
        time.sleep(1.2)
    except Exception as e:
        print(f'  !! {outname}: {e}')
