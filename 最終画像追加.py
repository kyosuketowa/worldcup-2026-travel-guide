"""Walk of Fame（猫になってる）と残りDisney画像を実写化。"""
import sys, io, urllib.request, urllib.parse, urllib.error, os, json, time
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'text/html,image/*',
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

def search(q, limit=30):
    qe = urllib.parse.quote(q)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch={qe}&srnamespace=6&srlimit={limit}'
    return [it.get('title','') for it in json.loads(fetch(url).decode('utf-8')).get('query',{}).get('search',[])]

def thumb(fn):
    q = urllib.parse.quote(fn)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&titles={q}&prop=imageinfo&iiprop=url|mime&iiurlwidth=1400'
    d = fetch(url).decode('utf-8')
    for _, p in json.loads(d).get('query',{}).get('pages',{}).items():
        ii = p.get('imageinfo', [])
        if ii and ii[0].get('mime','').startswith('image/'):
            return ii[0].get('thumburl') or ii[0].get('url')
    return None

def is_image_file(name):
    return name.lower().endswith(('.jpg','.jpeg','.png'))

AVOID = ['logo','poster','svg','diagram','plan','postcard','ticket','emblem','coat_of_arms']

JOBS = [
    ('walk-of-fame.jpg',     ['Hollywood Walk of Fame star Disney','Hollywood Walk of Fame','Hollywood Boulevard star sidewalk']),
    ('pixar-pier.jpg',       ['Pixar Pal-A-Round ferris wheel','Mickey Fun Wheel Disneyland','Paradise Pier ferris wheel']),
    ('guardians-breakout.jpg',['Guardians of the Galaxy Mission Breakout Disneyland','Tower of Terror Disney California']),
    ('web-slingers.jpg',     ['Avengers Campus Disneyland','WEB SLINGERS Spider Man']),
    ('pirates-lair.jpg',     ['Tom Sawyer Island Disneyland','Pirates Lair Disneyland']),
    ('animation-building.jpg',['Disney Animation Building','Disney Hollywood Land','Turtle Talk with Crush']),
]

ok = fail = 0
for outname, queries in JOBS:
    print(f'\n[[{outname}]]', flush=True)
    found = None
    for q in queries:
        time.sleep(1.5)
        print(f'  🔎 {q}', flush=True)
        try:
            names = search(q)
        except Exception as e:
            print(f'    ERR search: {e}', flush=True)
            continue
        img_names = [n for n in names if is_image_file(n) and not any(a in n.lower() for a in AVOID)]
        print(f'    候補 {len(img_names)}件', flush=True)
        for fn in img_names[:15]:
            time.sleep(0.6)
            try:
                u = thumb(fn)
                if not u: continue
                d = fetch(u)
                if not is_img(d): continue
                im = Image.open(io.BytesIO(d))
                if max(im.size) < 800 or len(d) < 60*1024: continue
                found = (u, d, fn)
                print(f'    ✅ {fn[:70]}', flush=True)
                break
            except Exception:
                continue
        if found: break
    if not found:
        print(f'  ❌ 失敗', flush=True)
        fail += 1
        continue
    u, d, fn = found
    sz = save_jpeg(d, os.path.join(BASE, outname))
    print(f'  💾 {sz:,}B', flush=True)
    ok += 1
    time.sleep(1.0)

print(f'\n=== {ok}/{len(JOBS)} ===', flush=True)
