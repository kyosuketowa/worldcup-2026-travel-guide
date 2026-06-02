"""残りの5枚（cars-land, pirates-caribbean, tianas-bayou, mickey-mouse, fireworks）を確実に取得。"""
import sys, io, urllib.request, urllib.parse, os, json, time
from PIL import Image
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', line_buffering=True)

BASE = r'C:/Users/kyosu/worldカップ旅行/images'
HDRS = {'User-Agent':'MorishitaTravelGuide/1.0 (contact:beat@example.com) Python','Accept':'application/json,image/*'}

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

def search(query, limit=30):
    q = urllib.parse.quote(query)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&list=search&srsearch={q}&srnamespace=6&srlimit={limit}'
    d = fetch(url).decode('utf-8')
    return [it.get('title','') for it in json.loads(d).get('query',{}).get('search',[])]

def thumb(file_title, width=1400):
    q = urllib.parse.quote(file_title)
    url = f'https://commons.wikimedia.org/w/api.php?action=query&format=json&titles={q}&prop=imageinfo&iiprop=url|mime&iiurlwidth={width}'
    d = fetch(url).decode('utf-8')
    for _, p in json.loads(d).get('query',{}).get('pages',{}).items():
        ii = p.get('imageinfo', [])
        if ii:
            mime = ii[0].get('mime','')
            if 'pdf' in mime or 'video' in mime:
                return None
            return ii[0].get('thumburl') or ii[0].get('url')
    return None

AVOID = ['logo','poster','svg','diagram','plan','postcard','ticket','emblem','coat_of_arms',
         'map.jpg','map.png','.pdf','.ogv','.webm','project_blue','record_card','report']

JOBS = [
    ('cars-land.jpg',         [
        'Cars Land night Disneyland',
        'Cars Land Radiator Springs Racers',
        'Carsland Anaheim',
        'Disney California Adventure Cars Land',
    ]),
    ('pirates-caribbean.jpg', [
        'Pirates of the Caribbean attraction Disneyland boat',
        'New Orleans Square attraction',
        'Disneyland Pirates Caribbean facade',
    ]),
    ('tianas-bayou.jpg',      [
        'Splash Mountain Disneyland',
        'Disneyland Critter Country',
        'Tiana Bayou Adventure',
    ]),
    ('mickey-mouse.jpg',      [
        'Mickey Mouse character Disney',
        'Disneyland Main Street Mickey Mouse character',
        'Mickey Mouse parade Magic Kingdom',
    ]),
    ('fireworks.jpg',         [
        'Disneyland Forever castle fireworks',
        'Sleeping Beauty Castle night fireworks',
        'Wondrous Journeys Disneyland',
        'Disneyland fireworks castle',
    ]),
]

ok = fail = 0
for outname, queries in JOBS:
    print(f'\n[[{outname}]]')
    found = None
    for q in queries:
        print(f'  query: {q}')
        time.sleep(1.5)  # レート制限対策
        try:
            names = search(q)
        except Exception as e:
            print(f'    search ERR: {e}')
            continue
        print(f'    hits={len(names)}')
        for fn in names:
            low = fn.lower()
            if any(a in low for a in AVOID): continue
            if '.pdf' in low or '.ogv' in low or '.webm' in low: continue
            time.sleep(0.6)
            try:
                u = thumb(fn)
                if not u:
                    continue
                d = fetch(u)
                if not is_img(d): continue
                im = Image.open(io.BytesIO(d))
                if im.size[0] < 600 or len(d) < 80*1024: continue
                found = (u, d, fn)
                print(f'    ✅ {fn[:70]}')
                break
            except Exception:
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
    time.sleep(1.0)

print(f'\n=== {ok}/{len(JOBS)} 成功 ===')
