"""PDFを完全排除して残り5枚を確実に取得。"""
import sys, io, urllib.request, urllib.parse, urllib.error, os, json, time
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.5',
    'Referer': 'https://commons.wikimedia.org/',
}

def fetch(u):
    return urllib.request.urlopen(urllib.request.Request(u, headers=HDRS), timeout=40).read()

def is_img(d):
    if len(d) < 12: return False
    return d[:3]==b'\xff\xd8\xff' or d[:8].startswith(b'\x89PNG')

def save_jpeg(data, path, max_w=1400):
    im = Image.open(io.BytesIO(data)).convert('RGB')
    if im.size[0] > max_w:
        im = im.resize((max_w, int(im.size[1]*max_w/im.size[0])), Image.LANCZOS)
    buf = io.BytesIO()
    im.save(buf, format='JPEG', quality=85, optimize=True, progressive=True)
    with open(path,'wb') as f: f.write(buf.getvalue())
    return len(buf.getvalue())

def search(q, limit=40):
    qe = urllib.parse.quote(q)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch={qe}&srnamespace=6&srlimit={limit}'
    return [it.get('title','') for it in json.loads(fetch(url).decode('utf-8')).get('query',{}).get('search',[])]

def thumb(file_title, width=1400):
    q = urllib.parse.quote(file_title)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&titles={q}&prop=imageinfo&iiprop=url|mime&iiurlwidth={width}'
    d = fetch(url).decode('utf-8')
    for _, p in json.loads(d).get('query',{}).get('pages',{}).items():
        ii = p.get('imageinfo', [])
        if ii:
            mime = ii[0].get('mime','')
            if not mime.startswith('image/'): return None
            return ii[0].get('thumburl') or ii[0].get('url')
    return None

# 画像ファイル拡張子を最初に判定
def is_image_file(name):
    low = name.lower()
    return low.endswith(('.jpg','.jpeg','.png','.gif'))

AVOID = ['logo','poster','svg','diagram','plan','postcard','ticket','emblem','coat_of_arms','movie_poster']

JOBS = [
    ('cars-land.jpg',         ['Radiator Springs Racers Cars Land','Cars Land']),
    ('pirates-caribbean.jpg', ['Pirates Caribbean attraction queue','Pirates Caribbean boat Disneyland']),
    ('tianas-bayou.jpg',      ['Splash Mountain Disneyland','Splash Mountain Exterior']),
    ('mickey-mouse.jpg',      ['Mickey Mouse character parade','Mickey Mouse Disneyland character']),
    ('fireworks.jpg',         ['Disneyland Forever fireworks','Sleeping Beauty Castle fireworks']),
]

ok = fail = 0
for outname, queries in JOBS:
    print(f'\n[[{outname}]]')
    found = None
    for q in queries:
        time.sleep(1.5)
        print(f'  🔎 {q}')
        try:
            names = search(q)
        except Exception as e:
            print(f'    ERR search: {e}')
            continue
        # JPG/PNG のみ残す
        img_names = [n for n in names if is_image_file(n)]
        # 避けるワードを含むものを除外
        img_names = [n for n in img_names if not any(a in n.lower() for a in AVOID)]
        print(f'    image files: {len(img_names)}/{len(names)}')
        for fn in img_names[:20]:
            time.sleep(0.6)
            try:
                u = thumb(fn)
                if not u:
                    print(f'      [nourl] {fn[:50]}')
                    continue
                d = fetch(u)
                if not is_img(d):
                    print(f'      [noimg] {fn[:50]}')
                    continue
                im = Image.open(io.BytesIO(d))
                if max(im.size) < 800 or len(d) < 60*1024:
                    print(f'      [small size={im.size} bytes={len(d)}] {fn[:40]}')
                    continue
                found = (u, d, fn)
                print(f'    ✅ {fn[:75]}')
                break
            except Exception as e:
                print(f'      [ERR {type(e).__name__}] {fn[:40]}: {str(e)[:60]}')
                continue
        if found: break
    if not found:
        print(f'  ❌ 失敗')
        fail += 1
        continue
    u, d, fn = found
    sz = save_jpeg(d, os.path.join(BASE, outname))
    print(f'  💾 {sz:,}B')
    ok += 1
    time.sleep(1.2)

print(f'\n=== {ok}/{len(JOBS)} ===')
