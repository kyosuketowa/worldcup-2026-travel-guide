"""不足アトラクション画像を Wikipedia media-list から探索。"""
import sys, io, urllib.request, os, json, time
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {'User-Agent':'MorishitaTravelGuide/1.0 (contact:beat@example.com)','Accept':'application/json,image/*'}

def fetch(u):
    r = urllib.request.urlopen(urllib.request.Request(u, headers=HDRS), timeout=30)
    return r.read()

def resize_save(data, out_path, max_w=1200):
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.size[0] > max_w:
        im = im.resize((max_w, int(im.size[1]*max_w/im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=85, optimize=True)
    with open(out_path,'wb') as f: f.write(buf.getvalue())
    return len(buf.getvalue())

def best_from_media_list(title, blacklist=None, min_size=80000):
    """media-listから、ロゴ系でなく十分大きい画像を探す。"""
    blacklist = blacklist or ['logo','svg','icon','seal','map','diagram','chart']
    try:
        ml = json.loads(fetch(f'https://en.wikipedia.org/api/rest_v1/page/media-list/{title}').decode('utf-8'))
    except Exception as e:
        print(f'  !! {title}: media-list {e}')
        return None
    for item in ml.get('items', []):
        if item.get('type') != 'image': continue
        n = item.get('title','').lower()
        if any(b in n for b in blacklist): continue
        srcs = item.get('srcset') or []
        if not srcs: continue
        u = srcs[-1]['src']
        if u.startswith('//'): u = 'https:' + u
        try:
            d = fetch(u)
            if d[:3] != b'\xff\xd8\xff' and not d[:8].startswith(b'\x89PNG'): continue
            im = Image.open(io.BytesIO(d))
            w, h = im.size
            if w < 600 or h < 400:  # ロゴっぽい小画像を弾く
                continue
            return u, d
        except Exception:
            continue
    return None

TARGETS = [
    # (Wikipedia記事, 出力ファイル名)
    ("Haunted_Mansion_(Disneyland)",  'haunted-mansion.jpg'),
    ("Haunted_Mansion",               'haunted-mansion.jpg'),  # fallback
    ("It's_a_Small_World_(attraction)", 'small-world.jpg'),
    ("Star_Wars:_Galaxy's_Edge",      'rise-resistance.jpg'),
    ("Adventureland_(Disneyland)",    'indy-adventure.jpg'),
    ("Tiana's_Bayou_Adventure",       'tianas-bayou.jpg'),
    ("Cars_Land",                     'cars-land.jpg'),
    ("Pixar_Pier",                    'pixar-pier.jpg'),
    ("Main_Street,_U.S.A.",           'main-street.jpg'),
    ("Blue_Bayou_Restaurant",         'blue-bayou.jpg'),
    ("Fantasyland",                   'fantasyland.jpg'),
]

ok = 0
for title, outname in TARGETS:
    fp = os.path.join(BASE, outname)
    # サイズが十分なら既にOK
    if os.path.exists(fp) and os.path.getsize(fp) > 80000:
        print(f'  -- {outname}: already good ({os.path.getsize(fp):,}B)')
        continue
    result = best_from_media_list(title)
    if not result:
        print(f'  !! {outname}: nothing usable from {title}')
        time.sleep(1.2)
        continue
    u, data = result
    sz = resize_save(data, fp)
    print(f'  OK {outname:<22} {sz:>7,}B  <- {title}')
    ok += 1
    time.sleep(1.2)

print(f'\n=== {ok} updated ===')
